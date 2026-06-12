import streamlit as st
import os
import sys
import io
import chess.pgn
import numpy as np
import pandas as pd
sys.path.append(os.path.abspath("../src"))

from recommender import load_recommendations, recommend_new_player
from features import extract_features, load_features
from clustering import load_model, load_clusters, visualize_clusters, evaluate_clusters
from evaluation import mean_win_rate_per_cluster

@st.cache_data
def load_data():
    player_names, labels = load_clusters("../data/processed/clusters.csv")
    recommendations = load_recommendations("../data/results/recommendations.csv")
    model, data_mean, data_std = load_model("../data/processed/model.pkl")
    X = np.array(list(load_features().values()))
    scaled_matrix = (X - data_mean) / data_std
    return player_names, labels, recommendations, model, data_mean, data_std, X, scaled_matrix

player_names, labels, recommendations, model, data_mean, data_std, X, scaled_matrix = load_data()
player_to_cluster = dict(zip(player_names, labels))

st.title("Sustav preporuka šahovskih otvaranja")

tab1, tab2, tab3 = st.tabs(["Pretraži igrača", "Analiziraj svoju partiju", "Prikaz klastera"])

with tab1:
    player = st.selectbox("Odaberi igrača", sorted(player_names))
    label = player_to_cluster[player]

    st.markdown(f"**Klaster:** {label} - {"Agresivan" if label == 0 else "Eksperimentalni" if label == 1 else "Pozicijski"} stil")
    st.markdown("### Preporučena otvaranja")

    top_n = st.slider("Broj preporuka", min_value=1, max_value=10, value=5, key="slider1")

    recs = recommendations[label][:top_n]
    for r in recs:
        st.markdown(f"**{r['opening']}**")
        col1, col2 = st.columns(2)
        col1.metric("Win rate", f"{r['win_rate']:.1%}")
        col2.metric("Broj partija", int(r['total_games']))
        st.divider()

with tab2:
    color = st.radio("S kojom bojom si igrao?", ["White", "Black"], horizontal=True)
    pgn_input = st.text_area("Zalijepi svoju PGN partiju ovdje")
    top_n2 = st.slider("Broj preporuka", min_value=1, max_value=10, value=5, key="slider2")

    if pgn_input:
        try:
            game = chess.pgn.read_game(io.StringIO(pgn_input))
            fv = extract_features([{
                "game": list(game.mainline_moves()),
                "color": color
            }])

            recs, best_cluster = recommend_new_player(fv, model, data_mean, data_std, recommendations, top_n=top_n2)

            st.markdown(f"**Preporučeni klaster:** {best_cluster} - {'Agresivan' if best_cluster == 0 else 'Eksperimentalni' if best_cluster == 1 else 'Pozicijski'} stil")
            st.markdown("### Preporučena otvaranja za tvoj stil")

            for r in recs:
                st.markdown(f"**{r['opening']}**")
                col1, col2 = st.columns(2)
                col1.metric("Win rate", f"{r['win_rate']:.1%}")
                col2.metric("Broj partija", int(r['total_games']))
                st.divider()

        except Exception as e:
            st.error(f"Greška pri parsiranju PGN-a: {e}")
with tab3:
    st.markdown("### PCA vizualizacija klastera")
    visualize_clusters(scaled_matrix, labels)
    fig = visualize_clusters(scaled_matrix, labels, streamlit=True)
    st.pyplot(fig)
    st.markdown("### Profil klastera")
    FEATURE_NAMES = ["center_pressure", "sacrifices_count", "sacrifices_score",
                     "exchange_count", "early_captures", "development", "repeated_moves",
                     "castled", "castling_delay", "attacks", "checks", "pawn_moves"]
    
    df = pd.DataFrame(X, columns=FEATURE_NAMES)
    df["cluster"] = labels
    profile = df.groupby("cluster").mean().round(3)
    st.dataframe(profile)
    st.markdown("### Evaluacija")

    col1, col2, col3 = st.columns(3)

    sil, db = evaluate_clusters(scaled_matrix, labels)
    col1.metric("Silhouette score", f"{sil:.3f}")
    col2.metric("Davies-Bouldin score", f"{db:.3f}")

    st.markdown("### Win rate po klasteru")
    wr_data = mean_win_rate_per_cluster(recommendations)
    st.dataframe(pd.DataFrame.from_dict(wr_data, orient="index", columns=["Avg win rate"]))