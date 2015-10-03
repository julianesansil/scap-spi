'''
Created on 20/09/2015

@author: Juliane
'''

import os

class Util():

    def getNomeAutor(self, arquivo):
        nomeArquivo = [os.path.basename(arquivo)]
        nomeAutor = nomeArquivo[0][0:nomeArquivo[0].find("-")]
        return nomeAutor

    def getNomeArquivo(self, arquivo):
        nomeArquivo = [os.path.basename(arquivo)]
        return nomeArquivo[0]

    def excluirArquivo(self, arquivo):
        if (os.path.isfile(arquivo)):
            os.remove(arquivo)