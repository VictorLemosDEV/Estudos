from typing import Protocol, List, Dict, Callable
from utils.attribute_calculator import hp_calculator
from data.racas import IRaca, Raca, RACA_CATALOGO
from data.items import Item
from data.skills import Skill

# INTERFACES



class IFiliacao(Protocol):
    membro: Entity
    level: int
    
class IStats(Protocol):
    _forca: ObservableStat
    _constituicao: ObservableStat
    _agilidade: ObservableStat
    _inteligencia: ObservableStat
    
    bonus: Dict[str, int]
    

class ObservableStat:
    """Descritor que adiciona lógica de observação a um atributo."""
    
    def __init__(self, valor_inicial=1):
        self._valor_inicial = valor_inicial
        # O nome real do atributo na instância será definido em __set_name__
        self.nome_atributo_interno = None 

    def __set_name__(self, owner, name):
        # Define o nome da variável privada (ex: _forca, _constituicao)
        self.nome_atributo_interno = f'_{name}' 

    def __get__(self, instance, owner):
        # Retorna o valor atual da instância
        if instance is None:
            return self
        # Pega o valor do dicionário interno da instância (ex: instance.__dict__['_constituicao'])
        return instance.__dict__.get(self.nome_atributo_interno, self._valor_inicial)

    def __set__(self, instance, novo_valor):
        # Pega o valor antigo para comparação
        valor_antigo = self.__get__(instance, owner=None)
        
        if novo_valor != valor_antigo:
            # 1. Atualiza o valor na instância
            instance.__dict__[self.nome_atributo_interno] = novo_valor
            
            # 2. Notifica a instância principal (PersonagemStats)
            # O 'instance' aqui é o objeto PersonagemStats que possui o descritor
            instance._notify_observers(
                attribute_name=self.nome_atributo_interno.strip('_'), # 'constituicao'
                old=valor_antigo, 
                new=novo_valor
            )
            
    

# --------------------

# Implementações das Intefaces


class EntityStats():
    
    forca = ObservableStat(valor_inicial=1)
    constituicao = ObservableStat(valor_inicial=1)
    agilidade = ObservableStat(valor_inicial=1)
    inteligencia = ObservableStat(valor_inicial=1)

    def __init__(self, **kwargs):
        self._observers: List[Callable] = []
        self.bonus: Dict[str, int] = {}
        
        
        for stat, valor in kwargs.items():
            if hasattr(self, stat) and stat != 'bonus':
                setattr(self, stat, valor)
            elif stat == 'bonus':
                self.bonus = valor
            
        
        
    def register_observer(self, observer_func):
        if observer_func not in self._observers:
            self._observers.append(observer_func)
            print(f"-> Observer {observer_func.__name__} registrado.")
            
    def _notify_observers(self, attribute_name: str, old: int, new: int):
        for observer in self._observers:
            observer(attribute_name, old, new)
            
            

    
    
   

#----------------------------------------------

class Entity:
    def __init__(self, nome: str, raca: IRaca,stats: EntityStats = EntityStats(), level: int = 1, filiacaoLista: List[IFiliacao] = [], inventario = [], abilities: List['Skill'] = []):
        self.initialized = False
        self.id: str = ""
        self.nome = nome
        self.raca = raca
        self.level = level
        self.stats = stats
        self.filiacoes = filiacaoLista
        self.inventario = inventario
        self.equipment: Dict[str, Item | None]
        
        self.abilities: List['Skill'] = abilities
        
        
        # Calculando Atributos Dinamicos
        self.vida_maxima =  hp_calculator(self.stats.constituicao)
        self.vida_atual = self.vida_maxima
        self.mana_maxima = 100
        self.mana = self.mana_maxima
        
        
        self.ApplyRaceBonus()
        
        
        
        self.stats.register_observer(self.recalc_attributes)
        
        self.initialized = True
        
        
    def is_alive(self):
        return self.vida_atual > 0
    
    def take_damage(self, damage):
        self.vida_atual -= damage
        print(f"{self.nome} sofreu {damage} de dano. HP restante: {self.vida_atual}")
        if not self.is_alive():
            print(f"{self.nome} foi derrotado!")
            
    def choose_action(self, manager):
        raise NotImplementedError("Ação deve ser escolhida por Player ou NPC.")
        
        targets = [p for p in manager.participants if p.is_alive() and p is not self]
        
        if targets:
            target = targets[0]
            damage = self.stats.forca
            print(f"{self.nome} ataca {target.nome} causando {damage} de dano.")
            target.take_damage(damage)
        else:
            print(f"{self.nome} não tem alvos.")
        
        
    def ApplyRaceBonus(self):
        if len(self.raca.attributeBonus) <= 0:
            return
        
        
        for stat, bonus in self.raca.attributeBonus.items():
            if self.stats.bonus.get(stat, None):
                self.stats.bonus[stat] += bonus
            else:
                self.stats.bonus[stat] = bonus
                
                
            if hasattr(self.stats, stat):
                old = getattr(self.stats,stat)
                setattr(self.stats, stat, old + bonus)
    
        
    def recalc_attributes(self, attribute_name: str, old: int, new: int):
        if attribute_name == "constituicao":
            if self.vida_atual == self.vida_maxima:
                self.vida_maxima = hp_calculator(self.stats.constituicao)
                self.vida_atual = self.vida_maxima
            else:
                self.vida_maxima = hp_calculator(self.stats.constituicao)
            
    
    def level_up(self):
        self.level += 1
        
        
        
        for stat, bonus in self.raca.attributeBonus.items():
            if self.stats.bonus.get(stat, None):
                self.stats.bonus[stat] += bonus
            else:
                self.stats.bonus[stat] = bonus
                
                
            if hasattr(self.stats, stat):
                old = getattr(self.stats,stat)
                setattr(self.stats, stat, old + bonus)
        
            

class NPC(Entity):
    def choose_action(self, combat_manager):
        return combat_manager.npc_choose_ability(self)

class Player(Entity):
   def choose_action(self, combat_manager):
        # Implementação da escolha do usuário
        return combat_manager.player_choose_ability(self)
