"""Testes do Scanner (T08).

Cobrem os casos mínimos exigidos (identificador, inteiro, float, operador de
dois caracteres, delimitador) e as regras especiais de erro léxico previstas
em SPECIFICATIONS.md (tabela pendente: 123abc, 5., .5, 9.8.7; ! isolado;
caractere fora de Σ).
"""

import unittest

from src.lexer import Scanner
from src.tokens import Categoria, ErroLexico, Token


class TestScanner(unittest.TestCase):
    def scan(self, codigo):
        return Scanner(codigo).scan()

    def test_identificador(self):
        """Identificador simples vira IDENTIFIER."""
        tokens, erros = self.scan("contador")
        self.assertEqual(erros, [])
        self.assertEqual(tokens, [Token(Categoria.IDENTIFIER, "contador", 1, 1)])

    def test_inteiro(self):
        """Inteiro com zeros à esquerda é INTEGER (regra 4)."""
        tokens, erros = self.scan("007")
        self.assertEqual(erros, [])
        self.assertEqual(tokens[0].categoria, Categoria.INTEGER)
        self.assertEqual(tokens[0].lexema, "007")

    def test_float(self):
        """Decimal com dígitos antes e depois do ponto é FLOAT (regra 5)."""
        tokens, erros = self.scan("3.14")
        self.assertEqual(erros, [])
        self.assertEqual(tokens[0].categoria, Categoria.FLOAT)
        self.assertEqual(tokens[0].lexema, "3.14")

    def test_operador_dois_caracteres(self):
        """Operador relacional de dois chars é um único token (maximal munch, regra 7)."""
        tokens, erros = self.scan(">=")
        self.assertEqual(erros, [])
        self.assertEqual(tokens[0].categoria, Categoria.RELATIONAL_OPERATOR)
        self.assertEqual(tokens[0].lexema, ">=")

    def test_delimitador(self):
        """Ponto-e-vírgula é DELIMITER."""
        tokens, erros = self.scan(";")
        self.assertEqual(erros, [])
        self.assertEqual(tokens[0].categoria, Categoria.DELIMITER)
        self.assertEqual(tokens[0].lexema, ";")

    def test_palavra_reservada_sobre_identificador(self):
        """farejar é KEYWORD; farejares (não está em K) é IDENTIFIER (regra 2)."""
        tokens, _ = self.scan("farejar")
        self.assertEqual(tokens[0].categoria, Categoria.KEYWORD)
        tokens, _ = self.scan("farejares")
        self.assertEqual(tokens[0].categoria, Categoria.IDENTIFIER)

    def test_atribuicao_vs_relacional(self):
        """'=' é ASSIGNMENT; '>=', '<', '>' são RELATIONAL_OPERATOR (cat. pelo lexema)."""
        tokens, _ = self.scan("=")
        self.assertEqual(tokens[0].categoria, Categoria.ASSIGNMENT)
        tokens, _ = self.scan(">=")
        self.assertEqual(tokens[0].categoria, Categoria.RELATIONAL_OPERATOR)

    def test_ponto_isolado_erro(self):
        """Ponto sozinho gera ErroLexico e não token (regra 5)."""
        tokens, erros = self.scan(".")
        self.assertEqual(tokens, [])
        self.assertEqual(len(erros), 1)
        self.assertEqual(erros[0].lexema, ".")

    def test_exclamacao_isolada_erro(self):
        """'!' isolado não é token; deve ser '!=' (regra 9)."""
        tokens, erros = self.scan("!")
        self.assertEqual(tokens, [])
        self.assertEqual(len(erros), 1)
        self.assertEqual(erros[0].lexema, "!")

    def test_digitos_seguidos_de_letra_erro_unico(self):
        """'123abc' gera UM erro consumindo toda a sequência (decisão D-LEX-06)."""
        tokens, erros = self.scan("123abc")
        self.assertEqual(tokens, [])
        self.assertEqual(len(erros), 1)
        self.assertEqual(erros[0].lexema, "123abc")

    def test_ponto_apos_inteiro(self):
        """'5.' → INTEGER('5') + erro no ponto (tabela pendente)."""
        tokens, erros = self.scan("5.")
        self.assertEqual([t.categoria for t in tokens], [Categoria.INTEGER])
        self.assertEqual(tokens[0].lexema, "5")
        self.assertEqual(len(erros), 1)
        self.assertEqual(erros[0].lexema, ".")

    def test_caractere_fora_alfabeto_nao_interrompe(self):
        """'@' fora de Σ gera ErroLexico e a leitura continua (regra 9)."""
        tokens, erros = self.scan("@x@")
        self.assertEqual([t.lexema for t in tokens], ["x"])
        self.assertEqual(len(erros), 2)
        self.assertTrue(all(isinstance(e, ErroLexico) for e in erros))

    def test_eof_opcional(self):
        """incluir_eof=True anexa Token(EOF) ao final da lista."""
        tokens, _ = self.scan("x")
        self.assertEqual(len(tokens), 1)
        tokens_eof, _ = Scanner("x").scan(incluir_eof=True)
        self.assertEqual(len(tokens_eof), 2)
        self.assertEqual(tokens_eof[-1].categoria, Categoria.EOF)
        self.assertEqual(tokens_eof[-1].lexema, "")

    def test_diretivas_de_regiao_rathyon(self):
        """As diretivas novas geram as categorias oficiais de região."""
        tokens, erros = self.scan(
            "#tunel inicio\n#toca\n#vaparatunel inicio"
        )
        self.assertEqual(erros, [])
        self.assertEqual(
            [(token.categoria, token.lexema) for token in tokens],
            [
                (Categoria.REGION_START, "inicio"),
                (Categoria.REGION_END, ""),
                (Categoria.GOTO_REGION, "inicio"),
            ],
        )

    def test_diretiva_antiga_nao_e_mais_reconhecida(self):
        """A grafia antiga #region não deve continuar sendo uma diretiva."""
        tokens, erros = self.scan("#region inicio")
        self.assertTrue(erros)
        self.assertFalse(any(
            token.categoria == Categoria.REGION_START for token in tokens
        ))

    def test_posicao_linha_coluna(self):
        """Linha e coluna 1-based apontam para o primeiro caractere do lexema."""
        tokens, _ = self.scan("a\nb;")
        self.assertEqual(tokens[0].linha, 1)
        self.assertEqual(tokens[0].coluna, 1)
        self.assertEqual(tokens[1].linha, 2)
        self.assertEqual(tokens[1].coluna, 1)
        self.assertEqual(tokens[2].linha, 2)
        self.assertEqual(tokens[2].coluna, 2)


if __name__ == "__main__":
    unittest.main()
