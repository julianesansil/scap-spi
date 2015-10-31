
import os
import config
from datetime import datetime
from main.ExecucaoExperimento import ExecucaoExperimento


listBase = config.dirBase
listN = config.n
listL = config.L
comConsultaRetirada = config.comConsultaRetirada
comQuebraLinha = config.comQuebraLinha

for dirBase in listBase:

    if (os.path.isdir(dirBase) and os.path.isdir(config.dirResultados) and os.path.isdir(config.dirIndicesValidacao)):
        dataInicial = datetime.now()
        resultadosExperimentos = []
    
        print "******************************************************************************"
        print "DIRETORIO-BASE: ", dirBase
        print "******************************************************************************\n"
        
        comComentariosELiterais = True
        comTermos1Ocorrencia = True
        resultadosExperimentos.append(ExecucaoExperimento.executar(dirBase, listN, listL, comConsultaRetirada, comQuebraLinha, comComentariosELiterais, comTermos1Ocorrencia))
        resultadosExperimentos.append("\n")

        comComentariosELiterais = False
        comTermos1Ocorrencia = True
        resultadosExperimentos.append(ExecucaoExperimento.executar(dirBase, listN, listL, comConsultaRetirada, comQuebraLinha, comComentariosELiterais, comTermos1Ocorrencia))
        resultadosExperimentos.append("\n")
        
        comComentariosELiterais = True
        comTermos1Ocorrencia = False
        resultadosExperimentos.append(ExecucaoExperimento.executar(dirBase, listN, listL, comConsultaRetirada, comQuebraLinha, comComentariosELiterais, comTermos1Ocorrencia))
        resultadosExperimentos.append("\n")
        
        comComentariosELiterais = False
        comTermos1Ocorrencia = False
        resultadosExperimentos.append(ExecucaoExperimento.executar(dirBase, listN, listL, comConsultaRetirada, comQuebraLinha, comComentariosELiterais, comTermos1Ocorrencia))
        resultadosExperimentos.append("\n")
    
        nomedirBase = dirBase.split("/")
        nomedirBase = nomedirBase[len(nomedirBase)-2]
        ExecucaoExperimento.salvarResultado(config.dirResultados, "".join(resultadosExperimentos), nomedirBase, config.extensaoPadrao)
        
        dataFinal = datetime.now()
        tempo = dataFinal - dataInicial
        print "Data inicial:" , dataInicial
        print "Data final:" , dataFinal
        print "Tempo: ", tempo
        
        print "[FIM DA BASE]"
        print "******************************************************************************\n"
    
    else: print "Verifique se o diretorio dos indices, da base e o de consulta existem"
