#!/usr/bin/env python3
"""
Rathyon
Versão 0.0.4 (Suporte a PyInstaller)
Como usar: python rathyon.py <arquivo.ra> ou rathyon <arquivo.ra> (após compilar)
"""
import sys
import os
import re
import json

# --- NOVO: Função para o PyInstaller achar a pasta certa ---
def obter_diretorio_base():
    """Retorna a pasta do script original ou a pasta temporária do PyInstaller."""
    if getattr(sys, 'frozen', False):
        # Se estiver rodando como .exe (PyInstaller)
        return sys._MEIPASS
    # Se estiver rodando como .py normal
    return os.path.dirname(os.path.abspath(__file__))

#le o .json do colega pra trocar os termos reservados
def carregar_traducao():
    """Lê config/palavras_reservadas.json e devolve {rathyon: python}."""
    # --- MUDANÇA MÍNIMA: Usa a função auxiliar em vez do os.path.dirname direto ---
    caminho = os.path.join(
        obter_diretorio_base(), 
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
        print("Uso: rathyon <arquivo.ra> (ou: python rathyon.py <arquivo.ra>)")
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