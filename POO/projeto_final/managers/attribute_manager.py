from typing import Dict, Any, List
from data.entity import Entity

class AttributeManager:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(AttributeManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        self._initialized = True

    def calculate_final_stats(self, entity: Entity) -> Dict[str, Any]:
        final_stats = dict(entity.raca.attributeBonus)
        
        BASE_HP = 40
        
        final_stats['vida_maxima'] = BASE_HP + final_stats['constituicao'] * 2
        
        return final_stats
        
    def apply_damage(self, entity: Entity, raw_damage: int):
        mitigation = self.calculate_damage_mitigation(entity)
        final_damage = max(0, raw_damage - mitigation)
        
        entity.current_hp -= final_damage
        print(f"{entity.nome} sofreu {final_damage} de dano. HP restante: {entity.current_hp}")
        
        if entity.current_hp <= 0:
            print(f"{entity.nome} foi derrotado!")
            
    def heal_entity(self, entity: Entity, amount: int):
        max_hp = self.calculate_final_stats(entity)['MAX_HP']
        entity.current_hp = min(entity.current_hp + amount, max_hp)
        print(f"{entity.nome} curado em {amount}. HP atual: {entity.current_hp}")
        
    def calculate_damage_mitigation(self, entity: Entity) -> int:
        final_stats = self.calculate_final_stats(entity)
        defense = final_stats.get('constituicao', 0)
        return defense // 2