""" 
Trabalho de Implementação de Árvore B+ de Banco de Dados II

Algoritmo da árvore B+

Autores:
Clara Araújo Maia - RA: 0065609
Nicolas Augusto Montovani - RA: 0065527  
"""
from base_btree import No 
from math import floor, ceil
from sys import getsizeof, maxsize

class ArvoreBPlus:
    def __init__(self, tamanho, quantidade):
        """
        Contrutor parametrizado da classe
        
        Essa classe armazena a árvore B+
        
        Args:
            tamanho: tamanho da página
            quantidade: quantidade de campos da página
            ordem: ordem do nó
            ordem_pai: ordem do nó pai
            raiz: raiz da árvore
        """ 
        self.ordem, self.ordem_pai = self.calcularOrdem(tamanho, quantidade)    #Valores da ordem do nó
        self.raiz = No(self.ordem)
        
        #Diz, de início, que a raiz da árvore é uma folha
        self.raiz.eFolha = True
    #enddef
    
    def calcularOrdem(self, tamanho, num_campos):
        """
        Faz o cálculo da ordem baseando-se no tamanho definido da página e da quantidade de campos
        
        Args:
            tamanho: tamanho da página
            num_campos: quantidade de campos da página

        Returns:
            Ordem do nó folha e do não folha
        """
        
        #Vetor criado para auxiliar com a quantidade de campos informados
        vetor = [maxsize] * num_campos
        
        #Tamanho da página (bytes) dividido pelo tamanho do registro (bytes)
        ordem_folha = tamanho // getsizeof(vetor)
        ordem_n_folha = tamanho // getsizeof(maxsize)
        
        return (ordem_folha, ordem_n_folha)
    #enddef
    
    def inserir(self, chave, registro):
        """
        Função que insere registros na árvore

        Args:
            chave: chave na árvore onde o registro deve ser inserido
            registro: registro a ser inserido na árvore
        """
        
        #Busca o nó que deverá armazenar o registro
        no = self.procurar(chave)
        
        if not self.procurarChave(no, chave):
            if len(no.registros) == no.getOrdem():  #Caso o nó esteja cheio
                
                #Fazendo a divisão do nó para armazenar o registro
                direita = no.dividir(chave, registro)   
                
                if direita:     #Se a divisão do nó foi feita
                    
                    #A chave é inserida no nó pai e são feitos os apontamentos
                    self.__inserirPai(no, direita.registros[0][0], direita)
                #endif
            #endif
            else:   #Caso o nó não esteja cheio
                
                #Insere o registro normalmente na folha
                no.inserirFolha(chave, registro)
            #endelse
        #endif
    #enddef
    
    def __inserirPai(self, esquerda, chave, direita):
        """
        Usada na divisão ao inserir uma chave

        Args:
            esquerda: nó da esquerda
            chave: chave a ser inserida na árvore
            direita: nó da direita
        """
        if self.raiz == esquerda:   #Se a divisão for feita na raiz da árvore
            
            #Como a raiz não será folha, ela recebe uma ordem de não folha
            no_raiz = No(self.ordem_pai)
            
            no_raiz.registros = [chave]
            no_raiz.filhos = [esquerda, direita]
            
            #Atualizando a raiz da árvore
            self.raiz = no_raiz    
            
            #Atualizando os filhos
            esquerda.pai = no_raiz
            direita.pai = no_raiz
        #endif
        else:   #Se a divisão não for feita na raiz da árvore
            
            #O pai da esquerda recebe o do pai do nó da esquerda
            pai_esquerda = esquerda.pai     
            
            #Uma variável auxiliar que recebe os filhos do nó da esquerda
            aux_esquerda = pai_esquerda.filhos 
            
            for i in range(len(aux_esquerda)):
                
                #Se o filho do nó analisado for igual ao nó dividido e a quantidade
                #de chaves do pai for igual à ordem daquele nó, a divisão do pai é
                #feita
                if aux_esquerda[i] == esquerda and len(pai_esquerda.registros) == pai_esquerda.getOrdem():
                    
                    #Cria um nó auxiliar para armazenar o pai da direita
                    pai_direita = No(self.ordem_pai)
                    
                    pai_direita.pai = pai_esquerda.pai 
                    
                    #Inserindo a chave entre os registros que se encontram no nó pai
                    pai_esquerda.registros = pai_esquerda.registros[:i] + [chave] + pai_esquerda.registros[i:]
                    
                    #Reorganizando os filhos
                    pai_esquerda.filhos = pai_esquerda.filhos[:i + 1] + [direita] + pai_esquerda.filhos[i + 1:]
                    
                    #Definindo o pivô
                    meio = ceil(pai_esquerda.getOrdem() / 2)
                    
                    #Variável que recebe o valor da chave que está sendo armazenada
                    #na posição do pivô
                    valor = pai_esquerda.registros[meio]
                    
                    #Pivô é usado para reorganizar as chaves do nó da esquerda,
                    #assim como seus filhos
                    pai_direita.registros = pai_esquerda.registros[meio + 1:]
                    pai_direita.filhos = pai_esquerda.filhos[meio + 1:]
                    
                    pai_esquerda.registros = pai_esquerda.registros[:meio]
                    pai_esquerda.filhos = pai_esquerda.filhos[:meio + 1]
                    
                    #Reorganizando os apontadores dos filhos para os pais
                    for x in pai_esquerda.filhos:
                        x.pai = pai_esquerda
                    #endfor
                    
                    for y in pai_direita.filhos:
                        y.pai = pai_direita
                    #endfor
                    
                    #O valor é subido na divisão de páginas
                    self.__inserirPai(pai_esquerda, valor, pai_direita)
                    
                    break
                #endif
                
                #Se a raiz não estiver cheia
                elif aux_esquerda[i] == esquerda:
                    
                    #Sobe uma chave para a raiz
                    pai_esquerda.registros = pai_esquerda.registros[:i] + [chave] + pai_esquerda.registros[i:]
                    pai_esquerda.filhos = pai_esquerda.filhos[:i + 1] + [direita] + pai_esquerda.filhos[i + 1:]
                    
                    break
                #endelif
            #endfor
        #endelse
    #enddef
    
    def excluir(self, chave):
        """
        Função que fará a exclusão de uma chave da árvore

        Args:
            chave: chave a ser apagada
        """
        
        no = self.procurar(chave)
        
        #Caso 1 - só tem chaves na raiz, mas ainda não teve divisão
        if no == self.raiz or len(no.registros) > floor(no.getOrdem() / 2):
            no.excluir(chave)
        #endif
        
        #Caso 2 - o nó é folha e tem quantidade mínima para remoção 
        else:
            self.excluirAuxiliar(no, chave)
        #endelse
    #enddef
    
    def excluirAuxiliar(self, no, chave):
        """
        Função que auxilia a função de exclusão acima
        
        Args:
            no: qual nó que deverá ser feita a operação de exclusão
            chave: chave a ser excluída
        """
        
        #Caso 3 - não tem quantidade mínima para remoção
        if len(no.registros) == floor(no.getOrdem() / 2):
            vizinho_esquerda = no.anterior
            
            #Caso 3a - irmão imediato da esquerda pode emprestar um registro
            if vizinho_esquerda and vizinho_esquerda.pai == no.pai and len(vizinho_esquerda.registros) > floor(no.getOrdem() / 2):
                vizinho_esquerda.emprestar(no, 0)
                
                no.excluir(chave)
                
                #Atualizando a chave no nó pai
                for i in range(len(no.pai.registros)):
                    if no.registros[0][0] <= no.pai.registros[i]:
                        no.pai.registros[i] = no.registros[0][0]
                        
                        break
                    #endif
                #endfor
            #endif
            else:
                vizinho_direita = no.proximo
                
                #Caso 3b - irmão imediato da direita pdoe emprestar um registro
                if vizinho_direita and vizinho_direita.pai == no.pai and len(vizinho_direita.registros) > floor(no.getOrdem() / 2):
                    vizinho_direita.emprestar(no, 1)
                    
                    no.excluir(chave)
                    
                    #Atualizando a chave no nó pai, percorrendo as chaves dele ao
                    #contrário
                    for i in range(len(no.pai.registros) - 1, -1, -1):
                        if vizinho_direita.registros[0][0] >= no.pai.registros[i]:
                            no.pai.registros[i] == vizinho_direita.registros[0][0]
                            
                            break
                        #endif
                    #endfor
                #endif
                
                #Caso 4 - faz a fusão com o irmão esquerdo ou direito
                else:
                    no_merge = None
                    indice = -1
                    
                    #Certificando que o nó possui um irmão esquerdo e que ele tenha
                    #um pai
                    if vizinho_esquerda and vizinho_esquerda.pai == no.pai:
                        no.excluir(chave)
                        indice = no.pai.filhos.index(no)
                        no_merge = vizinho_esquerda.juntar(no)
                    #endif
                    
                    #Certificando que o nó possui um irmão direito e que ele tenha
                    #um pai
                    elif vizinho_direita and vizinho_direita.pai == no.pai:
                        no.excluir(chave)
                        indice = no.pai.filhos.index(no)
                        no_merge = no.juntar(vizinho_direita)
                    #endelif
                    
                    #Remove o nó
                    del no
                    
                    #Atualizando o nó pai
                    no_pai = no_merge.pai
                    
                    #Se a raiz ficar vazia
                    if no_pai == self.raiz and len(self.raiz.registros) == 1:
                        no_pai = None
                        
                        #Atualizando a raiz pelo novo nó que sofreu a fusão
                        self.raiz = no_merge
                        
                        #Removendo o apontador para filho e a chave que sofreu a fusão
                        del no_merge    
                        
                        return 
                    #endif
                    
                    if indice > 0 and indice < len(no_pai.registros):
                        no_pai.filhos.pop(indice)
                        no_pai.registros.pop(indice - 1)
                    #endif
                    elif indice == 0:
                        no_pai.filhos.pop(indice + 1)
                        no_pai.registros.pop(indice)
                    #endelif
                    else:
                        no_pai.filhos.pop(-1)
                        no_pai.registros.pop(-1)
                    #endelse
                    
                    #Verificando se o nó é diferente da raiz e se a quantidade de chaves
                    #é menor do que a ordem
                    if no_pai != self.raiz and len(no_pai.registros) < int(floor(no_pai.getOrdem() / 2)):
                        
                        #Modificando o nó não folha
                        self.mudarPai(no_pai)
                    #endif
                #endelse
            #endelse
        #endif
    #enddef
    
    def procurar(self, chave):
        """
        Função que pesquisa um nó para que seja inserido um registro

        Args:
            chave: chave a ser procurada para inserir o registro

        Returns:
            retorna o nó onde ficará armazenado o registro
        """
        
        #Define o nó que será a raiz, e é onde será iniciada a busca
        no = self.raiz
        
        #Enquanto não encontrar um nó folha, o laço continua
        while not no.eFolha:
            
            #Variável auxiliar usada para armazenar os registros do nó
            aux = no.registros
            
            for i in range(len(aux)):
                
                #Se o índice da chave existir
                if chave == aux[i]:
                    
                    #Retorna o nó da posição i + 1 
                    no = no.filhos[i + 1]
                    
                    break
                #endif
                
                #Se o índice da chave for menor do que aquele existente
                elif chave > aux[i]:
                    
                    #Retorna o nó da posição i
                    no = no.filhos[i]
                    
                    break
                #endelif
                
                #Se chegar ao final da árvore
                elif i + 1 == len(no.registros):
                    
                    #Retorna o nó da posição i + 1
                    no = no.filhos[i + 1]
                    
                    break
                #endelif
            #endfor
        #endwhile
        
        return no
    #enddef
    
    def procurarChave(self, no, chave):
        """
        Função que faz a pesquisa da chave por igualdade

        Args:
            no: nó que se encontra a chave a ser pesquisada
            chave: chave a ser pesquisada

        Returns:
            Se achar a chave, retorna ela. Se não encontrar, retorna vazio
        """
        
        #Percorrendo a árvore 
        for r in no.registros:
            
            #Verifica se o chave está no nó
            if chave == r[0]:
                return r
            #endif
        #endfor
        
        return None
    #enddef
    
    def procurarIntervalo(self, no, c1, c2, operador):
        """
        Função que faz a pesquisa da chave usando intervalos

        Args:
            no: nó que tem a chave a ser pesquisada
            c1: primeiro índice a ser usado no intervalo
            c2: segundo índice a ser usado no intervalo
            operador: operador do intervalo
        """
        
        #Se o operador for o de "maior que"
        if operador == '>':
            while no:
                for i in range(len(no.registros)):
                    
                    #Faz a busca por valores maiores que um dado índice
                    if no.registros[i][0] > c1:
                        print(no.registros[i:], end=" <-> ")
                        
                        break
                    #endif
                #endfor
                
                no = no.proximo
            #endwhile
        #endif
        
        #Se o operador for o de "menor que"
        elif operador == '<':
            while no:
                for i in range(len(no.registros) - 1, -1, -1):
                    
                    #Faz a busca por valores menores que um dado índice
                    if no.registros[i][0] < c1:
                        print(no.registros[:i + 1], end=" <-> ")
                        
                        break
                    #endif
                #endfor
                
                no = no.anterior 
            #endwhile
        #endelif
        
        #Se o operador for o do "entre"
        elif operador == '|':
            while no:
                for i in range(len(no.registros)):
                    
                    #Faz um comparativo entre os extremos do intervalo, comparando o 
                    #índice de cada registro com cada um deles
                    if no.registros[i][0] > c1 and no.registros[i][0] < c2:
                        print(no.registros[i], end=" <-> ")
                        
                        break
                    #endif
                #endfor
                
                no = no.proximo
            #endwhile
        #endelif
    #enddef
    
    def mudarPai(self, no):
        """
        Função que reorganiza os pais do nó quando ele fica abaixo da ordem mínima permitida

        Args:
            no: nó que terá os pais reorganizados
        """
        
        no_pai = no.pai
        vizinho_esquerda = vizinho_direita = None
        
        #Procura pelo nó passado por referência no pai do nó
        indice = no_pai.filhos.index(no)
        
        #Se o índice for diferente de 0 ou se esse é o último índice da árvore
        if indice != 0 or len(no.pai.registros) == indice:
            
            #O vizinho da esquerda recebe o nó da esquerda do nó passado por referência
            vizinho_esquerda = no.pai.filhos[indice - 1]
            
            #Se o irmão da esquerda puder emprestar um registro
            if len(vizinho_esquerda.registros) > floor(vizinho_esquerda.getOrdem() / 2):
                
                #Faz uma rotação de chaves
                no.pai.rotacionarChaves(vizinho_esquerda, no, indice - 1, 0)
                
                return
            #endif
        #endif
        
        #Se o índice for igual a 0 ou se ele for menor do que o último índice
        elif indice == 0 or indice < len(no.pai.registros):
            
            #O vizinho da direita recebe o nó da direita do nó passado na assinatura da função
            vizinho_direita = no.pai.filhos[indice + 1]
            
            #Verifica se o vizinho da direita pode emprestar chaves
            if len(vizinho_direita.registros) > floor(vizinho_direita.getOrdem() / 2):
                
                #Rotaciona as chaves
                no.pai.rotacionarChaves(no, vizinho_direita, indice + 1, 1)
                
                return
            #endif
        #endelif
        
        #Verifica se existe um vizinho na esquerda
        if vizinho_esquerda:
            
            #Removendo o vizinho à esquerda do índice
            chave = no_pai.registros.pop(indice - 1)
            
            #Insere a chave na esquerda desse irmão
            vizinho_esquerda.inserir(chave)
            
            #Reorganização dos registros
            vizinho_esquerda.registros += no.registros
            
            #Reorganização dos nós
            vizinho_esquerda.filhos += no.filhos
            
            #Atualizando os pais para cada filho
            for f in no.filhos:
                f.pai = vizinho_esquerda
            #endfor
            
            #Remoção do filho do pai do nó
            no_pai.filhos.pop(indice)
            
            #O nó recebe agora o vizinho da esquerda
            no = vizinho_esquerda
        #endif
        
        #Verifica se existe um vizinho na direita
        elif vizinho_direita:
            
            #Removendo o vizinho à direita do índice
            chave = no_pai.registros.pop(indice)
            
            #Insere a chave na direita desse irmão
            no.inserir(chave)
            
            #Reorganização dos registros
            no.registros += vizinho_direita.registros 
            
            #Reorganização dos nós
            no.filhos += vizinho_direita.filhos 
            
            #Atualizando os pais para cada filho
            for f in vizinho_direita.filhos:
                f.pai = no
            #endfor
            
            #Remoção do filho do pai do nó
            no_pai.filhos.pop(indice + 1)
        #endelif
        
        #Verifica se o pai do nó está sem chaves e se o nó pai é raiz
        if len(no_pai.registros) == 0 and no_pai == self.raiz:
            
            #Transforma o nó em raiz
            self.raiz = no
        #endif
        
        #Verifica se a quantidade de chaves do nó pai ficou abaixo do mínimo e se o nó
        #pai não é raiz
        elif len(no_pai.registros) < floor(no_pai.getOrdem() / 2) and no_pai != self.raiz:
            
            #Faz a modificação do pai do nó por recursão
            self.mudarPai(no_pai)
        #endelif
    #enddef
    
    def mostrarArvore(self):
        """
        Mostra a árvore montada, por meio de níveis
        """
        
        #Se a árvore não possui registros, retorna nada
        if not len(self.raiz.registros):
            return
        #endif
        
        delimitador = None
        lista = list()
        
        lista.append(self.raiz)
        lista.append(delimitador)
        
        #Percorrendo a árvore 
        while True:
            atual = lista.pop(0)
            
            #Usa um delimitador para cada nível da árvore
            if atual != delimitador:
                if atual.eFolha:
                    print(atual.registros, end=" <-> ")
                #endif
                else:
                    print(atual.registros, end="   ")
                #endelse
                
                #Verifica se ainda está no nível
                if len(atual.filhos):
                    for i in atual.filhos:
                        
                        #Adiciona as chaves à fila
                        lista.append(i)
                    #endfor
                #endif
            #endif
            else:
                print()
                
                if not len(lista):
                    break
                #endif
                
                lista.append(delimitador)
            #endelse
        #endwhile
    #enddef
#endclass          