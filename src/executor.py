"""src/executor.py — Executa a AST produzida pelo Parser."""

from __future__ import annotations

import operator
from contextlib import contextmanager


class _Break(Exception):
    pass


class _Return(Exception):
    def __init__(self, value):
        self.value = value


class Executor:
    _BIN_OPS = {
        "+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.truediv,
        "==": operator.eq, "!=": operator.ne,
        "<": operator.lt, "<=": operator.le, ">": operator.gt, ">=": operator.ge,
    }
    # Operadores binários mapeados para funções do módulo operator.

    _SENTINEL = object()
    # Valor sentinela: distingue "variável não existia" de "variável era None".

    def __init__(self):
        self.globals = {
            "__name__": "__main__",
            "guinchar": print,
            "queijo": int,
            "migalha": float,
            "trilha": range,
        }
        self.eventos = {}
        self.fired_gotos = set()   # ids de nós GotoRegion já disparados

    def rodar(self, ast):
        self.exec_node(ast)
        # dispara eventos emitidos antes de ouvir? não — só sinalizar dentro de handler
        return self.globals

    def exec_node(self, n):
        """Despacha para o método _exec_<tipo> correspondente ao tipo do nó."""
        handler = getattr(self, f"_exec_{n['type']}", None)
        if handler is None:
            raise RuntimeError(f"Nó desconhecido: {n['type']}")
        handler(n)
    # ---- comandos ----
    def _exec_Program(self, n):
        self._exec_program(n["body"])

    def _exec_Block(self, n):
        self._exec_block_with_regions(n["body"])

    def _exec_Region(self, n):
        self._exec_block_with_regions(n["body"])

    def _exec_GotoRegion(self, n):
        raise RuntimeError("GotoRegion só pode aparecer dentro de um bloco executável")

    def _exec_Declaration(self, n):
        val = self.eval(n["value"]) if n["value"] else (
            0 if n["data_type"] == "queijo" else 0.0)
        if n["data_type"] == "queijo":
            val = int(val)
        elif n["data_type"] == "migalha":
            val = float(val)
        self.globals[n["name"]] = val

    def _exec_Assignment(self, n):
        self.globals[n["name"]] = self.eval(n["value"])

    def _exec_If(self, n):
        for ramo in n["branches"]:
            if self.eval(ramo["condition"]):
                self.exec_node(ramo["body"])
                return
        if n["otherwise"]:
            self.exec_node(n["otherwise"])

    def _exec_While(self, n):
        while self.eval(n["condition"]):
            try:
                self.exec_node(n["body"])
            except _Break:
                break

    def _exec_For(self, n):
        for item in self.eval(n["iterable"]):
            self.globals[n["variable"]] = item
            try:
                self.exec_node(n["body"])
            except _Break:
                break

    def _exec_Function(self, n):
        """Cria a função com escopo temporário de parâmetros (restaura globals ao sair)."""
        def _fn(*args, _p=n["params"], _b=n["body"]):
            with self._escopo(dict(zip(_p, args))):
                try:
                    self.exec_node(_b)
                except _Return as r:
                    return r.value
            return None
        self.globals[n["name"]] = _fn

    def _exec_EventHandler(self, n):
        self.eventos[n["name"]] = (n["params"], n["body"])

    def _exec_Emit(self, n):
        self.disparar(n["name"], [self.eval(a) for a in n["arguments"]])

    def _exec_Return(self, n):
        raise _Return(self.eval(n["value"]) if n["value"] else None)

    def _exec_Break(self, n):
        raise _Break()

    def _exec_ExpressionStatement(self, n):
        self.eval(n["expression"])
    # ---- regiões e #vaparatunel ----
    def _montar_region_map(self, statements):
        """Mapeia o nome de cada região para seu índice na lista de comandos."""
        return {s["name"]: i for i, s in enumerate(statements)
                if s["type"] == "Region"}

    def _processar_goto(self, stmt, region_map, reservados=frozenset()):
        """Retorna o índice alvo de um #vaparatunel, ou None se já foi disparado."""
        if id(stmt) in self.fired_gotos:
            return None
        nome = stmt["name"]
        if nome in reservados:
            raise RuntimeError(
                f"#vaparatunel '{nome}': '{nome}' é reservado")
        if nome not in region_map:
            raise RuntimeError(
                f"#vaparatunel '{nome}': região não encontrada neste bloco")
        self.fired_gotos.add(id(stmt))
        return region_map[nome]

    def _executar_sequencia(self, statements, region_map, pular=frozenset(), reservados=frozenset()):
        """Executa os comandos em ordem, com suporte a saltos #vaparatunel.

        pular: índices a ignorar (usado para entrada/saída no programa).
        reservados: nomes de região que não podem ser alvo do salto.
        """
        i = 0
        while i < len(statements):
            if i in pular:
                i += 1
                continue
            stmt = statements[i]
            if stmt["type"] == "GotoRegion":
                alvo = self._processar_goto(stmt, region_map, reservados)
                if alvo is None:
                    i += 1
                else:
                    i = alvo
                continue
            self.exec_node(stmt)
            i += 1

    def _exec_program(self, statements):
        """Executa o programa. #tunel entrada roda primeiro, #tunel saida por último.

        O posicionamento dessas regiões no arquivo é irrelevante: são encontradas
        pelo nome 'entrada' / 'saida' em qualquer índice. Se não existirem, nada muda.
        """
        region_map = self._montar_region_map(statements)
        start_idx = region_map.get("entrada", -1)
        end_idx = region_map.get("saida", -1)

        if start_idx >= 0:
            self.exec_node(statements[start_idx])

        self._executar_sequencia(
            statements, region_map,
            pular={start_idx, end_idx}, reservados={"entrada", "saida"})

        if end_idx >= 0:
            self.exec_node(statements[end_idx])

    def _exec_block_with_regions(self, statements):
        """Executa uma lista de comandos com PC e suporte a #vaparatunel."""
        region_map = self._montar_region_map(statements)
        self._executar_sequencia(statements, region_map)

    # ---- eventos ----
    @contextmanager
    def _escopo(self, bindings):
        """Executa com bindings temporários em globals; restaura ao sair."""
        backup = {}
        for k, v in bindings.items():
            backup[k] = self.globals.get(k, self._SENTINEL)
            self.globals[k] = v
        try:
            yield
        finally:
            for k, antigo in backup.items():
                if antigo is self._SENTINEL:
                    self.globals.pop(k, None)
                else:
                    self.globals[k] = antigo

    def disparar(self, nome, args):
        """Executa o handler do evento com os parâmetros fornecidos."""
        if nome not in self.eventos:
            return  # ou erro, depende da semântica desejada
        params, body = self.eventos[nome]
        with self._escopo(dict(zip(params, args))):
            self.exec_node(body)

    # ---- expressões ----
    def eval(self, n):
        """Despacha para o método _eval_<tipo> correspondente ao tipo da expressão."""
        handler = getattr(self, f"_eval_{n['type']}", None)
        if handler is None:
            raise RuntimeError(f"Expressão desconhecida: {n['type']}")
        return handler(n)

    def _eval_Literal(self, n):
        return n["value"]

    def _eval_Identifier(self, n):
        if n["name"] not in self.globals:
            raise RuntimeError(f"Variável não definida: {n['name']}")
        return self.globals[n["name"]]

    def _eval_Binary(self, n):
        a = self.eval(n["left"])
        b = self.eval(n["right"])
        try:
            return self._BIN_OPS[n["operator"]](a, b)
        except KeyError:
            raise RuntimeError(f"Operador desconhecido: {n['operator']}")

    def _eval_Unary(self, n):
        v = self.eval(n["operand"])
        return -v if n["operator"] == "-" else v

    def _eval_Call(self, n):
        f = self.eval(n["callee"])
        args = [self.eval(a) for a in n["arguments"]]
        return f(*args)


