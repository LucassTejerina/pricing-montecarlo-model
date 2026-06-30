# Monte Carlo Pricing Model

## Overview
This model simulates **optimal product pricing under demand uncertainty** 
using Monte Carlo simulation. Given a cost structure and demand behavior, 
it identifies the price that maximizes expected profit across thousands 
of simulated scenarios.

## Methodology
- Demand is modeled as a **normal distribution** with price-dependent mean
- **Price elasticity** adjusts expected demand as price changes
- **10,000 scenarios** are simulated for each candidate price
- Results include expected profit and a **P10-P90 uncertainty band**

## Key Parameters
| Parameter | Default | Description |
|-----------|---------|-------------|
| Unit Cost | $50 | Production cost per unit |
| Base Price | $100 | Reference price |
| Elasticity | 0.8 | Price sensitivity of demand |
| Demand Mean | 1000 | Average units sold at base price |
| Demand Std | 200 | Demand volatility |

## Results
The model outputs:
- Optimal price point
- Expected profit at optimal price
- Pessimistic scenario (P10)
- Optimistic scenario (P90)
- Visualization of the full profit curve with uncertainty band

## Tech Stack
- Python 3.14
- NumPy · Pandas · Matplotlib

## Author
Lucas Tejerina — Actuarial Science Student, UBA  
Quantitative Finance | Risk Modeling | Data Analysis