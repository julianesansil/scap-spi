#coding: utf-8

import glob, os
import config
from scap import Preparador
from Util import Util


dirBase = config.dirBase[0]
n = config.n[0]
comQuebraEspaco = True
comComentariosELiterais = True

preparador = Preparador(config.dirBasePreparada, config.extensaoPadrao, n, comQuebraEspaco, comComentariosELiterais)

# Antes de iniciar a preparacao dos arquivos, esvazia o diretorio onde os n-grams ficarao
Util.esvaziarDiretorio(config.dirBasePreparada)
# Recupera e salva as caracteristicas relevantes dos arquivos para posterior indexacao
arquivosParaPreparar = glob.glob(os.path.join(dirBase, "*" + config.extensaoAceita))
preparador.prepararArquivos(arquivosParaPreparar)
# Imprime os arquivos preparados
preparador.imprimirDiretorioPreparado()
