from typing import List

ITEM_CATALOGO = {}
RUNAS = {}

class Runa(IRuna):

    def __init__(self, cor: str, nivel: int):
        self.cor = cor
        self.nivel = nivel

        RUNAS[self.cor] = self #insere a nova instancia de runa dentro do dicionario de runas

    def effect(self)


class Item(IItem):

    def __init__(self, nome: str, level: int, descricao: str, peso: float, runas: List[Runa]
        self.nome = nome
        self.level = level
        self.description = descricao
        self.peso = peso

        ITEM_CATALOGO[self.nome] = self #insere a nova instancia de item dentro do dicionario de itens
        
    
       


        



#This code fkng sux