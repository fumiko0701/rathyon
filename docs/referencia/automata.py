"""
automata.py — Cursor e simulação explícita dos AFDs do Scanner (tarefas 63-64).

Base: docs/markdown/AUTOMATA.md (T04/T05), tabelas de transição dos AFDs
aprovados, sem alterar nenhuma regra léxica.

Todo AFD é M = (Q, Sigma, delta, q0, F) com delta total sobre o Sigma do AFD.
q_d (estado -1) é o poço. Os nomes dos estados são locais a cada AFD.
Um símbolo fora do Sigma do AFD não é tratado por ele: o Scanner escolhe outro
reconhecedor ou reporta erro.

A simulação é feita caractere a caractere sobre o cursor (maximal munch:
guardar o último estado final válido). Não se usa uma regex geral que oculte o
autômato.
"""

from __future__ import annotations

from typing import Iterable, Optional

from .tokens import Categoria, ErroLexico, Token

# ---------------------------------------------------------------------------
# Alfabeto e classes de símbolo (colunas das tabelas de AUTOMATA.md)
# ---------------------------------------------------------------------------

SEPARADORES = {' ', '\t', '\n'}  # não geram tokens (regra 8 de SPECIFICATIONS.md)

ESTADO_D = -1  # poço de todos os AFDs


def eh_letra(c: str) -> bool:
    """Letra L = a..z, A..Z, sem acento (SPECIFICATIONS.md §2)."""
    return ('a' <= c <= 'z') or ('A' <= c <= 'Z')


def eh_digito(c: str) -> bool:
    return '0' <= c <= '9'


def classe_simbolo(c: str) -> Optional[str]:
    """Retorna a coluna da tabela de transição para c, ou None se c ∉ Σ.

    Exemplos de fora de Σ: '@', '#', '~', 'á', '"'. Eles geram erro léxico
    e a leitura continua.
    """
    if eh_letra(c):
        return 'L'
    if eh_digito(c):
        return 'D'
    if c == '_':
        return '_'
    if c == '.':
        return '.'
    if c in '=!<>':
        return c
    if c in '+-*/':
        return c
    if c in '(){};,':
        return c
    return None


# ---------------------------------------------------------------------------
# Conjunto K de palavras reservadas (SPECIFICATIONS.md §4; 17 palavras)
# ---------------------------------------------------------------------------

K_PADRAO = frozenset({
    "farejar", "refarejar", "fujir", "roer", "voltar", "escapar",
    "queijo", "migalha", "guinchar", "ouvir", "sinalizar",
    "cheio", "vazio", "vasculhar", "dentro", "trilha", "cavar",
})


# ---------------------------------------------------------------------------
# Cursor sobre o texto (tarefa 63)
# ---------------------------------------------------------------------------

class Cursor:
    """Posição atual, avanço de caractere e atualização de linha/coluna.

    linha e coluna são 1-based e apontam para o caractere atual (o próximo a
    ser consumido por avancar()).
    """

    def __init__(self, texto: str) -> None:
        self.texto = texto
        self.pos = 0          # índice do caractere atual
        self.linha = 1


# ---------------------------------------------------------------------------
# Tabelas de transição dos AFDs (AUTOMATA.md, seções 3.1 a 3.4)
# ---------------------------------------------------------------------------

# --- IDENTIFIER: Q={0, 1, q_d}, Sigma={L, D, _}, F={1}                ---
# ER: (L | _)(L | D | _)*
#   0 --L/_--> 1 ;  1 --L/D/_--> 1 ;  q_d --qualquer--> q_d
DELTA_ID = {
    (0, 'L'): 1,
    (0, '_'): 1,
    (1, 'L'): 1,
    (1, 'D'): 1,
    (1, '_'): 1,
}
F_ID = {1}

# --- Números combinados (INTEGER + FLOAT): Q={0,1,2,3,q_d}, F={1, 3} --
# INTEGER (ER: D+): q1 final. FLOAT (ER: D+ . D+): q3 final.
#   0 --D--> 1 ; 1 --D--> 1 ; 1 --.--> 2 ; 2 --D--> 3 ; 3 --D--> 3
#   0 --.--> q_d ; q_d --qualquer--> q_d
DELTA_NUM = {
    (0, 'D'): 1,
    (1, 'D'): 1,
    (1, '.'): 2,
    (2, 'D'): 3,
    (3, 'D'): 3,
    (0, '.'): ESTADO_D,  # ponto inicial / ponto isolado
}
F_NUM = {1, 3}  # estado 1 -> INTEGER ; estado 3 -> FLOAT

