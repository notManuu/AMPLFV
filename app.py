import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Dashboard Fotovoltaico",
    page_icon="☀️",
    layout="wide"
)

# --- FUNCIÓN PARA GENERAR DATOS DE EJEMPLO ---
def generate_sample_data(ancho_area, largo_area, num_paneles, num_inversores):
    """
    Genera DataFrames de ejemplo para paneles, inversores y subestación.
    """
    # 1. Generar Paneles Solares en una cuadrícula
    num_cols = 10
    num_rows = 10
    
    x_points = np.linspace(0.5, ancho_area - 0.5, num_cols)
    y_points = np.linspace(0.5, largo_area - 0.5, num_rows)
    
    xv, yv = np.meshgrid(x_points, y_points)
    
    panel_coords = {
        'panel_id': range(num_paneles),
        'x': xv.flatten(),
        'y': yv.flatten(),
        'inversor_asignado': [i % num_inversores for i in range(num_paneles)]
    }
    df_paneles = pd.DataFrame(panel_coords)

    # 2. Generar Inversores (distribuidos en el área)
    inversor_coords = {
        'inversor_id': range(num_inversores),
        'x': [ancho_area * 0.25, ancho_area * 0.75, ancho_area * 0.25, ancho_area * 0.75],
        'y': [largo_area * 0.25, largo_area * 0.25, largo_area * 0.75, largo_area * 0.75]
    }
    df_inversores = pd.DataFrame(inversor_coords)
    
    # 3. Generar Subestación (en una posición fija)
    subestacion_coords = {
        'x': [ancho_area / 2],
        'y': [-2]
    }
    df_subestacion = pd.DataFrame(subestacion_coords)
    
    return df_paneles, df_inversores, df_subestacion

# --- FUNCIÓN PARA GENERAR EL DASHBOARD (VERSIÓN CON LEYENDA MEJORADA) ---
def generate_dashboard(df_paneles, df_inversores, df_subestacion, ancho_terreno_definido, largo_terreno_definido):
    # --- MÉTRICAS ---
    st.header("Resumen del Proyecto")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Paneles", f"{len(df_paneles)} unidades")
    col2.metric("Total de Inversores", f"{len(df_inversores)} unidades")
    col3.metric("Área del Terreno", f"{ancho_terreno_definido * largo_terreno_definido:,.0f} m²")

    st.markdown("---")

    # --- GRÁFICO ---
    st.header("Disposición Óptima de la Planta")
    fig = go.Figure()
    
    # Añadir componentes al gráfico
    fig.add_trace(go.Scatter(
        x=df_paneles['x'], y=df_paneles['y'], mode='markers',
        marker=dict(color=df_paneles['inversor_asignado'], size=10, colorscale='Viridis', showscale=True, colorbar=dict(title='Inversor ID')),
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
        type="rect", x0=0, y0=0, x1=ancho_terreno_definido, y1=largo_terreno_definido,
        line=dict(color="RoyalBlue", width=2), fillcolor="LightSkyBlue", opacity=0.1, layer="below"
    )
    
    # Actualizamos el layout del gráfico con la nueva configuración de la leyenda
    fig.update_layout(
        title='Mapa Interactivo de la Planta Fotovoltaica (10m x 15m)',
        xaxis_title=f'Ancho del Terreno ({ancho_terreno_definido:.1f} m)', 
        yaxis_title=f'Largo del Terreno ({largo_terreno_definido:.1f} m)',
        xaxis=dict(range=[-2, ancho_terreno_definido + 2], scaleanchor="y", scaleratio=1), 
        yaxis=dict(range=[-3, largo_terreno_definido + 2]),
        height=750,
        
        legend=dict(
            title='Componentes',
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
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
    st.header("Datos Detallados de Paneles")
    st.dataframe(df_paneles)


# --- LÓGICA PRINCIPAL ---
st.title("☀️ Dashboard de Optimización de Planta Fotovoltaica")
st.info("Mostrando una distribución de ejemplo con **100 paneles** en un área de **10m x 15m**.")

# Definimos las dimensiones del terreno y la cantidad de componentes
ANCHO_TERRENO = 10
LARGO_TERRENO = 15
NUM_PANELES = 100
NUM_INVERSORES = 4

# Generamos los datos de forma programática
df_p, df_i, df_s = generate_sample_data(ANCHO_TERRENO, LARGO_TERRENO, NUM_PANELES, NUM_INVERSORES)

# Llamamos a la función que crea todo el dashboard
generate_dashboard(df_p, df_i, df_s, ANCHO_TERRENO, LARGO_TERRENO)
