import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="DataViz Python Lab", layout="wide")
st.title("📊 Proyecto Final - DataViz Python Lab")
st.write("Análisis de indicadores económicos en tiempo real mediante API REST pública.")

# Selección del indicador
opcion = st.sidebar.selectbox("Selecciona el indicador:", ["Dólar", "Euro"])
codigo = "dolar" if opcion == "Dólar" else "euro"

# API pública alternativa más rápida y estable para Streamlit Cloud
url = f"https://cl.dolarapi.com/v1/cotizaciones/{codigo}"

try:
    response = requests.get(url, timeout=15)
    if response.status_code == 200:
        data = response.json()
        
        # Métrica principal
        valor_actual = data.get("valor", 0)
        fecha = data.get("fechaActualizacion", "")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label=f"Valor actual ({opcion})", value=f"${valor_actual:,.2f} CLP")
        with col2:
            st.metric(label="Fecha actualización", value=fecha[:10] if fecha else "Hoy")
            
        st.markdown("---")
        st.subheader("📋 Datos del Indicador")
        st.json(data)
    else:
        st.error("No se pudo obtener respuesta de la API.")
except Exception as e:
    st.error(f"Error al conectar con la API: {e}")
