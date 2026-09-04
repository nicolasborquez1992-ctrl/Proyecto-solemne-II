import streamlit as st
import requests

st.set_page_config(page_title="DataViz Python Lab", layout="wide")
st.title("📊 Proyecto Final - DataViz Python Lab")
st.write("Análisis de indicadores económicos en tiempo real mediante API REST pública.")

# API estable y directa
url = "https://cl.dolarapi.com/v1/cotizaciones"

try:
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        data = response.json()
        
        # Opciones disponibles
        opciones = [item["moneda"] for item in data]
        seleccion = st.sidebar.selectbox("Selecciona el indicador:", opciones)
        
        # Filtrar datos de la selección
        indicador = next(item for item in data if item["moneda"] == seleccion)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label=f"Precio Compra ({seleccion})", value=f"${indicador['compra']:,.2f} CLP")
        with col2:
            st.metric(label=f"Precio Venta ({seleccion})", value=f"${indicador['venta']:,.2f} CLP")
            
        st.markdown("---")
        st.subheader("📋 Información del Indicador")
        st.json(indicador)
    else:
        st.error("No se pudieron obtener los datos de la API.")
except Exception as e:
    st.error(f"Error al conectar con la API: {e}")
