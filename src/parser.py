import chess.pgn
import pickle
import os
from collections import defaultdict

def find_winner(result:str):
    if result == "1-0":
        return "Win", "Loss"
    elif result == "0-1":
        return "Loss", "Win"
    return "Draw", "Draw"

def parse_games(data:str, min_games = 20):
    player_games = defaultdict(list)
    opening_counts = defaultdict(int)
    player_opening_stats = defaultdict(lambda: defaultdict(lambda: {"wins": 0, "total": 0}))
    num_of_games = 0
    with open(data) as f:
        while True:
            num_of_games += 1
            game = chess.pgn.read_game(f)
            if game is None: break
            black_name = game.headers["Black"]
            white_name = game.headers["White"]

            opening = game.headers["Opening"].split(":")[0].strip()
            opening_counts[opening] +=1
            w, b = find_winner(game.headers["Result"])

            player_games[white_name].append(
                {
                "color": "White",
                "result": w,
                "opening": game.headers["Opening"],
                "game": list(game.mainline_moves())
                })
            player_opening_stats[white_name][opening]["total"] += 1
            if w == "Win":
                player_opening_stats[white_name][opening]["wins"] += 1

            player_games[black_name].append(
                {
                "color": "Black",
                "result": b,
                "opening": game.headers["Opening"],
                "game": list(game.mainline_moves())
                })
            player_opening_stats[black_name][opening]["total"] += 1
            if b == "Win":
                player_opening_stats[black_name][opening]["wins"] +=1
            
        player_games = {
            player: games
            for player, games in player_games.items()
            if (len(games)) >= min_games
        }
        player_opening_stats = {
            p: stats for p, stats in player_opening_stats.items()
            if p in player_games
        }
        return player_games, opening_counts, player_opening_stats, num_of_games        
            
def save_parsed(path: str, player_games, opening_counts, player_opening_stats, num_of_games):
    data = {
        "player_games": dict(player_games),
        "opening_counts": dict(opening_counts),
        "player_opening_stats": {p: dict(s) for p, s in player_opening_stats.items()},
        "num_of_games": num_of_games
    }
    with open(path, "wb") as f:
        pickle.dump(data, f)

def load_parsed(path: str):
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        return pickle.load(f)            

def get_parsed_data(pgn_path: str, cache_path: str = "../data/processed/cache.pkl", min_games=20):
    cached = load_parsed(cache_path)
    if cached:
        return cached["player_games"], cached["opening_counts"], cached["player_opening_stats"], cached["num_of_games"]
    
    result = parse_games(pgn_path, min_games)
    save_parsed(cache_path, *result)
    return result
