
'''
Created on 04/10/2015
@author: Juliane
'''

import glob, os, shutil
from Util import Util


class Experimento():
    
    def __init__(self, indexador, buscador):
        self.indexador = indexador
        self.buscador = buscador


    # Compara 1 arquivo-consulta com todos da base, depois outro com todos e assim por diante...
    # Reindexando o perfil do autor desse arquivo antes da comparacao
    # A fim de encontrar o autor do arquivo
    def testar(self, dirBase, dirParaConsultar, finalAceito):
        # Informacoes do experimento
        numExperimentos = 0
        numAcertos = 0
        autorAnterior = ""

        arquivosBase = glob.glob(os.path.join(dirBase, finalAceito))

        for arquivoRetirado in arquivosBase:
            autorVerdadeiro = Util.getNomeAutor(arquivoRetirado)
            autorScap = ""

            if (autorAnterior != "" and autorAnterior != autorVerdadeiro):
                # Reindexa todos os codigos do autor anterior
                self.indexador.indexarDiretorio(os.path.join(dirBase, autorAnterior + finalAceito))
                #print "Autor anterior re-indexado: %s\n" % (autorAnterior)

            # Move o arquivo-consulta do diretorio atual para um de consulta
            shutil.move(arquivoRetirado, dirParaConsultar)
            # Exclui o perfil indexado do autor (se houver) do diretorio de indices
            Util.excluirArquivo(os.path.join(self.indexador.dirIndices, Util.getNomeAutor(arquivoRetirado) + self.indexador.extensaoIndices))
            # Reindexa os codigo deste autor (sem o arquivo retirado)
            self.indexador.indexarDiretorio(os.path.join(dirBase, autorVerdadeiro + finalAceito))
            
            arquivoConsulta = os.path.join(dirParaConsultar, Util.getNomeArquivo(arquivoRetirado))
            # Faz a consulta/comparacao e sugere quem e o autor do arquivo
            autorScap = self.buscador.compararComTodosDaBase(arquivoConsulta)
            
            # Retorna o arquivo retirado para o diretorio das bases
            shutil.move(arquivoConsulta, dirBase)
         
            numExperimentos += 1
            if (autorVerdadeiro == autorScap):
                numAcertos += 1
            acuracia = numAcertos/float(numExperimentos)
            
            autorAnterior = autorVerdadeiro
            
            # self.imprimirResultado(arquivoRetirado, autorVerdadeiro, autorScap, numExperimentos, numAcertos, acuracia)
            # if para imprimir somente o ultimo resultado, ou seja, a acuracia total do algoritmo
            if (numExperimentos == len(arquivosBase)):
                self.imprimirResultado(numExperimentos, numAcertos, acuracia)
        
        return self.guardarResultado(numExperimentos, numAcertos, acuracia)


    #def imprimirResposta(self, arquivoConsulta, autorVerdadeiro, autorScap, numExperimentos, numAcertos, acuracia):
    def imprimirResultado(self, numExperimentos, numAcertos, acuracia):
        #print "Arquivo-consulta: ", arquivoConsulta
        
        #print "Autor verdadeiro re-indexado: ", autorVerdadeiro
        #print "Autor scap: ", autorScap
    
        print "Numero de experimentos: ", numExperimentos
        print "Numero de acertos: ", numAcertos
        print "Acuracia: %f\n" % (acuracia)


    def guardarResultado(self, numExperimentos, numAcertos, acuracia):
        resultado = []
        resultado.append(str(numExperimentos))
        resultado.append(" ")
        resultado.append(str(numAcertos))
        resultado.append(" ")
        resultado.append(str(acuracia))

        return "".join(resultado)
