
'''
Created on 20/09/2015
@author: Juliane
'''

import os


class Util():

    @staticmethod
    def getNomeArquivo(arquivo):
        return [os.path.basename(arquivo)][0]


    @staticmethod
    def getNomeAutor(arquivo):
        nomeArquivo = Util.getNomeArquivo(arquivo)
        nomeAutor = nomeArquivo[0:2]
        return nomeAutor


    @staticmethod
    def salvarArquivo(arquivo, conteudo):
        with open(arquivo, "wb") as f:
            f.write(str(conteudo))


    @staticmethod
    def lerArquivo(arquivo):
        with open(arquivo, "rb") as f:
            return f.read()


    # Le o arquivo sem considerar as quebras de linha (LF, CR)
    @staticmethod
    def lerArquivoSemQuebraLinha(arquivo):
        with open(arquivo, "rb") as f:
            stringArquivo = "".join(f.readlines())
            stringArquivo = stringArquivo.replace("\n", " ").replace("\r", "")
            return stringArquivo


    @staticmethod
    def excluirArquivo(arquivo):
        if (os.path.isfile(arquivo)):
            os.remove(arquivo)


    @staticmethod
    def esvaziarDiretorio(diretorio):
        for arquivo in os.listdir(diretorio):
            arquivo = os.path.join(diretorio, arquivo)
            Util.excluirArquivo(arquivo)
