
import os
import config
from main.ExecucaoExperimento import ExecucaoExperimento


listN = [6, 10, 14]
listL = [0, 2000]

if (os.path.isdir(config.dirParaPreparar) and os.path.isdir(config.dirIndices) and os.path.isdir(config.dirParaConsultar)):
    
    resultadosExperimentos = []

    print "******************************************************************************"
    print "DIRETORIO-BASE: ", config.dirParaPreparar
    print "******************************************************************************\n"
    
    comComentariosELiterais = True
    comTermos1Ocorrencia = True
    resultadosExperimentos.append(ExecucaoExperimento.executar(listN, listL, comComentariosELiterais, comTermos1Ocorrencia))
    resultadosExperimentos.append("\n")
    
    comComentariosELiterais = False
    comTermos1Ocorrencia = True
    resultadosExperimentos.append(ExecucaoExperimento.executar(listN, listL, comComentariosELiterais, comTermos1Ocorrencia))
    resultadosExperimentos.append("\n")
    
    comComentariosELiterais = True
    comTermos1Ocorrencia = False
    resultadosExperimentos.append(ExecucaoExperimento.executar(listN, listL, comComentariosELiterais, comTermos1Ocorrencia))
    resultadosExperimentos.append("\n")
    
    comComentariosELiterais = False
    comTermos1Ocorrencia = False
    resultadosExperimentos.append(ExecucaoExperimento.executar(listN, listL, comComentariosELiterais, comTermos1Ocorrencia))
    resultadosExperimentos.append("\n")

    nomeBase = config.dirParaPreparar.split("/")
    nomeBase = nomeBase[len(nomeBase)-2]
    ExecucaoExperimento.salvarResultado(config.dirResultados, "".join(resultadosExperimentos), nomeBase, config.extensaoPadrao)
    
else: print "Verifique se o diretorio dos indices, da base e o de consulta existem"
