# Importa a classe que queremos testar do diretório src
import pytest
from POO.Dice import Dice

#(notação, min_esperado, max_esperado)
CASOS_DE_TESTE = [
    ("1d6", 1, 6),
    ("2d8+2", 4, 18),
    ("3d10-1", 2, 29),
    ("#2d20", 1, 20) # Vantagem não muda min/max
]

# Teste 1: Verifica a criação de um dado simples e seus limites
def test_criacao_dado_simples():
    # 1. Arrange
    d6 = Dice(6)

    # 2. Act (A ação já foi a criação, agora vamos verificar os atributos)
    min_val = d6.min_result()
    max_val = d6.max_result()

    # 3. Assert
    assert d6.notation == "1d6"
    assert min_val == 1
    assert max_val == 6

# Teste 2: Verifica a análise de uma notação mais complexa
def test_notacao_complexa_min_max():
    # Arrange
    dado_ataque = Dice("2d8+5")

    # Act
    min_val = dado_ataque.min_result()
    max_val = dado_ataque.max_result()

    # Assert
    assert min_val == 7  # (1 * 2) + 5
    assert max_val == 21 # (8 * 2) + 5

# Teste 3: Verifica o que acontece com uma notação inválida
def test_notacao_invalida_lanca_erro():
    # Arrange: Importa a classe de exceção do pytest

    # Act & Assert: Verifica se o código DENTRO do 'with' lança um ValueError
    with pytest.raises(ValueError):
        Dice("isso nao e um dado")

@pytest.mark.parametrize("notacao, min_esperado, max_esperado", CASOS_DE_TESTE)
def test_multiplas_notacoes(notacao, min_esperado, max_esperado):
    dado = Dice(notacao)
    assert dado.min_result() == min_esperado
    assert dado.max_result() == max_esperado