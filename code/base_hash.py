""" 
Trabalho de Implementação de Hash de Banco de Dados II

Algoritmo de base para o hash

Autores:
Clara Araújo Maia - RA: 0065609
Nicolas Augusto Montovani - RA: 0065527
"""
class Bucket:
    """ 
    Classe Bucket que cria uma base para realizar o algoritmo de hash linear
    """
    def __init__(self, tamanho):
        """
        Construtor parametrizado da classe Bucket

        Args:
            tamanho: tamanho dos registros que o bucket suporta (sem overflow)
        """
        self.tamanho = tamanho
        
        #Lista de overflow
        self.overflow = [] 
        
        #Determina se o bucket é overflow
        self.e_overflow = False
        
        #Lista de registros agrupados
        self.registros = []
    #enddef
    
    def vazio(self):
        """
        Função que verifica se o bucket está vazio

        Returns:
            True/False -> se o bucket está vazio
        """
        return len(self.registros) == 0
    #enddef
    
    def cheio(self):
        """
        Função que verifica se o bucket está cheio

        Returns:
            True/False -> se o bucket está cheio
        """
        return len(self.registros) == self.tamanho
    #enddef
    
    def getOverflow(self):
        """
        Função que pega o overflow do hash, verificando se ele é ou não um overflow

        Returns:
            True/False -> se o bucket é overflow
        """
        return self.e_overflow
    #enddef
     
    def setOverflow(self, e_overflow):
        """
        Determina o overflow do bucket

        Args:
            e_overflow: determina se é overflow ou não
        """
        self.e_overflow = e_overflow
    #enddef
#endclass