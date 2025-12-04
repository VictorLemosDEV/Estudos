from typing import List, Tuple, Union
from data.skills import Skill
from data.entity import NPC, Entity, Player
from random import choices, choice

class CombatManager:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(CombatManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if hasattr(self, '_initialized'):
            return

        
        self.is_active = False
        self.turn_count = 0
        self.participants: List = [] 
        self.current_turn_index = 0
        self.winner = None # Novo atributo para armazenar o vencedor
        
        self._initialized = True
        
    def start_combat(self, combatants: List): # Recebe uma lista única de combatentes
        if self.is_active:
            print("Já existe uma batalha em andamento!")
            return

        self.is_active = True
        self.turn_count = 1
        self.winner = None
        
        # Todos são participantes sem distinção de time
        self.participants = combatants
        
        print("\n--- Batalha Free-for-All Iniciada! ---")
        print(f"Participantes: {[p.nome for p in self.participants]}")
        self.process_turn()

    def process_turn(self):
        if not self.is_active:
            print("🚫 Nenhuma batalha ativa para processar.")
            return

        # Garante que a entidade ainda está viva antes de dar o turno a ela
        current_entity = self.participants[self.current_turn_index]
        
        if current_entity.is_alive():
            print(f"\n--- Turno {self.turn_count} / Vez de: {current_entity.nome} (HP: {current_entity.current_hp}) ---")
            
            chosen_skill, target = current_entity.choose_action(self)
            
            chosen_skill.execute_func(current_entity, target, self.attribute_manager)
        else:
            print(f"💀 {current_entity.nome} está fora de combate. Pulando turno.")


        self._next_participant()


    def _next_participant(self):
        # Verifica a condição de fim de combate
        if not self._check_victory_condition():
            return
            
        # Avança para o próximo índice, pulando se necessário
        self.current_turn_index = (self.current_turn_index + 1) % len(self.participants)
        
        if self.current_turn_index == 0:
            self.turn_count += 1
            print("Round. Começando novo Round...")
            
        self.process_turn()
        
        
    def _check_victory_condition(self):
        # Filtra apenas os participantes vivos
        living_combatants = self.get_participants()
        combatants_alive = len(living_combatants)

        if combatants_alive == 1:
            # Apenas um vivo: Vitória!
            self.winner = living_combatants[0]
            self.end_combat("vitoria")
            return False
        
        if combatants_alive == 0:
            # Ninguém vivo: Empate
            self.end_combat("empate")
            return False
            
        return True # Combate continua
        
    def end_combat(self, result):
        self.is_active = False
        self.turn_count = 0
        # self.participants é limpo, mas self.winner é mantido para referência
        
        # Mensagens adaptadas
        if result == "vitoria":
            print(f"\n🏆 Vitória! O vencedor é: {self.winner.nome}")
        elif result == "empate":
            print("\n💀 Empate! Todos os participantes foram derrotados.")
        else:
            # Caso "derrota" não deve mais ocorrer neste modo
            print("\n--- Batalha Encerrada ---") 

        self.participants = []
        self.current_turn_index = 0
        print("--- Batalha Encerrada ---")
        
    def npc_choose_ability(self, npc: 'NPC') -> Tuple['Skill', 'Entity']:
        """
        Implementa a lógica de escolha de habilidade baseada em peso (weight).
        """
        
        # 1. Filtra as habilidades que o NPC PODE usar (mana/cooldown)
        available_abilities = [
            skill for skill in npc.abilities 
            if self.skill_manager.can_use_skill(npc, skill)
        ]

        if not available_abilities:
            print(f"{npc.nome} usa Ataque Básico.")
            # return basic_attack_skill, target
            print(npc.abilities)
            return choice(npc.abilities), self._select_random_target(npc)


        weights = [skill.weight for skill in available_abilities]
        
        chosen_skill: 'Skill' = choices(available_abilities, weights=weights, k=1)[0]
        
        target = self._select_target_by_type(npc, chosen_skill.target_type)
        
        return chosen_skill, target
    
    def player_choose_ability(self, player: 'Player') -> Tuple['Skill', 'Entity']:
        """
        Solicita a entrada do usuário para escolher a habilidade e o alvo.
        """
        available_abilities = [
            skill for skill in player.abilities 
            if self.skill_manager.can_use_skill(player, skill)
        ]
        
        print("\n--- Escolha uma Habilidade ---")
        for i, skill in enumerate(available_abilities):
            print(f"[{i + 1}] {skill.nome} (Custo: {skill.cost})")

        while True:
            try:
                choice_index = int(input("Sua escolha: ")) - 1
                if 0 <= choice_index < len(available_abilities):
                    chosen_skill = available_abilities[choice_index]
                    target = self._select_player_target(player, chosen_skill.target_type)
                    return chosen_skill, target
                else:
                    print("Escolha inválida.")
            except ValueError:
                print("Entrada inválida. Digite o número.")
                
    def _select_player_target(self, caster: 'Entity', target_type: str) -> 'Entity' | None:
        """Permite que o jogador escolha um alvo entre os participantes válidos."""
        

        if target_type == 'SINGLE_ENEMY':
            candidates = [p for p in self.participants if p.is_alive() and p is not caster]
        elif target_type == 'SELF':
            return caster
        else:
            candidates = []

        if not candidates:
            print("Nenhum alvo válido encontrado.")
            return None

        # 2. Exibir opções para o usuário
        print("\n--- Escolha um Alvo ---")
        for i, target in enumerate(candidates):
            print(f"[{i + 1}] {target.nome} ({target.current_hp}/{target.max_hp} HP)")

        while True:
            try:
                choice_index = int(input("Número do alvo: ")) - 1
                if 0 <= choice_index < len(candidates):
                    return candidates[choice_index]
                else:
                    print("Escolha de alvo inválida.")
            except ValueError:
           
                print("Entrada inválida. Digite o número.")
        
        
    def _select_target_by_type(self, caster: 'Entity', target_type: str) -> Union['Entity', List['Entity'], None]:
        """
        Seleciona o(s) alvo(s) para o NPC com base no tipo de habilidade.
        
        Args:
            caster: A entidade que está usando a habilidade (o NPC).
            target_type: O tipo de alvo ('SELF', 'SINGLE_ENEMY', 'ALL_ENEMIES').
        
        Returns:
            A entidade alvo, uma lista de entidades alvo, ou None.
        """
        
        # 1. Alvos Vivos no Combate, excluindo o Atacante.
        potential_enemies = [
            p for p in self.participants 
            if p.is_alive() and p is not caster
        ]

        if target_type == 'SELF':
            # Tipo: SELF (Apenas o usuário da habilidade)
            return caster
            
        elif target_type == 'SINGLE_ENEMY':
            # Tipo: SINGLE_ENEMY (Escolhe um alvo aleatório entre os inimigos)
            if potential_enemies:
                return choice(potential_enemies)
            return None # Nenhum inimigo vivo
            
        elif target_type == 'ALL_ENEMIES':
            # Tipo: ALL_ENEMIES (Retorna uma lista com todos os inimigos vivos)
            return potential_enemies
            
    def _select_random_target(self, caster: 'Entity') -> 'Entity':
        targets = [p for p in self.participants if p.is_alive() and p is not caster]
        return choice(targets) if targets else caster
        
    def get_participants(self):
        # Retorna apenas os participantes que estão vivos
        return [p for p in self.participants if p.is_alive()]