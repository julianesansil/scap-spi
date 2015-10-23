#coding: utf-8

import os
import config
from scap import Preparador
from Util import Util


n = config.n[0]
comQuebraEspaco = True
comComentariosELiterais = True

preparador = Preparador(config.dirBasePreparada, config.extensaoParaSalvar, n, comQuebraEspaco, comComentariosELiterais)

# Antes de iniciar a preparacao dos arquivos, esvazia o diretorio onde os n-grams ficarao
Util.esvaziarDiretorio(config.dirBasePreparada)
# Recupera e salva as caracteristicas relevantes dos arquivos para posterior indexacao
preparador.prepararDiretorio(os.path.join(config.dirBase, "*" + config.extensaoAceita))
# Imprime os arquivos preparados
preparador.imprimirDiretorioPreparado()
