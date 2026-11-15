#!/usr/bin/env python3
"""
Rathyon
Versão 0.0.2
Como usar: python rathyon.py <arquivo.ra>
"""
import sys
import os
import re
import json

#le o .json do colega pra trocar os termos reservados
def carregar_traducao():
    """Lê config/palavras_reservadas.json e devolve {rathyon: python}."""
    caminho = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "config", "palavras_reservadas.json"
    )
    with open(caminho, encoding="utf-8") as f:
        mapa = json.load(f)
    return {v: k for k, v in mapa.items()}

#tradução no dicionario
def traduzir(codigo, mapa):
    """Troca palavras Rathyon por palavras Python no texto."""
    for ra, py in mapa.items():
        codigo = re.sub(rf'\b{re.escape(ra)}\b', py, codigo)
    return codigo

def main():
    if len(sys.argv) != 2:
        print("Uso: python rathyon.py <arquivo.ra>")
        sys.exit(1)

    caminho = sys.argv[1]

    try:
        with open(caminho, encoding="utf-8") as f:
            codigo = f.read()
    except FileNotFoundError:
        print(f"Não achei o arquivo: {caminho}")
        sys.exit(1)
    except OSError as e:
        print(f"Erro ao abrir: {e}")
        sys.exit(1)

    #carrega e aplica a traducao dos termos reservados da rathyon
    try:
        mapa = carregar_traducao()
    except Exception as e:
        print(f"Erro ao carregar config/palavras_reservadas.json: {e}")
        sys.exit(1)

    codigo = traduzir(codigo, mapa)

    #roda .ra como se fosse py puro.
    # __name__ vira "__main__" dentro do arquivo, igual a `python arquivo.py`.
    try:
        exec(compile(codigo, caminho, "exec"), {"__name__": "__main__", "__file__": caminho})
    except SyntaxError as e:
        print(f"Erro de sintaxe em {caminho}: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Erro ao executar: {e}")
        sys.exit(2)


if __name__ == "__main__":
    main()