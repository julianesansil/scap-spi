
'''
Created on 20/10/2015
@author: Juliane
'''

import os
import config
from scap import Preparador, Indexador, Buscador, Experimento
from Util import Util


class ExecucaoExperimento():
    
    # Dado um conjunto de parametros para experimento, testa as possibilidades e retorna um resultado
    @staticmethod
    def executar(listN, listL, comComentariosELiterais, comTermos1Ocorrencia):
        resultadosExperimentos = []
        
        for n in listN:
            preparador = Preparador(config.dirNGrams, config.extensaoPadrao, n, comComentariosELiterais)
            
            # Antes de iniciar a preparacao dos arquivos, esvazia o diretorio onde os n-grams ficarao
            Util.esvaziarDiretorio(config.dirNGrams)
            
            # Recupera e salva as caracteristicas relevantes dos arquivos para posterior indexacao
            preparador.prepararDiretorio(os.path.join(config.dirParaPreparar, "*" + config.extensaoAceita))        
            
            for L in listL:
                if (comComentariosELiterais):
                    print "COM comentarios e literais"
                else: print "SEM comentarios e literais"
                
                if (comTermos1Ocorrencia):
                    print "COM termos com 1 ocorrencia"
                else: print "SEM termos com 1 ocorrencia"
                
                print "Para n = ", n
                print "Para L = ", L
                print "=> RESULTADO <="
                
                indexador = Indexador(preparador, config.dirIndices, config.extensaoPadrao, L, comTermos1Ocorrencia)
                buscador = Buscador(indexador, L)
                experimento = Experimento(indexador, buscador)
                
                # Antes de iniciar a indexacao, esvazia o diretorio onde os indices e os indices de validacao ficarao
                Util.esvaziarDiretorio(config.dirIndices)
                Util.esvaziarDiretorio(config.dirIndicesValidacao)
                # Antes de iniciar o teste, esvazia o diretorio onde o arquivo-consulta ficara
                Util.esvaziarDiretorio(config.dirParaConsultar)
                
                # Indexa os arquivos do diretorio de acordo com as regras do algoritmo scap
                indexador.indexarDiretorio(os.path.join(config.dirParaIndexar, "*" + config.extensaoPadrao))
                # Imprime os arquivos indexados
                # indexador.imprimirDiretorioIndexado()
                
                # Compara 1 arquivo-consulta com todos da base, depois outro com todos e assim por diante...
                # Reindexando o perfil do autor desse arquivo antes da comparacao
                # A fim de encontrar o autor do arquivo
                # resultadoExperimento = numExperimentos + numAcertos + acuracia
                resultadoExperimento = experimento.testar(config.dirParaIndexar, config.dirParaConsultar, "*" + config.extensaoPadrao)
                resultadosExperimentos.append(ExecucaoExperimento.guardarResultado(n, L, comComentariosELiterais, comTermos1Ocorrencia, resultadoExperimento))
                
            print "[FIM DO n]"
            print "******************************************************************************\n"
        print "[FIM DO TESTE]"
        print "******************************************************************************\n"
        return "".join(resultadosExperimentos)

    @staticmethod
    def guardarResultado(n, L, comComentariosELiterais, comTermos1Ocorrencia, resultadoExperimento):
        resultado = []

        resultado.append(str(n))
        resultado.append(" ")
        
        resultado.append(str(L))
        resultado.append(" ")
        
        if (comComentariosELiterais):
            resultado.append("Sim")
        else: resultado.append("Nao")
        resultado.append(" ")
        
        if (comTermos1Ocorrencia):
            resultado.append("Sim")
        else: resultado.append("Nao")
        resultado.append(" ")
        
        resultado.append(resultadoExperimento)
        resultado.append("\n")
        
        return "".join(resultado)


    @staticmethod
    def salvarResultado(dirResultados, resultado, nomeBase, extensao):
        print os.path.join(dirResultados, nomeBase + extensao)
        Util.salvarArquivo(os.path.join(dirResultados, nomeBase + extensao), resultado)
