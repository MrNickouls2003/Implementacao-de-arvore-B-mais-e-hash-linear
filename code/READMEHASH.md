# Hash Linear

- Implementação do algoritmo de Hash Linear, em Python, para a disciplina de Banco de Dados II
- Feito por: Clara Araújo Maia e Nícolas Augusto Montovani

## Introdução

Maneiras de utilizar o código implementado:

- 1- [Inserção](#inserção);

- 2- [Exclusão](#exclusão);

- 3- [Busca por Igualdade](#busca-por-igualdade);

- 4- [Mostrar Hash](#mostrar-hash);

- 5- [Casos de Teste](#casos-de-teste).

## Como usar

Deve-se executar o arquivo main.py, usando uma IDE de escolha pessoal. Após isso, deverá ser informado a quantidade de buckets iniciais, tamanho da página e a quantidade de campos do registro. Em seguida, um menu de ações com os possíveis comandos será exibido para que o usuário escolha entre realizar inserções, exclusões ou buscas no hash.

### Inserção

Para inserir um registro, digite a opção 1 no menu de ações. Em seguida, realize o seguinte passo:

- Informe o registro com a quantidade de campos definida anteriormente (separando por "-").

        Exemplo: Para um hash com um registro de 5 campos, digite: 30-90-1-3-5.

Lembrando que o primeiro número será a chave do registro.

### Exclusão

Para remover um registro, digite a opção 2 no menu de ações. Em seguida, realize o seguinte passo:

- Informe a chave que deverá ser feita a exclusão.

        Exemplo: Para um hash com um registro de 5 campos: [30-90-1-3-5], digite 30.

### Busca por Igualdade

Para pesquisar por um registro, digite a opção 3 no menu de ações. Como é busca por igualdade, é preciso que informe somente a chave do registro a ser procurado no hash.

### Mostrar Hash

Para mostrar os buckets do hash, digite a opção 4 no menu de ações.

Buckets com overflow são sinalizados com 'Overflow -> '.

### Casos de Teste

Para realizar um caso de teste, digite a opção 5 no menu de ações.
É preciso ser usado um arquivo do tipo .csv, já gerado pela ferramenta [SIOgen](https://ribeiromarcos.github.io/siogen/).

No código fonte, seria necessário mudar o nome do arquivo para realizar outros testes diferentes.

## Conclusão

Para terminar e sair do menu de ações, digite 0.
