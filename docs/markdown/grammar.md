# Gramática Regular e Derivações — Linguagem do Rato 🐀

## 1. Objetivo

Este documento apresenta a definição de gramáticas regulares para representar os padrões léxicos da Linguagem do Rato.

O objetivo é formalizar matematicamente a formação de identificadores, números inteiros e números decimais, demonstrando como as cadeias são geradas por meio de produções gramaticais.

Esta gramática tem finalidade exclusivamente léxica. Portanto, não representa uma gramática sintática completa da linguagem e não tem como objetivo reconhecer estruturas completas de comandos ou executar programas.

## 2. Notação utilizada

Serão utilizados os seguintes símbolos:

- `L`: conjunto de letras de A até Z e de a até z.
- `D`: conjunto de dígitos de 0 até 9.
- `_`: símbolo de sublinhado.
- `.`: ponto decimal.
- `ε`: cadeia vazia.

A gramática será representada pela tupla:

**G = (V, Σ, R, S)**

Onde:

- V: conjunto de símbolos não terminais.
- Σ: conjunto de símbolos terminais.
- R: conjunto de regras de produção.
- S: símbolo inicial da gramática.

As produções seguem o padrão de uma gramática regular à direita.

## 3. Gramática de identificadores

A gramática de identificadores representa nomes de variáveis, eventos e funções.

De acordo com a especificação léxica, um identificador deve começar obrigatoriamente com uma letra ou sublinhado. Após o primeiro caractere, podem aparecer letras, números ou sublinhados.

### 3.1 Definição formal

G_ID = (V_ID, Σ_ID, R_ID, S_ID)

**V_ID:**

{S_ID, A}

**Σ_ID:**

L ∪ D ∪ {_}

**S_ID:**

S_ID

**R_ID:**

S_ID → L A | _ A

A → L A | D A | _ A | ε

### 3.2 Exemplos aceitos

| Identificador | Resultado |
|---|---|
| rato | Aceito |
| _rato1 | Aceito |

Exemplo de identificador rejeitado:

| Identificador | Motivo |
|---|---|
| 1rato | Rejeitado: começa com um número |

### 3.3 Derivações

**Exemplo 1: rato**

S_ID ⇒ L A

⇒ r A

⇒ r L A

⇒ r a A

⇒ r a L A

⇒ r a t A

⇒ r a t L A

⇒ r a t o A

⇒ r a t o

Resultado: IDENTIFIER.

**Exemplo 2: _rato1**

S_ID ⇒ _ A

⇒ _ L A

⇒ _ r A

⇒ _ r L A

⇒ _ r a A

⇒ _ r a L A

⇒ _ r a t A

⇒ _ r a t L A

⇒ _ r a t o A

⇒ _ r a t o D A

⇒ _ r a t o 1 A

⇒ _ r a t o 1

Resultado: IDENTIFIER.

**Exemplo rejeitado: 1rato**

A gramática não consegue iniciar uma derivação com o número 1, pois S_ID permite somente uma letra ou o caractere _ no primeiro símbolo.

Portanto, a cadeia não pertence à linguagem dos identificadores.

## 4. Gramática de números inteiros

A gramática de números inteiros representa sequências de um ou mais dígitos, sem sinal negativo.

### 4.1 Definição formal

G_INT = (V_INT, Σ_INT, R_INT, S_INT)

**V_INT:**

{S_INT, A}

**Σ_INT:**

D

**S_INT:**

S_INT

**R_INT:**

S_INT → D A

A → D A | ε

### 4.2 Exemplos aceitos

| Número | Resultado |
|---|---|
| 007 | Aceito |
| 123 | Aceito |

Exemplo rejeitado:

| Número | Motivo |
|---|---|
| 12a | Não pertence ao padrão de inteiro, pois contém uma letra |

### 4.3 Derivações

**Exemplo 1: 007**

S_INT ⇒ D A

⇒ 0 A

⇒ 0 D A

⇒ 00 A

⇒ 00 D A

⇒ 007 A

⇒ 007

Resultado: INTEGER.

