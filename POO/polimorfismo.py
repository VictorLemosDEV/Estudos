

from vector import Vector
from abc import ABC, abstractmethod
from typing import List

class Animal(ABC):
    def __init__(self, posicao: Vector = Vector(0,0)):
        super().__init__()
        self.posicao = posicao
        self.historico_posicoes: List[Vector] = [self.posicao]
        
    @abstractmethod
    def mover(self, timesteps: int = 1): pass
    

class Aquatico(Animal):
    
    def mover(self, timesteps = 1):
        """Faz o Animal se Mover x posições

        Args:
            timesteps (int, optional): Quantas unidades de Movimento o animal se movimenta por chamada. Defaults to 1.
        """
        velocidade_step = Vector(2, -1)
            
        for _ in range(timesteps):
            # Calcula o próximo passo
            self.posicao = self.posicao + velocidade_step
            # Adiciona o passo ao histórico
            self.historico_posicoes.append(self.posicao)
                
        print(f"Aquatico moveu-se para a posição final {self.posicao}")
        

class Terrestre(Animal):
    def mover(self, timesteps = 1):
        velocidade_step = Vector(2, 0)
        for _ in range(timesteps):
            self.posicao = self.posicao + velocidade_step
            self.historico_posicoes.append(self.posicao)
            
        print(f"Terrestre moveu-se para a posição final {self.posicao}")

class Aereo(Animal):
    def mover(self, timesteps = 1):
        velocidade_step = Vector(1, 3)
        for _ in range(timesteps):
            self.posicao = self.posicao + velocidade_step
            self.historico_posicoes.append(self.posicao)
            
        print(f"Aereo moveu-se para a posição final {self.posicao}")

animais: Animal = [Aquatico(), Terrestre(), Aereo()]

print("Iniciando simulação...")
for animal in animais:
    animal.mover(3)
print("Simulação concluída.")

def Grafico():
    import matplotlib.pyplot as plt
    print("\nGerando gráfico da simulação...")

    plt.figure(figsize=(10, 8))

    for animal in animais:
        
        x_coords = [pos.x for pos in animal.historico_posicoes]
        y_coords = [pos.y for pos in animal.historico_posicoes]
        
        plt.plot(
            x_coords,
            y_coords,
            marker="o",
            linestyle='-',
            label=f"{type(animal).__name__}"
        )
        
        
    plt.title("Simulação de Movimento de Animais (3 Timesteps)")
    plt.xlabel("Posição X")
    plt.ylabel("Posição Y")
    plt.legend()
    plt.grid(True)
    plt.axhline(0, color="black", linewidth=0.5)
    plt.axvline(0, color="black", linewidth=0.5)
    plt.gca().set_aspect('equal', adjustable='box')

    plt.show()
    
    
Grafico() # Inicia Gráfico