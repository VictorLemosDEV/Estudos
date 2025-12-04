from typing import List, Dict, Tuple, Any, TypeAlias, Callable
from data.entity import Entity
from data.items import Item, ConsumableItem

# 🔄 TypeAlias para representar um slot de inventário: Item e sua quantidade
InventorySlot: TypeAlias = Tuple[Item, int]


class InventoryManager:
    _instance = None
    
    # Capacidade máxima de itens no inventário
    MAX_CAPACITY = 50 

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(InventoryManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        self._initialized = True

    def get_inventory(self, entity: Entity) -> Dict[str, InventorySlot]:
        """Retorna o inventário de uma entidade."""
        # Assumindo que a Entity possui um atributo 'inventory: Dict[str, InventorySlot]'
        return entity.inventory

    def add_item(self, entity: Entity, item: Item, quantity: int = 1) -> bool:
        """Adiciona um item ao inventário da entidade."""
        inventory = self.get_inventory(entity)
        
        if len(inventory) >= self.MAX_CAPACITY:
             print(f"Inventário de {entity.nome} está cheio!")
             return False

        if item.id in inventory:
            current_item, current_qty = inventory[item.id]
            inventory[item.id] = (current_item, current_qty + quantity)
        else:
            inventory[item.id] = (item, quantity)
        
        print(f"📦 {entity.nome} ganhou {quantity}x {item.nome}.")
        return True

    def remove_item(self, entity: Entity, item_id: str, quantity: int = 1) -> bool:
        """Remove uma quantidade específica de um item do inventário."""
        inventory = self.get_inventory(entity)
        
        if item_id not in inventory:
            print(f"{item_id} não encontrado no inventário de {entity.nome}.")
            return False

        current_item, current_qty = inventory[item_id]
        
        if current_qty < quantity:
            print(f"Apenas {current_qty}x de {current_item.nome} em posse. Remoção falhou.")
            return False
            
        new_qty = current_qty - quantity
        
        if new_qty <= 0:
            del inventory[item_id]
        else:
            inventory[item_id] = (current_item, new_qty)
            
        print(f"🗑️ {entity.nome} perdeu {quantity}x {current_item.nome}.")
        return True
        
    def equip_item(self, entity: Entity, item_id: str) -> bool:
        """Equipa um item na entidade, aplicando seus atributos."""
        inventory = self.get_inventory(entity)
        
        if item_id not in inventory:
            return False

        item, _ = inventory[item_id]
        
        
        
        # Lógica de desequipar item no slot atual (se houver) e equipar o novo
        
        print(f"🛡️ {entity.nome} equipou {item.nome}.")
        return True
    
    def use_consumable(self, entity: Entity, item_id: str) -> bool:
        """Usa um item consumível na entidade."""
        inventory = self.get_inventory(entity)
        
        if item_id not in inventory:
            return False
        
        item, _ = inventory[item_id]
        
        if not isinstance(item, ConsumableItem):
            print(f"{item.nome} não é um item consumível.")
            return False
            
        # item.apply_effect(entity) 
        print(f"🧪 {entity.nome} usou {item.nome}.")
        
        # 2. Remover o item do inventário
        return self.remove_item(entity, item_id, 1)