**Exemplo 2: 123**

S_INT ⇒ D A

⇒ 1 A

⇒ 1 D A

⇒ 12 A

⇒ 12 D A

⇒ 123 A

⇒ 123

Resultado: INTEGER.

**Exemplo rejeitado: 12a**

A gramática permite somente dígitos. Após gerar os caracteres 1 e 2, não existe produção que permita gerar a letra a.

Portanto, a cadeia completa não pertence à linguagem dos números inteiros.

## 5. Gramática de números decimais

A gramática de números decimais representa números que possuem uma parte inteira, seguida obrigatoriamente de um ponto e de pelo menos um dígito na parte decimal.

### 5.1 Definição formal

G_FLOAT = (V_FLOAT, Σ_FLOAT, R_FLOAT, S_FLOAT)

**V_FLOAT:**

{S_FLOAT, A, B, C}

**Σ_FLOAT:**

D ∪ {.}

**S_FLOAT:**

S_FLOAT

**R_FLOAT:**

S_FLOAT → D A

A → D A | . B

B → D C

C → D C | ε

### 5.2 Exemplos aceitos

| Número | Resultado |
|---|---|
| 3.14 | Aceito |
| 10.5 | Aceito |

Exemplos rejeitados:

| Número | Motivo |
|---|---|
| 5. | Não possui dígito após o ponto decimal |
| .5 | Não possui parte inteira antes do ponto |

### 5.3 Derivações

**Exemplo 1: 3.14**

S_FLOAT ⇒ D A

⇒ 3 A

⇒ 3 . B

⇒ 3 . D C

⇒ 3 . 1 C

⇒ 3 . 1 D C

⇒ 3 . 14 C

⇒ 3 . 14

Resultado: FLOAT.

**Exemplo 2: 10.5**

S_FLOAT ⇒ D A

⇒ 1 A

⇒ 1 D A

⇒ 10 A

⇒ 10 . B

⇒ 10 . D C

⇒ 10 . 5 C

⇒ 10 . 5

Resultado: FLOAT.

**Exemplo rejeitado: 5.**

A gramática exige que depois do ponto decimal seja produzido obrigatoriamente pelo menos um dígito.

Como não existe dígito após o ponto, a derivação não pode ser concluída.

Portanto, 5. não pertence à linguagem dos números decimais.

## 6. Relação entre a gramática e a especificação léxica

As gramáticas apresentadas correspondem às expressões regulares definidas na especificação léxica da Linguagem do Rato:

| Categoria | Expressão regular |
|---|---|
| IDENTIFIER | (L \| _)(L \| D \| _)* |
| INTEGER | D+ |
| FLOAT | D+ . D+ |

As três gramáticas representam linguagens regulares e podem ser reconhecidas por autômatos finitos determinísticos (AFDs).

A gramática de identificadores permite gerar palavras reservadas, pois elas também seguem o padrão de identificador. A classificação final entre KEYWORD e IDENTIFIER é realizada posteriormente pelo Scanner, por meio da consulta ao conjunto de palavras reservadas K.

## 7. Limitações da gramática

As gramáticas desenvolvidas neste documento representam somente padrões léxicos selecionados da Linguagem do Rato.

Elas não definem a estrutura completa de comandos, condições, repetições, eventos ou funções.

O reconhecimento desses padrões é responsabilidade do analisador léxico, enquanto a construção de uma gramática sintática completa não faz parte do escopo desta tarefa.

Além disso, regras especiais de tratamento de erros, como números malformados e caracteres inválidos, são decisões do Scanner e não são integralmente representadas pelas gramáticas individuais.

## 8. Conclusão

A formalização das gramáticas regulares permite demonstrar matematicamente como identificadores, números inteiros e números decimais são construídos.

Por meio das produções e derivações apresentadas, é possível verificar quais cadeias pertencem às linguagens definidas e quais são rejeitadas.

Dessa forma, a gramática complementa as expressões regulares e os autômatos finitos do projeto, mantendo a correspondência entre a especificação matemática e o funcionamento esperado do analisador léxico.