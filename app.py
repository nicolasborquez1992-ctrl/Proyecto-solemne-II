import streamlit as st
import requests

st.set_page_config(page_title="DataViz Python Lab", layout="wide")
st.title("📊 Proyecto Final - DataViz Python Lab")
st.write("Análisis de indicadores económicos en tiempo real mediante API REST pública.")

# Selección del indicador
opcion = st.sidebar.selectbox("Selecciona el indicador:", ["Dólar", "Euro"])
codigo = "dolar" if opcion == "Dólar" else "euro"

url = f"https://cl.dolarapi.com/v1/cotizaciones/{codigo}"

try:
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        data = response.json()
        
        # Extracción de valores
        moneda = data.get("moneda", opcion)
        compras = data.get("compra", 0)
        ventas = data.get("venta", 0)
        fecha = data.get("fechaActualizacion", "Hoy")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label=f"Valor Compra ({moneda})", value=f"${compras:,.2f} CLP")
        with col2:
            st.metric(label=f"Valor Venta ({moneda})", value=f"${ventas:,.2f} CLP")
            
        st.markdown("---")
        st.subheader("📋 Datos del Indicador")
        st.json(data)
    else:
        st.error(f"Error {response.status_code}: No se pudo obtener respuesta de la API.")
except Exception as e:
    st.error(f"Error al conectar con la API: {e}")
