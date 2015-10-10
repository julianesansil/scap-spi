
import config
from scap.Indexador import Indexador
from Util import Util


indexador = Indexador(config.dirIndices, config.extensaoIndice, config.n)

# Antes de iniciar a indexacao, esvazia o diretorio onde os indices ficarao
Util.esvaziarDiretorio(config.dirIndices)

# Indexa os arquivos do diretorio de acordo com as regras do algoritmo scap
indexador.indexarDiretorio(config.dirParaIndexar, "*" + config.extensaoAceita)
# Imprime os arquivos indexados
indexador.imprimirDiretorioIndexado()
