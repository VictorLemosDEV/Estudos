from typing import Callable, Dict
from data.entity import Entity
from managers.attribute_manager import AttributeManager


SKILL_CATALOG: Dict[str, 'Skill'] = {}


class Skill:
    def __init__(self, id: str, nome: str, cost: int, cooldown: int,
                 target_type: str, execute_func: Callable, weight: int = 10):
        self.id = id
        self.nome = nome
        self.cost = cost
        self.cooldown = cooldown
        self.target_type = target_type  # 'SINGLE_ENEMY', 'SELF', 'ALL_ENEMIES'
        self.execute_func = execute_func # Função que aplica o efeito real
        self.weight = weight            # Peso de IA para NPCs

        if self.id in SKILL_CATALOG:
            print(f"Aviso: A habilidade ID '{self.id}' já existe e será sobrescrita.")
            
        SKILL_CATALOG[self.id] = self



def execute_basic_attack(caster: 'Entity', target: 'Entity', am: 'AttributeManager'):

    caster_stats = am.calculate_final_stats(caster)
    

    base_damage = caster_stats.get('strength', 1) 
    

    print(f"{caster.nome} realiza um Ataque Básico em {target.nome}.")
    am.apply_damage(target, base_damage)
    
    
ataque_basico = Skill(
    id="basic_attack", 
    nome="Ataque", 
    cost=0, 
    cooldown=0,
    target_type='SINGLE_ENEMY', 
    execute_func=lambda c, t, am: print(f"Ataque de {c.nome} em {t.nome}"),
    weight=100
)