# 📘 Module 3: Contact Network Analyzer | EpiModelAI Suite
# 🌐 Visualize disease spread potential using graph theory
# 📦 Author: Ved Thakur | IPS Academy Indore | BTech ChemEng

import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import random

def run():
    # === Title ===
    st.title("📘 Contact Network Analyzer")
    st.markdown("Analyze how a disease may spread through social contact networks using graph theory.")

    # === Sidebar Parameters ===
    st.sidebar.header("🔧 Network Settings")
    num_nodes = st.sidebar.slider("Number of People (Nodes)", 10, 300, 100)
    avg_degree = st.sidebar.slider("Avg. Number of Contacts", 1, 20, 4)
    infection_prob = st.sidebar.slider("Infection Probability per Contact", 0.01, 1.0, 0.2, 0.01)
    infected_count = st.sidebar.slider("Initial Infected People", 1, 10, 3)

    # === Generate Small-World Graph ===
    G = nx.watts_strogatz_graph(n=num_nodes, k=avg_degree, p=0.1)

    # === Assign Node Statuses ===
    status = {node: 'S' for node in G.nodes()}
    infected = random.sample(list(G.nodes()), infected_count)
    for node in infected:
        status[node] = 'I'

    # === Simulate 1 Step of Infection Spread ===
    new_status = status.copy()
    for node in G.nodes():
        if status[node] == 'I':
            for neighbor in G.neighbors(node):
                if status[neighbor] == 'S' and random.random() < infection_prob:
                    new_status[neighbor] = 'I'

    status = new_status.copy()

    # === Visualization ===
    color_map = {'S': 'blue', 'I': 'red'}
    node_colors = [color_map[status[n]] for n in G.nodes()]

    fig, ax = plt.subplots(figsize=(10, 6))
    nx.draw_spring(G, node_color=node_colors, node_size=100, with_labels=False, ax=ax)
    ax.set_title("🌐 Contact Network After 1 Infection Step")
    st.pyplot(fig)

    # === Stats ===
    st.subheader("📊 Summary After 1 Step")
    total_infected = list(status.values()).count('I')
    total_susceptible = list(status.values()).count('S')

    col1, col2 = st.columns(2)
    col1.metric("Susceptible", total_susceptible)
    col2.metric("Infected", total_infected)

    # === Explanation ===
    with st.expander("📘 What This Shows"):
        st.markdown("""
        - Each person is a node in the graph.
        - Edges represent social connections.
        - Infection spreads from infected nodes to susceptible neighbors.
        - This model helps visualize how local contacts affect disease outbreaks.
        """)
