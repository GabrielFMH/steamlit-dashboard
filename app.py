import streamlit as st
import pandas as pd
import numpy as np

# Configuración de la página
st.set_page_config(
    page_title="Dashboard de Ventas",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Título de la aplicación
st.title("📊 Dashboard de Ventas")

# Generar datos ficticios
np.random.seed(42)
df = pd.DataFrame({
    'Región': np.random.choice(['Norte', 'Sur', 'Este', 'Oeste'], 1000),
    'Producto': np.random.choice(['Producto A', 'Producto B', 'Producto C'], 1000),
    'Ventas': np.random.randint(200, 2000, 1000),
    'Fecha': pd.date_range(start='2023-01-01', periods=1000, freq='D')
})

# Sidebar - Filtros
st.sidebar.header("Filtros")
regiones = st.sidebar.multiselect(
    "Selecciona la(s) Región(es):",
    options=df['Región'].unique(),
    default=df['Región'].unique()
)

productos = st.sidebar.multiselect(
    "Selecciona el(los) Producto(s):",
    options=df['Producto'].unique(),
    default=df['Producto'].unique()
)

df_filtrado = df[(df['Región'].isin(regiones)) & (df['Producto'].isin(productos))]

# KPIs
total_ventas = df_filtrado['Ventas'].sum()
ventas_promedio = df_filtrado['Ventas'].mean()
ventas_maximas = df_filtrado['Ventas'].max()

st.write("## Indicadores Clave de Rendimiento (KPIs)")
col1, col2, col3 = st.columns(3)
col1.metric("Ventas Totales", f"${total_ventas:,.0f}")
col2.metric("Venta Promedio", f"${ventas_promedio:,.2f}")
col3.metric("Venta Máxima", f"${ventas_maximas:,.0f}")

# Gráfico de barras - Ventas por región usando Streamlit
st.write("### Ventas por Región")
df_region = df_filtrado.groupby('Región')['Ventas'].sum().reset_index()
st.bar_chart(df_region.set_index('Región')['Ventas'])

# Gráfico de líneas - Ventas a lo largo del tiempo usando Streamlit
st.write("### Ventas a lo Largo del Tiempo")
df_tiempo = df_filtrado.groupby('Fecha')['Ventas'].sum().reset_index()
st.line_chart(df_tiempo.set_index('Fecha')['Ventas'])

# Gráfico de dispersión - Ventas por producto usando Streamlit
st.write("### Ventas por Producto")
df_producto = df_filtrado.groupby(['Producto', 'Región'])['Ventas'].sum().reset_index()
st.write("Nota: El gráfico de dispersión en Streamlit no es tan flexible. Este es un gráfico de datos tabulados.")
st.dataframe(df_producto.pivot(index='Producto', columns='Región', values='Ventas'))

# Tabla de detalles
st.write("### Detalles de Ventas")
st.dataframe(df_filtrado)

# Descarga de datos
st.sidebar.markdown("### Descargar Datos Filtrados")
csv = df_filtrado.to_csv(index=False).encode('utf-8')
st.sidebar.download_button(
    label="📥 Descargar CSV",
    data=csv,
    file_name='datos_filtrados.csv',
    mime='text/csv',
)
