#!/usr/bin/env python3

import time
import math
from typing import Optional, List, Dict

# Importações do Textual, incluindo o sistema de Mensagens
from textual.app import App, ComposeResult
from textual.widgets import Static, Footer, Header
from textual.widget import Widget
from textual.reactive import var
from textual.events import Key
from textual.message import Message


# --- 1. Engenharia de Software: Mensagens Customizadas ---

class GameStateChanged(Message):
    """Postado quando o estado do jogo (moedas, itens) muda."""


class NotEnoughCoins(Message):
    """Postado quando uma compra falha."""

    def __init__(self, widget_to_shake: Widget) -> None:
        self.widget_to_shake = widget_to_shake
        super().__init__()


class ItemUnlocked(Message):
    """Postado quando um novo item é desbloqueado."""

    def __init__(self, item_name: str) -> None:
        self.item_name = item_name
        super().__init__()


class PrestigeReset(Message):
    """Postado quando o jogador reseta para prestígio."""


# --- 2. Classes de Estado (com Fórmulas de Game Design) ---

class Player:
    def __init__(self):
        self.coins = 0.0
        self.global_upgrade_level = 1
        # Fator de Prestígio: Começa em 0
        self.prestige_points = 0

    def get_prestige_bonus(self) -> float:
        """Cada ponto de prestígio dá +1% de bônus de produção."""
        return 1.0 + (self.prestige_points * 0.01)

    def reset_for_prestige(self, new_points: int):
        """Reseta o estado para um novo ciclo."""
        self.coins = 0.0
        self.global_upgrade_level = 1
        self.prestige_points += new_points


