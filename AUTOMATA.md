# T05 — AFDs de operadores e delimitadores

## 1. Objetivo

Formalizar os AFDs de atribuição, operadores relacionais, operadores aritméticos e delimitadores da Linguagem do Rato.

Este documento utiliza a Especificação Léxica da Linguagem do Rato, versão 1.0, especialmente as seções 4.5, 4.6 e 6, sem alterar suas regras.

## 2. Convenções

Cada AFD é representado pela tupla:

M = (Q, Σ, δ, q₀, F)

Onde:

- Q é o conjunto de estados.
- Σ é o alfabeto do autômato.
- δ é a função de transição.
- q₀ é o estado inicial.
- F é o conjunto de estados finais.

Nas tabelas:

- `→` indica o estado inicial.
- `*` indica um estado final.
- q_d é o estado poço.
- Toda transição de q_d retorna a q_d.

Os alfabetos apresentados são específicos de cada reconhecedor. Caracteres externos a esses alfabetos são tratados pelo scanner, que seleciona outro reconhecedor ou informa erro.

## 3. AFD de ASSIGNMENT e RELATIONAL_OPERATOR

### 3.1 Linguagem reconhecida

```text
{ =, ==, !=, <, <=, >, >= }
```

A classificação dos lexemas é:

| Lexema | Categoria |
|---|---|
| `=` | ASSIGNMENT |
| `==` | RELATIONAL_OPERATOR |
| `!=` | RELATIONAL_OPERATOR |
| `<` | RELATIONAL_OPERATOR |
| `<=` | RELATIONAL_OPERATOR |
| `>` | RELATIONAL_OPERATOR |
| `>=` | RELATIONAL_OPERATOR |

O caractere `!` isolado não é um token válido.

### 3.2 Definição formal

```text
M_OP = (Q_OP, Σ_OP, δ_OP, q₀, F_OP)

Q_OP = {q₀, q₁, q₂, q₃, q₄, q₅, q₆, q₇, q₈, q_d}

Σ_OP = {=, !, <, >}

F_OP = {q₁, q₂, q₄, q₅, q₆, q₇, q₈}
```

A função δ_OP é definida pela tabela de transição abaixo.

### 3.3 Significado dos estados

| Estado | Significado | Categoria se a leitura terminar |
|---|---|---|
| q₀ | Nenhum símbolo foi lido | Não aceita |
| q₁ | Foi lido `=` | ASSIGNMENT |
| q₂ | Foi lido `==` | RELATIONAL_OPERATOR |
| q₃ | Foi lido `!` | Não aceita; falta `=` |
| q₄ | Foi lido `!=` | RELATIONAL_OPERATOR |
| q₅ | Foi lido `<` | RELATIONAL_OPERATOR |
| q₆ | Foi lido `<=` | RELATIONAL_OPERATOR |
| q₇ | Foi lido `>` | RELATIONAL_OPERATOR |
| q₈ | Foi lido `>=` | RELATIONAL_OPERATOR |
| q_d | A cadeia deixou de corresponder a um único operador | Não aceita |

### 3.4 Tabela de transição

| Estado | `=` | `!` | `<` | `>` |
|---|---|---|---|---|
| → q₀ | q₁ | q₃ | q₅ | q₇ |
| * q₁ | q₂ | q_d | q_d | q_d |
| * q₂ | q_d | q_d | q_d | q_d |
| q₃ | q₄ | q_d | q_d | q_d |
| * q₄ | q_d | q_d | q_d | q_d |
| * q₅ | q₆ | q_d | q_d | q_d |
| * q₆ | q_d | q_d | q_d | q_d |
| * q₇ | q₈ | q_d | q_d | q_d |
| * q₈ | q_d | q_d | q_d | q_d |
| q_d | q_d | q_d | q_d | q_d |

### 3.5 Simulações de aceitação

#### Entrada: `=`

```text
q₀ ──=──> q₁
```

A entrada termina em q₁ ∈ F_OP.

Resultado:

```text
ASSIGNMENT("=")
```

#### Entrada: `==`

