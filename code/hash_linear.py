""" 
Trabalho de Implementação de Hash de Banco de Dados II

Algoritmo do hash linear

Autores:
Clara Araújo Maia - RA: 0065609
Nicolas Augusto Montovani - RA: 0065527
"""
from base_hash import Bucket
from sys import getsizeof, maxsize

class HashLinear:
    """
    Classe de Hash Linear
    """
    def __init__(self, buckets, tamanho, campos) -> None:
        """
        Construtor parametrizado da classe de Hash Linear

        Args:
            buckets: quantidade inicial de buckets que terá no hash
            tamanho: tamanho da página
            campos: quantidade de campos na página
        """
        self.buckets_n0 = buckets
        self.tamanho_bucket = self.tamanhoBucket(tamanho, campos)
        
        #Lista de buckets
        self.buckets_ = []
        
        #Nível inicial do hash
        self.nivel = 0
        
        #Próximo bucket que sofrerá a divisão
        self.proximo = 0
        
        #Criando buckets iniciais vazios
        for _ in range(buckets):
            self.buckets_.append(Bucket(self.tamanho_bucket))
        #endfor
    #enddef
    
    def bucketsAtuais(self):
        """
        Função que calcula a quantidade de buckets, usando o nível do hash e o número de buckets iniciais
        
        Returns:
            Quantidade de buckets no hash
        """
        return self.buckets_n0 * 2**(self.nivel)
    #enddef
    
    def tamanhoBucket(self, tamanho, campos):
        """
        Determina o tamanho dos registros no bucket de acordo com o tamanho da página

        Args:
            tamanho: tamanho da página
            campos: quantidade de campos na página

        Returns:
            Tamanho encontrado para cada registro no bucket
        """
        
        #Vetor que armazena o tamanho máximo que Python consegue armazenar 
        #em um tipo de variável, multiplicado pelo número de campos que a 
        #página terá
        vetor = [maxsize] * campos
        
        return tamanho // getsizeof(vetor)
    #enddef
    
    def inserir(self, chave, registro):
        """
        Função que realiza a inserção de um registro no hash

        Args:
            chave: onde deverá ser inserido o registro
            registro: dado a ser inserido
        """
        
        #Calculando a posição que o registro pode ser inserido
        posicao = self.nivelH(chave, self.nivel)
        
        #Verifica se a posição que o bucket está inserido está cheio
        if posicao == self.proximo and self.buckets_[posicao].cheio():
            
            #Criação de um novo bucket
            self.buckets_.append(Bucket(self.tamanho_bucket))
            
            #Dividindo o bucket apontado pelo próximo para fazer a inserção
            self.dividirBucket(self.buckets_[self.proximo], self.proximo, 0)
            
            posicao = self.nivelH(chave, self.nivel + 1)
            
            #Verifica se o bucket está cheio
            if self.buckets_[posicao].cheio():
                
                #Inserindo um overflow no bucket para acomodar o novo registro
                self.inserirOverflow(posicao, registro)
            #endif
            else:
                
                #Inserindo o registro no bucket
                self.buckets_[posicao].registros.append(registro)
            #endelse
            
            #Incrementando o apontador para o próximo
            self.proximo += 1
            
            #Verificando se o próximo ultrapassou o nível (H) do bucket
            self.novaPassada()
            
            return 
        #endif
        
        #Verifica se o bucket que receberá a chave já sofreu alguma divisão
        elif posicao < self.proximo:
            
            #Recalculando a posição em que o registro deverá ser inserido
            posicao = self.nivelH(chave, self.nivel + 1)
        #endelif
        
        #Verifica se o bucket está cheio
        if self.buckets_[posicao].cheio():
            
            #Inserindo um overflow no bucket
            self.inserirOverflow(posicao, registro)
            
            #Adiciona um novo bucket ao hash
            self.buckets_.append(Bucket(self.tamanho_bucket))
            
            #Faz a divisão do bucket que está sendo apontado por próximo
            self.dividirBucket(self.buckets_[self.proximo], self.proximo, 0)
            
            #Atualiza o próximo
            self.proximo += 1
            
            #Verificando se o próximo ultrapassou o nível (H) do bucket
            self.novaPassada()
            
            return
        #endif
        else:
            
            #Inserindo o registro no bucket
            self.buckets_[posicao].registros.append(registro)
        #endelse
    #enddef
    
    def inserirOverflow(self, posicao, registro):
        """
        Função que realiza a inserção de registros no hash quando houver overflow

        Args:
            posicao: índice da posição onde o registro deve ser inserido
            registro: dado a ser inserido no bucket de overflow
        """
        
        #Verifica se o bucket na posição especificada não possui overflow
        if not self.buckets_[posicao].getOverflow():
            
            #Criando um novo bucket de overflow
            overflow = Bucket(self.tamanho_bucket)
            
            #Inserindo o registro no bucket de overflow criado
            overflow.registros.append(registro)
            
            #Adicionando esse bucket de overflow ao bucket principal
            self.buckets_[posicao].overflow.append(overflow)
            
            #Definindo que agora o bucket principal possui overflow
            self.buckets_[posicao].setOverflow(True)
        #endif
        else:
            
            #Flag adicionada para saber se o registro foi inserido 
            #corretamente
            flag = False
            
            for bucket_over in self.buckets_[posicao].overflow:
                
                #Verifica se o bucket de overflow não está cheio
                if not bucket_over.cheio():
                    
                    #Inserindo o registro no bucket de overflow
                    bucket_over.registros.append(registro)
                    
                    #Indicando que o registro foi adicionado com sucesso
                    flag = True
                    
                    break
                #endif
                
                #Verifica se foi encontrado algum bucket com overflow não
                #cheio
                if not flag:
                    
                    #Criando um novo bucket de overflow
                    overflow = Bucket(self.tamanho_bucket)
                    
                    #Inserindo o registro no bucket de overflow
                    overflow.registros.append(registro)
                    
                    #Adicionando o bucket de overflow ao bucket principal
                    self.buckets_[posicao].overflow.append(overflow)
                    
                    #Definindo que agora o bucket principal possui overflow
                    self.buckets_[posicao].setOverflow(True)
                #endif
            #endfor
        #endelse
    #enddef
    
    def nivelH(self, chave, nivel):
        """
        Função que calcula a posição que o registro a ser inserido será armazenado

        Args:
            chave: chave a ser armazenada no hash
            nivel: nível em que será armazenada a chave

        Returns:
            Posição que o registro ficará, de acordo com o número de buckets e o nível de hash 
        """
        
        #Verifica se o nível de hash é igual àquele informado
        if self.nivel == nivel:
            return chave % self.bucketsAtuais()
        #endif
        
        #Verifica se o nível é de hash sucessor é igual àquele informado
        elif nivel == self.nivel + 1:
            return chave % (2 * self.bucketsAtuais())
        #endelif
    #enddef
    
    def dividirBucket(self, bucket, posicao_atual, c):
        """
        Função que realiza a divisão do bucket ao atingir sua capacidade máxima, redistribuindo os registros para os buckets apropriados

        Args:
            bucket: bucket que precisa ser dividido
            posicao_atual: posição do bucket que encheu
            c: controla a recursividade ao lidar com overflow

        Returns:
            Caso tenha overflow, retornará a própria função como uma maneira de recursão 
        """
        
        #Variável que armazerá a quantidade de registros no vetor
        i = 0
        
        #Percorrendo todos os registros do vetor
        while i < len(bucket.registros):
            registro = bucket.registros[i]
            
            #Pegando a posição do registro usando H(nível + 1)
            posicao = self.nivelH(registro[0], self.nivel + 1)
            
            #Verificando se a posição do registro mudou
            if posicao != posicao_atual:
                
                #Excluindo a posição antiga e adiciona a posição nova no
                #bucket
                self.buckets_[posicao].registros.append(bucket.registros.pop(i))
            #endif
            else:
                
                #Incrementando o i, para que tenha a continuação da 
                #varredura
                i += 1
            #endif
        #endwhile
        
        #Verifica se o bucket possui overflow
        if bucket.e_overflow:
            
            #Retorna a divisão do bucket, de maneira recursiva
            return self.dividirBucket(bucket.overflow[c], posicao_atual, c + 1)
        #endif
    #enddef
    
    def novaPassada(self):
        """
        Função que atualiza o estado do hash após uma nova iteração
        """
        
        #Verifica se o índice atual atingiu o número total de buckets
        #permitidos
        if self.proximo == self.bucketsAtuais():
            
            #Incrementando o nível de hash
            self.nivel += 1
            
            #Reinicia o índice para 0, indicando o início de uma nova 
            #passada
            self.proximo = 0
        #endif
    #enddef
    
    def procurar(self, chave):
        """
        Função que realiza a busca de um registro usando sua chave no hash

        Args:
            chave: chave que se tem o registro armazenado

        Returns:
            Registro procurado, juntamente com o bucket aonde ele está armazenado. Se não encontrar o registro no hash, retorna None
        """
        
        #Calculando a possível posição do registro
        posicao = self.nivelH(chave, self.nivel)
         
        #Verifica se o registro está nos buckets H(nível)
        if posicao < self.proximo:
            
            #Recalculando a posição para H(nível + 1)
            posicao = self.nivelH(chave, self.nivel + 1)
        #endif
        
        for x, registro in enumerate(self.buckets_[posicao].registros):
            
            #Verifica se a chave procurada é igual à chave do registro atual
            if chave == registro[0]:
                return x, self.buckets_[posicao]
            #endif
        #endfor
        
        #Verifica se o bucket tem overflow
        if len(self.buckets_[posicao].overflow):
            for b in self.buckets_[posicao].overflow:
                for y, registro in enumerate(b.registros):
                    
                    #Verifica se a chave procurada é igual á chave do 
                    #registro atual
                    if chave == registro[0]:
                        return y, b
                    #endif
                #endfor
            #endfor
        #endif
        
        return None, None
    #enddef
    
    def excluir(self, chave):
        """
        Função que realiza a exclusão de um registro pela chave dele no hash

        Args:
            chave: chave que se encontra o registro a ser excluído
        """
        
        #Buscando o registro pela chave
        i, bucket = self.procurar(chave)
        
        #Verificando se o registro foi encontrado
        if bucket:
            
            #Excluindo o registro do hash
            bucket.registros.pop(i)
        #endif
    #enddef
    
    def mostrarHash(self):
        """
        Função que mostra o hash ao usuário
        """
        
        for i in range(len(self.buckets_)):
            if len(self.buckets_[i].overflow):
                print(i, ' - ', self.buckets_[i].registros, end=' -> ')

                for b in self.buckets_[i].overflow:
                    print(b.registros, end=' -> ')
                    print('Overflow')
                #endfor
                
                print()
            #endif
            else:
                print(i, ' - ', self.buckets_[i].registros)
            #endelse
        #endfor
    #enddef
#endclass
