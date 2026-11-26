"""src/automata.py — Cursor e simulação explícita dos AFDs (tarefas 63-64).

Implementa o cursor sobre o texto-fonte e a simulação caractere a caractere
dos AFDs aprovados (AUTOMATA.md). Não usa regex geral que oculte o autômato.

Todo AFD é M = (Q, Sigma, delta, q0, F) com delta total sobre o Sigma do AFD.
q_d (estado -1) é o poço. Os nomes dos estados são locais a cada AFD.
Um símbolo fora do Sigma do AFD não é tratado por ele: o Scanner escolhe
outro reconhecedor ou reporta erro.
"""

from __future__ import annotations

from typing import Iterable, Optional

try:  # Import como pacote (rathyon.automata) ou módulo na raiz do projeto.
    from .tokens import Categoria, ErroLexico, Token
except ImportError:  # Compatibilidade com os testes que importam src.* na raiz.
    from src.tokens import Categoria, ErroLexico, Token

# Separadores: não geram tokens, apenas avançam a posição do cursor (regra 8).
SEPARADORES = {' ', '\t', '\n'}

# Estado poço de todos os AFDs. Qualquer transição para q_d permanece em q_d.
ESTADO_D = -1


def eh_letra(c: str) -> bool:
    """Letra L = a..z, A..Z, sem acento (SPECIFICATIONS.md §2)."""
    return ('a' <= c <= 'z') or ('A' <= c <= 'Z')


def eh_digito(c: str) -> bool:
    """Dígito D = 0..9."""
    return '0' <= c <= '9'

def reconhecer_diretiva(cursor: "Cursor"):
    """Reconhece #tunel NOME, #toca e #vaparatunel NOME.

    Emite tokens REGION_START / REGION_END / GOTO_REGION.
    Qualquer outro '#' vira ErroLexico de um caractere.
    """
    inicio = cursor.salvar()
    cursor.avancar()  # consome '#'
    palavra = []
    while not cursor.fim() and (eh_letra(cursor.peek()) or cursor.peek() == '_'):
        palavra.append(cursor.avancar())
    nome = "".join(palavra)

    def _ler_identificador():
        while not cursor.fim() and cursor.peek() in ' \t':
            cursor.avancar()
        buf = []
        while not cursor.fim() and (eh_letra(cursor.peek()) or eh_digito(cursor.peek()) or cursor.peek() == '_'):
            buf.append(cursor.avancar())
        return "".join(buf)

    def _pular_resto_da_linha():
        while not cursor.fim() and cursor.peek() != '\n':
            cursor.avancar()

    if nome == "tunel":
        reg = _ler_identificador()
        if not reg:
            cursor.restaurar(inicio)
            primeiro = cursor.avancar()
            return ErroLexico(primeiro, inicio[1], inicio[2],
                              "'#tunel' sem nome de região")
        _pular_resto_da_linha()
        return Token(Categoria.REGION_START, reg, inicio[1], inicio[2])

    if nome == "toca":
        _pular_resto_da_linha()
        return Token(Categoria.REGION_END, "", inicio[1], inicio[2])

    if nome == "vaparatunel":
        reg = _ler_identificador()
        if not reg:
            cursor.restaurar(inicio)
            primeiro = cursor.avancar()
            return ErroLexico(primeiro, inicio[1], inicio[2],
                              "'#vaparatunel' sem nome de região")
        _pular_resto_da_linha()
        return Token(Categoria.GOTO_REGION, reg, inicio[1], inicio[2])

    cursor.restaurar(inicio)
    primeiro = cursor.avancar()
    return ErroLexico(primeiro, inicio[1], inicio[2],
                      f"caractere fora do alfabeto: {primeiro!r}")

# Tabela fixa de classes para caracteres ASCII (Σ dos AFDs).
_CLASSE_ASCII: dict[str, str] = {}


def _construir_tabela_classe() -> dict[str, str]:
    tabela: dict[str, str] = {}
    for codigo in range(128):
        c = chr(codigo)
        if eh_letra(c):
            tabela[c] = 'L'
        elif eh_digito(c):
            tabela[c] = 'D'
        elif c == '_':
            tabela[c] = '_'
        elif c == '.':
            tabela[c] = '.'
        elif c in '=!<>+-*/(){}[];,#':
            tabela[c] = c
    return tabela


