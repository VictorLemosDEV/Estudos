# main.py
from game import Game

if __name__ == "__main__":
    try:
        # Cria uma instância do jogo e inicia o loop principal
        Game().run()
    except KeyboardInterrupt:
        print("\nJogo encerrado abruptamente.")
    except Exception as e:
        print(f"\nOcorreu um erro inesperado: {e}")