import spacy
import os


from model.DTO.trechoDTO import trechoDTO


def getEntities(listText):
    listFinal = list()
    for text in listText:
        entidades = list()
        nlp2 = spacy.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../treinamentos/treinamento1'))
        doc = nlp2(text)
        for ent in doc.ents:
            entidades.append(ent.text)
        trecho = trechoDTO(text, entidades)
        print("Entities", [(ent.text, ent.label_) for ent in doc.ents])
        print("Tokens", [(t.text, t.ent_type_, t.ent_iob) for t in doc])
        listFinal.append({'text':trecho.trecho, 'entidades':trecho.name})

    return listFinal