_CLASSE_ASCII = _construir_tabela_classe()


def classe_simbolo(c: str) -> Optional[str]:
    """Retorna a coluna da tabela de transição para c, ou None se c ∉ Σ.

    Exemplos de fora dos AFDs: '@', '#', '~', 'á' e '"'. Aspas são tratadas
    pelo reconhecedor de strings antes desta função.
    """
    return _CLASSE_ASCII.get(c)


# Conjunto K de palavras reservadas (SPECIFICATIONS.md §4; 24 palavras).
# Prioridade: se o lexema completo pertence a K, é KEYWORD; senão IDENTIFIER.
K_PADRAO = frozenset({
    "farejar", "refarejar", "fujir", "roer", "voltar", "escapar",
    "queijo", "migalha", "guinchar", "ouvir", "sinalizar",
    "cheio", "vazio", "vasculhar", "dentro", "trilha", "cavar",
    "barriga", "ninho", "seguir", "cace", "presa", "chiado", "procure",
})


class Cursor:
    """Posição atual, avanço de caractere e atualização de linha/coluna.

    linha e coluna são 1-based e apontam para o caractere atual (o próximo a
    ser consumido por avancar()).
    """

    def __init__(self, texto: str) -> None:
        self.texto = texto
        self.pos = 0          # índice do caractere atual
        self.linha = 1
        self.coluna = 1

    def fim(self) -> bool:
        return self.pos >= len(self.texto)

    def peek(self) -> Optional[str]:
        return None if self.fim() else self.texto[self.pos]

    def avancar(self) -> Optional[str]:
        """Consome o caractere atual, atualiza linha/coluna e devolve o caractere."""
        if self.fim():
            return None
        c = self.texto[self.pos]
        self.pos += 1
        if c == '\n':
            self.linha += 1
            self.coluna = 1
        else:
            self.coluna += 1
        return c

    def salvar(self) -> tuple:
        """Snapshot (pos, linha, coluna) para restaurar depois (maximal munch)."""
        return (self.pos, self.linha, self.coluna)

    def restaurar(self, s: tuple) -> None:
        self.pos, self.linha, self.coluna = s


# ---------------------------------------------------------------------------
# Tabelas de transição dos AFDs (AUTOMATA.md, seções 3.1 a 3.4)
# ---------------------------------------------------------------------------

# IDENTIFIER: Q={0, 1, q_d}, Sigma={L, D, _}, F={1}
# ER: (L | _)(L | D | _)*
DELTA_ID = {(0, 'L'): 1, (0, '_'): 1, (1, 'L'): 1, (1, 'D'): 1, (1, '_'): 1}
F_ID = {1}

# Números combinados (INTEGER + FLOAT): Q={0,1,2,3,q_d}, F={1, 3}
# q1 = INTEGER (D+); q3 = FLOAT (D+ . D+)
DELTA_NUM = {(0, 'D'): 1, (1, 'D'): 1, (1, '.'): 2, (2, 'D'): 3, (3, 'D'): 3, (0, '.'): ESTADO_D}
F_NUM = {1, 3}

# Atribuição e relacionais (modelo mínimo, 5 estados)
# 0=I, 1=A ('=', '<', '>'), 2=B ('==', '!=', '>=', '<='), 3=N ('!' pendente)
# Categoria definida pelo lexema: '=' -> ASSIGNMENT; demais -> RELATIONAL_OPERATOR.
DELTA_OP = {(0, '='): 1, (0, '!'): 3, (0, '<'): 1, (0, '>'): 1, (1, '='): 2, (3, '='): 2}
F_OP = {1, 2}

# Aritméticos: Q={0, q_f, q_d}, Sigma={+, -, *, /}, F={q_f}
DELTA_ARI = {(0, '+'): 1, (0, '-'): 1, (0, '*'): 1, (0, '/'): 1}
F_ARI = {1}

# Delimitadores: Q={0, q_f, q_d}, Sigma={( ) { } [ ] ; , .}, F={q_f}
DELTA_DEL = {(0, '('): 1, (0, ')'): 1, (0, '{'): 1, (0, '}'): 1,
             (0, '['): 1, (0, ']'): 1, (0, ';'): 1, (0, ','): 1,
             (0, '.'): 1}
F_DEL = {1}


