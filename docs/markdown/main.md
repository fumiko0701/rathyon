# Analisador Léxico (Scanner) — Linguagem do Rato

**Centro Universitário Maurício de Nassau**
**Curso de Ciência da Computação**
**Maceió — AL, 2026**

## Integrantes

- Alessandra Júlia Santos Mendonça — 01710330
- Jhonas Xavier dos Santos Silva — 01694333
- Marcos Emanuel Celestino Tavares — 01718690
- Guilherme de Oliveira Lopes Silva — 01699872
- Alan Sergio Rodrigues de Carvalho — 01697157
- Alfred Manoel Vincente Silva da Rocha — 01695802
- Pedro Artur Rolemberg Ferreira Nogueira — 01705061

## Sumário

1. [Introdução](#1-introdução)
2. [Objetivos](#2-objetivos)
3. [Fundamentação teórica](#3-fundamentação-teórica)
4. [Metodologia](#4-metodologia)
5. [Desenvolvimento do Scanner](#5-desenvolvimento-do-scanner)
6. [Diagramas dos autômatos](#6-diagramas-dos-autômatos)
7. [Testes e resultados](#7-testes-e-resultados)
8. [Conclusão](#8-conclusão)
9. [Referências](#9-referências)

## 1. Introdução

O desenvolvimento de uma mini-linguagem de programação envolve a definição de uma estrutura própria para representar comandos e de regras para escrever e interpretar as instruções. Este projeto propõe uma mini-linguagem fundamentada no paradigma de programação orientada a eventos, cuja sintaxe e semântica são inspiradas em comportamentos e ações associados aos ratos.

A proposta usa elementos temáticos relacionados a esses animais como referência para organizar eventos e ações, dando identidade própria à linguagem e uma abordagem diferenciada para aplicar conceitos de linguagens formais.

O relatório apresenta os conceitos e as regras do analisador léxico (Scanner), responsável por percorrer o código-fonte e classificar seus elementos em categorias chamadas tokens. A especificação formal ainda registra decisões pendentes de validação pelo grupo.

Na execução de arquivos `.ra`, o programa usa Scanner, Parser e Executor. O console interativo segue um caminho separado e traduz algumas palavras para Python. O relatório aborda linguagens formais, expressões regulares e autômatos usados no Scanner.

## 2. Objetivos

Desenvolver e documentar a especificação de um analisador léxico (Scanner) para uma linguagem de programação temática, usando conceitos de linguagens formais, expressões regulares e autômatos finitos determinísticos, com a finalidade de reconhecer e classificar os elementos léxicos presentes no código-fonte.

### 2.1 Objetivo geral

- Definir o alfabeto e as categorias de tokens da linguagem.
- Estabelecer expressões regulares para representar padrões léxicos.
- Modelar autômatos finitos determinísticos para reconhecer identificadores, números e operadores.
- Descrever a identificação e a classificação dos lexemas.
- Aplicar a estratégia de maior casamento (*maximal munch*) durante o reconhecimento dos tokens.
- Especificar mecanismos para identificar e tratar erros léxicos.
- Documentar as simulações da proposta de Scanner.

### 2.2 Objetivos específicos

- Definir as categorias de tokens da linguagem.
- Representar seus padrões com expressões regulares e autômatos.
- Descrever o tratamento de erros léxicos.

## 3. Fundamentação teórica

### 3.1 Compiladores e análise léxica

Um compilador traduz um código escrito em uma linguagem de programação para outra representação, geralmente linguagem de máquina ou uma forma intermediária. Esse processo é dividido em etapas que analisam diferentes aspectos do código-fonte.

A análise léxica é uma das primeiras etapas. Ela percorre o código-fonte, identifica sequências de caracteres que formam unidades significativas e as classifica em categorias chamadas tokens. O componente que realiza essa atividade é chamado analisador léxico ou Scanner. Além de reconhecer elementos válidos, ele pode identificar caracteres inválidos e informar erros léxicos.

### 3.2 Tokens e lexemas

Token é a classificação atribuída a uma unidade reconhecida durante a análise léxica. Lexema é a sequência de caracteres do código-fonte que representa esse token. Na proposta, a instrução abaixo seria dividida nos lexemas `roer`, `queijo`, `=`, `18` e `;`, cada um associado à sua categoria léxica.

```text
roer queijo = 18;
```

### 3.3 Expressões regulares

Expressões regulares descrevem padrões de cadeias de caracteres e permitem definir sequências pertencentes a determinadas linguagens regulares. No Scanner, são usadas para especificar padrões de reconhecimento de tokens, como identificadores, números inteiros, números decimais e operadores.

### 3.4 Autômatos finitos

Autômatos finitos são modelos matemáticos usados para reconhecer linguagens regulares. Um autômato finito determinístico é definido por um conjunto de estados, um alfabeto, uma função de transição, um estado inicial e um conjunto de estados finais.

## 4. Metodologia

Foram reunidas as palavras e os símbolos previstos para a linguagem. Depois, foram definidos padrões para os tokens e implementados reconhecedores por meio de autômatos. Os testes do projeto verificam o Scanner, o Parser e casos de integração.

## 5. Desenvolvimento do Scanner

### 5.1 Especificação da linguagem e categorias de tokens

A proposta considera palavras reservadas, identificadores, números inteiros e decimais, strings entre aspas duplas, operadores e delimitadores. Colchetes são delimitadores usados em listas. A lista completa e as decisões ainda pendentes estão em [SPECIFICATIONS.md](SPECIFICATIONS.md).

### 5.2 Modelagem matemática e expressões regulares

Os padrões e as tabelas dos autômatos estão descritos em [REGULAR_EXPRESSIONS.md](REGULAR_EXPRESSIONS.md) e [AUTOMATA.md](AUTOMATA.md). Por exemplo, um identificador segue o padrão `(L|_)(L|D|_)*`, em que `L` representa uma letra e `D`, um dígito.

### 5.3 Implementação e funcionamento do Scanner

O Scanner implementado em `src/lexer.py` reconhece tokens e registra suas posições no código. Strings são reconhecidas por uma regra própria, com aspas duplas e escapes definidos na especificação. Ele também reconhece as diretivas `#tunel`, `#toca` e `#vaparatunel` por uma regra específica. O Parser, em `src/parser.py`, usa esses tokens para montar a árvore do programa. O Executor, em `src/executor.py`, percorre essa árvore e executa as instruções.

### 5.4 Tratamento de erros léxicos

Quando encontra caracteres fora do alfabeto definido, o Scanner registra erros com linha e coluna e continua a leitura. Ao analisar um arquivo, o Parser interrompe a execução se houver erro léxico ou sintático.

## 6. Diagramas dos autômatos

### 6.1 AFD de identificadores

O modelo e as simulações estão em [AUTOMATA.md](AUTOMATA.md).

### 6.2 AFD de números

O modelo e as simulações estão em [AUTOMATA.md](AUTOMATA.md).

### 6.3 AFD de operadores relacionais e atribuição

Os modelos e as simulações estão em [AUTOMATA.md](AUTOMATA.md).

### 6.4 AFDs de operadores aritméticos e delimitadores

Os modelos e as simulações estão em [AUTOMATA.md](AUTOMATA.md).

## 7. Testes e resultados

O projeto contém testes automatizados para o Scanner e o Parser, além de testes de integração. Eles verificam o reconhecimento de tokens, a formação da árvore e a execução do programa.

## 8. Conclusão

O trabalho apresenta as regras léxicas e os autômatos do Rathyon. No programa atual, o Scanner, o Parser e o Executor formam o caminho usado para executar arquivos `.ra`. A especificação léxica continua em rascunho enquanto algumas decisões aguardam validação do grupo.

## 9. Referências

- Projeto Rathyon. Código-fonte: `src/lexer.py`, `src/parser.py`, `src/executor.py` e `src/automata.py`.
- Projeto Rathyon. Testes automatizados: `tests/`.
- Projeto Rathyon. [Especificação léxica](SPECIFICATIONS.md).
- Projeto Rathyon. [Autômatos](AUTOMATA.md).
- Projeto Rathyon. [Expressões regulares](REGULAR_EXPRESSIONS.md).
- Projeto Rathyon. [Gramática](grammar.md).
