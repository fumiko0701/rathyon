<p align="center">
  <img src="assets/rathyon_brand.svg" alt="Rathyon" width="240"/>
</p>

<h3 align="center">
  Linguagem de programação interpretada, simples e básica,<br/>
  com sintaxe em português e palavras-chave inspiradas nos<br/>
  movimentos e hábitos de um rato:
  <strong>roer</strong>, <strong>farejar</strong>, <strong>fujir</strong>,
  <strong>guinchar</strong>, <strong>escapar</strong>.
</h3>

<br/>

- **Extensão:** `.ra`
- **Versão da linguagem:** 0.2.0
- **Implementação:** Python (interpretador em arquivo único)
- **Plataforma do instalador:** Windows

---
## Referência da linguagem

### Palavras-chave

| Rathyon     | Equivalente | Função                  |
| ----------- | ----------- | ----------------------- |
| `queijo`    | `int`       | Declara inteiro         |
| `migalha`   | `float`     | Declara decimal         |
| `farejar`   | `if`        | Condicional             |
| `refarejar` | `elif`      | Condicional alternativa |
| `fujir`     | `else`      | Caso contrário          |
| `roer`      | `while`     | Laço de repetição       |
| `escapar`   | `break`     | Sai do laço             |
| `guinchar`  | `print`     | Imprime na saída        |
| `cheio`     | `true`      | Booleano verdadeiro     |
| `vazio`     | `false`     | Booleano falso          |
| `vasculhar` | `for`       | Laço sobre sequência    |
| `dentro`    | `in`        | Usado com o `for`       |
| `trilha`    | `range`     | Sequência de números    |
| `cavar`     | `def`       | Define uma função       |

### Operadores

- **Aritméticos:** `+  -  *  /`
- **Comparação:** `==  !=  <  >  <=  >=`
- **Atribuição:** `=`
- **Comentário:** `// texto`
- **Texto:** `"entre aspas"`

### Regiões

As regiões organizam blocos do programa e permitem saltar para uma região pelo nome:

- `#tunel nome` — inicia uma região.
- `#toca` — encerra a região atual.
- `#vaparatunel nome` — salta para a região indicada.
---
### Regras e limitações

- Todo comando termina com `;`.
- Variáveis devem ser declaradas (`queijo` / `migalha`) antes do uso.
- Atribuir decimal não inteiro a `queijo` gera erro de tipo.
- Não há funções, entrada de dados (`input`) ou laço `for` nesta versão.

---

## Instalação e setup

### Requisitos

- Windows 10 ou superior
- Para usar o instalador, não é necessário instalar Python.

### Opção 1 — Instalador gráfico (recomendado)

1. Abra a [versão mais recente](https://github.com/fumiko0701/rathyon/releases/latest) e baixe `rathyonsetup.exe` em **Assets**.
2. Execute o arquivo e siga o assistente. Ele configura o PATH e associa arquivos `.ra` ao Rathyon.
3. No Bloco de Notas, escreva `guinchar("Ola, mundo!")` e salve como `meu_programa.ra` (tipo **Todos os arquivos**).
4. Abra a pasta do arquivo no Explorador de Arquivos, digite `powershell` na barra de endereço e pressione Enter. Execute:

```powershell
rathyon meu_programa.ra
```

O terminal deve mostrar `Ola, mundo!`.

### Opção 2 — Executar a partir do código-fonte

Com Python 3.10 ou superior instalado, execute na raiz do projeto:

```bash
python rathyon.py teste.ra
```

### Opção 3 — Build via `config/build.py` (Desenvolvedores)

Para gerar o executável, abra o PowerShell na raiz do projeto e execute:

```powershell
python -m pip install -r requirements.txt
python config/build.py
```

No Windows, o executável será criado em `dist/rathyon.exe`. Para executá-lo da raiz do projeto, use `.\dist\rathyon.exe teste.ra`.

#### Configurando o PATH (apenas Windows)

Para poder rodar `rathyon arquivo.ra` de qualquer pasta no seu terminal (sem precisar digitar o caminho completo do `.exe`):

1. Copie o caminho completo da pasta `dist` (ex: `C:\Users\SeuUsuario\Documents\rathyon\dist`).
2. Pesquise no menu Iniciar por **"Editar as variáveis de ambiente do sistema"**.
3. Clique em **Variáveis de Ambiente** → encontre a variável **Path** e clique em **Editar**.
4. Clique em **Novo**, cole o caminho copiado e dê **OK** em tudo.

> **Importante:** feche e abra um novo terminal para que as alterações tenham efeito.

### Uso da CLI

```bash
python rathyon.py teste.ra   # executa pelo código-fonte
rathyon teste.ra             # executa o .exe se dist estiver no PATH
```

As opções `--help`, `--version` e `--info` não estão disponíveis nesta versão.

---

## Estrutura do projeto

```text
RATHYON/
├── rathyon.py                  # Interpretador (lexer, parser, executor, CLI)
├── principal.ra                # Programa de exemplo
├── requirements.txt            # Gerado pelo build (dependências do pip)
├── config/
│   ├── palavras_reservadas.json
│   └── build.py                # Script de build (gera dist/rathyon.exe)
├── assets/
│   └── rathyon.ico             # Ícone do executável
└── rathyon_setup/
    ├── rathyon_setup.py        # Instalador gráfico (Tkinter)
    ├── rathyon_setup.spec      # Configuração PyInstaller do instalador
    ├── rathyon.ico             # Ícone
    └── RaSetup_v1-3-0.exe      # Instalador compilado (v1.3.0)
```

---

## Tecnologias

| Tecnologia      | Uso                                                              |
|-----------------|------------------------------------------------------------------|
| **Python 3**    | Implementação do interpretador (somente biblioteca padrão)       |
| **Tkinter**     | Interface gráfica do instalador                                  |
| **PyInstaller** | Gera os executáveis `rathyon.exe` e `RaSetup`                    |
| **winreg**      | Configuração de PATH e associação de arquivos `.ra` no Windows   |

### Arquitetura do interpretador

```text
arquivo .ra → Lexer (tokens) → Parser (AST) → Executor
```

1. **Lexer** (`ler_tokens`): converte o texto em tokens, com linha e coluna.
2. **Parser** (`Analisador`): descida recursiva, gera a árvore de comandos.
3. **Executor** (`Executor`): percorre a árvore e avalia expressões.

Erros são reportados como `Erro de sintaxe` ou `Erro ao executar`, com linha e coluna quando disponíveis.

---

## Criadores

| Aluno                             | Matrícula |
| --------------------------------- | --------- |
| Pedro Artur R. F. Nogueira        | 01705061  |
| Marcos Emanuel Celestino Tavares  | 01718690  |
| Jhonas Xavier dos Santos Silva    | 01694333  |
| Alessandra Júlia Santos Mendonça  | 01710330  |
| Guilherme de Oliveira Lopes Silva | 01699872  |
| Alfred Vicente Silva da Rocha     | 01695802  |
| Alan Sergio Rodrigues De Carvalho | 01697157  |

---
**_"Rathyon é um projeto sem fim lucrativos feito por universitários cansados para o mundo."_**
