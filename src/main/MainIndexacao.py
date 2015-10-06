
import config
from scap.Indexador import Indexador


indexador = Indexador(config.dirDosIndices)

# Indexa os arquivos do diretorio de acordo com as regras do algoritmo scap
indexador.indexarDiretorio(config.dirParaIndexar, "*" + config.extensaoAceita)
# Imprime os arquivos indexados
indexador.imprimirIndices()
