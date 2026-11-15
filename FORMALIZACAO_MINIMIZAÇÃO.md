# T06 — Formalização e minimização

## 1. Objetivo

Consolidar a formalização dos autômatos da Linguagem do Rato e demonstrar sua minimização pelo algoritmo de preenchimento de tabela.

Este documento utiliza as seções 4 e 5 da Especificação Léxica da Linguagem do Rato, versão 1.0, complementadas pelas formalizações da T04 e T05.

As regras léxicas da linguagem são preservadas. As inconsistências matemáticas identificadas no documento original são registradas explicitamente.

## 2. Notação formal

Um autômato finito determinístico é representado por:

M = (Q, Σ, δ, q₀, F)

Onde:

- Q: conjunto finito de estados.
- Σ: alfabeto de entrada.
- δ: função de transição, δ: Q × Σ → Q.
- q₀: estado inicial.
- F: conjunto de estados finais.

Convenções:

```text
L = {a, …, z, A, …, Z}
D = {0, …, 9}
```

q_d representa o estado poço.

Nas tabelas, → indica o estado inicial e * indica um estado final.

ε representa a cadeia vazia.

## 3. Consolidação dos modelos

Os nomes dos estados são locais a cada autômato.

| Modelo | Q | Σ | Inicial | F |
|---|---|---|---|---|
| IDENTIFIER | {q₀, q₁, q_d} | L ∪ D ∪ {_} | q₀ | {q₁} |
| INTEGER original | {q₀, q₁, q_d} | D | q₀ | {q₁} |
| FLOAT | {q₀, q₁, q₂, q₃, q_d} | D ∪ {.} | q₀ | {q₃} |
| Números combinados | {q₀, q₁, q₂, q₃, q_d} | D ∪ {.} | q₀ | {q₁, q₃} |
| Atribuição e relacionais | {q₀, q₁, q₂, q₃, q₄, q₅, q₆, q₇, q₈, q_d} | {=, !, <, >} | q₀ | {q₁, q₂, q₄, q₅, q₆, q₇, q₈} |
| Aritméticos | {q₀, q_f, q_d} | {+, -, *, /} | q₀ | {q_f} |
| Delimitadores | {q₀, q_f, q_d} | {'(', ')', '{', '}', ';', ','} | q₀ | {q_f} |

As funções de transição são as tabelas apresentadas na T04 e T05. As tabelas necessárias às demonstrações são reproduzidas nas seções seguintes.

## 4. Algoritmo de preenchimento de tabela

Antes de comparar estados, removem-se os estados inalcançáveis a partir de q₀.

Depois:

1. Listam-se todos os pares de estados distintos.
2. Na rodada 0, marcam-se os pares com um estado final e outro não final.
3. Nas rodadas seguintes, marca-se um par (p, q) quando existe um símbolo a tal que o par (δ(p,a), δ(q,a)) já estava marcado.
4. Repete-se o processo até nenhuma nova marcação ocorrer.
5. Pares não marcados representam estados equivalentes.
6. Estados equivalentes são agrupados no autômato mínimo.

Neste documento, cada rodada utiliza somente as marcações das rodadas anteriores.

Dois estados são distinguíveis quando existe uma cadeia que, partindo de um deles, termina em estado final e, partindo do outro, termina em estado não final.

Uma cadeia com essa propriedade é chamada de cadeia distinguidora.

## 5. AFD combinado de números

### 5.1 Definição e transições

```text
Q = {q₀, q₁, q₂, q₃, q_d}
Σ = D ∪ {.}
F = {q₁, q₃}

q₁ → INTEGER
q₃ → FLOAT
```

| Estado | D | `.` |
|---|---|---|
| → q₀ | q₁ | q_d |
| * q₁ | q₁ | q₂ |
| q₂ | q₃ | q_d |
| * q₃ | q₃ | q_d |
| q_d | q_d | q_d |

Todos os estados são alcançáveis:

| Estado | Entrada que o alcança |
|---|---|
| q₀ | ε |
| q₁ | `0` |
| q₂ | `0.` |
| q₃ | `0.0` |
| q_d | `.` |

