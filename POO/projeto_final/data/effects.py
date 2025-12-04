from typing import Dict, Any, Callable
from data.entity import Entity
from managers.attribute_manager import AttributeManager

EFFECT_CATALOG: Dict[str, 'Effect'] = {}

class Effect:
    def __init__(self, id: str, nome: str, duration: int, 
                 stat_modifiers: Dict[str, int] = None, # Modificadores imediatos (ex: +5 STRENGTH)
                 tick_func: Callable[['Entity', 'AttributeManager'], None] = None, # Função executada a cada turno
                 is_stackable: bool = False):
        
        self.id = id
        self.nome = nome
        self.initial_duration = duration # Duração original (para resetar ou saber o máximo)
        self.duration = duration       # Duração restante
        self.stat_modifiers = stat_modifiers if stat_modifiers is not None else {}
        self.tick_func = tick_func
        self.is_stackable = is_stackable
        
        if self.id in EFFECT_CATALOG:
            print(f"Aviso: O Efeito ID '{self.id}' já existe e será sobrescrita.")
            
        EFFECT_CATALOG[self.id] = self

    def __repr__(self):
        return f"Effect(ID: {self.id}, Duração: {self.duration})"
    
    
def tick_poison_damage(entity: 'Entity', am: 'AttributeManager'):
    # O dano baseia-se em um atributo do alvo (ex: metade da Agilidade, simulando resistência)
    target_stats = am.calculate_final_stats(entity)
    damage = max(1, target_stats.get('DEXTERITY', 2) // 2)
    
    # Aplica o dano diretamente ao HP atual da entidade
    entity.current_hp -= damage
    print(f"🤢 {entity.nome} sofre {damage} de dano de Veneno. HP restante: {entity.current_hp}")
    
    if entity.current_hp <= 0:
        print(f"💀 {entity.nome} morreu envenenado!")
        
def tick_regeneration(entity: 'Entity', am: 'AttributeManager'):
    # A cura baseia-se em um valor fixo ou atributo (ex: 5 + 10% da CONSTITUICAO)
    target_stats = am.calculate_final_stats(entity)
    heal_amount = 5 + (target_stats.get('VITALITY', 1) // 10)
    
    # Aplica cura usando o AttributeManager para respeitar o MAX_HP
    am.heal_entity(entity, heal_amount)
    print(f"✨ {entity.nome} se regenera em {heal_amount} HP.")
    
    
def tick_rage(entity: 'Entity', am: 'AttributeManager'):
    import random
    if random.random() < 0.2:  # 20% de chance de levar 1 de dano
        print(f"🔥 {entity.nome} está exausto pela Fúria e sofre 1 de dano por fadiga.")
        am.apply_damage(entity, 1) # Dano sem mitigação
    
    
effect_rage = Effect(
    id="rage_buff",
    nome="Fúria",
    duration=2,
    stat_modifiers={"strength": 10},
    tick_func=tick_rage,
    is_stackable=False
)
    
effect_slow = Effect(
    id="slow_debuff",
    nome="Lentidão",
    duration=3,
    stat_modifiers={"agility": -5},
    is_stackable=False
)

effect_poison = Effect(
    id="poison_damage",
    nome="Veneno",
    duration=4,
    tick_func=tick_poison_damage,
    is_stackable=True 
)

effect_regen = Effect(
    id="regeneration",
    nome="Regeneração",
    duration=5,
    tick_func=tick_regeneration,
    is_stackable=False
)