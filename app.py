import streamlit as st
import pandas as pd
import numpy as np

# ------------------------------
# CONFIGURACIÓN DE LA APP
# ------------------------------
st.set_page_config(
    page_title="Asistente Radiológico",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🩻 Asistente de Parámetros Radiológicos")
st.write("Selecciona los valores y obtén tus factores.")

# ------------------------------
# CARGA DEL ARCHIVO
# ------------------------------
EXCEL_PATH = "Base de datos.xlsx"

try:
    df = pd.read_excel(EXCEL_PATH)
except Exception as e:
    st.error(f"❌ No se pudo leer '{EXCEL_PATH}'. Verifica que esté en el repositorio.")
    st.stop()

# --------------------------------
# NORMALIZACIÓN DE NOMBRES DE COLUMNAS
# --------------------------------
df.columns = (
    df.columns
    .str.strip()
    .str.replace("á", "a", regex=False)
    .str.replace("é", "e", regex=False)
    .str.replace("í", "i", regex=False)
    .str.replace("ó", "o", regex=False)
    .str.replace("ú", "u", regex=False)
    .str.replace(",", "", regex=False)  # elimina coma del nombre
    .str.lower()
)

rename_map = {
    "zona de estudio": "zona",
    "nombre de la proyeccion": "proyeccion",
    "tipo de paciente": "tipo_paciente",
    "kv hipoestenico": "kv_hipo",
    "mas hipoestenico": "mas_hipo",
    "kv normoestenico (ref unica)": "kv_normo",   # <-- nombre corregido
    "mas normoestenico (ref unica)": "mas_normo",
    "kv hiperestenico": "kv_hiper",
    "mas hiperestenico": "mas_hiper"
}

df = df.rename(columns=rename_map)

# ------------------------------
# LIMPIEZA DE VALORES
# ------------------------------
for col in ["zona", "proyeccion", "tipo_paciente"]:
    df[col] = df[col].astype(str).str.strip()

# elimina valores NaN, vacíos o basura
df = df[df["zona"].notna()]
df = df[df["zona"].str.lower() != "nan"]
df = df[df["zona"].str.lower() != "zona de estudio"]
df = df[df["zona"].str.strip() != ""]

# ------------------------------
# SELECTORES
# ------------------------------

# ZONA
zona_lista = sorted(df["zona"].unique())
zona = st.selectbox("1) Selecciona la zona de estudio:", zona_lista)

# PROYECCIÓN
proyecciones_disp = df[df["zona"] == zona]["proyeccion"].unique()
proyeccion = st.selectbox("2) Selecciona la proyección:", sorted(proyecciones_disp))

# TIPO DE PACIENTE
paciente_disp = df[
    (df["zona"] == zona) &
    (df["proyeccion"] == proyeccion)
]["tipo_paciente"].unique()

tipo_paciente = st.selectbox("3) Selecciona el tipo de paciente:", sorted(paciente_disp))

# HABITUS
habitus = st.selectbox(
    "4) Selecciona habitus corporal:",
    ["Hipoesténico", "Normoesténico", "Hiperesténico"]
)

st.markdown("---")

# ------------------------------
# FILTRO
# ------------------------------
filtro = df[
    (df["zona"] == zona) &
    (df["proyeccion"] == proyeccion) &
    (df["tipo_paciente"] == tipo_paciente)
]

if filtro.empty:
    st.err
