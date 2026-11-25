# Especificação Léxica — Linguagem do Rato

- **Versão:** 0.3-rascunho — T01.
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
| Símbolos | `+`, `-`, `*`, `/`, `=`, `!`, `<`, `>`, `(`, `)`, `{`, `}`, `;`, `,`, `.`, `_`, `#` |
| Separadores | Espaço, tabulação e quebra de linha (`\n`) |

O alfabeto `Σ` reúne esses quatro grupos. Separadores não geram tokens. `!` e `.` pertencem ao alfabeto, mas não são tokens isolados. `#` só é válido no início de uma diretiva de região (seção 3.1); em qualquer outro uso é erro.

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

### 3.1 Diretivas de região

O Scanner reconhece três diretivas, cada uma com um token próprio. A palavra depois do `#` pertence ao conjunto `D = {tunel, toca, vaparatunel}`.

| Forma | Token | Lexema do token |
| --- | --- | --- |
| `#tunel <nome>` | `REGION_START` | o nome |
| `#toca` | `REGION_END` | vazio |
| `#vaparatunel <nome>` | `GOTO_REGION` | o nome |

Linha e coluna do token apontam para o `#`. `#` seguido de palavra fora de `D`, de espaço ou de símbolo gera erro no `#`, e a leitura continua logo depois. `#tunel` ou `#vaparatunel` sem nome também geram erro. A formalização (ERs, AFDs e simulações) está em [AUTOMATA.md](AUTOMATA.md#45-diretivas-de-região). Dois comportamentos do código dependem de decisão do grupo: D03 e D04.

## 4. Palavras reservadas — conjunto K

As 17 palavras abaixo são `KEYWORD` na proposta atual. As 13 primeiras vêm do PDF; as 4 últimas (`vasculhar`, `dentro`, `trilha`, `cavar`) foram acrescentadas a partir do `teste.ra` e dependem da decisão D02. A categoria de `cheio` e `vazio` ainda será confirmada (D01).

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
| `vasculhar` | `for` — D02 |
| `dentro` | `in` — D02 |
| `trilha` | `range` — D02 |
| `cavar` | `def` — D02 |

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
9. **Erros:** caracteres fora de `Σ`, como `@`, `!` isolado e diretivas desconhecidas ou sem nome geram erro. A leitura continua depois deles.

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

Todas aguardam resposta do grupo. Quando uma decisão for tomada, registrar nesta seção a data, a resposta, a justificativa, quem validou e as regras afetadas.

### D01 — cheio e vazio

- **Alternativas:** manter `KEYWORD` ou criar `BOOLEAN`.

### D02 — palavras acrescentadas pelo teste.ra

- **Proposta:** incluir `vasculhar` (`for`), `dentro` (`in`), `trilha` (`range`) e `cavar` (`def`) em K, como `KEYWORD`, com K passando de 13 para 17 palavras.
- **Alternativas:** manter só as 13 palavras (e então `for`, `in`, `range` e `def` não fazem parte da linguagem) ou escolher outros nomes.
- **Efeito:** nenhum AFD muda. O conjunto K e os testes de palavras reservadas passam a incluir as quatro palavras.

### D03 — token das diretivas e nome da região

- **Situação atual (código):** um token por diretiva, com o nome da região no lexema. O nome é lido por um AFD próprio (M_NOME) que aceita começar por dígito (`#tunel 1abc`), e `#tunel1` é aceito sem espaço.
- **Proposta B:** o token da diretiva leva o lexema `#tunel`, `#toca` ou `#vaparatunel`, e o nome vira um `IDENTIFIER` comum, lido pelo AFD da seção 3.1 do `AUTOMATA.md`. O nome passa a obedecer à regra de identificadores e exige separador depois da diretiva.
- **Efeito da proposta B:** o parser passa a consumir um IDENTIFIER depois da diretiva. M_NOME deixa de existir e o Scanner fica mais uniforme.

### D04 — resto da linha depois da diretiva

- **Situação atual (código):** o Scanner descarta tudo até o fim da linha. `#toca guinchar(1);` ignora o `guinchar`, e `#tunel a @@` não gera erro.
- **Proposta:** não descartar; o que sobra na linha é lido normalmente.
- **Alternativa:** manter o descarte e documentá-lo como comentário da diretiva.
- **Efeito:** remover a etapa 3 (resto da linha) do reconhecedor de diretivas.