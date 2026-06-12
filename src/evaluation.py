import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def cluster_size_distribution(labels):
    unique, counts = np.unique(labels, return_counts=True)
    for cluster, count in zip(unique, counts):
        print(f"Klaster {cluster}: {count} igrača ({count/len(labels):.1%})") 

def hit_rate(player_opening_stats, player_names, labels, recommendations, top_n=5):
    hits = total = 0
    for player, label in zip(player_names, labels):
        recommended = {r["opening"] for r in recommendations[label][:top_n]}
        for opening, stats in player_opening_stats[player].items():
            if opening in recommended:
                win_rate = stats["wins"] / stats["total"] if stats["total"] > 0 else 0
                if win_rate > 0.5:
                    hits += 1
            total += 1
    rate = hits / total
    print(f"Hit rate for top {top_n} openings is: {rate:.1%}")
    return rate

def player_coverage(player_opening_stats, player_names, labels, recommendations, top_n=5):
    covered = 0
    for player, label in zip(player_names, labels):
        recommended = {r["opening"] for r in recommendations[label][:top_n]}
        played = set(player_opening_stats[player].keys())
        if recommended & played:
            covered += 1
    rate = covered / len(player_names)
    print(f"Player coverage: {rate:.1%}")
    return rate

def mean_win_rate_per_cluster(recommendations):
    data = {}
    for cluster_id, openings in recommendations.items():
        data[cluster_id] = np.mean([r["win_rate"] for r in openings])
    return data

def coverage(recommendations, opening_counts):
    all_openings = set(opening_counts.keys())
    recommended = set()
    for openings in recommendations.values():
        for o in openings:
            recommended.add(o["opening"])
    covr = len(recommended) / len(all_openings)
    print(f"Coverage: {len(recommended)}/ {len(all_openings)} otvaranja ({covr:.1%})")

def plot_cluster_profiles(feature_matrix, labels, feature_names):

    df = pd.DataFrame(feature_matrix, columns=feature_names)
    df["cluster"] = labels
    profile = df.groupby("cluster").mean()

    profile.T.plot(kind="bar", figsize=(14, 5))
    plt.title("Profili klastera po featurima")
    plt.xlabel("Feature")
    plt.ylabel("Srednja vrijednost")
    plt.xticks(rotation=45, ha="right")
    plt.legend(title="Klaster")
    plt.tight_layout()
    plt.show()

def plot_top_openings_per_cluster(recommendations, top_n=5):
    for cluster_id, openings in recommendations.items():
        top = openings[:top_n]
        names = [r["opening"] for r in top]
        rates = [r["win_rate"] for r in top]

        plt.figure(figsize=(14, 5))
        bars = plt.bar(names, rates, color="steelblue")
        plt.axhline(y=0.5, color="red", linestyle="--", label="50% win rate")
        plt.title(f"Klaster {cluster_id} — top {top_n} otvaranja")
        plt.ylabel("Win rate")
        plt.xticks(rotation=20, ha="right")
        plt.ylim(0, 1)
        for bar, rate in zip(bars, rates):
            plt.text(bar.get_x() + bar.get_width()/2, 
                    bar.get_height() + 0.01,
                    f"{rate:.1%}", ha="center", fontsize=9)
        plt.tight_layout()
        plt.show()

