
'''
Created on 29/09/2015
@author: Juliane
'''

import glob
from Util import Util


class Buscador():

    def __init__(self, indexador, L):
        self.indexador = indexador
        self.L = L


    # Compara o arquivo-consulta com os demais arquivos da base
    # E retorna o autor com maior semelhancas de n-grams comparado ao arquivo-consulta
    def compararComTodosDaBase(self, arquivoConsulta):
        dicionarioConsulta = self.indexador.indexarArquivo(arquivoConsulta)
        dicionarioConsulta = self.indexador.recuperarLNGrams(dicionarioConsulta, self.L)
        
        arquivosDosIndices = glob.glob(self.indexador.dirDosIndices + "*" + self.indexador.extensaoDosIndices)
        autor = ""
        maiorSemelhancas = 0
        qtdeSemelhancas = 0
        
        for arquivo in arquivosDosIndices:
            dicionarioTemp = self.indexador.recuperarDicionario(arquivo)
            dicionarioTemp = self.indexador.recuperarLNGrams(dicionarioTemp, self.L)
            qtdeSemelhancas = self.getQtdeSemelhancas(dicionarioConsulta, dicionarioTemp)
            
            if (qtdeSemelhancas >= maiorSemelhancas):
                maiorSemelhancas = qtdeSemelhancas
                autor = Util.getNomeAutorTxt(arquivo)
        
        return autor


    # Retorna a quantidade de semelhancas de n-grams que tem 2 arquivos
    def getQtdeSemelhancas(self, dicionarioConsulta, dicionarioTemp):
        # Retorna os n-grams que tem na consulta, mas nao tem no dicionario comparado
        diferencaNGrams = set(dicionarioConsulta.keys()) - set(dicionarioTemp.keys())
        qtdeSemelhancas = len(dicionarioConsulta.keys()) - len(diferencaNGrams)
        
        return qtdeSemelhancas
