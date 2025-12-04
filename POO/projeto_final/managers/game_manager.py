from typing import List
from managers.dialogue_manager import DialogueManager
from managers.combat_manager import CombatManager
from managers.entity_manager import EntityManager
from managers.inventory_manager import InventoryManager
from managers.attribute_manager import AttributeManager
from managers.skill_manager import SkillManager
from data.racas import RACA_CATALOGO
from data.entity import Entity, Player
from data.skills import SKILL_CATALOG

class GameManager:
    _instance = None
    
    # Managers Principais
    dialogue_manager: DialogueManager
    combat_manager: CombatManager
    entity_manager: EntityManager
    inventory_manager: InventoryManager
    attribute_manager: AttributeManager
    skill_manager: SkillManager
    
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
        self.attribute_manager = AttributeManager() 
        self.inventory_manager = InventoryManager() 
        self.skill_manager = SkillManager()
        
        self.combat_manager.skill_manager = self.skill_manager
        self.combat_manager.attribute_manager = self.attribute_manager
        
        if not RACA_CATALOGO:
             print("ERRO: Catálogo de Raças vazio!")
        
        self.player: Player | None = None
        self.create_player("Joãozinho", "Humano")
        
        if self.player:
            initial_stats = self.attribute_manager.calculate_final_stats(self.player)
            max_hp = initial_stats.get('vida_maxima', 10)
            self.player.max_hp = max_hp
            self.player.current_hp = max_hp
            print(f"👤 Jogador criado e inicializado. HP: {self.player.current_hp}/{self.player.max_hp}")
            
            self.current_state = "MENU"


    def create_player(self, nome: str, raca_id: str):
        """Cria e define a Entidade do jogador."""
        raca_data = RACA_CATALOGO.get(raca_id)
        if raca_data:
            basic_attack = SKILL_CATALOG["basic_attack"]
            self.player = Player(nome=nome, raca=raca_data,abilities=[basic_attack])
            print(f"Jogador '{nome}' ({raca_id}) criado.")
        else:
            print(f"ERRO: Raça '{raca_id}' não encontrada.")


    def start_game(self):
        """Inicia o fluxo principal do jogo (ex: mostra o diálogo inicial)."""
        print("\nJogo Iniciado. Entrando em modo DIALOGUE.")
        self.current_state = "DIALOGUE"
        # Inicia a sequência de diálogo
        self.dialogue_manager.showDialogue("tutorial.1")
        
        


    def trigger_combat(self, enemy_raca_ids: List[str]):
        """Cria inimigos e inicia o combate, mudando o estado do jogo."""
        if not self.player:
            return

        enemy_entities: List['NPC'] = []
        for i, raca_id in enumerate(enemy_raca_ids):
            # Cria inimigos usando o EntityManager
            enemy = self.entity_manager.create_npc(f"Inimigo {i+1}", raca_id,abilities=[SKILL_CATALOG["basic_attack"]])
            if enemy:
                 # Inicializa HP para o inimigo também
                initial_stats = self.attribute_manager.calculate_final_stats(enemy)
                enemy.current_hp = initial_stats.get('vida_maxima', 10)
                enemy.max_hp = enemy.current_hp
                enemy_entities.append(enemy)

        if not enemy_entities:
            print("Não foi possível criar inimigos. Combate cancelado.")
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