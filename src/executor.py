"""src/executor.py — Executa a AST produzida pelo Parser."""

from __future__ import annotations

class _Break(Exception):
    pass


class _Return(Exception):
    def __init__(self, value):
        self.value = value


class Executor:
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
        t = n["type"]

        if t == "Program":
            self._exec_program(n["body"])
            return

        if t == "Block":
            self._exec_block_with_regions(n["body"])
            return

        if t == "Region":
            self._exec_block_with_regions(n["body"])
            return

        if t == "GotoRegion":
            raise RuntimeError(
                "GotoRegion só pode aparecer dentro de um bloco executável")

        if t == "Declaration":
            val = self.eval(n["value"]) if n["value"] else (
                0 if n["data_type"] == "queijo" else 0.0)
            if n["data_type"] == "queijo":
                val = int(val)
            elif n["data_type"] == "migalha":
                val = float(val)
            self.globals[n["name"]] = val
            return

        if t == "Assignment":
            self.globals[n["name"]] = self.eval(n["value"])
            return

        if t == "If":
            for ramo in n["branches"]:
                if self.eval(ramo["condition"]):
                    self.exec_node(ramo["body"])
                    return
            if n["otherwise"]:
                self.exec_node(n["otherwise"])
            return

        if t == "While":
            while self.eval(n["condition"]):
                try:
                    self.exec_node(n["body"])
                except _Break:
                    break
            return

        if t == "For":
            it = self.eval(n["iterable"])
            for item in it:
                self.globals[n["variable"]] = item
                try:
                    self.exec_node(n["body"])
                except _Break:
                    break
            return

        if t == "Function":
            params = n["params"]
            body = n["body"]
            nome = n["name"]
            def _fn(*args, _p=params, _b=body):
                locais = dict(zip(_p, args))
                backup = {k: self.globals.get(k) for k in _p}
                self.globals.update(locais)
                try:
                    self.exec_node(_b)
                except _Return as r:
                    return r.value
                finally:
                    for k, v in backup.items():
                        if v is None:
                            self.globals.pop(k, None)
                        else:
                            self.globals[k] = v
                return None
            self.globals[nome] = _fn
            return

        if t == "EventHandler":
            self.eventos[n["name"]] = (n["params"], n["body"])
            return

        if t == "Emit":
            self.disparar(n["name"], [self.eval(a) for a in n["arguments"]])
            return

        if t == "Return":
            raise _Return(self.eval(n["value"]) if n["value"] else None)

        if t == "Break":
            raise _Break()

        if t == "ExpressionStatement":
            self.eval(n["expression"])
            return

        raise RuntimeError(f"Nó desconhecido: {t}")


    def _exec_program(self, statements):
        """Executa o programa. #tunel entrada roda primeiro, #tunel saida por último.

        O posicionamento dessas regiões no arquivo é irrelevante: são encontradas
        pelo nome 'entrada' / 'saida' em qualquer índice. Se não existirem, nada muda.
        """
        start_idx = -1
        end_idx = -1
        region_map = {}
        for i, stmt in enumerate(statements):
            if stmt["type"] == "Region":
                region_map[stmt["name"]] = i
                if stmt["name"] == "entrada" and start_idx < 0:
                    start_idx = i
                elif stmt["name"] == "saida" and end_idx < 0:
                    end_idx = i

        # 1) #tunel entrada primeiro (se existir)
        if start_idx >= 0:
            self.exec_node(statements[start_idx])

        # 2) fluxo normal, pulando entrada/saida
        i = 0
        while i < len(statements):
            if i == start_idx or i == end_idx:
                i += 1
                continue
            stmt = statements[i]
            if stmt["type"] == "GotoRegion":
                if id(stmt) in self.fired_gotos:
                    i += 1
                    continue
                name = stmt["name"]
                if name in ("entrada", "saida"):
                    raise RuntimeError(
                        f"#vaparatunel '{name}': 'entrada' e 'saida' são reservadas")
                if name not in region_map:
                    raise RuntimeError(
                        f"#vaparatunel '{name}': região não encontrada neste bloco")
                self.fired_gotos.add(id(stmt))
                i = region_map[name]
                continue
            self.exec_node(stmt)
            i += 1

        # 3) #tunel saida por último (se existir)
        if end_idx >= 0:
            self.exec_node(statements[end_idx])

    def _exec_block_with_regions(self, statements):
        """Executa uma lista de comandos com PC e suporte a #vaparatunel."""
        region_map = {}
        for i, stmt in enumerate(statements):
            if stmt["type"] == "Region":
                region_map[stmt["name"]] = i

        i = 0
        while i < len(statements):
            stmt = statements[i]
            if stmt["type"] == "GotoRegion":
                if id(stmt) in self.fired_gotos:
                    i += 1
                    continue
                name = stmt["name"]
                if name not in region_map:
                    raise RuntimeError(
                        f"#vaparatunel '{name}': região não encontrada neste bloco")
                self.fired_gotos.add(id(stmt))
                i = region_map[name]
                continue
            self.exec_node(stmt)
            i += 1

    def disparar(self, nome, args):
        if nome not in self.eventos:
            return  # ou erro, depende da semântica desejada
        params, body = self.eventos[nome]
        backup = {k: self.globals.get(k) for k in params}
        self.globals.update(dict(zip(params, args)))
        try:
            self.exec_node(body)
        finally:
            for k, v in backup.items():
                if v is None:
                    self.globals.pop(k, None)
                else:
                    self.globals[k] = v

    def eval(self, n):
        t = n["type"]

        if t == "Literal":
            return n["value"]

        if t == "Identifier":
            if n["name"] not in self.globals:
                raise RuntimeError(f"Variável não definida: {n['name']}")
            return self.globals[n["name"]]

        if t == "Binary":
            a = self.eval(n["left"])
            b = self.eval(n["right"])
            op = n["operator"]
            return {
                "+": lambda: a + b, "-": lambda: a - b,
                "*": lambda: a * b, "/": lambda: a / b,
                "==": lambda: a == b, "!=": lambda: a != b,
                "<": lambda: a < b, "<=": lambda: a <= b,
                ">": lambda: a > b, ">=": lambda: a >= b,
            }[op]()

        if t == "Unary":
            v = self.eval(n["operand"])
            return -v if n["operator"] == "-" else v

        if t == "Call":
            f = self.eval(n["callee"])
            args = [self.eval(a) for a in n["arguments"]]
            return f(*args)

        raise RuntimeError(f"Expressão desconhecida: {t}")