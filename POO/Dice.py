from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Union, TypeAlias, Dict, List
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
    
    def roll(self) -> 'RollResult':
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
        main_value = max(rolls) if advantage else sum(rolls)

        return RollResult(
        total=main_value + bonus,
        rolls=rolls,
        bonus=bonus,
        dice_used=self
    )
    
    def min_result(self) -> int:
        if self.parts != None:
            if self.parts["advantage"]:
                return 1 + self.parts["bonus"]

            # A soma dos valores mínimos (1) de cada dado, mais o bônus.
            return (1 * self.parts["times"]) + self.parts["bonus"]
        else:
            raise ValueError("Dado é inválido.")
        
    def max_result(self) -> int:
        if self.parts != None:
            if self.parts["advantage"]:
                return (self.parts["sides"]) + self.parts["bonus"]
            
            return (self.parts["times"] * self.parts["sides"]) + self.parts["bonus"]
        else:
            raise ValueError("Dado é inválido.")
        

        
    
    # --- Métodos mágicos ---

    def __call__(self) -> 'RollResult':
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


@dataclass(frozen=True)
class RollResult:
    total: int
    rolls: List[int]
    bonus: int
    dice_used: Dice

    def was_critical(self) -> bool:
        """Verifica se foi um acerto crítico (20 natural em um d20)."""
        if self.dice_used.parts != None:
            return len(self.rolls) == 1 and self.rolls[0] == 20 and self.dice_used.parts["sides"] == 20
        else:
            raise ValueError(f"Dice is invalid: '{self.dice_used}'")
        
    def was_critical_failure(self) -> bool:
        """Verifica se foi uma falha crítica (1 natural em um d20)."""
        if self.dice_used.parts != None:
            return len(self.rolls) == 1 and self.rolls[0] == 1 and self.dice_used.parts["sides"] == 20
        else:
            raise ValueError(f"Dice is invalid: '{self.dice_used}'")
        
    def __str__(self) -> str:
        rolagens_str = " + ".join(map(str, self.rolls))
        bonus_str = ""
        if self.bonus > 0:
            bonus_str = f" + {self.bonus}"
        elif self.bonus < 0:
            # Garante o espaçamento correto para bônus negativos
            bonus_str = f" - {abs(self.bonus)}"
        
        return f"({rolagens_str}){bonus_str} = {self.total}"
    
    def __eq__(self, other) -> bool:
        if isinstance(other, RollResult):
            return self.total == other.total
        return self.total == other
    
    def __lt__(self, other) -> bool:
        if isinstance(other, RollResult):
            return self.total < other.total
        return self.total < other
    
    def __gt__(self,other) -> bool:
        if isinstance(other, RollResult):
            return self.total > other.total
        return self.total > other
    
    def __le__(self, other) -> bool:
        if isinstance(other, RollResult):
            return self.total <= other.total
        return self.total <= other
    
    def __ge__(self, other) -> bool:
        if isinstance(other, RollResult):
            return self.total >= other.total
        return self.total >= other
      


       



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

    ataque = Dice("1d20+5")
    defesa_do_monstro = 15

    resultado_ataque = ataque() # Usando __call__
    print(f"Você rolou um ataque: {resultado_ataque}")

    if resultado_ataque.was_critical():
        print("ACERTO CRÍTICO!")
    elif resultado_ataque >= defesa_do_monstro:
        print("Você acertou o monstro!")
    else:
        print("Você errou...")
        

    

        
        




