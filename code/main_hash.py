""" 
Trabalho de Implementação de Hash Linear de Banco de Dados II

Algoritmo da main usando hash linear

Autores:
Clara Araújo Maia - RA: 0065609 
Nicolas Augusto Montovani - RA: 0065527
"""
from hash_linear import HashLinear
from time import time, sleep
 
def main():
    """
    Função main() que coloca em prática o conceito de Hash Linear
    """
    
    qnt_buckets = int(input("Informe a quantidade de buckets inicial: "))
    tamanho_pagina = int(input("Informe o tamanho da página (em bytes): "))
    campos = int(input("Quantidade de campos do registro: "))
    hash_linear = HashLinear(qnt_buckets, tamanho_pagina, campos)
    
    while True:
        #Menu de ações para usar o hash linear
        print("====== MENU DE AÇÕES (HASH LINEAR) ======")
        print("1. Inserir registro")
        print("2. Remover registro")
        print("3. Fazer busca por igualdade")
        print("4. Mostrar hash linear")
        print("5. Casos de teste")
        print("0. Sair do menu")
        
        resp = int(input("Informe sua resposta: "))
        
        #Usuário escolheu a opção de inserir um registro no hash
        if resp == 1:
            registro = [int (x) for x in input("Registro completo (campos separados por -): ").split('-')]
            
            if len(registro) == campos:
                hash_linear.inserir(registro[0], registro)
            #endif
            else:
                print("Tamanho incompatível com o valor informado.")
            #endelse
        #endif
        
        #Usuário escolheu a opção de remover um registro no hash
        elif resp == 2:
            chave = int(input("Chave do registro a ser removido: "))
            
            hash_linear.excluir(chave)
        #endelif
        
        #Usuário escolheu a opção de procurar um registro no hash
        elif resp == 3:
            chave = int(input("Chave do registro a ser buscado: "))
            
            i, r = hash_linear.procurar(chave)
            
            if r:
                print(r)
            #endif
        #endelif
        
        #Usuário escolheu a opção de mostrar o hash criado por ele
        elif resp == 4:
            hash_linear.mostrarHash()
        #endelif
        
        #Usuário escolheu a opção de realizar um caso de teste usando hash
        elif resp == 5:
            arquivo = open('C:/Users/clara/Documents/Clara/IFMG/6º período/Banco de Dados II/Trabalho Final de Banco de Dados II - Clara e Nicolas/testes/teste2.csv', 'r')
            
            comeco = time()
            
            for coluna in arquivo:
                registro = coluna.split(',')
                
                if registro[0] == '+':
                    registro = [int (x) for x in registro[1:]]
                    
                    hash_linear.inserir(registro[0], registro)
                #endif
                elif registro[0] == '-':
                    registro = [int (x) for x in registro[1:]]
                    
                    hash_linear.excluir(registro[0])
                #endelif
                
                fim = time()
            #endfor
            
            print(f"Tempo total decorrido: {fim - comeco}")
            
            arquivo.close()
        #endelif
        
        #Usuário escolheu a opção de sair do menu de ações
        elif resp == 0:
            print("====== SAINDO ======")
            sleep(2)
            
            break
        #endelif
        
        #Usuário escolheu uma opção inválida
        else:
            print("Opção inválida. Tente novamente.")
        #endelse
    #endwhile
#enddef

if __name__ == '__main__':
    main()
#endif                         