import chess.pgn

def find_winner(result:str):
    if result == "1-0":
        w = "Win"
        b = "Lose"
    elif result == "0-1":
        w = "Lose"
        b = "Win"
    else:
        w = b = "Draw"
    return w,b


def parse_games(data:str, min_games = 20):
    player_games = {}
    opening_counts = {}
    num_of_games = 0
    with open(data) as f:
        while True:
            num_of_games += 1
            game = chess.pgn.read_game(f)
            if game is None: break
            w, b = find_winner(game.headers["Result"])
            op = game.headers["Opening"].split(":")
            if op[0] not in opening_counts:
                opening_counts[op[0]] = 0
            opening_counts[op[0]] += 1
            white = {
                "color": "White",
                "result": w,
                "opening": game.headers["Opening"],
                "game": list(game.mainline_moves())}
            black = {
                "color": "Black",
                "result": b,
                "opening": game.headers["Opening"],
                "game": list(game.mainline_moves())}
            player_games.setdefault(game.headers["White"], []).append(white)
            player_games.setdefault(game.headers["Black"], []).append(black)
        player_games = {
            player: games
            for player, games in player_games.items()
            if (len(games)) >= min_games
        }
        return player_games, opening_counts, num_of_games        
            
            

