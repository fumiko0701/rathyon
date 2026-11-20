"""Testes do Parser integrados ao Scanner oficial da Rathyon."""
import unittest

from src.parser import (
    Parser,
    RathyonLexicalError,
    RathyonSyntaxError,
    parse,
    parse_tokens,
)
from src.lexer import Scanner


class TestParser(unittest.TestCase):
    def test_declaracao_inteiro(self):
        ast = parse("queijo idade = 18;")
        declaration = ast["body"][0]
        self.assertEqual(declaration["type"], "Declaration")
        self.assertEqual(declaration["data_type"], "queijo")
        self.assertEqual(declaration["name"], "idade")
        self.assertEqual(declaration["value"]["value"], 18)

    def test_atribuicao(self):
        ast = parse("idade = idade + 1;")
        assignment = ast["body"][0]
        self.assertEqual(assignment["type"], "Assignment")
        self.assertEqual(assignment["value"]["type"], "Binary")
        self.assertEqual(assignment["value"]["operator"], "+")

    def test_precedencia(self):
        ast = parse("guinchar(2 + 3 * 4);")
        call = ast["body"][0]["expression"]
        addition = call["arguments"][0]
        self.assertEqual(addition["operator"], "+")
        self.assertEqual(addition["right"]["operator"], "*")

    def test_condicional_com_senao(self):
        ast = parse("farejar cheio { guinchar(1); } fujir { guinchar(0); }")
        statement = ast["body"][0]
        self.assertEqual(statement["type"], "If")
        self.assertIsNotNone(statement["otherwise"])

    def test_laco_e_break(self):
        ast = parse("roer cheio { escapar; }")
        self.assertEqual(ast["body"][0]["type"], "While")
        self.assertEqual(ast["body"][0]["body"]["body"][0]["type"], "Break")

    def test_for_com_trilha(self):
        ast = parse("vasculhar i dentro trilha(3) { guinchar(i); }")
        statement = ast["body"][0]
        self.assertEqual(statement["type"], "For")
        self.assertEqual(statement["variable"], "i")
        self.assertEqual(statement["iterable"]["type"], "Call")

    def test_chamadas_de_conversao_queijo_e_migalha(self):
        ast = parse("guinchar(queijo(3.9)); guinchar(migalha(5));")
        first_call = ast["body"][0]["expression"]["arguments"][0]
        second_call = ast["body"][1]["expression"]["arguments"][0]
        self.assertEqual(first_call["type"], "Call")
        self.assertEqual(first_call["callee"]["name"], "queijo")
        self.assertEqual(second_call["callee"]["name"], "migalha")

    def test_funcao_e_retorno(self):
        ast = parse("cavar soma(a, b) { voltar a + b; }")
        function = ast["body"][0]
        self.assertEqual(function["type"], "Function")
        self.assertEqual(function["params"], ["a", "b"])
        self.assertEqual(function["body"]["body"][0]["type"], "Return")

    def test_evento_e_sinalizar(self):
        ast = parse("ouvir clique(x) { guinchar(x); } sinalizar clique(1);")
        self.assertEqual(ast["body"][0]["type"], "EventHandler")
        self.assertEqual(ast["body"][1]["type"], "Emit")

    def test_escapar_fora_de_laco_rejeitado(self):
        with self.assertRaises(RathyonSyntaxError):
            parse("escapar;")

    def test_voltar_fora_de_funcao_rejeitado(self):
        with self.assertRaises(RathyonSyntaxError):
            parse("voltar;")

    def test_parametro_duplicado_rejeitado(self):
        with self.assertRaises(RathyonSyntaxError):
            parse("cavar soma(a, a) { voltar a; }")

    def test_erro_lexico_e_reportado(self):
        with self.assertRaises(RathyonLexicalError):
            parse("queijo x = @;")

    def test_string_nao_suportada_pelo_lexer_atual(self):
        # Strings estão fora da especificação léxica atual; não devem ser
        # silenciosamente aceitas pelo Parser.
        with self.assertRaises(RathyonLexicalError):
            parse('guinchar("oi");')

    def test_parse_tokens_usa_tokens_do_scanner(self):
        tokens, errors = Scanner("queijo x;").scan(incluir_eof=True)
        self.assertEqual(errors, [])
        ast = parse_tokens(tokens)
        self.assertEqual(ast["body"][0]["name"], "x")


if __name__ == "__main__":
    unittest.main()
