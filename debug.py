import streamlit as st
import pandas as pd
import requests

st.set_page_config(layout="wide")

st.title("Herramienta de Depuración de API")
st.write("Datos 'en crudo' de datos.gov.co (vy9n-w6hc)")

# URL de la API que estamos probando
url_api = "https://www.datos.gov.co/resource/vy9n-w6hc.json"
params = {"$limit": 10} # Solo necesitamos 10 filas

try:
    response = requests.get(url_api, params=params)
    response.raise_for_status() 
    data_json = response.json()
    
    # Convertir a DataFrame PERO SIN RENOMBRAR
    df = pd.DataFrame(data_json)
    
    # --- ¡ clave! ---
    st.subheader("Primeras Filas (Datos en Crudo):")
    st.dataframe(df.head())
    
    st.subheader("Nombres Reales de las Columnas:")
    st.write(df.columns.to_list()) # Mostramos los nombres como una lista
    
    st.info("Por favor, busca en la tabla de arriba la columna que tiene los números de 'Capacidad' y comparte su nombre exacto (de la lista) con el programador.")

except Exception as e:
    st.error(f"Error al cargar los datos: {e}")