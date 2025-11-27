import streamlit as st
import pandas as pd

st.set_page_config(page_title="Asistente Radiológico", layout="wide")

st.title("🩻 Asistente de Parámetros Radiológicos")
st.write("Selecciona los valores y obtén tus factores radiológicos.")

EXCEL_PATH = "Base de datos.xlsx"

# ------------------------------
# CARGA DEL EXCEL
# ------------------------------
try:
    df = pd.read_excel(EXCEL_PATH)
except Exception:
    st.error("❌ No se pudo cargar la base de datos. Verifica que el archivo exista en el repositorio.")
    st.stop()

# ------------------------------
# RENOMBRAR COLUMNAS EXACTAS
# ------------------------------
df = df.rename(columns={
    "Zona de Estudio": "zona",
    "Nombre de la Proyección": "proyeccion",
    "Tipo de paciente": "tipo_paciente",

    "kV Hipoesténico": "kv_hipo",
    "mAs Hipoesténico": "mas_hipo",

    # Estas son EXACTAS según lo que tú enviaste (con coma ,)
    "kV Normoesténico (Ref, Única)": "kv_normo",
    "mAs Normoesténico (Ref, Única)": "mas_normo",

    "kV Hiperesténico": "kv_hiper",
    "mAs Hiperesténico": "mas_hiper"
})

# ------------------------------
# LIMPIEZA DE FILAS
# ------------------------------
df = df[df["zona"].notna()]
df = df[df["zona"] != "Zona de Estudio"]  # evita que aparezca como opción repetida

# Asegurar texto limpio
df["zona"] = df["zona"].astype(str).str.strip()
df["proyeccion"] = df["proyeccion"].astype(str).str.strip()
df["tipo_paciente"] = df["tipo_paciente"].astype(str).str.strip()

# ------------------------------
# SELECTORES
# ------------------------------

# ZONAS LIMPIAS (sin nan)
zona_list = sorted(z for z in df["zona"].unique() if z.lower() not in ["nan", "", "none"])
zona = st.selectbox("1) Selecciona la zona de estudio:", zona_list)

# PROYECCIONES
proy_list = sorted(df[df["zona"] == zona]["proyeccion"].unique())
proyeccion = st.selectbox("2) Selecciona la proyección:", proy_list)

# TIPO PACIENTE
pac_list = sorted(df[(df["zona"] == zona) & (df["proyeccion"] == proyeccion)]["tipo_paciente"].unique())
tipo_paciente = st.selectbox("3) Tipo de paciente:", pac_list)

# HABITUS
habitus = st.selectbox(
    "4) Habitus corporal:",
    ["Hipoesténico", "Normoesténico", "Hiperesténico"]
)

st.markdown("---")

# ------------------------------
# FILTRO FINAL (FILA OBJETIVO)
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
# OBTENER PARÁMETROS SEGÚN HABITUS
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
st.subheader("📌 Parámetros Radiológicos Recomendados")

col1, col2 = st.columns(2)
col1.metric("kV", str(kv))
col2.metric("mAs", str(mas))

st.success("Parámetros cargados correctamente.")

st.markdown("### 🔍 Fila utilizada para el cálculo:")
st.dataframe(filtro, use_container_width=True)