### 5.2 Rodada 0

Marcam-se os pares final/não final:

```text
(q₀, q₁)
(q₁, q₂)
(q₁, q_d)
(q₀, q₃)
(q₂, q₃)
(q₃, q_d)
```

### 5.3 Rodada 1

```text
(q₀, q_d):
com 0 → (q₁, q_d), marcado na rodada 0.

(q₂, q_d):
com 0 → (q₃, q_d), marcado na rodada 0.
```

### 5.4 Rodada 2

```text
(q₁, q₃):
com . → (q₂, q_d), marcado na rodada 1.
```

### 5.5 Rodada 3

```text
(q₀, q₂):
com 0 → (q₁, q₃), marcado na rodada 2.
```

### 5.6 Tabela completa dos pares

| Par | Rodada | Cadeia distinguidora |
|---|---|---|
| (q₀, q₁) | 0 | ε |
| (q₀, q₂) | 3 | `0.0` |
| (q₀, q₃) | 0 | ε |
| (q₀, q_d) | 1 | `0` |
| (q₁, q₂) | 0 | ε |
| (q₁, q₃) | 2 | `.0` |
| (q₁, q_d) | 0 | ε |
| (q₂, q₃) | 0 | ε |
| (q₂, q_d) | 1 | `0` |
| (q₃, q_d) | 0 | ε |

### 5.7 Conclusão

Todos os dez pares foram marcados e todos os estados são alcançáveis.

Portanto, o AFD combinado de números já é mínimo, com cinco estados.

Os estados q₁ e q₃ permanecem distintos. A classificação INTEGER/FLOAT é preservada.

## 6. AFD de atribuição e operadores relacionais

### 6.1 Modelo original

```text
Q = {q₀, q₁, q₂, q₃, q₄, q₅, q₆, q₇, q₈, q_d}
Σ = {=, !, <, >}
F = {q₁, q₂, q₄, q₅, q₆, q₇, q₈}
```

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

Todos os estados são alcançáveis:

| Estado | Entrada |
|---|---|
| q₀ | ε |
| q₁ | `=` |
| q₂ | `==` |
| q₃ | `!` |
| q₄ | `!=` |
| q₅ | `<` |
| q₆ | `<=` |
| q₇ | `>` |
| q₈ | `>=` |
| q_d | `!!` |

### 6.2 Rodada 0

Finais:

```text
{q₁, q₂, q₄, q₅, q₆, q₇, q₈}
```

Não finais:

```text
{q₀, q₃, q_d}
```

Marcam-se todos os pares com um elemento de cada conjunto: 7 × 3 = 21 pares.

### 6.3 Rodada 1 — pares entre não finais

| Par | Símbolo | Par de destino |
|---|---|---|
| (q₀, q₃) | `<` | (q₅, q_d) |
| (q₀, q_d) | `=` | (q₁, q_d) |
| (q₃, q_d) | `=` | (q₄, q_d) |

Os três pares de destino foram marcados na rodada 0.

Logo, os três pares desta tabela são marcados.

### 6.4 Rodada 1 — pares entre finais

Considere os conjuntos:

```text
A = {q₁, q₅, q₇}
B = {q₂, q₄, q₆, q₈}
```

Um estado de A pode consumir `=` e continuar em um estado final.

Um estado de B, ao consumir `=`, vai para q_d.

Portanto, marcam-se os doze pares:

```text
(q₁, q₂), (q₁, q₄), (q₁, q₆), (q₁, q₈)
(q₅, q₂), (q₅, q₄), (q₅, q₆), (q₅, q₈)
(q₇, q₂), (q₇, q₄), (q₇, q₆), (q₇, q₈)
```

Para todos eles, `=` é uma cadeia distinguidora.

### 6.5 Rodada 2 — estabilização

Nenhum novo par é marcado.

Os pares internos a A permanecem não marcados:

```text
(q₁, q₅), (q₁, q₇), (q₅, q₇)
```

Os pares internos a B também permanecem não marcados:

