"""Benchmark de eficiência — Executor e Scanner da Rathyon.

Mede o tempo de execução em vários tamanhos de entrada e, quando a
biblioteca externa ``matplotlib`` estiver disponível, gera gráficos
(PNG) para visualizar a eficiência do Scanner e do Executor.

Serve para comparar desempenho antes e depois de futuras otimizações
sem alterar nada no repositório.
"""

from __future__ import annotations

import sys
sys.setrecursionlimit(100000)
import time
import os
import json
from datetime import datetime

# Adiciona a raiz do projeto ao path para importar os módulos src.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.executor import Executor
from src.lexer import Scanner
from src.parser import parse


RAIZ_PROJETO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASTA_RESULTADOS = os.path.join(RAIZ_PROJETO, "bench", "resultados")


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


def _cabecalho(titulo: str) -> str:
    return "\n" + "=" * 60 + "\n" + titulo + "\n" + "=" * 60


def medir_tempo(funcao, *args, repeticoes: int = 3):
    """Mede o tempo de execução em segundos.

    Retorna (media, minima, maxima, lista_de_tempos).
    """
    tempos = []
    for _ in range(repeticoes):
        inicio = time.perf_counter()
        funcao(*args)
        fim = time.perf_counter()
        tempos.append(fim - inicio)
    media = sum(tempos) / len(tempos)
    return media, min(tempos), max(tempos), tempos


def benchmark_executor_multi(tamanhos=(100, 300, 600, 1000), repeticoes: int = 3):
    """Mede o Executor em vários tamanhos de AST e devolve a lista de resultados."""
    print(_cabecalho("BENCHMARK — EXECUTOR (vários tamanhos)"))
    resultados = []
    for n_ops in tamanhos:
        ast = gerar_ast_grande(n_ops=n_ops)
        n_nos = len(ast["body"])
        media, minima, maxima, _ = medir_tempo(
            Executor().rodar, ast, repeticoes=repeticoes
        )
        resultados.append({
            "tamanho": n_ops,
            "nos": n_nos,
            "medio": media,
            "min": minima,
            "max": maxima,
        })
        print(
            f"n_ops={n_ops:5d} | nós={n_nos:5d} | "
            f"médio={media:.4f}s | mín={minima:.4f}s | máx={maxima:.4f}s"
        )
    return resultados


def benchmark_scanner_multi(tamanhos=(200, 500, 1000, 1500, 2000), repeticoes: int = 3):
    """Mede o Scanner em vários tamanhos de código-fonte e devolve resultados."""
    print(_cabecalho("BENCHMARK — SCANNER / LEXER (vários tamanhos)"))
    resultados = []
    for n_linhas in tamanhos:
        codigo = gerar_codigo_grande(n_linhas=n_linhas)
        n_chars = len(codigo)
        n_lines = codigo.count("\n") + 1
        media, minima, maxima, _ = medir_tempo(
            Scanner(codigo).scan, repeticoes=repeticoes
        )
        resultados.append({
            "tamanho": n_linhas,
            "chars": n_chars,
            "linhas": n_lines,
            "medio": media,
            "min": minima,
            "max": maxima,
        })
        print(
            f"linhas={n_linhas:5d} | chars={n_chars:7d} | "
            f"médio={media:.4f}s | mín={minima:.4f}s | máx={maxima:.4f}s"
        )
    return resultados


