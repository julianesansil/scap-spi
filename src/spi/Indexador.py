
'''
Created on 20/09/2015
@author: Juliane
'''

import itertools, os
from collections import Counter, OrderedDict
from Util import Util


class Indexador():

    def __init__(self, preparador, L, comTermos1Ocorrencia):
        self.preparador = preparador
        self.L = L
        self.comTermos1Ocorrencia = comTermos1Ocorrencia


    # Indexa os arquivos de acordo com as regras do algoritmo spi
    def indexarArquivos(self, arquivos):
        dictPerfilAutores = self.preparador.recuperarNGramsPorAutor(arquivos)   # {"autor", "nGramsAutor"} => {"autor", "vocabularioAutorIndexado"}
        
        for autor, nGramsAutor in dictPerfilAutores.iteritems():
            # Atualiza o dicionario de autores com o vocabulario indexado do autor
            dictPerfilAutores[autor] = self.indexarNGrams(nGramsAutor)
        
        for autor, vocabularioAutorIndexado in dictPerfilAutores.iteritems():
            if (self.L > 0):
                # Atualiza o dicionario de autores com os L n-grams mais frequentes
                dictPerfilAutores[autor] = self.recuperarLNGrams(vocabularioAutorIndexado, self.L)
        
        return dictPerfilAutores


    # Retira o arquivoRetirar para, em seguida, indexar os demais arquivos
    def indexarArquivosSemArquivoEspecifico(self, arquivos, arquivoParaRetirar):
        arquivos.remove(arquivoParaRetirar)
        return self.indexarArquivos(arquivos)


    # Indexa o vocabulario extraido dos n-grams
    # Ou seja, associa o n-gram a sua respectiva frequencia nos n-grams
    def indexarNGrams(self, nGrams):
        listNGrams = nGrams.split(" ")              # A cada espaco encontrado, 1 n-gram e recuperado
        listNGrams.remove("")
        vocabularioIndexado = Counter(listNGrams)   # {"nGram" : "frequenciaNGram"}
        
        # Se (comTermos1Ocorrencia = True), retira os termos com 1 ocorrencia do vocabulario
        if not (self.comTermos1Ocorrencia):
            return self.removerTermos1Ocorrencia(vocabularioIndexado)
        
        return vocabularioIndexado


    def removerTermos1Ocorrencia(self, vocabularioIndexado):
            vocabularioSemTermo1Ocorrencia = {}
            vocabularioSemTermo1Ocorrencia.update(vocabularioIndexado)
            
            for nGram, frequenciaNGram in vocabularioIndexado.iteritems():
                if (frequenciaNGram == 1):
                    del vocabularioSemTermo1Ocorrencia[nGram]
            
            return vocabularioSemTermo1Ocorrencia


    # Recupera os L primeiros n-grams mais frequentes do dicionario
    def recuperarLNGrams(self, nGrams, L):
        dicionario = OrderedDict(sorted(nGrams.items(), key=lambda t: t[1], reverse=True))
        return dict(itertools.islice(dicionario.iteritems(), L))


    def imprimirPerfilAutores(self, dictPerfilAutores):
        for autor, vocabularioAutorIndexado in dictPerfilAutores.iteritems():
            print "******************************************************************************"
            print "Autor:", autor
            print "**************************"
            
            for nGram, frequenciaNGram in sorted(vocabularioAutorIndexado.iteritems(), key=lambda (k, v): v, reverse=True):
                print nGram, " : ", frequenciaNGram
            
            print "**************************"
            print "Quantidade de termos: ", len(vocabularioAutorIndexado)
            print "******************************************************************************\n\n"



    def salvarValidacaoIndices(self, dirIndicesValidacao, dictPerfilAutores, extensaoPadrao):
        for autor, vocabularioAutorIndexado in dictPerfilAutores.iteritems():
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
            Util.salvarArquivo(os.path.join(dirIndicesValidacao, autor + extensaoPadrao), stringPerfilAutor)
