from typing import Dict, List, TypeAlias
from data.entity import Entity
from data.racas import RACA_CATALOGO, IRaca


EntityCatalog: TypeAlias = Dict[str, Entity]

class EntityManager:
    _instance = None
    
    # Dicionário para armazenar todas as entidades ativas no jogo
    active_entities: EntityCatalog = {}
    
    _entity_id_counter: int = 0 

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(EntityManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        self._initialized = True
        self.active_entities.clear()
        self._entity_id_counter = 0

    def _generate_unique_id(self, base_name: str) -> str:
        """Gera um ID único para uma nova entidade."""
        self._entity_id_counter += 1
        #  NomeBase_Contador (ex: Goblin_1, Goblin_2)
        return f"{base_name.replace(' ', '_')}_{self._entity_id_counter}"

    def create_entity(self, nome: str, raca_id: str) -> Entity | None:
        """
        Cria uma nova instância de Entity e a adiciona ao catálogo de entidades ativas.
        
        Args:
            nome (str): O nome da entidade (ex: 'Goblin').
            raca_id (str): O ID da raça no RACA_CATALOGO (ex: 'Gnomo Inventor').
            
        Returns:
            Entity | None: A entidade criada ou None se a raça não for encontrada.
        """
        raca_data: IRaca | None = RACA_CATALOGO.get(raca_id)
        
        if not raca_data:
            print(f"ERRO: Raça '{raca_id}' não encontrada para criar {nome}.")
            return None

        entity_id = self._generate_unique_id(nome)
        
        # 2. Cria a entidade
        new_entity = Entity(nome=nome, raca=raca_data)
        
        new_entity.id = entity_id
        self.active_entities[entity_id] = new_entity
        
        print(f"➕ Entidade '{nome}' (ID: {entity_id}) criada e adicionada.")
        return new_entity

    def get_entity(self, entity_id: str) -> Entity | None:
        """Busca uma entidade pelo seu ID único."""
        return self.active_entities.get(entity_id)

    def remove_entity(self, entity_id: str) -> bool:
        """Remove uma entidade do catálogo (ex: após morte ou sair da cena)."""
        if entity_id in self.active_entities:
            del self.active_entities[entity_id]
            print(f"➖ Entidade com ID '{entity_id}' removida.")
            return True
        return False
    
    def get_all_entities(self) -> List[Entity]:
        """Retorna uma lista de todas as entidades ativas."""
        return list(self.active_entities.values())