"""
CFE Tariff Analyzer - Aplicación Principal
==========================================
Análisis interactivo de tarifas de CFE por ubicación geográfica.
"""

import streamlit as st
import plotly.express as px
import pandas as pd
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
    calcular_variacion_componentes,
    get_datos_tendencia_comparativa,
    calcular_variacion_promedio_anual,
    mes_a_numero,
    numero_a_mes,
    calcular_rango_12_meses,
    pivotar_historico_por_mes,
    MESES_NOMBRES,
)

# Configuración de la página
st.set_page_config(
    page_title="CFE - Analizador de Tarifas",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Logo y título principal
col_logo, col_title = st.columns([1, 4])
with col_logo:
    st.image("assets/cfe_logo.svg", width=150)
with col_title:
    st.title("Analizador de Tarifas")
    st.caption("Análisis interactivo de tarifas eléctricas CFE")
st.markdown("---")

# Cargar datos al iniciar
with st.spinner("Cargando datos..."):
    df_geografia = load_geografia()
    df_tarifas = load_tarifas()
    stats = get_data_stats()
    match_info = verificar_match_regiones()

# Inicializar session_state para mantener estado entre modos
if 'estado_seleccionado' not in st.session_state:
    st.session_state.estado_seleccionado = "Selecciona un estado"
if 'municipio_seleccionado' not in st.session_state:
    st.session_state.municipio_seleccionado = None
if 'division_seleccionada' not in st.session_state:
    st.session_state.division_seleccionada = None
if 'tarifas_seleccionadas' not in st.session_state:
    st.session_state.tarifas_seleccionadas = []
if 'anio_seleccionado' not in st.session_state:
    st.session_state.anio_seleccionado = None

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
    
    # Usar session_state para mantener el valor entre modos
    index_estado = opciones_estado.index(st.session_state.estado_seleccionado) if st.session_state.estado_seleccionado in opciones_estado else 0
    estado_seleccionado = st.selectbox(
        "Estado",
        options=opciones_estado,
        index=index_estado,
        key="selector_estado",
        help="Selecciona tu estado para filtrar municipios"
    )
    st.session_state.estado_seleccionado = estado_seleccionado

with col_municipio:
    # El selector de municipio depende del estado seleccionado
    if estado_seleccionado != "Selecciona un estado":
        municipios = get_municipios(estado_seleccionado)
        opciones_municipio = ["Selecciona un municipio"] + municipios
        
        # Mantener selección previa si aplica
        if st.session_state.municipio_seleccionado and st.session_state.municipio_seleccionado in opciones_municipio:
            index_municipio = opciones_municipio.index(st.session_state.municipio_seleccionado)
        else:
            index_municipio = 0
        
        municipio_seleccionado = st.selectbox(
            "Municipio",
            options=opciones_municipio,
            index=index_municipio,
            key="selector_municipio",
            help="Selecciona tu municipio para identificar la División CFE"
        )
        st.session_state.municipio_seleccionado = municipio_seleccionado if municipio_seleccionado != "Selecciona un municipio" else None
    else:
        # Selector deshabilitado si no hay estado
        st.selectbox(
            "Municipio",
            options=["Selecciona primero un estado"],
            disabled=True,
            key="selector_municipio_disabled"
        )
        municipio_seleccionado = None
        st.session_state.municipio_seleccionado = None

# Mostrar selector de División si hay municipio seleccionado
division_seleccionada = None
if estado_seleccionado != "Selecciona un estado" and municipio_seleccionado and municipio_seleccionado != "Selecciona un municipio":
    divisiones = get_divisiones(estado_seleccionado, municipio_seleccionado)
    
    if len(divisiones) == 0:
        st.warning("No se encontró división para esta combinación")
        st.session_state.division_seleccionada = None
    elif len(divisiones) == 1:
        # Solo una división: mostrar directamente
        division_seleccionada = divisiones[0]
        st.session_state.division_seleccionada = division_seleccionada
        st.success(f"📌 **División CFE:** {division_seleccionada}")
    else:
        # Múltiples divisiones: mostrar selector
        st.info(f"📍 Este municipio pertenece a **{len(divisiones)} divisiones** de CFE. Selecciona una:")
        # Mantener selección previa si aplica
        if st.session_state.division_seleccionada and st.session_state.division_seleccionada in divisiones:
            index_division = divisiones.index(st.session_state.division_seleccionada)
        else:
            index_division = 0
        division_seleccionada = st.selectbox(
            "División CFE",
            options=divisiones,
            index=index_division,
            key="selector_division",
            help="Selecciona la división que corresponde a tu ubicación exacta"
        )
        st.session_state.division_seleccionada = division_seleccionada
        st.success(f"📌 **División seleccionada:** {division_seleccionada}")
else:
    st.session_state.division_seleccionada = None
    division_seleccionada = None

# Usar división del session_state si está disponible
if not division_seleccionada and st.session_state.division_seleccionada:
    division_seleccionada = st.session_state.division_seleccionada

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
    tarifa_descripcion = {}  # HU-1.5: Para mapear código a descripción completa
    for _, row in df_tarifas_disp.iterrows():
        opcion = f"{row['tarifa']} - {row['descripcion']}"
        opciones_tarifa.append(opcion)
        tarifa_map[opcion] = row['tarifa']
        tarifa_descripcion[row['tarifa']] = row['descripcion']
    
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
        st.session_state.tarifas_seleccionadas = tarifas_seleccionadas
        
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
        st.session_state.tarifas_seleccionadas = []
else:
    # Sin división: selector deshabilitado y usar session_state si hay
    if st.session_state.tarifas_seleccionadas:
        tarifas_seleccionadas = st.session_state.tarifas_seleccionadas
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
    
    # Mantener selección previa si aplica
    if st.session_state.anio_seleccionado and st.session_state.anio_seleccionado in anios:
        index_anio = anios.index(st.session_state.anio_seleccionado)
    else:
        index_anio = len(anios) - 1  # Último año como default
    
    # Selector de año con el más reciente como default
    anio_seleccionado = st.selectbox(
        "Año de análisis",
        options=anios,
        index=index_anio,
        key="selector_anio",
        help="Selecciona el año que deseas analizar. Se comparará con el año anterior."
    )
    st.session_state.anio_seleccionado = anio_seleccionado
    
    # Calcular año comparativo
    anio_comparativo = anio_seleccionado - 1
    
    # Mostrar información de comparación
    st.success(f"📊 **Análisis:** {anio_seleccionado} vs {anio_comparativo}")
    
    # Resumen de selección completa
    st.markdown("---")
    st.subheader("✅ Resumen de Selección")
    
    col_res1, col_res2, col_res3 = st.columns(3)
    with col_res1:
        st.metric("División", division_seleccionada or "No seleccionada")
    with col_res2:
        st.metric("Tarifas", f"{len(tarifas_seleccionadas)} seleccionada(s)")
    with col_res3:
        st.metric("Periodo", f"{anio_seleccionado} vs {anio_comparativo}" if anio_seleccionado else "No seleccionado")
    
    # Sistema de navegación con tabs (HU-5.2)
    st.markdown("---")
    modo_tabs = st.tabs(["📊 Análisis de Comportamiento", "📋 Generar Histórico", "📥 Captura de Datos"])
    
    # Tab 1: Análisis de Comportamiento (Features 2 y 3 existentes)
    with modo_tabs[0]:
        if division_seleccionada and tarifas_seleccionadas and anio_seleccionado:
            # KPI de Variación Total Diciembre (HU-2.1)
            st.markdown("---")
            st.subheader("📊 Comparativo Diciembre vs Diciembre")
            st.caption(f"Variación del costo total entre diciembre {anio_comparativo} y diciembre {anio_seleccionado}")
            
            # Obtener años para la validación
            anios = get_anios_disponibles()
            
            # Advertencia si es el año más reciente (puede no tener diciembre)
            if anio_seleccionado == max(anios):
                st.warning(f"⚠️ {anio_seleccionado} es el año más reciente. Si no hay datos de diciembre, selecciona un año anterior.")
            
            # Pestañas por tarifa (HU-2.2 mejora de UX)
            tabs = st.tabs(tarifas_seleccionadas)
            
            for tab, tarifa in zip(tabs, tarifas_seleccionadas):
                with tab:
                    # Calcular variación
                    resultado = calcular_variacion_diciembre(
                        tarifa=tarifa,
                        region=division_seleccionada,
                        anio_actual=anio_seleccionado,
                        anio_anterior=anio_comparativo
                    )
                    
                    if resultado["disponible"]:
                        # === HU-1.5: Descripción completa de la tarifa seleccionada ===
                        descripcion_tarifa = tarifa_descripcion.get(tarifa, "")
                        if descripcion_tarifa:
                            st.info(f"**{tarifa}** — {descripcion_tarifa}")
                        
                        # === TABLA RESUMEN ===
                        st.markdown("##### 📋 Resumen de Tarifas")
                        
                        if resultado["es_horaria"]:
                            horarios_info = [
                                ("B", "Base"),
                                ("I", "Intermedia"),
                                ("P", "Punta"),
                                ("capacidad", "Capacidad"),
                            ]
                            
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
                        
                        # === GRÁFICA COMPARATIVA ===
                        st.markdown("##### 📊 Gráfica Comparativa")
                        
                        datos_kwh = []
                        datos_kw = []
                        
                        for key, datos_cargo in resultado["horarios"].items():
                            if datos_cargo.get("actual") is not None or datos_cargo.get("anterior") is not None:
                                if key == "B":
                                    concepto, es_capacidad = "Base", False
                                elif key == "I":
                                    concepto, es_capacidad = "Intermedia", False
                                elif key == "P":
                                    concepto, es_capacidad = "Punta", False
                                elif key == "capacidad":
                                    concepto, es_capacidad = "Capacidad", True
                                elif key == "simple":
                                    concepto, es_capacidad = "Variable", False
                                else:
                                    concepto, es_capacidad = key, False
                                
                                lista_destino = datos_kw if es_capacidad else datos_kwh
                                
                                if datos_cargo.get("anterior") is not None:
                                    lista_destino.append({
                                        "Concepto": concepto,
                                        "Año": str(anio_comparativo),
                                        "Valor": datos_cargo["anterior"]
                                    })
                                if datos_cargo.get("actual") is not None:
                                    lista_destino.append({
                                        "Concepto": concepto,
                                        "Año": str(anio_seleccionado),
                                        "Valor": datos_cargo["actual"]
                                    })
                        
                        colores = {
                            str(anio_comparativo): "#636EFA",
                            str(anio_seleccionado): "#EF553B"
                        }
                        
                        tiene_kwh = len(datos_kwh) > 0
                        tiene_kw = len(datos_kw) > 0
                        
                        if tiene_kwh and tiene_kw:
                            col_kwh, col_kw = st.columns([3, 1])
                        elif tiene_kwh:
                            col_kwh, col_kw = st.container(), None
                        elif tiene_kw:
                            col_kwh, col_kw = None, st.container()
                        else:
                            col_kwh, col_kw = None, None
                        
                        if tiene_kwh and col_kwh:
                            with col_kwh:
                                df_kwh = pd.DataFrame(datos_kwh)
                                fig_kwh = px.bar(df_kwh, x="Concepto", y="Valor", color="Año",
                                                barmode="group", title="Variable ($/kWh)",
                                                color_discrete_map=colores, text_auto=".2f")
                                fig_kwh.update_layout(yaxis_title="$/kWh", xaxis_title="",
                                                    legend_title="Año", height=300, margin=dict(t=40, b=40))
                                fig_kwh.update_traces(hovertemplate="<b>%{x}</b><br>$%{y:.4f}/kWh<extra></extra>")
                                st.plotly_chart(fig_kwh, use_container_width=True)
                        
                        if tiene_kw and col_kw:
                            with col_kw:
                                df_kw = pd.DataFrame(datos_kw)
                                fig_kw = px.bar(df_kw, x="Concepto", y="Valor", color="Año",
                                               barmode="group", title="Capacidad ($/kW)",
                                               color_discrete_map=colores, text_auto=".2f")
                                fig_kw.update_layout(yaxis_title="$/kW", xaxis_title="",
                                                   legend_title="Año", height=300, margin=dict(t=40, b=40),
                                                   showlegend=False)
                                fig_kw.update_traces(hovertemplate="<b>%{x}</b><br>$%{y:.2f}/kW<extra></extra>")
                                st.plotly_chart(fig_kw, use_container_width=True)
                        
                        # === DESGLOSE POR COMPONENTES ===
                        st.markdown("##### 🔍 Desglose por Componente")
                        
                        if resultado["es_horaria"]:
                            horarios_analizar = [("B", "Base"), ("I", "Intermedia"), ("P", "Punta")]
                            cols_desglose = st.columns(3)
                            for idx, (horario_key, horario_nombre) in enumerate(horarios_analizar):
                                with cols_desglose[idx]:
                                    componentes = calcular_variacion_componentes(
                                        tarifa=tarifa, region=division_seleccionada,
                                        anio_actual=anio_seleccionado, anio_anterior=anio_comparativo,
                                        horario=horario_key, tipo_cargo="Variable"
                                    )
                                    if componentes:
                                        datos_comp = [
                                            {"Componente": c["nombre"], "Variación": c["var_absoluta"],
                                             "Anterior": c["anterior"] or 0, "Actual": c["actual"] or 0,
                                             "Var %": c["var_pct"] or 0}
                                            for c in componentes if c["var_absoluta"] is not None
                                        ]
                                        if datos_comp:
                                            df_comp = pd.DataFrame(datos_comp)
                                            df_comp["Color"] = df_comp["Variación"].apply(
                                                lambda x: "Subió" if x > 0 else "Bajó"
                                            )
                                            fig_comp = px.bar(
                                                df_comp, y="Componente", x="Variación", color="Color",
                                                orientation="h", title=f"{horario_nombre}",
                                                color_discrete_map={"Subió": "#EF553B", "Bajó": "#00CC96"},
                                                text=df_comp["Var %"].apply(lambda x: f"{x:+.1f}%")
                                            )
                                            fig_comp.update_layout(
                                                xaxis_title="$/kWh", yaxis_title="",
                                                height=250, showlegend=False,
                                                margin=dict(l=10, r=10, t=30, b=30)
                                            )
                                            fig_comp.update_traces(
                                                hovertemplate="<b>%{y}</b><br>Var: $%{x:.4f}<extra></extra>"
                                            )
                                            st.plotly_chart(fig_comp, use_container_width=True)
                        else:
                            componentes = calcular_variacion_componentes(
                                tarifa=tarifa, region=division_seleccionada,
                                anio_actual=anio_seleccionado, anio_anterior=anio_comparativo,
                                horario=None, tipo_cargo="Variable"
                            )
                            if componentes:
                                datos_comp = [
                                    {"Componente": c["nombre"], "Variación": c["var_absoluta"],
                                     "Anterior": c["anterior"] or 0, "Actual": c["actual"] or 0,
                                     "Var %": c["var_pct"] or 0}
                                    for c in componentes if c["var_absoluta"] is not None
                                ]
                                if datos_comp:
                                    df_comp = pd.DataFrame(datos_comp)
                                    df_comp["Color"] = df_comp["Variación"].apply(
                                        lambda x: "Subió 🔴" if x > 0 else "Bajó 🟢"
                                    )
                                    fig_comp = px.bar(
                                        df_comp, y="Componente", x="Variación", color="Color",
                                        orientation="h", title="Variación por Componente",
                                        color_discrete_map={"Subió 🔴": "#EF553B", "Bajó 🟢": "#00CC96"},
                                        text=df_comp["Var %"].apply(lambda x: f"{x:+.1f}%")
                                    )
                                    fig_comp.update_layout(
                                        xaxis_title="Variación ($/kWh)", yaxis_title="",
                                        height=300, showlegend=True, legend_title="",
                                        margin=dict(l=10, r=10, t=40, b=40)
                                    )
                                    st.plotly_chart(fig_comp, use_container_width=True)
                        
                        # === KPI DE PROMEDIO ANUAL (HU-3.1) ===
                        st.markdown("##### 📊 Promedio Anual")
                        
                        if resultado["es_horaria"]:
                            prom_fijo = calcular_variacion_promedio_anual(
                                tarifa=tarifa, region=division_seleccionada,
                                anio_actual=anio_seleccionado, anio_anterior=anio_comparativo,
                                horario=None, tipo_cargo="Fijo"
                            )
                            cols_fijo_horarios = st.columns([1, 1, 1, 1])
                            with cols_fijo_horarios[0]:
                                if prom_fijo["disponible"]:
                                    st.metric(
                                        label="📋 Cargo Fijo",
                                        value=f"${prom_fijo['promedio_actual']:.2f}/mes",
                                        delta=f"{prom_fijo['variacion_pct']:+.1f}%",
                                        delta_color="inverse",
                                        help=f"Promedio de {prom_fijo['num_meses_comunes']} meses. Anterior: ${prom_fijo['promedio_anterior']:.2f}"
                                    )
                                else:
                                    st.metric(label="📋 Cargo Fijo", value="N/D", delta="Sin datos")
                            horarios_prom = [("B", "Base"), ("I", "Intermedia"), ("P", "Punta")]
                            for idx, (horario_key, horario_nombre) in enumerate(horarios_prom):
                                with cols_fijo_horarios[idx + 1]:
                                    prom_data = calcular_variacion_promedio_anual(
                                        tarifa=tarifa, region=division_seleccionada,
                                        anio_actual=anio_seleccionado, anio_anterior=anio_comparativo,
                                        horario=horario_key, tipo_cargo="Variable"
                                    )
                                    if prom_data["disponible"]:
                                        st.metric(
                                            label=f"⏰ {horario_nombre}",
                                            value=f"${prom_data['promedio_actual']:.4f}/kWh",
                                            delta=f"{prom_data['variacion_pct']:+.1f}%",
                                            delta_color="inverse",
                                            help=f"Promedio de {prom_data['num_meses_comunes']} meses. Anterior: ${prom_data['promedio_anterior']:.4f}"
                                        )
                                    else:
                                        st.metric(label=f"⏰ {horario_nombre}", value="N/D", delta="Sin datos")
                            st.caption("🕐 **Horarios típicos:** Base (0:00-6:00) | Intermedia (6:00-18:00, 22:00-0:00) | Punta (18:00-22:00)")
                        else:
                            cols_simple = st.columns(2)
                            with cols_simple[0]:
                                prom_fijo = calcular_variacion_promedio_anual(
                                    tarifa=tarifa, region=division_seleccionada,
                                    anio_actual=anio_seleccionado, anio_anterior=anio_comparativo,
                                    horario=None, tipo_cargo="Fijo"
                                )
                                if prom_fijo["disponible"]:
                                    st.metric(
                                        label="📋 Promedio Cargo Fijo",
                                        value=f"${prom_fijo['promedio_actual']:.2f}/mes",
                                        delta=f"{prom_fijo['variacion_pct']:+.1f}%",
                                        delta_color="inverse",
                                        help=f"Promedio de {prom_fijo['num_meses_comunes']} meses. Anterior: ${prom_fijo['promedio_anterior']:.2f}"
                                    )
                                else:
                                    st.metric(label="📋 Promedio Cargo Fijo", value="N/D", delta="Sin datos")
                            with cols_simple[1]:
                                prom_data = calcular_variacion_promedio_anual(
                                    tarifa=tarifa, region=division_seleccionada,
                                    anio_actual=anio_seleccionado, anio_anterior=anio_comparativo,
                                    horario=None, tipo_cargo="Variable"
                                )
                                if prom_data["disponible"]:
                                    st.metric(
                                        label="⚡ Promedio Variable (Energía)",
                                        value=f"${prom_data['promedio_actual']:.4f}/kWh",
                                        delta=f"{prom_data['variacion_pct']:+.1f}%",
                                        delta_color="inverse",
                                        help=f"Promedio de {prom_data['num_meses_comunes']} meses. Anterior: ${prom_data['promedio_anterior']:.4f}"
                                    )
                                else:
                                    st.metric(label="⚡ Promedio Variable", value="N/D", delta="Sin datos")
                        
                        # === GRÁFICA DE TENDENCIA MENSUAL (HU-3.4) ===
                        st.markdown("##### 📈 Tendencia Mensual")
                        
                        if resultado["es_horaria"]:
                            horarios_tendencia = [("B", "Base"), ("I", "Intermedia"), ("P", "Punta")]
                            cols_tendencia = st.columns(3)
                            for idx, (horario_key, horario_nombre) in enumerate(horarios_tendencia):
                                with cols_tendencia[idx]:
                                    datos_tend = get_datos_tendencia_comparativa(
                                        tarifa=tarifa, region=division_seleccionada,
                                        anio_actual=anio_seleccionado, anio_anterior=anio_comparativo,
                                        horario=horario_key, tipo_cargo="Variable"
                                    )
                                    if datos_tend:
                                        df_tend = pd.DataFrame(datos_tend)
                                        df_tend = df_tend.sort_values("Mes_Num")
                                        fig_tend = px.line(
                                            df_tend, x="Mes", y="Valor", color="Año",
                                            title=f"{horario_nombre}",
                                            markers=True,
                                            color_discrete_map={
                                                str(anio_comparativo): "#636EFA",
                                                str(anio_seleccionado): "#EF553B"
                                            }
                                        )
                                        fig_tend.update_layout(
                                            xaxis_title="", yaxis_title="$/kWh",
                                            height=280, showlegend=True,
                                            legend=dict(orientation="h", yanchor="bottom", y=1.02),
                                            margin=dict(l=10, r=10, t=50, b=30)
                                        )
                                        fig_tend.update_traces(
                                            hovertemplate="<b>%{x}</b><br>$%{y:.4f}/kWh<extra></extra>"
                                        )
                                        st.plotly_chart(fig_tend, use_container_width=True)
                                    else:
                                        st.info(f"Sin datos para {horario_nombre}")
                        else:
                            datos_tend = get_datos_tendencia_comparativa(
                                tarifa=tarifa, region=division_seleccionada,
                                anio_actual=anio_seleccionado, anio_anterior=anio_comparativo,
                                horario=None, tipo_cargo="Variable"
                            )
                            if datos_tend:
                                df_tend = pd.DataFrame(datos_tend)
                                df_tend = df_tend.sort_values("Mes_Num")
                                fig_tend = px.line(
                                    df_tend, x="Mes", y="Valor", color="Año",
                                    title="Evolución Mensual Variable (Energía)",
                                    markers=True,
                                    color_discrete_map={
                                        str(anio_comparativo): "#636EFA",
                                        str(anio_seleccionado): "#EF553B"
                                    }
                                )
                                fig_tend.update_layout(
                                    xaxis_title="Mes", yaxis_title="$/kWh",
                                    height=350, showlegend=True,
                                    legend=dict(orientation="h", yanchor="bottom", y=1.02),
                                    margin=dict(l=10, r=10, t=50, b=40)
                                )
                                fig_tend.update_traces(
                                    hovertemplate="<b>%{x}</b><br>$%{y:.4f}/kWh<extra></extra>"
                                )
                                st.plotly_chart(fig_tend, use_container_width=True)
                            else:
                                st.info("Sin datos de tendencia mensual")
                    else:
                        st.warning(f"No hay datos de diciembre para {tarifa} en {anio_seleccionado} o {anio_comparativo}")
        else:
            st.info("👆 Selecciona Estado, Municipio, Tarifa y Año para ver el análisis de comportamiento")
    
    # Tab 2: Generar Histórico (HU-5.1)
    with modo_tabs[1]:
        if division_seleccionada and tarifas_seleccionadas and anio_seleccionado:
            # Una tarifa para el histórico (selector si hay varias)
            if len(tarifas_seleccionadas) == 1:
                tarifa_historico = tarifas_seleccionadas[0]
            else:
                tarifa_historico = st.selectbox(
                    "Tarifa para histórico",
                    options=tarifas_seleccionadas,
                    key="tarifa_historico",
                    help="Elige la tarifa para generar la tabla de 12 meses"
                )
            
            st.subheader("📋 Rango de 12 meses")
            mes_final_nombre = st.selectbox(
                "Mes final del rango",
                options=MESES_NOMBRES,
                index=11,
                key="mes_final_historico",
                help="Se calcularán 12 meses hacia atrás desde este mes y año"
            )
            mes_final_num = mes_a_numero(mes_final_nombre)
            
            # Calcular rango con casos borde
            rango = calcular_rango_12_meses(
                mes_final_num, anio_seleccionado, df_tarifas,
                tarifa_historico, division_seleccionada
            )
            mes_inicial, anio_inicial, mes_final_ajustado, anio_final_ajustado, mensaje_info = rango
            
            if mensaje_info:
                st.info(mensaje_info)
            
            # Filtrar datos en el rango
            start_ord = anio_inicial * 12 + mes_inicial
            end_ord = anio_final_ajustado * 12 + mes_final_ajustado
            fecha_ord = df_tarifas["anio"] * 12 + df_tarifas["mes_numero"]
            mask_hist = (
                (df_tarifas["region"] == division_seleccionada.upper().strip()) &
                (df_tarifas["tarifa"] == tarifa_historico) &
                (fecha_ord >= start_ord) &
                (fecha_ord <= end_ord)
            )
            df_hist = df_tarifas.loc[mask_hist].copy()
            df_hist = df_hist.sort_values(by=["anio", "mes_numero", "cargo", "int_horario"], ignore_index=True)

            # Vista pivotada: una fila por mes (Año, Mes, Fecha, Cargo Fijo, Base, Intermedia, Punta, Cargo Cap)
            df_vista = pivotar_historico_por_mes(df_hist)

            def fmt_miles(v):
                if v is None or (isinstance(v, float) and pd.isna(v)):
                    return ""
                return f"{float(v):,.2f}"

            def fmt_cuatro(v):
                if v is None or (isinstance(v, float) and pd.isna(v)):
                    return ""
                return f"{float(v):.4f}"

            df_display = df_vista.copy()
            for col in ["Cargo Fijo", "Cargo Cap"]:
                if col in df_display.columns:
                    df_display[col] = df_display[col].apply(fmt_miles)
            for col in ["Base", "Intermedia", "Punta"]:
                if col in df_display.columns:
                    df_display[col] = df_display[col].apply(fmt_cuatro)

            st.caption(f"**Total:** {len(df_display)} meses. Rango: {numero_a_mes(mes_inicial)} {anio_inicial} — {numero_a_mes(mes_final_ajustado)} {anio_final_ajustado}")

            if df_display.empty:
                st.warning("No hay datos en el rango calculado para esta tarifa y división.")
            else:
                st.dataframe(
                    df_display,
                    use_container_width=True,
                    column_config={
                        "Año": st.column_config.NumberColumn("Año", format="%d", width="small"),
                        "Mes": st.column_config.TextColumn("Mes", width="medium"),
                        "Fecha": st.column_config.TextColumn("Fecha", width="small"),
                        "Cargo Fijo": st.column_config.TextColumn("Cargo Fijo", width="medium"),
                        "Base": st.column_config.TextColumn("Base", width="medium"),
                        "Intermedia": st.column_config.TextColumn("Intermedia", width="medium"),
                        "Punta": st.column_config.TextColumn("Punta", width="medium"),
                        "Cargo Cap": st.column_config.TextColumn("Cargo Cap", width="medium"),
                    },
                )

                # Exportar CSV: mismo contenido mostrado (vista pivotada formateada)
                nombre_archivo = f"historico_{tarifa_historico}_{division_seleccionada.replace(' ', '_')}_{numero_a_mes(mes_inicial)}{anio_inicial}_{numero_a_mes(mes_final_ajustado)}{anio_final_ajustado}.csv"
                csv_bytes = df_display.to_csv(index=False, encoding="utf-8")
                st.download_button(
                    "Descargar CSV",
                    data=csv_bytes,
                    file_name=nombre_archivo,
                    mime="text/csv",
                    key="download_historico_csv"
                )
        else:
            st.info("👆 Selecciona Estado, Municipio, Tarifa y Año para generar el histórico")
    
    # Tab 3: Captura de Datos de Recibo (Feature 6 - placeholder)
    with modo_tabs[2]:
        st.info("🚧 Esta funcionalidad se implementará en el Feature 6: Captura de Datos de Recibo")
        st.markdown("""
        **Próximamente:** Podrás capturar y analizar datos de recibos de CFE.
        """)
else:
    # Selector deshabilitado si no hay tarifas
    st.selectbox(
        "Año de análisis",
        options=["Selecciona primero las tarifas"],
        disabled=True,
        key="selector_anio_disabled"
    )
    
    # Mostrar tabs incluso si no hay selección completa
    st.markdown("---")
    modo_tabs = st.tabs(["📊 Análisis de Comportamiento", "📋 Generar Histórico", "📥 Captura de Datos"])
    
    with modo_tabs[0]:
        st.info("👆 Completa los selectores arriba para ver el análisis de comportamiento")
    
    with modo_tabs[1]:
        st.info("👆 Completa los selectores arriba para generar el histórico")
    
    with modo_tabs[2]:
        st.info("🚧 Esta funcionalidad se implementará en el Feature 6: Captura de Datos de Recibo")

# Footer
st.markdown("---")
st.caption("CFE Analizador de Tarifas v1.6.3 | Desarrollado con Streamlit")
