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

O projeto concentra-se no desenvolvimento de um analisador léxico (Scanner), responsável por percorrer o código-fonte, identificar seus elementos e classificá-los em categorias chamadas tokens. O processo reconhece palavras reservadas, identificadores, operadores e outros componentes léxicos conforme as regras definidas para a linguagem.

O trabalho aplica conhecimentos de linguagens formais, expressões regulares e autômatos finitos na construção de um analisador léxico, demonstrando como fundamentos teóricos da computação podem ser usados na definição e no reconhecimento dos elementos de uma linguagem própria.

## 2. Objetivos

Desenvolver e documentar a especificação de um analisador léxico (Scanner) para uma linguagem de programação temática, usando conceitos de linguagens formais, expressões regulares e autômatos finitos determinísticos, com a finalidade de reconhecer e classificar os elementos léxicos presentes no código-fonte.

### 2.1 Objetivo geral

- Definir o alfabeto e as categorias de tokens da linguagem.
- Estabelecer expressões regulares para representar padrões léxicos.
- Modelar autômatos finitos determinísticos para reconhecer identificadores, números e operadores.
- Descrever a identificação e a classificação dos lexemas.
- Aplicar a estratégia de maior casamento (*maximal munch*) durante o reconhecimento dos tokens.
- Especificar mecanismos para identificar e tratar erros léxicos.
- Documentar e analisar os testes realizados pelo Scanner.

### 2.2 Objetivos específicos

Seção reservada para detalhar os objetivos específicos.

## 3. Fundamentação teórica

### 3.1 Compiladores e análise léxica

Um compilador traduz um código escrito em uma linguagem de programação para outra representação, geralmente linguagem de máquina ou uma forma intermediária. Esse processo é dividido em etapas que analisam diferentes aspectos do código-fonte.

A análise léxica é uma das primeiras etapas. Ela percorre o código-fonte, identifica sequências de caracteres que formam unidades significativas e as classifica em categorias chamadas tokens. O componente que realiza essa atividade é chamado analisador léxico ou Scanner. Além de reconhecer elementos válidos, ele pode identificar caracteres inválidos e informar erros léxicos.

### 3.2 Tokens e lexemas

Token é a classificação atribuída a uma unidade reconhecida durante a análise léxica. Lexema é a sequência de caracteres do código-fonte que representa esse token. Por exemplo, na instrução abaixo, o Scanner deve reconhecer `roer`, `queijo`, `=`, `18` e `;` e associá-los às respectivas categorias léxicas.

```text
roer queijo = 18;
```

### 3.3 Expressões regulares

Expressões regulares descrevem padrões de cadeias de caracteres e permitem definir sequências pertencentes a determinadas linguagens regulares. No Scanner, são usadas para especificar padrões de reconhecimento de tokens, como identificadores, números inteiros, números decimais e operadores.

### 3.4 Autômatos finitos

Autômatos finitos são modelos matemáticos usados para reconhecer linguagens regulares. Um autômato finito determinístico é definido por um conjunto de estados, um alfabeto, uma função de transição, um estado inicial e um conjunto de estados finais.

## 4. Metodologia

Seção reservada para descrever a metodologia do trabalho.

## 5. Desenvolvimento do Scanner

### 5.1 Especificação da linguagem e categorias de tokens

Seção reservada para apresentar a especificação da linguagem e as categorias de tokens.

### 5.2 Modelagem matemática e expressões regulares

Seção reservada para apresentar a modelagem matemática e as expressões regulares.

### 5.3 Implementação e funcionamento do Scanner

O Scanner percorre o código-fonte sequencialmente, analisando os caracteres e identificando padrões correspondentes às categorias de tokens definidas para a linguagem. O projeto descreve o uso das transições dos autômatos para determinar se uma sequência corresponde a um elemento válido.

Para reconhecer lexemas, é adotada a estratégia de maior casamento (*maximal munch*): selecionar a maior sequência possível de caracteres que corresponda a um padrão válido, considerando o último estado de aceitação alcançado.

Espaços em branco, tabulações e quebras de linha são tratados como separadores e não são retornados como tokens. Depois do reconhecimento, cada lexema é associado à sua categoria léxica, formando uma sequência organizada de tokens para as próximas etapas do processamento.

### 5.4 Tratamento de erros léxicos

O analisador léxico deve identificar caracteres e sequências que não correspondam aos padrões válidos da linguagem. Quando encontra uma entrada inválida, deve registrar o erro e informar sua localização por linha e coluna. As situações previstas no material incluem:

- Caracteres que não pertencem ao alfabeto definido.
- O símbolo `!` isolado, sem formar o operador `!=`.
- Números decimais incompletos, como `5.`.
- Letras ou sublinhados imediatamente após uma sequência numérica, como em `123abc`.
- Mais de um ponto em uma sequência numérica, como em `9.8.7`.

Após identificar um erro, o Scanner deve continuar a análise do restante do código-fonte para que uma ocorrência inválida não interrompa completamente o processamento.

## 6. Diagramas dos autômatos

### 6.1 AFD de identificadores

Seção reservada ao diagrama do AFD de identificadores.

### 6.2 AFD de números

Seção reservada ao diagrama do AFD de números.

### 6.3 AFD de operadores relacionais e atribuição

Seção reservada aos diagramas dos AFDs de operadores relacionais e de atribuição.

### 6.4 AFDs de operadores aritméticos e delimitadores

Seção reservada aos diagramas dos AFDs de operadores aritméticos e delimitadores.

## 7. Testes e resultados

Seção reservada para documentar os testes e seus resultados.

## 8. Conclusão

Seção reservada para a conclusão do trabalho.

## 9. Referências

Seção reservada às referências utilizadas no trabalho.
