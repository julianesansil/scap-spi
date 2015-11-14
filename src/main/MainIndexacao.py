#coding: utf-8

import glob, os
import config
from spi import Preparador, Indexador
from Util import Util


dirBase = config.dirBase[0]
n = config.n[0]
L = config.L[0]
comQuebraLinha = True
comComentariosELiterais = True
comTermos1Ocorrencia = True

preparador = Preparador(config.dirBasePreparada, config.extensaoPadrao, n, comQuebraLinha, comComentariosELiterais)
indexador = Indexador(preparador, L, comTermos1Ocorrencia)

# Antes de iniciar a preparacao dos arquivos, esvazia o diretorio onde os n-grams ficarao
Util.esvaziarDiretorio(config.dirBasePreparada)
# Recupera e salva as caracteristicas relevantes dos arquivos para posterior indexacao
arquivosParaPreparar = glob.glob(os.path.join(dirBase, "*" + config.extensaoAceita))
preparador.prepararArquivos(arquivosParaPreparar)

# Indexa os arquivos do diretorio de acordo com as regras do algoritmo spi
arquivosParaIndexar = glob.glob(os.path.join(config.dirBasePreparada, "*" + config.extensaoPadrao))
# dictPerfilAutores = {"autor", "vocabularioAutorIndexado"}
dictPerfilAutores = indexador.indexarArquivos(arquivosParaIndexar)
# Imprime os arquivos indexados
indexador.imprimirPerfilAutores(dictPerfilAutores)

# Antes de salvar os indides para validacao, esvazia o diretorio onde eles ficarao
Util.esvaziarDiretorio(config.dirIndicesValidacao)
indexador.salvarValidacaoIndices(config.dirIndicesValidacao, dictPerfilAutores, config.extensaoPadrao)
