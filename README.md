
# SCN Growth Calculator (Streamlit)

Calculadora docente para estimar crecimiento esperado de **serous cystic neoplasms (SCN)** pancreaticos y detectar posibles **outliers** de crecimiento.

## Como ejecutar localmente
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Despliegue en Streamlit Community Cloud
1. Cree un repositorio en GitHub y suba estos archivos.
2. Vaya a https://share.streamlit.io, conecte su repo y seleccione `app.py`.
3. Configure la rama principal y despliegue.

## Supuestos del modelo
- Crecimiento exponencial promedio anual: **6.2%**.
- Duplicacion de tamano: **11.6 anos**.
- Banda de tolerancia: **+/- 10.74 mm** (RMSE reportado).
- La publicacion original usa splines cubicos y GLS. Esta app **aproxima** usando la tasa promedio por falta de coeficientes publicos.

> Esta herramienta es educativa y no sustituye el juicio clinico ni guias.
