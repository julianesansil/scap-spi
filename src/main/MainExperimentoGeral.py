
import config
import os
from scap.Indexador import Indexador
from scap.Buscador import Buscador
from scap.Experimento import Experimento
from Util import Util


indexador = Indexador(config.dirDosIndices)
buscador = Buscador()
experimento = Experimento(indexador, buscador)

if (os.path.isdir(config.dirParaIndexar) and os.path.isdir(config.dirDosIndices) and os.path.isdir(config.dirParaConsultar)):
    # Antes de iniciar a indexacao, esvazia o diretorio onde os indices ficaram
    Util.esvaziarDiretorio(config.dirDosIndices)
    
    # Indexa os arquivos do diretorio de acordo com as regras do algoritmo scap
    indexador.indexarDiretorio(config.dirParaIndexar, config.extensaoAceita)
    # Imprime os arquivos indexados
    indexador.imprimirIndices()
    
    # Compara 1 arquivo-consulta com todos da base, depois outro com todos e assim por diante...
    # Reindexando o perfil do autor desse arquivo antes da comparacao
    # Por fim, o metodo retorna quem ele acha ser o autor do arquivo
    experimento.testar(config.dirParaIndexar, config.dirParaConsultar, config.extensaoAceita)

else: print("Verifique se o diretorio dos indices, da base e o de consulta existem")
