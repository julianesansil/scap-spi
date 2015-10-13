#coding: utf-8

import config
from scap.Indexador import Indexador
from Util import Util


indexador = Indexador(config.dirIndices, config.extensaoIndice, config.L)

# Antes de iniciar a indexacao, esvazia o diretorio onde os indices ficarao
Util.esvaziarDiretorio(config.dirIndices)

# Indexa os arquivos do diretorio de acordo com as regras do algoritmo scap
indexador.indexarDiretorio(config.dirNGrams, "*" + config.extensaoNGram)
# Imprime os arquivos indexados
indexador.imprimirDiretorioIndexado()
