"""
Interface de Terminal para Sistema RPG
Menu interativo com operações CRUD completas
"""

from managers.data_manager import DataManager
from managers.game_manager import GameManager
from data.entity import Entity, Player, NPC, EntityStats
from data.racas import RACA_CATALOGO
from data.skills import SKILL_CATALOG
from data.items import ITEM_CATALOGO
import os


class Interface:
    def __init__(self):
        self.dm = DataManager()
        self.gm = GameManager()
        self.running = True
    
    def limpar_tela(self):
        """Limpa a tela do terminal."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def mostrar_titulo(self):
        """Mostra o título do sistema."""
        print("\n" + "="*60)
        print(" "*15 + "SISTEMA RPG - GERENCIADOR")
        print("="*60 + "\n")
    
    def pausar(self):
        """Pausa e aguarda o usuário."""
        input("\n[Pressione ENTER para continuar...]")
    
    def menu_principal(self):
        """Menu principal do sistema."""
        while self.running:
            self.limpar_tela()
            self.mostrar_titulo()
            
            print("MENU PRINCIPAL\n")
            print("1. Gerenciar Personagens (CRUD)")
            print("2. Gerenciar Inventário")
            print("3. Sistema de Combate")
            print("4. Salvar/Carregar Jogo")
            print("5. Visualizar Catálogos")
            print("6. Estatísticas")
            print("0. Sair")
            
            opcao = input("\nEscolha uma opção: ").strip()
            
            if opcao == "1":
                self.menu_personagens()
            elif opcao == "2":
                self.menu_inventario()
            elif opcao == "3":
                self.menu_combate()
            elif opcao == "4":
                self.menu_save_load()
            elif opcao == "5":
                self.menu_catalogos()
            elif opcao == "6":
                self.menu_estatisticas()
            elif opcao == "0":
                self.sair()
            else:
                print("\nOpção inválida!")
                self.pausar()
    
    # ===== MENU PERSONAGENS (CRUD) =====
    
    def menu_personagens(self):
        """Menu de gerenciamento de personagens."""
        while True:
            self.limpar_tela()
            self.mostrar_titulo()
            
            print("GERENCIAR PERSONAGENS\n")
            print("1. Criar Novo Personagem (CREATE)")
            print("2. Listar Personagens (READ)")
            print("3. Ver Detalhes de Personagem (READ)")
            print("4. Editar Personagem (UPDATE)")
            print("5. Deletar Personagem (DELETE)")
            print("0. Voltar")
            
            opcao = input("\nEscolha uma opção: ").strip()
            
            if opcao == "1":
                self.criar_personagem()
            elif opcao == "2":
                self.listar_personagens()
            elif opcao == "3":
                self.ver_detalhes_personagem()
            elif opcao == "4":
                self.editar_personagem()
            elif opcao == "5":
                self.deletar_personagem()
            elif opcao == "0":
                break
            else:
                print("\nOpção inválida!")
                self.pausar()
    
    def criar_personagem(self):
        """CREATE - Cria um novo personagem."""
        self.limpar_tela()
        print("=== CRIAR NOVO PERSONAGEM ===\n")
        
        # Nome
        nome = input("Nome do personagem: ").strip()
        if not nome:
            print("Nome inválido!")
            self.pausar()
            return
        
        # Tipo
        print("\nTipo:")
        print("1. Player (Jogador)")
        print("2. NPC")
        tipo = input("Escolha: ").strip()
        
        # Raça
        print("\nRaças disponíveis:")
        racas = list(RACA_CATALOGO.keys())
        for i, raca in enumerate(racas, 1):
            print(f"{i}. {raca}")
        
        try:
            idx_raca = int(input("\nEscolha a raça (número): ")) - 1
            raca_escolhida = RACA_CATALOGO[racas[idx_raca]]
        except:
            print("Raça inválida!")
            self.pausar()
            return
        
        # Stats
        print("\nDefina os atributos (padrão: 5 para cada):")
        try:
            forca = int(input("Força [5]: ") or "5")
            constituicao = int(input("Constituição [5]: ") or "5")
            agilidade = int(input("Agilidade [5]: ") or "5")
            inteligencia = int(input("Inteligência [5]: ") or "5")
        except:
            print("Valores inválidos! Usando padrão (5).")
            forca = constituicao = agilidade = inteligencia = 5
        
        stats = EntityStats(
            forca=forca,
            constituicao=constituicao,
            agilidade=agilidade,
            inteligencia=inteligencia
        )
        
        # Level
        try:
            level = int(input("Level [1]: ") or "1")
        except:
            level = 1
        
        # Criar entidade
        if tipo == "1":
            personagem = Player(
                nome=nome,
                raca=raca_escolhida,
                stats=stats,
                level=level,
                abilities=[SKILL_CATALOG["basic_attack"]]
            )
        else:
            personagem = NPC(
                nome=nome,
                raca=raca_escolhida,
                stats=stats,
                level=level,
                abilities=[SKILL_CATALOG["basic_attack"]]
            )
        
        # Gerar ID único
        import uuid
        personagem.id = f"{tipo}_" + str(uuid.uuid4())[:8]
        
        # Salvar no banco
        if self.dm.save_entity(personagem):
            print(f"\n✓ {personagem.nome} criado com sucesso!")
            print(f"  ID: {personagem.id}")
            print(f"  HP: {personagem.current_hp}/{personagem.max_hp}")
        else:
            print("\nErro ao criar personagem!")
        
        self.pausar()
    
    def listar_personagens(self):
        """READ - Lista todos os personagens."""
        self.limpar_tela()
        print("=== LISTA DE PERSONAGENS ===\n")
        
        entidades = self.dm.list_saved_entities()
        
        if not entidades:
            print("Nenhum personagem cadastrado.")
        else:
            print(f"Total: {len(entidades)} personagens\n")
            for e in entidades:
                print(f"ID: {e['id']}")
                print(f"  Nome: {e['nome']}")
                print(f"  Tipo: {e['entity_type']}")
                print(f"  Raça: {e['raca_id']}")
                print(f"  Level: {e['level']}")
                print(f"  HP: {e['current_hp']}/{e['max_hp']}")
                print()
        
        self.pausar()
    
    def ver_detalhes_personagem(self):
        """READ - Mostra detalhes completos de um personagem."""
        self.limpar_tela()
        print("=== DETALHES DO PERSONAGEM ===\n")
        
        entity_id = input("Digite o ID do personagem: ").strip()
        
        data = self.dm.load_entity(entity_id)
        
        if not data:
            print("\nPersonagem não encontrado!")
        else:
            print(f"\nNome: {data['nome']}")
            print(f"Tipo: {data['entity_type']}")
            print(f"Raça: {data['raca_id']}")
            print(f"Level: {data['level']}")
            print(f"HP: {data['current_hp']}/{data['max_hp']}")
            print(f"Mana: {data['mana']}/{data['mana_maxima']}")
            
            if data['stats']:
                print(f"\nAtributos:")
                print(f"  Força: {data['stats']['forca']}")
                print(f"  Constituição: {data['stats']['constituicao']}")
                print(f"  Agilidade: {data['stats']['agilidade']}")
                print(f"  Inteligência: {data['stats']['inteligencia']}")
                print(f"  Bônus: {data['stats']['bonus']}")
            
            if data['abilities']:
                print(f"\nHabilidades: {', '.join(data['abilities'])}")
            
            if data['inventario']:
                print(f"\nInventário: {len(data['inventario'])} itens")
        
        self.pausar()
    
    def editar_personagem(self):
        """UPDATE - Edita um personagem existente."""
        self.limpar_tela()
        print("=== EDITAR PERSONAGEM ===\n")
        
        entity_id = input("Digite o ID do personagem: ").strip()
        data = self.dm.load_entity(entity_id)
        
        if not data:
            print("\nPersonagem não encontrado!")
            self.pausar()
            return
        
        print(f"\nEditando: {data['nome']}\n")
        print("O que deseja editar?")
        print("1. Level")
        print("2. HP Atual")
        print("3. Atributos")
        print("0. Cancelar")
        
        opcao = input("\nEscolha: ").strip()
        
        if opcao == "1":
            try:
                novo_level = int(input(f"Novo level [atual: {data['level']}]: "))
                # Recriar entidade com novo level
                stats = EntityStats(
                    forca=data['stats']['forca'],
                    constituicao=data['stats']['constituicao'],
                    agilidade=data['stats']['agilidade'],
                    inteligencia=data['stats']['inteligencia']
                )
                
                if data['entity_type'] == 'Player':
                    entity = Player(
                        nome=data['nome'],
                        raca=RACA_CATALOGO[data['raca_id']],
                        stats=stats,
                        level=novo_level,
                        abilities=[SKILL_CATALOG[s] for s in data['abilities']]
                    )
                else:
                    entity = NPC(
                        nome=data['nome'],
                        raca=RACA_CATALOGO[data['raca_id']],
                        stats=stats,
                        level=novo_level,
                        abilities=[SKILL_CATALOG[s] for s in data['abilities']]
                    )
                
                entity.id = entity_id
                entity.current_hp = data['current_hp']
                
                if self.dm.save_entity(entity):
                    print("\n✓ Level atualizado!")
                
            except Exception as e:
                print(f"\nErro: {e}")
        
        elif opcao == "2":
            try:
                novo_hp = int(input(f"Novo HP [atual: {data['current_hp']}, max: {data['max_hp']}]: "))
                
                # Recriar entidade
                stats = EntityStats(
                    forca=data['stats']['forca'],
                    constituicao=data['stats']['constituicao'],
                    agilidade=data['stats']['agilidade'],
                    inteligencia=data['stats']['inteligencia']
                )
                
                if data['entity_type'] == 'Player':
                    entity = Player(
                        nome=data['nome'],
                        raca=RACA_CATALOGO[data['raca_id']],
                        stats=stats,
                        level=data['level'],
                        abilities=[SKILL_CATALOG[s] for s in data['abilities']]
                    )
                else:
                    entity = NPC(
                        nome=data['nome'],
                        raca=RACA_CATALOGO[data['raca_id']],
                        stats=stats,
                        level=data['level'],
                        abilities=[SKILL_CATALOG[s] for s in data['abilities']]
                    )
                
                entity.id = entity_id
                entity.current_hp = min(novo_hp, entity.max_hp)
                
                if self.dm.save_entity(entity):
                    print("\n✓ HP atualizado!")
                
            except Exception as e:
                print(f"\nErro: {e}")
        
        elif opcao == "3":
            print("\nNovos valores de atributos:")
            try:
                forca = int(input(f"Força [atual: {data['stats']['forca']}]: ") or data['stats']['forca'])
                const = int(input(f"Constituição [atual: {data['stats']['constituicao']}]: ") or data['stats']['constituicao'])
                agi = int(input(f"Agilidade [atual: {data['stats']['agilidade']}]: ") or data['stats']['agilidade'])
                inte = int(input(f"Inteligência [atual: {data['stats']['inteligencia']}]: ") or data['stats']['inteligencia'])
                
                stats = EntityStats(forca=forca, constituicao=const, agilidade=agi, inteligencia=inte)
                
                if data['entity_type'] == 'Player':
                    entity = Player(
                        nome=data['nome'],
                        raca=RACA_CATALOGO[data['raca_id']],
                        stats=stats,
                        level=data['level'],
                        abilities=[SKILL_CATALOG[s] for s in data['abilities']]
                    )
                else:
                    entity = NPC(
                        nome=data['nome'],
                        raca=RACA_CATALOGO[data['raca_id']],
                        stats=stats,
                        level=data['level'],
                        abilities=[SKILL_CATALOG[s] for s in data['abilities']]
                    )
                
                entity.id = entity_id
                entity.current_hp = data['current_hp']
                
                if self.dm.save_entity(entity):
                    print("\n✓ Atributos atualizados!")
                
            except Exception as e:
                print(f"\nErro: {e}")
        
        self.pausar()
    
    def deletar_personagem(self):
        """DELETE - Remove um personagem."""
        self.limpar_tela()
        print("=== DELETAR PERSONAGEM ===\n")
        
        entity_id = input("Digite o ID do personagem: ").strip()
        data = self.dm.load_entity(entity_id)
        
        if not data:
            print("\nPersonagem não encontrado!")
            self.pausar()
            return
        
        print(f"\nVocê tem certeza que deseja deletar '{data['nome']}'?")
        confirmacao = input("Digite 'SIM' para confirmar: ").strip().upper()
        
        if confirmacao == "SIM":
            if self.dm.delete_entity(entity_id):
                print(f"\n✓ {data['nome']} foi deletado!")
            else:
                print("\nErro ao deletar!")
        else:
            print("\nOperação cancelada.")
        
        self.pausar()
    
    # ===== MENU INVENTÁRIO =====
    
    def menu_inventario(self):
        """Menu de gerenciamento de inventário."""
        self.limpar_tela()
        print("=== INVENTÁRIO ===\n")
        print("Sistema de inventário disponível no jogo.")
        print("Use o GameManager para gerenciar inventários durante o jogo.")
        self.pausar()
    
    # ===== MENU COMBATE =====
    
    def menu_combate(self):
        """Menu de combate."""
        self.limpar_tela()
        print("=== SISTEMA DE COMBATE ===\n")
        print("Para iniciar um combate, use:")
        print("  gm.trigger_combat(['Raça1', 'Raça2'])")
        self.pausar()
    
    # ===== MENU SAVE/LOAD =====
    
    def menu_save_load(self):
        """Menu de salvar/carregar."""
        while True:
            self.limpar_tela()
            self.mostrar_titulo()
            
            print("SALVAR/CARREGAR JOGO\n")
            print("1. Salvar Estado do Jogo")
            print("2. Carregar Estado do Jogo")
            print("3. Quick Save")
            print("4. Quick Load")
            print("0. Voltar")
            
            opcao = input("\nEscolha uma opção: ").strip()
            
            if opcao == "1":
                self.salvar_jogo()
            elif opcao == "2":
                self.carregar_jogo()
            elif opcao == "3":
                self.quick_save()
            elif opcao == "4":
                self.quick_load()
            elif opcao == "0":
                break
            else:
                print("\nOpção inválida!")
                self.pausar()
    
    def salvar_jogo(self):
        """Salva o estado do jogo."""
        self.limpar_tela()
        print("=== SALVAR JOGO ===\n")
        
        if not self.gm.player:
            print("Nenhum jogador ativo!")
            self.pausar()
            return
        
        metadata = {
            "estado": self.gm.current_state,
            "timestamp": "agora"
        }
        
        if self.dm.save_game_state(self.gm.player, self.gm.current_state, metadata):
            print("\n✓ Jogo salvo com sucesso!")
        else:
            print("\nErro ao salvar!")
        
        self.pausar()
    
    def carregar_jogo(self):
        """Carrega o estado do jogo."""
        self.limpar_tela()
        print("=== CARREGAR JOGO ===\n")
        
        game_state = self.dm.load_game_state()
        
        if game_state:
            print(f"Player ID: {game_state['player_id']}")
            print(f"Estado: {game_state['current_state']}")
            print(f"Salvo em: {game_state['save_timestamp']}")
            print("\n✓ Jogo carregado!")
        else:
            print("Nenhum save encontrado!")
        
        self.pausar()
    
    def quick_save(self):
        """Quick save."""
        self.limpar_tela()
        print("=== QUICK SAVE ===\n")
        
        entity_id = input("ID do personagem: ").strip()
        slot = input("Nome do slot [quicksave]: ").strip() or "quicksave"
        
        data = self.dm.load_entity(entity_id)
        if not data:
            print("\nPersonagem não encontrado!")
            self.pausar()
            return
        
        # Recriar entidade
        stats = EntityStats(
            forca=data['stats']['forca'],
            constituicao=data['stats']['constituicao'],
            agilidade=data['stats']['agilidade'],
            inteligencia=data['stats']['inteligencia']
        )
        
        if data['entity_type'] == 'Player':
            entity = Player(
                nome=data['nome'],
                raca=RACA_CATALOGO[data['raca_id']],
                stats=stats,
                level=data['level'],
                abilities=[SKILL_CATALOG[s] for s in data['abilities']]
            )
        else:
            entity = NPC(
                nome=data['nome'],
                raca=RACA_CATALOGO[data['raca_id']],
                stats=stats,
                level=data['level'],
                abilities=[SKILL_CATALOG[s] for s in data['abilities']]
            )
        
        entity.id = entity_id
        entity.current_hp = data['current_hp']
        
        if self.dm.quick_save(entity, slot):
            print(f"\n✓ Quick save no slot '{slot}'!")
        
        self.pausar()
    
    def quick_load(self):
        """Quick load."""
        self.limpar_tela()
        print("=== QUICK LOAD ===\n")
        
        entity_id = input("ID do personagem: ").strip()
        slot = input("Nome do slot [quicksave]: ").strip() or "quicksave"
        
        data = self.dm.quick_load(entity_id, slot)
        
        if data:
            print(f"\n✓ Carregado do slot '{slot}'!")
            print(f"Nome: {data['nome']}")
            print(f"Level: {data['level']}")
            print(f"HP: {data['current_hp']}/{data['max_hp']}")
        
        self.pausar()
    
    # ===== MENU CATÁLOGOS =====
    
    def menu_catalogos(self):
        """Menu de visualização de catálogos."""
        while True:
            self.limpar_tela()
            self.mostrar_titulo()
            
            print("CATÁLOGOS\n")
            print("1. Raças")
            print("2. Itens")
            print("3. Habilidades")
            print("0. Voltar")
            
            opcao = input("\nEscolha uma opção: ").strip()
            
            if opcao == "1":
                self.ver_racas()
            elif opcao == "2":
                self.ver_itens()
            elif opcao == "3":
                self.ver_habilidades()
            elif opcao == "0":
                break
            else:
                print("\nOpção inválida!")
                self.pausar()
    
    def ver_racas(self):
        """Mostra catálogo de raças."""
        self.limpar_tela()
        print("=== CATÁLOGO DE RAÇAS ===\n")
        
        for nome, raca in RACA_CATALOGO.items():
            print(f"{nome}")
            print(f"  Bônus: FOR+{raca.attributeBonus.get('forca', 0)}, "
                  f"CON+{raca.attributeBonus.get('constituicao', 0)}, "
                  f"AGI+{raca.attributeBonus.get('agilidade', 0)}, "
                  f"INT+{raca.attributeBonus.get('inteligencia', 0)}")
            print(f"  {raca.description}")
            print()
        
        self.pausar()
    
    def ver_itens(self):
        """Mostra catálogo de itens."""
        self.limpar_tela()
        print("=== CATÁLOGO DE ITENS ===\n")
        
        print(f"Total: {len(ITEM_CATALOGO)} itens\n")
        
        for i, (nome, item) in enumerate(ITEM_CATALOGO.items(), 1):
            print(f"{i}. {nome} (Peso: {item.peso})")
            if i % 10 == 0:
                input("\n[Enter para ver mais...]")
        
        self.pausar()
    
    def ver_habilidades(self):
        """Mostra catálogo de habilidades."""
        self.limpar_tela()
        print("=== CATÁLOGO DE HABILIDADES ===\n")
        
        for skill_id, skill in SKILL_CATALOG.items():
            print(f"{skill.nome}")
            print(f"  ID: {skill_id}")
            print(f"  Custo: {skill.cost} | Cooldown: {skill.cooldown}")
            print(f"  Alvo: {skill.target_type}")
            print()
        
        self.pausar()
    
    # ===== ESTATÍSTICAS =====
    
    def menu_estatisticas(self):
        """Mostra estatísticas do sistema."""
        self.limpar_tela()
        print("=== ESTATÍSTICAS ===\n")
        
        entidades = self.dm.list_saved_entities()
        players = [e for e in entidades if e['entity_type'] == 'Player']
        npcs = [e for e in entidades if e['entity_type'] == 'NPC']
        
        print(f"Total de personagens: {len(entidades)}")
        print(f"  Players: {len(players)}")
        print(f"  NPCs: {len(npcs)}")
        print(f"\nRaças disponíveis: {len(RACA_CATALOGO)}")
        print(f"Itens disponíveis: {len(ITEM_CATALOGO)}")
        print(f"Habilidades disponíveis: {len(SKILL_CATALOG)}")
        
        if entidades:
            level_medio = sum(e['level'] for e in entidades) / len(entidades)
            print(f"\nLevel médio: {level_medio:.1f}")
        
        self.pausar()
    
    # ===== SAIR =====
    
    def sair(self):
        """Sai do sistema."""
        self.limpar_tela()
        print("\nEncerrando sistema...")
        self.dm.close()
        self.running = False
        print("Até logo!")


def main():
    """Inicia a interface."""
    interface = Interface()
    interface.menu_principal()


if __name__ == "__main__":
    main()
