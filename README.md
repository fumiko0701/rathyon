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
- **Versão da linguagem:** 0.0.1
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

### Operadores

- **Aritméticos:** `+  -  *  /`
- **Comparação:** `==  !=  <  >  <=  >=`
- **Atribuição:** `=`
- **Comentário:** `// texto`
- **Texto:** `"entre aspas"`
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
- [Python 3.10+](https://www.python.org/downloads/) instalado (o instalador compila o interpretador)
- Conexão com a internet (download do PyInstaller)

### Opção 1 — Instalador gráfico (recomendado)

1. Execute `rathyon_setup/RaSetup_v1-3-0.exe`.
2. Escolha o diretório de instalação (padrão: `%LOCALAPPDATA%\Programs\Rathyon`).
3. Marque as opções desejadas:
   - **Adicionar ao PATH** do Windows
   - **Associar arquivos `.ra`** à Rathyon (duplo clique executa e exibe o ícone)
4. Clique em instalar e aguarde as 7 etapas:
   1. Ambiente Python (`.venv`)
   2. Dependências
   3. Localização do arquivo principal
   4. Compilação com PyInstaller
   5. Cópia do executável e ícone
   6. Configuração do PATH
   7. Associação `.ra`
5. Reabra o terminal e valide:

```bash
rathyon --version
```

### Opção 2 — Executar a partir do código-fonte

```bash
python rathyon.py principal.ra
```

### Opção 3 — Build manual via terminal (Desenvolvedores)

Se você é um desenvolvedor e precisa compilar o interpretador manualmente para testar alterações no código ou gerar o `.exe` sem usar o instalador gráfico, siga os passos abaixo:

#### 1. Instale as dependências

Certifique-se de ter o Python 3.10+ instalado (com a opção **"Add python.exe to PATH"** marcada na instalação).
No terminal, dentro da pasta raiz do projeto, instale o PyInstaller:

```bash
python -m pip install pyinstaller
```

#### 2. Compile o interpretador (Rathyon)

Como o projeto utiliza um arquivo de configuração externo (`config/palavras_reservadas.json`), é **obrigatório** usar a flag `--add-data` para embutir esse arquivo dentro do executável. Caso contrário, o `.exe` gerado não conseguirá traduzir as palavras-chave.

Execute o comando abaixo na raiz do projeto:

**No Windows (CMD/PowerShell):**

```bash
python -m PyInstaller --onefile --add-data "config/palavras_reservadas.json;config" rathyon.py
```

**No Linux / macOS:**

```bash
python -m PyInstaller --onefile --add-data "config/palavras_reservadas.json:config" rathyon.py
```

> **Nota:** a única diferença entre os sistemas é o separador do `--add-data`: `;` no Windows e `:` no Linux/macOS.

#### 3. Localizando o executável

Após o término do processo, o PyInstaller criará uma pasta chamada `dist`. O seu executável final estará em `dist/rathyon.exe` (ou `dist/rathyon` no Linux/macOS).

#### 4. Configurando o PATH (apenas Windows)

Para poder rodar `rathyon arquivo.ra` de qualquer pasta no seu terminal (sem precisar digitar o caminho completo do `.exe`):

1. Copie o caminho completo da pasta `dist` (ex: `C:\Users\SeuUsuario\Documents\rathyon\dist`).
2. Pesquise no menu Iniciar por **"Editar as variáveis de ambiente do sistema"**.
3. Clique em **Variáveis de Ambiente** → encontre a variável **Path** e clique em **Editar**.
4. Clique em **Novo**, cole o caminho copiado e dê **OK** em tudo.

> **Importante:** feche e abra um novo terminal para que as alterações tenham efeito.

### Uso da CLI

```bash
rathyon <arquivo.ra>     # executa um programa
rathyon -h, --help       # ajuda
rathyon -v, --version    # versão (alias: --v)
rathyon --info           # informações da instalação
```

---

## Estrutura do projeto

```text
RATHYON/
├── rathyon.py                  # Interpretador (lexer, parser, executor, CLI)
├── principal.ra                # Programa de exemplo
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