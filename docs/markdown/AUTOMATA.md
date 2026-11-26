# Autômatos da Linguagem do Rato

AFDs do Scanner: formalização, simulações e minimização (T04, T05 e T06).
Strings usam um reconhecedor próprio; colchetes e o ponto de acesso a módulo foram acrescentados aos delimitadores.

## 1. Convenções

Cada AFD é `M = (Q, Σ, δ, q₀, F)` com `δ: Q × Σ → Q` total.

- `L = {a…z, A…Z}` e `D = {0…9}`. Nas tabelas, a coluna `L` ou `D` vale para qualquer símbolo da classe.
- `→` marca o estado inicial, `*` marca estado final e `q_d` é o poço (só transita para `q_d`).
- Os nomes dos estados são locais a cada AFD.
- Um símbolo fora do Σ do AFD não é tratado por ele: o scanner escolhe outro reconhecedor ou reporta erro.
- O AFD decide se uma **cadeia inteira** é aceita. Já o **scanner** aplica maximal munch (seção 4.4).

As diretivas de região (`#tunel`, `#toca`, `#vaparatunel`) estão formalizadas na seção 4.5.

## 2. Modelos

| AFD | Q | Σ | F |
|---|---|---|---|
| IDENTIFIER | {q₀, q₁, q_d} | L ∪ D ∪ {_} | {q₁} |
| INTEGER | {q₀, q₁} | D | {q₁} |
| FLOAT | {q₀, q₁, q₂, q₃, q_d} | D ∪ {.} | {q₃} |
| Números combinados | {q₀, q₁, q₂, q₃, q_d} | D ∪ {.} | {q₁, q₃} |
| Atribuição e relacionais | {q₀, …, q₈, q_d} | {=, !, <, >} | {q₁, q₂, q₄, q₅, q₆, q₇, q₈} |
| Aritméticos | {q₀, q_f, q_d} | {+, -, *, /} | {q_f} |
| Delimitadores | {q₀, q_f, q_d} | {(, ), {, }, [, ], ;, ,, .} | {q_f} |
| Palavra de diretiva (M_DIR) | {q₀, q₁, q₂, q_d} | {#} ∪ L ∪ {_} | {q₂} |
| Nome de região (M_NOME) | {p₀, p₁, q_d} | L ∪ D ∪ {_, espaço, tab} | {p₁} |

O estado inicial é sempre q₀.

## 3. Identificadores e números (T04)

### 3.1 IDENTIFIER

ER: `(L | _)(L | D | _)*`

| Estado | L | D | `_` | Significado |
|---|---|---|---|---|
| → q₀ | q₁ | q_d | q₁ | Nada lido |
| * q₁ | q₁ | q₁ | q₁ | Nome válido até aqui |
| q_d | q_d | q_d | q_d | Começou por dígito: não é identificador |

Letra ou `_` inicia o identificador e dígitos só entram depois do primeiro caractere. Assim, `1x` é rejeitado e não há conflito com INTEGER.

### 3.2 INTEGER e FLOAT

**INTEGER** (ER `D+`): `M = ({q₀, q₁}, D, δ, q₀, {q₁})`

| Estado | D | Significado |
|---|---|---|
| → q₀ | q₁ | Nada lido |
| * q₁ | q₁ | Um ou mais dígitos |

O PDF lista também `q_d`, mas com Σ = D ele é inalcançável e foi removido (seção 5.4). A linguagem é a mesma.

**FLOAT** (ER `D+ . D+`):

| Estado | D | `.` | Significado |
|---|---|---|---|
| → q₀ | q₁ | q_d | Nada lido |
| q₁ | q₁ | q₂ | Parte inteira lida |
| q₂ | q₃ | q_d | Ponto lido, falta dígito |
| * q₃ | q₃ | q_d | Parte decimal lida |
| q_d | q_d | q_d | Ponto inicial ou segundo ponto |

**Comparação** (cadeia inteira; `—` = `.` não pertence ao Σ do AFD):

| Entrada | INTEGER | FLOAT |
|---|---|---|
| `7` | aceita | rejeita (para em q₁) |
| `007` | aceita | rejeita (para em q₁) |
| `3.14` | — rejeita | aceita (q₃) |
| `5.` | — rejeita | rejeita (para em q₂) |
| `.5` | — rejeita | rejeita (q₀ → q_d) |

### 3.3 Números combinados

O scanner usa um único AFD para números. Ele tem a tabela do FLOAT, mas com `F = {q₁, q₃}`:

- **q₁ é final de INTEGER** (só dígitos).
- **q₃ é final de FLOAT** (dígitos, ponto, dígitos).

q₁ e q₃ são distinguíveis pela cadeia `.0` (seção 5.2), então a categoria nunca é ambígua.

### 3.4 Simulações

Os resultados abaixo seguem o scanner (maximal munch e regras 6 a 8 da especificação).

| Entrada | Percurso | Resultado |
|---|---|---|
| `nota1` | q₀ -n→ q₁ -o→ q₁ -t→ q₁ -a→ q₁ -1→ q₁ | IDENTIFIER |
| `_rato1` | q₀ -_→ q₁ -r→ q₁ … -1→ q₁ | IDENTIFIER |
| `1x` (AFD de identificador) | q₀ -1→ q_d | rejeita |
| `refarejar` | q₀ -r→ q₁ -e→ q₁ … -r→ q₁, lexema ∈ K | KEYWORD |
| `farejares` | q₀ -f→ q₁ … -s→ q₁, lexema ∉ K | IDENTIFIER |
| `007` | q₀ -0→ q₁ -0→ q₁ -7→ q₁ | INTEGER |
| `3.14` | q₀ -3→ q₁ -.→ q₂ -1→ q₃ -4→ q₃ | FLOAT |
| `5.` | q₀ -5→ q₁ -.→ q₂ (não final) | INTEGER `5` + erro em `.` |
| `5.abc` | q₀ -5→ q₁; o `.` seguido de letra vira delimitador | INTEGER `5`, DELIMITER `.`, IDENTIFIER `abc` |
| `.5` | q₀ -.→ q_d | erro em `.` + INTEGER `5` |
| `9.8.7` | q₀ -9→ q₁ -.→ q₂ -8→ q₃ -.→ q_d | FLOAT `9.8` + erro em `.` + INTEGER `7` |
| `123abc` | q₀ -1→ q₁ -2→ q₁ -3→ q₁, `a` ∉ Σ | erro único (regra 6) |

Em `5.`, o scanner volta ao último estado final (q₁) e emite `5`. Em `9.8.7`, volta a q₃ e emite `9.8`.

`123abc` é a única linha que **não** vem só do AFD: ele aceitaria `123` e o scanner leria `abc` como identificador. O erro único é a regra 6 da especificação (letra ou `_` colado a um número), que é controle do scanner.

Conferência com a especificação (seção 7, base do T11): sem divergências. **Reconferir contra o arquivo final de casos do T11.**

### 3.5 Palavras reservadas (conjunto K)

K é um conjunto finito, logo regular, com **24 palavras**. Elas não têm AFD próprio: o scanner lê o identificador inteiro pelo AFD da seção 3.1 e depois consulta K (`K ⊂ L(IDENTIFIER)`).

| Equivalente | Palavra | Equivalente | Palavra |
|---|---|---|---|
| `if` | `farejar` | `int` | `queijo` |
| `elif` | `refarejar` | `float` | `migalha` |
| `else` | `fujir` | `print` | `guinchar` |
| `while` | `roer` | `on` (evento) | `ouvir` |
| `return` | `voltar` | `emit` (evento) | `sinalizar` |
| `break` | `escapar` | `True` | `cheio` |
| `False` | `vazio` | `for` | `vasculhar` |
| `in` | `dentro` | `def` | `cavar` |
| `range` | `trilha` | | |
| `import` | `procure` | | |
| `bool` | `barriga` | `str` | `chiado` |
| `list` | `ninho` | `continue` | `seguir` |
| `switch` | `cace` | `case` | `presa` |

`vasculhar`, `dentro`, `cavar` e `trilha` vêm do `teste.ra` e dependem da decisão D02. As sete palavras das quatro últimas linhas da tabela (`procure`, `barriga`, `chiado`, `ninho`, `seguir`, `cace` e `presa`) vieram da evolução do Scanner e não constam de D02. Todas as palavras são lidas por inteiro antes da consulta ao conjunto K.

```text
se lexema ∈ K → KEYWORD
senão         → IDENTIFIER
```

## 4. Operadores, delimitadores e diretivas de região (T05)

### 4.1 Atribuição e relacionais

Linguagem: `{ =, ==, !=, <, <=, >, >= }`. Σ = {=, !, <, >}.

| Estado | Lido | `=` | `!` | `<` | `>` | Categoria |
|---|---|---|---|---|---|---|
| → q₀ | nada | q₁ | q₃ | q₅ | q₇ | — |
| * q₁ | `=` | q₂ | q_d | q_d | q_d | ASSIGNMENT |
| * q₂ | `==` | q_d | q_d | q_d | q_d | RELATIONAL |
| q₃ | `!` | q₄ | q_d | q_d | q_d | não aceita (falta `=`) |
| * q₄ | `!=` | q_d | q_d | q_d | q_d | RELATIONAL |
| * q₅ | `<` | q₆ | q_d | q_d | q_d | RELATIONAL |
| * q₆ | `<=` | q_d | q_d | q_d | q_d | RELATIONAL |
| * q₇ | `>` | q₈ | q_d | q_d | q_d | RELATIONAL |
| * q₈ | `>=` | q_d | q_d | q_d | q_d | RELATIONAL |
| q_d | — | q_d | q_d | q_d | q_d | não aceita |

### 4.2 Aritméticos e delimitadores

Os dois AFDs têm a mesma forma, com `Q = {q₀, q_f, q_d}` e `F = {q_f}`:

| Estado | qualquer c ∈ Σ |
|---|---|
| → q₀ | q_f |
| * q_f | q_d |
| q_d | q_d |

- **Aritméticos:** Σ = {+, -, *, /}. Categoria ARITHMETIC_OPERATOR.
- **Delimitadores:** Σ = {(, ), {, }, [, ], ;, ,, .}. Categoria DELIMITER.

Strings são reconhecidas caractere a caractere, fora dos AFDs desta tabela. Aspas duplas delimitam o lexema; escapes JSON são permitidos e a quebra de linha encerra uma string sem fechamento. O ponto é delimitador quando vem logo antes de letra ou `_` (`modulo.funcao`); nos demais casos segue o reconhecimento numérico, e `5.` ou `.5` geram erro no ponto. Por isso `5.abc` gera INTEGER `5`, DELIMITER `.` e IDENTIFIER `abc`, sem erro.

### 4.3 Simulações

| Entrada | Percurso | Resultado |
|---|---|---|
| `=` | q₀ -=→ q₁ | ASSIGNMENT |
| `==` | q₀ -=→ q₁ -=→ q₂ | RELATIONAL |
| `!=` | q₀ -!→ q₃ -=→ q₄ | RELATIONAL |
| `!` | q₀ -!→ q₃ (não final) | erro léxico |
| `<=` | q₀ -<→ q₅ -=→ q₆ | RELATIONAL |
| `>=` | q₀ -`>`→ q₇ -`=`→ q₈ | RELATIONAL |
| `+` (também `-`, `*`, `/`) | q₀ -+→ q_f | ARITHMETIC_OPERATOR |
| `;` (também `(`, `)`, `{`, `}`, `[`, `]`, `,`, `.` em acesso a módulo) | q₀ -;→ q_f | DELIMITER |
| `@` | sem reconhecedor (∉ Σ) | erro léxico |

### 4.4 Maximal munch no scanner

1. Parte de q₀ e consome enquanto houver transição que não vá a q_d.
2. Guarda o último estado final visitado e a posição.
3. Ao falhar, emite o maior prefixo aceito e recomeça no caractere seguinte.
4. Se nunca houve estado final, reporta erro no primeiro caractere, consome-o e continua.

| Entrada | Tokens |
|---|---|
| `>=` | RELATIONAL `>=` (maior prefixo, não `>` + `=`) |
| `=<` | ASSIGNMENT `=`, RELATIONAL `<` (`=<` não é operador) |
| `x!=y` | IDENTIFIER `x`, RELATIONAL `!=`, IDENTIFIER `y` |
| `++` | ARITHMETIC `+`, ARITHMETIC `+` (não existe incremento) |
| `-5` | ARITHMETIC `-`, INTEGER `5` (não existe literal negativo) |
| `()` | DELIMITER `(`, DELIMITER `)` (balanceamento não é léxico) |
| `!+;@` | erro `!` (col. 1), ARITHMETIC `+`, DELIMITER `;`, erro `@` (col. 4) |

No último caso, o erro em `!` não descarta o `+`.

### 4.5 Diretivas de região

Formas: `#tunel nome` (abre região), `#toca` (fecha) e `#vaparatunel nome` (salta). O Scanner as reconhece em três etapas, cada uma um AFD simples.

**Etapa 1: palavra da diretiva (M_DIR).** Lê `#` e a maior sequência de letras ou `_` que vem depois. Σ = {#} ∪ L ∪ {_}, F = {q₂}.

| Estado | `#` | L | `_` | Significado |
|---|---|---|---|---|
| → q₀ | q₁ | q_d | q_d | Nada lido |
| q₁ | q_d | q₂ | q₂ | `#` lido |
| * q₂ | q_d | q₂ | q₂ | Palavra lida |
| q_d | q_d | q_d | q_d | Sem palavra (`#` seguido de espaço, dígito ou símbolo) |

A palavra lida é consultada no conjunto `D = {tunel, toca, vaparatunel}`, como o conjunto K das palavras reservadas. Se `palavra ∈ D`, segue a etapa 2; se não, o Scanner reporta erro no `#` e recomeça logo depois dele (`#foo` gera erro e depois IDENTIFIER `foo`).

**Etapa 2: nome da região (M_NOME), só após `tunel` e `vaparatunel`.** Pula espaços e tabs e lê letras, dígitos ou `_`. Σ = L ∪ D ∪ {_, espaço, tab}, F = {p₁}.

| Estado | L | D | `_` | espaço ou tab |
|---|---|---|---|---|
| → p₀ | p₁ | p₁ | p₁ | p₀ |
| * p₁ | p₁ | p₁ | p₁ | q_d |
| q_d | q_d | q_d | q_d | q_d |

Se o nome ficar vazio (p₀ não é final), é erro: `'#tunel' sem nome`.

**Etapa 3: resto da linha.** Tudo até o `\n` (exclusive) é descartado. O padrão é `R = (Σ ∖ {\n})*`.

**Tokens emitidos** (linha e coluna apontam para o `#`):

| Diretiva | Token | Lexema |
|---|---|---|
| `#tunel nome` | REGION_START | `nome` |
| `#toca` | REGION_END | vazio |
| `#vaparatunel nome` | GOTO_REGION | `nome` |

**Simulações:**

| Entrada | Percurso | Resultado |
|---|---|---|
| `#tunel inicio` | M_DIR: q₀ -#→ q₁ -t→ q₂ … -l→ q₂, `tunel` ∈ D. M_NOME: p₀ -espaço→ p₀ -i→ p₁ … -o→ p₁ | REGION_START `inicio` |
| `#vaparatunel x` | M_DIR lê `vaparatunel` ∈ D. M_NOME: p₀ -espaço→ p₀ -x→ p₁ | GOTO_REGION `x` |
| `#toca` | M_DIR lê `toca` ∈ D | REGION_END |
| `#tunel` | M_DIR lê `tunel` ∈ D; M_NOME: p₀ não final | erro no `#`; depois IDENTIFIER `tunel` |
| `#foo` | M_DIR lê `foo` ∉ D | erro no `#`; depois IDENTIFIER `foo` |
| `# tunel a` | q₀ -#→ q₁ -espaço→ q_d | erro no `#`; depois IDENTIFIER `tunel` e `a` |
| `#tocaX` | M_DIR lê `tocaX` ∉ D | erro no `#`; depois IDENTIFIER `tocaX` |

**Comportamentos do código que a formalização revela** (decisões D03 e D04 da especificação):

- **Dígito encerra a palavra:** `#tunel1` e `#toca1` são aceitos, pois M_DIR para no `1`. O primeiro vira REGION_START com nome `1`.
- **Nome de região pode começar por dígito** (`#tunel 1abc`), ao contrário do IDENTIFIER da seção 3.1.
- **Resto da linha é descartado sem análise:** `#toca guinchar(1);` ignora o `guinchar`, e `#tunel a @@` não gera erro.

## 5. Minimização (T06)

### 5.1 Método

Primeiro removem-se os estados inalcançáveis. Depois, pelo preenchimento de tabela:

- **Rodada 0:** marca-se todo par (final, não final).
- **Rodada k:** marca-se (p, q) se existe símbolo `a` com (δ(p,a), δ(q,a)) marcado em rodada anterior.
- Repete-se até estabilizar. Pares não marcados são equivalentes e são fundidos.

Uma **cadeia distinguidora** de (p, q) leva um dos estados a final e o outro a não final.

### 5.2 Números combinados: já é mínimo (5 estados)

Alcançáveis: q₀ (ε), q₁ (`0`), q₂ (`0.`), q₃ (`0.0`), q_d (`.`). Sendo F = {q₁, q₃}:

| Rodada | Pares marcados | Motivo |
|---|---|---|
| 0 | (q₀,q₁) (q₀,q₃) (q₁,q₂) (q₁,q_d) (q₂,q₃) (q₃,q_d) | final × não final |
| 1 | (q₀,q_d) (q₂,q_d) | com `0` vão a (q₁,q_d) e (q₃,q_d), da rodada 0 |
| 2 | (q₁,q₃) | com `.` vai a (q₂,q_d), da rodada 1 |
| 3 | (q₀,q₂) | com `0` vai a (q₁,q₃), da rodada 2 |

Os 10 pares ficam marcados, então não há fusão. Cadeias distinguidoras: (q₁,q₃) por `.0`, (q₀,q₂) por `0.0` e (q₀,q_d) por `0`. Como q₁ e q₃ continuam separados, INTEGER e FLOAT se mantêm distintos.

### 5.3 Atribuição e relacionais: de 10 para 5 estados

Todos são alcançáveis (q_d por `!!`). Finais: {q₁, q₂, q₄, q₅, q₆, q₇, q₈}. Não finais: {q₀, q₃, q_d}.

| Rodada | Pares marcados | Motivo |
|---|---|---|
| 0 | 21 (7 finais × 3 não finais) | final × não final |
| 1 | (q₀,q₃) | com `<` vai a (q₅,q_d) |
| 1 | (q₀,q_d), (q₃,q_d) | com `=` vão a (q₁,q_d) e (q₄,q_d) |
| 1 | 12 pares entre A = {q₁,q₅,q₇} e B = {q₂,q₄,q₆,q₈} | com `=`, A segue para final e B vai a q_d |
| 2 | nenhum | estabilizou |

Conferência: 45 pares = 21 + 15 + 9 não marcados (3 em A e 6 em B).

**Classes:** I = {q₀}, A = {q₁, q₅, q₇}, B = {q₂, q₄, q₆, q₈}, N = {q₃}, P = {q_d}.

**AFD mínimo:** `M_OP_MIN = ({I, A, B, N, P}, {=, !, <, >}, δ', I, {A, B})`

| Estado | `=` | `!` | `<` | `>` |
|---|---|---|---|---|
| → I | A | N | A | A |
| * A | B | P | P | P |
| * B | P | P | P | P |
| N | B | P | P | P |
| P | P | P | P | P |

**Classificação.** O mínimo preserva a linguagem, mas A mistura `=`, `<` e `>`, e o estado não separa ASSIGNMENT de RELATIONAL. Por isso o scanner classifica pelo lexema: `=` → ASSIGNMENT, os demais → RELATIONAL. Se a categoria tivesse de sair só do estado final, ASSIGNMENT teria de ficar separado e o modelo teria 6 estados.

### 5.4 Demais AFDs

**FLOAT: mínimo (5 estados).** Alcançáveis: q₀ (ε), q₁ (`0`), q₂ (`0.`), q₃ (`0.0`), q_d (`.`). Único final: q₃.

| Rodada | Pares marcados | Motivo |
|---|---|---|
| 0 | (q₀,q₃) (q₁,q₃) (q₂,q₃) (q₃,q_d) | final × não final |
| 1 | (q₀,q₂) (q₁,q₂) (q₂,q_d) | com `0` vão a (q₁,q₃) ou (q₃,q_d) |
| 2 | (q₀,q₁) (q₁,q_d) | com `.` vão a (q_d,q₂) e (q₂,q_d) |
| 3 | (q₀,q_d) | com `0` vai a (q₁,q_d) |

Os 10 pares ficam marcados e não há fusão.

**INTEGER: mínimo com 2 estados.** Com Σ = D, nenhuma cadeia leva q₀ a q_d, então q_d é inalcançável e sai. Resta o par (q₀,q₁), distinguido por ε na rodada 0. A linguagem `D+` não muda. Isso corrige a afirmação do PDF de que o modelo de 3 estados é mínimo.

**M_DIR: mínimo (4 estados).** Alcançáveis: q₀ (ε), q₁ (`#`), q₂ (`#a`), q_d (`a`). Único final: q₂.

| Rodada | Pares marcados | Motivo |
|---|---|---|
| 0 | (q₀,q₂) (q₁,q₂) (q₂,q_d) | final × não final |
| 1 | (q₁,q_d) (q₀,q₁) | com L vão a (q₂,q_d) e (q_d,q₂) |
| 2 | (q₀,q_d) | com `#` vai a (q₁,q_d) |

Os 6 pares ficam marcados e não há fusão.

**M_NOME: mínimo (3 estados).** Alcançáveis: p₀ (ε), p₁ (`a`), q_d (`a espaço`). Rodada 0: (p₀,p₁) e (p₁,q_d). Rodada 1: (p₀,q_d), pois com L vai a (p₁,q_d).

**IDENTIFIER, aritméticos e delimitadores: mínimos com 3 estados.** Todos têm a mesma estrutura de pares:

| AFD | Alcança q₀, q₁ (ou q_f), q_d por | Rodada 0 | Rodada 1 |
|---|---|---|---|
| IDENTIFIER | ε, `a`, `0` | (q₀,q₁) (q₁,q_d) | (q₀,q_d) com `a` → (q₁,q_d) |
| Aritméticos | ε, `+`, `++` | (q₀,q_f) (q_f,q_d) | (q₀,q_d) com `+` → (q_f,q_d) |
| Delimitadores | ε, `;`, `;;` | (q₀,q_f) (q_f,q_d) | (q₀,q_d) com `;` → (q_f,q_d) |

### 5.5 Resultado

| AFD | Estados no modelo original | Estados no mínimo | Observação |
|---|---:|---:|---|
| IDENTIFIER | 3 | 3 | Já mínimo |
| INTEGER | 3 | 2 | q_d inalcançável removido |
| FLOAT | 5 | 5 | Já mínimo |
| Números combinados | 5 | 5 | Já mínimo |
| Atribuição e relacionais | 10 | 5 | Fusão A e B; categoria pelo lexema |
| Aritméticos | 3 | 3 | Já mínimo |
| Delimitadores | 3 | 3 | Já mínimo |
| Palavra de diretiva (M_DIR) | 4 | 4 | Já mínimo |
| Nome de região (M_NOME) | 3 | 3 | Já mínimo |

Palavras reservadas não têm AFD próprio: o scanner lê o identificador completo e consulta o conjunto K (24 palavras, seção 3.5).

## 6. Pendências

- [ ] Diagramas TikZ de todos os AFDs (T13), conferidos com as tabelas acima.
- [ ] Revisão independente da minimização (T06), por alguém que não fez os cálculos.
- [ ] Reconferir a seção 3.4 contra os casos finais do T11.
- [ ] Avisar o grupo da correção do INTEGER (2 estados).
- [ ] Decidir D03 e D04 (token das diretivas e resto da linha) em SPECIFICATIONS.md.
- [ ] Aprovar as 11 palavras acrescentadas depois das 13 do PDF (4 em D02 e 7 sem decisão registrada) e manter K igual em todos os documentos.
