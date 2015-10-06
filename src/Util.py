'''
Created on 20/09/2015

@author: Juliane
'''

import os


class Util():

    @staticmethod
    def getNomeArquivo(arquivo):
        nomeArquivo = [os.path.basename(arquivo)]
        return nomeArquivo[0]


    @staticmethod
    def getNomeAutor(arquivo):
        nomeArquivo = Util.getNomeArquivo(arquivo)
        nomeAutor = nomeArquivo[0:2]
        return nomeAutor


    @staticmethod
    def getNomeAutorTxt(arquivo):
        nomeArquivo = Util.getNomeArquivo(arquivo)
        nomeAutor = nomeArquivo[0:nomeArquivo.find(".")]
        return nomeAutor


    @staticmethod
    def excluirArquivo(arquivo):
        if (os.path.isfile(arquivo)):
            os.remove(arquivo)


    # Le e recupera toda a string do arquivo
    @staticmethod
    def getStringDeArquivo(arquivo):
        arquivoString = open(arquivo).read()
        return arquivoString


    @staticmethod
    def esvaziarDiretorio(diretorio):
        for raiz, diretorios, arquivos in os.walk(diretorio):
            for arquivo in arquivos:
                Util.excluirArquivo(raiz + arquivo)
