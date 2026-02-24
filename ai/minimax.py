class minimax:

    def __init__(self, player_name, max_depth=3):
        self.player_name = player_name
        self.max_depth = max_depth

    def solve(self, state):
        move, _ = self.minimax(
            state,
            depth=self.max_depth,
            alpha=float("-inf"),
            beta=float("inf"),
            maximizing=True
        )
        return move

    def minimax(self, state, depth, alpha, beta, maximizing):

        # 1️⃣ Caso base
        if depth == 0 or state.is_terminal():
            return state.last_move, state.get_winner_points()[self.player_name]

        best_move = None

        # 2️⃣ MAX
        if maximizing:
            max_eval = float("-inf")

            for child in state.children():

                move, eval_value = self.minimax(
                    child,              # ✅ USAR CHILD
                    depth - 1,          # ✅ REDUCIR DEPTH
                    alpha,
                    beta,
                    False
                )

                if eval_value > max_eval:
                    max_eval = eval_value
                    best_move = child.last_move

                alpha = max(alpha, eval_value)

                if beta <= alpha:
                    break   # poda

            return best_move, max_eval

        # 3️⃣ MIN
        else:
            min_eval = float("inf")

            for child in state.children():

                move, eval_value = self.minimax(
                    child,              # ✅ USAR CHILD
                    depth - 1,          # ✅ REDUCIR DEPTH
                    alpha,
                    beta,
                    True
                )

                if eval_value < min_eval:
                    min_eval = eval_value
                    best_move = child.last_move

                beta = min(beta, eval_value)

                if beta <= alpha:
                    break   # poda

            return best_move, min_eval