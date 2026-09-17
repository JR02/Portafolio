import pandas as pd
import streamlit as st
import plotly.express as px

# Configuración de la página web
st.set_page_config(page_title="Dashboard Parque Vehicular", layout="wide")

# Título Principal en Español
st.title("📊 Análisis Interactivo del Parque Vehicular")
st.markdown("Evolución histórica y composición de los vehículos registrados en el país.")

# Cargar los datos limpios generados en el notebook
@st.cache_data
def cargar_datos():
    return pd.read_csv("vehiculos_cleaned.csv")

df = cargar_datos()

# --- BARRA LATERAL (Filtros) ---
st.sidebar.header("⚙️ Filtros de Control")

# Filtro interactivo por Rango de Años
año_min, año_max = int(df['año'].min()), int(df['año'].max())
rango_años = st.sidebar.slider(
    "Selecciona el rango de años:",
    min_value=año_min,
    max_value=año_max,
    value=(año_min, año_max)
)

# Filtrar el DataFrame según la selección del usuario
df_filtrado = df[(df['año'] >= rango_años[0]) & (df['año'] <= rango_años[1])]

# --- CUADRO DE MÉTRICAS PRINCIPALES ---
st.subheader("📈 Resumen del Período Seleccionado")
col1, col2, col3 = st.columns(3)

total_inicio = df_filtrado.iloc[0]['Total_Vehiculos']
total_fin = df_filtrado.iloc[-1]['Total_Vehiculos']
crecimiento = ((total_fin - total_inicio) / total_inicio) * 100

col1.metric(f"Total Vehículos ({rango_años[0]})", f"{total_inicio:,.0f}")
col2.metric(f"Total Vehículos ({rango_años[1]})", f"{total_fin:,.0f}")
col3.metric("Crecimiento del Periodo", f"+{crecimiento:.2f}%")

# --- GRÁFICOS INTERACTIVOS (Plotly) ---
st.write("---")
col_izq, col_der = st.columns(2)

with col_izq:
    st.subheader("📉 Crecimiento Histórico por Categoría")
    # Convertir datos a formato largo para Plotly Express (excluir Total_Vehiculos)
    vehicle_cols = [col for col in df_filtrado.columns if col not in ['año', 'Total_Vehiculos']]
    df_melted = df_filtrado.melt(id_vars=['año'], value_vars=vehicle_cols, var_name='Tipo de Vehículo', value_name='Unidades')
    
    fig_lineas = px.line(
        df_melted, x='año', y='Unidades', color='Tipo de Vehículo',
        labels={'Unidades': 'Cantidad de Vehículos', 'año': 'año del Registro'},
        template="plotly_white"
    )
    st.plotly_chart(fig_lineas, use_container_width=True)

with col_der:
    st.subheader("🍕 Distribución Promedio del Parque Vehicular")
    # Calcular el promedio de cada columna en el rango seleccionado (excluir Total_Vehiculos)
    vehicle_cols = [col for col in df_filtrado.columns if col not in ['año', 'Total_Vehiculos']]
    promedios = df_filtrado[vehicle_cols].mean().reset_index()
    promedios.columns = ['Tipo de Vehículo', 'Promedio Unidades']
    
    fig_pastel = px.pie(
        promedios, values='Promedio Unidades', names='Tipo de Vehículo',
        hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu
    )
    st.plotly_chart(fig_pastel, use_container_width=True)
#Ejecuta el servidor local de Streamlit con en la terminal de VSCode. Asegúrate de estar en el entorno virtual correcto y de tener Streamlit instalado.
# .venv\Scripts\activate
#streamlit run app.py