import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Dashboard Fotovoltaico",
    page_icon="☀️",
    layout="wide"
)

# --- FUNCIÓN PARA GENERAR EL DASHBOARD (Sin cambios) ---
# Esta función es reutilizable, toma los dataframes y crea la visualización.
def generate_dashboard(df_paneles, df_inversores, df_subestacion):
    # --- 1. CÁLCULO PRECISO DE DIMENSIONES ---
    margen = 5 # Metros de margen alrededor del área de paneles
    min_x, max_x = df_paneles['x'].min(), df_paneles['x'].max()
    min_y, max_y = df_paneles['y'].min(), df_paneles['y'].max()
    ancho_neto_paneles = max_x - min_x
    largo_neto_paneles = max_y - min_y
    area_neta = ancho_neto_paneles * largo_neto_paneles
    x0_terreno, y0_terreno = min_x - margen, min_y - margen
    x1_terreno, y1_terreno = max_x + margen, max_y + margen
    ancho_total_terreno = x1_terreno - x0_terreno
    largo_total_terreno = y1_terreno - y0_terreno

    # --- 2. MÉTRICAS ---
    st.header("Resumen del Proyecto")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Paneles", f"{len(df_paneles)} unidades")
    col2.metric("Total de Inversores", f"{len(df_inversores)} unidades")
    col3.metric("Área Neta de Paneles", f"{area_neta:,.1f} m²")
    st.markdown("---")

    # --- 3. GRÁFICO ---
    st.header("Disposición de la Planta Fotovoltaica")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_paneles['x'], y=df_paneles['y'], mode='markers',
        marker=dict(color=df_paneles['inversor_asignado'], size=10, colorscale='Viridis', showscale=True, colorbar=dict(title='Inversor ID')),
        name='Paneles Solares', text=df_paneles.apply(lambda row: f"Panel ID: {row['panel_id']}<br>X: {row['x']}, Y: {row['y']}<br>Inversor: {row['inversor_asignado']}", axis=1), hoverinfo='text'
    ))
    fig.add_trace(go.Scatter(
        x=df_inversores['x'], y=df_inversores['y'], mode='markers',
        marker=dict(color='red', size=15, symbol='diamond'), name='Inversores',
        text=df_inversores.apply(lambda row: f"Inversor ID: {row['inversor_id']}<br>X: {row['x']}, Y: {row['y']}", axis=1), hoverinfo='text'
    ))
    fig.add_trace(go.Scatter(
        x=df_subestacion['x'], y=df_subestacion['y'], mode='markers',
        marker=dict(color='black', size=20, symbol='star'), name='Subestación',
        text=df_subestacion.apply(lambda row: f"Subestación<br>X: {row['x']}, Y: {row['y']}", axis=1), hoverinfo='text'
    ))
    fig.add_shape(
        type="rect", x0=x0_terreno, y0=y0_terreno, x1=x1_terreno, y1=y1_terreno,
        line=dict(color="RoyalBlue", width=2), fillcolor="LightSkyBlue", opacity=0.1, layer="below"
    )
    fig.update_layout(
        title='Mapa Interactivo de la Planta Fotovoltaica (Ajuste Automático)',
        xaxis_title=f'Ancho del Terreno ({ancho_total_terreno:.1f} m)',
        yaxis_title=f'Largo del Terreno ({largo_total_terreno:.1f} m)',
        xaxis=dict(range=[x0_terreno - margen/2, x1_terreno + margen/2], scaleanchor="y", scaleratio=1),
        yaxis=dict(range=[y0_terreno - margen/2, y1_terreno + margen/2]),
        height=800,
        legend=dict(title='Componentes', orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig, use_container_width=True)

    # --- 4. EXPORTAR Y DATOS ---
    st.markdown("### Exportar Gráfico")
    img_bytes = fig.to_image(format="png", scale=2)
    st.download_button(
        label="📥 Descargar Gráfico como PNG",
        data=img_bytes,
        file_name="disposicion_planta_solar.png",
        mime="image/png"
    )
    st.markdown("---")
    st.header("Datos Detallados de Paneles")
    st.dataframe(df_paneles)


# --- BARRA LATERAL PARA CARGAR ARCHIVOS (NUEVO) ---
with st.sidebar:
    st.header("Cargar Archivos CSV")
    st.markdown("Sube tus propios archivos para actualizar el dashboard.")
    uploaded_file_paneles = st.file_uploader("1. Sube el CSV de Paneles", type="csv")
    uploaded_file_inversores = st.file_uploader("2. Sube el CSV de Inversores", type="csv")
    uploaded_file_subestacion = st.file_uploader("3. Sube el CSV de Subestación", type="csv")

# --- LÓGICA PRINCIPAL (MODIFICADA) ---
st.title("☀️ Dashboard de Planta Fotovoltaica")
st.info("Visualización con **ajuste automático** al tamaño de los datos para asegurar que todos los componentes sean visibles.")

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
        st.error("No se encontraron los archivos CSV de ejemplo. Por favor, sube tus archivos para comenzar.")