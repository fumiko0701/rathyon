"""Benchmark de eficiência — Executor e Scanner da Rathyon.

Este script mede o tempo de execução atual do código-fonte
sem alterar nada no repositório. Serve apenas para comparar
desempenho antes e depois de futuras otimizações.
"""

import sys
sys.setrecursionlimit(100000)
import time
import os

# Adiciona a raiz do projeto ao path para importar os módulos src.
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.executor import Executor
from src.lexer import Scanner
from src.parser import parse


def gerar_codigo_grande(n_linhas: int = 1000) -> str:
    """Gera código-fonte .ra grande para testar o scanner."""
    linhas = []
    for i in range(n_linhas):
        linhas.append(f"queijo x{i} = {i} + {i} * 2;")
        linhas.append(f"farejar x{i} >= 0 {{ guinchar(x{i}); }}")
        linhas.append(f"vasculhar j dentro trilha(3) {{ roer cheio {{ escapar; }} }}")
    return "\n".join(linhas)


def gerar_ast_grande(n_ops: int = 300) -> dict:
    """Gera uma AST grande com muitas expressões binárias aninhadas."""
    expr = {"type": "Literal", "value": 1}
    for i in range(2, n_ops + 1):
        expr = {
            "type": "Binary",
            "left": expr,
            "operator": "+",
            "right": {"type": "Literal", "value": i},
        }

    statements = []
    for i in range(200):
        statements.append({
            "type": "Declaration",
            "name": f"var{i}",
            "data_type": "queijo",
            "value": expr,
        })
        statements.append({
            "type": "Assignment",
            "name": f"var{i}",
            "value": expr,
        })

    return {"type": "Program", "body": statements}


def medir_tempo(funcao, *args, repeticoes: int = 3):
    """Mede o tempo médio de execução em segundos."""
    tempos = []
    for _ in range(repeticoes):
        inicio = time.perf_counter()
        funcao(*args)
        fim = time.perf_counter()
        tempos.append(fim - inicio)
    media = sum(tempos) / len(tempos)
    return media, min(tempos), max(tempos)


def benchmark_executor():
    print("=" * 60)
    print("BENCHMARK — EXECUTOR")
    print("=" * 60)
    ast = gerar_ast_grande(n_ops=300)
    print(f"\nAST gerada: {len(ast['body'])} nós no corpo\n")

    print("--- Versão atual do código ---")
    media, minima, maxima = medir_tempo(Executor().rodar, ast)
    print(f"Médio: {media:.4f}s | Mín: {minima:.4f}s | Máx: {maxima:.4f}s")
    return media


def benchmark_scanner():
    print("=" * 60)
    print("BENCHMARK — SCANNER / LEXER")
    print("=" * 60)

    codigo = gerar_codigo_grande(n_linhas=500)
    print(f"\nCódigo-fonte: {len(codigo)} caracteres, {codigo.count(chr(10))+1} linhas\n")

    print("--- Versão atual do código ---")
    media, minima, maxima = medir_tempo(Scanner(codigo).scan)
    print(f"Médio: {media:.4f}s | Mín: {minima:.4f}s | Máx: {maxima:.4f}s")
    return media


if __name__ == "__main__":
    print("Benchmark de eficiência — Rathyon (código atual, sem alterações)\n")
    benchmark_executor()
    print()
    benchmark_scanner()
