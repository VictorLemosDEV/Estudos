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
    "Media poção de cura", .35 , None, "Oferece cura média"   
)
L_heal_potion = Item(
    "Poção grande de cura", .4 , None, "Oferece grande taxa de cura porem lenta de consumir"   
)
    #speed
S_speed_potion = Item(
    "Poção pequena de velocidade", .3 , None, "Pequeno buff de velocidade"   
)
M_speed_potion = Item(
    "Media poção de velocidade", .35 , None, "Médio buff de velocidade"   
)
L_speed_potion = Item(
    "Poção grande de velocidade", .4 , None, "Oferece grande buff de velocidade porem lenta de consumir"   
)
    #damage
S_damage_potion = Item(
    "Poção pequena de dano", .3 , None, "Pequeno buff de dano"   
)
M_damage_potion = Item(
    "Media poção de dano", .35 , None, "Médio buff de dano"   
)
L_damage_potion = Item(
    "Poção grande de dano", .4 , None, "Oferece grande buff de dano porem lenta de consumir"   
)
    #defense
S_defense_potion = Item(
    "Poção pequena de defesa", .3 , None, "Pequeno buff de defesa"   
)
M_defense_potion = Item(
    "Media poção de defesa", .35 , None, "Médio buff de defesa"   
)
L_defense_potion = Item(
    "Poção grande de defesa", .4 , None, "Oferece grande buff de defesa porem lenta de consumir"   
)
    #wisdom
S_wisdom_potion = Item(
    "Poção pequena de intelgencia", .3 , None, "Pequeno buff de inteligencia"   
)
M_wisdom_potion = Item(
    "Media poção de intelgencia", .35 , None, "Médio buff de inteligencia"   
)
L_wisdom_potion = Item(
    "Poção grande de intelgencia", .4 , None, "Oferece grande buff de inteligencia porem lenta de consumir"
)
    #efeitos
        #invisibilidade
S_invisibility_potion = Item(
    "Poção pequena de invisibilidade", .3 , None, "Oferece invisibilidade por 1 minutos"   
)
M_velocidade_potion = Item(
    "Media poção de invisibilidade", .35 , None, "Oferece invisibilidade por 2,5 minutos"   
)
L_velocidade_potion = Item(
    "Poção grande de invisibilidade", .4 , None, "Oferece invisibilidade por 5 minutos"   
)
        #taxa de drop
S_drop_rate_potion = Item(
    "Poção pequena de sorte", .3 , None, "Oferece pequena taxa de drop aumentada por 1 minuto"   
)
M_drop_rate_potion = Item(
    "Media poção de sorte", .35 , None, "Oferece média taxa de drop aumentada por 2,5 minutos"   
)
L_drop_rate_potion = Item(
    "Poção pequena de sorte", .4 , None, "Oferece alta taxa de drop aumentada por 5 minutos"   
)


#This code fkng sux