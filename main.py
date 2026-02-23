from game.game_manager import GameManager

# PERSONA 5: Cuando benchmark.py esté listo, descomentar esta línea:
# from ai.benchmark import run_all_benchmarks


def main():
    import sys

    # Modo benchmark: ejecutar con "python main.py --benchmark"
    # PERSONA 5: Implementar este bloque cuando benchmark.py esté listo.
    if len(sys.argv) > 1 and sys.argv[1] == "--benchmark":
        # run_all_benchmarks(num_games=10)
        print("Benchmark no implementado aún.")
        return

    # Modo normal: juego interactivo
    game = GameManager()
    game.start()


if __name__ == "__main__":
    main()
