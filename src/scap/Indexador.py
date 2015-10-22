
'''
Created on 20/09/2015
@author: Juliane
'''

import itertools, glob, os
import config
from collections import Counter, OrderedDict
from Util import Util


class Indexador():

    def __init__(self, preparador, dirIndices, extensaoIndices, L, comTermos1Ocorrencia):
        self.preparador = preparador
        self.dirIndices = dirIndices
        self.extensaoIndices = extensaoIndices
        self.L = L
        self.comTermos1Ocorrencia = comTermos1Ocorrencia


    # Indexa os arquivos do caminho passado de acordo com as regras do algoritmo scap
    # comL = considera ou desconsidera o L para indexacao
    def indexarDiretorio(self, pathParaIndexar):
        arquivosNGrams = glob.glob(pathParaIndexar)
        dictPerfilAutor = self.preparador.recuperarNGramsPorAutor(arquivosNGrams)   # {"autor", "nGramsAutor"} => {"autor", "vocabularioAutorIndexado"}
        
        for autor, nGramsAutor in dictPerfilAutor.iteritems():
            # Atualiza o dicionario de autores com o vocabulario indexado do autor
            dictPerfilAutor[autor] = self.indexarNGrams(nGramsAutor)
        
        for autor, vocabularioAutorIndexado in dictPerfilAutor.iteritems():
            #imprimir dictPerfilAutor
            #salvar dictPerfilAutor num arquivo
            if (self.L > 0):
                # Atualiza o dicionario de autores com os L n-grams mais frequentes
                dictPerfilAutor[autor] = self.recuperarLNGrams(vocabularioAutorIndexado, self.L)
            self.salvarPerfilAutor(autor, dictPerfilAutor[autor])
            self.salvarDiretorioIndexado(config.dirIndicesValidacao)
        
        return dictPerfilAutor


    # Indexa o arquivo passado de acordo com as regras do algoritmo scap
    def indexarArquivo(self, arquivo):
        nGrams = self.preparador.recuperarNGrams(arquivo)
        vocabularioIndexado = self.indexarNGrams(nGrams)

        # Considera ou desconsidera o L para indexacao        
        if (self.L > 0):
            return self.recuperarLNGrams(vocabularioIndexado, self.L)
        else: return vocabularioIndexado

    # Indexa o vocabulario extraido dos n-grams
    # Ou seja, associa o n-gram a sua respectiva frequencia nos n-grams
    def indexarNGrams(self, nGrams):
        listNGrams = nGrams.split(" ")              # A cada espaco encontrado, 1 n-gram e recuperado
        vocabularioIndexado = Counter(listNGrams)   # {"nGram" : "frequenciaNGram"}
        
        # Se (comTermos1Ocorrencia = True), retira os termos com 1 ocorrencia do dicionario
        if not (self.comTermos1Ocorrencia):
            dictSemTermo1Ocorrencia = {}
            
            for nGram, frequenciaNGram in vocabularioIndexado.iteritems():
                if (frequenciaNGram != 1):
                    dictSemTermo1Ocorrencia[nGram] = vocabularioIndexado[nGram]

            return dictSemTermo1Ocorrencia
        
        return vocabularioIndexado


    # Recupera os L primeiros n-grams mais frequentes do dicionario
    def recuperarLNGrams(self, nGrams, L):
        dicionario = OrderedDict(sorted(nGrams.items(), key=lambda t: t[1], reverse=True))
        return dict(itertools.islice(dicionario.iteritems(), L))


    # Salva o perfil do autor (vocabulario indexado) num arquivo pickle
    def salvarPerfilAutor(self, autor, vocabularioAutorIndexado):
        Util.salvarArquivoPickle(os.path.join(self.dirIndices, autor + self.extensaoIndices), vocabularioAutorIndexado)


    # Recupera o perfil do autor (vocabulario indexado) do arquivo pickle passado
    def recuperarPerfilAutor(self, arquivo):
        return Util.lerArquivoPickle(arquivo)


    def imprimirDiretorioIndexado(self):
        arquivosIndexados = glob.glob(self.dirIndices + "*" + self.extensaoIndices)
        
        for arquivo in arquivosIndexados:
            print "\n******************************************************************************"
            print "Arquivo: ", arquivo
            print "**************************"
            vocabularioAutorIndexado = self.recuperarPerfilAutor(arquivo)
            
            for nGram, frequenciaNGram in sorted(vocabularioAutorIndexado.iteritems(), key=lambda (k, v): v, reverse=True):
                print nGram, " : ", frequenciaNGram
            print "**************************"
            print "Quantidade de termos: ", len(vocabularioAutorIndexado)
            print "******************************************************************************\n"


    def salvarDiretorioIndexado(self, dirIndicesValidacao):
        arquivosIndexados = glob.glob(self.dirIndices + "*" + self.extensaoIndices)
        
        for arquivo in arquivosIndexados:
            vocabularioAutorIndexado = self.recuperarPerfilAutor(arquivo)
            stringArquivo = []

            qtdeTermos1Ocorrencia = 0
            for nGram, frequenciaNGram in sorted(vocabularioAutorIndexado.iteritems(), key=lambda (k, v): v, reverse=True):
                stringArquivo.append(nGram + " : " + str(frequenciaNGram) + "\r\n")

                if (frequenciaNGram == 1):
                    qtdeTermos1Ocorrencia += 1
            
            if (len(vocabularioAutorIndexado) > 0):
                percentTermos1Ocorrencia = 100*qtdeTermos1Ocorrencia/float(len(vocabularioAutorIndexado))
            else: percentTermos1Ocorrencia = 100
            stringArquivo.append("\r\nQuantidade de termos: " + str(len(vocabularioAutorIndexado)))
            stringArquivo.append("\r\nQuantidade de termos com 1 ocorrencia: " + str(qtdeTermos1Ocorrencia))
            stringArquivo.append("\r\nPorcentagem dos termos com 1 ocorrencia: " + str(percentTermos1Ocorrencia) + "%")
                                     
            stringPerfilAutor = "".join(stringArquivo)
            Util.salvarArquivo(os.path.join(dirIndicesValidacao, Util.getNomeAutor(arquivo) + self.extensaoIndices), stringPerfilAutor)