```text
q₀ ──=──> q₁
q₁ ──=──> q₂
```

A entrada termina em q₂ ∈ F_OP.

Resultado:

```text
RELATIONAL_OPERATOR("==")
```

#### Entrada: `!=`

```text
q₀ ──!──> q₃
q₃ ──=──> q₄
```

A entrada termina em q₄ ∈ F_OP.

Resultado:

```text
RELATIONAL_OPERATOR("!=")
```

#### Entrada: `<`

```text
q₀ ──<──> q₅
```

A entrada termina em q₅ ∈ F_OP.

Resultado:

```text
RELATIONAL_OPERATOR("<")
```

#### Entrada: `<=`

```text
q₀ ──<──> q₅
q₅ ──=──> q₆
```

A entrada termina em q₆ ∈ F_OP.

Resultado:

```text
RELATIONAL_OPERATOR("<=")
```

#### Entrada: `>`

```text
q₀ ──>──> q₇
```

A entrada termina em q₇ ∈ F_OP.

Resultado:

```text
RELATIONAL_OPERATOR(">")
```

#### Entrada: `>=`

```text
q₀ ──>──> q₇
q₇ ──=──> q₈
```

A entrada termina em q₈ ∈ F_OP.

Resultado:

```text
RELATIONAL_OPERATOR(">=")
```

### 3.6 Simulação de rejeição: `!`

```text
q₀ ──!──> q₃
```

A entrada termina em q₃ ∉ F_OP.

Nenhum prefixo aceito foi encontrado. O scanner informa erro léxico na posição de `!` e continua a análise.

Resultado:

```text
ERRO("!")
```

## 4. AFD de ARITHMETIC_OPERATOR

### 4.1 Linguagem reconhecida

```text
{ +, -, *, / }
```

Cada operador possui exatamente um caractere.

### 4.2 Definição formal

```text
M_AR = (Q_AR, Σ_AR, δ_AR, q₀, F_AR)

Q_AR = {q₀, q_f, q_d}

Σ_AR = {+, -, *, /}

F_AR = {q_f}
```

A função δ_AR é definida pela tabela de transição abaixo.

### 4.3 Significado dos estados

| Estado | Significado |
|---|---|
| q₀ | Aguarda um operador aritmético |
| q_f | Um operador aritmético foi reconhecido; é final |
| q_d | A cadeia não representa um único operador aritmético |

### 4.4 Tabela de transição

| Estado | `+` | `-` | `*` | `/` |
|---|---|---|---|---|
| → q₀ | q_f | q_f | q_f | q_f |
| * q_f | q_d | q_d | q_d | q_d |
| q_d | q_d | q_d | q_d | q_d |

### 4.5 Simulações de aceitação

| Entrada | Percurso | Resultado |
|---|---|---|
| `+` | q₀ ──+──> q_f | ARITHMETIC_OPERATOR |
| `-` | q₀ ──-──> q_f | ARITHMETIC_OPERATOR |
| `*` | q₀ ──*──> q_f | ARITHMETIC_OPERATOR |
| `/` | q₀ ──/──> q_f | ARITHMETIC_OPERATOR |

Todas terminam em q_f ∈ F_AR.

### 4.6 Dois operadores consecutivos: `++`

Como cadeia inteira:

```text
q₀ ──+──> q_f
q_f ──+──> q_d
```

A cadeia `++` é rejeitada como um único operador aritmético.

Na varredura, o scanner recupera o último prefixo aceito, emite o primeiro `+` e reinicia o reconhecimento no segundo `+`.

Resultado:

```text
ARITHMETIC_OPERATOR("+")
ARITHMETIC_OPERATOR("+")
```

A especificação não define um operador de incremento.

### 4.7 Operador antes de um número: `-5`

O reconhecedor aritmético aceita `-`:

```text
q₀ ──-──> q_f
```

O caractere seguinte, `5`, pertence ao reconhecimento numérico e inicia outro token.

Resultado:

```text
ARITHMETIC_OPERATOR("-")
INTEGER("5")
```

