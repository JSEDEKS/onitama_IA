class Rules:

    def check_victory(self, board, player):
        return (
            self.master_captured(board, player) or
            self.master_in_temple(board, player)
        )



    def master_captured(self, board, player):
        opponent = board.get_opponent(player)
        return not opponent.has_master()



    def master_in_temple(self, board, player):
        master = player.get_master()
        temple_position = board.get_enemy_temple(player)
        return master.position == temple_position
