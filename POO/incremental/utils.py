# utils.py
import os
import sys
from typing import Optional

# --- Input setup ---
if os.name == 'nt':
    import msvcrt


    def get_key() -> Optional[str]:
        """Lê uma tecla pressionada no Windows sem bloquear."""
        if msvcrt.kbhit():
            return msvcrt.getwch()
        return None
else:
    import termios
    import tty
    import select


    def get_key() -> Optional[str]:
        """Lê uma tecla pressionada no Linux/macOS sem bloquear."""
        dr, _, _ = select.select([sys.stdin], [], [], 0)
        if dr:
            return sys.stdin.read(1)
        return None


# --- Clear screen ---
def clear_screen() -> None:
    """Limpa o terminal, com fallback para IDEs."""
    if os.name == 'nt':
        result = os.system('cls')
    else:
        result = os.system('clear')

    # Fallback para terminais que não suportam 'clear' ou 'cls' (como IDEs)
    if result != 0 or "PYCHARM_HOSTED" in os.environ or not sys.stdout.isatty():
        print("\033[2J\033[H", end="")