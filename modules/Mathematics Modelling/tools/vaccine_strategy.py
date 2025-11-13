# 📘 Module 5: Vaccination Strategy Optimizer | EpiModelAI Suite
# 💉 Compare vaccination strategies on infection spread reduction
# 📦 Author: Ved Thakur | IPS Academy Indore | BTech ChemEng

import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random

def run():
    # === Title ===
    st.title("📘 Vaccination Strategy Optimizer")
    st.markdown("Test different vaccination strategies and compare their effect on infection spread.")

    # === Sidebar Parameters ===
    st.sidebar.header("💉 Vaccination Settings")
    num_people = st.sidebar.slider("Total People", 50, 500, 200, 10)
    avg_contacts = st.sidebar.slider("Average Contacts", 2, 20, 4)
    vaccination_rate = st.sidebar.slider("Vaccination Coverage (%)", 0, 100, 20) / 100
    transmission_prob = st.sidebar.slider("Transmission Probability (β)", 0.01, 1.0, 0.2, 0.01)
    recovery_prob = st.sidebar.slider("Recovery Probability (γ)", 0.01, 1.0, 0.05, 0.01)
    sim_steps = st.sidebar.slider("Simulation Steps", 10, 100, 40)

    # === Strategy Selection ===
    strategy = st.radio("Select Vaccination Strategy", [
        "🟡 Random Selection",
        "🔴 High-Contact First",
        "🧓 Elderly Priority (Simulated Ages)"
    ])

    # === Generate Network ===
    G = nx.watts_strogatz_graph(n=num_people, k=avg_contacts, p=0.1)
    degrees = dict(G.degree())
    ages = {node: random.randint(20, 80) for node in G.nodes}

    # === Assign Vaccination ===
    vaccinated = set()
    num_vaccinated = int(vaccination_rate * num_people)

    if strategy == "🟡 Random Selection":
        vaccinated = set(random.sample(sorted(G.nodes()), num_vaccinated))

    elif strategy == "🔴 High-Contact First":
        sorted_nodes = sorted(degrees, key=degrees.get, reverse=True)
        vaccinated = set(sorted_nodes[:num_vaccinated])

    elif strategy == "🧓 Elderly Priority (Simulated Ages)":
        sorted_nodes = sorted(ages, key=ages.get, reverse=True)
        vaccinated = set(sorted_nodes[:num_vaccinated])

    # === Initialize Infection Status ===
    status = {node: 'S' for node in G.nodes}
    initial_infected = random.choice(list(set(G.nodes()) - vaccinated))
    status[initial_infected] = 'I'
    for node in vaccinated:
        status[node] = 'V'  # Vaccinated

    history = []

    # === Run Simulation ===
    for _ in range(sim_steps):
        new_status = status.copy()
        for node in G.nodes:
            if status[node] == 'I':
                for neighbor in G.neighbors(node):
                    if status[neighbor] == 'S' and random.random() < transmission_prob:
                        new_status[neighbor] = 'I'
                if random.random() < recovery_prob:
                    new_status[node] = 'R'
        status = new_status.copy()
        history.append(status.copy())

    # === Final Network Plot ===
    final_status = history[-1]
    color_map = {'S': 'blue', 'I': 'red', 'R': 'green', 'V': 'gray'}
    node_colors = [color_map[final_status[n]] for n in G.nodes]

    fig, ax = plt.subplots(figsize=(10, 6))
    nx.draw_spring(G, node_color=node_colors, with_labels=False, node_size=100, ax=ax)
    ax.set_title("🧬 Final Infection Status (V = Vaccinated)")
    st.pyplot(fig)

    # === Timeline Chart ===
    st.subheader("📈 Epidemic Timeline")

    sus, inf, rec, vac = [], [], [], []
    for stat in history:
        sus.append(list(stat.values()).count('S'))
        inf.append(list(stat.values()).count('I'))
        rec.append(list(stat.values()).count('R'))
        vac.append(list(stat.values()).count('V'))

    fig2, ax2 = plt.subplots()
    ax2.plot(sus, label='Susceptible', color='blue')
    ax2.plot(inf, label='Infected', color='red')
    ax2.plot(rec, label='Recovered', color='green')
    ax2.plot(vac, label='Vaccinated', color='gray')
    ax2.set_xlabel("Time Step")
    ax2.set_ylabel("Population Count")
    ax2.set_title("🕒 SIRV Timeline")
    ax2.legend()
    st.pyplot(fig2)

    # === Summary Metrics ===
    st.subheader("📊 Final Statistics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Susceptible", sus[-1])
    col2.metric("Infected", inf[-1])
    col3.metric("Recovered", rec[-1])
    col4.metric("Vaccinated", len(vaccinated))

    with st.expander("📘 Strategy Details"):
        st.markdown(f"""
        **Strategy Used:** {strategy}  
        **Vaccinated:** {len(vaccinated)} out of {num_people}  
        - Red = Infected  
        - Blue = Susceptible  
        - Green = Recovered  
        - Gray = Vaccinated
        """)
