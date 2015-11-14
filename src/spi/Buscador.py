
'''
Created on 29/09/2015
@author: Juliane
'''


class Buscador():

    def __init__(self, preparador, indexador):
        self.preparador = preparador
        self.indexador = indexador


    # Compara o vocabulario indexado do arquivo-consulta com os demais da base
    # E retorna o autor com maior numero de semelhancas de n-grams
    def compararComTodosDaBase(self, arquivoConsulta, dictPerfilAutor):
        nGramsConsulta = self.preparador.prepararArquivo(arquivoConsulta)
        vocabularioConsultaIndexado = self.indexador.indexarNGrams(nGramsConsulta)
        if (self.indexador.L > 0):
                # Atualiza o dicionario com os L n-grams mais frequentes
                vocabularioConsultaIndexado = self.indexador.recuperarLNGrams(vocabularioConsultaIndexado, self.indexador.L)
        #print "Vocabulario-consulta indexado: ", vocabularioConsultaIndexado
        
        autorScap = ""
        qtdeSemelhancas = 0
        maiorSemelhancas = 0
        
        for autor, vocabularioAutorIndexado in dictPerfilAutor.iteritems():
            #print "Vocabulario-autor indexado: ", vocabularioAutorIndexado
            qtdeSemelhancas = self.getQtdeSemelhancas(vocabularioConsultaIndexado, vocabularioAutorIndexado)
            
            if (qtdeSemelhancas >= maiorSemelhancas):
                maiorSemelhancas = qtdeSemelhancas
                autorScap = autor
        
        return autorScap


    # Retorna a quantidade de semelhancas de n-grams que tem 2 arquivos
    def getQtdeSemelhancas(self, dictConsulta, dictTemp):
        # Retorna os n-grams que tem na consulta, mas nao tem no dicionario comparado
        diferencaNGrams = set(dictConsulta.keys()) - set(dictTemp.keys())
        #print "diferenca (consulta - autor): ", diferencaNGrams
        qtdeSemelhancas = len(dictConsulta.keys()) - len(diferencaNGrams)
        
        return qtdeSemelhancas
