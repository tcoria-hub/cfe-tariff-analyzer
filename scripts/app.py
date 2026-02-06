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
                    # Usar columnas para mostrar los 3 horarios lado a lado
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
                    # Tarifa simple: una sola gráfica de desglose
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
            else:
                st.warning(f"No hay datos de diciembre para {tarifa} en {anio_seleccionado} o {anio_comparativo}")
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
st.caption("CFE Tariff Analyzer v1.3.0 | Desarrollado con Streamlit")
