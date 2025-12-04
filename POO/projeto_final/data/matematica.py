from data.entity import Entity

from random import random, randrange, choice

def definePeso(base): 
    return((randrange(1, 3) + (round(randrange(100, 1000)/1000, 1) * 10 + choice([0, .5]))/10.00))+base

def calculaDefesa(pirokapreta: Entity):
    return((((pirokapreta.stats.constituicao)/2)+(pirokapreta.level))+randrange(pirokapreta.level, pirokapreta.level + 15))