```text
(q₂, q₄), (q₂, q₆), (q₂, q₈)
(q₄, q₆), (q₄, q₈), (q₆, q₈)
```

Em A, as transições com `=` levam a B e as demais levam a q_d.

Em B, todas as transições levam a q_d.

Assim, nenhuma continuação distingue estados de uma mesma classe.

Conferência:

```text
Total de pares: 10 × 9 / 2 = 45

Marcados na rodada 0: 21
Marcados na rodada 1: 15
Não marcados: 9

21 + 15 + 9 = 45
```

### 6.6 Classes de equivalência

```text
I = {q₀}
A = {q₁, q₅, q₇}
B = {q₂, q₄, q₆, q₈}
N = {q₃}
P = {q_d}
```

### 6.7 AFD mínimo

```text
M_OP_MIN = (Q', Σ, δ', I, F')

Q' = {I, A, B, N, P}
Σ = {=, !, <, >}
F' = {A, B}
```

| Estado | `=` | `!` | `<` | `>` |
|---|---|---|---|---|
| → I | A | N | A | A |
| * A | B | P | P | P |
| * B | P | P | P | P |
| N | B | P | P | P |
| P | P | P | P | P |

Esse resultado corresponde ao AFD mínimo apresentado no PDF, utilizando I para a classe inicial e P para a classe do estado poço.

### 6.8 Preservação da classificação

A minimização acima preserva a linguagem reconhecida:

```text
{ =, ==, !=, <, <=, >, >= }
```

Porém, a classe A reúne os lexemas `=`, `<` e `>`.

O estado final sozinho não permite distinguir ASSIGNMENT de RELATIONAL_OPERATOR.

Por isso, conforme a especificação, o scanner deve classificar pelo lexema:

```text
se lexema = "=" → ASSIGNMENT
senão          → RELATIONAL_OPERATOR
```

Exemplos:

| Lexema | Estado final mínimo | Categoria |
|---|---|---|
| `=` | A | ASSIGNMENT |
| `<` | A | RELATIONAL_OPERATOR |
| `>` | A | RELATIONAL_OPERATOR |
| `==` | B | RELATIONAL_OPERATOR |
| `!=` | B | RELATIONAL_OPERATOR |
| `<=` | B | RELATIONAL_OPERATOR |
| `>=` | B | RELATIONAL_OPERATOR |

Se a classificação precisar estar exclusivamente no estado final, sem consultar o lexema, ASSIGNMENT deve permanecer separado dos estados relacionais. Nesse outro critério de minimização, o modelo possui seis estados.

O modelo de cinco estados do PDF é correto para reconhecimento acompanhado de classificação pelo lexema.

## 7. Minimalidade do AFD de IDENTIFIER

### 7.1 Modelo

```text
Q = {q₀, q₁, q_d}
Σ = L ∪ D ∪ {_}
F = {q₁}
```

| Estado | L | D | `_` |
|---|---|---|---|
| → q₀ | q₁ | q_d | q₁ |
| * q₁ | q₁ | q₁ | q₁ |
| q_d | q_d | q_d | q_d |

Todos os estados são alcançáveis:

```text
q₀: ε
q₁: a
q_d: 0
```

### 7.2 Tabela de pares

| Par | Rodada | Justificativa |
|---|---|---|
| (q₀, q₁) | 0 | Um é final e o outro não |
| (q₁, q_d) | 0 | Um é final e o outro não |
| (q₀, q_d) | 1 | Com `a`, alcança (q₁, q_d), já marcado |

### 7.3 Conclusão

Todos os pares são distinguíveis e todos os estados são alcançáveis.

O AFD de IDENTIFIER é mínimo, com três estados.

A classificação de palavras reservadas continua sendo feita pela consulta ao conjunto K após o reconhecimento.

## 8. Minimização do AFD de INTEGER

### 8.1 Modelo original

```text
Q = {q₀, q₁, q_d}
Σ = D
F = {q₁}
```

| Estado | D |
|---|---|
| → q₀ | q₁ |
| * q₁ | q₁ |
| q_d | q_d |

