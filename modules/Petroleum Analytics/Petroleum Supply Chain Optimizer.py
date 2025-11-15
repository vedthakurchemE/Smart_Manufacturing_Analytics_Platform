# 📘 Module 9: Petroleum Supply Chain Optimizer | PetroStream AI Suite
# 🚚 Optimize logistics cost from oil wells to refineries using MILP + GeoMap
# 📦 Author: Ved Thakur | IPS Academy Indore | BTech ChemEng

import streamlit as st
import pandas as pd
import numpy as np
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpStatus
import plotly.express as px

def run():
    st.set_page_config(page_title="🚚 Supply Chain Optimizer", layout="wide")
    st.title("🚚 Petroleum Supply Chain Optimizer")
    st.markdown("Optimize transport cost from wells to refineries using Mixed Integer Linear Programming (MILP).")

    # Load demo data if not uploaded
    if wells_file and refineries_file:
        wells_df = pd.read_csv(wells_file)
        ref_df = pd.read_csv(refineries_file)
    else:
        st.sidebar.info("Using demo data...")
        wells_df = pd.DataFrame({
            "Well": ["Well-A", "Well-B", "Well-C"],
            "Supply": [100, 150, 120],
            "Lat": [20.5, 21.0, 22.1],
            "Lon": [72.9, 73.1, 72.5]
        })

        ref_df = pd.DataFrame({
            "Refinery": ["Ref-1", "Ref-2"],
            "Demand": [200, 170],
            "Lat": [19.8, 22.3],
            "Lon": [73.0, 72.6]
        })

    st.subheader("🛢️ Oil Wells")
    st.dataframe(wells_df)

    st.subheader("🏭 Refineries")
    st.dataframe(ref_df)

    # Calculate cost matrix (Euclidean Distance * cost per km)
    cost_per_km = st.sidebar.number_input("Transport Cost (₹/unit/km)", value=10.0)
    cost_matrix = pd.DataFrame(index=wells_df["Well"], columns=ref_df["Refinery"])

    for i, w in wells_df.iterrows():
        for j, r in ref_df.iterrows():
            dist = np.sqrt((w["Lat"] - r["Lat"])**2 + (w["Lon"] - r["Lon"])**2) * 111  # rough conversion
            cost_matrix.loc[w["Well"], r["Refinery"]] = round(dist * cost_per_km, 2)

    st.subheader("💰 Cost Matrix (₹/unit)")
    st.dataframe(cost_matrix)

    # MILP Optimization
    st.subheader("📊 Optimal Transportation Plan")

    prob = LpProblem("PetroleumTransport", LpMinimize)

    routes = [(w, r) for w in wells_df["Well"] for r in ref_df["Refinery"]]
    vars = LpVariable.dicts("Route", routes, lowBound=0, cat="Continuous")

    # Objective
    prob += lpSum([vars[(w, r)] * float(cost_matrix.loc[w, r]) for (w, r) in routes])

    # Supply constraints
    for i, w in wells_df.iterrows():
        prob += lpSum([vars[(w["Well"], r)] for r in ref_df["Refinery"]]) <= w["Supply"]

    # Demand constraints
    for i, r in ref_df.iterrows():
        prob += lpSum([vars[(w, r["Refinery"])] for w in wells_df["Well"]]) >= r["Demand"]

    prob.solve()

    results = []
    for (w, r) in routes:
        qty = vars[(w, r)].varValue
        if qty > 0:
            results.append({"Well": w, "Refinery": r, "Qty": qty, "Cost": float(cost_matrix.loc[w, r])})

    result_df = pd.DataFrame(results)
    result_df["Total Cost"] = result_df["Qty"] * result_df["Cost"]

    st.dataframe(result_df.round(2))

    total_cost = result_df["Total Cost"].sum()
    st.success(f"✅ Total Optimized Transport Cost: ₹ {total_cost:,.2f}")

    # Plot map
    st.subheader("🗺️ Transportation Routes Map")

    map_df = pd.merge(result_df, wells_df, on="Well").rename(columns={"Lat": "WellLat", "Lon": "WellLon"})
    map_df = pd.merge(map_df, ref_df, on="Refinery").rename(columns={"Lat": "RefLat", "Lon": "RefLon"})

    fig = px.scatter_mapbox(
        pd.concat([
            pd.DataFrame({"Name": wells_df["Well"], "Lat": wells_df["Lat"], "Lon": wells_df["Lon"], "Type": "Well"}),
            pd.DataFrame({"Name": ref_df["Refinery"], "Lat": ref_df["Lat"], "Lon": ref_df["Lon"], "Type": "Refinery"})
        ]),
        lat="Lat", lon="Lon", color="Type", hover_name="Name", zoom=4,
        mapbox_style="open-street-map"
    )
    st.plotly_chart(fig)
