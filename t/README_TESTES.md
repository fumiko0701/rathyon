# Testes manuais da Rathyon

Os arquivos `.ra` desta pasta exercitam o interpretador atual (Scanner → Parser → Executor).
Execute os testes de sucesso a partir da raiz do repositório:

```powershell
python rathyon.py t/teste.ra
python rathyon.py t/teste_scanner.ra
python rathyon.py t/teste_parser.ra
python rathyon.py t/teste_operadores.ra
python rathyon.py t/teste_condicionais.ra
python rathyon.py t/teste_lacos.ra
python rathyon.py t/teste_funcoes.ra
python rathyon.py t/teste_listas.ra
python rathyon.py t/teste_selecao.ra
python rathyon.py t/teste_eventos.ra
python rathyon.py t/teste_importacoes.ra
python rathyon.py t/teste_regioes.ra
python rathyon.py t/testezao_region.ra
python rathyon.py t/teste_completo.ra
```

Cada um desses programas deve terminar com código de saída `0` e sem mensagem de erro.
Os resultados impressos são parte da verificação: confira se correspondem às operações
e aos caminhos de execução descritos no próprio teste.

## Testes que devem falhar de propósito

Estes arquivos são casos negativos. O comportamento esperado é encerrar com código
de saída diferente de `0` e apresentar a categoria de erro indicada:

| Arquivo | O que verifica | Resultado esperado |
| --- | --- | --- |
| `teste_erros.ra` | Caracteres inválidos, `!` isolado e número malformado `123abc` | Erro léxico |
| `teste_erros_sintaticos.ra` | Expressão incompleta em uma declaração | Erro sintático |
| `teste_erros_regioes_sintaxe.ra` | Região sem `#toca` de fechamento | Erro sintático |
| `teste_erros_execucao.ra` | Uso de variável não definida | Erro durante execução |
| `teste_erros_tipos.ra` | Argumento incompatível com parâmetro tipado | Erro de tipo durante execução |
| `teste_erros_regioes.ra` | Salto para região inexistente | Erro durante execução |
| `teste_erros_regioes_reservadas.ra` | Tentativa de saltar para a região reservada `entrada` | Erro durante execução |

Execute os casos negativos individualmente, pois a falha é intencional:

```powershell
python rathyon.py t/teste_erros.ra
python rathyon.py t/teste_erros_sintaticos.ra
python rathyon.py t/teste_erros_regioes_sintaxe.ra
python rathyon.py t/teste_erros_execucao.ra
python rathyon.py t/teste_erros_tipos.ra
python rathyon.py t/teste_erros_regioes.ra
python rathyon.py t/teste_erros_regioes_reservadas.ra
```

## Cobertura por arquivo

- `teste_scanner.ra`: identificadores, palavras reservadas, inteiros, floats, strings, escapes, booleanos, listas e operadores.
- `teste_parser.ra`: declarações tipadas, atribuições, blocos, condicionais, funções, parâmetros, retornos e chamadas.
- `teste_operadores.ra`: operadores aritméticos, unário e relacionais.
- `teste_condicionais.ra`: `farejar`, `refarejar` e `fujir`.
- `teste_lacos.ra`: `roer`, `vasculhar`, `trilha`, `escapar` e `seguir`.
- `teste_funcoes.ra`: funções com e sem anotação de tipos, retorno e conversões `queijo`/`migalha`.
- `teste_listas.ra`: listas, listas aninhadas, leitura e atribuição por índice.
- `teste_selecao.ra`: seleção `cace`, alternativas `presa` e padrão `fujir`.
- `teste_eventos.ra`: declaração de handlers com `ouvir` e disparo com `sinalizar`.
- `teste_importacoes.ra`: `procure`, acesso a membro de módulo e chamada de função importada.
- `teste_regioes.ra`: `#tunel`, `#toca`, `#vaparatunel`, região comum `passagem` e execução especial de `entrada`/`saida`.
- `testezao_region.ra`: salto entre regiões aninhadas dentro de outra região, além de `entrada`/`saida`.
- `teste_completo.ra`: integração de recursos centrais em um único programa.

## Limitações que os testes respeitam

- Os testes de erro são intencionalmente inválidos e não devem ser incluídos na sequência de testes de sucesso.
- A saída exata do sistema pode variar quando funções importadas dependem de valores de ponto flutuante; compare o valor e o comportamento, não uma quantidade excessiva de casas decimais.
