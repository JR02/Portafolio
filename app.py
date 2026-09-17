import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard de Ventas", layout="wide")
st.title("Dashboard de Ventas")

ventas = pd.read_excel("datos_ejemplo.xlsx")

if "Fecha" in ventas.columns:
    ventas["Fecha"] = pd.to_datetime(ventas["Fecha"])

ventas_total = float(ventas["Ventas"].sum())
ventas_promedio_diaria = float(ventas["Ventas"].mean())

ventas_por_categoria = (
    ventas.groupby("Categoria", as_index=False)["Ventas"].sum()
    .sort_values("Ventas", ascending=False)cls
)

fig = px.bar(
    ventas_por_categoria,
    x="Categoria",
    y="Ventas",
    title="Ventas por Categoría",
    labels={"Categoria": "Categoría", "Ventas": "Ventas Totales"},
    color="Categoria",
)

fig.update_layout(
    template="plotly_white",
    xaxis_tickangle=-45,
    title_x=0.5,
    legend_title_text="Categoría",
)

col1, col2 = st.columns(2)
col1.metric("Total de Ventas", f"${ventas_total:,.2f}")
col2.metric("Promedio de Ventas Diarias", f"${ventas_promedio_diaria:,.2f}")

st.plotly_chart(fig, use_container_width=True)

st.subheader("Datos de ventas")
st.dataframe(ventas, use_container_width=True)