Não existe literal negativo na especificação atual.

## 5. AFD de DELIMITER

### 5.1 Linguagem reconhecida

```text
{ (, ), {, }, ;, , }
```

Cada delimitador possui exatamente um caractere.

### 5.2 Definição formal

```text
M_DEL = (Q_DEL, Σ_DEL, δ_DEL, q₀, F_DEL)

Q_DEL = {q₀, q_f, q_d}

Σ_DEL = { '(', ')', '{', '}', ';', ',' }

F_DEL = {q_f}
```

As aspas acima apenas separam visualmente os elementos do conjunto. Elas não fazem parte dos tokens.

A função δ_DEL é definida pela tabela de transição abaixo.

### 5.3 Significado dos estados

| Estado | Significado |
|---|---|
| q₀ | Aguarda um delimitador |
| q_f | Um delimitador foi reconhecido; é final |
| q_d | A cadeia não representa um único delimitador |

### 5.4 Tabela de transição

| Estado | `(` | `)` | `{` | `}` | `;` | `,` |
|---|---|---|---|---|---|---|
| → q₀ | q_f | q_f | q_f | q_f | q_f | q_f |
| * q_f | q_d | q_d | q_d | q_d | q_d | q_d |
| q_d | q_d | q_d | q_d | q_d | q_d | q_d |

### 5.5 Simulações de aceitação

| Entrada | Percurso | Resultado |
|---|---|---|
| `(` | q₀ ──(──> q_f | DELIMITER |
| `)` | q₀ ──)──> q_f | DELIMITER |
| `{` | q₀ ──{──> q_f | DELIMITER |
| `}` | q₀ ──}──> q_f | DELIMITER |
| `;` | q₀ ──;──> q_f | DELIMITER |
| `,` | q₀ ──,──> q_f | DELIMITER |

Todas terminam em q_f ∈ F_DEL.

### 5.6 Delimitadores consecutivos: `()`

Como cadeia inteira:

```text
q₀ ──(──> q_f
q_f ──)──> q_d
```

A cadeia `()` é rejeitada como um único delimitador.

No scanner, cada caractere é reconhecido separadamente, reiniciando o autômato entre os tokens:

```text
Primeiro token: q₀ ──(──> q_f
Segundo token:  q₀ ──)──> q_f
```

Resultado:

```text
DELIMITER("(")
DELIMITER(")")
```

O reconhecimento léxico não verifica o balanceamento de parênteses ou chaves.

## 6. Maximal munch

O scanner aplica a regra do maior prefixo aceito:

1. Inicia o reconhecedor em q₀.
2. Consome caracteres enquanto houver continuação válida.
3. Guarda o último estado final visitado e sua posição.
4. Quando a continuação falha, emite o maior prefixo aceito.
5. Reinicia a análise no primeiro caractere após o token emitido.
6. Se nenhum prefixo foi aceito, aplica o tratamento de erro correspondente.

Entrar no estado poço durante uma simulação de cadeia inteira significa rejeição dessa cadeia. Na varredura, a tentativa de entrar no poço encerra a busca pelo token atual; o scanner utiliza o último aceite registrado.

### 6.1 Exemplo: `>=`

```text
q₀ ──>──> q₇    último aceite: ">"
q₇ ──=──> q₈    último aceite: ">="
```

O scanner emite `>=` como um único RELATIONAL_OPERATOR, pois esse é o maior prefixo aceito.

### 6.2 Exemplo: `=<`

```text
q₀ ──=──> q₁    último aceite: "="
q₁ ──<──> q_d   a continuação falha
```

O scanner recupera o aceite de `=` e emite ASSIGNMENT.

O caractere `<` permanece disponível e inicia uma nova tentativa:

```text
q₀ ──<──> q₅
```

Resultado:

```text
ASSIGNMENT("=")
RELATIONAL_OPERATOR("<")
```

`=<` não é um operador único da linguagem.

### 6.3 Exemplo: `x!=y`

O scanner reconhece `x` pelo AFD de identificadores.

Ao encontrar `!`, inicia o AFD de operadores:

