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
    get_municipios,
    get_divisiones,
    get_tarifas_disponibles,
    es_tarifa_horaria,
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

# Selectores Geográficos (Feature 1: Smart Locator)
st.markdown("---")
st.subheader("📍 Selector Geográfico")

# Obtener lista de estados
estados = get_estados()

# Selector de Estado
col_estado, col_municipio = st.columns(2)

with col_estado:
    # Agregar placeholder al inicio de la lista
    opciones_estado = ["Selecciona un estado"] + estados
    
    estado_seleccionado = st.selectbox(
        "Estado",
        options=opciones_estado,
        index=0,
        key="selector_estado",
        help="Selecciona tu estado para filtrar municipios"
    )

with col_municipio:
    # El selector de municipio depende del estado seleccionado
    if estado_seleccionado != "Selecciona un estado":
        municipios = get_municipios(estado_seleccionado)
        opciones_municipio = ["Selecciona un municipio"] + municipios
        
        municipio_seleccionado = st.selectbox(
            "Municipio",
            options=opciones_municipio,
            index=0,
            key="selector_municipio",
            help="Selecciona tu municipio para identificar la División CFE"
        )
    else:
        # Selector deshabilitado si no hay estado
        st.selectbox(
            "Municipio",
            options=["Selecciona primero un estado"],
            disabled=True,
            key="selector_municipio_disabled"
        )
        municipio_seleccionado = None

# Mostrar selector de División si hay municipio seleccionado
division_seleccionada = None
if estado_seleccionado != "Selecciona un estado" and municipio_seleccionado and municipio_seleccionado != "Selecciona un municipio":
    divisiones = get_divisiones(estado_seleccionado, municipio_seleccionado)
    
    if len(divisiones) == 0:
        st.warning("No se encontró división para esta combinación")
    elif len(divisiones) == 1:
        # Solo una división: mostrar directamente
        division_seleccionada = divisiones[0]
        st.success(f"📌 **División CFE:** {division_seleccionada}")
    else:
        # Múltiples divisiones: mostrar selector
        st.info(f"📍 Este municipio pertenece a **{len(divisiones)} divisiones** de CFE. Selecciona una:")
        division_seleccionada = st.selectbox(
            "División CFE",
            options=divisiones,
            key="selector_division",
            help="Selecciona la división que corresponde a tu ubicación exacta"
        )
        st.success(f"📌 **División seleccionada:** {division_seleccionada}")

# Selector de Tarifas (HU-1.3) - Selección múltiple
st.markdown("---")
st.subheader("⚡ Selector de Tarifas")

tarifas_seleccionadas = []
if division_seleccionada:
    # Obtener tarifas disponibles
    df_tarifas_disp = get_tarifas_disponibles()
    
    # Crear opciones con formato "CÓDIGO - Descripción"
    opciones_tarifa = []
    tarifa_map = {}  # Para mapear la opción al código
    for _, row in df_tarifas_disp.iterrows():
        opcion = f"{row['tarifa']} - {row['descripcion']}"
        opciones_tarifa.append(opcion)
        tarifa_map[opcion] = row['tarifa']
    
    tarifas_opciones = st.multiselect(
        "Tarifas de interés",
        options=opciones_tarifa,
        default=[],
        key="selector_tarifas",
        help="Selecciona una o más tarifas para analizar (puedes elegir varias)"
    )
    
    # Extraer códigos de tarifas seleccionadas
    if tarifas_opciones:
        tarifas_seleccionadas = [tarifa_map[op] for op in tarifas_opciones]
        
        # Clasificar tarifas seleccionadas
        horarias = [t for t in tarifas_seleccionadas if es_tarifa_horaria(t)]
        simples = [t for t in tarifas_seleccionadas if not es_tarifa_horaria(t)]
        
        # Mostrar resumen de selección
        col_info1, col_info2 = st.columns(2)
        with col_info1:
            if horarias:
                st.info(f"⏰ **Horarias:** {', '.join(horarias)}")
        with col_info2:
            if simples:
                st.info(f"📊 **Simples:** {', '.join(simples)}")
        
        st.success(f"✅ {len(tarifas_seleccionadas)} tarifa(s) seleccionada(s)")
else:
    # Selector deshabilitado si no hay división
    st.multiselect(
        "Tarifas de interés",
        options=["Selecciona primero Estado y Municipio"],
        disabled=True,
        key="selector_tarifas_disabled"
    )

# Placeholder para selector de Año (HU-1.4)
st.markdown("---")
st.subheader("🔧 En desarrollo")
st.info("El selector de Año se implementará en la siguiente historia de usuario (HU-1.4).")

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
st.caption("CFE Tariff Analyzer v0.4.0 | Desarrollado con Streamlit")
