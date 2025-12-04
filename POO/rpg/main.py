from typing import Union, List, Dict
from time import sleep

story_map: List[Union[str, List[Union[str, int]]]]  = [

    ["Bem vindo ao Rpg Fodão das Galáxias",2.5],

    ["Eu sou o mestre dos magos", 1.5],

    "E tenho uma mensagem a passar"


]




if __name__ == "__main__":
    for line in story_map:
        if type(line) == str:
            print(line)
        else:
            text = line[0]
            interval = line[1]
            print(text)
            sleep(interval)
            