"""src/tokens.py — Estrutura de um token do Scanner (tarefa 62).

Define a estrutura de um token da Linguagem do Rato e as categorias léxicas
previstas em SPECIFICATIONS.md §3.

Convenções de posição (usadas por todo o Scanner):
- linha e coluna são 1-based;
- apontam para o PRIMEIRO caractere do lexema;
- separadores não geram tokens, mas avançam a posição do cursor.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Categoria(str, Enum):
    """Categorias de token (SPECIFICATIONS.md §3).

    Herança de `str` permite comparar direto com strings, p. ex.
    `token.categoria == "KEYWORD"`.
    """

    KEYWORD = "KEYWORD"
    IDENTIFIER = "IDENTIFIER"
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    STRING = "STRING"
    ARITHMETIC_OPERATOR = "ARITHMETIC_OPERATOR"
    RELATIONAL_OPERATOR = "RELATIONAL_OPERATOR"
    ASSIGNMENT = "ASSIGNMENT"
    DELIMITER = "DELIMITER"
    REGION_START = "REGION_START"
    REGION_END = "REGION_END"
    GOTO_REGION = "GOTO_REGION"
    ERRO = "ERRO"
    EOF = "EOF"


@dataclass(frozen=True)
class Token:
    """Token reconhecido pelo Scanner.

    frozen garante imutabilidade depois de criado, evitando que etapas
    posteriores (parser, tradutor) alterem acidentalmente um token já emitido.
    """

    categoria: Categoria
    lexema: str
    linha: int
    coluna: int

    def __repr__(self) -> str:
        return f"Token({self.categoria.value}, {self.lexema!r}, L{self.linha}:C{self.coluna})"


@dataclass(frozen=True)
class ErroLexico:
    """Erro léxico com posição e mensagem.

    Um erro não interrompe a varredura: o Scanner continua após o caractere
    inválido (SPECIFICATIONS.md §5, regra 9). É responsabilidade do chamador
    (parser, T09/T10) decidir como lidar com a lista de erros.
    """

    lexema: str
    linha: int
    coluna: int
    mensagem: str

    def __repr__(self) -> str:
        return f"ErroLexico({self.lexema!r}, L{self.linha}:C{self.coluna}): {self.mensagem}"
