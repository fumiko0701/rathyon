#!/usr/bin/env python3
"""Lê todos os arquivos da extensão vscode-rathyon e valida estrutura."""
import json
from pathlib import Path

# localizar a pasta independente de onde o script é chamado
root = Path("vscode-rathyon")
if not root.exists():
    root = Path(__file__).resolve().parent / "vscode-rathyon"
if not root.exists():
    print("Pasta 'vscode-rathyon' não encontrada.")
    raise SystemExit(1)

# ---- 1. Conteúdo ----
print("=" * 70)
print("CONTEÚDO DOS ARQUIVOS")
print("=" * 70)
for f in sorted(root.rglob("*")):
    if f.is_file():
        print(f"\n----- {f.relative_to(root)} -----")
        try:
            print(f.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"[erro ao ler: {e}]")

# ---- 2. Validação ----
print("\n" + "=" * 70)
print("VALIDAÇÃO DE EXTENSÃO VS CODE")
print("=" * 70)

pkg_path = root / "package.json"
if not pkg_path.exists():
    print("✗ package.json NÃO ENCONTRADO")
    raise SystemExit(1)

try:
    pkg = json.loads(pkg_path.read_text(encoding="utf-8"))
    print("✓ package.json é JSON válido")
except json.JSONDecodeError as e:
    print(f"✗ package.json inválido: {e}")
    raise SystemExit(1)

# campos mínimos que o VS Code exige
for campo in ("name", "publisher", "version", "engines"):
    if campo in pkg:
        print(f"✓ campo '{campo}' presente")
    else:
        print(f"✗ campo '{campo}' AUSENTE (obrigatório)")

# engines.vscode compatível
eng = pkg.get("engines", {}).get("vscode")
if eng:
    print(f"  engines.vscode = {eng}")

# contributes
contributes = pkg.get("contributes", {})
if not contributes:
    print("✗ 'contributes' vazio — extensão não declara nada")

for g in contributes.get("grammars", []):
    p = root / g["path"].replace("./", "", 1)
    print(f"{'✓' if p.exists() else '✗'} gramática: {g['path']}")

for l in contributes.get("languages", []):
    ext_list = l.get("extensions", [])
    print(f"✓ linguagem '{l.get('id')}' extensões {ext_list}")
    cfg = l.get("configuration")
    if cfg:
        p = root / cfg.replace("./", "", 1)
        print(f"  {'✓' if p.exists() else '✗'} config: {cfg}")

# pasta fora do padrão publisher.name-version
print(f"\nPasta física: {root.resolve()}")
print(f"Nome da pasta: {root.name}")
if root.name.count(".") < 2:
    print("⚠ VS Code (instalação manual) espera 'publisher.nome-versao' "
          "(ex: marcos.rathyon-0.0.1)")

# checagem rápida do tmLanguage (se existir)
for g in contributes.get("grammars", []):
    tm = root / g["path"].replace("./", "", 1)
    if tm.exists():
        try:
            data = json.loads(tm.read_text(encoding="utf-8"))
            if "scopeName" in data and "patterns" in data:
                print(f"✓ {tm.name}: JSON válido com scopeName + patterns")
            else:
                print(f"✗ {tm.name}: faltando 'scopeName' ou 'patterns'")
        except json.JSONDecodeError as e:
            print(f"✗ {tm.name}: JSON inválido ({e})")