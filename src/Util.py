
'''
Created on 20/09/2015
@author: Juliane
'''

import os, pickle


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
    def getNomeAutorTxt(arquivo):
        nomeArquivo = Util.getNomeArquivo(arquivo)
        nomeAutor = nomeArquivo[0:nomeArquivo.find(".")]
        return nomeAutor


    @staticmethod
    def salvarArquivo(arquivo, conteudo):
        with open(arquivo, "wb") as f:
            f.write(str(conteudo))


    @staticmethod
    def salvarArquivoPickle(arquivo, conteudo):
        with open(arquivo, "wb") as f:
            pickle.dump(conteudo, f)


    @staticmethod
    def lerArquivo(arquivo):
        with open(arquivo, "rb") as f:
            # Le com LF, CR
            return f.read()

            # Le sem LF, CR
            #string = "".join(f.readlines())
            #string = string.replace("\n", " ").replace("\r", "")
            #return string


    @staticmethod
    def lerArquivoPickle(arquivo):
        with open(arquivo, "rb") as f:
            return dict(pickle.load(f))


    @staticmethod
    def excluirArquivo(arquivo):
        if (os.path.isfile(arquivo)):
            os.remove(arquivo)


    @staticmethod
    def esvaziarDiretorio(diretorio):
        for arquivo in os.listdir(diretorio):
            arquivo = os.path.join(diretorio, arquivo)
            Util.excluirArquivo(arquivo)