class Item:
    def __init__(self, id_name: str, name: str, base_cost: int, power: int, cost_multiplier: float,
                 upgrade_cost_base: int, unlock_at: Dict[str, int]):
        self.id_name = id_name
        self.name = name
        self.base_cost = base_cost
        self.cost = base_cost
        self.power = power
        self.cost_multiplier = cost_multiplier
        self.amount = 0

        self.unlocked = (len(unlock_at) == 0)  # Desbloqueado se não houver requisitos
        self.unlock_at = unlock_at  # Ex: {"clicker": 25}

        # Upgrades Específicos
        self.specific_upgrade_level = 0
        self.upgrade_cost_base = upgrade_cost_base  # Adicionado para resetar
        self.specific_upgrade_cost = upgrade_cost_base
        self.specific_upgrade_power_multiplier = 1.5
        self.specific_upgrade_cost_multiplier = 3.0

    def buy(self, coins: float) -> float:
        if coins >= self.cost:
            coins -= self.cost
            self.amount += 1
            self.cost = int(self.base_cost * (self.cost_multiplier ** self.amount))  # Fórmula exponencial mais justa
        return coins

    def buy_specific_upgrade(self, coins: float) -> float:
        if coins >= self.specific_upgrade_cost:
            coins -= self.specific_upgrade_cost
            self.specific_upgrade_level += 1
            self.specific_upgrade_cost = int(self.specific_upgrade_cost * self.specific_upgrade_cost_multiplier)
        return coins

    def get_synergy_bonus(self, all_items: Dict[str, 'Item']) -> float:
        """Fórmula de Sinergia: Itens afetam outros itens."""
        bonus = 1.0
        if self.id_name == "minerador" and "clicker" in all_items:
            # Mineradores ganham +10% de bônus para cada 25 Clickers
            clicker_count = all_items["clicker"].amount
            bonus += (clicker_count // 25) * 0.10
        return bonus

    def income(self, player: Player, all_items: Dict[str, 'Item']) -> int:
        if self.amount == 0:
            return 0

        base_production = self.amount * self.power
        specific_bonus = self.specific_upgrade_power_multiplier ** self.specific_upgrade_level
        global_bonus = (1.5 ** (player.global_upgrade_level - 1))
        synergy_bonus = self.get_synergy_bonus(all_items)

        # Bônus final de Prestígio aplicado a tudo
        prestige_bonus = player.get_prestige_bonus()

        return int(base_production * specific_bonus * global_bonus * synergy_bonus * prestige_bonus)

    def reset_for_prestige(self):
        """Reseta o item para um novo ciclo."""
        self.amount = 0
        self.cost = self.base_cost
        self.specific_upgrade_level = 0
        self.specific_upgrade_cost = self.upgrade_cost_base
        self.unlocked = (len(self.unlock_at) == 0)

    def __str__(self):
        s_cost = f"{self.cost:,}".replace(",", ".")
        s_power = f"{self.power:,}".replace(",", ".")
        return f"{self.name} (x{self.amount}) | +{s_power}/s | Custo: {s_cost}"


# --- 3. O "Motor" do Jogo (Lógica Pura) ---

class GameEngine:
    """Classe não-visual que contém todo o estado e lógica do jogo."""

    def __init__(self, app: App):
        self.app = app  # Para poder postar mensagens
        self.player = Player()
        self.items = {
            "clicker": Item("clicker", "Clicker", 15, 1, 1.15, 100, {}),
            "minerador": Item("minerador", "Minerador", 200, 8, 1.20, 1000, {"clicker": 25}),
            "fabrica": Item("fabrica", "Fábrica", 5000, 50, 1.25, 10000, {"minerador": 25})
        }
        self.last_time = time.time()
        self.upgrade_keys = {'a': 'clicker', 's': 'minerador', 'd': 'fabrica'}
        self.item_keys = {'1': 'clicker', '2': 'minerador', '3': 'fabrica'}

    def update_income(self) -> None:
        """Calcula a renda e posta uma atualização de estado."""
        now = time.time()
        delta = now - self.last_time
        self.last_time = now  # Atualiza o tempo mesmo se não houver renda
        if delta > 0:
            income_per_second = sum(item.income(self.player, self.items) for item in self.items.values())
            if income_per_second > 0:
                self.player.coins += income_per_second * delta
                self.app.post_message(GameStateChanged())

    def click_coin(self) -> None:
        self.player.coins += 1
        self.app.post_message(GameStateChanged())

    def buy_item(self, item_id: str, source_widget: Widget):
        if item_id not in self.items: return

        item = self.items[item_id]
        if not item.unlocked: return

        if self.player.coins >= item.cost:
            self.player.coins = item.buy(self.player.coins)
            self.check_unlocks()
            self.app.post_message(GameStateChanged())
        else:
            self.app.post_message(NotEnoughCoins(source_widget))

    def buy_specific_upgrade(self, item_id: str, source_widget: Widget):
        if item_id not in self.items: return

        item = self.items[item_id]
        if not item.unlocked: return

        if self.player.coins >= item.specific_upgrade_cost:
            self.player.coins = item.buy_specific_upgrade(self.player.coins)
            self.app.post_message(GameStateChanged())
        else:
            self.app.post_message(NotEnoughCoins(source_widget))

    def get_global_upgrade_cost(self) -> int:
        return 1000 * (4 ** (self.player.global_upgrade_level - 1))

    def buy_global_upgrade(self, source_widget: Widget):
        cost = self.get_global_upgrade_cost()
        if self.player.coins >= cost:
            self.player.coins -= cost
            self.player.global_upgrade_level += 1
            self.app.post_message(GameStateChanged())
        else:
            self.app.post_message(NotEnoughCoins(source_widget))

    def check_unlocks(self):
        """Verifica se novos itens podem ser desbloqueados."""
        for item in self.items.values():
            if not item.unlocked:
                can_unlock = True
                for req_id, req_amount in item.unlock_at.items():
                    if self.items[req_id].amount < req_amount:
                        can_unlock = False
                        break
                if can_unlock:
                    item.unlocked = True
                    self.app.post_message(ItemUnlocked(item.name))

    def calculate_prestige_gain(self) -> int:
        """Fórmula de Prestígio: logarítmica."""
        if self.player.coins < 1_000_000:
            return 0
        # A cada "ordem de magnitude" (10x) acima de 1M, você ganha pontos
        gain = int(math.log10(self.player.coins / 1_000_000) * 5)
        return max(0, gain)

    def do_prestige_reset(self):
        """Executa o reset de prestígio."""
        gain = self.calculate_prestige_gain()
        if gain > 0:
            self.player.reset_for_prestige(gain)
            for item in self.items.values():
                item.reset_for_prestige()
            self.app.post_message(PrestigeReset())
            self.app.post_message(GameStateChanged())


# --- 4. Widgets de UI (A "View") ---
# Eles não têm lógica de jogo, apenas reagem a mensagens.

class StatsDisplay(Static):
    """Exibe Moedas, Renda e Bônus de Prestígio."""

    def on_mount(self) -> None:
        self.border_title = "📊 Estatísticas"
        self.update_render(self.app.engine)  # Render inicial

    def on_game_state_changed(self, message: GameStateChanged) -> None:
        """Assina a mensagem e atualiza o render."""
        self.update_render(self.app.engine)
        # "Juice": Pisca o painel
        self.add_class("highlight")
        self.set_timer(0.3, lambda: self.remove_class("highlight"))

    def on_prestige_reset(self, message: PrestigeReset) -> None:
        """Atualiza no reset."""
        self.update_render(self.app.engine)

    def update_render(self, engine: GameEngine):
        """Lógica de renderização."""
        player = engine.player
        items = engine.items

        total_income = sum(item.income(player, items) for item in items.values())
        s_coins = f"{int(player.coins):,}".replace(",", ".")
        s_income = f"{total_income:,}".replace(",", ".")
        bonus = (1.5 ** (player.global_upgrade_level - 1))
        prestige_bonus = player.get_prestige_bonus()

        output_lines = [
            f"Moedas: {s_coins}",
            f"Renda por segundo: {s_income}",
            f"Bônus Global: x{bonus:.2f}",
            f"Bônus de Prestígio: x{prestige_bonus:.2f} ({player.prestige_points} pontos)"
        ]
        self.update("\n".join(output_lines))


class ItemsDisplay(Static):
    """Exibe os Itens e Upgrades."""

    def on_mount(self) -> None:
        self.border_title = "🏪 Loja de Itens"
        self.update_render(self.app.engine)

    def on_game_state_changed(self, message: GameStateChanged) -> None:
        self.update_render(self.app.engine)

    def on_prestige_reset(self, message: PrestigeReset) -> None:
        self.update_render(self.app.engine)

    def on_not_enough_coins(self, message: NotEnoughCoins) -> None:
        """"Juice": Tremer o painel se a compra falhar."""
        if message.widget_to_shake == self:
            self.add_class("shake")
            self.set_timer(0.4, lambda: self.remove_class("shake"))

    def update_render(self, engine: GameEngine):
        player = engine.player
        items = engine.items
        upgrade_keys = engine.upgrade_keys

        output_lines = ["Itens disponíveis:"]

        for i, (item_id, item) in enumerate(items.items(), 1):
            if not item.unlocked:
                # Mostra o requisito de desbloqueio
                req_id, req_amount = next(iter(item.unlock_at.items()))
                req_name = items[req_id].name
                output_lines.append(f"[{i}] ??? (Requer {req_amount} {req_name}s)")
                continue

            # Item está desbloqueado
            affordable = "(Pode comprar!)" if player.coins >= item.cost else ""
            output_lines.append(f"[{i}] {item} {affordable}")

            upg_key = [k for k, v in upgrade_keys.items() if v == item_id][0].upper()
            upg_cost = item.specific_upgrade_cost
            upg_level = item.specific_upgrade_level
            upg_bonus = item.specific_upgrade_power_multiplier ** upg_level
            upg_affordable = "(Pode!)" if player.coins >= upg_cost else ""
            s_upg_cost = f"{upg_cost:,}".replace(",", ".")

            output_lines.append(f"    [{upg_key}] Upg. Específico (Nível {upg_level}, Bônus: x{upg_bonus:.1f})")
            output_lines.append(f"        Custo: {s_upg_cost} {upg_affordable}")

        # Upgrade Global
        upgrade_cost = engine.get_global_upgrade_cost()
        can_upgrade = "(Pode comprar!)" if player.coins >= upgrade_cost else ""
        s_g_upg_cost = f"{upgrade_cost:,}".replace(",", ".")
        output_lines.append(f"\n[U] Upgrade Global (Custo: {s_g_upg_cost}) {can_upgrade}")

        self.update("\n".join(output_lines))


class PrestigeDisplay(Static):
    """Exibe as informações de Prestígio."""

    def on_mount(self) -> None:
        self.border_title = "✨ Prestígio"
        self.update_render(self.app.engine)

    def on_game_state_changed(self, message: GameStateChanged) -> None:
        self.update_render(self.app.engine)

    def on_prestige_reset(self, message: PrestigeReset) -> None:
        self.update_render(self.app.engine)

    def on_not_enough_coins(self, message: NotEnoughCoins) -> None:
        if message.widget_to_shake == self:
            self.add_class("shake")
            self.set_timer(0.4, lambda: self.remove_class("shake"))

    def update_render(self, engine: GameEngine):
        prestige_gain = engine.calculate_prestige_gain()

        if prestige_gain > 0:
            self.remove_class("hidden")  # Mostra o painel
            self.update(
                f"Você pode resetar agora para ganhar {prestige_gain} Pontos de Prestígio.\n"
                f"Isso irá resetar seu jogo, mas dará um bônus permanente de +{prestige_gain}% na produção!\n\n"
                f"[P] Fazer Prestígio!"
            )
        else:
            self.add_class("hidden")  # Esconde o painel
            self.update("Alcance 1.000.000 de moedas para desbloquear o Prestígio.")


# --- 5. A Aplicação (O "Controlador") ---

class IncrementalGameApp(App):
    """A aplicação Textual que junta tudo."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # O engine é agora uma propriedade DA INSTÂNCIA
        self.engine = GameEngine(self)

    # REMOVIDA a definição de 'engine' no nível da classe.

    BINDINGS = [
        ("1", "buy_item('1')", "Item 1"),
        ("2", "buy_item('2')", "Item 2"),
        ("3", "buy_item('3')", "Item 3"),
        ("a", "buy_specific('a')", "Upg. 1"),
        ("s", "buy_specific('s')", "Upg. 2"),
        ("d", "buy_specific('d')", "Upg. 3"),
        ("u", "buy_global", "Upg. Global"),
        ("p", "prestige", "Prestígio"),
        ("space", "click_coin", "Clicar"),  # Mantido no BINDINGS
        ("q", "quit", "Sair"),
    ]

    # CSS com "Juice": Animações de 'highlight' e 'shake'
    CSS = """
    Screen { layout: vertical; }
    Header { dock: top; }
    Footer { dock: bottom; }

    GameContainer {
        width: 100%;
        height: 1fr;
        layout: vertical;
    }

    StatsDisplay {
        width: 100%;
        height: 6;
        border: round white;
        padding: 1;
        margin-bottom: 1;
        /* Transição suave para a cor de fundo */
        transition: background 0.3s;
    }

    /* Animação de 'highlight' */
    StatsDisplay.highlight {
        background: $accent-lighten-2;
    }

    ItemsDisplay {
        width: 100%;
        height: 1fr;
        border: round white;
        padding: 1;
    }

    PrestigeDisplay {
        width: 100%;
        height: 6;
        border: round $warning;
        padding: 1;
        margin-top: 1;
    }

    /* Esconde o widget de prestígio por padrão */
    PrestigeDisplay.hidden {
        display: none;
    }

    /* Animação 'shake' para erros */
    .shake {
        border: round $error;
    }
    """

    # GameWidget foi renomeado para GameContainer para clareza
    class GameContainer(Widget):
        """Container que simplesmente organiza os widgets de UI."""

        def compose(self) -> ComposeResult:
            yield StatsDisplay()
            yield ItemsDisplay()
            yield PrestigeDisplay()

    def compose(self) -> ComposeResult:
        """Cria os widgets da UI."""
        yield Header(name="=== 💰 Meu Jogo Incremental v2.0 ===")
        yield self.GameContainer()  # Instancia o container
        yield Footer()

    def on_mount(self) -> None:
        """Inicia o 'game loop' do engine."""
        self.set_interval(1 / 20, self.engine.update_income)

    # --- Handlers de Mensagens (para Notificações) ---

    def on_item_unlocked(self, message: ItemUnlocked) -> None:
        """"Juice": Mostra uma notificação."""
        self.notify(f"Novo item desbloqueado: {message.item_name}!", title="Promoção!")

    def on_prestige_reset(self, message: PrestigeReset) -> None:
        self.notify("Prestígio realizado!", title="✨ Renascimento!", severity="success")

    def on_not_enough_coins(self, message: NotEnoughCoins) -> None:
        self.notify("Moedas insuficientes!", title="Compra Falhou", severity="error")

    # --- Ações (delegam para o Engine) ---

    def action_buy_item(self, key: str) -> None:
        if item_id := self.engine.item_keys.get(key):
            self.engine.buy_item(item_id, self.query_one(ItemsDisplay))

    def action_buy_specific(self, key: str) -> None:
        if item_id := self.engine.upgrade_keys.get(key):
            self.engine.buy_specific_upgrade(item_id, self.query_one(ItemsDisplay))

    def action_buy_global(self) -> None:
        self.engine.buy_global_upgrade(self.query_one(ItemsDisplay))

    def action_prestige(self) -> None:
        self.engine.do_prestige_reset()

    def action_click_coin(self) -> None:
        """Clica na moeda para ganhar 1 moeda."""
        self.engine.click_coin()

    # REMOVIDO o handler on_key.
    # O BINDINGS para "space" agora é a única fonte da verdade,
    # e ele lida nativamente com a repetição de teclas.


if __name__ == "__main__":
    app = IncrementalGameApp()
    app.run()

