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
- **Implementação:** Python (Scanner, Parser e Executor em módulos separados)
- **Plataforma do instalador:** Windows

---
## Referência da linguagem

### Palavras-chave

| Rathyon     | Equivalente | Função                  |
| ----------- | ----------- | ----------------------- |
| `queijo`    | `int`       | Declara inteiro         |
| `migalha`   | `float`     | Declara decimal         |
| `barriga`   | `bool`      | Declara booleano        |
| `chiado`    | `str`       | Declara texto           |
| `ninho`     | `list`      | Declara lista           |
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
| `procure`   | `import`    | Importa um módulo       |
| `seguir`    | `continue`  | Vai à próxima repetição |
| `cace`      | `switch`    | Seleciona um caso       |
| `presa`     | `case`      | Define uma alternativa  |

### Operadores

- **Aritméticos:** `+  -  *  /`
- **Comparação:** `==  !=  <  >  <=  >=`
- **Atribuição:** `=`
- **Strings:** use aspas duplas; escapes como `\n`, `\t`, `\\` e `\"` são aceitos.
- **Comentários:** ainda não são aceitos pelo interpretador.

### Regiões

As regiões organizam blocos do programa e permitem saltar para uma região pelo nome:

- `#tunel nome` — inicia uma região.
- `#toca` — encerra a região atual.
- `#vaparatunel nome` — salta para a região indicada.

As regiões `entrada` e `saida` são executadas no início e no fim do programa. `passagem` identifica uma região comum e recebe destaque no VS Code.

> O instalador publicado na versão 0.2.0 ainda usa os nomes antigos das regiões. Os nomes desta seção estão no código-fonte atual.
---
### Regras e limitações

- Declarações, atribuições e chamadas terminam com `;`; blocos usam `{}`.
- Atribuir um valor cria a variável, mesmo sem declaração prévia.
- `queijo` converte o valor inicial para inteiro; atribuições posteriores não verificam o tipo.
- `barriga`, `chiado` e `ninho` declaram booleanos, textos e listas. Listas usam `[]`, aceitam acesso por índice e podem ser percorridas com `vasculhar`.
- Parâmetros de funções podem receber tipo: `cavar somar(queijo a, queijo b) { voltar a + b; }`. Funções sem anotação continuam aceitas.
- `procure math;` importa um módulo Python; seus membros podem ser chamados com ponto, como `math.sqrt(4)`.
- `cace valor { presa 1 { ... } fujir { ... } }` executa o primeiro caso correspondente; `fujir` é opcional e funciona como padrão.
- Não há entrada de dados (`input`) nesta versão.

---

## Instalação e setup

### Requisitos

- Windows 10 ou superior
- Para usar o instalador, não é necessário instalar Python.

### Opção 1 — Instalador gráfico (recomendado)

1. Abra a [versão mais recente](https://github.com/fumiko0701/rathyon/releases/latest) e baixe `rathyon_setup.exe` em **Assets**.
2. Execute o arquivo e siga o assistente. Ele configura o PATH e associa arquivos `.ra` ao Rathyon.
3. Crie `meu_programa.ra` com estas instruções:

```rathyon
queijo idade = 18;
guinchar(idade);
```

Salve como **Todos os arquivos**.
4. Abra a pasta do arquivo no Explorador de Arquivos, digite `powershell` na barra de endereço e pressione Enter. Execute:

```powershell
rathyon meu_programa.ra
```

O terminal deve mostrar `18`.

### Opção 2 — Executar a partir do código-fonte

Com Python 3.10 ou superior instalado, execute na raiz do projeto:

```bash
python rathyon.py t/teste_completo.ra
```

### Opção 3 — Build via `config/build.py` (Desenvolvedores)

Para gerar o executável, abra o PowerShell na raiz do projeto e execute:

```powershell
python -m pip install -r requirements.txt
python config/build.py
```

No Windows, o executável será criado em `dist/rathyon.exe`. Para executá-lo da raiz do projeto, use `.\dist\rathyon.exe t\teste_completo.ra`.

#### Configurando o PATH (apenas Windows)

Para poder rodar `rathyon arquivo.ra` de qualquer pasta no seu terminal (sem precisar digitar o caminho completo do `.exe`):

1. Copie o caminho completo da pasta `dist` (ex: `C:\Users\SeuUsuario\Documents\rathyon\dist`).
2. Pesquise no menu Iniciar por **"Editar as variáveis de ambiente do sistema"**.
3. Clique em **Variáveis de Ambiente** → encontre a variável **Path** e clique em **Editar**.
4. Clique em **Novo**, cole o caminho copiado e dê **OK** em tudo.

> **Importante:** feche e abra um novo terminal para que as alterações tenham efeito.

### Uso da CLI

```bash
python rathyon.py t/teste_completo.ra   # executa pelo código-fonte
rathyon t/teste_completo.ra             # executa o .exe se dist estiver no PATH
```

Sem arquivo, `rathyon` abre o console interativo, que traduz algumas palavras para Python. Arquivos `.ra` usam o Scanner, o Parser e o Executor do Rathyon.

As opções `--help`, `--version` e `--info` não estão disponíveis nesta versão.

---

## Estrutura do projeto

```text
RATHYON/
├── rathyon.py                  # CLI e ponto de entrada
├── src/                        # Scanner, Parser, Executor e autômatos
├── config/
│   ├── palavras_reservadas.json
│   └── build.py                # Script de build (gera dist/rathyon.exe)
├── assets/
│   ├── rathyon.ico
│   └── rathyon_brand.svg
├── tests/                      # Testes automatizados
├── t/                          # Programas de exemplo
├── docs/                       # Relatório e documentos de apoio
├── vscode_rathyon_v0.2.0/      # Extensão do VS Code
└── requirements.txt            # Dependências do build
```

---

## Tecnologias

| Tecnologia      | Uso                                                              |
|-----------------|------------------------------------------------------------------|
| **Python 3**    | Scanner, Parser, Executor e CLI                                  |
| **JavaScript**  | Extensão de suporte para o VS Code                               |
| **PyInstaller** | Gera `rathyon.exe` a partir do código-fonte                      |

### Arquitetura do interpretador

```text
arquivo .ra → Scanner (tokens) → Parser (AST) → Executor
```

1. **Scanner** (`src/lexer.py`): converte o texto em tokens com linha e coluna.
2. **Parser** (`src/parser.py`): analisa os tokens e gera a árvore do programa.
3. **Executor** (`src/executor.py`): percorre a árvore e executa as instruções.

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
