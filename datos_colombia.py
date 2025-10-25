import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns
import html

# --- Estilo de los gráficos ---
try:
    plt.style.use('seaborn-v0_8-whitegrid')
except OSError:
    st.warning("Estilo 'seaborn-v0_8-whitegrid' no encontrado. Usando estilo por defecto.")
    plt.style.use('default')

# --- Configuración de la Página ---
st.set_page_config(
    page_title="🍃 Eco-Datos Colombia | ConcienciaVerde",
    page_icon="🇨🇴",
    layout="wide"
)

# --- Cargar CSS externo ---
def cargar_css_local(nombre_archivo):
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"No se encontró el archivo CSS: {nombre_archivo}")
        st.info(f"Asegúrate de que el archivo esté en la misma carpeta que este script.")

# --- Cargar HTML externo ---
def cargar_html(nombre_archivo):
    try:
        with open(nombre_archivo, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        st.error(f"No se encontró el archivo HTML: {nombre_archivo}")
        return "<p>Error al cargar el archivo.</p>"

# --- Cargar datos desde la API ---
@st.cache_data
def cargar_datos_fncer():
    url_api = "https://www.datos.gov.co/resource/vy9n-w6hc.json"
    params = {"$limit": 10000}
    try:
        response = requests.get(url_api, params=params)
        response.raise_for_status()
        df = pd.DataFrame(response.json())

        df = df.rename(columns={
            'proyecto': 'Proyecto',
            'tipo': 'Tecnologia',
            'capacidad': 'Capacidad (MW)',
            'departamento': 'Departamento'
        })

        df['Capacidad (MW)'] = pd.to_numeric(df['Capacidad (MW)'], errors='coerce')
        df = df.dropna(subset=['Capacidad (MW)'])
        df['Departamento'] = df['Departamento'].fillna('Sin especificar')
        df['Tecnologia'] = df['Tecnologia'].fillna('Sin especificar')

        return df
    except requests.exceptions.RequestException as e:
        st.error(f"Error al cargar datos desde la API: {e}")
        return pd.DataFrame()

# --- Cargar estilos y datos ---
cargar_css_local("estadistica.css")
df_completo = cargar_datos_fncer()

# --- Título y explicación ---
st.title(" 🍃 Eco-Datos Colombia: El Futuro de la Energía Renovable")

with st.expander("Haz clic aquí para entender qué significan estos datos"):
    html_explicacion = cargar_html("explicacion.html")
    st.markdown(html_explicacion, unsafe_allow_html=True)

# --- Si los datos cargaron ---
if not df_completo.empty:
    st.sidebar.header("Filtros del Dashboard 📊")
    lista_deptos = sorted(df_completo['Departamento'].unique())
    lista_tecnologias = sorted(df_completo['Tecnologia'].unique())

    if 'deptos_seleccionados' not in st.session_state:
        st.session_state.deptos_seleccionados = lista_deptos
    if 'tecnologias_seleccionadas' not in st.session_state:
        st.session_state.tecnologias_seleccionadas = lista_tecnologias

    def seleccionar_todo_deptos(): st.session_state.deptos_seleccionados = lista_deptos
    def borrar_todo_deptos(): st.session_state.deptos_seleccionados = []
    def seleccionar_todo_tecn(): st.session_state.tecnologias_seleccionadas = lista_tecnologias
    def borrar_todo_tecn(): st.session_state.tecnologias_seleccionadas = []

    st.sidebar.subheader("Departamentos")
    col1, col2 = st.sidebar.columns(2)
    col1.button("Seleccionar Todos", on_click=seleccionar_todo_deptos, use_container_width=True)
    col2.button("Borrar Todos", on_click=borrar_todo_deptos, use_container_width=True)

    st.sidebar.multiselect(
        "Filtrar por Departamento:", options=lista_deptos,
        key='deptos_seleccionados', label_visibility="collapsed"
    )

    st.sidebar.subheader("Tecnologías")
    col3, col4 = st.sidebar.columns(2)
    col3.button("Seleccionar Todas", on_click=seleccionar_todo_tecn, use_container_width=True)
    col4.button("Borrar Todas", on_click=borrar_todo_tecn, use_container_width=True)

    st.sidebar.multiselect(
        "Filtrar por Tecnología:", options=lista_tecnologias,
        key='tecnologias_seleccionadas', label_visibility="collapsed"
    )

    df_filtrado = df_completo[
        (df_completo['Departamento'].isin(st.session_state.deptos_seleccionados)) &
        (df_completo['Tecnologia'].isin(st.session_state.tecnologias_seleccionadas))
    ]

    st.header("Resumen de Proyectos Seleccionados")
    st.caption("Usa los filtros para ver los detalles.")
    total_mw = df_filtrado['Capacidad (MW)'].sum()
    num_proyectos = len(df_filtrado)
    hogares_alimentados = total_mw * 1000
    HOGARES_TOTAL_COLOMBIA = 18_500_000
    pct_colombia = (hogares_alimentados / HOGARES_TOTAL_COLOMBIA) * 100 if HOGARES_TOTAL_COLOMBIA > 0 else 0

    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Proyectos Totales Encontrados", f"{num_proyectos:,.0f}")
    kpi2.metric("Capacidad Total (MW)", f"{total_mw:,.1f} MW")
    kpi3.metric("% de Hogares de Colombia", f"{pct_colombia:,.2f} %",
                help=f"Basado en {HOGARES_TOTAL_COLOMBIA:,.0f} hogares (DANE 2024)")

    st.markdown("---")

    st.header("Proyectos por Departamento y Tecnología")
    if df_filtrado.empty:
        st.warning("⚠️ No hay datos para los filtros seleccionados.")
    else:
        fig_col1, fig_col2 = st.columns(2)

        with fig_col1:
            st.markdown("#### Departamentos con Más Proyectos")
            df_deptos = df_filtrado.groupby('Departamento')['Proyecto'].count().nlargest(15).sort_values()
            fig1, ax1 = plt.subplots(figsize=(7, 6))
            df_deptos.plot(kind='barh', ax=ax1, color='#27ae60')
            ax1.set_xlabel('Cantidad de Proyectos')
            ax1.set_ylabel('Departamento')
            fig1.patch.set_alpha(0)
            st.pyplot(fig1)

        with fig_col2:
            st.markdown("#### Capacidad Total por Tecnología")
            df_agrupado = df_filtrado.groupby('Tecnologia')['Capacidad (MW)'].sum().sort_values()
            fig2, ax2 = plt.subplots(figsize=(7, 6))
            df_agrupado.plot(kind='barh', ax=ax2, color='#2980b9')
            ax2.set_xlabel('Capacidad Total Instalada (MW)')
            ax2.set_ylabel('Tecnología')
            fig2.patch.set_alpha(0)
            st.pyplot(fig2)

    with st.expander("Haz clic aquí para ver la tabla con el detalle de los proyectos"):
        st.dataframe(df_filtrado[['Proyecto', 'Tecnologia', 'Departamento', 'Capacidad (MW)']])

        if not df_filtrado.empty:
            st.markdown("#### Estadísticas Descriptivas (Tabla Filtrada)")
            stats_desc = df_filtrado['Capacidad (MW)'].describe()
            st.dataframe(stats_desc[['mean', '50%', 'min', '25%', '75%', 'max']].to_frame().T)
        else:
            st.caption("No hay datos para calcular estadísticas con los filtros actuales.")

else:
    st.error("Error Crítico: No se pudieron cargar los datos iniciales de FNCER.")

