
'''
Created on 29/09/2015
@author: Juliane
'''

import glob, os
from Util import Util


class Buscador():

    def __init__(self, indexador, L):
        self.indexador = indexador
        self.L = L


    # Compara o arquivo-consulta com os demais arquivos da base
    # E retorna o autor com maior semelhancas de n-grams comparado ao arquivo-consulta
    def compararComTodosDaBase(self, arquivoConsulta):
        dictConsulta = self.indexador.indexarArquivo(arquivoConsulta)
        
        arquivosIndices = glob.glob(os.path.join(self.indexador.dirIndices, "*" + self.indexador.extensaoIndices))
        autor = ""
        maiorSemelhancas = 0
        qtdeSemelhancas = 0
        
        for arquivo in arquivosIndices:
            dictTemp = self.indexador.recuperarPerfilAutor(arquivo)
            qtdeSemelhancas = self.getQtdeSemelhancas(dictConsulta, dictTemp)
            
            if (qtdeSemelhancas >= maiorSemelhancas):
                maiorSemelhancas = qtdeSemelhancas
                autor = Util.getNomeAutorTxt(arquivo)
        
        return autor


    # Retorna a quantidade de semelhancas de n-grams que tem 2 arquivos
    def getQtdeSemelhancas(self, dictConsulta, dictTemp):
        # Retorna os n-grams que tem na consulta, mas nao tem no dicionario comparado
        diferencaNGrams = set(dictConsulta.keys()) - set(dictTemp.keys())
        qtdeSemelhancas = len(dictConsulta.keys()) - len(diferencaNGrams)
        
        return qtdeSemelhancas
