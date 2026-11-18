# src/tokens.py
from enum import Enum, auto
from dataclasses import dataclass

class Categoria(Enum):
    KEYWORD = auto()
    IDENTIFIER = auto()
    INTEGER = auto()
    FLOAT = auto()
    ARITHMETIC_OPERATOR = auto()
    RELATIONAL_OPERATOR = auto()
    ASSIGNMENT = auto()
    DELIMITER = auto()

@dataclass
class Token:
    categoria: Categoria
    lexema: str
    linha: int
    coluna: int

@dataclass
class ErroLexico:
    lexema: str
    linha: int
    coluna: int
    mensagem: str