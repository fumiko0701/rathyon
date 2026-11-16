#!/usr/bin/env python3
"""
Rathyon — build.py
Gera o executável em um único comando:
    python config/build.py
"""
import os
import sys
import subprocess

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REQ = os.path.join(RAIZ, "requirements.txt")
MAIN = os.path.join(RAIZ, "rathyon.py")
ICONE = os.path.join(RAIZ, "assets", "rathyon.ico")
JSON = os.path.join(RAIZ, "config", "palavras_reservadas.json")


def criar_requirements():
    """Cria requirements.txt na raiz se ele ainda não existir."""
    if os.path.exists(REQ):
        return
    print("Criando requirements.txt ...")
    resultado = subprocess.run(
        [sys.executable, "-m", "pip", "freeze"],
        capture_output=True, text=True, check=True,
    )
    conteudo = resultado.stdout
    if "pyinstaller" not in conteudo.lower():
        conteudo += "pyinstaller\n"
    with open(REQ, "w", encoding="utf-8") as f:
        f.write(conteudo)


def instalar_dependencias():
    """Instala as dependências do requirements.txt se o PyInstaller faltar."""
    try:
        import PyInstaller  # noqa: F401
        return
    except ImportError:
        pass
    print("Instalando dependências ...")
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", REQ],
        check=True,
    )


def compilar():
    """Roda o PyInstaller com ícone e JSON embutidos."""
    print("Compilando rathyon.exe ...")
    sep = ";" if os.name == "nt" else ":"
    subprocess.run(
        [
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            f"--icon={ICONE}",
            "--add-data", f"{JSON}{sep}config",
            MAIN,
        ],
        check=True,
        cwd=RAIZ,
    )


def main():
    criar_requirements()
    instalar_dependencias()
    compilar()
    print("\nPronto! Executável em: dist/rathyon.exe")


if __name__ == "__main__":
    main()