def gerar_graficos(resultados_executor, resultados_scanner, pasta_saida=PASTA_RESULTADOS):
    """Gera gráficos de linha (tempo × tamanho) e devolve os caminhos dos arquivos.

    Retorna None se o matplotlib não estiver instalado.
    """
    try:
        import matplotlib
        matplotlib.use("Agg")  # backend sem exibição (serve em servidor/sem tela)
        import matplotlib.pyplot as plt
    except ImportError:
        print(
            "\n[AVISO] matplotlib não instalado. Gráficos não serão gerados.\n"
            "        Instale com:  pip install matplotlib\n"
        )
        return None

    os.makedirs(pasta_saida, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    caminhos = {}

    # --- Gráfico 1: Executor (tempo médio vs n_ops) ---
    xs_exec = [r["tamanho"] for r in resultados_executor]
    ys_exec = [r["medio"] for r in resultados_executor]
    ys_exec_min = [r["min"] for r in resultados_executor]
    ys_exec_max = [r["max"] for r in resultados_executor]

    plt.figure(figsize=(8, 5))
    plt.plot(xs_exec, ys_exec, marker="o", label="Médio", color="#1f77b4")
    plt.fill_between(xs_exec, ys_exec_min, ys_exec_max, color="#1f77b4", alpha=0.2, label="Mín–Máx")
    plt.xlabel("Tamanho da AST (n_ops — expressões binárias aninhadas)")
    plt.ylabel("Tempo de execução (s)")
    plt.title("Executor — Eficiência vs Tamanho da Entrada")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    caminho_exec = os.path.join(pasta_saida, f"executor_tempo_vs_tamanho_{timestamp}.png")
    plt.savefig(caminho_exec, dpi=150)
    plt.close()
    caminhos["executor"] = caminho_exec

    # --- Gráfico 2: Scanner (tempo médio vs n_linhas) ---
    xs_scan = [r["tamanho"] for r in resultados_scanner]
    ys_scan = [r["medio"] for r in resultados_scanner]
    ys_scan_min = [r["min"] for r in resultados_scanner]
    ys_scan_max = [r["max"] for r in resultados_scanner]

    plt.figure(figsize=(8, 5))
    plt.plot(xs_scan, ys_scan, marker="o", label="Médio", color="#2ca02c")
    plt.fill_between(xs_scan, ys_scan_min, ys_scan_max, color="#2ca02c", alpha=0.2, label="Mín–Máx")
    plt.xlabel("Tamanho do código-fonte (número de linhas .ra)")
    plt.ylabel("Tempo de execução (s)")
    plt.title("Scanner / Lexer — Eficiência vs Tamanho da Entrada")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    caminho_scan = os.path.join(pasta_saida, f"scanner_tempo_vs_tamanho_{timestamp}.png")
    plt.savefig(caminho_scan, dpi=150)
    plt.close()
    caminhos["scanner"] = caminho_scan

    return caminhos


def salvar_resultados_json(resultados_executor, resultados_scanner, pasta_saida=PASTA_RESULTADOS):
    """Salva os resultados brutos em JSON para reprodução posterior."""
    os.makedirs(pasta_saida, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    caminho = os.path.join(pasta_saida, f"resultados_{timestamp}.json")
    dados = {
        "gerado_em": datetime.now().isoformat(),
        "executor": resultados_executor,
        "scanner": resultados_scanner,
    }
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
    return caminho


def imprimir_resumo(resultados_executor, resultados_scanner):
    print("\n" + "=" * 60)
    print("RESUMO DOS RESULTADOS")
    print("=" * 60)
    print("\n-- Executor --")
    print(f"{'n_ops':>7} | {'nós':>6} | {'médio (s)':>10} | {'mín (s)':>9} | {'máx (s)':>9}")
    for r in resultados_executor:
        print(f"{r['tamanho']:>7} | {r['nos']:>6} | {r['medio']:>10.4f} | {r['min']:>9.4f} | {r['max']:>9.4f}")
    print("\n-- Scanner / Lexer --")
    print(f"{'linhas':>7} | {'chars':>8} | {'médio (s)':>10} | {'mín (s)':>9} | {'máx (s)':>9}")
    for r in resultados_scanner:
        print(f"{r['tamanho']:>7} | {r['chars']:>8} | {r['medio']:>10.4f} | {r['min']:>9.4f} | {r['max']:>9.4f}")


if __name__ == "__main__":
    print("Benchmark de eficiência — Rathyon (código atual, sem alterações)")
    print(f"Projeto: {RAIZ_PROJETO}\n")

    res_exec = benchmark_executor_multi()
    print()
    res_scan = benchmark_scanner_multi()

    imprimir_resumo(res_exec, res_scan)

    caminho_json = salvar_resultados_json(res_exec, res_scan)
    print(f"\nResultados brutos salvos em: {caminho_json}")

    caminhos_graficos = gerar_graficos(res_exec, res_scan)
    if caminhos_graficos:
        print("\nGráficos gerados (visualização da eficiência):")
        for chave, caminho in caminhos_graficos.items():
            print(f"  - {chave}: {caminho}")
    print("\nBenchmark concluído.")
