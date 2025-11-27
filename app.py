import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Asistente Radiológico", layout="wide")

st.title("🩻 Asistente de Parámetros Radiológicos")

EXCEL_PATH = "Base de datos.xlsx"

# ------------------------------
# CARGA SEGURA DEL EXCEL
# ------------------------------
try:
    df = pd.read_excel(EXCEL_PATH)
except Exception as e:
    st.error("❌ No se pudo cargar la base de datos.")
    st.stop()

# --- LIMPIEZA DE COLUMNAS ---
df.columns = (
    df.columns.str.strip()
    .str.replace("á", "a").str.replace("é", "e")
    .str.replace("í", "i").str.replace("ó", "o")
    .str.replace("ú", "u").str.replace(",", "")
    .str.lower()
)

# --- MAPEO FLEXIBLE (TOLERA ERRORES) ---
possible_cols = {
    "zona": ["zona", "zona de estudio"],
    "proyeccion": ["proyeccion", "nombre de la proyeccion"],
    "tipo_paciente": ["tipopaciente", "tipo de paciente"],
    "kv_hipo": ["kv hipoestenico"],
    "mas_hipo": ["mas hipoestenico"],
    "kv_normo": ["kv normoestenico (ref unica)"],
    "mas_normo": ["mas normoestenico (ref unica)"],
    "kv_hiper": ["kv hiperestenico"],
    "mas_hiper": ["mas hiperestenico"]
}

def find_column(df, options):
    for col in df.columns:
        if col in options:
            return col
    return None

# Asignamos los nombres definitivos
colnames = {}
for key, options in possible_cols.items():
    col = find_column(df, options)
    if col is None:
        st.error(f"❌ No encontré la columna requerida: {options}")
        st.stop()
    colnames[key] = col

df = df.rename(columns={
    colnames["zona"]: "zona",
    colnames["proyeccion"]: "proyeccion",
    colnames["tipo_paciente"]: "tipo_paciente",
    colnames["kv_hipo"]: "kv_hipo",
    colnames["mas_hipo"]: "mas_hipo",
    colnames["kv_normo"]: "kv_normo",
    colnames["mas_normo"]: "mas_normo",
    colnames["kv_hiper"]: "kv_hiper",
    colnames["mas_hiper"]: "mas_hiper"
})

# LIMPIAR FILAS VACÍAS
df = df.dropna(subset=["zona", "proyeccion", "tipo_paciente"], how="any")

# ------------------------------
# SELECTORES (LIMPIOS)
# ------------------------------
zona_list = sorted([z for z in df["zona"].unique() if z.lower() not in ["nan", "", "none"]])
zona = st.selectbox("1) Selecciona la zona de estudio:", zona_list)

proy_list = sorted(df[df["zona"] == zona]["proyeccion"].unique())
proyeccion = st.selectbox("2) Selecciona la proyección:", proy_list)

pac_list = sorted(df[(df["zona"] == zona) & (df["proyeccion"] == proyeccion)]["tipo_paciente"].unique())
tipo_paciente = st.selectbox("3) Tipo de paciente:", pac_list)

habitus = st.selectbox("4) Habitus:", ["Hipoesténico", "Normoesténico", "Hiperesténico"])

# ------------------------------
# FILTRO
# ------------------------------
filtro = df[
    (df["zona"] == zona) &
    (df["proyeccion"] == proyeccion) &
    (df["tipo_paciente"] == tipo_paciente)
]

if filtro.empty:
    st.error("⚠ No existe una fila exacta en la base de datos para esta combinación.")
    st.stop()

fila = filtro.iloc[0]

# ------------------------------
# OBTENER PARÁMETROS
# ------------------------------
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
# MOSTRAR RESULTADOS
# ------------------------------
st.subheader("📌 Parámetros Radiológicos")
col1, col2 = st.columns(2)

col1.metric("kV", str(kv))
col2.metric("mAs", str(mas))

st.success("Parámetros cargados correctamente.")

st.markdown("### 🔍 Fila utilizada")
st.dataframe(filtro)
