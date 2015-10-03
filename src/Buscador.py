'''
Created on 29/09/2015

@author: Juliane
'''

import pickle
from Util import Util

class Buscador():
    
    def __init__(self):
        self.util = Util()

    def indexarConsulta(self, indexadorConsulta, arquivoParaConsultar, dicionarioConsulta):
        dicionarioConsulta = indexadorConsulta.separarEmNGrams(arquivoParaConsultar, dicionarioConsulta, indexadorConsulta.n)
        dicionarioConsulta = indexadorConsulta.recuperarLNGrams(dicionarioConsulta)
        return dicionarioConsulta

    def recuperarArquivoIndexado(self, arquivo):
        dicionario = pickle.load(open(arquivo, "rb"))
        return dict(dicionario)

    def getQtdeSemelhancas(self, dicionarioConsulta, dicionarioTemp):
        # Retorna os n-grams que tem na consulta, mas nao tem no dicionario comparado
        diferencaNGrams = set(dicionarioConsulta.keys()) - set(dicionarioTemp.keys())
        qtdeSemelhancas = len(dicionarioConsulta.keys()) - len(diferencaNGrams)
        return qtdeSemelhancas
