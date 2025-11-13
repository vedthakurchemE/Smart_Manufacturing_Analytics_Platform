# 📘 Module 4: Agent-Based Simulation | EpiModelAI Suite
# 🧍 Individual-level epidemic simulation with random motion and transmission
# 📦 Author: Ved Thakur | IPS Academy Indore | BTech ChemEng

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import random

def run():
    # === Title ===
    st.title("📘 Agent-Based Disease Spread Simulation")
    st.markdown("Simulate the spread of infection in a population with mobile individuals (agents).")

    # === Sidebar Parameters ===
    st.sidebar.header("🧬 Agent Parameters")
    num_agents = st.sidebar.slider("Total Number of Agents", 10, 500, 100)
    initial_infected = st.sidebar.slider("Initially Infected Agents", 1, 20, 3)
    infection_radius = st.sidebar.slider("Infection Radius", 0.01, 0.2, 0.05, step=0.01)
    transmission_prob = st.sidebar.slider("Transmission Probability", 0.0, 1.0, 0.5, step=0.05)
    recovery_time = st.sidebar.slider("Recovery Time (in steps)", 5, 100, 30)
    sim_steps = st.sidebar.slider("Simulation Steps", 10, 200, 100)

    # === Agent Initialization ===
    class Agent:
        def __init__(self):
            self.x = random.random()
            self.y = random.random()
            self.state = 'S'
            self.infected_time = 0

        def move(self):
            self.x += np.random.normal(0, 0.01)
            self.y += np.random.normal(0, 0.01)
            self.x = min(max(self.x, 0), 1)
            self.y = min(max(self.y, 0), 1)

    agents = [Agent() for _ in range(num_agents)]
    for i in range(initial_infected):
        agents[i].state = 'I'

    S_count, I_count, R_count = [], [], []

    # === Simulation ===
    for t in range(sim_steps):
        for agent in agents:
            agent.move()

        for i, a in enumerate(agents):
            if a.state == 'I':
                for j, b in enumerate(agents):
                    if i != j and b.state == 'S':
                        distance = np.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)
                        if distance < infection_radius and random.random() < transmission_prob:
                            b.state = 'I'

                a.infected_time += 1
                if a.infected_time > recovery_time:
                    a.state = 'R'

        # Count status
        S_count.append(sum(a.state == 'S' for a in agents))
        I_count.append(sum(a.state == 'I' for a in agents))
        R_count.append(sum(a.state == 'R' for a in agents))

    # === Final State Visualization ===
    st.subheader("🧍 Agent Final Position Map")
    fig1, ax1 = plt.subplots()
    for a in agents:
        color = {'S': 'blue', 'I': 'red', 'R': 'green'}[a.state]
        ax1.plot(a.x, a.y, 'o', color=color)
    ax1.set_title("Final Agent States")
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    st.pyplot(fig1)

    # === Timeline Plot ===
    st.subheader("📈 Agent State Timeline")
    fig2, ax2 = plt.subplots()
    ax2.plot(S_count, label='Susceptible', color='blue')
    ax2.plot(I_count, label='Infected', color='red')
    ax2.plot(R_count, label='Recovered', color='green')
    ax2.set_xlabel("Simulation Step")
    ax2.set_ylabel("Number of Agents")
    ax2.legend()
    st.pyplot(fig2)

    # === Final Counts ===
    st.subheader("📊 Final Agent Counts")
    col1, col2, col3 = st.columns(3)
    col1.metric("Susceptible", S_count[-1])
    col2.metric("Infected", I_count[-1])
    col3.metric("Recovered", R_count[-1])

    # === Info Box ===
    with st.expander("📘 How It Works"):
        st.markdown("""
        - Each dot is an individual (agent) moving randomly.
        - Red agents can infect nearby blue agents.
        - After `recovery_time` steps, infected agents become green (recovered).
        """)
