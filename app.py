import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="DataViz Python Lab", layout="wide")
st.title("📊 Proyecto Final - DataViz Python Lab")
st.write("Análisis de indicadores económicos en tiempo real mediante API REST pública.")

indicador = st.sidebar.selectbox("Selecciona el indicador:", ["dolar", "euro", "uf", "utm"])
url = f"https://mindicador.cl/api/{indicador}"

try:
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data.get("serie", []))
        df["fecha"] = pd.to_datetime(df["fecha"]).dt.tz_localize(None)
        df = df.sort_values(by="fecha")
        
        num_registros = st.sidebar.slider("Número de últimos registros:", 5, len(df), 30)
        df_filtered = df.tail(num_registros)
        
        ultimo_valor = df_filtered["valor"].iloc[-1]
        st.metric(label=f"Último valor registrado ({indicador.upper()})", value=f"${ultimo_valor:,.2f} CLP")
        
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(df_filtered["fecha"], df_filtered["valor"], marker="o", color="#0066cc")
        ax.set_title(f"Evolución del {indicador.upper()}")
        ax.set_xlabel("Fecha")
        ax.set_ylabel("Valor (CLP)")
        ax.grid(True, linestyle="--", alpha=0.5)
        plt.xticks(rotation=45)
        st.pyplot(fig)
        
        st.subheader("Tabla de Datos")
        st.dataframe(df_filtered.rename(columns={"fecha": "Fecha", "valor": "Valor (CLP)"}))
except Exception as e:
    st.error(f"Error al conectar con la API: {e}")
