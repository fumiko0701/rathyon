"""Compatibilidade: os tokens oficiais ficam definidos em tokens.py na raiz.

Este módulo mantém os imports antigos `src.tokens` sem duplicar Enum/dataclasses.
"""
try:
    from ..tokens import Categoria, Token, ErroLexico
except ImportError:
    from tokens import Categoria, Token, ErroLexico

__all__ = ["Categoria", "Token", "ErroLexico"]
