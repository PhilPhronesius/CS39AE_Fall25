import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from networkx.algorithms.community import greedy_modularity_communities

phishing_data = [("Alice", "Bob", 1), ("Alice", "Charlie", 1), ("Bob", "Charlie", 1),
                 ("Charlie", "Diana", 1), ("Diana", "Eve", 1), ("Bob", "Diana", 1),
                 ("Frank", "Eve", 1), ("Eve", "Ian", 1), ("Diana", "Ian", 1),
                 ("Ian", "Grace", 1), ("Grace", "Hannah", 1), ("Hannah", "Jack", 1),
                 ("Grace", "Jack", 1), ("Charlie", "Frank", 1), ("Alice", "Eve", 1),
                 ("Bob", "Jack", 1)]

G = nx.DiGraph()
for sender, receiver, weight in phishing_data:
    G.add_edge(sender, receiver, weight=weight)

def plot_graph():
    pos = nx.spring_layout(G)
    plt.figure(figsize=(10, 8))
    weights = nx.get_edge_attributes(G, 'weight')
    nx.draw(
        G, pos, with_labels=True, node_size=3000, node_color='skyblue', edge_color='gray', font_size=10, font_weight='bold'
    )
    nx.draw_networkx_edge_labels(G, pos, edge_labels=weights)
    plt.title("Friendship Network with Weighted Edges")
    st.pyplot(plt)

def display_centralities():
    betweenness_centrality = nx.betweenness_centrality(G, weight='weight')
    closeness_centrality = nx.closeness_centrality(G)
    
    st.write("Betweenness Centrality:")
    for node, score in betweenness_centrality.items():
        st.write(f"{node}: {score:.4f}")

    st.write("Closeness Centrality:")
    for node, score in closeness_centrality.items():
        st.write(f"{node}: {score:.4f}")

def display_community_detection():
    communities = greedy_modularity_communities(G)
    st.write("Community Detection (Greedy Modularity):")
    for i, community in enumerate(communities, 1):
        st.write(f"Community {i}: {list(community)}")


    palette = ["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple"]
    node_to_comm = {}
    for c_index, comm in enumerate(communities):
        for node in comm:
            node_to_comm[node] = c_index

    community_colors = [palette[node_to_comm[n]] for n in G.nodes()]

    pos = nx.spring_layout(G)
    plt.figure(figsize=(10, 8))
    nx.draw(
        G, pos, with_labels=True, node_size=3000, node_color=community_colors, edge_color="gray", font_size=10, font_weight="bold", arrows=True
    )
    nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'))
    plt.title("Network Colored by Community")
    st.pyplot(plt)

st.title("Network Analysis with Streamlit")

plot_graph()

display_centralities()

display_community_detection()
