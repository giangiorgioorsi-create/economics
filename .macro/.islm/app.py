import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Simulador IS/LM", layout="wide")

# --- VALORES INICIALES (DE FÁBRICA) ---
# Definimos los valores base para asegurar que sliders y gráfico nazcan y mueran juntos
DEFAULTS = {
    'alpha': 800.0,
    'c': 0.6,
    'b': 40.0,
    'G': 800.0,
    'ms': 500.0,
    'k': 0.5,
    'h': 100.0
}

# Inicializar session_state al cargar la app por primera vez
for key, val in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = val

# --- ENCABEZADO ---
st.title("Simulador Interactivo del Modelo IS/LM")
st.markdown("Ajuste los parámetros para observar el equilibrio. El botón de restablecer sincroniza **sliders y gráfico** al estado inicial.")

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("Controles del Modelo")
    
    # BOTÓN DE RESET TOTAL: Sincroniza sliders y gráfico
    if st.button("Restablecer Parámetros Iniciales"):
        # Actualizamos explícitamente los valores en el session_state
        for key, val in DEFAULTS.items():
            st.session_state[key] = val
        # Forzamos el reinicio para que los sliders lean los nuevos valores del session_state
        st.rerun()

    st.subheader("Mercado de Bienes (IS)")
    # Al asignar una 'key' y tener el valor ya en session_state, el slider se vincula bidireccionalmente
    alpha = st.slider("Consumo Autónomo (α)", 100.0, 1500.0, key="alpha")
    c = st.slider("Propensión Marginal al Consumo (c)", 0.1, 0.9, key="c")
    b = st.slider("Sensibilidad de la Inversión (b)", 5.0, 100.0, key="b")
    G = st.slider("Gasto Público (G)", 100.0, 1500.0, key="G")

    st.subheader("Mercado de Dinero (LM)")
    ms = st.slider("Oferta Monetaria Real (M/P)", 100.0, 5000.0, key="ms")
    k = st.slider("Sensibilidad al Ingreso (k)", 0.1, 0.9, key="k")
    h = st.slider("Sensibilidad a la Tasa de Interés (h)", 10.0, 200.0, key="h")

# --- LÓGICA MATEMÁTICA ---
# Cálculo del equilibrio algebraico Y* e i*
num_eq = ((alpha + G) / b) + (ms / h)
den_eq = ((1 - c) / b) + (k / h)
Y_star = num_eq / den_eq
i_star = (k / h) * Y_star - (ms / h)
multiplicador = 1 / (1 - c)

# Escalado dinámico de los ejes para que el cruce siempre esté centrado
intercepto_is_x = (alpha + G) / (1 - c)
limite_x = max(intercepto_is_x, Y_star) * 1.2
limite_i = max((alpha + G) / b, i_star) * 1.2

Y_plot = np.linspace(0.1, limite_x, 1000)
is_curve = ((alpha + G) / b) - (((1 - c) / b) * Y_plot)
lm_curve = (k / h) * Y_plot - (ms / h)

# --- VISUALIZACIÓN ---
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(Y_plot, is_curve, label="Curva IS (Bienes)", color="#1f77b4", lw=2.5)
ax.plot(Y_plot, lm_curve, label="Curva LM (Dinero)", color="#d62728", lw=2.5)

# Punto de equilibrio
if 0 < i_star < limite_i:
    ax.scatter(Y_star, i_star, color="black", s=150, zorder=5)
    ax.vlines(Y_star, 0, i_star, linestyle="--", color="gray", alpha=0.5)
    ax.hlines(i_star, 0, Y_star, linestyle="--", color="gray", alpha=0.5)
    ax.annotate(f' Equilibrio\n Y*={Y_star:.0f}, i*={i_star:.2f}%', 
                (Y_star, i_star), xytext=(Y_star*1.05, i_star*1.05),
                arrowprops=dict(arrowstyle="->"), 
                bbox=dict(boxstyle="round", fc="white", alpha=0.8))

ax.set_xlim(0, limite_x)
ax.set_ylim(0, limite_i)
ax.set_xlabel("Producción / Ingreso (Y)")
ax.set_ylabel("Tasa de Interés (i)")
ax.legend()
ax.grid(True, alpha=0.3)
st.pyplot(fig)

# --- CUADRO DE MANDO ---
st.markdown("---")
st.subheader("Análisis de Impacto")

# Asegurar que el escenario base exista tras un reset
if 'base' not in st.session_state:
    st.session_state.base = {'Y': Y_star, 'i': i_star, 'G': G, 'M': ms}

col1, col2 = st.columns([1, 1])
if col1.button("Fijar Escenario Actual como Base"):
    st.session_state.base = {'Y': Y_star, 'i': i_star, 'G': G, 'M': ms}
    st.success("Base actualizada.")

col2.metric("Multiplicador Keynesiano", f"{multiplicador:.2f}")

st.table({
    "Variable": ["Ingreso (Y*)", "Tasa Interés (i*)", "Gasto (G)", "Oferta Mon. (M/P)"],
    "Base": [f"{st.session_state.base['Y']:.1f}", f"{st.session_state.base['i']:.2f}%", st.session_state.base['G'], st.session_state.base['M']],
    "Actual": [f"{Y_star:.1f}", f"{i_star:.2f}%", G, ms],
    "Variación": [f"{Y_star - st.session_state.base['Y']:.1f}", f"{i_star - st.session_state.base['i']:.2f}%", G - st.session_state.base['G'], ms - st.session_state.base['M']]
})
