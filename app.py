import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Dashboard Fotovoltaico",
    page_icon="☀️",
    layout="wide"
)

# --- FUNCIÓN PARA GENERAR EL DASHBOARD (VERSIÓN CON CÁLCULO PRECISO DE ÁREA) ---
def generate_dashboard(df_paneles, df_inversores, df_subestacion):
    # --- 1. CÁLCULO PRECISO DE DIMENSIONES ---
    margen = 5 # Metros de margen alrededor del área de paneles

    # Encontramos las coordenadas mínimas y máximas para saber el área real que ocupan los paneles
    min_x = df_paneles['x'].min()
    max_x = df_paneles['x'].max()
    min_y = df_paneles['y'].min()
    max_y = df_paneles['y'].max()

    # Calculamos el ancho y largo netos (el espacio que realmente cubren los paneles)
    ancho_neto_paneles = max_x - min_x
    largo_neto_paneles = max_y - min_y
    area_neta = ancho_neto_paneles * largo_neto_paneles

    # Definimos el área total del terreno a dibujar (el área de paneles + márgenes)
    x0_terreno, y0_terreno = min_x - margen, min_y - margen
    x1_terreno, y1_terreno = max_x + margen, max_y + margen
    ancho_total_terreno = x1_terreno - x0_terreno
    largo_total_terreno = y1_terreno - y0_terreno


    # --- 2. MÉTRICAS (ACTUALIZADAS) ---
    st.header("Resumen del Proyecto")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Paneles", f"{len(df_paneles)} unidades")
    col2.metric("Total de Inversores", f"{len(df_inversores)} unidades")
    # La métrica ahora muestra el área NETA que ocupan los paneles
    col3.metric("Área Neta de Paneles", f"{area_neta:,.1f} m²")

    st.markdown("---")

    # --- 3. GRÁFICO ---
    st.header("Disposición de la Planta Fotovoltaica")
    fig = go.Figure()

    # Añadir Paneles Solares
    fig.add_trace(go.Scatter(
        x=df_paneles['x'], y=df_paneles['y'], mode='markers',
        marker=dict(
            color=df_paneles['inversor_asignado'],
            size=10,
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title='Inversor ID')
        ),
        name='Paneles Solares',
        text=df_paneles.apply(lambda row: f"Panel ID: {row['panel_id']}<br>X: {row['x']}, Y: {row['y']}<br>Inversor: {row['inversor_asignado']}", axis=1),
        hoverinfo='text'
    ))

    # Añadir Inversores
    fig.add_trace(go.Scatter(
        x=df_inversores['x'], y=df_inversores['y'], mode='markers',
        marker=dict(color='red', size=15, symbol='diamond'), name='Inversores',
        text=df_inversores.apply(lambda row: f"Inversor ID: {row['inversor_id']}<br>X: {row['x']}, Y: {row['y']}", axis=1),
        hoverinfo='text'
    ))

    # Añadir Subestación
    fig.add_trace(go.Scatter(
        x=df_subestacion['x'], y=df_subestacion['y'], mode='markers',
        marker=dict(color='black', size=20, symbol='star'), name='Subestación',
        text=df_subestacion.apply(lambda row: f"Subestación<br>X: {row['x']}, Y: {row['y']}", axis=1),
        hoverinfo='text'
    ))

    # Dibujar el rectángulo del terreno usando las nuevas coordenadas precisas
    fig.add_shape(
        type="rect", x0=x0_terreno, y0=y0_terreno, x1=x1_terreno, y1=y1_terreno,
        line=dict(color="RoyalBlue", width=2), fillcolor="LightSkyBlue", opacity=0.1, layer="below"
    )

    # Actualizamos el layout para que se ajuste al nuevo marco
    fig.update_layout(
        title='Mapa Interactivo de la Planta Fotovoltaica (Ajuste Automático)',
        xaxis_title=f'Ancho del Terreno ({ancho_total_terreno:.1f} m)',
        yaxis_title=f'Largo del Terreno ({largo_total_terreno:.1f} m)',
        xaxis=dict(range=[x0_terreno - margen/2, x1_terreno + margen/2], scaleanchor="y", scaleratio=1),
        yaxis=dict(range=[y0_terreno - margen/2, y1_terreno + margen/2]),
        height=800,
        legend=dict(
            title='Componentes', orientation="h", yanchor="bottom",
            y=1.02, xanchor="right", x=1
        )
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


# --- LÓGICA PRINCIPAL ---
st.title("☀️ Dashboard de Planta Fotovoltaica (desde CSV)")
st.info("Visualización con **ajuste automático** al tamaño de los datos para asegurar que todos los componentes sean visibles.")

# Intentamos cargar los archivos CSV locales
try:
    df_paneles = pd.read_csv("coordenadas_paneles.csv")
    df_inversores = pd.read_csv("coordenadas_inversores.csv")
    df_subestacion = pd.read_csv("coordenadas_subestacion.csv")

    # Una vez cargados los datos, llamamos a la función que hace todo el trabajo
    generate_dashboard(df_paneles, df_inversores, df_subestacion)

except FileNotFoundError as e:
    st.error(f"Error: No se pudo encontrar el archivo '{e.filename}'.")
    st.error("Asegúrate de que los archivos CSV estén en la misma carpeta que el script.")
