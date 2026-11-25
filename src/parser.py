"""src/Parser sintático experimental da Rathyon (AST, sem execução).

O Parser consome exclusivamente os tokens oficiais produzidos por Scanner.
A estrutura da AST (dicionários com a chave ``type``) preserva o formato do
parser experimental original do projeto.

Sintaxe implementada conforme a proposta recebida:
- blocos delimitados por { };
- instruções simples terminadas em ;;
- condicionais: farejar / refarejar / fujir;
- laços: roer e vasculhar ... dentro ...;
- funções: cavar nome(parametros) { ... };
- eventos: ouvir nome(parametros) { ... } e sinalizar nome(argumentos);.

Strings e comentários ainda não são aceitos pelo Scanner oficial, pois não
fazem parte da especificação léxica atual. A gramática sintática completa
continua sendo uma proposta e depende de validação do grupo.
"""
from __future__ import annotations

import json
import sys
from typing import Iterable, Sequence

from .lexer import Scanner
from .tokens import Categoria, ErroLexico, Token


class RathyonSyntaxError(SyntaxError):
    """Erro sintático com posição de linha e coluna."""


class RathyonLexicalError(Exception):
    """Um ou mais erros foram encontrados antes da análise sintática."""


def node(kind: str, **kwargs):
    """Cria um nó da AST mantendo o formato do parser experimental original."""
    return {"type": kind, **kwargs}


def _categoria(token: Token) -> str:
    categoria = token.categoria
    return categoria.value if hasattr(categoria, "value") else str(categoria)


