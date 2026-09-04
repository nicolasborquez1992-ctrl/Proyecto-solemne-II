import streamlit as st
import requests
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(page_title="DataViz Python Lab", layout="wide")
st.title("📊 Proyecto Final - DataViz Python Lab")
st.write("Análisis de indicadores económicos en tiempo real mediante API REST pública.")

url = "https://cl.dolarapi.com/v1/cotizaciones"

try:
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        data = response.json()
        
        # Crear DataFrame para procesar y graficar
        df = pd.DataFrame(data)
        
        # Menú lateral para elegir indicador
        opciones = df["moneda"].tolist()
        seleccion = st.sidebar.selectbox("Selecciona el indicador:", opciones)
        
        # Filtro de datos seleccionados
        indicador = df[df["moneda"] == seleccion].iloc[0]
        
        # Métricas en columnas
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label=f"Precio Compra ({seleccion})", value=f"${indicador['compra']:,.2f} CLP")
        with col2:
            st.metric(label=f"Precio Venta ({seleccion})", value=f"${indicador['venta']:,.2f} CLP")
            
        st.markdown("---")
        
        # Sección del Gráfico
        st.subheader("📈 Comparativa de Precios (Compra vs Venta)")
        fig, ax = plt.subplots(figsize=(8, 4))
        
        monedas = df["moneda"]
        compras = df["compra"]
        ventas = df["venta"]
        
        x = range(len(monedas))
        width = 0.35
        
        ax.bar([p - width/2 for p in x], compras, width, label='Compra', color='#1f77b4')
        ax.bar([p + width/2 for p in x], ventas, width, label='Venta', color='#aec7e8')
        
        ax.set_ylabel('Valor en CLP')
        ax.set_title('Cotizaciones Actuales')
        ax.set_xticks(x)
        ax.set_xticklabels(monedas)
        ax.legend()
        ax.grid(axis='y', linestyle='--', alpha=0.5)
        
        st.pyplot(fig)
        
        # Tabla de datos
        st.subheader("📋 Tabla de Datos")
        st.dataframe(df[["moneda", "nombre", "compra", "venta", "fechaActualizacion"]])
        
    else:
        st.error("No se pudieron obtener los datos de la API.")
except Exception as e:
    st.error(f"Error al conectar con la API: {e}")
