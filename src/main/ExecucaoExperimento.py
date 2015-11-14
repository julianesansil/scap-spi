
'''
Created on 20/10/2015
@author: Juliane
'''

import glob, os
import config
from spi import Preparador, Indexador, Buscador, Experimento
from Util import Util


class ExecucaoExperimento():
    
    # Dado um conjunto de parametros para experimento, testa as possibilidades e retorna um resultado
    @staticmethod
    def executar(dirBase, listN, listL, comConsultaRetirada, comQuebraLinha, comComentariosELiterais, comTermos1Ocorrencia):
        resultadosExperimentos = []
        
        for n in listN:
            preparador = Preparador(config.dirBasePreparada, config.extensaoPadrao, n, comQuebraLinha, comComentariosELiterais)
            # Configura o preparador da consulta (o baseline e comComentariosELiterais = False)
            preparadorConsulta = Preparador(config.dirBasePreparada, config.extensaoPadrao, n, comQuebraLinha, False)
            
            # Antes de iniciar a preparacao dos arquivos, esvazia o diretorio onde os n-grams ficarao
            Util.esvaziarDiretorio(config.dirBasePreparada)
            # Recupera e salva as caracteristicas relevantes dos arquivos para posterior indexacao
            arquivosParaPreparar = glob.glob(os.path.join(dirBase, "*" + config.extensaoAceita))
            preparador.prepararArquivos(arquivosParaPreparar)
            
            for L in listL:
                indexador = Indexador(preparador, L, comTermos1Ocorrencia)
                # Configura o indexador da consulta (o baseline e comTermos1Ocorrencia = True)
                indexadorConsulta = Indexador(preparadorConsulta, L, True)
                buscador = Buscador(preparadorConsulta, indexadorConsulta)
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
                
                # Indexa os arquivos do diretorio de acordo com as regras do algoritmo spi
                arquivosParaIndexar = glob.glob(os.path.join(config.dirBasePreparada, "*" + config.extensaoPadrao))
                # dictPerfilAutores = {"autor", "vocabularioAutorIndexado"}
                dictPerfilAutores = indexador.indexarArquivos(arquivosParaIndexar)
                
                # Antes de salvar os indides para validacao, esvazia o diretorio onde eles ficarao
                Util.esvaziarDiretorio(config.dirIndicesValidacao)
                indexador.salvarValidacaoIndices(config.dirIndicesValidacao, dictPerfilAutores, config.extensaoPadrao)
                
                # Compara 1 arquivo-consulta com todos da base, depois outro com todos e assim por diante...
                # Reindexando o perfil do autor desse arquivo antes da comparacao
                # A fim de encontrar o autor do arquivo
                arquivosConsulta = glob.glob(os.path.join(dirBase, "*" + config.extensaoAceita))
                # resultadoExperimento = numExperimentos + numAcertos + acuracia
                resultadoExperimento = experimento.testar(arquivosConsulta, dictPerfilAutores, config.dirBasePreparada, config.extensaoPadrao)
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
    def salvarResultado(dirResultados, resultado, nomedirBase, extensao):
        print os.path.join(dirResultados, nomedirBase + extensao)
        Util.salvarArquivo(os.path.join(dirResultados, nomedirBase + extensao), resultado)
