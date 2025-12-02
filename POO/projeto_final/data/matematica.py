from random import random, randrange, choice

def definePeso(): 
    return(randrange(1, 10) + (round(randrange(100, 1000)/1000, 1) *10 + choice([.0, .5]))/10.00)

    