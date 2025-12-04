from typing import Dict, Any, List, Callable, TypeAlias
from data.entity import Entity
from managers.attribute_manager import AttributeManager
from data.skills import Skill
from data.effects import Effect

Cooldowns: TypeAlias = Dict[str, int]

class SkillManager:
    _instance = None
    
    attribute_manager: AttributeManager
    
    active_cooldowns: Dict[str, Cooldowns] = {} 

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SkillManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        self._initialized = True
        self.attribute_manager = AttributeManager() 

    def can_use_skill(self, caster: Entity, skill: 'Skill') -> bool:
        # AQUI: Lógica de custo (ex: Mana)
        # if caster.current_mana < skill.cost:
        #     return False

        cooldowns = self.active_cooldowns.get(caster.id, {})
        if cooldowns.get(skill.id, 0) > 0:
            print(f"{skill.nome} está em Cooldown ({cooldowns[skill.id]} turnos restantes).")
            return False
            
        return True

    def execute_skill(self, caster: Entity, target: Entity, skill: 'Skill') -> bool:
        if not self.can_use_skill(caster, skill):
            return False
        
        
        caster.mana -= skill.cost 
        
        self.set_cooldown(caster, skill.id, skill.cooldown)
        
        # skill.effect_function(caster, target, self.attribute_manager) 
        print(f"{caster.nome} usou {skill.nome} em {target.nome}.")
        
        return True

    def set_cooldown(self, entity: Entity, skill_id: str, turns: int):
        if entity.id not in self.active_cooldowns:
            self.active_cooldowns[entity.id] = {}
        self.active_cooldowns[entity.id][skill_id] = turns

    def tick_cooldowns(self, entity: Entity):
        entity_cooldowns = self.active_cooldowns.get(entity.id)
        if entity_cooldowns:
            keys_to_remove = [] 
            for skill_id, turns in entity_cooldowns.items():
                if turns > 0:
                    entity_cooldowns[skill_id] -= 1
                    if entity_cooldowns[skill_id] <= 0:
                        keys_to_remove.append(skill_id)
                        
            for skill_id in keys_to_remove:
                del entity_cooldowns[skill_id]
                print(f"Cooldown de {skill_id} de {entity.nome} resetado.")

    def apply_effect(self, target: Entity, effect: 'Effect'):
        # target.active_effects.append(effect) 
        
       
        print(f"✨ {target.nome} recebeu o efeito {effect.nome}.")


    def tick_effects(self, entity: Entity):
        # Lógica para processar a duração e o efeito por turno de todos os efeitos ativos.
        # for effect in entity.active_effects:
        #     1. Aplicar tick de dano/cura usando self.attribute_manager
        #     2. Reduzir a duração (effect.duration -= 1)
        #     3. Remover se duration <= 0
        pass