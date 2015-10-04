'''
Created on 20/09/2015

@author: Juliane
'''

import glob
import os
import pickle
import config
from Util import Util


class Indexador():
    
    def __init__(self, dirDosIndices):
        self.L = config.L
        self.n = config.n
        
        self.dirDosIndices = dirDosIndices
        self.extensaoDosIndices = config.extensaoDosIndices


    # Indexa os arquivos do diretorio passado de acordo com as regras do algoritmo scap
    def indexar(self, dirParaIndexar, finalAceito):
        dicionario = {}
        arquivosParaIndexar = glob.glob(dirParaIndexar + finalAceito)
        
        for arquivo in arquivosParaIndexar:
            dicionario = self.recuperarPerfil(Util.getNomeAutor(arquivo))
            dicionario = self.separarEmNGrams(arquivo, dicionario)
            dicionario = self.recuperarLNGrams(dicionario)
            self.salvarPerfil(dicionario, Util.getNomeAutor(arquivo))


    # Recupera o perfil do autor no arquivo pickle antes salvo
    def recuperarPerfil(self, nomeAutor):
        dicionario = {}
        
        if (self.existePerfil(nomeAutor)):
            dicionario = pickle.load(open(self.dirDosIndices + nomeAutor + self.extensaoDosIndices, "rb"))
        
        return dict(dicionario)


    # Indexa o arquivo passado com a tecnica de n-grams
    # Ou seja, divide a string de entrada em pedacos de tamanho n e associa a sua respectiva frequencia no documento
    def separarEmNGrams(self, arquivo, dicionario):
        arquivoString = Util.getStringDeArquivo(arquivo)
        
        # Vai de 0 ate o tamanho da entrada - n+1
        for i in range(len(arquivoString) - self.n + 1):
            nGramTemp = ''.join(arquivoString[i : i + self.n])
            dicionario.setdefault(nGramTemp, 0)
            dicionario[nGramTemp] += 1
        
        return dict(dicionario)


    # Recupera os L primeiros n-grams mais frequentes do dicionario
    def recuperarLNGrams(self, dicionario):
        dicionarioL = {}
        i = 0

        for key, value in sorted(dicionario.iteritems(), key=lambda (k, v): v, reverse=True):
            dicionarioL.update({key : value})
            i += 1
            if (i == self.L):
                break
        dicionarioL = sorted(dicionarioL.iteritems(), key=lambda (k, v): v, reverse=True)

        return dict(dicionarioL)


    # Salva o perfil do autor indexado como um dicionario num arquivo pickle
    def salvarPerfil(self, dicionario, nomeAutor):
        pickle.dump(dicionario, open(self.dirDosIndices + nomeAutor + self.extensaoDosIndices, "wb"))


    # Verifica se determinado perfil ja existe
    def existePerfil(self, nomeAutor):
        return os.path.isfile(self.dirDosIndices + nomeAutor + self.extensaoDosIndices)


    def imprimirIndices(self):
        arquivosIndexados = glob.glob(self.dirDosIndices + "*" + self.extensaoDosIndices)
        
        for arquivo in arquivosIndexados:
            dicionario = pickle.load(open(arquivo, "rb"))
            
            for key, value in dicionario.iteritems():
                print "%s: %s" % (key, value)
            print "**************************"
            print "Quantidade de termos: %s" % (len(dicionario))
            print "*************************************************\n"
