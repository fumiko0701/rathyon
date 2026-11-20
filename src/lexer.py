"""Compatibilidade: expõe o Scanner oficial em `src.lexer`.

A implementação única do Scanner fica em `lexer.py` na raiz e usa os AFDs
definidos em `automata.py`. Este módulo evita manter uma segunda implementação.
"""
try:
    from ..lexer import Scanner
except ImportError:
    from lexer import Scanner

__all__ = ["Scanner"]
