import streamlit as st
import pandas as pd

# ------------------------------
# CONFIGURACIÓN DE LA APP
# ------------------------------
st.set_page_config(
    page_title="Asistente Radiológico",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🩻 Asistente de Parámetros Radiológicos")
st.write("Aplicación para seleccionar zona, proyección, tipo de paciente y habitus para obtener parámetros kV y mAs.")

# ------------------------------
# CARGA DEL ARCHIVO EXCEL (desde GitHub/Cloud local)
# ------------------------------
EXCEL_PATH = "Base de datos.xlsx"  # Debe existir en el repo

try:
    df = pd.read_excel(EXCEL_PATH)
except Exception as e:
    st.error(f"❌ No se pudo leer el archivo '{EXCEL_PATH}'. Verifica que esté en el repositorio.")
    st.stop()

# ------------------------------
# RENOMBRAR COLUMNAS PARA TRABAJAR CÓMODAMENTE
# ------------------------------
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

# Asegurar que las columnas categóricas sean texto
df["zona"] = df["zona"].astype(str)
df["proyeccion"] = df["proyeccion"].astype(str)
df["tipo_paciente"] = df["tipo_paciente"].astype(str)

# ------------------------------
# SELECTORES
# ------------------------------

# ZONA
zona = st.selectbox(
    "1) Selecciona la zona de estudio:",
    sorted(df["zona"].unique())
)

# PROYECCIÓN (dependiente de zona)
proyecciones_disp = df[df["zona"] == zona]["proyeccion"].unique()
proyeccion = st.selectbox(
    "2) Selecciona la proyección:",
    sorted(proyecciones_disp)
)

# TIPO DE PACIENTE (adulto/pediátrico)
paciente_disp = df[
    (df["zona"] == zona) &
    (df["proyeccion"] == proyeccion)
]["tipo_paciente"].unique()

tipo_paciente = st.selectbox(
    "3) Selecciona el tipo de paciente:",
    sorted(paciente_disp)
)

# HABITUS
habitus = st.selectbox(
    "4) Selecciona habitus corporal:",
    ["Hipoesténico", "Normoesténico", "Hiperesténico"]
)

st.markdown("---")

# ------------------------------
# FILTRO Y OBTENCIÓN DE PARÁMETROS
# ------------------------------

filtro = df[
    (df["zona"] == zona) &
    (df["proyeccion"] == proyeccion) &
    (df["tipo_paciente"] == tipo_paciente)
]

if filtro.empty:
    st.error("⚠ No existe una fila exacta con esa combinación en la base de datos.")
    st.stop()

fila = filtro.iloc[0]

if habitus == "Hipoesténico":
    kv = fila["kv_hipo"]
    mas = fila["mas_hipo"]
elif habitus == "Normoesténico":
    kv = fila["kv_normo"]
    mas = fila["mas_normo"]
else:
    kv = fila["kv_hiper"]
    mas = fila["mas_hiper"]

# ------------------------------
# RESULTADOS VISUALES
# ------------------------------
st.subheader("📌 Parámetros recomendados según tu base de datos")

col1, col2 = st.columns(2)

col1.metric("kV", f"{kv}")
col2.metric("mAs", f"{mas}")

st.success("Parámetros cargados correctamente.")

st.markdown("### 🔍 Fila utilizada para el cálculo")
st.dataframe(filtro, use_container_width=True)

