# Especificação Léxica — Linguagem do Rato

- **Versão:** 0.2-rascunho — T01.
- **Data:** 15/11/2026.
- **Etapa:** em criação, antes do beta.
- **Status:** aguardando validação do grupo.
- **Fontes:** PDF *Especificação Léxica da Linguagem do Rato* (v1.0, rascunho) e T01 do documento de escopo.

## 1. Objetivo e status

Definir os caracteres, tokens e regras do analisador léxico. Ele reconhece partes do código e informa erros com linha e coluna. Não executa programas nem verifica a sintaxe completa.

Este arquivo contém apenas a T01. As regras seguem o PDF e têm status **PROPOSTA**. As escolhas em aberto estão como **PENDENTE**. Usar **APROVADA** somente após registrar a confirmação do grupo.

## 2. Alfabeto e separadores

| Grupo | Caracteres |
| --- | --- |
| Letras `L` | `a` a `z` e `A` a `Z`, sem acento |
| Dígitos `D` | `0` a `9` |
| Símbolos | `+`, `-`, `*`, `/`, `=`, `!`, `<`, `>`, `(`, `)`, `{`, `}`, `;`, `,`, `.`, `_` |
| Separadores | Espaço, tabulação e quebra de linha (`\n`) |

O alfabeto `Σ` reúne esses quatro grupos. Separadores não geram tokens. `!` e `.` pertencem ao alfabeto, mas não são tokens isolados.

## 3. Categorias de tokens

Um **token** é uma parte reconhecida do código, como um nome, número ou operador.

| Categoria | O que reconhece |
| --- | --- |
| `KEYWORD` | Palavras reservadas da seção 4 |
| `IDENTIFIER` | Nomes de variáveis, eventos e funções |
| `INTEGER` | Inteiros sem sinal |
| `FLOAT` | Decimais com ponto |
| `ARITHMETIC_OPERATOR` | `+`, `-`, `*`, `/` |
| `RELATIONAL_OPERATOR` | `==`, `!=`, `>=`, `<=`, `>`, `<` |
| `ASSIGNMENT` | `=` |
| `DELIMITER` | `(`, `)`, `{`, `}`, `;`, `,` |

## 4. Palavras reservadas — conjunto K

As 13 palavras abaixo são `KEYWORD` na proposta atual. A categoria de `cheio` e `vazio` ainda será confirmada.

| Palavra | Referência |
| --- | --- |
| `farejar` | `if` |
| `refarejar` | `elif` |
| `fujir` | `else` |
| `roer` | `while` |
| `voltar` | `return` |
| `escapar` | `break` |
| `queijo` | Tipo `int` |
| `migalha` | Tipo `float` |
| `guinchar` | `print` |
| `ouvir` | `on` — evento |
| `sinalizar` | `emit` — disparar evento |
| `cheio` | `true` |
| `vazio` | `false` |

A grafia `fujir` foi mantida conforme o PDF. As referências explicam os nomes; não definem como os comandos serão executados.

## 5. Regras confirmadas no documento-base

Confirmadas no PDF, mas ainda **PROPOSTAS** para aprovação do grupo:

1. **Identificadores:** começam por letra ou `_`. Depois, aceitam letras, dígitos e `_`. Exemplos: `contador`, `_rato1`, `_`.
2. **Palavras reservadas:** ler a palavra inteira e consultar `K`. `farejar` é `KEYWORD`; `farejares` é `IDENTIFIER`.
3. **Maiúsculas:** fazem diferença. `Farejar` é `IDENTIFIER`.
4. **Inteiros:** têm um ou mais dígitos. Zeros à esquerda são aceitos: `007` é `INTEGER`.
5. **Decimais:** exigem dígitos antes e depois do ponto. `3.14` é `FLOAT`; `5.` e `.5` não são.
6. **Menos:** `-` é sempre operador. `-5` gera operador `-` e inteiro `5`.
7. **Maior casamento (maximal munch):** escolher o maior trecho aceito, guardando o último estado final. `>=` gera um único token.
8. **Posição:** ignorar separadores na saída, mas registrar linha e coluna de tokens e erros.
9. **Erros:** caracteres fora de `Σ`, como `@`, e `!` isolado geram erro. A leitura continua depois deles.

As regras numéricas abaixo estão **PENDENTES** de confirmação:

| Entrada | Resultado proposto no PDF |
| --- | --- |
| `123abc` | Um erro que consome toda a sequência; não emitir `123` separadamente |
| `5.` | `INTEGER("5")` e erro no ponto |
| `.5` | Erro no ponto e `INTEGER("5")` |
| `9.8.7` | `FLOAT("9.8")`, erro no segundo ponto e `INTEGER("7")` |

O erro único de `123abc` é uma regra especial: apenas reconhecer os tokens válidos pelo maior casamento não basta para produzir esse resultado.

Comentários e strings não estão previstos na proposta inicial; confirmar esse limite na seção 6.

## 6. Decisões pendentes

Todas aguardam resposta do grupo. Ao decidir, registrar em `decisions.md`: data, resposta, justificativa, quem validou e regras afetadas.

### D01 — cheio e vazio

- **Alternativas:** manter `KEYWORD` ou criar `BOOLEAN`.