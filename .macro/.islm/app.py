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
    c = st.slider("Propensión Marginal al Consumo (c)", 0.1, 0.9, 0.6, help="Fracción de cada unidad adicional de ingreso que se destina al consumo.")
    b = st.slider("Sensibilidad de la Inversión (b)", 5, 50, 20, help="Grado de respuesta de la inversión privada ante cambios en la tasa de interés.")
    G = st.slider("Gasto Público (G)", 100, 1000, 300, help="Instrumento de política fiscal del Gobierno Federal.")

    st.subheader("Mercado de Dinero (Curva LM)")
    ms = st.slider("Oferta Monetaria Real (M/P)", 500, 3000, 1500, help="Cantidad de saldos reales determinada por el Banco Central.")
    k = st.slider("Sensibilidad al Ingreso (k)", 0.1, 0.8, 0.4, help="Demanda de dinero por motivos de transacción y precaución.")
    h = st.slider("Sensibilidad a la Tasa de Interés (h)", 5, 100, 50, help="Demanda especulativa de dinero (preferencia por la liquidez).")

# --- LÓGICA MATEMÁTICA Y EQUILIBRIO ---
# --- NEW/MODIFIED CODE: Cálculo dinámico de rangos y límites ---
# 1. Calculamos el equilibrio algebraico exacto antes de generar los vectores del gráfico
# IS: i = (alpha + G)/b - (1-c)/b * Y
# LM: i = (k/h) * Y - (ms/h)
numerador_eq = ((alpha + G) / b) + (ms / h)
denominador_eq = ((1 - c) / b) + (k / h)
Y_star = numerador_eq / denominador_eq
i_star = (k / h) * Y_star - (ms / h)

# 2. Definimos un límite dinámico para el eje X (Ingreso) para asegurar visibilidad
# El gráfico mostrará al menos 5,000 unidades, o un 50% más allá del equilibrio si este es mayor
limite_x = max(5000, int(Y_star * 1.5))
Y = np.linspace(1, limite_x, 500)

# 3. Calculamos las curvas basadas en el nuevo rango dinámico
is_curve = ((alpha + G) / b) - (((1 - c) / b) * Y)
lm_curve = (k / h) * Y - (ms / h)
# --- END OF CHANGES ---

# --- VISUALIZACIÓN GRÁFICA ---
# --- NEW/MODIFIED CODE: Ajuste dinámico de los ejes del gráfico ---
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(Y, is_curve, label="Curva IS (Mercado de Bienes)", color="#1f77b4", lw=2.5)
ax.plot(Y, lm_curve, label="Curva LM (Mercado de Dinero)", color="#d62728", lw=2.5)

# Marcador de punto de equilibrio con coordenadas dinámicas
if 0 < i_star:
    ax.scatter(Y_star, i_star, color="black", s=120, zorder=5)
    ax.vlines(Y_star, 0, i_star, linestyle="--", color="gray", alpha=0.6)
    ax.hlines(i_star, 0, Y_star, linestyle="--", color="gray", alpha=0.6)
    
    # El texto de la anotación se desplaza dinámicamente según el tamaño del gráfico
    ax.annotate(f' Equilibrio (E*)\n Y* = {Y_star:.0f}\n i* = {i_star:.2f}%', 
                (Y_star, i_star), xytext=(Y_star + (limite_x * 0.02), i_star + 1),
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="black", alpha=0.8))

ax.set_xlim(0, limite_x)
# Ajuste dinámico del eje Y: tomamos el valor máximo entre la curva IS inicial, el equilibrio o un mínimo de 25%
ax.set_ylim(0, max(is_curve.max(), i_star * 1.5, 25))
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
    * **Mercado de Bienes (IS):** Representa el equilibrio donde el ahorro es igual a la inversión. Un aumento en el **Gasto Público ($G$)** desplaza la curva hacia la derecha, elevando el ingreso.
    * **Mercado de Dinero (LM):** Refleja el equilibrio entre la oferta monetaria y la liquidez. Si el **Banco Central** incrementa la oferta ($M/P$), la tasa de interés tiende a bajar, estimulando la inversión.
    * **Efecto de Desplazamiento:** Observe cómo un cambio en la sensibilidad ($b$ o $h$) modifica la pendiente de las curvas, alterando la efectividad de las políticas económicas.
    """)
