from typing import Protocol

class Pokemon:
    def __init__(self, nome: str, **kwargs):
        self.nome = nome
        # A lista de ataques aceita QUALQUER objeto que cumpra o protocolo IAtaque
        self.ataques: list[IAtaque] = [] 
        ...

    def usar_ataque(self, indice_ataque: int, alvo: 'Pokemon'):
        ataque_escolhido = self.ataques[indice_ataque]
        
        # O sistema de batalha não se importa com a classe, 
        # apenas chama .executar()
        log = ataque_escolhido.executar(self, alvo)
        print(log)

class IAtaque(Protocol):
    
    nome: str
    tipo: str
    pp_maximo: int
    
    def executar(self, usuario: 'Pokemon', alvo: 'Pokemon') -> str:
        ...
        
    def get_pp_atual(self) -> int:
        ...
        
class AtaqueDeDano:
    def __init__(self, nome: str, tipo: str, poder: int, pp: int):
        self.nome = nome
        self.tipo = tipo
        self.poder = poder
        self.pp_maximo = pp
        self._pp_atual = pp
        
    def executar(self, usuario: 'Pokemon', alvo: 'Pokemon') -> str:
        dano = (self.poder * usuario.get_ataque_stat()) // alvo.get_defesa_stat()
        alvo.sofrer_dano(dano)
        self._pp_atual -= 1
        return f"{usuario.nome} usou {self.nome} e causou {dano} de dano!"
    
    def get_pp_atual(self) -> int:
        return self._pp_atual