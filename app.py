import streamlit as st
import math

# ---------------------------
# Configuracion general
# ---------------------------
st.set_page_config(page_title="Calculadora de Crecimiento SCN", layout="centered")

st.title("Calculadora de Crecimiento de SCN")
st.markdown(
    """
Aplicacion **docente** para estimar el **crecimiento esperado** de neoplasias quisticas serosas (SCN) del pancreas
y detectar **posibles outliers** de crecimiento para su reevaluacion clinica.

**Notas**
- Esta app usa una **aproximacion** basada en una tasa media anual de crecimiento del **6.2%** y tiempo de duplicacion ~ **11.6 anos**.
- Se utiliza una **banda de tolerancia** de **+/- 10.74 mm (RMSE reportado)** para comparar observado vs esperado.
- No reemplaza el juicio clinico ni las guias.
"""
)

with st.expander("Supuestos y referencia del modelo", expanded=False):
    st.markdown(
        """
- Crecimiento esperado anual (media): 6.2%.
- Duplicacion de tamano aproximada: 11.6 anos.
- RMSE del modelo predictivo: 10.74 mm (validacion interna).
- La publicacion original emplea splines cubicos y modelos con minimos cuadrados generalizados.
  Esta app **simplifica** usando la tasa media por falta de coeficientes publicos del nomograma.
"""
    )

# ---------------------------
# Entradas
# ---------------------------
st.header("Parametros")

col1, col2 = st.columns(2)
with col1:
    size_prev = st.number_input(
        "Tamano previo (mm)",
        min_value=1.0,
        value=31.0,
        step=1.0,
        help="Mayor diametro disponible medido en CT o MRI"
    )
    months = st.number_input(
        "Intervalo de seguimiento (meses)",
        min_value=1.0,
        value=12.0,
        step=1.0
    )

with col2:
    location = st.selectbox("Localizacion", ["Cabeza/Uncinado", "Cuello", "Cuerpo/Cola"])
    symptomatic = st.checkbox("Sintomas (dolor, ictericia, pancreatitis, etc.)", value=False)

# ---------------------------
# Calculo de crecimiento esperado
# ---------------------------
st.subheader("Crecimiento esperado")

annual_rate = 0.062  # 6.2% anual
monthly_rate = (1.0 + annual_rate) ** (1.0 / 12.0) - 1.0
expected_size = size_prev * ((1.0 + annual_rate) ** (months / 12.0))
delta_expected = expected_size - size_prev

st.write(f"- **Crecimiento mensual compuesto (esperado)**: {monthly_rate*100:.2f} % por mes")
st.write(f"- **Tamano esperado en el control**: {expected_size:.1f} mm (variacion esperada +{delta_expected:.1f} mm)")
st.caption("El modelo original usa splines; aqui se aproxima con crecimiento exponencial promedio.")

# ---------------------------
# Comparacion con observado (opcional)
# ---------------------------
st.subheader("Comparacion con tamano observado (opcional)")
observed_size = st.number_input(
    "Tamano observado (mm)",
    min_value=0.0,
    value=0.0,
    step=0.5,
    help="Si no ingresa un valor, se omite la comparacion"
)

RMSE = 10.74
alerts = []
show_compare = False

if observed_size > 0.0:
    show_compare = True
    diff = observed_size - expected_size
    lower = max(0.0, expected_size - RMSE)
    upper = expected_size + RMSE

    st.write(f"- **Diferencia observado - esperado**: {diff:.1f} mm")
    st.write(f"- **Banda de tolerancia (+/- RMSE)**: {lower:.1f} - {upper:.1f} mm")

    if observed_size > upper:
        alerts.append("Crecimiento mayor al esperado (por encima de +RMSE). Reevaluar y discutir en equipo multidisciplinario.")
    elif observed_size < lower:
        alerts.append("Tamano menor al esperado (por debajo de -RMSE). Verificar consistencia de medicion y modalidad de imagen.")
    else:
        alerts.append("Crecimiento dentro del rango esperado para el intervalo.")

# ---------------------------
# Reglas orientativas y seguimiento
# ---------------------------
st.subheader("Reglas orientativas y alertas")
rules = []

size_for_rules = observed_size if observed_size > 0.0 else expected_size

# Regla de tamano absoluto
if size_for_rules >= 40.0:
    rules.append("Tamano >= 40 mm (4 cm): considerar discusion sobre riesgos locales y opcion quirurgica si hay crecimiento acelerado o sintomas.")

# Regla por localizacion y sintomas
if location == "Cabeza/Uncinado" and symptomatic:
    rules.append("SCN en cabeza/uncinado con sintomas: evaluar obstruccion biliar/pancreatica o compresion venosa.")

# Sugerencia de seguimiento
if show_compare and alerts and "dentro del rango esperado" in alerts[-1].lower():
    followup = "Control de imagen en 18-24 meses, si asintomatico."
else:
    followup = "Control de imagen en 6-12 meses o antes segun clinica."

if alerts:
    st.markdown("**Alertas**")
    for a in alerts:
        st.write("- " + a)

if rules:
    st.markdown("**Reglas clinicas orientativas**")
    for r in rules:
        st.write("- " + r)

st.write(f"**Sugerencia de intervalo de seguimiento:** {followup}")

st.info("Limites: medicion bidimensional, variabilidad entre CT y MRI, y esta es una aproximacion educativa sin validacion externa publica de esta forma simplificada.")

st.write("**Creditos** · Basado en datos publicados (Chang et al., Pancreatology 2024).")
