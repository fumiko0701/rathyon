# T02 — Formalizar expressões regulares

## 1. Objetivo

Documentar os padrões de identificadores, inteiros, decimais, operadores, delimitadores e palavras reservadas da Linguagem do Rato, explicando a prioridade de classificação de KEYWORD sobre IDENTIFIER.

Este documento utiliza a Especificação Léxica da Linguagem do Rato, versão 1.0 (rascunho para aprovação), sem alterar suas expressões ou regras.

## 2. Notação

Sejam:

- `letra = a|b|…|z|A|B|…|Z`
- `digito = 0|1|…|9`

Convenções:

| Notação | Significado |
|---|---|
| `a|b` | União: a ou b |
| `ab` | Concatenação |
| `a*` | Fecho de Kleene: zero ou mais repetições |
| `a+` | Uma ou mais repetições, equivalente a `aa*` |

Nas expressões abaixo, os caracteres dos operadores e delimitadores representam os símbolos literais da linguagem. O ponto de FLOAT representa o caractere `.`.

## 3. Expressões regulares

As expressões abaixo são mantidas conforme a seção 3 da especificação original.

```text
IDENTIFIER = (letra | _)(letra | digito | _)*

INTEGER = digito digito*

FLOAT = digito+ . digito+

ARITHMETIC = + | - | * | /

RELATIONAL = == | != | >= | <= | > | <

ASSIGNMENT = =

DELIMITER = ( | ) | { | } | ; | ,

KEYWORD = farejar | refarejar | fujir | roer | queijo | migalha
          | guinchar | ouvir | sinalizar | voltar | escapar | cheio
          | vazio | vasculhar | dentro | trilha | cavar
```

**Diretivas de região.** Não pertencem às categorias acima. Sejam `ESP = (espaço | tab)` e `RESTO = (qualquer caractere exceto \n)*`:

```
DIR_TUNEL = #tunel  ESP*  (letra | digito | _)+  RESTO
DIR_GOTO  = #vaparatunel  ESP*  (letra | digito | _)+  RESTO
DIR_TOCA  = #toca  RESTO
```

