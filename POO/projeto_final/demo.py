"""
DEMO - Sistema RPG com CRUD e POO
"""

from managers.data_manager import DataManager
from managers.game_manager import GameManager
from managers.dialogue_manager import DialogueManager
from managers.combat_manager import CombatManager
from managers.inventory_manager import InventoryManager
from managers.attribute_manager import AttributeManager
from data.entity import Entity, Player, NPC, EntityStats
from data.racas import RACA_CATALOGO
from data.skills import SKILL_CATALOG
from data.items import ITEM_CATALOGO, copper_sword

from time import sleep


def separador(titulo=""):
    print(f"\n{'='*60}")
    if titulo:
        print(f"  {titulo}")
        print("="*60)
    print()


def pausar():
    input("[Enter para continuar...]")


# ===== CONCEITOS DE POO =====

def demo_poo():
    separador("1. POO GOOOO BRRRRRRR")
    
    print("HERANÇA: Entity -> Player, NPC")
    print("POLIMORFISMO: choose_action() diferente em cada classe")
    print("ENCAPSULAMENTO: ObservableStat com descritores")
    print("SINGLETON: DataManager, GameManager")
    print("OBSERVER: EntityStats notifica mudanças")
    
    print("\n--- Criando Player e NPC ---")
    player = Player(
        nome="Herói",
        raca=RACA_CATALOGO["Humano"],
        stats=EntityStats(forca=5, constituicao=4, agilidade=3, inteligencia=2),
        abilities=[SKILL_CATALOG["basic_attack"]]
    )
    player.id = "player_1"
    print(f"✓ {player.nome} criado | Tipo: {type(player).__name__} | HP: {player.current_hp}")
    
    npc = NPC(
        nome="Goblin",
        raca=RACA_CATALOGO["Gnomo Inventor"],
        stats=EntityStats(forca=3, constituicao=3),
        abilities=[SKILL_CATALOG["basic_attack"]]
    )
    npc.id = "npc_1"
    print(f"✓ {npc.nome} criado | Tipo: {type(npc).__name__} | HP: {npc.current_hp}")
    
    print("\n--- Padrão Observer ---")
    print(f"Constituição: {player.stats.constituicao} | HP máximo: {player.max_hp}")
    player.stats.constituicao = 8
    print(f"Mudou para: {player.stats.constituicao} | HP máximo: {player.max_hp} (recalculado)")
    
    
    
    
    pausar()
    return player, npc


# ===== CRUD =====

def demo_crud(dm, player, npc):
    separador("2. CRUD COMPLETO")
    
    # CREATE
    print("CREATE - Salvando no banco...")
    dm.save_entity(player)
    dm.save_entity(npc)
    dm.save_game_state(player, "DEMO", {"versao": "1.0"})
    print("✓ Dados salvos")
    
    # READ
    print("\nREAD - Lendo do banco...")
    entidades = dm.list_saved_entities()
    print(f"Total: {len(entidades)} entidades")
    for e in entidades:
        print(f"  • {e['nome']} (Lvl {e['level']}) - HP: {e['current_hp']}/{e['max_hp']}")
    
    player_data = dm.load_entity("player_1")
    print(f"\nDados de {player_data['nome']}:")
    print(f"  Raça: {player_data['raca_id']}")
    print(f"  Stats: FOR={player_data['stats']['forca']}, CON={player_data['stats']['constituicao']}")
    
    # UPDATE
    print("\nUPDATE - Atualizando dados...")
    player.level = 2
    player.current_hp -= 10
    dm.save_entity(player)
    print(f"✓ {player.nome} agora é lvl {player.level} com {player.current_hp} HP")
    
    # DELETE
    print("\nDELETE - Removendo NPC...")
    dm.delete_entity("npc_1")
    entidades = dm.list_saved_entities()
    print(f"✓ Restam {len(entidades)} entidades")
    
    pausar()


# ===== MANAGERS =====

