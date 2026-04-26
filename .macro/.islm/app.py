# --- MANTENIENDO EL CÓDIGO PREVIO ---
# ... (Partes anteriores de cálculo de Y_star e i_star) ...

# --- NEW/MODIFIED CODE: Sistema de Comparación de Escenarios ---
st.divider()
st.subheader("Comparativa de Escenarios")

# Inicializar el estado de sesión para el escenario base
if 'base_y' not in st.session_state:
    st.session_state.base_y = Y_star
    st.session_state.base_i = i_star
    st.session_state.base_g = G
    st.session_state.base_m = ms

if st.button("Fijar como Escenario Base"):
    st.session_state.base_y = Y_star
    st.session_state.base_i = i_star
    st.session_state.base_g = G
    st.session_state.base_m = ms
    st.success("Escenario base guardado correctamente.")

# Creación de tabla comparativa
datos_comparativos = {
    "Variable": ["Producción (Y*)", "Tasa de Interés (i*)", "Gasto (G)", "Oferta Mon. (M/P)"],
    "Base": [f"{st.session_state.base_y:.2f}", f"{st.session_state.base_i:.2f}%", st.session_state.base_g, st.session_state.base_m],
    "Actual": [f"{Y_star:.2f}", f"{i_star:.2f}%", G, ms],
    "Diferencia": [f"{Y_star - st.session_state.base_y:.2f}", f"{i_star - st.session_state.base_i:.2f}%", G - st.session_state.base_g, ms - st.session_state.base_m]
}

st.table(datos_comparativos)
# --- END OF CHANGES ---

# --- EL RESTO DEL CÓDIGO SE MANTIENE IGUAL (Expander e Indicadores) ---
