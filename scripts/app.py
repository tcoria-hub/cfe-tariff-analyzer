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
    get_anios_disponibles,
    es_tarifa_horaria,
    get_data_stats,
    verificar_match_regiones,
    calcular_variacion_diciembre,
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

# Selector de Año (HU-1.4)
st.markdown("---")
st.subheader("📅 Selector de Año")

anio_seleccionado = None
anio_comparativo = None

if tarifas_seleccionadas:
    # Obtener años disponibles (ya filtrados desde 2018)
    anios = get_anios_disponibles()
    
    # Selector de año con el más reciente como default
    anio_seleccionado = st.selectbox(
        "Año de análisis",
        options=anios,
        index=len(anios) - 1,  # Último año como default
        key="selector_anio",
        help="Selecciona el año que deseas analizar. Se comparará con el año anterior."
    )
    
    # Calcular año comparativo
    anio_comparativo = anio_seleccionado - 1
    
    # Mostrar información de comparación
    st.success(f"📊 **Análisis:** {anio_seleccionado} vs {anio_comparativo}")
    
    # Resumen de selección completa
    st.markdown("---")
    st.subheader("✅ Resumen de Selección")
    
    col_res1, col_res2, col_res3 = st.columns(3)
    with col_res1:
        st.metric("División", division_seleccionada)
    with col_res2:
        st.metric("Tarifas", f"{len(tarifas_seleccionadas)} seleccionada(s)")
    with col_res3:
        st.metric("Periodo", f"{anio_seleccionado} vs {anio_comparativo}")
    
    # KPI de Variación Total Diciembre (HU-2.1)
    st.markdown("---")
    st.subheader("📊 Comparativo Diciembre vs Diciembre")
    st.caption(f"Variación del costo total entre diciembre {anio_comparativo} y diciembre {anio_seleccionado}")
    
    # Advertencia si es el año más reciente (puede no tener diciembre)
    if anio_seleccionado == max(anios):
        st.warning(f"⚠️ {anio_seleccionado} es el año más reciente. Si no hay datos de diciembre, selecciona un año anterior.")
    
    # Mostrar KPIs para cada tarifa seleccionada
    for tarifa in tarifas_seleccionadas:
        # Calcular variación
        resultado = calcular_variacion_diciembre(
            tarifa=tarifa,
            region=division_seleccionada,
            anio_actual=anio_seleccionado,
            anio_anterior=anio_comparativo
        )
        
        st.markdown(f"#### {tarifa}")
        
        if resultado["disponible"]:
            if resultado["es_horaria"]:
                # Tarifa horaria: mostrar Base, Intermedia, Punta + Capacidad
                horarios_info = [
                    ("B", "Base"),
                    ("I", "Intermedia"),
                    ("P", "Punta"),
                    ("capacidad", "Capacidad"),
                ]
                
                # Crear tabla con datos
                col_headers = st.columns(5)
                col_headers[0].markdown("**Concepto**")
                col_headers[1].markdown(f"**Dic {anio_comparativo}**")
                col_headers[2].markdown(f"**Dic {anio_seleccionado}**")
                col_headers[3].markdown("**Variación**")
                col_headers[4].markdown("**Unidad**")
                
                for key, nombre in horarios_info:
                    datos = resultado["horarios"].get(key, {})
                    cols = st.columns(5)
                    
                    if datos.get("actual") is not None:
                        anterior = datos.get("anterior")
                        actual = datos.get("actual")
                        variacion = datos.get("variacion_pct")
                        
                        unidad = "$/kW" if key == "capacidad" else "$/kWh"
                        
                        cols[0].write(f"⏰ {nombre}" if key != "capacidad" else f"⚡ {nombre}")
                        cols[1].write(f"${anterior:.4f}" if anterior else "N/D")
                        cols[2].write(f"${actual:.4f}")
                        if variacion is not None:
                            color = "🔴" if variacion > 0 else "🟢"
                            cols[3].write(f"{color} {variacion:+.2f}%")
                        else:
                            cols[3].write("N/D")
                        cols[4].write(unidad)
                    else:
                        cols[0].write(f"⏰ {nombre}" if key != "capacidad" else f"⚡ {nombre}")
                        cols[1].write("N/D")
                        cols[2].write("N/D")
                        cols[3].write("N/D")
                        cols[4].write("-")
            else:
                # Tarifa simple: mostrar cargo Variable + Capacidad
                col_headers = st.columns(5)
                col_headers[0].markdown("**Concepto**")
                col_headers[1].markdown(f"**Dic {anio_comparativo}**")
                col_headers[2].markdown(f"**Dic {anio_seleccionado}**")
                col_headers[3].markdown("**Variación**")
                col_headers[4].markdown("**Unidad**")
                
                for key, nombre, unidad in [("simple", "Variable (Energía)", "$/kWh"), ("capacidad", "Capacidad", "$/kW")]:
                    datos = resultado["horarios"].get(key, {})
                    cols = st.columns(5)
                    
                    if datos.get("actual") is not None:
                        anterior = datos.get("anterior")
                        actual = datos.get("actual")
                        variacion = datos.get("variacion_pct")
                        
                        cols[0].write(f"📊 {nombre}")
                        cols[1].write(f"${anterior:.4f}" if anterior else "N/D")
                        cols[2].write(f"${actual:.4f}")
                        if variacion is not None:
                            color = "🔴" if variacion > 0 else "🟢"
                            cols[3].write(f"{color} {variacion:+.2f}%")
                        else:
                            cols[3].write("N/D")
                        cols[4].write(unidad)
                    else:
                        cols[0].write(f"📊 {nombre}")
                        cols[1].write("N/D")
                        cols[2].write("N/D")
                        cols[3].write("N/D")
                        cols[4].write("-")
        else:
            st.warning(f"No hay datos de diciembre para {tarifa} en {anio_seleccionado} o {anio_comparativo}")
        
        st.markdown("---")
else:
    # Selector deshabilitado si no hay tarifas
    st.selectbox(
        "Año de análisis",
        options=["Selecciona primero las tarifas"],
        disabled=True,
        key="selector_anio_disabled"
    )

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
st.caption("CFE Tariff Analyzer v1.1.0 | Desarrollado con Streamlit")
