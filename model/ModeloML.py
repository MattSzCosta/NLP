from __future__ import unicode_literals, print_function
import os
import spacy
from spacy.util import minibatch, compounding
import random
from pathlib import Path


class modeloML:
    def __init__(self, numTreino=100, dadosDeTreino=None,output_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)), '../treinamentos/treinamento1'),model=None):
        self.numTreino = numTreino
        self.dadosDeTreino = dadosDeTreino
        self.output_dir = output_dir
        self.model = model


    def treinar(self):
        nlp = self.loadModel()
        self.pipeline(nlp)
        self.getEntities(self.dadosDeTreino)

    def getEntities(self,val):
        print("Loading from", self.output_dir)
        nlp2 = spacy.load(self.output_dir)
        for text, _ in val:
            doc = nlp2(text)
            print("Entities", [(ent.text, ent.label_) for ent in doc.ents])
            print("Tokens", [(t.text, t.ent_type_, t.ent_iob) for t in doc])

    def loadModel(self):
        """Load the model, set up the pipeline and train the entity recognizer."""
        if self.model is not None:
            nlp = spacy.load(self.model)  # load existing spaCy model
            print("Loaded model '%s'" % self.model)
        else:
            nlp = spacy.blank("en")  # create blank Language class
            print("Created blank 'en' model")
        return nlp

    def saveModel(self,nlp):
        # save model to output directory
        if self.output_dir is not None:
            output_dir = Path(self.output_dir)
            if not output_dir.exists():
                output_dir.mkdir()
            nlp.to_disk(output_dir)
            print("Saved model to", output_dir)

    def pipeline(self,nlp):
        # create the built-in pipeline components and add them to the pipeline
        # nlp.create_pipe works for built-ins that are registered with spaCy
        if "ner" not in nlp.pipe_names:
            ner = nlp.create_pipe("ner")
            nlp.add_pipe(ner, last=True)
        # otherwise, get it so we can add labels
        else:
            ner = nlp.get_pipe("ner")

        # add labels
        for _, annotations in self.dadosDeTreino:
            for ent in annotations.get("entities"):
                ner.add_label(ent[2])

        # get names of other pipes to disable them during training
        other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
        with nlp.disable_pipes(*other_pipes):  # only train NER
            # reset and initialize the weights randomly – but only if we're
            # training a new model
            if self.model is None:
                nlp.begin_training()
            for itn in range(self.numTreino):
                random.shuffle(self.dadosDeTreino)
                losses = {}
                # batch up the examples using spaCy's minibatch
                batches = minibatch(self.dadosDeTreino, size=compounding(4.0, 32.0, 1.001))
                for batch in batches:
                    texts, annotations = zip(*batch)
                    nlp.update(
                        texts,  # batch of texts
                        annotations,  # batch of annotations
                        drop=0.5,  # dropout - make it harder to memorise data
                        losses=losses,
                    )
                print("Losses", losses)
        for text, _ in self.dadosDeTreino:
            doc = nlp(text)
            print("Entities", [(ent.text, ent.label_) for ent in doc.ents])
            print("Tokens", [(t.text, t.ent_type_, t.ent_iob) for t in doc])

        self.saveModel(nlp)

