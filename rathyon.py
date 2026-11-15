#!/usr/bin/env python3
"""
Rathyon
Versão 0.0.1
Como usar: python rathyon.py <arquivo.ra>
"""
import sys


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