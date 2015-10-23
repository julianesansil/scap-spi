
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
    def executar(base, listN, listL, comConsultaRetirada, comQuebraLinha, comComentariosELiterais, comTermos1Ocorrencia):
        resultadosExperimentos = []
        
        for n in listN:
            preparador = Preparador(config.dirBasePreparada, config.extensaoParaSalvar, n, comQuebraLinha, comComentariosELiterais)
            
            # Antes de iniciar a preparacao dos arquivos, esvazia o diretorio onde os n-grams ficarao
            Util.esvaziarDiretorio(config.dirBasePreparada)
            # Recupera e salva as caracteristicas relevantes dos arquivos para posterior indexacao
            preparador.prepararDiretorio(os.path.join(base, "*" + config.extensaoAceita))
            
            for L in listL:
                indexador = Indexador(preparador, L, comTermos1Ocorrencia)
                buscador = Buscador(indexador, L)
                experimento = Experimento(indexador, buscador, comConsultaRetirada)
                
                if (comComentariosELiterais):
                    print "COM comentarios e literais"
                else: print "SEM comentarios e literais"
                
                if (comTermos1Ocorrencia):
                    print "COM termos com 1 ocorrencia"
                else: print "SEM termos com 1 ocorrencia"
                
                print "Para n = ", n
                print "Para L = ", L
                print "=> RESULTADO <="
                
                # Indexa os arquivos do diretorio de acordo com as regras do algoritmo scap
                dictPerfilAutores = indexador.indexarDiretorio(os.path.join(config.dirBasePreparada, "*" + config.extensaoParaSalvar))
                # Antes de salvar os indides para validacao, esvazia o diretorio onde eles ficarao
                Util.esvaziarDiretorio(config.dirIndicesValidacao)
                indexador.salvarValidacaoIndices(config.dirIndicesValidacao, dictPerfilAutores, config.extensaoParaSalvar)
                
                # Compara 1 arquivo-consulta com todos da base, depois outro com todos e assim por diante...
                # Reindexando o perfil do autor desse arquivo antes da comparacao
                # A fim de encontrar o autor do arquivo
                # resultadoExperimento = numExperimentos + numAcertos + acuracia
                resultadoExperimento = experimento.testar(dictPerfilAutores, config.dirBasePreparada, "*" + config.extensaoParaSalvar)
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
