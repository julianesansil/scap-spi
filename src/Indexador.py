'''
Created on 20/09/2015

@author: Juliane
'''

import os
import pickle

class Indexador():
    def __init__(self, dirDosIndices, extensaoDosIndices, dirParaIndexar, extensaoAceita, L, n):
        # Diretorio e arquivos permitidos de serem indexados
        self.dirParaIndexar = dirParaIndexar
        self.extensaoAceita = extensaoAceita
        # Diretorio onde os indices serao salvos
        self.dirDosIndices = dirDosIndices
        self.extensaoDosIndices = extensaoDosIndices
        # Tamanho L (quantidade de termos da indexacao)
        self.L = L
        # Tamanho n do n-grams (tamanho do termo)
        self.n = n


    # Indexa os n-grams do documento
    # Ou seja, divide a string de entrada em pedacos de tamanho n e associa a sua respectiva frequencia no documento
    def separarEmNGrams(self, arquivo, dicionario, n):
        arquivoString = self.getStringDeArquivo(arquivo)
        
        # Vai de 0 ate o tamanho da entrada - n+1
        for i in range(len(arquivoString) - n + 1):
            nGramTemp = ''.join(arquivoString[i : i + n])
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

    # Recupera o perfil do autor no arquivo pickle antes salvo
    def recuperarPerfil(self, nomeAutor):
        dicionario = {}
        if (self.existePerfil(nomeAutor)):
            dicionario = pickle.load(open(self.dirDosIndices + nomeAutor + self.extensaoDosIndices, "rb"))
        return dict(dicionario)
    
    # Le e recupera toda a string do arquivo
    def getStringDeArquivo(self, arquivo):
        arquivoString = open(arquivo).read()
        return arquivoString
