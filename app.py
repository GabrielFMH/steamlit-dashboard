import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import plotly.express as px

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

# Gráfico de barras - Ventas por región usando Seaborn
st.write("### Ventas por Región")
fig1 = sns.barplot(x='Región', y='Ventas', data=df_filtrado, estimator=np.sum, ci=None, palette="coolwarm")
fig1.set_title("Total de Ventas por Región")
fig1.set_xlabel("Región")
fig1.set_ylabel("Total de Ventas")
st.pyplot(fig1.figure)  # Usa el objeto `figure` para mostrar con `st.pyplot`

# Gráfico de líneas - Ventas a lo largo del tiempo usando Plotly
st.write("### Ventas a lo Largo del Tiempo")
df_tiempo = df_filtrado.groupby('Fecha').sum().reset_index()
fig2 = px.line(df_tiempo, x='Fecha', y='Ventas', title='Tendencia de Ventas Diarias')
st.plotly_chart(fig2)

# Gráfico de dispersión - Ventas por producto usando Seaborn
st.write("### Ventas por Producto")
fig3 = sns.scatterplot(x='Producto', y='Ventas', data=df_filtrado, hue='Región', palette='Set1', s=100)
fig3.set_title("Ventas por Producto")
fig3.set_xlabel("Producto")
fig3.set_ylabel("Ventas")
st.pyplot(fig3.figure)  # Usa el objeto `figure` para mostrar con `st.pyplot`

# Gráfico de mapa - Ventas por región (Mapa de calor) usando Plotly
st.write("### Mapa de Ventas por Región")
df_mapa = df_filtrado.groupby('Región').sum(numeric_only=True).reset_index()
fig4 = px.choropleth(df_mapa, 
                     locations='Región', 
                     locationmode='geojson-id',
                     geojson='https://raw.githubusercontent.com/johan/world.geo.json/master/countries/USA/regions.geo.json',
                     color='Ventas', 
                     scope='usa',
                     title="Ventas por Región (Mapa de Calor)",
                     color_continuous_scale='Viridis')
st.plotly_chart(fig4)

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
