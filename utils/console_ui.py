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

    # ===== MENU =====
    def show_main_menu(self):
        self.separator()
        print(self.BOLD + self.BLUE + "        ONITAMA        " + self.RESET)
        self.separator()
        print(self.GREEN + "1. Iniciar juego" + self.RESET)
        print(self.YELLOW + "2. Instrucciones" + self.RESET)
        print(self.RED + "3. Salir" + self.RESET)
        self.separator()

    def choose_menu_option(self):
        while True:
            option = input(self.BOLD + "Elige una opcion (1-3): " + self.RESET)
            if option in ("1", "2", "3"):
                return option
            print(self.RED + "Opcion invalida. Intenta otra vez." + self.RESET)

    # ===== INSTRUCCIONES =====
    def show_instructions(self):
        self.clear()
        self.separator()
        print(self.BOLD + self.BLUE + "INSTRUCCIONES DE ONITAMA" + self.RESET)
        self.separator()

        print(self.CYAN + "- Juego de 2 jugadores en un tablero 5x5" + self.RESET)
        print(self.CYAN + "- Cada jugador tiene:" + self.RESET)
        print("   " + self.YELLOW + "- 1 Maestro (M)" + self.RESET)
        print("   " + self.YELLOW + "- 4 Estudiantes (S)" + self.RESET)
        print(self.CYAN + "- Los movimientos dependen de cartas" + self.RESET)
        print(self.CYAN + "- Cada jugador tiene 2 cartas + 1 carta lateral" + self.RESET)
        print(self.CYAN + "- Las cartas se rotan: la usada pasa a lateral" + self.RESET)

        print("\n" + self.BOLD + "En tu turno:" + self.RESET)
        print("  1. Eliges una carta")
        print("  2. Se muestran los movimientos validos (*)")
        print("  3. Eliges una pieza que pueda moverse")
        print("  4. Eliges el destino de los disponibles")

        print("\n" + self.BOLD + "Ganas si:" + self.RESET)
        print(self.GREEN + "- Capturas el Maestro enemigo" + self.RESET)
        print(self.GREEN + "- Tu Maestro llega al templo enemigo (casilla central opuesta)" + self.RESET)

        self.separator()
        input("Presiona ENTER para volver al menu...")

    # ===== JUEGO =====
    def show_board(self, board, valid_moves=None):
        self.separator()
        print(self.BOLD + self.BLUE + "TABLERO" + self.RESET)
        self.separator()
        board.print_board(valid_moves)
        self.separator()

    def show_player_turn(self, player):
        color = self.RED if player.color == "RED" else self.BLUE
        print(
            f"\n{self.BOLD}Turno de:{self.RESET} "
            f"{color}{player.name} ({player.color}){self.RESET}"
        )

    def show_all_cards(self, current_player, opponent, side_card):
        cur_color = self.RED if current_player.color == "RED" else self.BLUE
        opp_color = self.RED if opponent.color == "RED" else self.BLUE

        print(f"\n{self.BOLD}Tus cartas:{self.RESET}", end="")
        for i, card in enumerate(current_player.cards):
            print(f"  {cur_color}[{i+1}] {card.name}{self.RESET}", end="")

        print(f"\n{self.BOLD}Carta lateral:{self.RESET} {self.YELLOW}{side_card.name}{self.RESET}")

        print(f"{self.BOLD}Cartas del oponente:{self.RESET}", end="")
        for card in opponent.cards:
            print(f"  {opp_color}{card.name}{self.RESET}", end="")
        print()

    def show_card_moves(self, card, player_color):
        oriented = card.moves if player_color == "RED" else [(-dx, -dy) for dx, dy in card.moves]
        print(f"\n{self.BOLD}Movimientos de {card.name}:{self.RESET}")
        grid = [["." for _ in range(5)] for _ in range(5)]
        cx, cy = 2, 2
        grid[cy][cx] = "P"
        for dx, dy in oriented:
            mx, my = cx + dx, cy + dy
            if 0 <= mx < 5 and 0 <= my < 5:
                grid[my][mx] = f"{self.GREEN}*{self.RESET}"
        for row in grid:
            print("  " + "  ".join(row))

    def choose_card(self, player):
        while True:
            try:
                print(f"\n{self.BOLD}Elige una carta (1-{len(player.cards)}):{self.RESET} ", end="")
                choice = int(input()) - 1
                if 0 <= choice < len(player.cards):
                    return player.cards[choice]
                else:
                    print(self.RED + "Numero fuera de rango." + self.RESET)
            except ValueError:
                print(self.RED + "Debes escribir un numero." + self.RESET)

    def choose_piece(self, pieces_with_moves):
        pieces_list = list(pieces_with_moves.keys())
        while True:
            try:
                print(f"\n{self.BOLD}Piezas que pueden moverse:{self.RESET}")
                for i, piece in enumerate(pieces_list):
                    print(
                        f"  {self.YELLOW}{i + 1}.{self.RESET} "
                        f"{piece.type} en ({piece.position[0]},{piece.position[1]})"
                    )

                choice = int(input(f"{self.BOLD}Elige una pieza: {self.RESET}")) - 1
                if 0 <= choice < len(pieces_list):
                    return pieces_list[choice]
                else:
                    print(self.RED + "Numero fuera de rango." + self.RESET)
            except ValueError:
                print(self.RED + "Debes escribir un numero." + self.RESET)

    def choose_destination(self, valid_moves):
        while True:
            try:
                print(f"\n{self.BOLD}Destinos disponibles:{self.RESET}")
                for i, (x, y) in enumerate(valid_moves):
                    print(f"  {self.GREEN}{i + 1}.{self.RESET} ({x},{y})")

                choice = int(input(f"{self.BOLD}Elige destino: {self.RESET}")) - 1
                if 0 <= choice < len(valid_moves):
                    return valid_moves[choice]
                else:
                    print(self.RED + "Numero fuera de rango." + self.RESET)
            except ValueError:
                print(self.RED + "Debes escribir un numero." + self.RESET)

    def show_no_moves(self, card):
        print(
            f"\n{self.YELLOW}No hay movimientos validos con {card.name}. "
            f"La carta se intercambia y se pasa el turno.{self.RESET}"
        )
        input("Presiona ENTER para continuar...")

    def show_winner(self, player):
        self.separator()
        color = self.RED if player.color == "RED" else self.BLUE
        print(
            self.BOLD + color +
            f"{player.name} HA GANADO LA PARTIDA!"
            + self.RESET
        )
        self.separator()
        input("Presiona ENTER para salir...")
