'''
Created on 20/09/2015

@author: Juliane
'''

import glob
import os
import pickle
import shutil
import config
from Util import Util


class Indexador():

    def __init__(self, dirDosIndices):
        self.L = config.L
        self.n = config.n
        
        self.dirDosIndices = dirDosIndices
        self.extensaoDosIndices = config.extensaoDosIndices


    # Indexa os arquivos do diretorio passado de acordo com as regras do algoritmo scap
    def indexarDiretorio(self, dirParaIndexar, finalAceito):
        autor = ""
        dicionarioAutores = {}
        dicionarioCodigosAutor = {}
        arquivosParaIndexar = glob.glob(dirParaIndexar + finalAceito)
        
        for arquivo in arquivosParaIndexar:
            autor = Util.getNomeAutor(arquivo)
            
            # Verifica se o autor ja foi incluido no dicionario de autores
            if (not dicionarioAutores.has_key(autor)):
                dicionarioCodigosAutor = {}
                dicionarioAutores.update({autor : dicionarioCodigosAutor})
            else :
                # Se ja foi, recupera o dicionario de codigos desse autor que vem sendo gerado na memoria
                dicionarioCodigosAutor = dicionarioAutores.get(autor)
            
            # Indexa o novo arquivo dando sequencia ao dicionario que ja vem sendo usado para esse autor
            dicionarioCodigosAutor = self.separarEmNGrams(arquivo, dicionarioCodigosAutor)
            dicionarioAutores.update({autor : dicionarioCodigosAutor})

           
        for chave, valor in dicionarioAutores.iteritems():
            # Recupera os L n-grams mais frequentes
            dicionarioCodigosAutor = self.recuperarLNGrams(valor)
            # Salvar perfil de um mesmo autor num mesmo arquivo
            self.salvarPerfil(dicionarioCodigosAutor, chave)


    # Indexa o arquivo (no dicionario, se ja existente) de acordo com as regras do algoritmo scap
    def indexarArquivo(self, arquivo, dicionario):
        dicionario = self.separarEmNGrams(arquivo, dicionario)
        dicionario = self.recuperarLNGrams(dicionario)
        # print dicionario
        # self.salvarPerfil(dicionario, Util.getNomeAutor(arquivo))
        
        return dicionario


    # Re-indexa somente os arquivos do autor do arquivo
    def reindexarPerfil(self, arquivo, dirParaIndexar, dirParaMover, extensaoAceita):
        # Move o arquivo do diretorio atual para um de consulta
        shutil.move(arquivo, dirParaMover)
    
        # Exclui o perfil indexado do autor do arquivo (se houver) da diretorio de indices
        Util.excluirArquivo(self.dirDosIndices + Util.getNomeAutor(arquivo) + self.extensaoDosIndices)
        # Re-indexa somente os arquivos deste autor
        self.indexarDiretorio(dirParaIndexar, Util.getNomeAutor(arquivo) + extensaoAceita)


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

        for chave, valor in sorted(dicionario.iteritems(), key=lambda (k, v): v, reverse=True):
            dicionarioL.update({chave : valor})
            i += 1
            if (i == self.L):
                break
        dicionarioL = sorted(dicionarioL.iteritems(), key=lambda (k, v): v, reverse=True)

        return dict(dicionarioL)


    # Salva o perfil do autor indexado como um dicionario num arquivo pickle
    def salvarPerfil(self, dicionario, nomeAutor):
        f = open(self.dirDosIndices + nomeAutor + self.extensaoDosIndices, "wb")
        pickle.dump(dicionario, f)
        f.close()


    # Verifica se determinado perfil ja existe
    def existePerfil(self, nomeAutor):
        return os.path.isfile(self.dirDosIndices + nomeAutor + self.extensaoDosIndices)


    def imprimirIndices(self):
        arquivosIndexados = glob.glob(self.dirDosIndices + "*" + self.extensaoDosIndices)
        
        for arquivo in arquivosIndexados:
            f = open(arquivo, "rb")
            dicionario = pickle.load(f)
            f.close()
            
            for chave, valor in sorted(dicionario.iteritems(), key=lambda (k, v): v, reverse=True):
                print "%s: %s" % (chave, valor)
            print "**************************"
            print "Quantidade de termos: %s" % (len(dicionario))
            print "*************************************************\n"
