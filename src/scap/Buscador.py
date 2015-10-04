'''
Created on 29/09/2015

@author: Juliane
'''

import glob
import pickle
import shutil
import config
from Util import Util


class Buscador():
    
    def __init__(self):
        self.extensaoAceita = config.extensaoAceita
        self.dirParaIndexar = config.dirParaIndexar
        self.dirDosIndices = config.dirDosIndices
        self.extensaoDosIndices = config.extensaoDosIndices

    
    def consultar(self, arquivosBase, indexadorBase, dirParaConsultar, indexadorConsulta):
        # Informacoes do experimento
        numExperimentos = 0
        numAcertos = 0
        autorVerdadeiro = ""
        autorScap = ""
        
        for arquivoRetirado in arquivosBase:
            autorVerdadeiro = Util.getNomeAutor(arquivoRetirado)
            self.reindexarPerfil(arquivoRetirado, dirParaConsultar, indexadorBase)
                        
            # Informacoes da consulta
            arquivoConsulta = dirParaConsultar + Util.getNomeArquivo(arquivoRetirado)
            dicionarioConsulta = {}
            dicionarioConsulta = self.indexarConsulta(indexadorConsulta, arquivoConsulta)
        
            arquivosDosIndices = glob.glob(self.dirDosIndices + "*" + self.extensaoDosIndices)
            maiorSemelhancas = 0
            qtdeSemelhancas = 0
            
            # Compara determinado arquivo com o arquivo-consulta
            for arquivo in arquivosDosIndices:
                dicionarioTemp = self.recuperarArquivoIndexado(arquivo)
            
                qtdeSemelhancas = self.getQtdeSemelhancas(dicionarioConsulta, dicionarioTemp)
                if (qtdeSemelhancas > maiorSemelhancas):
                    maiorSemelhancas = qtdeSemelhancas
                    autor = arquivo
            
            # Retorna o arquivo retirado para a pasta das bases
            shutil.move(arquivoConsulta, self.dirParaIndexar)
         
            autorScap = Util.getNomeAutorTxt(autor)
            print "Autor Verdadeiro: %s" % (autorVerdadeiro)
            print "Autor: %s" % (autorScap)
        
            numExperimentos += 1
            if (autorVerdadeiro == autorScap):
                numAcertos += 1
        
            acuracia = numAcertos/float(numExperimentos)
            print "Numero de experimentos: %s" % (numExperimentos)
            print "Numero de acertos: %s" % (numAcertos)
            print "Acuracia: %f\n" % (acuracia)


    # Re-indexa somente os arquivos do autor do arquivo-consulta
    def reindexarPerfil(self, arquivoConsulta, dirParaConsultar, indexadorBase):
        # Move o arquivo-consulta da pasta base para a de consulta
        shutil.move(arquivoConsulta, dirParaConsultar)
    
        # Exclui o perfil indexado (se houver) do autor do arquivo-consulta
        Util.excluirArquivo(self.dirDosIndices + Util.getNomeAutor(arquivoConsulta) + self.extensaoDosIndices)
        # Re-indexa somente os arquivos deste autor
        indexadorBase.indexar(self.dirParaIndexar, Util.getNomeAutor(arquivoConsulta) + "*" + self.extensaoAceita)


    # Indexa o arquivo de consulta de acordo com as regras do algoritmo scap
    def indexarConsulta(self, indexadorConsulta, arquivoParaConsultar):
        dicionario = {}
        dicionario = indexadorConsulta.separarEmNGrams(arquivoParaConsultar, dicionario)
        dicionario = indexadorConsulta.recuperarLNGrams(dicionario)
        indexadorConsulta.salvarPerfil(dicionario, Util.getNomeAutor(arquivoParaConsultar))
        
        return dicionario


    # Recupera o dicionario do arquivo pickle passado
    def recuperarArquivoIndexado(self, arquivo):
        return dict(pickle.load(open(arquivo, "rb")))


    # Retorna a quantidade de semelhancas de n-grams que tem 2 arquivos
    def getQtdeSemelhancas(self, dicionarioConsulta, dicionarioTemp):
        # Retorna os n-grams que tem na consulta, mas nao tem no dicionario comparado
        diferencaNGrams = set(dicionarioConsulta.keys()) - set(dicionarioTemp.keys())
        qtdeSemelhancas = len(dicionarioConsulta.keys()) - len(diferencaNGrams)
       
        return qtdeSemelhancas
