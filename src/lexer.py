
# src/lexer.py

#generico pra substituicao futura
from .tokens import Token, Categoria, ErroLexico

class Cursor:
    def __init__(self, texto: str):
        self.texto = texto
        self.pos = 0
        self.linha = 1
        self.coluna = 1   # ← FALTAVA ISSO

    def fim(self) -> bool:
        return self.pos >= len(self.texto)

    def peek(self):
        return None if self.fim() else self.texto[self.pos]

    def avancar(self):
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

    def salvar(self):
        return (self.pos, self.linha, self.coluna)

    def restaurar(self, snapshot):
        self.pos, self.linha, self.coluna = snapshot


# Exemplo de reconhecedor de identificador/palavra reservada
K_PADRAO = frozenset({...})  # coloque as 17 palavras reservadas aqui

def reconhecer_identificador(cursor: Cursor, palavras_reservadas):
    inicio = cursor.salvar()
    estado = 0
    ultimo_final = None

    while True:
        c = cursor.peek()
        if c is None:
            break
        if not (c.isalpha() or c == '_' or (estado == 1 and c.isdigit())):
            break
        cursor.avancar()
        if c.isalpha() or c == '_':
            estado = 1
        elif estado == 1 and c.isdigit():
            estado = 1
        if estado == 1:
            ultimo_final = cursor.salvar()

    if ultimo_final is None:
        return None

    cursor.restaurar(ultimo_final)
    lexema = cursor.texto[inicio[0]:cursor.pos]
    cat = Categoria.KEYWORD if lexema in palavras_reservadas else Categoria.IDENTIFIER
    return Token(cat, lexema, inicio[1], inicio[2])