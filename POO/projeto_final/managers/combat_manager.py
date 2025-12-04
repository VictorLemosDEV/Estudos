from typing import List
from data.entity import Entity

class CombatManager:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(CombatManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if hasattr(self, '_initialized'):
            return

        print("🎛️ CombatManager inicializado e pronto para a ação.")
        
        self.is_active = False
        self.turn_count = 0
        self.participants: List = [] 
        self.current_turn_index = 0
        self.winner = None # Novo atributo para armazenar o vencedor
        
        self._initialized = True
        
    def start_combat(self, combatants: List): # Recebe uma lista única de combatentes
        if self.is_active:
            print("🚨 Já existe uma batalha em andamento!")
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
            print(f"\n--- Turno {self.turn_count} / Vez de: {current_entity.nome} (HP: {current_entity.vida_atual}) ---")

            # Chama o método de ação da entidade
            # current_entity.choose_action(self) 
        else:
            # Pula entidades mortas (caso um ataque as mate fora de seu turno)
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
            print("➡️ Fim do Round. Começando novo Round...")
            
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
        
    def get_participants(self):
        # Retorna apenas os participantes que estão vivos
        return [p for p in self.participants if p.is_alive()]