# --- Atribuição e relacionais (modelo mínimo, 5 estados) ----------------
# Estados: 0=I, 1=A ('=', '<', '>'), 2=B ('==', '!=', '>=', '<='),
#          3=N ('!' pendente), q_d=poço. F={1, 2}.
#   I: '='/'<'/'>' -> A ; '!' -> N
#   A: '=' -> B ; N: '=' -> B ; resto -> q_d
DELTA_OP = {
    (0, '='): 1, (0, '!'): 3, (0, '<'): 1, (0, '>'): 1,
    (1, '='): 2,
    (3, '='): 2,
}
F_OP = {1, 2}  # 1 -> A ; 2 -> B

# --- Aritméticos: Q={0, q_f, q_d}, Sigma={+, -, *, /}, F={q_f} -------
DELTA_ARI = {
    (0, '+'): 1, (0, '-'): 1, (0, '*'): 1, (0, '/'): 1,
}
F_ARI = {1}

# --- Delimitadores: Q={0, q_f, q_d}, Sigma={( ) { } ; ,}, F={q_f} -----
DELTA_DEL = {
    (0, '('): 1, (0, ')'): 1, (0, '{'): 1,
    (0, '}'): 1, (0, ';'): 1, (0, ','): 1,
}
F_DEL = {1}


# ---------------------------------------------------------------------------
# Funções de reconhecimento por classe de token (tarefa 64)
# Cada uma simula o AFD correspondente caractere a caractere.
# ---------------------------------------------------------------------------

def reconhecer_identificador(
    cursor: Cursor, palavras_reservadas: Iterable[str]
) -> Optional[Token]:
    """AFD do identificador.

    Retorna KEYWORD se o lexema completo pertence a K, senão IDENTIFIER
    (prioridade de KEYWORD sobre IDENTIFIER, SPECIFICATIONS.md §5 regra 2).
    """
    inicio = cursor.salvar()
    estado = 0
    ultimo_final: Optional[tuple] = None  # (snapshot, estado)

    while True:
        c = cursor.peek()
        if c is None:
            break
        col = classe_simbolo(c)
        if col is None or (estado, col) not in DELTA_ID:
            break
        cursor.avancar()
        estado = DELTA_ID[(estado, col)]
        if estado in F_ID:
            ultimo_final = (cursor.salvar(), estado)
        if estado == ESTADO_D:
            break

    if ultimo_final is None:  # defensivo: não ocorre por construção (chamado com L ou '_')
        return None

    snap, estado_final = ultimo_final
    cursor.restaurar(snap)
    lexema = cursor.texto[inicio[0]:cursor.pos]
    categoria = (
        Categoria.KEYWORD if lexema in palavras_reservadas else Categoria.IDENTIFIER
    )
    return Token(categoria, lexema, inicio[1], inicio[2])


def reconhecer_numero(cursor: Cursor):
    """AFD combinado de números (F = {q1 INTEGER, q3 FLOAT}).

    Retorna Token(INTEGER/FLOAT) com maximal munch, ou ErroLexico quando o
    ponto está dentro de Sigma mas não leva a um estado final
    (ex.: ponto isolado, '5.', '.5').

    Regra especial do PDF/T02 (registrada como decisão D-LEX-06): dígitos
    seguidos de letra ou '_' formam um ÚNICO erro léxico que consome toda a
    sequência (ex.: '123abc' -> erro consumindo '123abc').
    """
    inicio = cursor.salvar()
    estado = 0
    ultimo_final: Optional[tuple] = None

    while True:
        c = cursor.peek()
        if c is None:
            break
        col = classe_simbolo(c)
        if col is None or (estado, col) not in DELTA_NUM:
            break
        cursor.avancar()
        estado = DELTA_NUM[(estado, col)]
        if estado in F_NUM:
            ultimo_final = (cursor.salvar(), estado)
        if estado == ESTADO_D:
            break

    if ultimo_final is None:
        # Dentro de Sigma ('.') mas nenhum estado final alcançado: rejeição.
        if cursor.pos > inicio[0]:
            lexema = cursor.texto[inicio[0]:cursor.pos]
            return ErroLexico(
                lexema, inicio[1], inicio[2], "número mal formado"
            )
        return None

    snap, estado_final = ultimo_final
    cursor.restaurar(snap)


