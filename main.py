import sys
from game.game_manager import GameManager
from ai.benchmark import run_all_benchmarks


def main():
    # Modo benchmark: python main.py --benchmark
    # Modo benchmark rápido: python main.py --benchmark 5   (5 partidas por escenario)
    if len(sys.argv) > 1 and sys.argv[1] == "--benchmark":
        num_games = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        run_all_benchmarks(num_games=num_games)
        return

    # Modo normal: juego interactivo
    game = GameManager()
    game.start()


if __name__ == "__main__":
    main()