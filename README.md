# ☀️ Visualizador de Diseño para Plantas Fotovoltaicas

Una aplicación web interactiva construida con Streamlit que lee los resultados de un modelo de optimización (coordenadas de paneles, inversores y subestación) y los presenta en un dashboard visual e interactivo.

*Esta herramienta permite a ingenieros y diseñadores analizar rápidamente la disposición óptima de los componentes de una planta solar.*



---

## 📜 Descripción del Proyecto

Este proyecto nace de la necesidad de interpretar los resultados numéricos de modelos de optimización complejos. A menudo, un modelo matemático genera miles de coordenadas y asignaciones que son difíciles de analizar en un formato de tabla.

Esta aplicación web soluciona ese problema al proveer una interfaz gráfica donde los usuarios pueden:
1.  **Visualizar un caso de ejemplo** cargado por defecto.
2.  **Subir sus propios archivos CSV** con los resultados de su modelo.
3.  **Analizar la disposición** de los componentes en un mapa interactivo.
4.  **Exportar la visualización** como una imagen para reportes o presentaciones.

El objetivo es cerrar la brecha entre la optimización matemática y la interpretación visual del diseño de ingeniería.

---

## ✨ Características Principales

-   **Dashboard Interactivo:** Mapa de la planta con funciones de zoom y desplazamiento para una inspección detallada.
-   **Carga de Archivos Dinámica:** Permite a cualquier usuario subir sus propios archivos CSV para visualizar diseños personalizados.
-   **Datos por Defecto:** Incluye un conjunto de datos de ejemplo para demostrar la funcionalidad de la aplicación al instante.
-   **Métricas Clave:** Presenta un resumen del proyecto con el número total de componentes y el área estimada del terreno.
-   **Exportación de Gráficos:** Integra un botón para descargar el plano de la planta como una imagen PNG de alta calidad.
-   **Visualización de Datos:** Muestra las coordenadas exactas en tablas interactivas.

---

## 🛠️ Tecnologías Utilizadas

-   **Lenguaje:** Python
-   **Interfaz Web:** Streamlit
-   **Manipulación de Datos:** Pandas
-   **Visualización de Datos:** Plotly
-   **Exportación de Imágenes:** Kaleido

---

## 🚀 Cómo Ejecutar la Aplicación Localmente

Para ejecutar este proyecto en tu propia máquina, sigue estos pasos.

### **1. Prerrequisitos**
- Tener Python 3.8+ instalado.
- (Opcional) Usar un entorno virtual para mantener las dependencias organizadas.

### **2. Clonar el Repositorio**
```bash
git clone [https://github.com/tu-usuario/tu-repositorio.git](https://github.com/tu-usuario/tu-repositorio.git)
cd tu-repositorio
```

### **3. Instalar las Dependencias**
El archivo `requirements.txt` contiene todas las librerías necesarias.
```bash
pip install -r requirements.txt
```

### **4. Ejecutar la Aplicación**
Una vez instaladas las dependencias, lanza la aplicación con el siguiente comando:
```bash
streamlit run app.py
```
La aplicación se abrirá automáticamente en tu navegador web.

---
## 📁 Estructura del Proyecto

```
.
├── app.py                      # El script principal de la aplicación Streamlit
├── requirements.txt            # Lista de dependencias de Python
├── coordenadas_paneles.csv     # Archivo de ejemplo con datos de los paneles
├── coordenadas_inversores.csv  # Archivo de ejemplo con datos de los inversores
└── coordenadas_subestacion.csv # Archivo de ejemplo con datos de la subestación
```
