#!/usr/bin/env python3
"""
Rathyon
Versão 0.2.0
Como usar: python rathyon.py <arquivo.ra> ou rathyon <arquivo.ra>
"""
import sys
import os
import re
import json
import code
import tokenize
from io import StringIO

from src.lexer import Scanner
from src.parser import parse as parse_ast
from src.executor import Executor


#função para o PyInstaller achar a pasta certa ---
def obter_diretorio_base():
    """Retorna a pasta do script original ou a pasta temporária do PyInstaller."""
    if getattr(sys, 'frozen', False):
        #se estiver rodando como .exe (PyInstaller)
        return sys._MEIPASS
    #se estiver rodando como .py normal
    return os.path.dirname(os.path.abspath(__file__))

#le o .json do colega pra trocar os termos reservados
def carregar_traducao():
    """Lê config/palavras_reservadas.json e devolve {rathyon: python}."""
    #MUDANÇA MÍNIMA: Usa a função auxiliar em vez do os.path.dirname direto
    caminho = os.path.join(
        obter_diretorio_base(), 
        "config", "palavras_reservadas.json"
    )
    with open(caminho, encoding="utf-8") as f:
        mapa = json.load(f)
    return {v: k for k, v in mapa.items()}

#tradução no dicionario
def traduzir(codigo, mapa):
    """Traduz os nomes do console e preserva o texto entre aspas."""
    linhas = codigo.split("\n")
    nomes = []
    try:
        for token in tokenize.generate_tokens(StringIO(codigo).readline):
            if token.type == tokenize.NAME and token.string in mapa:
                nomes.append(token)
    except (tokenize.TokenError, IndentationError):
        pass  # O console também recebe comandos incompletos.
    for token in reversed(nomes):
        linha, inicio = token.start
        texto = linhas[linha - 1]
        linhas[linha - 1] = texto[:inicio] + mapa[token.string] + texto[token.end[1]:]
    return "\n".join(linhas)

def _pausar():
    """Pausa para o usuário ler antes de fechar (double-click no .ra)."""
    if os.name == 'nt':
        try:
            import msvcrt
            print("Pressione qualquer tecla para encerrar...", end="", flush=True)
            msvcrt.getch()
            print()
            return
        except Exception:
            pass
    try:
        input("Pressione qualquer tecla para encerrar (Enter)")
    except EOFError:
        pass


def foi_duplo_clique():
    """True se o console pertence só a este processo (caso típico de 2 cliques)."""
    if os.name != 'nt':
        return False
    try:
        import ctypes
        buf = (ctypes.c_uint * 2)()
        n = ctypes.windll.kernel32.GetConsoleProcessList(buf, 2)
        return n <= 1
    except Exception:
        return False


def tem_finalizacao_explicita(codigo):
    """Detecta se o script já define como terminar."""
    padroes = [
        r'\bsys\.exit\b', r'\bexit\s*\(', r'\bquit\s*\(',
        r'\braise\s+SystemExit\b', r'\bSystemExit\b',
        r'\bsair\b', r'\bencerrar\b', r'\bterminar\b',
    ]
    return any(re.search(p, codigo) for p in padroes)


def pausar_se_necessario(codigo_original, ja_erro=False):
    if not foi_duplo_clique():
        return
    if not ja_erro and tem_finalizacao_explicita(codigo_original):
        return
    _pausar()

class RathyonConsole(code.InteractiveConsole):
    """REPL: traduz cada entrada antes de executar."""
    def __init__(self, mapa, locals=None):
        super().__init__(locals)
        self._mapa = mapa

    def runsource(self, source, filename="<input>", symbol="single"):
        try:
            source = traduzir(source, self._mapa)
        except Exception as e:
            print(f"Erro na tradução: {e}")
            return False
        return super().runsource(source, filename, symbol)


def iniciar_repl():
    """Abre a CLI quando o usuário digita apenas 'rathyon'."""
    try:
        mapa = carregar_traducao()
    except Exception as e:
        print(f"Erro ao carregar config/palavras_reservadas.json: {e}")
        sys.exit(1)

    print("Rathyon 0.2.0 - CLI interativa")
    print("Digite instruções Rathyon. Ctrl+Z para sair.\n")
    console = RathyonConsole(mapa)
    console.interact(banner="")


def main():
    if len(sys.argv) == 1:
        iniciar_repl()
        return
    if len(sys.argv) != 2:
        print("Uso: rathyon <arquivo.ra>")
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

    #codigo_original = codigo
    #codigo = traduzir(codigo, mapa)

    #roda .ra como se fosse py puro.
    try:
        ast = parse_ast(codigo)
    except Exception as e:
        print(f"Erro de sintaxe/lexico em {caminho}: {e}")
        pausar_se_necessario(codigo, ja_erro=True)
        sys.exit(1)

    try:
        Executor().rodar(ast)
    except Exception as e:
        print(f"Erro ao executar: {e}")
        pausar_se_necessario(codigo, ja_erro=True)
        sys.exit(2)

    pausar_se_necessario(codigo)


if __name__ == "__main__":
    main()
