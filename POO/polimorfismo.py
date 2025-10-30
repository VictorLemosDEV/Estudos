from vector import Vector
from abc import ABC, abstractmethod

class Animal(ABC):
    def __init__(self, posicao: Vector = Vector(0,0)):
        super().__init__()
        self.posicao = posicao
        
    @abstractmethod
    def mover(self, timesteps: int = 1): pass
    

class Aquatico(Animal):
    
    def mover(self, timesteps = 1):
        """Faz o Animal se Mover x posições

        Args:
            timesteps (int, optional): Quantas unidades de Movimento o animal se movimenta por chamada. Defaults to 1.
        """
        self.posicao = self.posicao + Vector(2,-1) * timesteps
        print(f"Aquatico moveu-se para a posição {self.posicao}")
        

class Terrestre(Animal):
    def mover(self, timesteps = 1):
        self.posicao = self.posicao + Vector(2,0) * timesteps
        print(f"Terrestre moveu-se para a posição {self.posicao}")

class Aereo(Animal):
    def mover(self, timesteps = 1):
        self.posicao = self.posicao + Vector(1,3) * timesteps
        print(f"Aereo moveu-se para a posição {self.posicao}")

animais: Animal = [Aquatico(), Terrestre(), Aereo()]

for animal in animais:
    animal.mover(3)