def demo_managers():
    separador("3. GERENCIADORES (MANAGERS)")
    
    print("--- GameManager (Singleton) ---")
    gm = GameManager()
    print(f"✓ Player: {gm.player.nome}")
    print(f"  Estado: {gm.current_state}")
    
    print("\n--- AttributeManager ---")
    am = AttributeManager()
    stats_finais = am.calculate_final_stats(gm.player)
    print(f"✓ Stats finais calculados")
    print(f"  Força: {stats_finais.get('strength')}")
    print(f"  Vida máxima: {stats_finais.get('vida_maxima')}")
    
    print("\n--- InventoryManager ---")
    im = InventoryManager()
    gm.player.inventario = {}
    im.add_item(gm.player, copper_sword, 1)
    inv = im.get_inventory(gm.player)
    print(f"✓ Inventário tem {len(inv)} itens")
    for item_id, (item, qty) in inv.items():
        print(f"  • {item.nome} x{qty}")
    
    print("\n--- DialogueManager ---")
    dlg = DialogueManager()
    print("✓ Sistema de diálogos disponível")

    print(f"  Exemplo: dlg.showDialogue('tutorial.1')")
    
    dlg.showDialogue("tutorial.1")
    
    
    pausar()


# ===== QUICK SAVE/LOAD =====

def demo_quicksave(dm):
    separador("4. QUICK SAVE/LOAD")
    
    print("Criando personagem teste...")
    char = Player(
        nome="Quick Test",
        raca=RACA_CATALOGO["Dragão"],
        stats=EntityStats(forca=10, constituicao=8),
        level=5
    )
    char.id = "quicktest"
    char.current_hp = 50
    print(f"✓ {char.nome} | Lvl {char.level} | HP: {char.current_hp}")
    
    print("\nQuick Save slot 'save1'...")
    dm.quick_save(char, slot="save1")
    
    print("\nModificando personagem...")
    char.level = 10
    char.current_hp = 20
    print(f"  Agora: Lvl {char.level} | HP: {char.current_hp}")
    
    print("\nQuick Load slot 'save1'...")
    loaded = dm.quick_load("quicktest", slot="save1")
    print(f"✓ Carregado: Lvl {loaded['level']} | HP: {loaded['current_hp']}")
    
    dm.delete_entity("save1_quicktest")
    pausar()


# ===== CATÁLOGO =====

def demo_catalogo():
    separador("5. CATÁLOGOS")
    
    print(f"RAÇAS: {len(RACA_CATALOGO)} disponíveis")
    for nome in list(RACA_CATALOGO.keys())[:5]:
        raca = RACA_CATALOGO[nome]
        print(f"  • {nome}: FOR+{raca.attributeBonus.get('forca', 0)}")
    
    print(f"\nITENS: {len(ITEM_CATALOGO)} disponíveis")
    for nome in list(ITEM_CATALOGO.keys())[:5]:
        item = ITEM_CATALOGO[nome]
        print(f"  • {nome}: Peso {item.peso}")
    
    print(f"\nSKILLS: {len(SKILL_CATALOG)} disponíveis")
    for skill_id in list(SKILL_CATALOG.keys())[:5]:
        skill = SKILL_CATALOG[skill_id]
        print(f"  • {skill.nome}: Custo {skill.cost}")
    
    pausar()


# ===== RESUMO =====

def demo_resumo():
    separador("RESUMO")
    
    print("✓ POO:")
    print("  • Herança, Polimorfismo, Encapsulamento")
    print("  • Singleton, Observer")
    
    print("\n✓ CRUD:")
    print("  • CREATE: save_entity(), save_game_state()")
    print("  • READ: load_entity(), list_saved_entities()")
    print("  • UPDATE: save_entity() com dados modificados")
    print("  • DELETE: delete_entity()")
    
    print("\n✓ MANAGERS:")
    print("  • DataManager: Persistência")
    print("  • GameManager: Estado do jogo")
    print("  • AttributeManager: Cálculo de atributos")
    print("  • InventoryManager: Itens")
    print("  • DialogueManager: Diálogos")
    print("  • CombatManager: Combate")
    
    print("\n✓ EXTRAS:")
    print("  • Quick Save/Load")
    print("  • SQLite com Foreign Keys")
    print("  • JSON para dados complexos")
    
    print("\n" + "="*60)


def main():
    print("\n" + "="*60)
    print(" "*20 + "DEMO - SISTEMA RPG")
    print("="*60)
    
    try:
        # Limpa banco antigo
        import os
        if os.path.exists("rpg_game_data.db"):
            os.remove("rpg_game_data.db")
        
        player, npc = demo_poo()
        
        dm = DataManager()
        demo_crud(dm, player, npc)
        demo_managers()
        demo_quicksave(dm)
        demo_catalogo()
        demo_resumo()
        
        print("\nLimpando dados da demo...")
        dm.delete_entity("player_1")
        dm.delete_entity("demo_observer")
        dm.close()
        
        print("✓ DEMO concluída!")
        
    except Exception as e:
        print(f"\nErro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
