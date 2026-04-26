import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Simulador del Modelo IS/LM", layout="wide")
# --- END OF CHANGES ---

# --- ENCABEZADO Y TÍTULO ---
# --- NEW/MODIFIED CODE: Títulos en español académico ---
st.title("Simulador Interactivo del Modelo IS/LM")
st.markdown("""
Esta herramienta analiza el equilibrio macroeconómico de corto plazo mediante la interacción de los mercados de bienes y dinero. 
Ajuste los parámetros en el panel lateral para observar el impacto de las políticas fiscales y monetarias sobre el ingreso nacional ($Y$) y la tasa de interés ($i$).
""")
# --- END OF CHANGES ---

# --- PARÁMETROS EN LA BARRA LATERAL ---
with st.sidebar:
    st.header("Parámetros del Modelo")
    
    # --- NEW/MODIFIED CODE: Parámetros IS ---
    st.subheader("Mercado de Bienes (Curva IS)")
    alpha = st.slider("Consumo Autónomo (α)", 100, 1000, 500, help="Nivel de consumo que no depende del ingreso.")
    c = st.slider("Propensión Marginal al Consumo (c)", 0.1, 0.9, 0.6, help="Fracción de cada unidad adicional de ingreso que se destina al consumo.")
    b = st.slider("Sensibilidad de la Inversión (b)", 5, 50, 20, help="Grado de respuesta de la inversión privada ante cambios en la tasa de interés.")
    G = st.slider("Gasto Público (G)", 100, 1000, 300, help="Instrumento de política fiscal del Gobierno Federal.")
    # --- END OF CHANGES ---

    # --- NEW/MODIFIED CODE: Parámetros LM ---
    st.subheader("Mercado de Dinero (Curva LM)")
    ms = st.slider("Oferta Monetaria Real (M/P)", 500, 3000, 1500, help="Cantidad de saldos reales determinada por el Banco Central.")
    k = st.slider("Sensibilidad al Ingreso (k)", 0.1, 0.8, 0.4, help="Demanda de dinero por motivos de transacción y precaución.")
    h = st.slider("Sensibilidad a la Tasa de Interés (h)", 5, 100, 50, help="Demanda especulativa de dinero (preferencia por la liquidez).")
    # --- END OF CHANGES ---

# --- LÓGICA MATEMÁTICA Y EQUILIBRIO ---
# --- NEW/MODIFIED CODE: Motor de cálculo ---
Y = np.linspace(1, 5000, 500)

# Curva IS: r = (alpha + G)/b - (1-c)/b * Y
is_curve = ((alpha + G) / b) - (((1 - c) / b) * Y)

# Curva LM: r = (k/h) * Y - (ms/h)
lm_curve = (k / h) * Y - (ms / h)

# Cálculo del equilibrio algebraico
# Igualando ambas funciones de tasa de interés:
numerador = ((alpha + G) / b) + (ms / h)
denominador = ((1 - c) / b) + (k / h)
Y_star = numerador / denominador
r_star = (k / h) * Y_star - (ms / h)
# --- END OF CHANGES ---

# --- VISUALIZACIÓN GRÁFICA ---
# --- NEW/MODIFIED CODE: Gráfico estilizado ---
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(Y, is_curve, label="Curva IS (Mercado de Bienes)", color="#1f77b4", lw=2.5)
ax.plot(Y, lm_curve, label="Curva LM (Mercado de Dinero)", color="#d62728", lw=2.5)

# Marcador de punto de equilibrio
if 0 < r_star < max(is_curve):
    ax.scatter(Y_star, r_star, color="black", s=120, zorder=5)
    ax.vlines(Y_star, 0, r_star, linestyle="--", color="gray", alpha=0.6)
    ax.hlines(r_star, 0, Y_star, linestyle="--", color="gray", alpha=0.6)
    ax.annotate(f' Equilibrio (E*)\n Y* = {Y_star:.0f}\n i* = {r_star:.2f}%', 
                (Y_star, r_star), xytext=(Y_star + 100, r_star + 1),
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="black", alpha=0.8))

ax.set_xlim(0, 5000)
ax.set_ylim(0, max(is_curve.max(), 25))
ax.set_xlabel("Producción / Ingreso Nacional (Y)", fontsize=12)
ax.set_ylabel("Tasa de Interés Nominal (i)", fontsize=12)
ax.set_title("Equilibrio Macroeconómico IS/LM", fontsize=14, fontweight='bold')
ax.legend(loc="upper right")
ax.grid(True, linestyle=':', alpha=0.5)

st.pyplot(fig)
# --- END OF CHANGES ---

# --- RESUMEN DE INDICADORES ---
# --- NEW/MODIFIED CODE: Métricas y contexto final ---
col1, col2 = st.columns(2)
col1.metric("Producción de Equilibrio (Y*)", f"{Y_star:.2f}")
col2.metric("Tasa de Interés de Equilibrio (i*)", f"{r_star:.2f}%")

with st.expander("Interpretación Económica"):
    st.write(f"""
    * **Mercado de Bienes (IS):** El punto de equilibrio muestra donde el ahorro es igual a la inversión. Un aumento en el **Gasto Público ($G$)** desplaza la curva hacia la derecha, elevando el ingreso.
    * **Mercado de Dinero (LM):** Refleja el equilibrio entre la oferta monetaria y la liquidez. Si el **Banco Central** incrementa la oferta ($M/P$), la tasa de interés tiende a bajar, estimulando la inversión.
    * **Efecto de Desplazamiento:** Observe cómo un cambio en la sensibilidad ($b$ o $h$) modifica la pendiente de las curvas, alterando la efectividad de las políticas económicas.
    """)
# --- END OF CHANGES ---
