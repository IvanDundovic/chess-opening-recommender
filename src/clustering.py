import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score

def normalize(feature_matrix):
    data_mean = np.mean(feature_matrix, axis=0)
    data_std = np.std(feature_matrix, axis=0)
    scaled_matrix = (feature_matrix - data_mean) / data_std
    return scaled_matrix, data_mean, data_std

def find_optimal_k(scaled_data, max_k=15):
    wcss = []
    for k in range(1, max_k + 1):
        k_means = KMeans(n_clusters=k, random_state=42, n_init=10)
        k_means.fit(scaled_data)
        wcss.append(k_means.inertia_)
    plt.figure(figsize=(12,5))
    plt.plot(range(1, max_k + 1), wcss, marker="o")
    plt.xlabel("Broj klastera (k)")
    plt.ylabel("WCSS")
    plt.title("Elbow metoda")
    plt.show()

    return wcss

def evaluate_clusters(scaled_data, labels):
    sil = silhouette_score(scaled_data, labels)
    db = davies_bouldin_score(scaled_data, labels)
    return sil, db

def fit_clusters(scaled_data, k):
    k_means = KMeans(n_clusters=k)
    labels = k_means.fit_predict(scaled_data)
    return k_means, labels

def visualize_clusters(scaled_data, labels):
    pca = PCA(n_components=2)
    feat_reduced = pca.fit_transform(scaled_data)
    plt.figure(figsize=(12, 5))
    scatter = plt.scatter(feat_reduced[:,0], feat_reduced[:,1], c=labels, s=50, cmap="viridis")
    plt.colorbar(scatter, label="Cluster")
    plt.title("PCA-visualisation")
    plt.show()

def profile_clusters(feature_matrix, labels, feature_names):
    df = pd.DataFrame(feature_matrix, columns=feature_names)
    df["cluster"] = labels
    profile = df.groupby("cluster").mean().round(3)
    print(profile.to_string())
    return profile

def save_clusters(player_names, labels, filepath):
    with open(filepath, "w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["player","cluster"])
        for player, label in zip(player_names, labels):
            csv_writer.writerow([player, label])

def load_clusters(filepath):
    df = pd.read_csv(filepath)
    player_names = df["player"].tolist()
    labels = df["cluster"].to_numpy()
    return player_names, labels
    