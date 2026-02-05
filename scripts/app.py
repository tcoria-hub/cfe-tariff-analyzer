"""
CFE Tariff Analyzer - Aplicación Principal
==========================================
Análisis interactivo de tarifas de CFE por ubicación geográfica.
"""

import streamlit as st
from data_loader import (
    load_geografia,
    load_tarifas,
    get_estados,
    get_data_stats,
    verificar_match_regiones,
)

# Configuración de la página
st.set_page_config(
    page_title="CFE Tariff Analyzer",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
st.title("⚡ CFE Tariff Analyzer")
st.markdown("---")

# Cargar datos al iniciar
with st.spinner("Cargando datos..."):
    df_geografia = load_geografia()
    df_tarifas = load_tarifas()
    stats = get_data_stats()
    match_info = verificar_match_regiones()

# Mensaje de bienvenida
st.header("Bienvenido")
st.markdown("""
Esta aplicación te permite analizar las tarifas de la Comisión Federal de Electricidad (CFE) 
de manera interactiva, comparando costos por ubicación geográfica y periodo de tiempo.

### Características principales:
- 📍 **Selector Geográfico**: Encuentra tu tarifa por Estado y Municipio
- 📊 **Comparativo Anual**: Analiza variaciones Diciembre vs Diciembre
- 📈 **Tendencias**: Visualiza promedios anuales y patrones mensuales
- ⏰ **Inteligencia Horaria**: Detección automática de tarifas Base/Intermedia/Punta
""")

# Estadísticas de datos cargados
st.markdown("---")
st.subheader("📊 Datos Cargados")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Registros Geografía",
        value=f"{stats['geografia']['total_registros']:,}"
    )
with col2:
    st.metric(
        label="Estados",
        value=stats['geografia']['estados']
    )
with col3:
    st.metric(
        label="Registros Tarifas",
        value=f"{stats['tarifas']['total_registros']:,}"
    )
with col4:
    st.metric(
        label="Rango de Años",
        value=f"{stats['tarifas']['anio_min']} - {stats['tarifas']['anio_max']}"
    )

# Verificación de match entre regiones
if match_info["match_exitoso"]:
    st.success(f"✅ Match de regiones exitoso: {match_info['coinciden']} divisiones/regiones coinciden")
else:
    st.warning(f"⚠️ Algunas regiones no coinciden entre geografía y tarifas")
    if match_info["solo_en_geografia"]:
        st.caption(f"Solo en geografía: {', '.join(match_info['solo_en_geografia'])}")
    if match_info["solo_en_tarifas"]:
        st.caption(f"Solo en tarifas: {', '.join(match_info['solo_en_tarifas'])}")

# Placeholder para los selectores (se implementarán en HU-1.x)
st.markdown("---")
st.subheader("🔧 En desarrollo")
st.info("Los selectores de Estado, Municipio y Tarifa se implementarán en las siguientes historias de usuario.")

# Expandible con detalles de datos
with st.expander("Ver detalles de los datos"):
    st.markdown("#### Geografía (primeros 10 registros)")
    st.dataframe(df_geografia.head(10), use_container_width=True)
    
    st.markdown("#### Tarifas (primeros 10 registros)")
    st.dataframe(df_tarifas.head(10), use_container_width=True)
    
    st.markdown("#### Estadísticas completas")
    col1, col2 = st.columns(2)
    with col1:
        st.json(stats["geografia"])
    with col2:
        st.json(stats["tarifas"])

# Footer
st.markdown("---")
st.caption("CFE Tariff Analyzer v0.2.0 | Desarrollado con Streamlit")
