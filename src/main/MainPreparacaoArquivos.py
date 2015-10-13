#coding: utf-8

import config
from scap.PreparadorArquivos import PreparadorArquivos
from Util import Util


preparadorArquivos = PreparadorArquivos(config.dirNGrams, config.extensaoNGram, config.n)

# Antes de iniciar, esvazia o diretorio onde os n-grams ficarao
Util.esvaziarDiretorio(config.dirNGrams)

# Recupera e salva as caracteristicas relevantes dos arquivos para posterior indexacao
preparadorArquivos.prepararArquivos(config.dirParaPreparar, "*" + config.extensaoAceita)
