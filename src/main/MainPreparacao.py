#coding: utf-8

import os
import config
from scap import Preparador
from Util import Util


preparador = Preparador(config.dirNGrams, config.extensaoPadrao, config.n, True)

# Antes de iniciar, esvazia o diretorio onde os n-grams ficarao
Util.esvaziarDiretorio(config.dirNGrams)

# Recupera e salva as caracteristicas relevantes dos arquivos para posterior indexacao
preparador.prepararDiretorio(os.path.join(config.dirParaPreparar, "*" + config.extensaoAceita))
# Imprime os arquivos preparados
preparador.imprimirDiretorioPreparado()
