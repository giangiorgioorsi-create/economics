import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Simulador del Modelo IS/LM", layout="wide")

# --- ENCABEZADO Y TÍTULO ---
st.title("Simulador Interactivo del Modelo IS/LM")
st.markdown("""
Esta herramienta analiza el equilibrio macroeconómico de corto plazo mediante la interacción de los mercados de bienes y dinero. 
Ajuste los parámetros en el panel lateral para observar el impacto de las políticas fiscales y monetarias sobre el ingreso nacional ($Y$) e interés ($i$).
""")

# --- PARÁMETROS EN LA BARRA LATERAL ---
with st.sidebar:
    st.header("Parámetros del Modelo")
    
    st.subheader("Mercado de Bienes (Curva IS)")
    alpha = st.slider("Consumo Autónomo (α)", 100, 1000, 500, help="Nivel de consumo que no depende del ingreso.")
    c = st.slider("Propensión Marginal al Consumo (c)", 0.1, 0.9, 0.6)
    b = st.slider("Sensibilidad de la Inversión (b)", 5, 100, 50)
    G = st.slider("Gasto Público (G)", 100, 1500, 500)

    st.subheader("Mercado de Dinero (Curva LM)")
    ms = st.slider("Oferta Monetaria Real (M/P)", 500, 5000, 2000)
    k = st.slider("Sensibilidad al Ingreso (k)", 0.1, 0.9, 0.5)
    h = st.slider("Sensibilidad a la Tasa de Interés (h)", 10, 200, 100)

# --- LÓGICA MATEMÁTICA Y EQUILIBRIO ---
# --- NEW/MODIFIED CODE: Motor de Escalado Dinámico Total ---
# 1. Cálculo de intersección algebraica
# IS: i = (alpha + G)/b - (1-c)/b * Y
# LM: i = (k/h) * Y - (ms/h)
num_eq = ((alpha + G) / b) + (ms / h)
den_eq = ((1 - c) / b) + (k / h)
Y_star = num_eq / den_eq
i_star = (k / h) * Y_star - (ms / h)

# 2. Cálculo de interceptos para definir los límites de los ejes
intercepto_is_y = (alpha + G) / b  # Donde la IS toca el eje vertical (Y=0)
intercepto_is_x = (alpha + G) / (1 - c) # Donde la IS toca el eje horizontal (i=0)

# 3. Definición de límites de visualización (Padding del 20%)
limite_x = max(intercepto_is_x, Y_star) * 1.2
limite_i = max(intercepto_is_y, i_star) * 1.2

# 4. Generación de datos basados en los límites dinámicos
Y_plot = np.linspace(0, limite_x, 1000)
is_curve = ((alpha + G) / b) - (((1 - c) / b) * Y_plot)
lm_curve = (k / h) * Y_plot - (ms / h)
# --- END OF CHANGES ---

# --- VISUALIZACIÓN GRÁFICA ---
# --- NEW/MODIFIED CODE: Ajuste de ejes y anotaciones ---
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(Y_plot, is_curve, label="Curva IS (Mercado de Bienes)", color="#1f77b4", lw=2.5)
ax.plot(Y_plot, lm_curve, label="Curva LM (Mercado de Dinero)", color="#d62728", lw=2.5)

# Asegurar que el punto de equilibrio sea visible
if 0 < i_star < limite_i:
    ax.scatter(Y_star, i_star, color="black", s=150, zorder=5)
    ax.vlines(Y_star, 0, i_star, linestyle="--", color="gray", alpha=0.5)
    ax.hlines(i_star, 0, Y_star, linestyle="--", color="gray", alpha=0.5)
    
    ax.annotate(f' Equilibrio (E*)\n Y* = {Y_star:.0f}\n i* = {i_star:.2f}%', 
                (Y_star, i_star), 
                xytext=(Y_star + (limite_x * 0.05), i_star + (limite_i * 0.05)),
                arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color='black'),
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="black", alpha=0.8))

# Aplicación de los límites calculados dinámicamente
ax.set_xlim(0, limite_x)
ax.set_ylim(0, limite_i)
# --- END OF CHANGES ---

ax.set_xlabel("Producción / Ingreso Nacional (Y)", fontsize=12)
ax.set_ylabel("Tasa de Interés Nominal (i)", fontsize=12)
ax.set_title("Equilibrio Macroeconómico IS/LM", fontsize=14, fontweight='bold')
ax.legend(loc="upper right")
ax.grid(True, linestyle=':', alpha=0.5)

st.pyplot(fig)

# --- RESUMEN DE INDICADORES ---
col1, col2 = st.columns(2)
col1.metric("Producción de Equilibrio (Y*)", f"{Y_star:.2f}")
col2.metric("Tasa de Interés de Equilibrio (i*)", f"{i_star:.2f}%")

with st.expander("Interpretación Económica"):
    st.write(f"""
    * **Mercado de Bienes (IS):** El cruce ocurre cuando el ahorro es igual a la inversión.
    * **Mercado de Dinero (LM):** La tasa de interés equilibra la oferta y demanda de saldos reales.
    * **Dinámica de los Ejes:** El gráfico se ajusta automáticamente para mostrar el intercepto de la curva IS y el punto de equilibrio, garantizando una visibilidad completa de los cambios de política.
    """)