```text
q₀ ──!──> q₃
q₃ ──=──> q₄
```

O caractere `y` não pertence ao alfabeto desse reconhecedor. O token `!=` é concluído e `y` inicia um identificador.

Resultado:

```text
IDENTIFIER("x")
RELATIONAL_OPERATOR("!=")
IDENTIFIER("y")
```

## 7. Caracteres inválidos e continuidade da análise

### 7.1 Caractere fora do alfabeto: `@`

O caractere `@` não pertence ao alfabeto da Linguagem do Rato.

Ele não inicia nenhum dos tokens definidos. O scanner informa erro léxico com linha e coluna, consome o caractere e continua.

Resultado:

```text
ERRO("@")
```

Não é necessário acrescentar `@` aos alfabetos dos AFDs para representar esse comportamento: a identificação do caractere externo pertence ao controle do scanner.

### 7.2 Exemplo de continuidade: `!+;@`

Considerando a entrada na linha 1, com colunas contadas a partir de 1:

1. `!` leva o AFD de operadores a q₃, que não é final.
2. O próximo caractere, `+`, não completa `!=`.
3. O scanner informa erro para `!`, na coluna 1.
4. Reinicia a análise no `+`, reconhecendo ARITHMETIC_OPERATOR.
5. Reconhece `;` como DELIMITER.
6. Informa erro para `@`, na coluna 4.

Resultado:

```text
ERRO("!", linha=1, coluna=1)
ARITHMETIC_OPERATOR("+")
DELIMITER(";")
ERRO("@", linha=1, coluna=4)
```

A entrada `+` não é descartada junto com `!`.

## 8. Resumo de conferência

| Entrada | Resultado esperado |
|---|---|
| `=` | ASSIGNMENT |
| `==` | RELATIONAL_OPERATOR |
| `!=` | RELATIONAL_OPERATOR |
| `!` | Erro léxico |
| `<` | RELATIONAL_OPERATOR |
| `<=` | RELATIONAL_OPERATOR |
| `>` | RELATIONAL_OPERATOR |
| `>=` | RELATIONAL_OPERATOR |
| `=<` | ASSIGNMENT `=` e RELATIONAL_OPERATOR `<` |
| `+` | ARITHMETIC_OPERATOR |
| `-` | ARITHMETIC_OPERATOR |
| `*` | ARITHMETIC_OPERATOR |
| `/` | ARITHMETIC_OPERATOR |
| `;` | DELIMITER |
| `,` | DELIMITER |
| `(` | DELIMITER |
| `)` | DELIMITER |
| `{` | DELIMITER |
| `}` | DELIMITER |
| `@` | Erro léxico |
| `x!=y` | IDENTIFIER, RELATIONAL_OPERATOR e IDENTIFIER |

## 9. Referência para os diagramas

Os diagramas-base devem reproduzir as transições das tabelas:

- Atribuição e relacionais: q₀, q₁ a q₈ e q_d, com os sete estados finais indicados.
- Aritméticos: q₀, q_f e q_d.
- Delimitadores: q₀, q_f e q_d.

O estado poço pode ser omitido visualmente, desde que uma legenda informe que as transições não desenhadas levam a q_d.

A produção dos diagramas em TikZ pertence à T13. A demonstração de minimização pertence à T06.

## 10. Critérios de conclusão

- Tuplas formais dos três reconhecedores documentadas.
- Significado dos estados explicado.
- Tabelas de transição completas apresentadas.
- Todos os operadores e delimitadores simulados.
- Rejeição de `!` isolado demonstrada.
- Tratamento de caractere inválido demonstrado.
- Maximal munch explicado para operadores de um e dois caracteres.
- Diferença entre rejeitar uma cadeia inteira e emitir tokens consecutivos esclarecida.
- Correspondência com a especificação aprovada conferida pelo grupo.

## 11. Referências

- Especificação Léxica da Linguagem do Rato, versão 1.0 — seções 4.5, 4.6 e 6.
- Escopo do Projeto Linguagem do Rato — T05: AFD de operadores e delimitadores.