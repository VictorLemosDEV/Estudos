import re
from typing import Union, TypeAlias, Dict
from random import randint


DiceParts: TypeAlias = Dict[str, int]


class Dice:
    """
    Representa um ou mais dados, capazes de rolar com a notação padrão de RPG (ex: '2d8+3').
    """

    # Ex: #2d8+3 -> advantage=True, times=2, sides=8, bonus=3
    DICE_NOTATION_PATTERN = re.compile(
        r"^(?P<advantage>#)?"       # (Opcional) Vantagem (#)
        r"(?P<times>\d+)?"          # (Opcional) Número de dados
        r"d"                        # O 'd' separador literal
        r"(?P<sides>\d+)"           # Número de lados do dado
        r"([+-](?P<bonus>\d+))?$"   # (Opcional) Bônus com sinal
    )

    def __init__(self, notation: Union[int,str]):
        """
        Cria um dado a partir de um número de lados (int) ou notação de RPG (str).
        
        Args:
            notation: Um inteiro (ex: 6) ou uma string (ex: '2d10+5', '#1d20+2').
        
        Raises:
            ValueError: Se a notação for inválida.
        """
        if isinstance(notation, int):
            if notation <= 0:
                raise ValueError("O número de lados deve ser positivo.")
            self.notation = f"1d{notation}"
        else:
            self.notation = notation.replace(" ", "").lower()

        self.parts = self._evaluate_notation(self.notation)
        if not self.parts:
            raise ValueError(f"Notação de dado inválida: '{self.notation}'")


        

    
    @staticmethod
    def _evaluate_notation(notation: str) -> Union[DiceParts, None]:
        """Analisa a string de notação de dado usando regex."""
        
        match = Dice.DICE_NOTATION_PATTERN.match(notation)
        if not match:
            return None
        
        parts = match.groupdict()

        return {
            "times": int(parts["times"] or 1),
            "sides": int (parts["sides"]),
            "bonus": int (parts["bonus"] or 0) * (1 if notation.find("+") != -1 else -1),
            "advantage": 1 if parts["advantage"] else 0
        }
    
    def roll(self) -> int:
        """
        Executa a rolagem do dado de acordo com sua notação.
        
        Returns:
            O resultado final da rolagem.
        """

        if not self.parts:
            raise ValueError(f"Notação de dado inválida: '{self.notation}'")

        times = self.parts["times"]
        sides = self.parts["sides"]
        bonus = self.parts["bonus"]
        advantage = self.parts["advantage"]

        rolls = [randint(1, sides) for _ in range(times)]

        if advantage:
            # Pega o maior resultado se for uma rolagem com vantagem
            return max(rolls) + bonus
        else:
            # Soma todos os resultados
            return sum(rolls) + bonus
        
    
    # --- Métodos mágicos ---

    def __call__(self) -> int:
        """Permite chamar o objeto como uma função para rolar o dado. Ex: d20()"""
        return self.roll()
    
    def __str__(self) -> str:
        """Representação amigável para o usuário. Ex: print(d20)"""
        return self.notation
    
    def __repr__(self) -> str:
        """Representação para o dev, que pode recriar o objeto."""
        return f"Dice('{self.notation}')"
    
    def __add__(self, bonus: int):
        """Permite adicionar um bônus à notação. Ex: Dado('1d20') + 5"""
        if isinstance(bonus, int):
            if self.parts is None:
                return ValueError(f"Notação de dado inválida: '{self.notation}'")

            new_bonus = self.parts["bonus"] + bonus
            sign = "+" if new_bonus >= 0 else ""
            return Dice(f"{self.parts["times"]}d{self.parts["sides"]}{sign}{new_bonus}")
        return NotImplemented
    


# --- Exemplo de Uso ---
if __name__ == "__main__":
    d6 = Dice(6)
    print(f"Rolando um d6: {d6.roll()}")

    print(f"Rolando um d6 (com __call__): {d6()}")

    ataque_espada = Dice("2d8+5")
    print(f"Representação do dado: {ataque_espada}") # __str__
    print(f"Dano do ataque com {ataque_espada}: {ataque_espada()}")

    teste_habilidade = Dice("#2d20+2")
    print(f"Teste de habilidade com vantagem ({teste_habilidade}): {teste_habilidade()}")

    d20_com_magia = Dice("1d20") + 4
    print(f"Um d20 com bônus mágico ({d20_com_magia}): {d20_com_magia()}")
        

    

        
        




