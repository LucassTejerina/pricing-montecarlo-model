import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Monte Carlo Pricing Model", layout="centered")

st.title("📊 Monte Carlo Pricing Model")
st.markdown("Optimal pricing simulation under demand uncertainty")

# -------------------------------------------------------------
# SIDEBAR - User inputs
# -------------------------------------------------------------
st.sidebar.header("Model Parameters")

costo_unitario = st.sidebar.number_input("Unit Cost ($)", min_value=1.0, value=50.0, step=1.0)
precio_base = st.sidebar.number_input("Base Price ($)", min_value=1.0, value=100.0, step=1.0)
demanda_media = st.sidebar.number_input("Average Demand", min_value=1.0, value=1000.0, step=10.0)
demanda_std = st.sidebar.number_input("Demand Std Dev", min_value=0.0, value=200.0, step=10.0)
elasticidad = st.sidebar.slider("Price Elasticity", min_value=0.0, max_value=2.0, value=0.8, step=0.1)
simulaciones = st.sidebar.slider("Number of Simulations", min_value=1000, max_value=20000, value=10000, step=1000)

# -------------------------------------------------------------
# SIMULATION
# -------------------------------------------------------------
np.random.seed(42)

precios = np.arange(costo_unitario + 1, precio_base * 4, 1)
resultados = []

for precio in precios:
    factor_demanda = 1 - elasticidad * ((precio - precio_base) / precio_base)
    demanda_simulada = np.random.normal(demanda_media * factor_demanda, demanda_std, simulaciones)
    demanda_simulada = np.maximum(demanda_simulada, 0)
    
    ganancia = (precio - costo_unitario) * demanda_simulada
    
    resultados.append({
        'precio': precio,
        'ganancia_media': ganancia.mean(),
        'ganancia_p10': np.percentile(ganancia, 10),
        'ganancia_p90': np.percentile(ganancia, 90)
    })

df = pd.DataFrame(resultados)
optimo = df.loc[df['ganancia_media'].idxmax()]

# -------------------------------------------------------------
# RESULTS
# -------------------------------------------------------------
col1, col2, col3 = st.columns(3)
col1.metric("Optimal Price", f"${optimo['precio']:.0f}")
col2.metric("Expected Profit", f"${optimo['ganancia_media']:,.0f}")
col3.metric("Pessimistic (P10)", f"${optimo['ganancia_p10']:,.0f}")

# -------------------------------------------------------------
# CHART
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df['precio'], df['ganancia_media'], label='Expected profit', color='blue', linewidth=2)
ax.fill_between(df['precio'], df['ganancia_p10'], df['ganancia_p90'],
                alpha=0.3, color='blue', label='P10-P90 uncertainty band')
ax.axvline(optimo['precio'], color='red', linestyle='--', label=f"Optimal price: ${optimo['precio']:.0f}")
ax.set_xlabel('Price')
ax.set_ylabel('Profit')
ax.set_title('Monte Carlo Simulation - Optimal Pricing')
ax.legend()
ax.grid(True, alpha=0.3)

st.pyplot(fig)

st.markdown("---")
st.caption("Built by Lucas Tejerina — Actuarial Science Student, UBA")