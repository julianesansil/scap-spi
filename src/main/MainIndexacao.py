#coding: utf-8

import os
import config
from scap import Preparador, Indexador
from Util import Util


n = config.n[0]
L = config.L[0]
comQuebraLinha = True
comComentariosELiterais = True
comTermos1Ocorrencia = True

preparador = Preparador(config.dirBasePreparada, config.extensaoParaSalvar, n, comQuebraLinha, comComentariosELiterais)
indexador = Indexador(preparador, L, comTermos1Ocorrencia)

# Antes de iniciar a preparacao dos arquivos, esvazia o diretorio onde os n-grams ficarao
Util.esvaziarDiretorio(config.dirBasePreparada)
# Recupera e salva as caracteristicas relevantes dos arquivos para posterior indexacao
preparador.prepararDiretorio(os.path.join(config.dirBase, "*" + config.extensaoAceita))

# Indexa os arquivos do diretorio de acordo com as regras do algoritmo scap
# dictPerfilAutores = {"autor", "vocabularioAutorIndexado"}
dictPerfilAutores = indexador.indexarDiretorio(os.path.join(config.dirBasePreparada, "*" + config.extensaoParaSalvar))
# Imprime os arquivos indexados
indexador.imprimirPerfilAutores(dictPerfilAutores)

# Antes de salvar os indides para validacao, esvazia o diretorio onde eles ficarao
Util.esvaziarDiretorio(config.dirIndicesValidacao)
indexador.salvarValidacaoIndices(config.dirIndicesValidacao, dictPerfilAutores, config.extensaoParaSalvar)
