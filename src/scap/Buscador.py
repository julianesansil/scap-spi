
'''
Created on 29/09/2015
@author: Juliane
'''


class Buscador():

    def __init__(self, indexador, L):
        self.indexador = indexador
        self.L = L


    # Compara o vocabulario indexado do arquivo-consulta com os demais da base
    # E retorna o autor com maior numero de semelhancas de n-grams
    def compararComTodosDaBase(self, arquivoConsulta, dictPerfilAutor):
        vocabularioConsultaIndexado = self.indexador.indexarArquivo(arquivoConsulta)
        #print "vocabulario consulta: ", vocabularioConsultaIndexado
        
        autorScap = ""
        qtdeSemelhancas = 0
        maiorSemelhancas = 0
        
        for autor, vocabularioAutorIndexado in dictPerfilAutor.iteritems():
            #print "vocabulario autor: ", vocabularioAutorIndexado
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
