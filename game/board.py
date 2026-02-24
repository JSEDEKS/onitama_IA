class Board:
    RESET = "\033[0m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BOLD = "\033[1m"
    BG_GREEN = "\033[42m"

    def __init__(self):
        self.size = 5
        self.grid = [[None for _ in range(self.size)] for _ in range(self.size)]
        
    def setup(self, players):
        p1, p2 = players

        p1_positions = {
            "master": (2, 4),
            "students": [(0, 4), (1, 4), (3, 4), (4, 4)]
        }

        p2_positions = {
            "master": (2, 0),
            "students": [(0, 0), (1, 0), (3, 0), (4, 0)]
        }

        p1.create_pieces(p1_positions)
        p2.create_pieces(p2_positions)

        for player in players:
            for piece in player.pieces:
                x, y = piece.position
                self.grid[y][x] = piece
                
    def print_board(self, valid_moves=None):
        print(f"\n     0   1   2   3   4")
        for y in range(self.size):
            row = f"  {y}  "
            for x in range(self.size):
                piece = self.grid[y][x]
                if piece is not None:
                    color = self.RED if piece.owner.color == "RED" else self.BLUE
                    symbol = "M" if piece.type == "MASTER" else "S"
                    if valid_moves and (x, y) in valid_moves:
                        row += f"{self.BG_GREEN}{color}{self.BOLD}{symbol}{self.RESET}   "
                    else:
                        row += f"{color}{self.BOLD}{symbol}{self.RESET}   "
                elif valid_moves and (x, y) in valid_moves:
                    row += f"{self.GREEN}*{self.RESET}   "
                else:
                    row += ".   "
            print(row)

    def move_piece(self, from_pos, to_pos):
        fx, fy = from_pos
        tx, ty = to_pos

        piece = self.grid[fy][fx]
        target = self.grid[ty][tx]

        if target is not None:
            target.owner.remove_piece(target)

        self.grid[fy][fx] = None
        self.grid[ty][tx] = piece
        piece.move((tx, ty))

    def get_opponent(self, player):
        for row in self.grid:
            for piece in row:
                if piece and piece.owner != player:
                    return piece.owner
        return None

    def get_enemy_temple(self, player):
        if player.color == "RED":
            return (2, 0)
        return (2, 4)
