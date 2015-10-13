#coding: utf-8

'''
Created on 07/10/2015
@author: Juliane
'''

import glob
from Util import Util
from _collections import defaultdict


class PreparadorArquivos():

    def __init__(self, dirNGrams, extensaoNGram, n):
        self.dirNGrams = dirNGrams
        self.extensaoNGram = extensaoNGram
        self.n = n


    # Seleciona as caracteristicas relevantes dos arquivos para indexacao
    def prepararArquivos(self, dirParaPreparar, finalAceito):
        arquivos = glob.glob(dirParaPreparar + finalAceito)
        
        print "N-grams extraidos dos arquivos..."
        for arquivo in arquivos:
            print arquivo
            nGramsArquivo = []
            
            # Recupera os n-grams do arquivo
            nGramsArquivo = self.separarEmNGrams(arquivo)
            self.salvarNGrams(Util.getNomeArquivo(arquivo), nGramsArquivo)


    # Divide a string de entrada em pedacos de tamanho n
    # Utilizando a tecnica de janela deslizante para percorrer a string
    def separarEmNGrams(self, arquivo):
        arquivoString = Util.getStringDeArquivo(arquivo)
        listNGramsArquivo = []
        
        # Vai de 0 ate o tamanho da entrada - n+1
        for i in range(len(arquivoString) - self.n + 1):
            nGram  = ''.join(arquivoString[i : i + self.n])
            nGram = nGram.replace(" ", "ç")
            listNGramsArquivo.append(nGram)
            listNGramsArquivo.append(" ")
        
        nGramsArquivo = "".join(listNGramsArquivo)
        return nGramsArquivo


    # Salva os n-grams de determinado arquivo num arquivo
    def salvarNGrams(self, nomeArquivo, nGramsArquivo):
        f = open(self.dirNGrams + nomeArquivo + self.extensaoNGram, "wb")
        f.write(nGramsArquivo)
        f.close()


    # De um conjunto de arquivos com varios n-grams, separa os n-grams por autor
    @staticmethod
    def recuperarNGramsPorAutor(arquivosNGrams):
        autor = ""
        dictNGramsPorAutor = defaultdict(list)      # {"autor", "listNGramsAutor"}
        
        print "N-grams recuperados dos arquivos..."
        for arquivo in arquivosNGrams:
            print arquivo
            
            autor = Util.getNomeAutor(arquivo)
            # Recupera os n-grams do arquivo e atualiza o dicionario de autores
            dictNGramsPorAutor[autor].append(Util.getStringDeArquivo(arquivo))
        
        # Transforma a lista de n-grams numa string unica
        for autor, listNGramsAutor in dictNGramsPorAutor.iteritems():
            dictNGramsPorAutor.update({autor : "".join(listNGramsAutor)})
        
        return dictNGramsPorAutor
