from game.pieces import Master, Student

class Heuristics:
   

    # Perfiles de personalidad para la IA
    PROFILES = {
        "BALANCED": {
            "piece_count": 100.0,
            "master_safety": 10.0,  # H2: Avance hacia el templo enemigo
            "mobility": 5.0,
            "master_threat": 50.0,
            "temple_control": 200.0
        },
        "AGGRESSIVE": {
            "piece_count": 80.0,    # Menos materialista
            "master_safety": 30.0,  # H2: Corre hacia el templo enemigo (muy agresivo)
            "mobility": 15.0,       # Busca asfixiar
            "master_threat": 80.0,  # Prioridad alta al Jaque
            "temple_control": 250.0
        },
        "DEFENSIVE": {
            "piece_count": 150.0,   # H1: Protege piezas a toda costa
            "master_safety": 0.0,   # H2: No tiene prisa por cruzar el tablero
            "mobility": 10.0,       # Mantiene opciones de escape
            "master_threat": 20.0,  # Solo ataca si es seguro
            "temple_control": 200.0
        },
        "TROLL": {
            "piece_count": 100.0,
            "master_safety": 10.0,  # H2: Avance hacia el templo enemigo      
            "mobility": 5.0,        # H3: Movilidad (no le importa mucho)
            "master_threat": 50.0,  # H4: Amenaza al maestro enemigo
            "temple_control": 2000.0 # H5: Control del templo enemigo
        
        }
    }

    def evaluate(self, state, player, heuristics_count=5, weights=None):
      
        if weights is None:
            # Selecciona aquí el perfil: "BALANCED", "AGGRESSIVE" o "DEFENSIVE"
            weights = self.PROFILES["TROLL"]

        score = 0.0
        opponent = state.get_opponent(player) # Asumimos que GameState tiene este método

        # 1. Piece Count (Diferencia de piezas)
        if heuristics_count >= 1:
            val = self._h1_piece_count(player, opponent)
            score += val * weights["piece_count"]

        # 2. Master Safety / Progress (Distancia al templo enemigo)
        if heuristics_count >= 2:
            val = self._h2_master_distance(state, player)
            score += val * weights["master_safety"]

        # 3. Mobility (Cantidad de movimientos disponibles)
        if heuristics_count >= 3:
            val = self._h3_mobility(state, player, opponent)
            score += val * weights["mobility"]

        # 4. Master Threat (¿Amenazamos al maestro enemigo?)
        if heuristics_count >= 4:
            val = self._h4_master_threat(state, player, opponent)
            score += val * weights["master_threat"]

        # 5. Temple Control (¿Estamos a 1 paso de ganar por templo?)
        if heuristics_count >= 5:
            val = self._h5_temple_control(state, player)
            score += val * weights["temple_control"]

        return score

    # -------------------------------------------------------------------------
    # HEURÍSTICAS INDIVIDUALES
    # -------------------------------------------------------------------------

    def _h1_piece_count(self, player, opponent):
      
        return len(player.pieces) - len(opponent.pieces)

    def _h2_master_distance(self, state, player):
       
        master = player.get_master()
        if not master:
            return -100 # Perdió el maestro, muy malo

        # Obtenemos la posición del templo enemigo desde el tablero
        target_pos = state.board.get_enemy_temple(player)
        
        # Distancia Manhattan: |x1 - x2| + |y1 - y2|
        dist = abs(master.position[0] - target_pos[0]) + \
               abs(master.position[1] - target_pos[1])
        
        return 8 - dist

    def _h3_mobility(self, state, player, opponent):
       
        # Si GameState aún no está listo, usamos un estimado o 0
        try:
            my_moves = len(state.get_all_moves(player))
            opp_moves = len(state.get_all_moves(opponent))
            return my_moves - opp_moves
        except AttributeError:
            return 0

    def _h4_master_threat(self, state, player, opponent):
       
        try:
            # Obtenemos todos los destinos posibles de mis movimientos
            my_moves = state.get_all_moves(player) # Lista de (card, piece, (x,y))
            
            enemy_master = opponent.get_master()
            if not enemy_master:
                return 100 # Ya ganamos

            enemy_master_pos = enemy_master.position

            for _, _, dest in my_moves:
                if dest == enemy_master_pos:
                    return 1.0 # Jaque / Amenaza directa
            
            return 0.0
        except AttributeError:
            return 0.0

    def _h5_temple_control(self, state, player):
       
        target_pos = state.board.get_enemy_temple(player)
        tx, ty = target_pos

        for piece in player.pieces:
            px, py = piece.position
            # Distancia Manhattan al templo
            dist = abs(px - tx) + abs(py - ty)
            if dist == 0: return 100.0 # Ya ganamos (ocupamos templo)
            if dist == 1 and piece.type == "MASTER": return 1.0 # A un paso
            
        return 0.0