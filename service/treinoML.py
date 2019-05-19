from __future__ import unicode_literals, print_function

import plac
import random
from pathlib import Path
import spacy
from spacy.util import minibatch, compounding
import os


from model.ModeloML import modeloML
from util.util import Util
from model.DTO.trechoDTO import trechoDTO

def treino(listNome):
    dadosDeTreino = Util.transformListNome(listNome)
    modelo = modeloML(dadosDeTreino=dadosDeTreino)
    modelo.treinar()
