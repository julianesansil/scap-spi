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
        arquivosBase = glob.glob(dirParaIndexar + finalAceito)
        
        # Informacoes do experimento
        numExperimentos = 0
        numAcertos = 0
        autorAnterior = ""

        for arquivoRetirado in arquivosBase:
            autorVerdadeiro = Util.getNomeAutor(arquivoRetirado)
            autorScap = ""
        
            # Reindexa os codigo deste autor (sem o arquivo retirado)
            self.indexador.reindexarPerfil(arquivoRetirado, dirParaIndexar, dirParaConsultar, finalAceito)
            if (autorAnterior != "" and autorAnterior != autorVerdadeiro):
                # Reindexa todos os codigos do autor anterior
                self.indexador.indexarDiretorio(dirParaIndexar, autorAnterior + finalAceito)

            arquivoConsulta = dirParaConsultar + Util.getNomeArquivo(arquivoRetirado)
            # Faz a consulta/comparacao e sugere quem e o autor do arquivo
            autorScap = self.buscador.compararComTodosDaBase(arquivoConsulta, self.indexador)
            
            # Retorna o arquivo retirado para o diretorio das bases
            shutil.move(arquivoConsulta, dirParaIndexar)
         
            numExperimentos += 1
            if (autorVerdadeiro == autorScap):
                numAcertos += 1
            acuracia = numAcertos/float(numExperimentos)
            
            autorAnterior = autorVerdadeiro
            self.imprimirResposta(arquivoRetirado, autorVerdadeiro, autorScap, numExperimentos, numAcertos, acuracia)


    def imprimirResposta(self, arquivoConsulta, autorVerdadeiro, autorScap, numExperimentos, numAcertos, acuracia):
        print arquivoConsulta

        print "Autor verdadeiro: %s" % (autorVerdadeiro)
        print "Autor scap: %s" % (autorScap)
    
        print "Numero de experimentos: %s" % (numExperimentos)
        print "Numero de acertos: %s" % (numAcertos)
        print "Acuracia: %f\n" % (acuracia)
