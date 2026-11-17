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


CONTEUDO_REQ = "pyinstaller>=6.0\n"


def garantir_requirements():
    """Garante um requirements.txt mínimo (o projeto só usa stdlib + PyInstaller)."""
    if os.path.exists(REQ):
        return
    print("Criando requirements.txt ...")
    with open(REQ, "w", encoding="utf-8") as f:
        f.write(CONTEUDO_REQ)


def instalar_dependencias():
    """Instala/atualiza dependências do requirements.txt (pip pula o que já existe)."""
    print("Verificando dependências ...")
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", REQ],
        check=True,
    )


def validar_entradas():
    """Confere que todos os arquivos necessários existem antes de compilar."""
    for caminho in (MAIN, ICONE, JSON):
        if not os.path.isfile(caminho):
            sys.exit(f"Erro: arquivo não encontrado: {caminho}")


def compilar():
    """Roda o PyInstaller com ícone e JSON embutidos."""
    validar_entradas()
    print("Compilando rathyon.exe ...")
    sep = ";" if os.name == "nt" else ":"
    subprocess.run(
        [
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--noconfirm",
            "--clean",
            f"--icon={ICONE}",
            "--add-data", f"{JSON}{sep}config",
            MAIN,
        ],
        check=True,
        cwd=RAIZ,
    )


def main():
    try:
        garantir_requirements()
        instalar_dependencias()
        compilar()
    except subprocess.CalledProcessError as e:
        cmd = " ".join(map(str, e.cmd))
        sys.exit(f"\nFalha no passo: {cmd}\nCódigo de saída: {e.returncode}")
    print("\nPronto! Executável em: dist/rathyon.exe")


if __name__ == "__main__":
    main()