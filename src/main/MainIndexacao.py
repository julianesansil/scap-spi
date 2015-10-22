#coding: utf-8

import os
import config
from scap import Preparador, Indexador
from Util import Util


preparador = Preparador(config.dirNGrams, config.extensaoPadrao, config.n, True)
indexador = Indexador(preparador, config.dirIndices, config.extensaoPadrao, config.L, True)

# Antes de iniciar a indexacao, esvazia o diretorio onde os indices ficarao
Util.esvaziarDiretorio(config.dirIndices)
# Antes de iniciar a indexacao, esvazia o diretorio onde os indices de validacao ficarao
Util.esvaziarDiretorio(config.dirIndicesValidacao)

# Indexa os arquivos do diretorio de acordo com as regras do algoritmo scap
indexador.indexarDiretorio(os.path.join(config.dirParaIndexar, "*" + config.extensaoPadrao))
# Imprime os arquivos indexados
indexador.imprimirDiretorioIndexado()
indexador.salvarDiretorioIndexado(config.dirIndicesValidacao)
