
import glob
import shutil

from Indexador import Indexador
from Buscador import Buscador
from Util import Util


# Informacao dos codigos
extensaoAceita = ".java"
util = Util()

# Informacoes para indexacao
dirDosIndices = "C:/Users/Juliane/Dropbox/TCC/SCAP-Codigo/util/indices/"
extensaoDosIndices = ".txt"
L = 2000
n = 6

dirBase = "C:/Users/Juliane/Dropbox/TCC/SCAP-Codigo/util/base/"
dicionario = {}

indexador = Indexador(dirDosIndices, extensaoDosIndices, dirBase, extensaoAceita, L, n)


# Informacoes para consulta
dirDosIndicesConsulta = "C:/Users/Juliane/Dropbox/TCC/SCAP-Codigo/util/indices-consulta/"

dirParaConsultar = "C:/Users/Juliane/Dropbox/TCC/SCAP-Codigo/util/consulta/"
arquivoParaConsultar = ""
dicionarioConsulta = {}

indexadorConsulta = Indexador(dirDosIndicesConsulta, extensaoDosIndices, dirParaConsultar, extensaoAceita, L, n)
buscador = Buscador()


# Informacoes do autor
autorVerdadeiro = ""
autorScap = ""

#INDEXACAO
# arquivosDosIndices = glob.glob(dirDosIndices + "*" + extensaoDosIndices)
arquivosBase = glob.glob(dirBase + "*" + extensaoAceita)

for arquivoRetirado in arquivosBase:
    # Move o arquivo escolhido da pasta das bases para a de consulta
    shutil.move(arquivoRetirado, dirParaConsultar)
    autorVerdadeiro = util.getNomeAutor(arquivoRetirado)

    # Exclui o perfil indexado daquele autor (se houver)
    util.excluirArquivo(dirDosIndices + autorVerdadeiro + extensaoDosIndices)
    # Re-indexa somente os arquivos daquele autor
    arquivosParaIndexar = glob.glob(dirBase + autorVerdadeiro + "*" + extensaoAceita)

    for arquivo in arquivosParaIndexar:
        dicionario = indexador.recuperarPerfil(util.getNomeAutor(arquivo))
        dicionario = indexador.separarEmNGrams(arquivo, dicionario, n)
        dicionario = indexador.recuperarLNGrams(dicionario)
        indexador.salvarPerfil(dicionario, util.getNomeAutor(arquivo))
    
    
    #CONSULTA
    arquivoParaConsultar = dirParaConsultar + util.getNomeArquivo(arquivoRetirado)
    dicionarioConsulta = {}
    dicionarioConsulta = buscador.indexarConsulta(indexadorConsulta, arquivoParaConsultar, dicionarioConsulta)

    arquivosDosIndices = glob.glob(dirDosIndices + "*" + extensaoDosIndices)
    maiorSemelhancas = 0
    qtdeSemelhancas = 0
    
    for arquivo in arquivosDosIndices:
        dicionarioTemp = buscador.recuperarArquivoIndexado(arquivo)
    
        qtdeSemelhancas = buscador.getQtdeSemelhancas(dicionarioConsulta, dicionarioTemp)
        if (qtdeSemelhancas > maiorSemelhancas):
            maiorSemelhancas = qtdeSemelhancas
            autor = arquivo
    
    print "Autor Verdadeiro: %s" % (autorVerdadeiro)
    print "Autor: %s\n\n" % (util.getNomeAutor(autor))
    
    # Retorna o arquivo retirado para a pasta das bases
    shutil.move(arquivoParaConsultar, dirBase)
