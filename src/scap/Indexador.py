
'''
Created on 20/09/2015
@author: Juliane
'''

import glob
import pickle
from collections import Counter, OrderedDict
from scap.PreparadorArquivos import PreparadorArquivos
import itertools


class Indexador():

    def __init__(self, dirDosIndices, extensaoDosIndices, L):
        self.dirDosIndices = dirDosIndices
        self.extensaoDosIndices = extensaoDosIndices
        self.L = L


    # Indexa os arquivos do diretorio passado de acordo com as regras do algoritmo scap
    def indexarDiretorio(self, dirNGrams, finalAceito):
        arquivosNGrams = glob.glob(dirNGrams + finalAceito)
        dictPerfilAutor = PreparadorArquivos.recuperarNGramsPorAutor(arquivosNGrams)      # {"autor", "nGramsAutor"} => {"autor", "nGramsAutorIndexado"}
        
        for autor, nGramsAutor in dictPerfilAutor.iteritems():
            # Atualiza o dicionario de autores com o vocabulario indexado do autor
            dictPerfilAutor[autor] = self.indexarNGrams(nGramsAutor)
        
        for autor, nGramsAutorIndexado in dictPerfilAutor.iteritems():
            # Atualiza o dicionario de autores com os L n-grams mais frequentes
            dictPerfilAutor[autor] = self.recuperarLNGrams(nGramsAutorIndexado, self.L)
            self.salvarPerfilAutor(autor, dictPerfilAutor[autor])
        
        return dictPerfilAutor


    # Indexa o vocabulario extraido dos n-grams
    # Ou seja, associa o n-gram a sua respectiva frequencia nos n-grams
    def indexarNGrams(self, nGrams):
        listNGrams = nGrams.split()             # A cada espaco encontrado, 1 n-gram e recuperado
        dictVocabulario = Counter(listNGrams)   # {"nGram" : "frequenciaNGram"} = vocabularioIndexado
        return dictVocabulario


    # Recupera os L primeiros n-grams mais frequentes do dicionario
    def recuperarLNGrams(self, nGrams, L):
        dicionario = OrderedDict(sorted(nGrams.items(), key=lambda t: t[1], reverse=True))
        return dict(itertools.islice(dicionario.iteritems(), L))


    # Salva o perfil do autor (vocabulario indexado) num arquivo pickle
    def salvarPerfilAutor(self, autor, nGramsAutorIndexado):
        f = open(self.dirDosIndices + autor + self.extensaoDosIndices, "wb")
        pickle.dump(nGramsAutorIndexado, f)
        f.close()


    # Recupera o perfil do autor (vocabulario indexado) do arquivo pickle passado
    def recuperarPerfilAutor(self, arquivo):
        f = open(arquivo, "rb")
        dictPerfilAutor = dict(pickle.load(f))
        f.close()
        
        return dictPerfilAutor


    def imprimirDiretorioIndexado(self):
        arquivosIndexados = glob.glob(self.dirDosIndices + "*" + self.extensaoDosIndices)
        
        for arquivo in arquivosIndexados:
            print "\n******************************************************************************"
            print "Arquivo: %s" % (arquivo)
            print "**************************"
            dicionario = self.recuperarPerfilAutor(arquivo)
            
            for chave, valor in sorted(dicionario.iteritems(), key=lambda (k, v): v, reverse=True):
                print "%s: %s" % (chave, valor)
            print "Arquivo: %s" % (arquivo)
            print "**************************"
            print "Quantidade de termos: %s" % (len(dicionario))
            print "******************************************************************************\n"
