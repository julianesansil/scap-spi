'''
Created on 04/10/2015

@author: Juliane
'''

import glob
import shutil
from Util import Util


class Experimento():
    
    def __init__(self, indexador, buscador):
        self.indexador = indexador
        self.buscador = buscador


    # Compara 1 arquivo-consulta com todos da base, depois outro com todos e assim por diante...
    # Reindexando o perfil do autor desse arquivo antes da comparacao
    def testar(self, dirParaIndexar, dirParaConsultar, finalAceito):
        # Informacoes do experimento
        numExperimentos = 0
        numAcertos = 0
        autorAnterior = ""

        arquivosBase = glob.glob(dirParaIndexar + finalAceito)

        for arquivoRetirado in arquivosBase:
            autorVerdadeiro = Util.getNomeAutor(arquivoRetirado)
            autorScap = ""

            if (autorAnterior != "" and autorAnterior != autorVerdadeiro):
                # Reindexa todos os codigos do autor anterior
                self.indexador.indexarDiretorio(dirParaIndexar, autorAnterior + finalAceito)
                print "Autor anterior re-indexado: %s\n" % (autorAnterior)
            
            # Move o arquivo-consulta do diretorio atual para um de consulta
            shutil.move(arquivoRetirado, dirParaConsultar)
            # Exclui o perfil indexado do autor (se houver) do diretorio de indices
            Util.excluirArquivo(self.indexador.dirDosIndices + Util.getNomeAutor(arquivoRetirado) + self.indexador.extensaoDosIndices)
            # Reindexa os codigo deste autor (sem o arquivo retirado)
            self.indexador.indexarDiretorio(dirParaIndexar, autorVerdadeiro + finalAceito)
            
            arquivoConsulta = dirParaConsultar + Util.getNomeArquivo(arquivoRetirado)
            # Faz a consulta/comparacao e sugere quem e o autor do arquivo
            autorScap = self.buscador.compararComTodosDaBase(arquivoConsulta)
            
            # Retorna o arquivo retirado para o diretorio das bases
            shutil.move(arquivoConsulta, dirParaIndexar)
         
            numExperimentos += 1
            if (autorVerdadeiro == autorScap):
                numAcertos += 1
            acuracia = numAcertos/float(numExperimentos)
            
            autorAnterior = autorVerdadeiro
            self.imprimirResposta(arquivoRetirado, autorVerdadeiro, autorScap, numExperimentos, numAcertos, acuracia)


    def imprimirResposta(self, arquivoConsulta, autorVerdadeiro, autorScap, numExperimentos, numAcertos, acuracia):
        print "Arquivo-consulta: %s" % (arquivoConsulta)
        
        print "Autor verdadeiro re-indexado: %s" % (autorVerdadeiro)
        print "Autor scap: %s" % (autorScap)
    
        print "Numero de experimentos: %s" % (numExperimentos)
        print "Numero de acertos: %s" % (numAcertos)
        print "Acuracia: %f\n" % (acuracia)
