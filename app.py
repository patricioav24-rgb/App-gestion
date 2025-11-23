import streamlit as st
import pandas as pd

st.set_page_config(page_title="Asistente Radiológico", layout="wide")

# ------------------------------
# Cargar el archivo Excel
# ------------------------------
EXCEL_PATH = "Base de datos.xlsx"

df = pd.read_excel(EXCEL_PATH)

# Renombrar columnas para trabajar más fácil internamente
df = df.rename(columns={
    "Zona de Estudio": "zona",
    "Nombre de la Proyección": "proyeccion",
    "Tipo de paciente": "tipo_paciente",
    "kV Hipoesténico": "kv_hipo",
    "mAs Hipoesténico": "mas_hipo",
    "kV Normoesténico (Ref. Única)": "kv_normo",
    "mAs Normoesténico (Ref. Única)": "mas_normo",
    "kV Hiperesténico": "kv_hiper",
    "mAs Hiperesténico": "mas_hiper"
})

st.title("🩻 Asistente de Parámetros Radiológicos")
st.write("Selecciona los parámetros para obtener los kV y mAs recomendados según tu base de datos.")

# ------------------------------
# Selectores de usuario
# ------------------------------

df["zona"] = df["zona"].astype(str)

zona = st.selectbox(
    "1) Selecciona la zona de estudio:",
    sorted(df["zona"].astype(str).unique())
)


proyecciones_filtradas = df[df["zona"] == zona]["proyeccion"].unique()
proyeccion = st.selectbox("2) Selecciona la proyección:", sorted(proyecciones_filtradas))

pacientes_filtrados = df[
    (df["zona"] == zona) &
    (df["proyeccion"] == proyeccion)
]["tipo_paciente"].unique()

tipo_paciente = st.selectbox("3) Selecciona el tipo de paciente:", sorted(pacientes_filtrados))

habitus = st.selectbox(
    "4) Selecciona habitus corporal:",
    ["Hipoesténico", "Normoesténico", "Hiperesténico"]
)

st.markdown("---")

# ------------------------------
# Calcular parámetros
# ------------------------------

filtro = df[
    (df["zona"] == zona) &
    (df["proyeccion"] == proyeccion) &
    (df["tipo_paciente"] == tipo_paciente)
]

if filtro.empty:
    st.error("⚠ No hay coincidencias con esa combinación en la base de datos.")
else:
    fila = filtro.iloc[0]

    if habitus == "Hipoesténico":
        kv = fila["kv_hipo"]
        mas = fila["mas_hipo"]
    elif habitus == "Normoesténico":
        kv = fila["kv_normo"]
        mas = fila["mas_normo"]
    else:  # Hiperesténico
        kv = fila["kv_hiper"]
        mas = fila["mas_hiper"]

    st.subheader("📌 Parámetros recomendados")
    c1, c2 = st.columns(2)

    c1.metric("kV", f"{kv}")
    c2.metric("mAs", f"{mas}")

    st.success("Parámetros obtenidos correctamente según tu base de datos.")
    st.markdown("### 🔍 Fila completa utilizada")
    st.dataframe(filtro)

