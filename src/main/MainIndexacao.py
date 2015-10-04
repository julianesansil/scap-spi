
import config
from scap.Indexador import Indexador


indexadorBase = Indexador(config.dirDosIndices)

# Indexa os arquivos do diretorio de acordo com as regras do algoritmo scap
indexadorBase.indexar(config.dirParaIndexar, "*" + config.extensaoAceita)
# Imprime os arquivos indexados
indexadorBase.imprimirIndices()
