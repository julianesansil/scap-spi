
# Informacoes para o algoritmo
n = [6, 10, 14]             # Tamanho n do n-gram = tamanho do termo
L = [0, 2000]               # Tamanho L = quantidade de termos analisados
comConsultaRetirada = True  # Retira ou nao o arquivo-consulta da base na comparacao
comQuebraLinha = True       # Considera ou nao as quebras de linha (LF, CR) na leitura do arquivo

# Extensao e diretorios utilizados na preparacao, indexacao e consulta dos arquivos
extensaoAceita = ""
dirBase = ["S:/Dropbox/TCC/Codigo/util/base/b1/", "S:/Dropbox/TCC/Codigo/util/base/b2/", "S:/Dropbox/TCC/Codigo/util/base/b3/"]
#dirBase = ["S:/Dropbox/TCC/Codigo/util/base/b1/"]
dirBasePreparada = "S:/Dropbox/TCC/Codigo/util/n-grams/"

# Extensao e diretorios utilizados para salvar os resultados
extensaoPadrao = ".txt"
dirResultados = "S:/Dropbox/TCC/Codigo/util/resultados/spi/com_consulta_retirada/outros/"
dirIndicesValidacao = "S:/Dropbox/TCC/Codigo/util/indices/"
