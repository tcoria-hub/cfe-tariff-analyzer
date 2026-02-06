"""
CFE Tariff Analyzer - Data Loader Module
=========================================
Funciones para carga y gestión de datos desde archivos CSV.
Todas las funciones usan cache de Streamlit para optimizar rendimiento.
"""

from typing import Optional, List
import unicodedata
import pandas as pd
import streamlit as st
from pathlib import Path


def normalizar_texto(texto: str) -> str:
    """
    Normaliza texto: UPPER CASE, sin acentos, sin espacios extras.
    
    Args:
        texto: Texto a normalizar
        
    Returns:
        Texto normalizado
    """
    if pd.isna(texto):
        return ""
    # Convertir a string y UPPER CASE
    texto = str(texto).upper().strip()
    # Eliminar acentos (NFD descompone, luego filtramos marcas diacríticas)
    texto = unicodedata.normalize('NFD', texto)
    texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
    return texto

# Rutas a los archivos de datos
DATA_DIR = Path(__file__).parent.parent / "data"
GEOGRAFIA_FILE = DATA_DIR / "01_catalogo_regiones.csv"
TARIFAS_FILE = DATA_DIR / "02_tarifas_finales_suministro_basico.csv"


@st.cache_data
def load_geografia() -> pd.DataFrame:
    """
    Carga el catálogo de geografía (Estados, Municipios, Divisiones).
    
    Returns:
        DataFrame con columnas: estado, municipio, division (todas en UPPER CASE)
    """
    df = pd.read_csv(GEOGRAFIA_FILE)
    
    # El CSV tiene columnas extra vacías, tomamos solo las primeras 3
    df = df.iloc[:, :3]
    df.columns = ["estado", "municipio", "division"]
    
    # Normalizar: UPPER CASE, sin acentos, sin espacios extras
    df["estado"] = df["estado"].apply(normalizar_texto)
    df["municipio"] = df["municipio"].apply(normalizar_texto)
    df["division"] = df["division"].apply(normalizar_texto)
    
    # Eliminar filas con valores nulos
    df = df.dropna()
    
    return df


