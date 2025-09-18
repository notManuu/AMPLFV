import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Dashboard Fotovoltaico",
    page_icon="☀️",
    layout="wide"
)

# --- FUNCIÓN PARA GENERAR EL DASHBOARD ---
# Creamos una función para no repetir el código.
# Esta función toma los DataFrames y genera todos los elementos visuales.
def generate_dashboard(df_paneles, df_inversores, df_subestacion):
    # --- CÁLCULO DE DIMENSIONES ---
    max_x = df_paneles['x'].max()
    max_y = df_paneles['y'].max()
    margen = 10
    ancho_terreno = max_x + margen
    largo_terreno = max_y + margen

    # --- MÉTRICAS ---
    st.header("Resumen del Proyecto")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Paneles", f"{len(df_paneles)} unidades")
    col2.metric("Total de Inversores", f"{len(df_inversores)} unidades")
    col3.metric("Área Estimada del Terreno", f"{ancho_terreno * largo_terreno:,.0f} m²")

    st.markdown("---")

    # --- GRÁFICO ---
    st.header("Disposición Óptima de la Planta")
    fig = go.Figure()
    
    # Añadir componentes al gráfico
    fig.add_trace(go.Scatter(
        x=df_paneles['x'], y=df_paneles['y'], mode='markers',
        marker=dict(color=df_paneles['inversor_asignado'], size=8, colorscale='Viridis', showscale=True, colorbar=dict(title='Inversor ID')),
        name='Paneles Solares', text=df_paneles.apply(lambda row: f"Panel ID: {row['panel_id']}<br>Inversor: {row['inversor_asignado']}", axis=1), hoverinfo='text'
    ))
    fig.add_trace(go.Scatter(
        x=df_inversores['x'], y=df_inversores['y'], mode='markers',
        marker=dict(color='red', size=15, symbol='diamond'), name='Inversores',
        text=df_inversores['inversor_id'].apply(lambda id: f"Inversor ID: {id}"), hoverinfo='text'
    ))
    fig.add_trace(go.Scatter(
        x=df_subestacion['x'], y=df_subestacion['y'], mode='markers',
        marker=dict(color='black', size=20, symbol='star'), name='Subestación',
        text="Subestación", hoverinfo='text'
    ))
    fig.add_shape(
        type="rect", x0=0, y0=0, x1=ancho_terreno, y1=largo_terreno,
        line=dict(color="RoyalBlue", width=2), fillcolor="LightSkyBlue", opacity=0.1, layer="below"
    )
    fig.update_layout(
        title='Mapa Interactivo de la Planta Fotovoltaica',
        xaxis_title=f'Ancho del Terreno ({ancho_terreno:.1f} m)', yaxis_title=f'Largo del Terreno ({largo_terreno:.1f} m)',
        xaxis=dict(range=[-5, ancho_terreno + 5], scaleanchor="y", scaleratio=1), yaxis=dict(range=[-5, largo_terreno + 5]),
        legend_title_text='Componentes', height=700
    )
    st.plotly_chart(fig, use_container_width=True)

    # --- BOTÓN DE DESCARGA ---
    st.markdown("### Exportar Gráfico")
    img_bytes = fig.to_image(format="png", scale=2)
    st.download_button(
        label="📥 Descargar Gráfico como PNG",
        data=img_bytes,
        file_name="disposicion_planta_solar.png",
        mime="image/png"
    )
    st.markdown("---")

    # --- TABLA DE DATOS ---
    st.header("Datos Detallados")
    st.dataframe(df_paneles)

# --- BARRA LATERAL PARA CARGAR ARCHIVOS ---
with st.sidebar:
    st.header("Cargar Archivos CSV")
    st.markdown("Sube tus propios archivos para actualizar el dashboard.")
    uploaded_file_paneles = st.file_uploader("1. Sube el CSV de Paneles", type="csv")
    uploaded_file_inversores = st.file_uploader("2. Sube el CSV de Inversores", type="csv")
    uploaded_file_subestacion = st.file_uploader("3. Sube el CSV de Subestación", type="csv")

# --- LÓGICA PRINCIPAL ---
st.title("☀️ Dashboard de Optimización de Planta Fotovoltaica")

# Si el usuario subió sus propios archivos, úsalos.
if uploaded_file_paneles and uploaded_file_inversores and uploaded_file_subestacion:
    st.success("¡Archivos cargados! Mostrando visualización para tus datos.")
    df_p = pd.read_csv(uploaded_file_paneles)
    df_i = pd.read_csv(uploaded_file_inversores)
    df_s = pd.read_csv(uploaded_file_subestacion)
    generate_dashboard(df_p, df_i, df_s)
# Si no, intenta cargar los archivos locales como ejemplo.
else:
    st.info("Mostrando datos de ejemplo. Sube tus propios archivos en la barra lateral para actualizarlos.")
    try:
        df_p_local = pd.read_csv("coordenadas_paneles.csv")
        df_i_local = pd.read_csv("coordenadas_inversores.csv")
        df_s_local = pd.read_csv("coordenadas_subestacion.csv")
        generate_dashboard(df_p_local, df_i_local, df_s_local)
    except FileNotFoundError:
        st.error("No se encontraron los archivos CSV de ejemplo locales. Por favor, sube tus archivos para comenzar.")