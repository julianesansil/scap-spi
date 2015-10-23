#coding: utf-8

'''
Created on 07/10/2015
@author: Juliane
'''

import glob, os, re
from _collections import defaultdict
from Util import Util


class Preparador():

    def __init__(self, dirBasePreparada, extensaoParaSalvar, n, comQuebraLinha, comComentariosELiterais):
        self.dirBasePreparada = dirBasePreparada
        self.extensaoParaSalvar = extensaoParaSalvar
        self.n = n
        self.comQuebraLinha = comQuebraLinha
        self.comComentariosELiterais = comComentariosELiterais


    # Seleciona as caracteristicas relevantes dos arquivos do diretorio passado
    def prepararDiretorio(self, dirParaPreparar):
        arquivos = glob.glob(dirParaPreparar)
        
        for arquivo in arquivos:
            nGramsArquivo = []
            
            if (self.comQuebraLinha):
                stringArquivo = Util.lerArquivo(arquivo)
            else: 
                # Se (comQuebraLinha = False), le o arquivo sem considerar as quebras de linha (LF, CR)
                stringArquivo = Util.lerArquivoSemQuebraLinha(arquivo)
            
            # Se (comComentariosELiterais = False), retira os comentarios e literais da string
            if not (self.comComentariosELiterais):
                stringArquivo = self.removerComentarios(stringArquivo)
                stringArquivo = self.removerLiterais(stringArquivo)
                #print stringArquivo
            
            # Separa o arquivo em n-grams
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
            nGram = nGram.replace(" ", "ç")
            listNGramsArquivo.append(nGram)
            listNGramsArquivo.append(" ")

        nGramsArquivo = "".join(listNGramsArquivo)
        return nGramsArquivo


    # Salva os n-grams de determinado arquivo num arquivo
    def salvarNGrams(self, nomeArquivo, nGramsArquivo):
        Util.salvarArquivo(os.path.join(self.dirBasePreparada, nomeArquivo + self.extensaoParaSalvar), nGramsArquivo)


    # Recupera os n-grams do arquivo
    def recuperarNGrams(self, arquivo):
        return Util.lerArquivo(arquivo)


    # De um conjunto de arquivos com varios n-grams, separa os n-grams por autor
    def recuperarNGramsPorAutor(self, arquivosNGrams):
        autor = ""
        # Com defaultdict(list), dictNGramsPorAutor[autor] = []
        # O defaultdict() inicia o valor do dict com uma lista vazia
        dictNGramsPorAutor = defaultdict(list)      # {"autor", "listNGramsAutor"}
        
        #print "N-grams recuperados dos arquivos..."
        for arquivo in arquivosNGrams:
            #print arquivo
            
            autor = Util.getNomeAutor(arquivo)
            # Recupera os n-grams do arquivo e atualiza o dicionario de autores
            dictNGramsPorAutor[autor].append(self.recuperarNGrams(arquivo))
        
        # Transforma a lista de n-grams numa string unica
        for autor, listNGramsAutor in dictNGramsPorAutor.iteritems():
            dictNGramsPorAutor.update({autor : "".join(listNGramsAutor)})
        
        return dictNGramsPorAutor


    def imprimirDiretorioPreparado(self):
        arquivos = glob.glob(self.dirBasePreparada + "*" + self.extensaoParaSalvar)
        dictNGramsPorAutor = self.recuperarNGramsPorAutor(arquivos)
        
        print ""
        for autor, nGrams in dictNGramsPorAutor.iteritems():
            print "******************************************************************************"
            print autor, ": ", nGrams
        print "******************************************************************************"
