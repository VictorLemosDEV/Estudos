

from managers.game_manager import GameManager
from managers.combat_manager import CombatManager
from utils.attribute_calculator import hp_calculator
from data.racas import IRaca, Raca, RACA_CATALOGO
from data.entity import Entity

from random import choice






if __name__ == "__main__":

    GM = GameManager()
    

    # 2. Inicia o jogo
    GM.trigger_combat(["Gnomo Inventor"])
    