@st.cache_data
def load_tarifas() -> pd.DataFrame:
    """
    Carga el histórico de tarifas de CFE.
    
    Returns:
        DataFrame con todas las columnas del CSV, región normalizada a UPPER CASE
    """
    df = pd.read_csv(TARIFAS_FILE)
    
    # Normalizar región: UPPER CASE, sin acentos para match con geografía
    df["region"] = df["region"].apply(normalizar_texto)
    
    # Convertir columnas numéricas (manejar valores vacíos)
    numeric_cols = [
        "transmision", "distribucion", "cenace", "suministro", 
        "scnmem", "generacion", "capacidad", "total"
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    
    return df


@st.cache_data
def get_estados() -> List[str]:
    """
    Obtiene la lista de estados únicos ordenados alfabéticamente.
    
    Returns:
        Lista de nombres de estados en UPPER CASE
    """
    df = load_geografia()
    estados = sorted(df["estado"].unique().tolist())
    return estados


@st.cache_data
def get_municipios(estado: str) -> List[str]:
    """
    Obtiene la lista de municipios para un estado específico.
    
    Args:
        estado: Nombre del estado (se normaliza automáticamente)
        
    Returns:
        Lista de nombres de municipios ordenados alfabéticamente
    """
    df = load_geografia()
    estado_norm = normalizar_texto(estado)
    municipios = df[df["estado"] == estado_norm]["municipio"].unique().tolist()
    return sorted(municipios)


@st.cache_data
def get_division(estado: str, municipio: str) -> Optional[str]:
    """
    Obtiene la división de CFE correspondiente a un estado y municipio.
    Si hay múltiples divisiones, retorna la primera.
    
    Args:
        estado: Nombre del estado (se normaliza automáticamente)
        municipio: Nombre del municipio (se normaliza automáticamente)
        
    Returns:
        Nombre de la división o None si no se encuentra
    """
    divisiones = get_divisiones(estado, municipio)
    if divisiones:
        return divisiones[0]
    return None


@st.cache_data
def get_divisiones(estado: str, municipio: str) -> List[str]:
    """
    Obtiene TODAS las divisiones de CFE para un estado y municipio.
    Algunos municipios pertenecen a múltiples divisiones.
    
    Args:
        estado: Nombre del estado (se normaliza automáticamente)
        municipio: Nombre del municipio (se normaliza automáticamente)
        
    Returns:
        Lista de divisiones ordenadas alfabéticamente (puede tener 1 o más)
    """
    df = load_geografia()
    estado_norm = normalizar_texto(estado)
    municipio_norm = normalizar_texto(municipio)
    divisiones = df[
        (df["estado"] == estado_norm) & 
        (df["municipio"] == municipio_norm)
    ]["division"].unique().tolist()
    
    return sorted(divisiones)


# Tarifas que tienen estructura horaria (Base, Intermedia, Punta)
TARIFAS_HORARIAS = {"GDMTH", "DIST", "DIT"}


@st.cache_data
def get_tarifas_disponibles() -> pd.DataFrame:
    """
    Obtiene la lista de tarifas disponibles con su descripción.
    
    Returns:
        DataFrame con columnas: tarifa, descripcion (valores únicos)
    """
    df = load_tarifas()
    tarifas = df[["tarifa", "descripcion"]].drop_duplicates()
    tarifas = tarifas.sort_values("tarifa")
    return tarifas


def es_tarifa_horaria(tarifa: str) -> bool:
    """
    Determina si una tarifa tiene estructura horaria (Base, Intermedia, Punta).
    
    Args:
        tarifa: Código de la tarifa (ej: "GDMTH")
        
    Returns:
        True si es tarifa horaria, False si es tarifa simple
    """
    return tarifa.upper() in TARIFAS_HORARIAS


@st.cache_data
def get_anios_disponibles() -> List[int]:
    """
    Obtiene la lista de años disponibles en los datos.
    Excluye el primer año (2017) porque no tiene año anterior para comparar.
    
    Returns:
        Lista de años disponibles para análisis (desde 2018)
    """
    df = load_tarifas()
    anios = sorted(df["anio"].unique().tolist())
    # Excluir el primer año (no tiene año anterior para comparar)
    if len(anios) > 1:
        anios = anios[1:]  # Desde el segundo año en adelante
    return anios


@st.cache_data
def get_regiones_disponibles() -> List[str]:
    """
    Obtiene la lista de regiones/divisiones únicas en los datos de tarifas.
    
    Returns:
        Lista de regiones ordenadas alfabéticamente
    """
    df = load_tarifas()
    regiones = sorted(df["region"].unique().tolist())
    return regiones


def get_data_stats() -> dict:
    """
    Obtiene estadísticas de los datos cargados.
    
    Returns:
        Diccionario con estadísticas de carga
    """
    df_geo = load_geografia()
    df_tar = load_tarifas()
    
    return {
        "geografia": {
            "total_registros": len(df_geo),
            "estados": df_geo["estado"].nunique(),
            "municipios": df_geo["municipio"].nunique(),
            "divisiones": df_geo["division"].nunique(),
        },
        "tarifas": {
            "total_registros": len(df_tar),
            "anio_min": df_tar["anio"].min(),
            "anio_max": df_tar["anio"].max(),
            "tarifas_tipos": df_tar["tarifa"].nunique(),
            "regiones": df_tar["region"].nunique(),
        }
    }


def verificar_match_regiones() -> dict:
    """
    Verifica que las divisiones de geografía coincidan con las regiones de tarifas.
    
    Returns:
        Diccionario con resultados de la verificación
    """
    df_geo = load_geografia()
    df_tar = load_tarifas()
    
    divisiones_geo = set(df_geo["division"].unique())
    regiones_tar = set(df_tar["region"].unique())
    
    # Encontrar coincidencias y diferencias
    coinciden = divisiones_geo & regiones_tar
    solo_en_geo = divisiones_geo - regiones_tar
    solo_en_tar = regiones_tar - divisiones_geo
    
    return {
        "coinciden": len(coinciden),
        "total_divisiones_geo": len(divisiones_geo),
        "total_regiones_tar": len(regiones_tar),
        "solo_en_geografia": list(solo_en_geo),
        "solo_en_tarifas": list(solo_en_tar),
        "match_exitoso": len(solo_en_geo) == 0 and len(solo_en_tar) == 0
    }


def get_cargo_variable_diciembre(tarifa: str, region: str, anio: int, horario: Optional[str] = None) -> Optional[float]:
    """
    Obtiene el cargo Variable (Energía) de diciembre para una tarifa, región, año y horario.
    
    Args:
        tarifa: Código de tarifa (ej: "GDMTH")
        region: Nombre de la región/división (ej: "BAJIO")
        anio: Año a consultar
        horario: "B" (Base), "I" (Intermedia), "P" (Punta), o None para tarifas simples
        
    Returns:
        Valor del cargo Variable en pesos/kWh o None si no hay datos
    """
    df = load_tarifas()
    
    # Normalizar región
    region_norm = normalizar_texto(region)
    
    # Filtrar por tarifa, región, año, mes diciembre y cargo Variable
    filtro = (
        (df["tarifa"] == tarifa) &
        (df["region"] == region_norm) &
        (df["anio"] == anio) &
        (df["mes"] == "diciembre") &
        (df["cargo"].str.contains("Variable", case=False, na=False))
    )
    
    # Agregar filtro de horario si aplica
    if horario:
        filtro = filtro & (df["int_horario"] == horario)
    else:
        # Para tarifas simples, buscar "sin dato" en int_horario
        filtro = filtro & (df["int_horario"] == "sin dato")
    
    df_filtrado = df[filtro]
    
    if df_filtrado.empty:
        return None
    
    # Tomar el valor total del cargo Variable
    total = df_filtrado["total"].iloc[0]
    
    return total if not pd.isna(total) else None


def get_cargo_capacidad_diciembre(tarifa: str, region: str, anio: int) -> Optional[float]:
    """
    Obtiene el cargo de Capacidad de diciembre para una tarifa, región y año.
    
    Args:
        tarifa: Código de tarifa (ej: "DIST")
        region: Nombre de la región/división
        anio: Año a consultar
        
    Returns:
        Valor del cargo Capacidad en pesos/kW o None si no hay datos
    """
    df = load_tarifas()
    
    # Normalizar región
    region_norm = normalizar_texto(region)
    
    # Filtrar por tarifa, región, año, mes diciembre y cargo Capacidad
    filtro = (
        (df["tarifa"] == tarifa) &
        (df["region"] == region_norm) &
        (df["anio"] == anio) &
        (df["mes"] == "diciembre") &
        (df["cargo"].str.contains("Capacidad", case=False, na=False))
    )
    
    df_filtrado = df[filtro]
    
    if df_filtrado.empty:
        return None
    
    total = df_filtrado["total"].iloc[0]
    
    return total if not pd.isna(total) else None


def get_cargos_diciembre_por_horario(tarifa: str, region: str, anio: int) -> dict:
    """
    Obtiene todos los cargos Variable de diciembre para una tarifa horaria.
    
    Args:
        tarifa: Código de tarifa
        region: Nombre de la región
        anio: Año a consultar
        
    Returns:
        Diccionario con cargos por horario: {"B": valor, "I": valor, "P": valor, "capacidad": valor}
        o {"simple": valor, "capacidad": valor} para tarifas sin horario
    """
    capacidad = get_cargo_capacidad_diciembre(tarifa, region, anio)
    
    if es_tarifa_horaria(tarifa):
        return {
            "B": get_cargo_variable_diciembre(tarifa, region, anio, "B"),
            "I": get_cargo_variable_diciembre(tarifa, region, anio, "I"),
            "P": get_cargo_variable_diciembre(tarifa, region, anio, "P"),
            "capacidad": capacidad,
        }
    else:
        return {
            "simple": get_cargo_variable_diciembre(tarifa, region, anio, None),
            "capacidad": capacidad,
        }


def calcular_variacion_diciembre(tarifa: str, region: str, anio_actual: int, anio_anterior: int) -> dict:
    """
    Calcula la variación porcentual del cargo Variable entre dos diciembres.
    
    Para tarifas horarias, retorna variación por cada horario (B, I, P).
    Para tarifas simples, retorna variación del cargo único.
    
    Args:
        tarifa: Código de tarifa
        region: Nombre de la región/división
        anio_actual: Año de análisis
        anio_anterior: Año de comparación
        
    Returns:
        Diccionario con datos por horario y variaciones
    """
    cargos_actual = get_cargos_diciembre_por_horario(tarifa, region, anio_actual)
    cargos_anterior = get_cargos_diciembre_por_horario(tarifa, region, anio_anterior)
    
    resultado = {
        "tarifa": tarifa,
        "anio_actual": anio_actual,
        "anio_anterior": anio_anterior,
        "es_horaria": es_tarifa_horaria(tarifa),
        "horarios": {},
        "disponible": False
    }
    
    # Calcular variación para cada horario/cargo
    for key in cargos_actual.keys():
        actual = cargos_actual.get(key)
        anterior = cargos_anterior.get(key)
        
        variacion = None
        if actual is not None and anterior is not None and anterior != 0:
            variacion = ((actual / anterior) - 1) * 100
            resultado["disponible"] = True
        
        resultado["horarios"][key] = {
            "actual": actual,
            "anterior": anterior,
            "variacion_pct": variacion
        }
    
    return resultado


# Columnas de componentes disponibles en el CSV
COMPONENTES = ["transmision", "distribucion", "cenace", "suministro", "scnmem", "generacion", "capacidad"]

# Nombres legibles para cada componente
COMPONENTES_NOMBRES = {
    "transmision": "Transmisión",
    "distribucion": "Distribución",
    "cenace": "CENACE",
    "suministro": "Suministro",
    "scnmem": "SCnMEM",
    "generacion": "Generación",
    "capacidad": "Capacidad"
}


def get_componentes_diciembre(
    tarifa: str, 
    region: str, 
    anio: int, 
    horario: Optional[str] = None,
    tipo_cargo: str = "Variable"
) -> dict:
    """
    Obtiene el desglose de componentes de un cargo de diciembre.
    
    Args:
        tarifa: Código de tarifa
        region: Nombre de la región/división
        anio: Año a consultar
        horario: "B", "I", "P" para tarifas horarias, None para simples
        tipo_cargo: "Variable" o "Capacidad"
        
    Returns:
        Diccionario con valores de cada componente
    """
    df = load_tarifas()
    
    # Normalizar región
    region_norm = normalizar_texto(region)
    
    # Filtrar por tarifa, región, año, mes diciembre y tipo de cargo
    filtro = (
        (df["tarifa"] == tarifa) &
        (df["region"] == region_norm) &
        (df["anio"] == anio) &
        (df["mes"] == "diciembre") &
        (df["cargo"].str.contains(tipo_cargo, case=False, na=False))
    )
    
    # Agregar filtro de horario si aplica
    if horario:
        filtro = filtro & (df["int_horario"] == horario)
    else:
        filtro = filtro & (df["int_horario"] == "sin dato")
    
    df_filtrado = df[filtro]
    
    if df_filtrado.empty:
        return {}
    
    # Extraer valores de cada componente
    row = df_filtrado.iloc[0]
    resultado = {}
    
    for comp in COMPONENTES:
        valor = row.get(comp)
        if pd.notna(valor) and valor != 0:
            resultado[comp] = float(valor)
    
    return resultado


def calcular_variacion_componentes(
    tarifa: str,
    region: str,
    anio_actual: int,
    anio_anterior: int,
    horario: Optional[str] = None,
    tipo_cargo: str = "Variable"
) -> List[dict]:
    """
    Calcula la variación de cada componente entre dos diciembres.
    
    Args:
        tarifa: Código de tarifa
        region: Nombre de la región/división
        anio_actual: Año de análisis
        anio_anterior: Año de comparación
        horario: "B", "I", "P" para tarifas horarias, None para simples
        tipo_cargo: "Variable" o "Capacidad"
        
    Returns:
        Lista de diccionarios ordenados por impacto (abs(variación)) descendente
    """
    comp_actual = get_componentes_diciembre(tarifa, region, anio_actual, horario, tipo_cargo)
    comp_anterior = get_componentes_diciembre(tarifa, region, anio_anterior, horario, tipo_cargo)
    
    # Obtener todos los componentes presentes en ambos años
    todos_componentes = set(comp_actual.keys()) | set(comp_anterior.keys())
    
    resultados = []
    
    for comp in todos_componentes:
        actual = comp_actual.get(comp)
        anterior = comp_anterior.get(comp)
        
        # Calcular variación absoluta y porcentual
        var_absoluta = None
        var_pct = None
        
        if actual is not None and anterior is not None:
            var_absoluta = actual - anterior
            if anterior != 0:
                var_pct = ((actual / anterior) - 1) * 100
        elif actual is not None and anterior is None:
            var_absoluta = actual
            var_pct = 100.0  # 100% nuevo
        elif anterior is not None and actual is None:
            var_absoluta = -anterior
            var_pct = -100.0  # -100% eliminado
        
        resultados.append({
            "componente": comp,
            "nombre": COMPONENTES_NOMBRES.get(comp, comp),
            "anterior": anterior,
            "actual": actual,
            "var_absoluta": var_absoluta,
            "var_pct": var_pct
        })
    
    # Ordenar por impacto (abs(variación absoluta)) descendente
    resultados.sort(key=lambda x: abs(x["var_absoluta"]) if x["var_absoluta"] is not None else 0, reverse=True)
    
    return resultados


# Orden cronológico de meses
MESES_ORDEN = [
    'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
    'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'
]

# Abreviaciones para gráficas
MESES_ABREV = {
    'enero': 'Ene', 'febrero': 'Feb', 'marzo': 'Mar', 'abril': 'Abr',
    'mayo': 'May', 'junio': 'Jun', 'julio': 'Jul', 'agosto': 'Ago',
    'septiembre': 'Sep', 'octubre': 'Oct', 'noviembre': 'Nov', 'diciembre': 'Dic'
}


def get_tendencia_mensual(
    tarifa: str,
    region: str,
    anio: int,
    horario: Optional[str] = None,
    tipo_cargo: str = "Variable"
) -> List[dict]:
    """
    Obtiene los valores mensuales de un cargo para todo el año.
    
    Args:
        tarifa: Código de tarifa
        region: Nombre de la región/división
        anio: Año a consultar
        horario: "B", "I", "P" para tarifas horarias, None para simples
        tipo_cargo: "Variable" o "Capacidad"
        
    Returns:
        Lista de diccionarios con mes y valor, ordenados cronológicamente
    """
    df = load_tarifas()
    
    # Normalizar región
    region_norm = normalizar_texto(region)
    
    # Filtrar por tarifa, región, año y tipo de cargo
    filtro = (
        (df["tarifa"] == tarifa) &
        (df["region"] == region_norm) &
        (df["anio"] == anio) &
        (df["cargo"].str.contains(tipo_cargo, case=False, na=False))
    )
    
    # Agregar filtro de horario si aplica
    if horario:
        filtro = filtro & (df["int_horario"] == horario)
    else:
        filtro = filtro & (df["int_horario"] == "sin dato")
    
    df_filtrado = df[filtro]
    
    # Crear diccionario de mes -> valor
    datos_mes = {}
    for _, row in df_filtrado.iterrows():
        mes = row["mes"].lower()
        valor = row["total"]
        if pd.notna(valor):
            datos_mes[mes] = float(valor)
    
    # Construir lista ordenada por mes
    resultados = []
    for mes in MESES_ORDEN:
        valor = datos_mes.get(mes)
        resultados.append({
            "mes": mes,
            "mes_abrev": MESES_ABREV.get(mes, mes[:3].title()),
            "mes_num": MESES_ORDEN.index(mes) + 1,
            "valor": valor
        })
    
    return resultados


def get_datos_tendencia_comparativa(
    tarifa: str,
    region: str,
    anio_actual: int,
    anio_anterior: int,
    horario: Optional[str] = None,
    tipo_cargo: str = "Variable"
) -> List[dict]:
    """
    Obtiene datos para gráfica de tendencia comparando dos años.
    
    Args:
        tarifa: Código de tarifa
        region: Nombre de la región/división
        anio_actual: Año de análisis
        anio_anterior: Año de comparación
        horario: "B", "I", "P" para tarifas horarias, None para simples
        tipo_cargo: "Variable" o "Capacidad"
        
    Returns:
        Lista de diccionarios listos para Plotly (mes, año, valor)
    """
    tendencia_actual = get_tendencia_mensual(tarifa, region, anio_actual, horario, tipo_cargo)
    tendencia_anterior = get_tendencia_mensual(tarifa, region, anio_anterior, horario, tipo_cargo)
    
    datos = []
    
    # Agregar datos del año anterior
    for item in tendencia_anterior:
        if item["valor"] is not None:
            datos.append({
                "Mes": item["mes_abrev"],
                "Mes_Num": item["mes_num"],
                "Año": str(anio_anterior),
                "Valor": item["valor"]
            })
    
    # Agregar datos del año actual
    for item in tendencia_actual:
        if item["valor"] is not None:
            datos.append({
                "Mes": item["mes_abrev"],
                "Mes_Num": item["mes_num"],
                "Año": str(anio_actual),
                "Valor": item["valor"]
            })
    
    return datos


def calcular_promedio_anual(
    tarifa: str,
    region: str,
    anio: int,
    horario: Optional[str] = None,
    tipo_cargo: str = "Variable"
) -> dict:
    """
    Calcula el promedio anual de un cargo.
    
    Args:
        tarifa: Código de tarifa
        region: Nombre de la región/división
        anio: Año a consultar
        horario: "B", "I", "P" para tarifas horarias, None para simples
        tipo_cargo: "Variable" o "Capacidad"
        
    Returns:
        Diccionario con promedio, meses disponibles y lista de meses
    """
    tendencia = get_tendencia_mensual(tarifa, region, anio, horario, tipo_cargo)
    
    # Filtrar solo meses con valores
    valores = [item["valor"] for item in tendencia if item["valor"] is not None]
    meses_disponibles = [item["mes"] for item in tendencia if item["valor"] is not None]
    
    if not valores:
        return {
            "promedio": None,
            "num_meses": 0,
            "meses": []
        }
    
    return {
        "promedio": sum(valores) / len(valores),
        "num_meses": len(valores),
        "meses": meses_disponibles
    }


def calcular_variacion_promedio_anual(
    tarifa: str,
    region: str,
    anio_actual: int,
    anio_anterior: int,
    horario: Optional[str] = None,
    tipo_cargo: str = "Variable"
) -> dict:
    """
    Calcula la variación del promedio anual entre dos años.
    Compara solo los meses que existen en ambos años para una comparación justa.
    
    Args:
        tarifa: Código de tarifa
        region: Nombre de la región/división
        anio_actual: Año de análisis
        anio_anterior: Año de comparación
        horario: "B", "I", "P" para tarifas horarias, None para simples
        tipo_cargo: "Variable" o "Capacidad"
        
    Returns:
        Diccionario con promedios, variación y meses comparados
    """
    # Obtener tendencias de ambos años
    tendencia_actual = get_tendencia_mensual(tarifa, region, anio_actual, horario, tipo_cargo)
    tendencia_anterior = get_tendencia_mensual(tarifa, region, anio_anterior, horario, tipo_cargo)
    
    # Crear diccionarios de mes -> valor
    valores_actual = {item["mes"]: item["valor"] for item in tendencia_actual if item["valor"] is not None}
    valores_anterior = {item["mes"]: item["valor"] for item in tendencia_anterior if item["valor"] is not None}
    
    # Encontrar meses comunes (para comparación justa)
    meses_comunes = set(valores_actual.keys()) & set(valores_anterior.keys())
    
    if not meses_comunes:
        return {
            "promedio_actual": None,
            "promedio_anterior": None,
            "variacion_pct": None,
            "num_meses_actual": len(valores_actual),
            "num_meses_anterior": len(valores_anterior),
            "num_meses_comunes": 0,
            "disponible": False
        }
    
    # Calcular promedios solo de meses comunes
    promedio_actual = sum(valores_actual[m] for m in meses_comunes) / len(meses_comunes)
    promedio_anterior = sum(valores_anterior[m] for m in meses_comunes) / len(meses_comunes)
    
    # Calcular variación
    variacion_pct = None
    if promedio_anterior != 0:
        variacion_pct = ((promedio_actual / promedio_anterior) - 1) * 100
    
    return {
        "promedio_actual": promedio_actual,
        "promedio_anterior": promedio_anterior,
        "variacion_pct": variacion_pct,
        "num_meses_actual": len(valores_actual),
        "num_meses_anterior": len(valores_anterior),
        "num_meses_comunes": len(meses_comunes),
        "disponible": True
    }
