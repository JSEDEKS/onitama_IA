class ConsoleUI:
    def clear(self):
        # Limpia la pantalla (simple y compatible)
        print("\n" * 50)

    def show_board(self, board):
        # El tablero ya viene armado desde Board
        board.print_board()

    def show_player_turn(self, player):
        print(f"\nTurno de: {player.name} ({player.color})")

    def choose_card(self, player):
        print("\nCartas disponibles:")
        for i, card in enumerate(player.cards):
            print(f"{i + 1}. {card.name}")

        choice = int(input("Elige una carta: ")) - 1
        return player.cards[choice]

    def choose_move(self, player):
        print("\nPiezas:")
        for i, piece in enumerate(player.pieces):
            print(f"{i + 1}. {piece.type} en {piece.position}")

        p_index = int(input("Elige una pieza: ")) - 1
        piece = player.pieces[p_index]

        x = int(input("Mover a X: "))
        y = int(input("Mover a Y: "))

        return piece, (x, y)

    def show_winner(self, player):
        print(f"\n🏆 {player.name} HA GANADO 🏆")