class Parser:
    # Precedência: comparação < adição/subtração < multiplicação/divisão.
    PRECEDENCE = {
        "==": 1, "!=": 1, "<": 2, "<=": 2, ">": 2, ">=": 2,
        "+": 3, "-": 3, "*": 4, "/": 4,
    }

    def __init__(self, tokens: Sequence[Token]):
        self.tokens = list(tokens)
        self.pos = 0
        self.loop_depth = 0
        self.function_depth = 0
        if not self.tokens or _categoria(self.tokens[-1]) != "EOF":
            if self.tokens:
                last = self.tokens[-1]
                linha, coluna = last.linha, last.coluna + len(last.lexema)
            else:
                linha, coluna = 1, 1
            self.tokens.append(Token(Categoria.EOF, "", linha, coluna))

    def current(self) -> Token:
        return self.tokens[self.pos]

    def at(self, value: str) -> bool:
        return self.current().lexema == value

    def accept(self, value: str) -> bool:
        if self.at(value):
            self.pos += 1
            return True
        return False

    def expect(self, value: str) -> None:
        if not self.accept(value):
            self.error(f"Esperado {value!r}")

    def error(self, message: str):
        token = self.current()
        encontrado = repr(token.lexema) if token.lexema else "fim do arquivo"
        raise RathyonSyntaxError(
            f"{message}; encontrado {encontrado} na linha {token.linha}, "
            f"coluna {token.coluna}"
        )

    def identifier(self) -> str:
        token = self.current()
        if _categoria(token) != "IDENTIFIER":
            self.error("Esperado identificador")
        self.pos += 1
        return token.lexema

    def program(self):
        body = []
        while _categoria(self.current()) != "EOF":
            body.append(self.statement())
        return node("Program", body=body)

    def block(self):
        self.expect("{")
        body = []
        while not self.at("}"):
            if _categoria(self.current()) == "EOF":
                self.error("Bloco não fechado; esperado '}'")
            body.append(self.statement())
        self.expect("}")
        return node("Block", body=body)

    def statement(self):
        if _categoria(self.current()) == "REGION_START":
            name = self.current().lexema
            self.pos += 1
            body = []
            while _categoria(self.current()) not in ("REGION_END", "EOF"):
                body.append(self.statement())
            if _categoria(self.current()) != "REGION_END":
                self.error("Esperado '#toca'")
            self.pos += 1
            return node("Region", name=name, body=body)

        if _categoria(self.current()) == "GOTO_REGION":
            name = self.current().lexema
            self.pos += 1
            return node("GotoRegion", name=name)

        if self.at("farejar"):
            return self.conditional()

        if self.accept("roer"):
            condition = self.expression()
            self.loop_depth += 1
            try:
                body = self.block()
            finally:
                self.loop_depth -= 1
            return node("While", condition=condition, body=body)

        if self.accept("vasculhar"):
            variable = self.identifier()
            self.expect("dentro")
            iterable = self.expression()
            self.loop_depth += 1
            try:
                body = self.block()
            finally:
                self.loop_depth -= 1
            return node("For", variable=variable, iterable=iterable, body=body)

        if self.accept("cavar"):
            name = self.identifier()
            params = self.parameters()
            self.function_depth += 1
            try:
                body = self.block()
            finally:
                self.function_depth -= 1
            return node("Function", name=name, params=params, body=body)

        if self.accept("ouvir"):
            name = self.identifier()
            params = self.parameters()
            return node("EventHandler", name=name, params=params, body=self.block())

        if self.accept("sinalizar"):
            name = self.identifier()
            args = self.arguments()
            self.expect(";")
            return node("Emit", name=name, arguments=args)

        if self.at("queijo") or self.at("migalha"):
            data_type = self.current().lexema
            self.pos += 1
            name = self.identifier()
            initial = self.expression() if self.accept("=") else None
            self.expect(";")
            return node("Declaration", data_type=data_type, name=name, value=initial)

        if self.accept("voltar"):
            if not self.function_depth:
                self.error("voltar só pode ser usado dentro de função")
            value = None if self.at(";") else self.expression()
            self.expect(";")
            return node("Return", value=value)

        if self.accept("escapar"):
            if not self.loop_depth:
                self.error("escapar só pode ser usado dentro de laço")
            self.expect(";")
            return node("Break")

        # A atribuição é reconhecida pela categoria oficial ASSIGNMENT.
        if (_categoria(self.current()) == "IDENTIFIER"
                and _categoria(self.tokens[self.pos + 1]) == "ASSIGNMENT"):
            name = self.identifier()
            self.expect("=")
            value = self.expression()
            self.expect(";")
            return node("Assignment", name=name, value=value)

        value = self.expression()
        self.expect(";")
        return node("ExpressionStatement", expression=value)

    def conditional(self):
        self.expect("farejar")
        branches = [{"condition": self.expression(), "body": self.block()}]
        while self.accept("refarejar"):
            branches.append({"condition": self.expression(), "body": self.block()})
        otherwise = self.block() if self.accept("fujir") else None
        return node("If", branches=branches, otherwise=otherwise)

    def parameters(self) -> list[str]:
        self.expect("(")
        names = []
        if not self.at(")"):
            names.append(self.identifier())
            while self.accept(","):
                names.append(self.identifier())
        self.expect(")")
        if len(names) != len(set(names)):
            self.error("Parâmetro duplicado")
        return names

    def arguments(self) -> list:
        self.expect("(")
        args = []
        if not self.at(")"):
            args.append(self.expression())
            while self.accept(","):
                args.append(self.expression())
        self.expect(")")
        return args

    def expression(self, minimum: int = 0):
        left = self.primary()
        while True:
            operator = self.current().lexema
            precedence = self.PRECEDENCE.get(operator, -1)
            if precedence < minimum:
                break
            self.pos += 1
            right = self.expression(precedence + 1)
            left = node("Binary", operator=operator, left=left, right=right)
        return left

    def primary(self):
        token = self.current()
        category = _categoria(token)

        if self.accept("-"):
            return node("Unary", operator="-", operand=self.expression(5))

        if self.accept("("):
            result = self.expression()
            self.expect(")")
            return result

        if category == "INTEGER":
            self.pos += 1
            return node("Literal", value=int(token.lexema))

        if category == "FLOAT":
            self.pos += 1
            return node("Literal", value=float(token.lexema))

        # Mantém compatibilidade futura caso o Lexer passe a emitir STRING.
        if category == "STRING":
            self.pos += 1
            return node("String", raw=token.lexema)

        if self.accept("cheio"):
            return node("Literal", value=True)
        if self.accept("vazio"):
            return node("Literal", value=False)

        if category == "IDENTIFIER" or token.lexema in {"guinchar", "trilha", "queijo", "migalha"}:
            name = token.lexema
            self.pos += 1
            expression = node("Identifier", name=name)
            while self.at("("):
                expression = node("Call", callee=expression, arguments=self.arguments())
            return expression

        self.error("Esperada expressão")


def parse_tokens(tokens: Sequence[Token]):
    """Analisa tokens já produzidos pelo Scanner e devolve a AST."""
    return Parser(tokens).program()


def parse(source: str):
    """Executa Scanner e Parser; rejeita o código se houver erro léxico."""
    tokens, errors = Scanner(source).scan(incluir_eof=True)
    if errors:
        details = "; ".join(
            f"{error.mensagem} ({error.lexema!r}) na linha {error.linha}, coluna {error.coluna}"
            for error in errors
        )
        raise RathyonLexicalError(details)
    return parse_tokens(tokens)


def main(argv: Iterable[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) != 1:
        print("Uso: python -m src.parser <arquivo.ra>", file=sys.stderr)
        return 1
    try:
        with open(args[0], encoding="utf-8") as source_file:
            ast = parse(source_file.read())
        print(json.dumps(ast, ensure_ascii=False, indent=2))
        return 0
    except OSError as exc:
        print(f"Erro ao abrir arquivo: {exc}", file=sys.stderr)
        return 1
    except (RathyonSyntaxError, RathyonLexicalError) as exc:
        print(f"Erro: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
