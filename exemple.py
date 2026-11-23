# exemple.py
import argparse
import ast
import tokenize


class Regioes(dict):
    def __init__(self, nome_arquivo, funcoes):
        super().__init__(__name__="__main__", __file__=nome_arquivo)
        self.funcoes = funcoes
        self.carregando = set()

    def __missing__(self, nome):
        codigo = self.funcoes.get(nome)
        if codigo is None:
            raise KeyError(nome)

        if nome in self.carregando:
            raise RuntimeError(f"Dependência circular ao definir {nome!r}")

        self.carregando.add(nome)
        try:
            exec(codigo, self)
            return self[nome]
        finally:
            self.carregando.remove(nome)


def executar(nome_arquivo):
    with tokenize.open(nome_arquivo) as arquivo:
        fonte = arquivo.read()

    arvore = ast.parse(fonte, filename=nome_arquivo)
    definicoes = {}
    comandos = []
    imports_futuros = []

    for instrucao in arvore.body:
        if isinstance(instrucao, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if instrucao.name in definicoes:
                raise ValueError(f"Função declarada duas vezes: {instrucao.name}")
            definicoes[instrucao.name] = instrucao
        else:
            comandos.append(instrucao)
            if (
                isinstance(instrucao, ast.ImportFrom)
                and instrucao.module == "__future__"
                and instrucao.level == 0
            ):
                imports_futuros.append(instrucao)

    funcoes = {}
    for nome, definicao in definicoes.items():
        regiao = ast.Module(
            body=[*imports_futuros, definicao],
            type_ignores=[],
        )
        funcoes[nome] = compile(regiao, nome_arquivo, "exec", dont_inherit=True)

    programa = ast.Module(body=comandos, type_ignores=arvore.type_ignores)
    codigo = compile(programa, nome_arquivo, "exec", dont_inherit=True)
    exec(codigo, Regioes(nome_arquivo, funcoes))


if __name__ == "__main__":
    cli = argparse.ArgumentParser()
    cli.add_argument("arquivo", help="Arquivo Python com as funções")
    executar(cli.parse_args().arquivo)