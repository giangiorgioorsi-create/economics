import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Simulador del Modelo IS/LM", layout="wide")

# --- ENCABEZADO Y TÍTULO ---
st.title("Simulador Interactivo del Modelo IS/LM")
st.markdown("""
Esta herramienta analiza el equilibrio macroeconómico de corto plazo. El nivel de precios se considera rígido y la producción responde a las variaciones de la demanda agregada.
""")

# --- SEGMENTO DE SLIDERS EN APP.PY ---
with st.sidebar:
    st.header("Parámetros del Modelo")
    
    if st.button("Restablecer Valores Iniciales"):
        st.session_state.clear()
        st.rerun()

    st.subheader("Mercado de Bienes (Curva IS)")
    alpha = st.slider("Consumo Autónomo (α)", 100, 1500, 800, key="alpha")
    c = st.slider("Propensión Marginal al Consumo (c)", 0.1, 0.9, 0.6, key="c")
    b = st.slider("Sensibilidad de la Inversión (b)", 5, 100, 40, key="b")
    # --- CAMBIO QUIRÚRGICO: G inicial a 800 ---
    G = st.slider("Gasto Público (G)", 100, 1500, 800, key="G")
    # --- END OF CHANGES ---

    st.subheader("Mercado de Dinero (Curva LM)")
    ms = st.slider("Oferta Monetaria Real (M/P)", 100, 5000, 500, key="ms")
    k = st.slider("Sensibilidad al Ingreso (k)", 0.1, 0.9, 0.5, key="k")
    h = st.slider("Sensibilidad a la Tasa de Interés (h)", 10, 200, 100, key="h")

# --- LÓGICA MATEMÁTICA Y EQUILIBRIO ---
# Cálculo del equilibrio algebraico
num_eq = ((alpha + G) / b) + (ms / h)
den_eq = ((1 - c) / b) + (k / h)
Y_star = num_eq / den_eq
i_star = (k / h) * Y_star - (ms / h)
multiplicador = 1 / (1 - c)

# --- ESCALADO DINÁMICO ---
# Calculamos interceptos para que los ejes siempre contengan la información relevante
intercepto_is_x = (alpha + G) / (1 - c)
limite_x = max(intercepto_is_x, Y_star) * 1.2
limite_i = max((alpha + G) / b, i_star) * 1.2

Y_plot = np.linspace(0, limite_x, 1000)
is_curve = ((alpha + G) / b) - (((1 - c) / b) * Y_plot)
lm_curve = (k / h) * Y_plot - (ms / h)

# --- VISUALIZACIÓN GRÁFICA ---
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(Y_plot, is_curve, label="Curva IS (Mercado de Bienes)", color="#1f77b4", lw=2.5)
ax.plot(Y_plot, lm_curve, label="Curva LM (Mercado de Dinero)", color="#d62728", lw=2.5)

# Marcador de punto de equilibrio
if 0 < i_star < limite_i:
    ax.scatter(Y_star, i_star, color="black", s=150, zorder=5)
    ax.vlines(Y_star, 0, i_star, linestyle="--", color="gray", alpha=0.5)
    ax.hlines(i_star, 0, Y_star, linestyle="--", color="gray", alpha=0.5)
    ax.annotate(f' Equilibrio (E*)\n Y* = {Y_star:.0f}\n i* = {i_star:.2f}%', 
                (Y_star, i_star), xytext=(Y_star + (limite_x * 0.05), i_star + (limite_i * 0.05)),
                arrowprops=dict(arrowstyle="->"), bbox=dict(boxstyle="round", fc="white", ec="black", alpha=0.8))

ax.set_xlim(0, limite_x)
ax.set_ylim(0, limite_i)
ax.set_xlabel("Producción / Ingreso Nacional (Y)")
ax.set_ylabel("Tasa de Interés Nominal (i)")
ax.legend(loc="upper right")
ax.grid(True, linestyle=':', alpha=0.5)
st.pyplot(fig)

# --- TABLA COMPARATIVA ---
st.markdown("---")
st.subheader("Análisis de Impacto y Comparativa")

# Persistencia del escenario base calibrado
if 'base' not in st.session_state:
    st.session_state.base = {'Y': Y_star, 'i': i_star, 'G': G, 'M': ms}

col_btn, col_mult = st.columns([1, 1])

if col_btn.button("Fijar Escenario Actual como Base"):
    st.session_state.base = {'Y': Y_star, 'i': i_star, 'G': G, 'M': ms}
    st.success("Escenario base actualizado.")

col_mult.metric("Multiplicador Keynesiano (k)", f"{multiplicador:.2f}")

# Tabla Comparativa
tabla = {
    "Variable": ["Ingreso (Y*)", "Tasa Interés (i*)", "Gasto (G)", "Oferta Mon. (M/P)"],
    "Base": [f"{st.session_state.base['Y']:.1f}", f"{st.session_state.base['i']:.2f}%", st.session_state.base['G'], st.session_state.base['M']],
    "Actual": [f"{Y_star:.1f}", f"{i_star:.2f}%", G, ms],
    "Variación": [f"{Y_star - st.session_state.base['Y']:.1f}", f"{i_star - st.session_state.base['i']:.2f}%", G - st.session_state.base['G'], ms - st.session_state.base['M']]
}
st.table(tabla)

with st.expander("Interpretación Económica"):
    st.write(f"""
    * **Mercado de Crédito (IS):** El equilibrio iguala el ahorro con la inversión. La tasa de interés coordina a ahorradores e inversores.
    * **Mercado Monetario (LM):** La tasa de interés equilibra la oferta y demanda de dinero según el ingreso y la preferencia por liquidez.
    * **Dinámica:** Observe cómo el incremento en $G$ eleva $Y$ pero también $i$, lo que genera un desplazamiento parcial de la inversión privada.
    """)



