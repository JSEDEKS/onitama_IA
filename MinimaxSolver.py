import numpy as np
class MinimaxSolver():
    
    def __init__(self, player_name):
        self.player_name = player_name
        
    
    def _maximize(self, state, alpha, beta, depth):
        
        if state.is_terminal():
            return None, state.get_winner_points()[self.player_name]
        
        if depth == 0:
            return None, #Heuristic
        
        max_child, max_utility = None, -np.inf
        for child in state.children():
            _, utility = self._minimize(state, alpha, beta)
            
            if utility > max_utility:
                max_child, max_utility = child, utility
                
            if max_utility >= beta:
                break
            
            alpha = max(alpha, max_utility)
            
            
            return max_child, max_utility
               
           
           
    
    def _minimize(self, state, alpha, beta, depth):
        
        if state.is_terminal():
            return None, state.get_winner_points()[self.player_name]
        
        if depth == 0:
            return None, #Heuristic
        
        min_child, min_utility = None, np.inf
        for child in state.children():
            _, utility = self._maximize(state, alpha, beta, depth-1)
            
            if utility < min_utility:
                min_child, min_utility = child, utility
                
            if min_utility <= alpha:
                break
            
            beta = min(beta, min_child)
            
            
            return min_child, min_utility
        
    def solve(self, state):
        
        child, _ = self._maximize(state, -np.inf, np.inf)
        
        return child