# =============================================================
# MONTE CARLO PRICING MODEL
# Author: Lucas Tejerina
# Description: Optimal pricing simulation under demand uncertainty
# =============================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------------------------------------
# PARAMETERS - modify these to adapt the model to any product
# -------------------------------------------------------------
COSTO_UNITARIO = 10       # Unit production cost
PRECIO_BASE = 30         # Reference price for elasticity calculation
SIMULACIONES = 10000      # Number of Monte Carlo scenarios
DEMANDA_MEDIA = 100      # Average demand at base price
DEMANDA_STD = 50         # Demand volatility (standard deviation)
ELASTICIDAD = 0.8         # Price sensitivity (higher = more sensitive)

# -------------------------------------------------------------
# SIMULATION
# -------------------------------------------------------------
np.random.seed(42)  # Ensures reproducibility

precios = np.arange(COSTO_UNITARIO+1, PRECIO_BASE*4, 1)  # Price range to evaluate
resultados = []

for precio in precios:
    
    # Adjust mean demand based on price elasticity
    factor_demanda = 1 - ELASTICIDAD * ((precio - PRECIO_BASE) / PRECIO_BASE)
    
    # Simulate demand scenarios using normal distribution
    demanda_simulada = np.random.normal(
        DEMANDA_MEDIA * factor_demanda,
        DEMANDA_STD,
        SIMULACIONES
    )
    demanda_simulada = np.maximum(demanda_simulada, 0)  # No negative demand
    
    # Calculate profit for each scenario
    ganancia = (precio - COSTO_UNITARIO) * demanda_simulada
    
    resultados.append({
        'precio': precio,
        'ganancia_media': ganancia.mean(),
        'ganancia_p10': np.percentile(ganancia, 10),  # Pessimistic scenario
        'ganancia_p90': np.percentile(ganancia, 90)   # Optimistic scenario
    })

# -------------------------------------------------------------
# RESULTS
# -------------------------------------------------------------
df = pd.DataFrame(resultados)

optimo = df.loc[df['ganancia_media'].idxmax()]
print(f"Optimal price:     ${optimo['precio']}")
print(f"Expected profit:   ${optimo['ganancia_media']:,.0f}")
print(f"Pessimistic (P10): ${optimo['ganancia_p10']:,.0f}")
print(f"Optimistic (P90):  ${optimo['ganancia_p90']:,.0f}")

# -------------------------------------------------------------
# VISUALIZATION
# -------------------------------------------------------------
plt.figure(figsize=(10, 6))
plt.plot(df['precio'], df['ganancia_media'], 
         label='Expected profit', color='blue', linewidth=2)
plt.fill_between(df['precio'], df['ganancia_p10'], df['ganancia_p90'],
                 alpha=0.3, color='blue', label='P10-P90 uncertainty band')
plt.axvline(optimo['precio'], color='red', linestyle='--', 
            label=f"Optimal price: ${optimo['precio']}")
plt.xlabel('Price')
plt.ylabel('Profit')
plt.title('Monte Carlo Simulation - Optimal Pricing Under Demand Uncertainty')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()