### 8.2 Verificação de alcançabilidade

A partir de q₀:

- ε mantém o autômato em q₀.
- Qualquer dígito leva a q₁.
- Outros dígitos mantêm o autômato em q₁.

Não existe uma cadeia de D* que leve de q₀ a q_d.

Portanto, q_d é inalcançável e deve ser removido antes da minimização.

### 8.3 Tabela de pares após a remoção

Resta somente o par:

| Par | Rodada | Justificativa |
|---|---|---|
| (q₀, q₁) | 0 | q₀ não é final e q₁ é final |

Os dois estados são distinguíveis por ε.

### 8.4 AFD mínimo

```text
M_INT_MIN = ({q₀, q₁}, D, δ', q₀, {q₁})
```

| Estado | D |
|---|---|
| → q₀ | q₁ |
| * q₁ | q₁ |

### 8.5 Correção em relação ao PDF

O PDF afirma que o AFD de INTEGER com três estados é mínimo.

Com o alfabeto original Σ = D, essa afirmação não se sustenta porque q_d é inalcançável.

O mínimo possui dois estados e reconhece exatamente a mesma linguagem:

```text
D+
```

Essa correção não altera os números aceitos nem as regras do scanner.

Se fosse utilizado um alfabeto maior, contendo caracteres não numéricos, seria necessário definir as transições correspondentes. Esse seria outro modelo formal.

## 9. Minimalidade do AFD de FLOAT

### 9.1 Modelo

```text
Q = {q₀, q₁, q₂, q₃, q_d}
Σ = D ∪ {.}
F = {q₃}
```

| Estado | D | `.` |
|---|---|---|
| → q₀ | q₁ | q_d |
| q₁ | q₁ | q₂ |
| q₂ | q₃ | q_d |
| * q₃ | q₃ | q_d |
| q_d | q_d | q_d |

Todos os estados são alcançáveis:

```text
q₀: ε
q₁: 0
q₂: 0.
q₃: 0.0
q_d: .
```

### 9.2 Rodada 0

Marcam-se os pares com q₃, único estado final:

```text
(q₀, q₃)
(q₁, q₃)
(q₂, q₃)
(q₃, q_d)
```

### 9.3 Rodada 1

Marcam-se:

```text
(q₀, q₂):
com 0 → (q₁, q₃), marcado na rodada 0.

(q₁, q₂):
com 0 → (q₁, q₃), marcado na rodada 0.

(q₂, q_d):
com 0 → (q₃, q_d), marcado na rodada 0.
```

### 9.4 Rodada 2

Marcam-se:

```text
(q₀, q₁):
com . → (q_d, q₂), marcado na rodada 1.

(q₁, q_d):
com . → (q₂, q_d), marcado na rodada 1.
```

### 9.5 Rodada 3

Marca-se:

```text
(q₀, q_d):
com 0 → (q₁, q_d), marcado na rodada 2.
```

### 9.6 Tabela completa dos pares

| Par | Rodada | Cadeia distinguidora |
|---|---|---|
| (q₀, q₁) | 2 | `.0` |
| (q₀, q₂) | 1 | `0` |
| (q₀, q₃) | 0 | ε |
| (q₀, q_d) | 3 | `0.0` |
| (q₁, q₂) | 1 | `0` |
| (q₁, q₃) | 0 | ε |
| (q₁, q_d) | 2 | `.0` |
| (q₂, q₃) | 0 | ε |
| (q₂, q_d) | 1 | `0` |
| (q₃, q_d) | 0 | ε |

### 9.7 Conclusão

Todos os dez pares são distinguíveis e todos os estados são alcançáveis.

O AFD de FLOAT é mínimo, com cinco estados.

A conclusão do PDF é mantida, mas sua justificativa é completada: com rodadas simultâneas, a marcação termina na rodada 3, e não na rodada 1.

## 10. Minimalidade do AFD de operadores aritméticos

### 10.1 Modelo

```text
Q = {q₀, q_f, q_d}
Σ = {+, -, *, /}
F = {q_f}
```

