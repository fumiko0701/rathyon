"""Testes de integração das diretivas de região do Rathyon."""
import io
import unittest
from contextlib import redirect_stdout

from src.executor import Executor
from src.parser import parse


class TestRegioes(unittest.TestCase):
    def test_salto_para_regiao_com_nova_diretiva(self):
        codigo = (
            "#tunel entrada\n"
            "guinchar(1);\n"
            "#toca\n"
            "#vaparatunel etapa\n"
            "#tunel etapa\n"
            "guinchar(2);\n"
            "#toca\n"
            "#tunel saida\n"
            "guinchar(3);\n"
            "#toca\n"
        )
        saida = io.StringIO()
        with redirect_stdout(saida):
            Executor().rodar(parse(codigo))

        self.assertEqual(saida.getvalue(), "1\n2\n3\n")


if __name__ == "__main__":
    unittest.main()
