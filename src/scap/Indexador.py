'''
Created on 20/09/2015

@author: Juliane
'''

import glob
import pickle
from Util import Util


class Indexador():

    def __init__(self, dirDosIndices, extensaoDosIndices, n):
        self.dirDosIndices = dirDosIndices
        self.extensaoDosIndices = extensaoDosIndices
        self.n = n


    # Indexa os arquivos do diretorio passado de acordo com as regras do algoritmo scap
    def indexarDiretorio(self, dirParaIndexar, finalAceito):
        autor = ""
        dicionarioCodigosPorAutor = {}  # {"autor", "dicionarioCodigosAutor"}
        dicionarioCodigos = {}          # {"termosCodigos", "frequenciaTermosCodigos"} = codigosAutorIndexado
        
        arquivosParaIndexar = glob.glob(dirParaIndexar + finalAceito)
        
        # print "Arquivos indexados..."
        for arquivo in arquivosParaIndexar:
            # print arquivo
            autor = Util.getNomeAutor(arquivo)
            
            # Verifica se o autor ja foi incluido no dicionario de autores
            if (not dicionarioCodigosPorAutor.has_key(autor)):
                dicionarioCodigos = {}
                dicionarioCodigosPorAutor.update({autor : dicionarioCodigos})
            else :
                # Se autor ja incluido, recupera o dicionario de codigos desse autor que vem sendo gerado na memoria
                dicionarioCodigos = dicionarioCodigosPorAutor.get(autor)
            
            # Indexa o novo arquivo dando sequencia ao dicionario que ja vem sendo usado para esse autor
            dicionarioCodigos = self.indexarArquivoEmDicionarioExistente(arquivo, dicionarioCodigos)
            dicionarioCodigosPorAutor.update({autor : dicionarioCodigos})
            
        for chave, valor in dicionarioCodigosPorAutor.iteritems():
            # Salva perfil de um mesmo autor num mesmo arquivo
            self.salvarPerfil(chave, valor)


    # Indexa o arquivo passado com a tecnica de n-grams + janela deslizante
    # Ou seja, divide a string de entrada em termos de tamanho n e associa esses termos a sua respectiva frequencia no documento
    def indexarArquivo(self, arquivo):
        return self.indexarArquivoEmDicionarioExistente(arquivo, {})


    # Indexa o arquivo junto a um dicionario ja existente
    def indexarArquivoEmDicionarioExistente(self, arquivo, dicionario):
        vocabulario = self.separarEmNGrams(arquivo)
        
        for termo in vocabulario:
            dicionario.setdefault(termo, 0)
            dicionario[termo] += 1
        
        return dicionario


    # Divide a string de entrada em pedacos de tamanho n
    # Utilizando a tecnica de janela deslizante para percorrer a string
    def separarEmNGrams(self, arquivo):
        arquivoString = Util.getStringDeArquivo(arquivo)
        vocabulario = []
        
        # Vai de 0 ate o tamanho da entrada - n+1
        for i in range(len(arquivoString) - self.n + 1):
            termo  = ''.join(arquivoString[i : i + self.n])
            vocabulario.append(termo)
        
        return vocabulario


    # Recupera os L primeiros n-grams mais frequentes do dicionario
    def recuperarLNGrams(self, dicionario, L):
        dicionarioL = {}
        i = 0

        for chave, valor in sorted(dicionario.iteritems(), key=lambda (k, v): v, reverse=True):
            dicionarioL.update({chave : valor})
            i += 1
            if (i == L):
                break
        dicionarioL = sorted(dicionarioL.iteritems(), key=lambda (k, v): v, reverse=True)

        return dict(dicionarioL)


    # Salva o perfil do autor (codigos indexados/dicionario) num arquivo pickle
    def salvarPerfil(self, autor, dicionario):
        f = open(self.dirDosIndices + autor + self.extensaoDosIndices, "wb")
        pickle.dump(dicionario, f)
        f.close()


    # Recupera o dicionario do arquivo pickle passado
    def recuperarDicionario(self, arquivo):
        f = open(arquivo, "rb")
        dicionario = dict(pickle.load(f))
        f.close()

        return dicionario


    def imprimirDiretorioIndexado(self):
        arquivosIndexados = glob.glob(self.dirDosIndices + "*" + self.extensaoDosIndices)
        
        for arquivo in arquivosIndexados:
            print "\n******************************************************************************"
            print "Arquivo: %s" % (arquivo)
            print "**************************"
            f = open(arquivo, "rb")
            dicionario = pickle.load(f)
            f.close()
            
            for chave, valor in sorted(dicionario.iteritems(), key=lambda (k, v): v, reverse=True):
                print "%s: %s" % (chave, valor)
            print "Arquivo: %s" % (arquivo)
            print "**************************"
            print "Quantidade de termos: %s" % (len(dicionario))
            print "******************************************************************************\n"