Condição: a palavra depois do `#` é a maior sequência de `(letra | _)`, e ela deve ser exatamente `tunel`, `vaparatunel` ou `toca`. Por isso `#tocaX` é erro e `#toca1` é aceito. AFDs e simulações em [AUTOMATA.md](AUTOMATA.md#45-diretivas-de-região); decisões D03 e D04 em [SPECIFICATIONS.md](SPECIFICATIONS.md).

Na tabela de categorias da especificação, ARITHMETIC corresponde a ARITHMETIC_OPERATOR e RELATIONAL corresponde a RELATIONAL_OPERATOR. As expressões acima preservam os nomes utilizados na seção original.

## 4. Descrição dos padrões

### 4.1 IDENTIFIER

Começa com uma letra sem acento ou sublinhado (`_`). Os caracteres seguintes podem ser letras sem acento, dígitos ou sublinhados.

### 4.2 INTEGER

Contém um ou mais dígitos, sem sinal. Zeros à esquerda são aceitos.

O sinal `-` é um operador separado: `-5` produz ARITHMETIC_OPERATOR `-` e INTEGER `5`.

### 4.3 FLOAT

Contém um ou mais dígitos antes do ponto e um ou mais dígitos depois dele. As duas partes são obrigatórias.

### 4.4 ARITHMETIC

Reconhece um dos operadores aritméticos: `+`, `-`, `*` ou `/`.

### 4.5 RELATIONAL

Reconhece um dos operadores relacionais: `==`, `!=`, `>=`, `<=`, `>` ou `<`.

O caractere `!` isolado não é aceito.

### 4.6 ASSIGNMENT

Reconhece o símbolo de atribuição `=`.

### 4.7 DELIMITER

Reconhece um dos delimitadores: `(`, `)`, `{`, `}`, `;` ou `,`.

### 4.8 KEYWORD

Reconhece exatamente uma das 17 palavras reservadas:

| Palavra reservada |
|---|
| farejar |
| refarejar |
| fujir |
| roer |
| queijo |
| migalha |
| guinchar |
| ouvir |
| sinalizar |
| voltar |
| escapar |
| cheio |
| vazio |
| vasculhar |
| dentro |
| trilha |
| cavar |

Conforme a especificação atual, `cheio` e `vazio` pertencem à categoria KEYWORD. As palavras `vasculhar`, `dentro`, `trilha` e `cavar` vêm do `teste.ra` e dependem da decisão D02 da especificação.

## 5. Prioridade de KEYWORD sobre IDENTIFIER

Todo elemento de K também pertence a L(IDENTIFIER):

```text
K ⊂ L(IDENTIFIER)
```

O scanner reconhece primeiro a palavra completa pelo AFD de identificador e, depois, consulta o conjunto K:

```text
se lexema ∈ K → KEYWORD
senão        → IDENTIFIER
```

A linguagem é case-sensitive: as palavras reservadas são escritas em letras minúsculas.

| Lexema | Classificação | Justificativa |
|---|---|---|
| `farejar` | KEYWORD | Pertence a K |
| `refarejar` | KEYWORD | A palavra completa pertence a K |
| `farejares` | IDENTIFIER | Corresponde ao padrão de identificador, mas não pertence a K |
| `Farejar` | IDENTIFIER | A capitalização é diferente da palavra reservada |
| `_rato1` | IDENTIFIER | Corresponde ao padrão de identificador e não pertence a K |

O reconhecimento utiliza maximal munch: o scanner devolve o maior prefixo aceito. Assim, `refarejar` é reconhecido inteiro, e `farejares` não é dividido em uma palavra reservada e um sufixo.

## 6. Exemplos aceitos e rejeitados

Nesta tabela, “rejeitado” significa que a entrada inteira não corresponde ao padrão indicado. Isso não significa necessariamente que todos os seus caracteres geram erro: o scanner pode reconhecer tokens separados.

| Padrão | Exemplos aceitos | Exemplos rejeitados como um único lexema desse padrão |
|---|---|---|
| IDENTIFIER | `rato`, `_rato1`, `nota1`, `Farejar` | `1rato`, `rato@`, `3.14` |
| INTEGER | `0`, `5`, `007`, `123` | `-5`, `3.14`, `123abc` |
| FLOAT | `3.14`, `10.5`, `0.0` | `5.`, `.5`, `9.8.7`, `5` |
| ARITHMETIC | `+`, `-`, `*`, `/` | `=`, `>=`, `++` |
| RELATIONAL | `==`, `!=`, `>=`, `<=`, `>`, `<` | `!`, `=`, `=<` |
| ASSIGNMENT | `=` | `==`, `!=`, `=<` |
| DELIMITER | `(`, `)`, `{`, `}`, `;`, `,` | `.`, `_`, `()` |
| KEYWORD | `farejar`, `refarejar`, `cheio`, `vazio`, `vasculhar` | `Farejar`, `farejares`, `_rato1` |

Embora `farejar` corresponda à expressão de IDENTIFIER, sua classificação final é KEYWORD devido à consulta ao conjunto K.

## 7. Casos de decisão do scanner

Os resultados abaixo seguem as regras da especificação original.

| Entrada | Resultado esperado |
|---|---|
| `farejar` | KEYWORD |
| `refarejar` | KEYWORD, em um único token |
| `farejares` | IDENTIFIER |
| `Farejar` | IDENTIFIER |
| `_rato1` | IDENTIFIER |
| `007` | INTEGER |
| `3.14` | FLOAT |
| `-5` | ARITHMETIC_OPERATOR `-` e INTEGER `5` |
| `123abc` | Um único erro léxico de número malformado, consumindo toda a sequência |
| `5.` | INTEGER `5` e erro no ponto |
| `.5` | Erro no ponto e INTEGER `5` |
| `9.8.7` | FLOAT `9.8`, erro no segundo ponto e INTEGER `7` |
| `>=` | RELATIONAL_OPERATOR, em um único token |
| `=<` | ASSIGNMENT `=` e RELATIONAL_OPERATOR `<` |
| `!` | Erro léxico |
| `x!=y` | IDENTIFIER `x`, RELATIONAL_OPERATOR `!=` e IDENTIFIER `y` |
| `@` | Erro léxico |
| `cheio` | KEYWORD |
| `vasculhar` | KEYWORD |
| `dentro1` | IDENTIFIER (a palavra inteira não pertence a K) |

Espaço, tabulação e quebra de linha são ignorados e funcionam como separadores. Não há comentários na especificação atual.

## 8. Critérios de conclusão da T02

- Expressões regulares documentadas para todas as categorias previstas.
- Notação das expressões explicada.
- Prioridade de KEYWORD sobre IDENTIFIER explicada.
- Exemplos aceitos e rejeitados apresentados para cada padrão.
- Padrões conferidos com a proposta da T01; a aprovação do grupo continua pendente.
- Seção correspondente integrada ao relatório em LaTeX.

Este arquivo constitui o entregável Markdown da T02. A aprovação da especificação na T01 e a integração ao relatório LaTeX devem ser verificadas pelo grupo.

## 9. Referências

- Especificação Léxica da Linguagem do Rato, versão 1.0 — seções 1, 2, 3, 6 e 7.
- Escopo do Projeto Linguagem do Rato — tarefa T02: Formalizar expressões regulares