def reconhecer_relacional(cursor: Cursor):
    """AFD de atribuição e relacionais (modelo mínimo, 5 estados).

    Estado A (1): '=', '<', '>' ; Estado B (2): '==', '!=', '>=', '<='.
    A categoria vem do lexema (AUTOMATA.md §5.3):
    '=' -> ASSIGNMENT; os demais -> RELATIONAL_OPERATOR.
    '!' isolado não leva a estado final -> ErroLexico.
    """
    inicio = cursor.salvar()
    estado = 0
    ultimo_final: Optional[tuple] = None

    while True:
        c = cursor.peek()
        if c is None:
            break
        col = classe_simbolo(c)
        if col is None or (estado, col) not in DELTA_OP:
            break
        cursor.avancar()
        estado = DELTA_OP[(estado, col)]
        if estado in F_OP:
            ultimo_final = (cursor.salvar(), estado)
        if estado == ESTADO_D:
            break

    if ultimo_final is None:
        if cursor.pos > inicio[0]:
            lexema = cursor.texto[inicio[0]:cursor.pos]
            return ErroLexico(
                lexema,
                inicio[1],
                inicio[2],
                "operador '!' isolado não é válido; use '!='",
            )
        return None

    snap, estado_final = ultimo_final
    cursor.restaurar(snap)
    lexema = cursor.texto[inicio[0]:cursor.pos]
    if estado_final == 1:
        categoria = (
            Categoria.ASSIGNMENT if lexema == '=' else Categoria.RELATIONAL_OPERATOR
        )
    else:
        categoria = Categoria.RELATIONAL_OPERATOR
    return Token(categoria, lexema, inicio[1], inicio[2])


def reconhecer_aritmetico(cursor: Cursor) -> Token:
    """AFD dos operadores aritméticos (+, -, *, /). Um caractere por token."""
    inicio = cursor.salvar()
    estado = 0
    ultimo_final: Optional[tuple] = None

    while True:
        c = cursor.peek()
        if c is None:
            break
        col = classe_simbolo(c)
        if col is None or (estado, col) not in DELTA_ARI:
            break
        cursor.avancar()
        estado = DELTA_ARI[(estado, col)]
        if estado in F_ARI:
            ultimo_final = (cursor.salvar(), estado)
        if estado == ESTADO_D:
            break

    # Chamado apenas quando o primeiro caractere está em '+-*/', então
    # ultimo_final sempre existe (q0 --op--> q_f).
    snap, _estado_final = ultimo_final
    cursor.restaurar(snap)
    lexema = cursor.texto[inicio[0]:cursor.pos]
    return Token(Categoria.ARITHMETIC_OPERATOR, lexema, inicio[1], inicio[2])


def reconhecer_delimitador(cursor: Cursor) -> Token:
    """AFD dos delimitadores (( ) { } ; ,). Um caractere por token."""
    inicio = cursor.salvar()
    estado = 0
    ultimo_final: Optional[tuple] = None

    while True:
        c = cursor.peek()
        if c is None:
            break
        col = classe_simbolo(c)
        if col is None or (estado, col) not in DELTA_DEL:
            break
        cursor.avancar()
        estado = DELTA_DEL[(estado, col)]
        if estado in F_DEL:
            ultimo_final = (cursor.salvar(), estado)
        if estado == ESTADO_D:
            break

    snap, _estado_final = ultimo_final
    cursor.restaurar(snap)
    lexema = cursor.texto[inicio[0]:cursor.pos]
    return Token(Categoria.DELIMITER, lexema, inicio[1], inicio[2])


def reconhecer_qualquer(cursor: Cursor, palavras_reservadas: Iterable[str]):
    """Despacha para o reconhecedor da classe do caractere atual.

    Retorna Token, ErroLexico ou None quando o caractere está fora de Σ
    (nesse caso o Scanner gera um erro de um caractere).
    """
    c = cursor.peek()
    if c is None:
        return None
    if eh_letra(c) or c == '_':
        return reconhecer_identificador(cursor, palavras_reservadas)
    if eh_digito(c):
        return reconhecer_numero(cursor)
    if c in '=!<>':
        return reconhecer_relacional(cursor)
    if c in '+-*/':
        return reconhecer_aritmetico(cursor)
    if c in '(){};,':
        return reconhecer_delimitador(cursor)
    if c == '.':
        return reconhecer_numero(cursor)
    return None


    proximo = cursor.peek()
    if proximo is not None and (eh_letra(proximo) or proximo == '_'):
        # Regra especial: 123abc -> um erro consumindo a sequência toda.
        while True:
            c = cursor.peek()
            if c is None:
                break
            col = classe_simbolo(c)
            if col is None or col not in ('L', 'D', '_'):
                break
            cursor.avancar()
        lexema = cursor.texto[inicio[0]:cursor.pos]
        return ErroLexico(
            lexema,
            inicio[1],
            inicio[2],
            "número mal formado: dígitos seguidos de letra ou sublinhado",
        )

    lexema = cursor.texto[inicio[0]:cursor.pos]
    categoria = Categoria.INTEGER if estado_final == 1 else Categoria.FLOAT
    return Token(categoria, lexema, inicio[1], inicio[2])

        self.coluna = 1

    def fim(self) -> bool:
        return self.pos >= len(self.texto)

    def peek(self) -> Optional[str]:
        if self.fim():
            return None
        return self.texto[self.pos]

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

    def restaurar(self, snapshot: tuple) -> None:
        self.pos, self.linha, self.coluna = snapshot
