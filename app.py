
import streamlit as st
import math

st.set_page_config(page_title="SCN Growth Calculator", layout="centered")

st.title("SCN Growth Calculator")
st.markdown("""
Herramienta docente basada en datos publicados para estimar **crecimiento esperado** de neoplasias quisticas serosas (SCN) del pancreas
y detectar **posibles outliers** de crecimiento que ameriten reevaluacion clinica.

**Notas importantes**
- Modelo academico simplificado: usa crecimiento exponencial promedio anual de **6.2%** y tiempo de duplicacion ~ **11.6 anos**.
- Banda de tolerancia: +/- **10.74 mm** (RMSE reportado), para identificar crecimiento observado mayor al esperado.
- Esta herramienta **no reemplaza** el juicio clinico ni guias; es un apoyo educativo.
""")

with st.expander("Supuestos y referencias del modelo", expanded=False):
    st.markdown("""
- Crecimiento esperado anual (media): 6.2%.
- Duplicacion de tamano: ~11.6 anos.
- Error cuadratico medio (RMSE) del modelo predictivo validado internamente: 10.74 mm.
- La prediccion formal del articulo usa splines cubicos restringidos con minimos cuadrados generalizados; **esta app aproxima** con una curva exponencial simple por falta de coeficientes publicos.
    """)

st.header("Parametros de entrada")

col1, col2 = st.columns(2)
with col1:
    size_prev = st.number_input("Tamano previo (mm)", min_value=1.0, value=31.0, step=1.0, help="Mayor diametro disponible en CT/MRI")
    months = st.number_input("Intervalo de seguimiento (meses)", min_value=1.0, value=12.0, step=1.0)
with col2:
    location = st.selectbox("Localizacion", ["Cabeza/Uncinado", "Cuello", "Cuerpo/Cola"])
    symptomatic = st.checkbox("Sintomas (dolor, ictericia, pancreatitis, etc.)", value=False)

st.subheader("Calculo del crecimiento esperado")

annual_rate = 0.062  # 6.2% anual
monthly_rate = (1 + annual_rate) ** (1/12) - 1  # tasa mensual compuesta
expected_size = size_prev * ((1 + annual_rate) ** (months / 12.0))
delta_expected = expected_size - size_prev

st.metric(label="Crecimiento mensual compuesto (esperado)", value=f"{monthly_rate*100:.2f} %/mes")
st.metric(label="Tamano esperado en el control", value=f"{expected_size:.1f} mm", delta=f"+{delta_expected:.1f} mm")

st.caption("El modelo original utiliza splines; aqui se aproxima con crecimiento exponencial promedio.")

st.subheader("Comparacion con tamano observado (opcional)")
observed_size = st.number_input("Tamano observado (mm)", min_value=0.0, value=0.0, step=0.5, help="Si no ingresa, se omite la comparacion")
RMSE = 10.74

alerts = []
if observed_size > 0:
    diff = observed_size - expected_size
    st.write(f"Diferencia observado - esperado: **{diff:.1f} mm**")
    upper = expected_size + RMSE
    lower = max(0.0, expected_size - RMSE)
    st.write(f"Banda de tolerancia (+/-RMSE): **{lower:.1f} – {upper:.1f} mm**")
    if observed_size > upper:
        alerts.append("Crecimiento mayor al esperado (por encima de +RMSE) -> reevaluar y discutir con equipo multidisciplinario.")
    elif observed_size < lower:
        alerts.append("Tamano menor al esperado (por debajo de -RMSE). Verificar consistencia de medidas y modalidad.")
    else:
        alerts.append("Crecimiento dentro del rango esperado.")

# Reglas clinicas orientativas
st.subheader("Reglas orientativas y alertas")
rules = []

# Regla tamano absoluto cercano a 40 mm
if observed_size > 0:
    size_for_rules = observed_size
else:
    size_for_rules = expected_size

if size_for_rules >= 40:
    rules.append("Tamano >= 40 mm (4 cm): considerar discusion sobre riesgos locales y opcion quirurgica si hay crecimiento acelerado o sintomas.")

# Localizacion cabeza con sintomas
if location == "Cabeza/Uncinado" and symptomatic:
    rules.append("SCN en cabeza/uncinado con sintomas: evaluar obstruccion biliar/pancreatica o compresion venosa.")

# Intervalo de seguimiento sugerido
if observed_size > 0 and len(alerts)>0 and "dentro del rango esperado" in alerts[-1].lower():
    followup = "Control de imagen en 18–24 meses, si asintomatico."
else:
    followup = "Control de imagen en 6–12 meses o antes segun clinica."

if alerts:
    st.markdown("**Alertas**")
    for a in alerts:
        st.write("- " + a)

if rules:
    st.markdown("**Reglas clinicas orientativas**")
    for r in rules:
        st.write("- " + r)

st.markdown(f"**Sugerencia de intervalo de seguimiento:** {followup}")

st.info("Limites: medicion bidimensional, variabilidad CT/MRI, falta de validacion externa publica para esta aproximacion. Use con criterio clinico.")

st.divider()
st.markdown("**Creditos** · Basado en datos publicados (Chang et al., Pancreatology 2024). Esta app es con fines educativos.")
