import numpy as np
import chess.pgn

center_squares = [chess.E4, chess.E5, chess.D4, chess.D5]
piece_value = {
    chess.PAWN : 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9
    } 
# to doo
#    center_pressure_score = 0 ostalo podijeliti s brojem poteza i nakraju sum i kroz broj partija
#    sacrifices_count = 0 gotovo
#    sacrifices_score = 0 gotovo
#    exchange_count = 0 gotovo moze se lako pretvoriti u favorable_exchange_count
#    early_captures = 0 gotovo
#    development_score = 0 gotovo
#    repetated_piece_moves = 0 gotovo
#    open_files_created = 0
#    mirrors_center = 0
#    castling_preformed = 0 u openingu
#    castling_delay = 0 kroz cijelu partiju
#    attack_moves_count = 0 gotovo
#    checks_given = 0 gotovo
#    pawn_moves_ratio = 0 gotovo
#    
#    
#

def count_early_captures_and_development(moves, player_color, num_of_moves = 7):
    board = chess.Board()
    early_captures = 0
    development_score = 0
    developed_squares = set()
    for i, move in enumerate(moves):
        if i > num_of_moves * 2: break

        if board.turn == player_color:
            if board.is_capture(move):
                early_captures +=1

            piece = board.piece_type_at(move.from_square)
            if piece in [chess.KNIGHT, chess.BISHOP]:
                if move.from_square not in developed_squares:
                    development_score +=1
                    developed_squares.add(move.from_square)
                else: development_score -=1
            if board.is_castling(move):
                development_score +=1
        board.push(move)
    return early_captures, development_score 

def count_exchanges(moves, player_color):
    board = chess.Board()
    exchange_count = 0
    i = 0
    while i < (len(moves) - 1):
        move = moves[i]
        if board.turn == player_color and board.is_capture(move):
            board.push(move)
            oponnent_move = moves[i + 1]
            if board.is_capture(oponnent_move) and oponnent_move.to_square == move.to_square:
                board.push(oponnent_move)
                exchange_count += 1
                i += 2
                continue
            else: i += 1
        else: 
            board.push(move)
            i +=1
    #print(exchange_count)
    return exchange_count

def count_sacrifices(moves, player_color):
    board = chess.Board()
    sacrifices_count = 0
    sacrifices_score = 0
    i = 0
    while i < (len(moves) - 2):
        move = moves[i]
        if board.turn != player_color:
            board.push(move)
            i +=1
            continue
        moved_piece = board.piece_at(move.from_square)
        if moved_piece is None:
            board.push(move)
            i += 1
            continue

        board.push(move)
        oponnent_move = moves[i + 1]
        if board.is_capture(oponnent_move) and oponnent_move.to_square == move.to_square:
            board.push(oponnent_move)
            response_move = moves[i + 2]
            if not board.is_capture(response_move):
                sacrifices_count += 1
                sacrifices_score += piece_value[moved_piece.piece_type]
            board.push(response_move)
            i +=3
        else: 
            board.push(oponnent_move)
            i += 2
    #print(sacrifices_count)
    #print(sacrifices_score)
    return sacrifices_count, sacrifices_score

    

def extract_features(games, num_of_moves=10):
    MAX_DELAY = 40
    features = {
    "center_pressure": 0,
    "sacrifices_count": 0,
    "sacrifices_score": 0,
    "exchange_count": 0,
    "early_captures": 0,
    "development": 0,
    "repeated_moves": 0,
    "castled": 0,
    "castling_delay": 0,
    "attacks": 0,
    "checks": 0,
    "pawn_moves": 0
}  
    for g in games:
        seen_squares = set()
        developed_squares = set()
        late_features = {
            "sacrifices_count": 0,
            "sacrifices_score": 0,
            "exchange_count": 0,
            "attacks": 0,
            "checks": 0,
            "pawn_moves": 0
        }
        erl_features = {
            "center_pressure": 0,
            "early_captures": 0,
            "development": 0,
            "repeated_moves": 0,
        }
        board = chess.Board()
        moves = g["game"]
        player_color = chess.WHITE if g["color"] == "White" else chess.BLACK
        player_moves = castled = 0
        castling_delay = None
        late_features["sacrifices_count"], late_features["sacrifices_score"] = count_sacrifices(moves, player_color)
        late_features["exchange_count"] = count_exchanges(moves, player_color)
        for move in moves:  
            if board.turn == player_color:
                player_moves += 1
                if player_moves <= num_of_moves:
                    # center_pressure
                    erl_features["center_pressure"] += sum(
                        1 if board.is_attacked_by(player_color, sq) else 0
                        for sq in center_squares
                    )
                    # early captures
                    if board.is_capture(move):
                        erl_features["early_captures"] += 1
                    
                    # development and castling preformed
                    if board.is_castling(move):
                        castled = 1
                        erl_features["development"] += 1
                    else:
                        piece = board.piece_type_at(move.from_square)
                        if piece in [chess.KNIGHT, chess.BISHOP]:
                            if move.from_square not in developed_squares:
                                erl_features["development"] += 1
                                developed_squares.add(move.from_square)
                            else:
                                erl_features["development"] -= 1
                    
                    # repated_moves
                    if move.from_square in seen_squares:
                        erl_features["repeated_moves"] += 1
                    seen_squares.add(move.from_square)

                # whole game
                # castling delay
                if board.is_castling(move):
                    castling_delay = player_moves / MAX_DELAY

                # attack moves
                if board.is_capture(move):
                    late_features["attacks"] += 1
                
                # check moves
                if board.gives_check(move):
                    late_features["checks"] += 1
                # pawn ratio
                piece = board.piece_type_at(move.from_square)
                if piece == chess.PAWN:
                    late_features["pawn_moves"] += 1

            board.push(move)
        if castling_delay is None:
            castling_delay = 1
        # extraction of features  
        for key in late_features:
            late_features[key] /= max(1, player_moves)
            features[key] += late_features[key]
        for key in erl_features:
            erl_features[key] /= num_of_moves
            features[key] += erl_features[key]
        features["castled"] += castled
        features["castling_delay"] += castling_delay
    features_list = list()
    for key in features:
        features[key] /= len(games)
        #print(f"Dodajem {key}")
        features_list.append(features[key])
    return np.array(features_list)
