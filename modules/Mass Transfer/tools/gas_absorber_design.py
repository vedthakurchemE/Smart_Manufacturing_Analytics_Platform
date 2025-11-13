# 📦 Module 8: Gas Absorber Design Tool | MassTransferAI Suite
# 📘 Design Packed Towers (HTU/NTU) or Estimate Ideal Stages (McCabe-Thiele)
# 👨‍💻 Author: Ved Thakur | IPS Academy Indore | BTech ChemEng

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io

def run():
    st.title("🌫️ Gas Absorber Design Tool")
    st.markdown("""
    Estimate absorber design parameters using:
    1. 🌐 **Packed Tower Design (HTU/NTU Method)**
    2. 📊 **Ideal Stage Estimation (McCabe-Thiele Analogy)**  
    Useful for: CO₂ scrubbing, SO₂ removal, NH₃ absorption, etc.
    """)

    design_method = st.sidebar.selectbox("📌 Select Design Method", ["Packed Tower (HTU/NTU)", "Ideal Stages"])

    if design_method == "Packed Tower (HTU/NTU)":
        st.subheader("🌐 Packed Tower Design")

        L = st.number_input("Liquid Flow Rate (mol/s)", 0.01, 1e5, 100.0)
        G = st.number_input("Gas Flow Rate (mol/s)", 0.01, 1e5, 200.0)
        y1 = st.number_input("Inlet Gas Mole Fraction (y₁)", 0.0, 1.0, 0.2)
        y2 = st.number_input("Outlet Gas Mole Fraction (y₂)", 0.0, 1.0, 0.05)
        m = st.number_input("Equilibrium Line Slope (m)", 0.01, 10.0, 1.0)
        HTU = st.number_input("HTU (Height of Transfer Unit) in m", 0.01, 10.0, 0.5)

        try:
            A = m * L / G
            if A <= 1:
                NTU = (1 / (1 - A)) * np.log((y1 - A) / (y2 - A))
            else:
                NTU = (1 / (A - 1)) * np.log((y1 - A) / (y2 - A))

            Z = HTU * NTU

            st.success(f"✅ Packed Tower Height: `{Z:.2f} m`")
            st.info(f"📈 NTU: `{NTU:.2f}` | HTU: `{HTU} m`")

            # Plot
            y_vals = np.linspace(y2, y1, 100)
            x_eq = y_vals / m
            x_op = (L / G) * y_vals

            fig, ax = plt.subplots()
            ax.plot(x_eq, y_vals, label="Equilibrium Line", color='green')
            ax.plot(x_op, y_vals, label="Operating Line", color='blue')
            ax.set_xlabel("x (Liquid Mole Fraction)")
            ax.set_ylabel("y (Gas Mole Fraction)")
            ax.legend()
            ax.set_title("Equilibrium vs Operating Line")
            ax.grid(True)
            st.pyplot(fig)

            # Download Report
            report = f"""
Gas Absorber Design Report (Packed Tower)
-----------------------------------------
Method: HTU/NTU
Liquid Flow Rate (L): {L} mol/s
Gas Flow Rate (G): {G} mol/s
y₁: {y1}
y₂: {y2}
Slope of Equilibrium Line (m): {m}
HTU: {HTU} m
NTU: {NTU:.2f}
Estimated Tower Height (Z): {Z:.2f} m
"""
            st.download_button("⬇️ Download Report", report, file_name="absorber_packed_report.txt")

        except Exception as e:
            st.error(f"❌ Error: {e}")

    else:
        st.subheader("📊 Ideal Stage Estimation (McCabe-Thiele Style)")

        y1 = st.number_input("Inlet Gas Mole Fraction (y₁)", 0.0, 1.0, 0.3)
        y2 = st.number_input("Outlet Gas Mole Fraction (y₂)", 0.0, 1.0, 0.05)
        m = st.number_input("Equilibrium Line Slope (m)", 0.1, 5.0, 1.2)
        LbyG = st.number_input("L/G Ratio", 0.01, 10.0, 1.0)

        try:
            x_vals = np.linspace(0, y1, 100)
            y_eq = m * x_vals
            y_op = (1 / LbyG) * x_vals + y2

            fig, ax = plt.subplots()
            ax.plot(x_vals, y_eq, label="Equilibrium Line", color='green')
            ax.plot(x_vals, y_op, label="Operating Line", color='blue')
            ax.set_xlabel("x (Liquid Mole Fraction)")
            ax.set_ylabel("y (Gas Mole Fraction)")
            ax.set_title("McCabe-Thiele Diagram (Absorption)")
            ax.grid(True)

            # Stepping method
            N = 0
            x, y = (y2 / m), y2
            while y < y1 and N < 100:
                # Step up to eq line
                x1, y1_line = x, m * x
                ax.plot([x, x], [y, y1_line], color='red')
                y = y1_line
                # Step across to op line
                x2 = (y - y2) * LbyG
                ax.plot([x, x2], [y, y], color='red')
                x = x2
                N += 1

            st.pyplot(fig)
            st.success(f"🔢 Estimated Number of Ideal Stages: `{N}`")

        except Exception as e:
            st.error(f"❌ Error: {e}")

    # 📘 Notes
    with st.expander("📘 Engineering Notes"):
        st.markdown("""
        - **Packed Tower Design** uses mass transfer units (HTU/NTU). Valid when the absorber operates with dilute gases.
        - **Ideal Stage Method** is used in stage-wise (tray) columns with high-stage efficiency.
        - Ensure gas is the solute-rich phase (y1 > y2).
        - Slope `m` is from equilibrium data: `y = m·x`
        - `L/G` must maintain absorption feasibility: operating line should lie above equilibrium line.

        📚 Refer to McCabe, Smith, and Harriott's _Unit Operations of Chemical Engineering_.
        """)
