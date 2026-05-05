import chess.pgn
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
player_games = {}
resultW = ""
resultL = ""
num_of_games = 0
player_features = {}
openings = {}
with open("data/raw/lichess_db_standard_rated_2013-01.pgn") as f:
    while True:
        num_of_games += 1
        print(num_of_games)
        game = chess.pgn.read_game(f)
        if(game == None):
            break
        if(game.headers["Result"] == "1-0"):
            resultW = "Win"
            resultL = "Lose"
        elif(game.headers["Result"] == "0-1"):
            resultL = "Win" 
            resultW = "Lose"
        else:
            resultW = "Draw"
            resultL = "Draw"
        opening = game.headers["Opening"].split(":")
        if opening[0] not in openings:
            openings[opening[0]] = 0
        openings[opening[0]] += 1
        white = {"color": "White",
                "result": resultW,
                "opening": game.headers["Opening"],
                "game": game.mainline()}
        black = {"color": "Black",
                "result": resultL,
                "opening": game.headers["Opening"],
                "game": game.ma}
        player_games.setdefault(game.headers["White"], []).append(white)
        player_games.setdefault(game.headers["Black"], []).append(black)

player_games = {
    player: games
    for player, games in player_games.items()
    if (len(games)) >= 20
}

def extract_feature(games):
    global openings
    # player = [win_rate, avg_moves, num_of_games, %top1, %top2, %top3, %top4, %top5, diffOpenings]
    num_of_wins = 0
    avg_moves = 0
    counter = {}
    top5 = dict(sorted(openings.items(), key= lambda x: x[1], reverse=True)[:5])
    for game in games:
        moves = sum(1 for _ in game["game"])
        opening = game["opening"].split(":")
        if opening[0] not in counter:
            counter[opening[0]] = 0
        if game["result"] == "Win":
            num_of_wins += 1
        avg_moves += moves / 2
        counter[opening[0]] += 1
    helper = {}
    for opening in top5:
        if opening in counter:
            helper[opening] = float(counter[opening]) / float(len(games))
        else:
            helper[opening] = float(0)
    return [
        float(num_of_wins) / float(len(games)), # win_rate
        float(avg_moves) / float(len(games)), # avg_moves
        len(games), # num_of_games
        *[helper[o] for o in top5], # % of top5 openings
        len(counter) # diff_openings
    ]

for player in player_games:
    player_features[player] = extract_feature(player_games[player])
result = player_features.values()
data = list(result)
arr = np.array(data)
data_mean = np.mean(arr, axis=0)
data_std = np.std(arr, axis=0)
scaled_data = (arr - data_mean) / data_std

pca = PCA(n_components=2)
X_reduced = pca.fit_transform(scaled_data)

plt.scatter(X_reduced[:,0], X_reduced[:,1])
plt.show()

wcs = []
for k in range(1,15):
    k_means = KMeans(n_clusters=k)
    k_means.fit(scaled_data)
    y_kmeans = k_means.predict(scaled_data)
    plt.scatter(X_reduced[:,0], X_reduced[:,1], c=y_kmeans, s=50, cmap="viridis")
    plt.show()
    wcs.append(k_means.inertia_)
print(wcs)

plt.plot(range(1,15), wcs, marker="o")
plt.title("Elbow - Method")
plt.xlabel("Number of clusters")
plt.ylabel("WCSS")
plt.show()

#print(game.mainline())