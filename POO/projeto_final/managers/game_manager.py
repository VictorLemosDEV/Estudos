from typing import List
from managers.dialogue_manager import DialogueManager
from managers.combat_manager import CombatManager
from managers.entity_manager import EntityManager
from data.racas import RACA_CATALOGO
from data.entity import Entity

class GameManager:
    _instance = None
    
    # Managers Principais
    dialogue_manager: DialogueManager
    combat_manager: CombatManager
    entity_manager: EntityManager
    
    current_state: str = "MENU" # Estados: MENU, EXPLORING, COMBAT, DIALOGUE, GAME_OVER

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(GameManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        self._initialized = True
        
        self.dialogue_manager = DialogueManager()
        self.combat_manager = CombatManager()
        self.entity_manager = EntityManager()
        
        if not RACA_CATALOGO:
             print("ERRO: Catálogo de Raças vazio!")
        
        self.player: Entity | None = None
        self.create_player("Joãozinho", "Humano")


    def create_player(self, nome: str, raca_id: str):
        """Cria e define a Entidade do jogador."""
        raca_data = RACA_CATALOGO.get(raca_id)
        if raca_data:
            self.player = Entity(nome=nome, raca=raca_data)
            print(f"Jogador '{nome}' ({raca_id}) criado.")
        else:
            print(f"ERRO: Raça '{raca_id}' não encontrada.")


    def start_game(self):
        """Inicia o fluxo principal do jogo (ex: mostra o diálogo inicial)."""
        print("\nJogo Iniciado. Entrando em modo DIALOGUE.")
        self.current_state = "DIALOGUE"
        # Inicia a sequência de diálogo
        self.dialogue_manager.showDialogue("tutorial.1")


    def trigger_combat(self, enemy_entities: List[Entity]):
        """Transfere o controle para o CombatManager."""
        if not self.player:
            print("Não é possível iniciar combate: Jogador não existe.")
            return

        print("\nEntrando em modo COMBAT.")
        self.current_state = "COMBAT"
        participants = [self.player] + enemy_entities
        self.combat_manager.start_combat(participants)


    def end_combat(self, victory: bool):
        """Chamado pelo CombatManager ao fim da luta."""
        self.current_state = "EXPLORING"
        if victory:
            print("\n🏆 Vitória! Voltando ao modo EXPLORING.")
            # DIALOGO DE VITÒRIA
        else:
            print("\n💀 Derrota. Fim de Jogo.")
            self.current_state = "GAME_OVER"
            # DIALOGO DE DERROTA