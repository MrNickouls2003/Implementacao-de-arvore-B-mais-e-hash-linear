""" 
Trabalho de Implementação de Árvore B+ de Banco de Dados II

Algoritmo de base para a árvore B+

Autores:
Clara Araújo Maia - RA: 0065609
Nicolas Augusto Montovani - RA: 0065527
""" 
from math import ceil

class No:
    def __init__(self, ordem) -> None:
        """
        Construtor parametrizado da classe
        
        Essa classe armazena os registros e índices das páginas não folha da árvore B+
        
        Args:
            ordem: ordem do nó
            eFolha: diz se o nó é ou não folha
            pai: diz qual é o nó pai de um outro nó
            proximo: diz qual nó é o seu sucessor
            anterior: diz qual nó é o seu antecessor
            registros: lista que armazena os registros de um nó
            filhos: lista que armazena os filhos de um nó
        """
        self.ordem = ordem
        self.eFolha = False     
        self.pai = None  
        self.proximo = None
        self.anterior = None
        self.registros = []
        self.filhos = []
    #enddef
    
    def getOrdem(self):
        """
        A ordem nó não folha pode ser maior do que a do nó folha
        
        Returns:
            Ordem do nó, seja ele folha ou não
        """
        return self.ordem
    #enddef
    
    def inserir(self, chave) -> None:
        """
        Insere uma chave em um nó não folha

        Args:
            chave: chave a ser inserida
        """
        if len(self.registros):     #Se existerem registros no nó
            for i, item in enumerate(self.registros):
                if chave < item:    #Se o registro seja menor do que a chave do registro analisado, ele é inserido entre os registros
                    self.registros = self.registros[:i] + [chave] + self.registros[i:]  #Faz-se a inclusão entre registros
                    
                    break
                #endif
                elif i + 1 == len(self.registros):  #Se for a última posição do nó, e não foi encontrado nenhum registro maior, ele é então inserido ao final da folha
                    self.registros.append(chave)
                    
                    break
                #endelif
            #endfor
        #endif
        else:   #Se não existirem registros no nó, insere-se o primeiro registro no final do nó
            self.registros.append(chave)
        #endelse
    #enddef
    
    def inserirFolha(self, chave, registro) -> None:
        """
        Insere um registro em um nó folha

        Args:
            chave: chave a ser inserida
            registro: registro a ser inserido no nó
        """
        if len(self.registros):     #Se existirem registros no nó
            for i, item in enumerate(self.registros):
                if chave < item[0]:     #Se o registro for menor do que a chave do registro analisado, ele é inserido entre os registros
                    self.registros = self.registros[:i] + [registro] + self.registros[i:]   #Faz-se a inclusão entre os registros
                    
                    break
                #endif
                elif i + 1 == len(self.registros):  #Se chegar na última posição do nó e ainda não foi encontrado um registro maior, ele é inserido ao final da folha
                    self.registros.append(registro)

                    break
                #endelif
            #endfor
        #endif
        else:   #Se não existerem registros no nó, insere o primeiro registro ao final do nó
            self.registros.append(registro)
        #endelse
    #enddef
    
    def excluir(self, chave) -> None:
        """
        Exclui o registro com uma determinada chave de um nó    

        Args:
            chave: chave que contém o registro a ser excluído
        """
        if len(self.registros):     #Se existerem registros na página
            for i, item in enumerate(self.registros):
                if item[0] == chave:    #Verifica se a chave informada correponde ao índice
                    self.registros.pop(i)   #Apagando o registro daquela posição do nó
                    
                    break
                #endif
            #endfor
        #endif
    #enddef
    
    def rotacionarChaves(self, esquerda, direita, indice, lado):
        """
        Faz a rotação de chaves da árvore. É chamado quando existem vários níveis e é preciso reorganizar os índices das páginas não folha
        
        Args:
            esquerda: nó da esquerda
            direita: nó da direita
            indice: índice da chave
            lado: de qual lado será a rotação (0 = lado esquerdo e 1 = lado direito)
        """
        if lado == 0:   #Rotação realizada pela esquerda
            chave = self.registros.pop(indice)  #Chave do nó pai de uma determinada posição é removida
            direita.inserir(chave)  #Chave removida é inserida no nó a direita
            
            chave = esquerda.registros.pop(-1)  #A chave então recebe a remoção da chave do nó da esquerda
            
            self.inserir(chave)     #Chave removida é inserida no nó pai
            
            no_ = esquerda.filhos.pop(-1)   #Este no_ recebe os filhos do nó esquerdo removido
            no_.pai = direita   #O pai de no_ agora é o nó da direita
            
            direita.filhos = [no_] + direita.filhos     #Os filhos do nó direito são reorganizados e ele recebe os filhos do nó removido
        #endif
        elif lado == 1:     #Rotação realizada pela direita. Mesma lógica, porém muda-se os índices
            chave = self.registros.pop(indice - 1)
            esquerda.inserir(chave)
            
            chave = direita.registros.pop(0)
            
            self.inserir(chave)
            
            no_ = direita.filhos.pop(0)
            no_.pai = esquerda
            
            esquerda.filhos += [no_]    #Inclui os filhos do nó removido ao final do nó esquerdo
        #endelif
    #enddef
    
    def juntar(self, no):
        """
        Realiza a fusão/junção dos nós
        
        Args:
            no: nó a ser fundido

        Returns:
            Árvore atualizada
        """
        self.registros += no.registros  #Nó que chama a fusão recebe as chaves do outro nó
        no_auxiliar = no.proximo
        self.proximo = no_auxiliar
        
        if no_auxiliar:     #Se for um nó na última posição pode não haver nós posteriores
            no_auxiliar.anterior = self
        #endif
        
        del no  #Apaga o nó antigo (antes da fusão)
        
        return self
    #enddef
    
    def dividir(self, chave, registro):
        """
        Divide as chaves. Chamado quando o nó chega ao limite de sua capacidade
        
        Args:
            chave: chave a ser divida
            registro: registro a ser inserido

        Returns:
            Nó dividido
        """
        direita = No(self.getOrdem())   #Cria-se um nó auxiliar com a ordem daquele nó que será dividido
        direita.eFolha = True   #Este nó será folha
         
        meio = ceil(self.ordem / 2)     #Pivô do nó
        
        self.inserirFolha(chave, registro)  #O novo valor é inserido no nó folha
        
        direita.registros = self.registros[meio:]
        self.registros = self.registros[:meio]
        
        direita.pai = self.pai  #O pai do nó criado é o pai do nó que foi dividido
        direita.proximo = self.proximo  #Reapontamento
        direita.anterior = self
        self.proximo = direita
        
        if direita.proximo:     #Se for o primeiro nó, pode não ter vizinho à esquerda, precisando de verificação
            direita.proximo.anterior = direita
        #endif
        
        return direita  
    #enddef
    
    def emprestar(self, no, lado) -> None:
        """
        Pega um nó emprestado
        
        Args:
            no: nó a ser pego emprestado
            lado: lado que será feito o empréstimo (0 = esquerda e 1 = direita)
        """
        if lado == 0:   #Empréstimo será feito pela esquerda
            registro = self.registros[len(self.registros) - 1]
            self.registros.pop()    #Remoção do registro da última posição
            no.inserirFolha(registro[0], registro)
        #endif
        elif lado == 1:     #Empréstimo será feito pela direita
            registro = self.registros[0]
            self.registros.pop(0)   #Remoção do registro da primeira posição
            no.inserirFolha(registro[0], registro)
        #endelif
    #enddef
#endclass
            