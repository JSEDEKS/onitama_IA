class ConsoleUI:
    # ===== COLORES ANSI =====
    RESET = "\033[0m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"

    # ===== UTIL =====
    def clear(self):
        print("\n" * 50)

    def separator(self):
        print(self.CYAN + "-" * 40 + self.RESET)

    # ===== MENÚ =====
    def show_main_menu(self):
        self.separator()
        print(self.BOLD + self.BLUE + "        🀄 ONITAMA 🀄        " + self.RESET)
        self.separator()
        print(self.GREEN + "1️⃣  Iniciar juego" + self.RESET)
        print(self.YELLOW + "2️⃣  Instrucciones" + self.RESET)
        print(self.RED + "3️⃣  Salir" + self.RESET)
        self.separator()

    def choose_menu_option(self):
        while True:
            option = input(self.BOLD + "Elige una opción (1-3): " + self.RESET)
            if option in ("1", "2", "3"):
                return option
            print(self.RED + "❌ Opción inválida. Intenta otra vez." + self.RESET)

    # ===== INSTRUCCIONES =====
    def show_instructions(self):
        self.clear()
        self.separator()
        print(self.BOLD + self.BLUE + "📖 INSTRUCCIONES DE ONITAMA" + self.RESET)
        self.separator()

        print(self.CYAN + "• Juego de 2 jugadores en un tablero 5x5" + self.RESET)
        print(self.CYAN + "• Cada jugador tiene:" + self.RESET)
        print("   " + self.YELLOW + "- 1 Maestro (M)" + self.RESET)
        print("   " + self.YELLOW + "- 4 Discípulos (S)" + self.RESET)
        print(self.CYAN + "• Los movimientos dependen de cartas" + self.RESET)

        print("\n" + self.BOLD + "🔁 En tu turno:" + self.RESET)
        print("  1️⃣  Eliges una carta")
        print("  2️⃣  Eliges una pieza")
        print("  3️⃣  Eliges la posición destino")

        print("\n" + self.BOLD + "🏆 Ganas si:" + self.RESET)
        print(self.GREEN + "• Capturas el Maestro enemigo" + self.RESET)
        print(self.GREEN + "• Tu Maestro llega al templo enemigo" + self.RESET)

        self.separator()
        input("Presiona ENTER para volver al menú...")

    # ===== JUEGO =====
    def show_board(self, board):
        self.separator()
        print(self.BOLD + self.BLUE + "TABLERO" + self.RESET)
        self.separator()
        board.print_board()
        self.separator()

    def show_player_turn(self, player):
        color = self.RED if player.color == "RED" else self.BLUE
        print(
            f"\n{self.BOLD}🎮 Turno de:{self.RESET} "
            f"{color}{player.name} ({player.color}){self.RESET}"
        )

    def choose_card(self, player):
        while True:
            try:
                print("\n" + self.BOLD + "🃏 Cartas disponibles:" + self.RESET)
                for i, card in enumerate(player.cards):
                    print(f"  {self.YELLOW}{i + 1}.{self.RESET} {card.name}")

                choice = int(input("Elige una carta: ")) - 1
                if 0 <= choice < len(player.cards):
                    return player.cards[choice]
                else:
                    print(self.RED + "❌ Número fuera de rango." + self.RESET)
            except ValueError:
                print(self.RED + "❌ Debes escribir un número." + self.RESET)

    def choose_move(self, player):
        while True:
            try:
                print("\n" + self.BOLD + "♟️ Piezas disponibles:" + self.RESET)
                for i, piece in enumerate(player.pieces):
                    print(
                        f"  {self.YELLOW}{i + 1}.{self.RESET} "
                        f"{piece.type} en {piece.position}"
                    )

                p_index = int(input("Elige una pieza: ")) - 1
                if not (0 <= p_index < len(player.pieces)):
                    print(self.RED + "❌ Pieza fuera de rango." + self.RESET)
                    continue

                piece = player.pieces[p_index]

                x = int(input("Mover a X (0-4): "))
                y = int(input("Mover a Y (0-4): "))

                if 0 <= x <= 4 and 0 <= y <= 4:
                    return piece, (x, y)
                else:
                    print(self.RED + "❌ Coordenadas fuera del tablero (0-4)." + self.RESET)

            except ValueError:
                print(self.RED + "❌ Debes escribir solo números." + self.RESET)

    def show_winner(self, player):
        self.separator()
        print(
            self.BOLD + self.GREEN +
            f"🏆 ¡{player.name} HA GANADO LA PARTIDA! 🏆"
            + self.RESET
        )
        self.separator()
        input("Presiona ENTER para salir...")
