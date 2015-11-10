
'''
Created on 04/10/2015
@author: Juliane
'''

import glob, os
from Util import Util


class Experimento():

    def __init__(self, indexador, buscador, comConsultaRetirada):
        self.indexador = indexador
        self.buscador = buscador
        self.comConsultaRetirada = comConsultaRetirada


    # Compara 1 arquivo-consulta com todos da base, depois outro com todos e assim por diante...
    # Reindexando o perfil do autor desse arquivo antes da comparacao
    # A fim de encontrar o autor do arquivo
    def testar(self, arquivosConsulta, dictPerfilAutor, dirBasePreparada, extensaoPadrao):
        # Informacoes do experimento
        numExperimentos = 0
        numAcertos = 0
        autorAnterior = ""
        
        for arquivoConsulta in arquivosConsulta:
            autorVerdadeiro = Util.getNomeAutor(arquivoConsulta)
            
            # Se (comConsultaRetirada = True), retira o arquivo-consulta da base para nao constar na comparacao
            if (self.comConsultaRetirada):
                if (autorAnterior != "" and autorAnterior != autorVerdadeiro):
                    # Reindexa todos os codigos do autor anterior
                    arquivosParaIndexar = glob.glob(os.path.join(dirBasePreparada, autorAnterior + "*" + extensaoPadrao))
                    vocabularioAutorAnteriorIndexado = self.indexador.indexarArquivos(arquivosParaIndexar)
                    vocabularioAutorAnteriorIndexado = dict(vocabularioAutorAnteriorIndexado[autorAnterior])
                    dictPerfilAutor[autorAnterior] = vocabularioAutorAnteriorIndexado
                
                # Reindexa os codigo deste autor (sem o arquivoParaRetirar)
                arquivosParaIndexar = glob.glob(os.path.join(dirBasePreparada, autorVerdadeiro + "*" + extensaoPadrao))
                arquivoParaRetirar = Util.getNomeArquivo(arquivoConsulta)
                arquivoParaRetirar = dirBasePreparada[0:len(dirBasePreparada)-1] + "\\" + arquivoParaRetirar + extensaoPadrao

                vocabularioAutorIndexado = self.indexador.indexarArquivosSemArquivoEspecifico(arquivosParaIndexar, arquivoParaRetirar)
                vocabularioAutorIndexado = dict(vocabularioAutorIndexado[autorVerdadeiro])
                dictPerfilAutor[autorVerdadeiro] = vocabularioAutorIndexado
                
                # Verifica a presenca de termos com 1 ocorrencia na base indexada
                #for autor, ngramsIndexado in dictPerfilAutor.iteritems():
                #    for ngrams, frequencia in ngramsIndexado.iteritems():
                #        if (frequencia == 1):
                #            print "igual a 1"
                #            print autor
                #            print ngrams, " : " , frequencia
            
            # Faz a consulta/comparacao e sugere quem e o autor do arquivo
            autorScap = self.buscador.compararComTodosDaBase(arquivoConsulta, dictPerfilAutor)
            
            numExperimentos += 1
            if (autorVerdadeiro == autorScap):
                numAcertos += 1
            acuracia = numAcertos/float(numExperimentos)
            
            autorAnterior = autorVerdadeiro
            
            #self.imprimirResultado(arquivoConsulta, autorVerdadeiro, autorScap, numExperimentos, numAcertos, acuracia)
            # if para imprimir somente o ultimo resultado, ou seja, a acuracia total do algoritmo
            if (numExperimentos == len(arquivosConsulta)):
                self.imprimirResultado(numExperimentos, numAcertos, acuracia)
        
        return self.guardarResultado(numExperimentos, numAcertos, acuracia)


    #def imprimirResultado(self, arquivoConsulta, autorVerdadeiro, autorScap, numExperimentos, numAcertos, acuracia):
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
