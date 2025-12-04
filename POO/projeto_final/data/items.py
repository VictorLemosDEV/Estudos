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

    def __init__(self, nome: str, peso: float, runas: List[Runa], descricao: str):
        self.nome = nome
        self.level = randrange(1, 3)
        self.peso = definePeso(peso)
        self.runas = runas
        self.descricao = descricao

        ITEM_CATALOGO[self.nome] = self #insere a nova instancia de item dentro do dicionario de itens

    def __repr__(self):
        return f"Item:('{self.nome}', Lvl:{self.level}, Peso:{self.peso}, Runas:{self.runas}, Descricao:{self.descricao})"

#armas iniciais :p

copper_sword = Item(
    "Espada de cobre", 3, None, "Uma espada comum de cobre, versátil e durável, quase bom em quase qualquer situação"   
)
copper_spear = Item(
    "Lança de cobre", 2, None, "Uma lança comum de cobre, longo alcance, perfuração e veolidade mas não deixe seus inimigos chegarem perto"   
)
copper_dagger = Item(
    "Adaga de cobre", 1, None, "Uma adaga comum de cobre, rápida e curta, otimá para retaliar rapidmente, mas seu alcance deixa a desejar..."   
)
bamboo_short_bow = Item(
    "Arco curto de bambu", 1, None, "Um arco curto, velocidade de disparo rápida, mas de baixo calibre e alcance para um arco, otimo para rangers rápidos"   
)
bamboo_long_bow = Item(
    "Arco longo de bambu", 3, None, "Um arco longo de cobre, cadencia baixa mas com alcance e dano adimiraveis, otimo para hard rangers"   
)
stone_greatsword = Item(
    "Espada colossal de pedra", 12, None, "Uma espada gigantesca de pedra, altissimo dano, muito pesada, velocidade de ataque baixa, esmague seus oponentes com um ataque destruidor..."   
)
copper_halberd = Item(
    "Alabarda de cobre", 6, None, "Arma longa e destruidora, alto dano, medio alcance, media velocidade, ataques continuos e pesados, haja estamnia..."   
)

#poções iniais :P

S_heal_potion = Item(
    "Poção pequena de cura", .3 , None, "Oferece cura baixa porem rápida"   
)
M_heal_potion = Item(
    "Meida poção de cura", .35 , None, "Oferece cura média"   
)
L_heal_potion = Item(
    "Poção pequena de cura", .4 , None, "Oferece grande taxa de cura porem lenta de consumir"   
)

#This code fkng sux