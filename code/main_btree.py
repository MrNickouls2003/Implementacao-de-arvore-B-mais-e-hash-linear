""" 
Trabalho de Implementação de Árvore B+ de Banco de Dados II

Algoritmo da main usando árvore B+

Autores:
Clara Araújo Maia - RA: 0065609 
Nicolas Augusto Montovani - RA: 0065527
"""
from bplus_tree import ArvoreBPlus
from time import time, sleep

def main():
    """
    Função main() para rodar o algoritmo de Árvore B+
    """
    
    tamanho_pagina = int(input("Informe o tamanho da página em bytes: "))
    num_campos = int(input("Informe quantos campos tem o registro: "))
    
    arvore = ArvoreBPlus(tamanho_pagina, num_campos)
    
    while True:
        
        #Menu de ações para utilização da Árvore B+
        print("\n====== MENU DE AÇÕES (ÁRVORE B+) ======")
        print("1. Inserir registro")
        print("2. Remover registro")
        print("3. Fazer busca por igualdade")
        print("4. Fazer busca por intervalo")
        print("5. Mostrar árvore B+")
        print("6. Casos de teste")
        print("0. Sair do menu")
        
        resp = int(input("Informe sua resposta: "))
        
        #Usuário escolheu a opção de inserir registros na árvore
        if resp == 1:
            registro = [int(r) for r in input("Registro completo (campos separados por '-'): ").split('-')]
            
            if len(registro) == num_campos:
                arvore.inserir(registro[0], registro)
            #endif
            else:
                print("Tamanho incompatível com o valor informado.")
            #endelse
        #endif
        
        #Usuário escolheu a opção de remover registros da árvore
        elif resp == 2:
            chave = int(input("Chave do registro a ser removido: "))
            
            arvore.excluir(chave)
        #endelif
        
        #Usuário escolheu a opção de fazer a busca por uma chave na árvore, usando a 
        #busca de igualdade
        elif resp == 3:
            chave = int(input("Chave do registro a ser buscado: "))
            
            r = arvore.procurarChave(arvore.procurar(chave), chave)
            
            if r:
                print(f"Registro: {r}")
            #endif
        #endelif
        
        #Usuário escolheu a opção de fazer a busca por uma chave na árvore, usando a
        #busca por intervalos
        elif resp == 4:
            print("A - Maior ( > )")
            print("B - Menor ( < )")
            print("C - Entre dois números ( | )")
            
            opcao = input("Informe a opção desejada, juntamente com o(s) número(s), separados por ',': ").split(',')
            
            #Usuário escolheu a opção de busca por chaves maiores do que outra informada
            if opcao[0] == 'A':
                arvore.procurarIntervalo(arvore.procurar(int(opcao[1])), int(opcao[1]), 0, '>')
            #endif
            
            #Usuário escolheu a opção de busca por chaves menores do que outra informada
            elif opcao[0] == 'B':
                arvore.procurarIntervalo(arvore.procurar(int(opcao[1])), int(opcao[1]), 0, '<')
            #endelif
            
            #Usuário escolheu a opção de busca por chaves que se encontram entre dois 
            #outros números informados
            elif opcao[0] == 'C':
                arvore.procurarIntervalo(arvore.procurar(int(opcao[1])), int(opcao[1]), int(opcao[2]), '|')
            #endif
        #endelif
        
        #Usuário escolheu a opção de mostrar a árvore
        elif resp == 5:
            arvore.mostrarArvore()
        #endelif
        
        #Usuário escolheu a opção de realizar casos de teste
        elif resp == 6:
            arquivo = open('C:/Users/clara/Documents/Clara/IFMG/6º período/Banco de Dados II/Trabalho Final de Banco de Dados II - Clara e Nicolas/testes/teste1.csv', 'r')
            
            comeco = time()
            
            for coluna in arquivo:
                registro = coluna.split(',')
                
                if registro[0] == '+':
                    registro = [int(r) for r in registro[1:]]
                    
                    arvore.inserir(registro[0], registro)
                #endif
                elif registro[0] == '-':
                    registro = [int(r) for r in registro[1:]]
                    
                    arvore.excluir(registro[0])
                #endelif
                
                fim = time()
            #endfor
            
            #Tempo total que levou para fazer a árvore 
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