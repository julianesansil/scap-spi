
import os
import config
from datetime import datetime
from main.ExecucaoExperimento import ExecucaoExperimento


listBase = config.dirBase
listN = config.n
listL = config.L
comConsultaRetirada = config.comConsultaRetirada
comQuebraLinha = config.comQuebraLinha

for base in listBase:

    if (os.path.isdir(base) and os.path.isdir(config.dirResultados) and os.path.isdir(config.dirIndicesValidacao)):
        dataInicial = datetime.now()
        resultadosExperimentos = []
    
        print "******************************************************************************"
        print "DIRETORIO-BASE: ", base
        print "******************************************************************************\n"
        
        comComentariosELiterais = True
        comTermos1Ocorrencia = True
        resultadosExperimentos.append(ExecucaoExperimento.executar(base, listN, listL, comConsultaRetirada, comQuebraLinha, comComentariosELiterais, comTermos1Ocorrencia))
        resultadosExperimentos.append("\n")

        comComentariosELiterais = False
        comTermos1Ocorrencia = True
        resultadosExperimentos.append(ExecucaoExperimento.executar(base, listN, listL, comConsultaRetirada, comQuebraLinha, comComentariosELiterais, comTermos1Ocorrencia))
        resultadosExperimentos.append("\n")
        
        comComentariosELiterais = True
        comTermos1Ocorrencia = False
        resultadosExperimentos.append(ExecucaoExperimento.executar(base, listN, listL, comConsultaRetirada, comQuebraLinha, comComentariosELiterais, comTermos1Ocorrencia))
        resultadosExperimentos.append("\n")
        
        comComentariosELiterais = False
        comTermos1Ocorrencia = False
        resultadosExperimentos.append(ExecucaoExperimento.executar(base, listN, listL, comConsultaRetirada, comQuebraLinha, comComentariosELiterais, comTermos1Ocorrencia))
        resultadosExperimentos.append("\n")
    
        nomeBase = base.split("/")
        nomeBase = nomeBase[len(nomeBase)-2]
        ExecucaoExperimento.salvarResultado(config.dirResultados, "".join(resultadosExperimentos), nomeBase, config.extensaoParaSalvar)
        
        dataFinal = datetime.now()
        tempo = dataFinal - dataInicial
        print "Data inicial:" , dataInicial
        print "Data final:" , dataFinal
        print "Tempo: ", tempo
        
        print "[FIM DA BASE]"
        print "******************************************************************************\n"
    
    else: print "Verifique se o diretorio dos indices, da base e o de consulta existem"
