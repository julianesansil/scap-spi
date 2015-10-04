'''
Created on 20/09/2015

@author: Juliane
'''

import os


class Util():

    @staticmethod
    def getNomeAutor(arquivo):
        nomeArquivo = [os.path.basename(arquivo)]
        nomeAutor = nomeArquivo[0][0:nomeArquivo[0].find("-")]
        return nomeAutor


    @staticmethod
    def getNomeAutorTxt(arquivo):
        nomeArquivo = [os.path.basename(arquivo)]
        nomeAutor = nomeArquivo[0][0:nomeArquivo[0].find(".")]
        return nomeAutor


    @staticmethod
    def getNomeArquivo(arquivo):
        nomeArquivo = [os.path.basename(arquivo)]
        return nomeArquivo[0]


    @staticmethod
    def excluirArquivo(arquivo):
        if (os.path.isfile(arquivo)):
            os.remove(arquivo)


    # Le e recupera toda a string do arquivo
    @staticmethod
    def getStringDeArquivo(arquivo):
        arquivoString = open(arquivo).read()
        return arquivoString
