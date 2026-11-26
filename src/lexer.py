
"""src/lexer.py — Scanner da Linguagem do Rato (tarefas 65-66).

Laço principal: pula separadores e comentários, tenta reconhecer o próximo
token, mantém o último estado final válido (maior casamento / maximal munch)
e emite o token. Sinaliza o fim de arquivo e devolve a lista de tokens e erros.
"""

from __future__ import annotations

from typing import Iterable, List, Tuple

try:  # Import como pacote (rathyon.lexer) ou módulo na raiz do projeto.
    from .automata import Cursor, K_PADRAO, SEPARADORES, reconhecer_qualquer
    from .tokens import Categoria, ErroLexico, Token
except ImportError:  # Compatibilidade com os testes que importam src.* na raiz.
    from src.automata import Cursor, K_PADRAO, SEPARADORES, reconhecer_qualquer
    from src.tokens import Categoria, ErroLexico, Token


class Scanner:
    """Analisador léxico da Linguagem do Rato.

    Argumentos:
        texto: código-fonte a ser escaneado.
        palavras_reservadas: conjunto K opcional. Quando omitido, usa K_PADRAO
            (24 palavras de SPECIFICATIONS.md §4).
        normalizar_quebras_de_linha: converte '\\r\\n' e '\\r' para '\\n' antes de
            escanear, de modo que '\\r' não seja reportado como erro.
    """

    def __init__(
        self,
        texto: str,
        *,
        palavras_reservadas: Iterable[str] | None = None,
        normalizar_quebras_de_linha: bool = True
    ) -> None:
        if normalizar_quebras_de_linha:
            texto = texto.replace('\r\n', '\n').replace('\r', '\n')

        self._texto = texto
        self._palavras_reservadas = (
            set(K_PADRAO)
            if palavras_reservadas is None
            else set(palavras_reservadas)
        )

    @property
    def palavras_reservadas(self) -> set:
        return self._palavras_reservadas

    def scan(
        self, *, incluir_eof: bool = False
    ) -> Tuple[List[Token], List[ErroLexico]]:
        """Percorre todo o texto-fonte e devolve (tokens, erros).

        - Separadores são pulados (não aparecem na saída).
        - Comentários iniciados por # são ignorados até o fim da linha.
        - Cada caractere restante é enviado ao reconhecedor de sua classe.
        - O maior prefixo aceito (maximal munch) é emitido como um Token.
        - Caracteres inválidos ou construções rejeitadas viram ErroLexico e a
          leitura continua depois deles (não há exceção por erro léxico).
        - Fim de arquivo é sinalizado pelo fim da lista; opcionalmente anexa um
          Token(Categoria.EOF, "", linha, coluna) quando incluir_eof=True.

        Retorna:
            (tokens, erros): listas com Token e ErroLexico, na ordem da entrada.
        """

        tokens: List[Token] = []
        erros: List[ErroLexico] = []
        cursor = Cursor(self._texto)

        while not cursor.fim():
            c = cursor.peek()

            if c is None:
                break

            # Ignora espaços, tabulações e quebras de linha.
            if c in SEPARADORES:
                cursor.avancar()
                continue

            # Ignora comentários de linha iniciados por //.
            # A quebra de linha não é consumida neste bloco:
            # ela será processada normalmente como separador.
            if self._texto.startswith("//", cursor.pos):
                while not cursor.fim() and cursor.peek() != '\n':
                    cursor.avancar()
                continue

            # Reconhecimento dos demais elementos léxicos.
            item = reconhecer_qualquer(
                cursor,
                self._palavras_reservadas
            )

            if item is None:
                ini = cursor.salvar()
                cursor.avancar()
                ch = cursor.texto[ini[0]:cursor.pos]

                erros.append(
                    ErroLexico(
                        ch,
                        ini[1],
                        ini[2],
                        f"caractere fora do alfabeto: {ch!r}"
                    )
                )

            elif isinstance(item, Token):
                tokens.append(item)

            else:
                erros.append(item)

        if incluir_eof:
            fim = cursor.salvar()
            tokens.append(
                Token(
                    Categoria.EOF,
                    "",
                    fim[1],
                    fim[2]
                )
            )

        return tokens, erros
