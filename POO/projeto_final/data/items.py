from typing import List
from random import random, randrange
from matematica import definePeso

ITEM_CATALOGO = {}
RUNAS = {}

class Runa():
# class Runa(IRuna):

    def __init__(self, cor: str, nivel: int):
        self.cor = cor
        self.nivel = nivel

        RUNAS[self.cor] = self #insere a nova instancia de runa dentro do dicionario de runas

    #def effect(self)


# class Item(IItem):
class Item():

    def __init__(self, nome: str, level: int, peso: float, runas: List[Runa], descricao: str):
        self.nome = nome
        self.level = level
        self.peso = peso
        self.runas = runas
        self.descricao = descricao

        ITEM_CATALOGO[self.nome] = self #insere a nova instancia de item dentro do dicionario de itens

    def __repr__(self):
        return f"Item:('{self.nome}', Lvl:{self.level}, Peso:{self.peso}, Runas:{self.runas}, Descricao:{self.descricao})"



espada_de_cobre = Item(
    "Espada de cobre", randrange(1, 5), definePeso(), None ,"Uma espada comum de cobre, versátil e durável, quase bom em quase qualquer situação"   
)       
#This code fkng sux