#coding: utf-8

'''
Created on 07/10/2015
@author: Juliane
'''

import glob, os, re
from _collections import defaultdict
from Util import Util


class Preparador():

    def __init__(self, dirNGrams, extensaoNGram, n, comComentariosELiterais):
        self.dirNGrams = dirNGrams
        self.extensaoNGram = extensaoNGram
        self.n = n
        self.comComentariosELiterais = comComentariosELiterais


    # Seleciona as caracteristicas relevantes dos arquivos
    def prepararDiretorio(self, pathParaPreparar):
        arquivos = glob.glob(pathParaPreparar)
        
        #print "N-grams extraidos dos arquivos..."
        for arquivo in arquivos:
            #print arquivo
            nGramsArquivo = []
            
            stringArquivo = Util.lerArquivo(arquivo)
            if not (self.comComentariosELiterais):
                stringArquivo = self.removerComentarios(stringArquivo)
                stringArquivo = self.removerLiterais(stringArquivo)
                #print stringArquivo
            
            # Recupera os n-grams do arquivo
            nGramsArquivo = self.separarEmNGrams(stringArquivo)
            self.salvarNGrams(Util.getNomeArquivo(arquivo), nGramsArquivo)


    # Remove os comentarios (//..., /*...*/) da string passada
    def removerComentarios(self, stringArquivo):
        inicio = re.escape("//")
        regex = "%s(.*)" % (inicio)
        stringArquivo = re.sub(regex, "", stringArquivo)

        inicio = re.escape("/*")
        fim = re.escape("*/")
        regex = re.compile("%s(.*?)%s" % (inicio, fim), re.DOTALL)
        stringArquivo = re.sub(regex, "", stringArquivo)
        
        return stringArquivo


    # Remove os literais ("...") da string passada
    def removerLiterais(self, stringArquivo):
        token = "\""
        regex = re.compile("%s(.*?)%s" % (token, token), re.DOTALL)
        stringArquivo = re.sub(regex, "", stringArquivo)
        
        return stringArquivo

    # Divide a string de entrada em pedacos de tamanho n
    # Utilizando a tecnica de janela deslizante para percorrer a string
    def separarEmNGrams(self, stringArquivo):
        listNGramsArquivo = []
        
        # Vai de 0 ate o tamanho da entrada - n+1
        for i in range(len(stringArquivo) - self.n + 1):
            nGram  = "".join(stringArquivo[i : i + self.n])
            nGram = nGram.replace(" ", "รง")
            listNGramsArquivo.append(nGram)
            listNGramsArquivo.append(" ")

        nGramsArquivo = "".join(listNGramsArquivo)
        return nGramsArquivo


    # Salva os n-grams de determinado arquivo num arquivo
    def salvarNGrams(self, nomeArquivo, nGramsArquivo):
        Util.salvarArquivo(os.path.join(self.dirNGrams, nomeArquivo + self.extensaoNGram), nGramsArquivo)


    # Recupera os n-grams do arquivo
    def recuperarNGrams(self, arquivo):
        return Util.lerArquivo(arquivo)


    # De um conjunto de arquivos com varios n-grams, separa os n-grams por autor
    def recuperarNGramsPorAutor(self, arquivosNGrams):
        autor = ""
        dictNGramsPorAutor = defaultdict(list)      # {"autor", "listNGramsAutor"}
        
        # print "N-grams recuperados dos arquivos..."
        for arquivo in arquivosNGrams:
            # print arquivo
            
            autor = Util.getNomeAutor(arquivo)
            # Recupera os n-grams do arquivo e atualiza o dicionario de autores
            dictNGramsPorAutor[autor].append(self.recuperarNGrams(arquivo))
        
        # Transforma a lista de n-grams numa string unica
        for autor, listNGramsAutor in dictNGramsPorAutor.iteritems():
            dictNGramsPorAutor.update({autor : "".join(listNGramsAutor)})
        
        return dictNGramsPorAutor


    def imprimirDiretorioPreparado(self):
        arquivos = glob.glob(self.dirNGrams + "*" + self.extensaoNGram)
        dictNGramsPorAutor = self.recuperarNGramsPorAutor(arquivos)
        
        print ""
        for autor, nGrams in dictNGramsPorAutor.iteritems():
            print "******************************************************************************"
            print autor, ": ", nGrams
        print "******************************************************************************"
