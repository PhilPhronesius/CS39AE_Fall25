import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import random
import pandas as pd
import numpy as np
from networkx.algorithms.community import greedy_modularity_communities

friendship_data = [("Alice", "Bob"), ("Alice", "Charlie"), ("Bob", "Charlie"),
                   ("Charlie", "Diana"), ("Diana", "Eve"), ("Bob", "Diana"),
                   ("Frank", "Eve"), ("Eve", "Ian"), ("Diana", "Ian"),
                   ("Ian", "Grace"), ("Grace", "Hannah"), ("Hannah", "Jack"),
                   ("Grace", "Jack"), ("Charlie", "Frank"), ("Alice", "Eve"),
                   ("Bob", "Jack")]

friendship_data_with_weights = [(a, b, 1) for a, b in friendship_data]

G = nx.Graph()
for sender, receiver, weight in friendship_data_with_weights:
    G.add_edge(sender, receiver, weight=weight)

pos = nx.spring_layout(G, seed=42)

if 'graph_fig' not in st.session_state:
    st.session_state.graph_fig = None

if 'community_fig' not in st.session_state:
    st.session_state.community_fig = None

if 'influential_fig' not in st.session_state:
    st.session_state.influential_fig = None

def plot_graph():
  if st.session_state.graph_fig is None:
    plt.figure(figsize=(8, 6))
    
    weights = nx.get_edge_attributes(G, 'weight')
    
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color='lightgreen', edge_color='gray', font_size=10, font_weight='bold')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=weights)
    plt.title("Friendship Network with Random Weights")
  st.pyplot(st.session_state.graph_fig)

def display_adjacency_matrix():
    adjacency_matrix = nx.to_numpy_array(G)
    
    st.write("**Adjacency Matrix**:")
    fig, ax = plt.subplots(figsize=(8, 8))
    cax = ax.matshow(adjacency_matrix, cmap='binary')
    plt.colorbar(cax, shrink = 0.8)
    
    labels = list(G.nodes())
    ax.set_xticks(np.arange(len(labels)))
    ax.set_yticks(np.arange(len(labels)))
    ax.set_xticklabels(labels)
    ax.set_yticklabels(labels)
    
    plt.title("Adjacency Matrix of the Friendship Network")
    st.pyplot(fig)

def display_centralities():
    betweenness_centrality = nx.betweenness_centrality(G, weight='weight')
    closeness_centrality = nx.closeness_centrality(G)
    
    betweenness_df = pd.DataFrame(list(betweenness_centrality.items()), columns=["Node", "Betweenness Centrality"])
    closeness_df = pd.DataFrame(list(closeness_centrality.items()), columns=["Node", "Closeness Centrality"])

    col1, col2 = st.columns(2)

    with col1:
      st.write("**Betweenness Centrality**:")
      st.write(betweenness_df)
    with col2:
      st.write("**Closeness Centrality**:")
      st.write(closeness_df)

def display_community_detection():
  if st.session_state.community_fig is None:
    communities = greedy_modularity_communities(G)
    
    st.write("**Community Detection**:")
    for i, community in enumerate(communities, 1):
        st.write(f"Community {i}: {list(community)}")
    
    palette = ["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple"]
    node_to_comm = {}
    for c_index, comm in enumerate(communities):
        for node in comm:
            node_to_comm[node] = c_index

    community_colors = [palette[node_to_comm[n]] for n in G.nodes()]

    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color=community_colors, edge_color="gray", font_size=10, font_weight="bold", arrows=True)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'))
    plt.title("Network Colored by Community")
    plt.tight_layout()
  st.pyplot(st.session_state.community_fig)


def display_influential_person():
  if st.session_state.influential_fig is None:
    betweenness_centrality = nx.betweenness_centrality(G, weight = 'weight')
    degree_centrality = nx.degree_centrality(G)
    most_influential_person = max(betweenness_centrality, key=betweenness_centrality.get)
    most_connected_person = max(degree_centrality, key=degree_centrality.get)
  
    node_colors = ['lightblue' if node == most_influential_person else 'lightgreen' for node in G.nodes()]

    st.write(f"**Most Connected Person (Degree)**: {most_connected_person}")
    st.write(f"**Most Influential Person (Betweenness)**: {most_influential_person}")
  
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color=node_colors, edge_color='gray', font_size=10, font_weight='bold')
    plt.title("Friendship Network with Most Influential Person Highlighted")
    plt.tight_layout()
  st.pyplot(st.session_state.influential_fig)

def findings():
    st.write(f"**Findings**:")
    st.write("As we can see from our graphs, the most connected and influential person in spreading information within the network is Bob. Despite other friends having the same amount of connections, Bob knows at least one person in each community as visualized from the **Network Colored by Community** graph. This is further supported by the **Betweenness** and **Closeness** data tables as they show Bob's values being the greatest at 0.25 and 0.6429.")

st.title("Friendship Network in a College Class")

col1, col2 = st.columns(2)

with col1:
  plot_graph()
with col2:
  display_adjacency_matrix()

display_centralities()

col1, col2 = st.columns(2)

with col1:
  display_community_detection()
with col2:
  display_influential_person()

findings()
