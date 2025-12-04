

from managers.dialogue_manager import DialogueManager
from managers.combat_manager import CombatManager
from utils.attribute_calculator import hp_calculator
from data.racas import IRaca, Raca, RACA_CATALOGO
from data.entity import Entity

from random import choice






if __name__ == "__main__":

    DM = DialogueManager()
    DM.showDialogue("A")
    

    player = Entity(nome="Herói Lendário",raca=RACA_CATALOGO["Humano"])
    goblin = Entity(nome="Goblin", raca=RACA_CATALOGO["Gnomo Inventor"])
    orc = Entity(nome="Orc Brutal",raca=RACA_CATALOGO["Meio-Orc"])
    
    cm = CombatManager()
    
    CombatManager.process_turn = lambda self: (
        (self.participants[self.current_turn_index].choose_action(self), self._next_participant()) if self.is_active else
        print("Nenhuma batalha ativa para processar.")
    )

    cm.start_combat([player,goblin,orc])