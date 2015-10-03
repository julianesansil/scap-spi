
from Indexador import Indexador
from Buscador import Buscador
import glob

# Informacao dos codigos
extensaoAceita = ".java"

# Informacoes para indexacao
dirDosIndices = "C:/Users/Juliane/Dropbox/TCC/SCAP-Codigo/util/indices/"
extensaoDosIndices = ".txt"
L = 2000
n = 6

dirParaIndexar = "C:/Users/Juliane/Dropbox/TCC/SCAP-Codigo/util/base/"
dicionario = {}

indexador = Indexador(dirDosIndices, extensaoDosIndices, dirParaIndexar, extensaoAceita, L, n)


# Informacoes para consulta
dirDosIndicesConsulta = "C:/Users/Juliane/Dropbox/TCC/SCAP-Codigo/util/indices-consulta/"

dirParaConsultar = "C:/Users/Juliane/Dropbox/TCC/SCAP-Codigo/util/consulta/"
nomeParaConsultar = "01-consulta"
arquivoParaConsultar = dirParaConsultar + nomeParaConsultar + extensaoAceita
dicionarioConsulta = {}

indexadorConsulta = Indexador(dirDosIndicesConsulta, extensaoDosIndices, dirParaConsultar, extensaoAceita, L, n)
buscador = Buscador()



arquivosDosIndices = glob.glob(dirDosIndices + "*" + extensaoDosIndices)
arquivosParaIndexar = glob.glob(dirParaIndexar + "*" + extensaoAceita)

#INDEXACAO
for arquivo in arquivosParaIndexar:
    dicionario = indexador.recuperarPerfil(indexador.getNomeAutor(arquivo))
    dicionario = indexador.separarEmNGrams(arquivo, dicionario, n)
    dicionario = indexador.recuperarLNGrams(dicionario)
    indexador.salvarPerfil(dicionario, indexador.getNomeAutor(arquivo))

    
#CONSULTA
dicionarioConsulta = buscador.indexarConsulta(indexadorConsulta, arquivoParaConsultar, dicionarioConsulta)

print "Arquivo consulta..."
for key, value in dicionarioConsulta.iteritems():
    print "%s: %s" % (key, value)
print "**************************"
print "Quantidade de termos: %s" % (len(dicionarioConsulta))
print "*************************************************\n"

arquivosDosIndices = glob.glob(dirDosIndices + "*" + extensaoDosIndices)
maiorSemelhancas = 0
qtdeSemelhancas = 0

for arquivo in arquivosDosIndices:
    dicionarioTemp = buscador.recuperarArquivoIndexado(arquivo)
    print "Arquivo..."
    for key, value in dicionarioTemp.iteritems():
        print "%s: %s" % (key, value)

    qtdeSemelhancas = buscador.getQtdeSemelhancas(dicionarioConsulta, dicionarioTemp)
    if (qtdeSemelhancas > maiorSemelhancas):
        maiorSemelhancas = qtdeSemelhancas
        autor = arquivo
    print "**************************"
    print "Semelhancas: %s" % (qtdeSemelhancas)
    print "*************************************************\n"

print "\nAutor: %s" % (buscador.getNomeAutor(autor))