def simular_afd(cursor: Cursor, delta: dict, finais: set) -> tuple:
    """Simula o AFD caractere a caractere sobre o cursor (maximal munch).

    Avança o cursor enquanto houver transição definida. Guarda o snapshot
    (pos, linha, coluna) do ÚLTIMO estado final alcançado, que é o prefixo
    mais longo aceito (maior casamento). Devolve também o estado desse último
    final, usado para distinguir INTEGER (q1) de FLOAT (q3).

    O cursor NÃO é restaurado: cabe ao chamador restaurar para o último final
    quando for emitir o token.

    Retorna (snapshot_ultimo_final | None, estado_do_ultimo_final | None).
    """
    estado = 0
    ultimo: Optional[tuple] = None
    est_ultimo: Optional[int] = None
    while not cursor.fim():
        c = cursor.peek()
        col = classe_simbolo(c)
        if col is None or (estado, col) not in delta:
            break
        cursor.avancar()
        estado = delta[(estado, col)]
        if estado in finais:
            ultimo = cursor.salvar()
            est_ultimo = estado
        if estado == ESTADO_D:
            break
    return ultimo, est_ultimo


def reconhecer_identificador(cursor: Cursor, palavras_reservadas: Iterable[str]) -> Token:
    """AFD do identificador.

    Retorna KEYWORD se o lexema completo pertence a K, senão IDENTIFIER
    (prioridade de KEYWORD sobre IDENTIFIER, SPECIFICATIONS.md §5 regra 2).
    """
    inicio = cursor.salvar()
    ult, _ = simular_afd(cursor, DELTA_ID, F_ID)
    cursor.restaurar(ult)
    lexema = cursor.texto[inicio[0]:cursor.pos]
    cat = Categoria.KEYWORD if lexema in palavras_reservadas else Categoria.IDENTIFIER
    return Token(cat, lexema, inicio[1], inicio[2])


def reconhecer_numero(cursor: Cursor):
    """AFD combinado de números (F = {q1 INTEGER, q3 FLOAT}).

    Retorna Token(INTEGER/FLOAT) com maximal munch, ou ErroLexico quando o
    ponto está dentro de Sigma mas não leva a um estado final
    (ex.: ponto isolado, '5.', '.5').

    Regra especial (D-LEX-06): dígitos seguidos de letra ou '_' formam um
    ÚNICO erro léxico que consome toda a sequência (ex.: '123abc').
    """
    inicio = cursor.salvar()
    ult, est = simular_afd(cursor, DELTA_NUM, F_NUM)
    if ult is None:
        if cursor.pos > inicio[0]:
            return ErroLexico(cursor.texto[inicio[0]:cursor.pos], inicio[1], inicio[2], "número mal formado")
        return None
    cursor.restaurar(ult)
    p = cursor.peek()
    if p is not None and (eh_letra(p) or p == '_'):
        while not cursor.fim():
            c = cursor.peek()
            col = classe_simbolo(c)
            if col is None or col not in ('L', 'D', '_'):
                break
            cursor.avancar()
        return ErroLexico(cursor.texto[inicio[0]:cursor.pos], inicio[1], inicio[2], "número mal formado: dígitos seguidos de letra ou sublinhado")
    cat = Categoria.INTEGER if est == 1 else Categoria.FLOAT
    return Token(cat, cursor.texto[inicio[0]:cursor.pos], inicio[1], inicio[2])


def reconhecer_relacional(cursor: Cursor):
    """AFD de atribuição e relacionais (modelo mínimo, 5 estados).

    Estado A (1): '=', '<', '>' ; Estado B (2): '==', '!=', '>=', '<='.
    Categoria definida pelo lexema (AUTOMATA.md §5.3):
    '=' -> ASSIGNMENT; os demais -> RELATIONAL_OPERATOR.
    '!' isolado não leva a estado final -> ErroLexico.
    """
    inicio = cursor.salvar()
    ult, est = simular_afd(cursor, DELTA_OP, F_OP)
    if ult is None:
        if cursor.pos > inicio[0]:
            return ErroLexico(cursor.texto[inicio[0]:cursor.pos], inicio[1], inicio[2], "operador '!' isolado não é válido; use '!='")
        return None
    cursor.restaurar(ult)
    lexema = cursor.texto[inicio[0]:cursor.pos]
    cat = Categoria.ASSIGNMENT if (est == 1 and lexema == '=') else Categoria.RELATIONAL_OPERATOR
    return Token(cat, lexema, inicio[1], inicio[2])


