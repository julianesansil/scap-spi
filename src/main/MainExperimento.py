
import config
from scap.Indexador import Indexador
from scap.Buscador import Buscador
from scap.Experimento import Experimento


indexador = Indexador(config.dirDosIndices)
buscador = Buscador()
experimento = Experimento(indexador, buscador)

# Compara 1 arquivo-consulta com todos da base, depois outro com todos e assim por diante...
# Reindexando o perfil do autor desse arquivo antes da comparacao
# Por fim, o metodo retorna quem ele acha ser o autor do arquivo
experimento.testar(config.dirParaIndexar, config.dirParaConsultar, "*" + config.extensaoAceita)
