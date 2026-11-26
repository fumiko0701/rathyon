import unittest

from rathyon import RathyonConsole, carregar_traducao
from src.executor import Executor
from src.parser import RathyonSyntaxError, parse


class TestSintaxes(unittest.TestCase):
    def test_escrita_em_ninho_aninhado(self):
        programa = """
            ninho matriz = [[[1, 2]], [[3, 4]]];
            ninho linha = matriz[1][0];
            ninho ordem = [];
            cavar queijo marcar(queijo i) { ordem = ordem + [i]; voltar i; }
            matriz[marcar(1)][marcar(0)][marcar(-1)] = marcar(7);
        """
        estado = Executor().rodar(parse(programa))
        self.assertEqual(estado["matriz"], [[[1, 2]], [[3, 7]]])
        self.assertEqual(estado["linha"], [3, 7])
        self.assertEqual(estado["ordem"], [1, 0, -1, 7])

    def test_indice_inteiro_em_cada_nivel(self):
        for alvo in ("matriz[cheio][0]", "matriz[0][0.5]"):
            with self.subTest(alvo=alvo):
                executor = Executor()
                with self.assertRaisesRegex(RuntimeError, "índice de uma lista deve ser inteiro"):
                    executor.rodar(parse(f"ninho matriz = [[1]]; {alvo} = 7;"))
                self.assertEqual(executor.globals["matriz"], [[1]])

    def test_console_preserva_palavras_entre_aspas(self):
        console = RathyonConsole(carregar_traducao())
        self.assertTrue(console.push("dados = ninho(("))
        self.assertTrue(console.push('    "chiado", "ninho", "procure", queijo(2.5)'))
        self.assertFalse(console.push("))"))
        self.assertEqual(console.locals["dados"], ["chiado", "ninho", "procure", 2])

    def test_seguir_exige_laco_da_propria_funcao_ou_evento(self):
        for laco in ("roer cheio", "vasculhar i dentro [1]"):
            for rotina in ("cavar f()", "ouvir evento()"):
                with self.subTest(laco=laco, rotina=rotina):
                    with self.assertRaisesRegex(RathyonSyntaxError, "seguir"):
                        parse(f"{laco} {{ {rotina} {{ seguir; }} }}")

    def test_funcao_com_laco_proprio(self):
        programa = """
            procure math;
            ninho resultados = [];
            vasculhar i dentro [1, 2] {
                cavar queijo buscar(ninho valores) {
                    vasculhar v dentro valores {
                        farejar v == 0 { seguir; }
                        cace v {
                            presa 9 { voltar queijo(math.sqrt(v)); }
                            fujir { voltar v; }
                        }
                    }
                    voltar 0;
                }
                farejar i == 1 { seguir; }
                resultados = [buscar([0, 9]), buscar([4]), buscar([])];
            }
        """
        self.assertEqual(Executor().rodar(parse(programa))["resultados"], [3, 4, 0])

    def test_parametro_e_retorno_dos_cinco_tipos(self):
        valores = {"queijo": ("1", 1), "migalha": ("1.0", 1.0), "barriga": ("cheio", True),
                   "chiado": ('"eae"', "eae"), "ninho": ("[1]", [1])}
        for tipo in valores:
            for assinatura in (f"eco({tipo} x)", f"{tipo} eco(x)"):
                for recebido, (literal, valor) in valores.items():
                    with self.subTest(assinatura=assinatura, recebido=recebido):
                        ast = parse(f"cavar {assinatura} {{ voltar x; }} "
                                    f"entrada = {literal}; resposta = eco(entrada);")
                        if recebido == tipo:
                            resposta = Executor().rodar(ast)["resposta"]
                            self.assertIs(type(resposta), type(valor))
                            self.assertEqual(resposta, valor)
                        else:
                            with self.assertRaisesRegex(RuntimeError, f"esperado {tipo}"):
                                Executor().rodar(ast)