def _simples(cursor, delta, finais, categoria, mensagem_erro=None):
    """Reconhece um token de um caractere (ou prefixo fixo) via AFD."""
    inicio = cursor.salvar()
    ult, _ = simular_afd(cursor, delta, finais)
    if ult is None:
        if cursor.pos > inicio[0]:
            return ErroLexico(
                cursor.texto[inicio[0]:cursor.pos], inicio[1], inicio[2],
                mensagem_erro or "construção inválida")
        return None
    cursor.restaurar(ult)
    return Token(categoria, cursor.texto[inicio[0]:cursor.pos],
                 inicio[1], inicio[2])


def reconhecer_aritmetico(cursor: Cursor) -> Token:
    """AFD dos operadores aritméticos (+, -, *, /). Um caractere por token."""
    return _simples(cursor, DELTA_ARI, F_ARI,
                    Categoria.ARITHMETIC_OPERATOR)


def reconhecer_delimitador(cursor: Cursor) -> Token:
    """AFD dos delimitadores (( ) { } [ ] ; , .). Um caractere por token."""
    return _simples(cursor, DELTA_DEL, F_DEL, Categoria.DELIMITER)


def reconhecer_string(cursor: Cursor):
    """Reconhece string de aspas duplas com escapes no estilo JSON."""
    inicio = cursor.salvar()
    cursor.avancar()
    erro = None
    while not cursor.fim():
        caractere = cursor.peek()
        if caractere == '"':
            cursor.avancar()
            lexema = cursor.texto[inicio[0]:cursor.pos]
            if erro:
                return ErroLexico(lexema, inicio[1], inicio[2], erro)
            return Token(Categoria.STRING, lexema, inicio[1], inicio[2])
        if caractere == '\n':
            lexema = cursor.texto[inicio[0]:cursor.pos]
            return ErroLexico(lexema, inicio[1], inicio[2], erro or "string sem fechamento")
        if caractere == '\\':
            cursor.avancar()
            escapado = cursor.peek()
            if escapado is None or escapado == '\n':
                lexema = cursor.texto[inicio[0]:cursor.pos]
                return ErroLexico(lexema, inicio[1], inicio[2], erro or "string sem fechamento")
            if escapado in '"\\/bfnrt':
                cursor.avancar()
                continue
            if escapado == 'u':
                cursor.avancar()
                digitos = 0
                while digitos < 4 and cursor.peek() is not None and cursor.peek() in '0123456789abcdefABCDEF':
                    cursor.avancar()
                    digitos += 1
                if digitos != 4 and erro is None:
                    erro = "escape Unicode inválido em string"
                continue
            cursor.avancar()
            if erro is None:
                erro = "escape inválido em string"
            continue
        if ord(caractere) < 0x20 and erro is None:
            erro = "caractere de controle inválido em string"
        cursor.avancar()
    lexema = cursor.texto[inicio[0]:cursor.pos]
    return ErroLexico(lexema, inicio[1], inicio[2], erro or "string sem fechamento")


def reconhecer_qualquer(cursor: Cursor, palavras_reservadas: Iterable[str]):
    """Despacha para o reconhecedor da classe do caractere atual.

    Retorna Token, ErroLexico ou None quando o caractere está fora de Σ
    (nesse caso o Scanner gera um erro de um caractere).
    """
    c = cursor.peek()
    if c is None:
        return None
    if c == '"':
        return reconhecer_string(cursor)
    cls = classe_simbolo(c)
    if cls in ('L', '_'):
        return reconhecer_identificador(cursor, palavras_reservadas)
    if cls == '.':
        proximo = cursor.texto[cursor.pos + 1:cursor.pos + 2]
        if classe_simbolo(proximo) in ('L', '_'):
            return reconhecer_delimitador(cursor)
    if cls in ('D', '.'):
        return reconhecer_numero(cursor)
    if cls in ('=', '!', '<', '>'):
        return reconhecer_relacional(cursor)
    if cls in ('+', '-', '*', '/'):
        return reconhecer_aritmetico(cursor)
    if cls in ('(', ')', '{', '}', '[', ']', ';', ','):
        return reconhecer_delimitador(cursor)
    if cls == '#':
        return reconhecer_diretiva(cursor)
    return None