Para todo símbolo c ∈ Σ:

```text
δ(q₀, c) = q_f
δ(q_f, c) = q_d
δ(q_d, c) = q_d
```

Todos os estados são alcançáveis:

```text
q₀: ε
q_f: +
q_d: ++
```

### 10.2 Tabela de pares

| Par | Rodada | Justificativa |
|---|---|---|
| (q₀, q_f) | 0 | Um é final e o outro não |
| (q_f, q_d) | 0 | Um é final e o outro não |
| (q₀, q_d) | 1 | Com `+`, alcança (q_f, q_d), já marcado |

### 10.3 Conclusão

O AFD é mínimo, com três estados.

A cadeia `++` é usada para alcançar q_d no reconhecimento de uma cadeia inteira. No scanner, ela corresponde a dois tokens `+`, conforme maximal munch.

## 11. Minimalidade do AFD de delimitadores

### 11.1 Modelo

```text
Q = {q₀, q_f, q_d}
Σ = { '(', ')', '{', '}', ';', ',' }
F = {q_f}
```

Para todo símbolo c ∈ Σ:

```text
δ(q₀, c) = q_f
δ(q_f, c) = q_d
δ(q_d, c) = q_d
```

Todos os estados são alcançáveis:

```text
q₀: ε
q_f: ;
q_d: ;;
```

### 11.2 Tabela de pares

| Par | Rodada | Justificativa |
|---|---|---|
| (q₀, q_f) | 0 | Um é final e o outro não |
| (q_f, q_d) | 0 | Um é final e o outro não |
| (q₀, q_d) | 1 | Com `;`, alcança (q_f, q_d), já marcado |

### 11.3 Conclusão

O AFD é mínimo, com três estados.

A cadeia `;;` é rejeitada como um único delimitador. No scanner, corresponde a dois tokens DELIMITER.

## 12. Resultado consolidado

| AFD | Estados no modelo original | Estados no mínimo | Resultado |
|---|---:|---:|---|
| IDENTIFIER | 3 | 3 | Já mínimo |
| INTEGER | 3 | 2 | Remoção de q_d inalcançável |
| FLOAT | 5 | 5 | Já mínimo |
| Números combinados | 5 | 5 | Já mínimo |
| Atribuição e relacionais | 10 | 5 | Fusão de estados equivalentes; classificação pelo lexema |
| Aritméticos | 3 | 3 | Já mínimo |
| Delimitadores | 3 | 3 | Já mínimo |

## 13. Registro das correções e decisões

| Ponto | Registro |
|---|---|
| INTEGER | O mínimo é de dois estados para Σ = D. O estado poço do modelo original é inalcançável. |
| FLOAT | A minimalidade foi demonstrada com todas as rodadas necessárias. |
| Operadores | O AFD mínimo de cinco estados preserva o reconhecimento; a categoria é recuperada pelo lexema. |
| Regras da linguagem | Nenhuma regra léxica foi alterada. |
| Palavras reservadas | Continuam sendo classificadas por consulta ao conjunto K; não foi criado um AFD próprio. |

As correções matemáticas devem ser comunicadas ao grupo para manter os documentos consistentes.

## 14. Verificação da entrega

O conteúdo matemático inclui:

- Formalização dos modelos.
- Verificação de alcançabilidade.
- Tabelas de pares e rodadas de marcação.
- Classes de equivalência dos operadores.
- Tabela do AFD mínimo de operadores.
- AFD mínimo de INTEGER.
- Justificativa de minimalidade dos demais AFDs.
- Explicação da preservação das categorias de tokens.

Para encerrar a tarefa no projeto:

- Integrar a seção correspondente ao relatório LaTeX.
- Solicitar a revisão independente prevista no escopo.
- Registrar a revisão e as correções aprovadas.

A revisão independente não é considerada realizada por este documento.

## 15. Referências

- Especificação Léxica da Linguagem do Rato, versão 1.0 — seções 4 e 5.
- Escopo do Projeto Linguagem do Rato — T06: Formalização e minimização.
- Formalizações da T04 e T05 do projeto.