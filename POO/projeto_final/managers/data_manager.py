import sqlite3
import json
from typing import List, Tuple, Dict, Any, Union, Optional

class DataManager:
    _instance = None
    
    # Nome do arquivo do banco de dados
    DB_NAME = "rpg_game_data.db"
    
    # Conexão e Cursor (serão definidos no __init__)
    _connection: sqlite3.Connection | None = None
    _cursor: sqlite3.Cursor | None = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DataManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        self._initialized = True
        
        print(f"Inicializando o DataManager. Conectando a {self.DB_NAME}...")
        self._connect()
        self.initialize_schema() # Garante que as tabelas básicas existam

    def _connect(self):
        """Estabelece a conexão com o banco de dados SQLite."""
        try:
            self._connection = sqlite3.connect(self.DB_NAME)
            # Permite acessar colunas por nome - DEVE vir ANTES de criar o cursor
            self._connection.row_factory = sqlite3.Row
            self._cursor = self._connection.cursor()
            print("Conexão com SQLite estabelecida.")
        except sqlite3.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            self._connection = None
            self._cursor = None

    def close(self):
        """Fecha a conexão com o banco de dados."""
        if self._connection:
            self._connection.close()
            print(f"Conexão com {self.DB_NAME} fechada.")

    def initialize_schema(self):
        """Cria as tabelas iniciais necessárias (ex: Itens, Personagens)."""
        if not self._cursor:
            return

        try:
            # Tabela de Entidades (Player/NPC)
            self._cursor.execute("""
                CREATE TABLE IF NOT EXISTS Entities (
                    id TEXT PRIMARY KEY,
                    nome TEXT NOT NULL,
                    raca_id TEXT NOT NULL,
                    entity_type TEXT NOT NULL,
                    level INTEGER NOT NULL DEFAULT 1,
                    current_hp INTEGER NOT NULL,
                    max_hp INTEGER NOT NULL,
                    mana INTEGER NOT NULL DEFAULT 0,
                    mana_maxima INTEGER NOT NULL DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            # Tabela de Stats das Entidades
            self._cursor.execute("""
                CREATE TABLE IF NOT EXISTS EntityStats (
                    entity_id TEXT PRIMARY KEY,
                    forca INTEGER NOT NULL DEFAULT 1,
                    constituicao INTEGER NOT NULL DEFAULT 1,
                    agilidade INTEGER NOT NULL DEFAULT 1,
                    inteligencia INTEGER NOT NULL DEFAULT 1,
                    bonus_json TEXT,
                    FOREIGN KEY (entity_id) REFERENCES Entities(id) ON DELETE CASCADE
                );
            """)
            
            # Tabela de Inventário
            self._cursor.execute("""
                CREATE TABLE IF NOT EXISTS Inventory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    entity_id TEXT NOT NULL,
                    item_name TEXT NOT NULL,
                    quantity INTEGER NOT NULL DEFAULT 1,
                    FOREIGN KEY (entity_id) REFERENCES Entities(id) ON DELETE CASCADE,
                    UNIQUE(entity_id, item_name)
                );
            """)
            
            # Tabela de Equipamento
            self._cursor.execute("""
                CREATE TABLE IF NOT EXISTS Equipment (
                    entity_id TEXT NOT NULL,
                    slot TEXT NOT NULL,
                    item_name TEXT,
                    PRIMARY KEY (entity_id, slot),
                    FOREIGN KEY (entity_id) REFERENCES Entities(id) ON DELETE CASCADE
                );
            """)
            
            # Tabela de Habilidades das Entidades
            self._cursor.execute("""
                CREATE TABLE IF NOT EXISTS EntityAbilities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    entity_id TEXT NOT NULL,
                    skill_id TEXT NOT NULL,
                    FOREIGN KEY (entity_id) REFERENCES Entities(id) ON DELETE CASCADE,
                    UNIQUE(entity_id, skill_id)
                );
            """)
            
            # Tabela de Estado do Jogo
            self._cursor.execute("""
                CREATE TABLE IF NOT EXISTS GameState (
                    id INTEGER PRIMARY KEY CHECK (id = 1),
                    player_id TEXT,
                    current_state TEXT NOT NULL DEFAULT 'MENU',
                    save_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metadata_json TEXT,
                    FOREIGN KEY (player_id) REFERENCES Entities(id)
                );
            """)
            
            self._connection.commit()
            print("Esquema do banco de dados inicializado.")
        except sqlite3.Error as e:
            print(f"Erro ao inicializar o esquema: {e}")

    # --- Métodos de Execução Genéricos (CRUD) ---

    def execute_query(self, query: str, params: Union[Tuple, Dict[str, Any]] = ()) -> List[sqlite3.Row]:
        """Executa uma consulta SELECT e retorna os resultados."""
        if not self._cursor:
            return []
        try:
            self._cursor.execute(query, params)
            return self._cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Erro ao executar consulta: {query}. Erro: {e}")
            return []

    def execute_command(self, query: str, params: Union[Tuple, Dict[str, Any]] = ()) -> int:
        """Executa comandos INSERT, UPDATE, DELETE e retorna o número de linhas afetadas."""
        if not self._connection:
            return 0
        try:
            self._cursor.execute(query, params)
            self._connection.commit()
            return self._cursor.rowcount
        except sqlite3.Error as e:
            print(f"Erro ao executar comando: {query}. Erro: {e}")
            # Tenta reverter a transação em caso de erro
            self._connection.rollback()
            return 0

    # --- Métodos para Salvar Dados ---

    def save_entity(self, entity: 'Entity') -> bool:
        """Salva o estado completo de uma entidade (stats, inventário, equipamento, habilidades)."""
        if not self._connection:
            print("Erro: conexão com banco não estabelecida.")
            return False
        
        try:
            # Determina o tipo da entidade
            entity_type = entity.__class__.__name__
            
            # 1. Salva dados básicos da entidade
            self.execute_command("""
                INSERT OR REPLACE INTO Entities 
                (id, nome, raca_id, entity_type, level, current_hp, max_hp, mana, mana_maxima, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (entity.id, entity.nome, entity.raca.nome, entity_type, 
                  entity.level, entity.current_hp, entity.max_hp, 
                  entity.mana, entity.mana_maxima))
            
            # 2. Salva stats da entidade
            self._save_entity_stats(entity)
            
            # 3. Salva inventário
            self._save_inventory(entity)
            
            # 4. Salva equipamento
            self._save_equipment(entity)
            
            # 5. Salva habilidades
            self._save_abilities(entity)
            
            print(f"Dados de '{entity.nome}' salvos com sucesso.")
            return True
            
        except Exception as e:
            print(f"Erro ao salvar '{entity.nome}': {e}")
            self._connection.rollback()
            return False
    
    def _save_entity_stats(self, entity: 'Entity'):
        """Salva os stats de uma entidade."""
        bonus_json = json.dumps(entity.stats.bonus) if entity.stats.bonus else None
        
        self.execute_command("""
            INSERT OR REPLACE INTO EntityStats 
            (entity_id, forca, constituicao, agilidade, inteligencia, bonus_json)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (entity.id, entity.stats.forca, entity.stats.constituicao,
              entity.stats.agilidade, entity.stats.inteligencia, bonus_json))
    
    def _save_inventory(self, entity: 'Entity'):
        """Salva o inventário de uma entidade."""
        # Remove inventário antigo
        self.execute_command("DELETE FROM Inventory WHERE entity_id = ?", (entity.id,))
        
        # Salva inventário atual
        if hasattr(entity, 'inventario') and entity.inventario:
            for item_name, (item, quantity) in entity.inventario.items():
                self.execute_command("""
                    INSERT INTO Inventory (entity_id, item_name, quantity)
                    VALUES (?, ?, ?)
                """, (entity.id, item_name, quantity))
    
    def _save_equipment(self, entity: 'Entity'):
        """Salva o equipamento de uma entidade."""
        # Remove equipamento antigo
        self.execute_command("DELETE FROM Equipment WHERE entity_id = ?", (entity.id,))
        
        # Salva equipamento atual
        if hasattr(entity, 'equipment') and entity.equipment:
            for slot, item in entity.equipment.items():
                item_name = item.nome if item else None
                self.execute_command("""
                    INSERT INTO Equipment (entity_id, slot, item_name)
                    VALUES (?, ?, ?)
                """, (entity.id, slot, item_name))
    
    def _save_abilities(self, entity: 'Entity'):
        """Salva as habilidades de uma entidade."""
        # Remove habilidades antigas
        self.execute_command("DELETE FROM EntityAbilities WHERE entity_id = ?", (entity.id,))
        
        # Salva habilidades atuais
        if hasattr(entity, 'abilities') and entity.abilities:
            for skill in entity.abilities:
                self.execute_command("""
                    INSERT INTO EntityAbilities (entity_id, skill_id)
                    VALUES (?, ?)
                """, (entity.id, skill.id))
    
    def save_game_state(self, player: 'Entity', current_state: str, metadata: Optional[Dict] = None) -> bool:
        """Salva o estado geral do jogo."""
        if not self._connection:
            print("Erro: conexão com banco não estabelecida.")
            return False
        
        try:
            metadata_json = json.dumps(metadata) if metadata else None
            
            self.execute_command("""
                INSERT OR REPLACE INTO GameState 
                (id, player_id, current_state, save_timestamp, metadata_json)
                VALUES (1, ?, ?, CURRENT_TIMESTAMP, ?)
            """, (player.id, current_state, metadata_json))
            
            # Salva também a entidade do jogador
            self.save_entity(player)
            
            print(f"Jogo salvo com sucesso.")
            return True
            
        except Exception as e:
            print(f"Erro ao salvar o jogo: {e}")
            self._connection.rollback()
            return False
    
    # --- Métodos para Carregar Dados ---
    
    def load_entity(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """Carrega todos os dados de uma entidade."""
        if not self._cursor:
            print("Erro: conexão com banco não estabelecida.")
            return None
        
        try:
            # 1. Carrega dados básicos
            entity_rows = self.execute_query(
                "SELECT * FROM Entities WHERE id = ?", (entity_id,)
            )
            
            if not entity_rows:
                print(f"Entidade '{entity_id}' não foi encontrada.")
                return None
            
            # Converte sqlite3.Row para dict
            row = entity_rows[0]
            entity_data = {
                'id': row['id'],
                'nome': row['nome'],
                'raca_id': row['raca_id'],
                'entity_type': row['entity_type'],
                'level': row['level'],
                'current_hp': row['current_hp'],
                'max_hp': row['max_hp'],
                'mana': row['mana'],
                'mana_maxima': row['mana_maxima']
            }
            
            # 2. Carrega stats
            entity_data['stats'] = self._load_entity_stats(entity_id)
            
            # 3. Carrega inventário
            entity_data['inventario'] = self._load_inventory(entity_id)
            
            # 4. Carrega equipamento
            entity_data['equipment'] = self._load_equipment(entity_id)
            
            # 5. Carrega habilidades
            entity_data['abilities'] = self._load_abilities(entity_id)
            
            print(f"Dados de '{entity_data['nome']}' carregados.")
            return entity_data
            
        except Exception as e:
            print(f"Erro ao carregar '{entity_id}': {e}")
            return None
    
    def _load_entity_stats(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """Carrega os stats de uma entidade."""
        rows = self.execute_query(
            "SELECT * FROM EntityStats WHERE entity_id = ?", (entity_id,)
        )
        
        if not rows:
            return None
        
        # Converte sqlite3.Row para dict
        row = rows[0]
        stats_data = {
            'entity_id': row['entity_id'],
            'forca': row['forca'],
            'constituicao': row['constituicao'],
            'agilidade': row['agilidade'],
            'inteligencia': row['inteligencia']
        }
        
        if row['bonus_json']:
            stats_data['bonus'] = json.loads(row['bonus_json'])
        else:
            stats_data['bonus'] = {}
        
        return stats_data
    
    def _load_inventory(self, entity_id: str) -> Dict[str, Tuple[str, int]]:
        """Carrega o inventário de uma entidade."""
        rows = self.execute_query(
            "SELECT item_name, quantity FROM Inventory WHERE entity_id = ?", (entity_id,)
        )
        
        inventory = {}
        for row in rows:
            item_name = row['item_name']
            quantity = row['quantity']
            inventory[item_name] = (item_name, quantity)
        
        return inventory
    
    def _load_equipment(self, entity_id: str) -> Dict[str, Optional[str]]:
        """Carrega o equipamento de uma entidade."""
        rows = self.execute_query(
            "SELECT slot, item_name FROM Equipment WHERE entity_id = ?", (entity_id,)
        )
        
        equipment = {}
        for row in rows:
            slot = row['slot']
            item_name = row['item_name']
            equipment[slot] = item_name
        
        return equipment
    
    def _load_abilities(self, entity_id: str) -> List[str]:
        """Carrega as habilidades de uma entidade."""
        rows = self.execute_query(
            "SELECT skill_id FROM EntityAbilities WHERE entity_id = ?", (entity_id,)
        )
        
        return [row['skill_id'] for row in rows]
    
    def load_game_state(self) -> Optional[Dict[str, Any]]:
        """Carrega o estado geral do jogo."""
        if not self._cursor:
            print("Erro: conexão com banco não estabelecida.")
            return None
        
        try:
            rows = self.execute_query("SELECT * FROM GameState WHERE id = 1")
            
            if not rows:
                print("Nenhum save encontrado.")
                return None
            
            # Converte sqlite3.Row para dict
            row = rows[0]
            game_state = {
                'id': row['id'],
                'player_id': row['player_id'],
                'current_state': row['current_state'],
                'save_timestamp': row['save_timestamp']
            }
            
            if row['metadata_json']:
                game_state['metadata'] = json.loads(row['metadata_json'])
            else:
                game_state['metadata'] = {}
            
            print(f"Save carregado com sucesso.")
            return game_state
            
        except Exception as e:
            print(f"Erro ao carregar o save: {e}")
            return None
    
    # --- Métodos Utilitários ---
    
    def delete_entity(self, entity_id: str) -> bool:
        """Remove uma entidade e todos os seus dados relacionados."""
        if not self._connection:
            print("Erro: conexão com banco não estabelecida.")
            return False
        
        try:
            # Como temos CASCADE, ao deletar a entidade, todos os dados relacionados serão removidos
            rows_affected = self.execute_command(
                "DELETE FROM Entities WHERE id = ?", (entity_id,)
            )
            
            if rows_affected > 0:
                print(f"Entidade '{entity_id}' deletada.")
                return True
            else:
                print(f"Entidade '{entity_id}' não encontrada.")
                return False
                
        except Exception as e:
            print(f"Erro ao deletar '{entity_id}': {e}")
            self._connection.rollback()
            return False
    
    def list_saved_entities(self, entity_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Lista todas as entidades salvas."""
        if entity_type:
            rows = self.execute_query(
                "SELECT id, nome, raca_id, entity_type, level, current_hp, max_hp FROM Entities WHERE entity_type = ?",
                (entity_type,)
            )
        else:
            rows = self.execute_query(
                "SELECT id, nome, raca_id, entity_type, level, current_hp, max_hp FROM Entities"
            )
        
        # Converte sqlite3.Row para dict manualmente
        result = []
        for row in rows:
            result.append({
                'id': row['id'],
                'nome': row['nome'],
                'raca_id': row['raca_id'],
                'entity_type': row['entity_type'],
                'level': row['level'],
                'current_hp': row['current_hp'],
                'max_hp': row['max_hp']
            })
        return result
    
    def quick_save(self, entity: 'Entity', slot: str = "quicksave") -> bool:
        """Salva rapidamente uma entidade em um slot nomeado."""
        # Adiciona prefixo ao ID para criar slots de salvamento
        original_id = entity.id
        entity.id = f"{slot}_{original_id}"
        
        result = self.save_entity(entity)
        
        # Restaura o ID original
        entity.id = original_id
        
        if result:
            print(f"Quick save feito no slot '{slot}'.")
        
        return result
    
    def quick_load(self, entity_id: str, slot: str = "quicksave") -> Optional[Dict[str, Any]]:
        """Carrega rapidamente uma entidade de um slot nomeado."""
        slotted_id = f"{slot}_{entity_id}"
        data = self.load_entity(slotted_id)
        
        if data:
            print(f"Quick load feito do slot '{slot}'.")
        
        return data

