import pandas as pd
import numpy as np
from collections import defaultdict

def build_recommendations(player_opening_stats, player_names, labels, min_games=5):
    cluster_opening_stats = defaultdict(lambda: defaultdict(lambda: {"wins": 0, "total": 0}))
    for player, label in zip(player_names, labels):
        for opening, stats in player_opening_stats[player].items():
            cluster_opening_stats[label][opening]["wins"] += stats["wins"]
            cluster_opening_stats[label][opening]["total"] += stats["total"]
    recommendations = {}
    for cluster, openings in cluster_opening_stats.items():
        rated = []
        for opening, stats in openings.items():
            if stats["total"] >= min_games:
                win_rate = stats["wins"] / stats["total"]
                rated.append({
                    "opening": opening,
                    "win_rate": win_rate,
                    "total_games": stats["total"]
                })
        
        rated.sort(key=lambda x: x["win_rate"], reverse=True)
        recommendations[cluster] = rated

    return recommendations

def recommend_for_player(player_name, player_names, labels, recommendations, top_n=3):
    if player_name not in player_names:
        print(f"Igrač {player_name} nije u bazi")
        return []
    idx = player_names.index(player_name)
    cluster_id = labels[idx]
    
    print(f"Igrač: {player_name}")
    print(f"Klaster: {cluster_id}")
    print(f"Preporučena otvaranja:")
    for rec in recommendations[cluster_id][:top_n]:
        print(f"{rec['opening']} | win_rate: {rec['win_rate']:.1%} | partija: {rec['total_games']}")
    
    return recommendations[cluster_id][:top_n]

def recommend_new_player(feature_vector, model, mean, std, recommendations, top_n=3):
    scaled_data = (feature_vector - mean) / std
    cluster = model.predict([scaled_data])[0]
    
    print(f"Procijenjeni klaster: {cluster}")
    for rec in recommendations[cluster][:top_n]:
        print(f"{rec['opening']} | win_rate: {rec['win_rate']:.1%} | partija: {rec['total_games']}")
    return recommendations[cluster][:top_n]

def save_recommendations(recommendations, filepath):
    rows = []
    for cluster_id, openings in recommendations.items():
        for rec in openings:
            rows.append({
                "cluster": cluster_id,
                "opening": rec["opening"],
                "win_rate": rec["win_rate"],
                "total_games": rec["total_games"]
            })
    
    pd.DataFrame(rows).to_csv(filepath, index=False)

def load_recommendations(filepath):
    df = pd.read_csv(filepath)
    recommendations = defaultdict(list)
    for _, row in df.iterrows():
        recommendations[row["cluster"]].append({
            "opening": row["opening"],
            "win_rate": row["win_rate"],
            "total_games": row["total_games"]
        })
    return recommendations


