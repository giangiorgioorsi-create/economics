import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="IS/LM Model Explorer", layout="wide")
# --- END OF CHANGES ---

# --- STYLING & HEADER ---
st.title("Interactive IS/LM Model")
st.markdown("""
This application demonstrates the equilibrium between the **Goods Market (IS)** and the **Money Market (LM)**. 
In the short-run Keynesian model, production responds to variations in aggregate demand which are sensitive to the interest rate[cite: 1].
""")

# --- SIDEBAR PARAMETERS ---
with st.sidebar:
    st.header("Model Parameters")
    
    # --- NEW/MODIFIED CODE: IS Parameters ---
    st.subheader("Goods Market (IS)")
    alpha = st.slider("Auton. Consumption / Multiplier (α)", 100, 1000, 500, help="Initial demand factors.")
    c = st.slider("Marginal Propensity to Consume (c)", 0.1, 0.9, 0.6)
    b = st.slider("Interest Sensitivity of Investment (b)", 5, 50, 20, help="How much investment falls as interest rates rise[cite: 13].")
    G = st.slider("Government Spending (G)", 100, 1000, 300)
    # --- END OF CHANGES ---

    # --- NEW/MODIFIED CODE: LM Parameters ---
    st.subheader("Money Market (LM)")
    ms = st.slider("Real Money Supply (M/P)", 500, 3000, 1500, help="Controlled by the Central Bank.")
    k = st.slider("Income Sensitivity of Money Demand (k)", 0.1, 0.8, 0.4, help="Transactions demand for money[cite: 2].")
    h = st.slider("Interest Sensitivity of Money Demand (h)", 5, 100, 50, help="Speculative demand for money[cite: 2].")
    # --- END OF CHANGES ---

# --- MATHEMATICAL ENGINE ---
# --- NEW/MODIFIED CODE: Solving for Equilibrium ---
# IS Curve: Y = C + I + G -> Y = [alpha + G - b*r] / (1 - c)
# Rewritten for r: r = (alpha + G)/b - (1 - c)/b * Y

# LM Curve: M/P = k*Y - h*r
# Rewritten for r: r = (k/h) * Y - (M/P)/h

Y_range = np.linspace(1, 5000, 500)

def calculate_is(Y, alpha, G, b, c):
    return ((alpha + G) / b) - (((1 - c) / b) * Y)

def calculate_lm(Y, ms, k, h):
    return (k / h) * Y - (ms / h)

# Equilibrium Calculation (Algebraic Intersection)
# (alpha + G)/b - (1-c)/b * Y = (k/h) * Y - ms/h
numerator = ((alpha + G) / b) + (ms / h)
denominator = ((1 - c) / b) + (k / h)
Y_star = numerator / denominator
r_star = calculate_lm(Y_star, ms, k, h)

is_curve = calculate_is(Y_range, alpha, G, b, c)
lm_curve = calculate_lm(Y_range, ms, k, h)
# --- END OF CHANGES ---

# --- VISUALIZATION ---
# --- NEW/MODIFIED CODE: Plotting ---
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(Y_range, is_curve, label="IS (Goods Market)", color="blue", linewidth=2)
ax.plot(Y_range, lm_curve, label="LM (Money Market)", color="red", linewidth=2)

# Equilibrium point
if 0 < r_star < max(is_curve):
    ax.scatter(Y_star, r_star, color="black", s=100, zorder=5)
    ax.vlines(Y_star, 0, r_star, linestyle="--", color="gray")
    ax.hlines(r_star, 0, Y_star, linestyle="--", color="gray")
    ax.text(Y_star + 100, r_star + 0.5, f'E* ({Y_star:.0f}, {r_star:.2f}%)', fontweight='bold')

ax.set_xlim(0, 5000)
ax.set_ylim(0, max(is_curve.max(), 20))
ax.set_xlabel("National Income / Output (Y)")
ax.set_ylabel("Interest Rate (r)")
ax.set_title("IS/LM Equilibrium Analysis")
ax.legend()
ax.grid(True, alpha=0.3)

st.pyplot(fig)
# --- END OF CHANGES ---

# --- RESULTS SUMMARY ---
# --- NEW/MODIFIED CODE: Metrics ---
col1, col2 = st.columns(2)
col1.metric("Equilibrium Income (Y*)", f"{Y_star:.2f}")
col2.metric("Equilibrium Interest Rate (r*)", f"{r_star:.2f}%")

with st.expander("Theoretical Context"):
    st.write(f"""
    * **The IS Curve**: Represents the market for goods and services. It shows that as the interest rate falls, investment increases, which raises total income[cite: 13].
    * **The LM Curve**: Represents the money market. The interest rate adjusts to balance the supply of money with the demand for holding it[cite: 43].
    * **Equilibrium**: The point where both markets are cleared simultaneously, determining the levels of output and interest in the economy[cite: 3, 5].
    """)
# --- END OF CHANGES ---
