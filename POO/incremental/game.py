# game.py
import time
from typing import Optional
from utils import get_key, clear_screen  # Importa as funções do nosso arquivo


# --- Classes de Estado ---
class Player:
    def __init__(self):
        self.coins = 0
        self.global_upgrade_level = 1


class Item:
    def __init__(self, name: str, base_cost: int, power: int, cost_multiplier: float, upgrade_cost_base: int):
        self.name = name
        self.base_cost = base_cost
        self.cost = base_cost
        self.power = power
        self.cost_multiplier = cost_multiplier
        self.amount = 0

        # --- Variáveis de Upgrade Específico ---
        self.specific_upgrade_level = 0  # Começa no nível 0
        self.specific_upgrade_cost = upgrade_cost_base
        self.specific_upgrade_power_multiplier = 1.5  # Cada upgrade dá +50% de bônus
        self.specific_upgrade_cost_multiplier = 3.0  # Custo do próximo upgrade triplica

    def buy(self, coins: int) -> int:
        if coins >= self.cost:
            coins -= self.cost
            self.amount += 1
            self.cost = int(self.cost * self.cost_multiplier)
        return coins

    # --- Método para comprar upgrade específico ---
    def buy_specific_upgrade(self, coins: int) -> int:
        if coins >= self.specific_upgrade_cost:
            coins -= self.specific_upgrade_cost
            self.specific_upgrade_level += 1
            # Aumenta o custo para o próximo nível
            self.specific_upgrade_cost = int(self.specific_upgrade_cost * self.specific_upgrade_cost_multiplier)
        return coins

    # --- Renda agora inclui o bônus específico ---
    def income(self, player: Player) -> int:
        base_production = self.amount * self.power

        # Bônus do Nível 0 é 1.5^0 = 1x (sem bônus)
        specific_bonus = self.specific_upgrade_power_multiplier ** self.specific_upgrade_level

        # Bônus global (Nível 1 não dá bônus, Nível 2 dá 1.5x)
        global_bonus = (1.5 ** (player.global_upgrade_level - 1))

        return int(base_production * specific_bonus * global_bonus)

    def progress_bar(self, length=20) -> str:
        """Visual bar showing amount relative to 50 items (arbitrário)."""
        filled = min(self.amount, 50)
        return "█" * int(filled / 50 * length) + "-" * (length - int(filled / 50 * length))

    def __str__(self):
        return f"{self.name}: {self.amount} | +{self.power}/s | Custo: {self.cost}"


# --- Classe Principal do Jogo ---
class Game:
    def __init__(self):
        self.player = Player()
        # --- Passa o custo base do primeiro upgrade específico ---
        self.items = [
            Item("Clicker", 15, 1, 1.15, 100),  # Upg. custa 100
            Item("Minerador", 200, 8, 1.20, 1000),  # Upg. custa 1000
            Item("Fábrica", 5000, 50, 1.25, 10000)  # Upg. custa 10000
        ]
        self.last_time = time.time()
        self.running = True

        # --- Mapeamento de teclas para os upgrades ---
        self.upgrade_keys = ['a', 's', 'd']  # Teclas para upgrades dos itens 1, 2, 3

    def get_global_upgrade_cost(self) -> int:
        """Centraliza o cálculo do custo do upgrade global."""
        # Custo base 1000, multiplicador 4x por nível
        return 1000 * (4 ** (self.player.global_upgrade_level - 1))

    def display(self):
        """Renderiza o estado atual do jogo no terminal."""
        clear_screen()
        total_income = sum(item.income(self.player) for item in self.items)

        print("=== 💰 Incremental Game ===")
        print(f"Moedas: {int(self.player.coins):,}".replace(",", "."))
        print(f"Renda por segundo: {total_income:,}".replace(",", "."))

        bonus = (1.5 ** (self.player.global_upgrade_level - 1))
        print(f"Bônus Global: x{bonus:.2f}\n")

        print("Itens disponíveis:")
        for i, item in enumerate(self.items, 1):
            affordable = "(Pode comprar!)" if self.player.coins >= item.cost else ""
            print(f"[{i}] {item} {affordable}")
            print(f"    {item.progress_bar()}")

            # --- Mostra informações do upgrade específico ---
            if i - 1 < len(self.upgrade_keys):
                upg_key = self.upgrade_keys[i - 1].upper()
                upg_cost = item.specific_upgrade_cost
                upg_level = item.specific_upgrade_level
                upg_bonus = item.specific_upgrade_power_multiplier ** upg_level
                upg_affordable = "(Pode!)" if self.player.coins >= upg_cost else ""

                print(f"    [{upg_key}] Upg. Específico (Nível {upg_level}, Bônus: x{upg_bonus:.1f})")
                print(f"        Custo: {upg_cost:,} {upg_affordable}".replace(",", "."))

        upgrade_cost = self.get_global_upgrade_cost()
        can_upgrade = "(Pode comprar!)" if self.player.coins >= upgrade_cost else ""
        print(f"\n[U] Upgrade Global (Custo: {upgrade_cost:,}) {can_upgrade}".replace(",", "."))

        # --- Texto de ajuda atualizado ---
        print("\n[Espaço] = +1 moeda | [1-3] = Comprar Item | [A,S,D] = Upg. Item | [U] = Upg. Global | [Q] = Sair")

    def update_income(self):
        """Calcula e adiciona a renda passiva baseada no tempo delta."""
        now = time.time()
        delta = now - self.last_time
        if delta > 0:
            income_per_second = sum(item.income(self.player) for item in self.items)
            self.player.coins += income_per_second * delta
        self.last_time = now

    def buy_item(self, index: int):
        if 0 <= index < len(self.items):
            self.player.coins = self.items[index].buy(int(self.player.coins))

    def buy_global_upgrade(self):
        cost = self.get_global_upgrade_cost()
        if self.player.coins >= cost:
            self.player.coins -= cost
            self.player.global_upgrade_level += 1

    # --- Método para comprar upgrade específico por índice ---
    def buy_specific_upgrade(self, index: int):
        if 0 <= index < len(self.items):
            self.player.coins = self.items[index].buy_specific_upgrade(int(self.player.coins))

    # --- Tick agora processa as teclas [A,S,D] ---
    def tick(self, key: Optional[str]):
        """Processa uma única atualização do jogo (input e lógica)."""
        if key:
            key_lower = key.lower()  # Converte para minúsculo para facilitar

            if key_lower == 'q':
                self.running = False
            elif key_lower == 'u':
                self.buy_global_upgrade()
            elif key.isdigit():
                idx = int(key) - 1
                self.buy_item(idx)
            elif key == ' ':
                self.player.coins += 1

            # --- Checa se a tecla está no nosso mapeamento ---
            elif key_lower in self.upgrade_keys:
                # Encontra o índice da tecla (ex: 'a' é 0, 's' é 1)
                idx = self.upgrade_keys.index(key_lower)
                self.buy_specific_upgrade(idx)

    def run(self):
        """Loop principal do jogo."""
        while self.running:
            key = get_key()
            self.tick(key)
            self.update_income()
            self.display()
            time.sleep(0.05)  # Mantém o uso de CPU baixo

        print("\nJogo encerrado.")