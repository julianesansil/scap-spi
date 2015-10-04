
import glob
import config
from scap.Indexador import Indexador
from scap.Buscador import Buscador


arquivosBase = glob.glob(config.dirParaIndexar + "*" + config.extensaoAceita)
indexadorBase = Indexador(config.dirDosIndices)
indexadorConsulta = Indexador(config.dirDosIndicesConsulta)
buscador = Buscador()

# Retorna o arquivo com maior semelhancas de n-grams comparando ao arquivo-consulta
buscador.consultar(arquivosBase, indexadorBase, config.dirParaConsultar, indexadorConsulta)
