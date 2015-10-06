'''
Created on 29/09/2015

@author: Juliane
'''

import glob
import pickle
import config
from Util import Util


class Buscador():

    def __init__(self):
        self.dirDosIndices = config.dirDosIndices
        self.extensaoDosIndices = config.extensaoDosIndices


    # Compara o arquivo-consulta com os demais arquivos da base
    # E retorna o autor com maior semelhancas de n-grams comparado ao arquivo-consulta
    def compararComTodosDaBase(self, arquivoConsulta, indexadorConsulta):
        dicionarioConsulta = {}
        dicionarioConsulta = indexadorConsulta.indexarArquivo(arquivoConsulta, dicionarioConsulta)
        
        arquivosDosIndices = glob.glob(self.dirDosIndices + "*" + self.extensaoDosIndices)
        autor = ""
        maiorSemelhancas = 0
        qtdeSemelhancas = 0
        
        for arquivo in arquivosDosIndices:
            dicionarioTemp = self.recuperarArquivoIndexado(arquivo)
            qtdeSemelhancas = self.getQtdeSemelhancas(dicionarioConsulta, dicionarioTemp)
            
            if (qtdeSemelhancas > maiorSemelhancas):
                maiorSemelhancas = qtdeSemelhancas
                autor = arquivo
        
        return Util.getNomeAutorTxt(autor)


    # Recupera o dicionario do arquivo pickle passado
    def recuperarArquivoIndexado(self, arquivo):
        f = open(arquivo, "rb")
        dicionario = dict(pickle.load(f))
        f.close()
        return dicionario


    # Retorna a quantidade de semelhancas de n-grams que tem 2 arquivos
    def getQtdeSemelhancas(self, dicionarioConsulta, dicionarioTemp):
        # Retorna os n-grams que tem na consulta, mas nao tem no dicionario comparado
        diferencaNGrams = set(dicionarioConsulta.keys()) - set(dicionarioTemp.keys())
        qtdeSemelhancas = len(dicionarioConsulta.keys()) - len(diferencaNGrams)
       
        return qtdeSemelhancas
