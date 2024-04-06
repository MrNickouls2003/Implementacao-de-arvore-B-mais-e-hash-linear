# Criadores:
Clara Araújo Maia

Nicolas Augusto Montovani

## Árvore B+
Possui a estrutura semelhante à da árvore B, porém armazena os dados somente em suas folhas, além de elas são encadeadas, ou seja, fazem o armazenamento de dados em um arquivo e o do índice em outro.
<ul>
  <li>
    Alterações sempre mantêm a árvore balanceada
  </li>
  <li>
    A ocupação mínima das páginas deve ser de 50% (menos a raiz)
  </li>
  <li>
    Pode ter repetição de valores
  </li>
  <li>
    Páginas folha são duplamente ligadas, ou seja, estão ligadas com sua página pai e com seus irmãos
  </li>
  <ul style="square">
    <li>Cada página tem m entradas, em que d ≤ m ≤ 2d</li>
    <li>A raiz tem 1 ≤ m ≤ 2d registros</li>
  </ul>
</ul>

### Inserir dados
A inserção sempre acontece em um nó folha

<ol>
  <li>Localizar a folha dentro da qual a chave será inserida</li>
  <li>Localizar a posição de inserção dentro da folha</li>
  <li>Inserir a chave</li>
  <li>Se, após a inserção, a folha estiver completa; deverá ser feita a cisão da página</li>
  <ol>
    <li>As m - 1 chaves são divididas em dois grupos:</li>
    <ul>
      <li>(m - 1) / 2 chaves menores ficam na folha da esquerda</li>
      <li>(m - 1) / 2 chaves maiores ficam na folha da direita</li>
    </ul>
    <li>A maior chave da esquerda é copiada para o nó pai</li>
  </ol>
</ol>

### Excluir dados
Podem ocorrer de duas maneiras diferentes:
<ol>
  <li><strong>Caso 1:</strong> A chave aparece apenas em um nó da folha</li>
  <ol>
    <li>A chave é simplesmente removida e a folha é reorganizada</li>
  </ol>
  <li><strong>Caso 2:</strong> A chave aparece também nos nós internos</li>
  <ol>
    <li>A chave é removida, porém não é removida dos nós internos</li>
    <li>A folha é reorganizada</li>
    <li>Quando uma chave é retirada de um nó folha, a página pode ter uma ocupação abaxio do mínimo. Com isso, pode-se fazer uma das </li>
    <ol>
      <li>Concatenação: páginas podem ser concatenadas se sçao irmãs adjacentes (têm o mesmo pai e são apontadas por ponteiros adjacentes nele) e juntas possuem menos de m - 1 chaves</li>
      <ul>
        <li>Agrupa as entradas de duas páginas em somente uma</li>
        <li>Remove uma página do nó pai</li>
      </ul>
      <li>Redistribuição: se uma página e seu irmão adjacente possuem um conjunto m - 1 ou mais chaves, essas podem ser distribuídas de maneira equilibrada</li>
      <ul>
        <li>Contatena as chaves</li>
        <li>Efetua a cisão da página resultante</li>
      </ul>
    </ol>
  </ol>
</ol>

## Índice Hash
Consiste na criação de uma tabela hash, em que os dados são armazenados em uma matriz de buckets; resolvida por uma função de hash, mapeando chaves para índices na tabela

### Resolução de Colisões
Utiliza a técnica de sondagem linear para resolver colisões. Se o slot inicial estiver ocupado, avança a busca linearmente para encontrar o próximo slot vazio

### Inserir dados
<ol>
  <li>Calcula o índice utilizando a função de hash</li>
  <li>Se o slot estiver vazio, insere o dado</li>
  <li>Se houver colisão, aplica sondagem linear para encontrar o próximo slot vazio. Quando encontrar, insere o dado nesse slot</li>
</ol>

### Excluir dados
<ol>
  <li>Localiza o dado na tabela hash usando a função de hash</li>
  <li>Se o dado existe, realiza a remoção</li>
  <li>Se houver colisão, realiza a busca linear para encontrar os dados. Depois disso, remove o dado do slot encontrado</li>
</ol>

### Redimensionamento
Quando a carga da tabela excede um limite predefinido, a tabela é então redimensionada para evitar colisões excessivas. Durante o redimensionamento, os dados são redistribuídos em uma nova tabela hash com maior capacidade, utilizando uma nova função de hash

### Eficiência
A busca e a inserção de dados têm complexidade de tempo médio O(1), mas podem se degradar para O(n) em casos de colisões excessivas. O redimensionamento pode ser custoso, porém é necessário para manter a eficiência da tabela hash

### Considerações Adicionais
<ul>
  <li>A técnica de sondagem linear é simples, mas pode resultar em agrupamento primário e redução da eficiência se não houver o controle adequado de colisões</li>
  <li>É importante escolher uma boa função de hash para distribuir os dados de maneira uniforme</li>
</ul>
