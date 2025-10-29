import streamlit as st
import math

st.set_page_config(page_title="Calculadora de Crecimiento SCN", layout="centered")

st.title("Calculadora de Crecimiento de SCN (Streamlit)")
st.markdown(
    """
Herramienta **docente** para estimar el **crecimiento esperado** de neoplasias quisticas serosas (SCN) del pancreas
y detectar **posibles outliers** de crecimiento para reevaluacion clinica.

**Notas importantes**
- Modelo academico simplificado: crecimiento exponencial promedio anual **6.2%**; tiempo de duplicacion ~ **11.6 anos**.
- Banda de tolerancia: **+/- 10.74 mm (RMSE reportado)** para interpretar observado vs esperado.
- No reemplaza el juicio clinico ni guias.
"""
)

with st.expander("Supuestos y referencia del modelo", expanded=False):
    st.markdown(
        """
- Crecimiento esperado anual (media): 6.2%.
- Duplicacion de tamano aproximada: 11.6 anos.
- RMSE del modelo predictivo: 10.74 mm (validacion interna).
- La publicacion original usa splines cubicos y GLS; esta app **aproxima** con una tasa promedio por falta de coeficientes publicos.
"""
    )

st.header("Parametros")
col1, col2 = st.columns(2)
with col1:
    size_prev = st.number_input(
        "Tamano previo (mm)", min_value=1.0, value=31.0, step=1.0,
        help="Mayor diametro disponible en CT/MRI"
    )
    months = st.number_input(
        "Intervalo de seguimiento (meses)", min_value=1.0, value=12.0, step=1.0
    )
with col2:
    location = st.selectbox("Localizacion", ["Cabeza/Uncinado", "Cuello", "Cuerpo/Cola"])
    symptomatic = st.checkbox("Sintomas (dolor, ictericia, pancreatitis, etc.)", value=False)

st.subheader("Crecimiento esperado")
annual_rate = 0.062
monthly_rate = (1 + annual_rate) ** (1/12) - 1
expected_size = size_prev * ((1 + annual_rate) ** (months / 12.0))
delta_expected = expected_size - size_prev

# Evitamos st.metric para no cambiar el DOM entre reruns
st.write(f"- **Crecimiento mensual compuesto (esperado)**: {monthly_rate*100:.2f} % por mes")
st.write(f"- **Tamano esperado en el control**: {expected_size:.1f} mm (variacion esperada +{delta_expected:.1f} mm)")

st.caption("El modelo original utiliza splines; aqui se aproxima con crecimiento exponencial promedio.")

st.subheader("Comparacion con tamano observado (opcional)")
observed_size = st.number_input(
    "Tamano observado (mm)", min_value=0.0, value=0.0, step=0.5,
    help="Si no ingresa, se omite la comparacion"
)
RMSE = 10.74

alerts = []
if observed_size > 0:
    diff = observed_size - expected_size
    lower = max(0.0, expected_size - RMSE)
    upper = expected_size + RMSE

    # Todo texto simple (sin caracteres especiales ni componentes que cambien de tipo)
    st.write(f"- **Diferencia observado - esperado**: {diff:.1f} mm")
    st.write(f"- **Banda de tolerancia (+/-RMSE)**: {lower:.1f} - {upper:.1f} mm")

    if observed_size > upper:
        alerts.append("Crecimiento mayor al esperado (por encima de +RMSE) -> reevaluar y discutir con equipo multidisciplinario.")
    elif observed_size < lower:
        alerts.append("Tamano menor al esperado (por debajo de -RMSE). Verificar consistencia de medidas y modalidad.")
    else:
        alerts.append("Crecimiento dentro del rango esperado.")

st.subhe
