"""
CFE Tariff Analyzer - Data Loader Module
=========================================
Funciones para carga y gestión de datos desde archivos CSV.
Todas las funciones usan cache de Streamlit para optimizar rendimiento.
"""

from typing import Optional, List, Tuple
import unicodedata
import pandas as pd
import streamlit as st
from pathlib import Path

# Orden de meses en español (minúsculas) para conversión 1-12
MESES_NOMBRES = [
    "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
]
# Abreviaturas de mes por número (1-12) para columna Fecha (ene-24, feb-23, etc.). No confundir con MESES_ABREV (dict) más abajo.
MESES_ABREV_POR_NUM = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]


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

def mes_a_numero(mes_nombre: str) -> int:
    """
    Convierte nombre de mes en español a número 1-12.
    
    Args:
        mes_nombre: Nombre del mes (ej: 'enero', 'diciembre')
        
    Returns:
        1-12 para meses válidos, 0 si no se reconoce
    """
    if not mes_nombre or pd.isna(mes_nombre):
        return 0
    m = str(mes_nombre).strip().lower()
    if m in MESES_NOMBRES:
        return MESES_NOMBRES.index(m) + 1
    return 0


def numero_a_mes(numero: int) -> str:
    """
    Convierte número 1-12 a nombre de mes en español.
    
    Args:
        numero: Número de mes (1-12)
        
    Returns:
        Nombre del mes (ej: 'enero') o cadena vacía si inválido
    """
    if 1 <= numero <= 12:
        return MESES_NOMBRES[numero - 1]
    return ""


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
    
    # Añadir mes_numero (1-12) para ordenamiento y filtrado
    df["mes"] = df["mes"].astype(str).str.strip().str.lower()
    df["mes_numero"] = df["mes"].apply(mes_a_numero)
    
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


def calcular_rango_12_meses(
    mes_final: int,
    anio: int,
    df_tarifas: pd.DataFrame,
    tarifa: str,
    division: str,
) -> Tuple[int, int, int, int, Optional[str]]:
    """
    Calcula el rango de 12 meses para histórico, aplicando casos borde.
    
    Args:
        mes_final: Número de mes final (1-12)
        anio: Año del mes final seleccionado
        df_tarifas: DataFrame de tarifas (con columnas anio, mes_numero, region, tarifa)
        tarifa: Código de tarifa
        division: División/región CFE (se normaliza)
        
    Returns:
        (mes_inicial, año_inicial, mes_final_ajustado, año_final_ajustado, mensaje_info)
        mensaje_info es None si no hubo ajuste, o texto informativo en casos borde.
    """
    div_norm = normalizar_texto(division)
    tarifa_norm = tarifa.upper() if tarifa else ""
    
    mask = (df_tarifas["region"] == div_norm) & (df_tarifas["tarifa"] == tarifa_norm)
    df_filt = df_tarifas.loc[mask, ["anio", "mes_numero"]].drop_duplicates()
    
    if df_filt.empty:
        return (1, anio, 12, anio, "Sin datos para esta tarifa y división.")
    
    df_filt = df_filt.sort_values(["anio", "mes_numero"])
    first = df_filt.iloc[0]
    last = df_filt.iloc[-1]
    first_anio, first_mes = int(first["anio"]), int(first["mes_numero"])
    last_anio, last_mes = int(last["anio"]), int(last["mes_numero"])
    
    first_ord = first_anio * 12 + first_mes
    last_ord = last_anio * 12 + last_mes
    desired_end_ord = anio * 12 + mes_final
    desired_start_ord = desired_end_ord - 11
    
    if desired_end_ord > last_ord:
        end_ord = last_ord
        start_ord = max(end_ord - 11, first_ord)
        end_anio = (end_ord - 1) // 12
        end_mes = (end_ord - 1) % 12 + 1
        start_anio = (start_ord - 1) // 12
        start_mes = (start_ord - 1) % 12 + 1
        msg = f"Último mes disponible: {numero_a_mes(end_mes)} {end_anio}. Mostrando histórico de 12 meses hasta esa fecha."
        return (start_mes, start_anio, end_mes, end_anio, msg)
    
    if desired_start_ord < first_ord:
        start_ord = first_ord
        end_ord = min(start_ord + 11, last_ord)
        start_anio = (start_ord - 1) // 12
        start_mes = (start_ord - 1) % 12 + 1
        end_anio = (end_ord - 1) // 12
        end_mes = (end_ord - 1) % 12 + 1
        msg = f"Primer mes disponible: {numero_a_mes(start_mes)} {start_anio}. Mostrando histórico de 12 meses desde esa fecha."
        return (start_mes, start_anio, end_mes, end_anio, msg)
    
    start_ord = desired_start_ord
    end_ord = desired_end_ord
    start_anio = (start_ord - 1) // 12
    start_mes = (start_ord - 1) % 12 + 1
    end_anio = (end_ord - 1) // 12
    end_mes = (end_ord - 1) % 12 + 1
    
    n_meses = end_ord - start_ord + 1
    msg = None
    if n_meses < 12:
        msg = f"Rango disponible: {numero_a_mes(start_mes)} {start_anio} - {numero_a_mes(end_mes)} {end_anio} ({n_meses} meses)"
    
    return (start_mes, start_anio, end_mes, end_anio, msg)


def pivotar_historico_por_mes(df_hist: pd.DataFrame) -> pd.DataFrame:
    """
    Convierte el histórico en formato largo a una fila por (Año, Mes) con columnas
    Cargo Fijo, Base, Intermedia, Punta, Cargo Cap para mejor legibilidad.

    Espera df_hist con columnas: anio, mes, mes_numero, cargo, int_horario, total.
    Para tarifas simples (int_horario "sin dato") el total variable va en Base.
    """
    if df_hist.empty or "total" not in df_hist.columns or "anio" not in df_hist.columns:
        return pd.DataFrame(columns=["Año", "Mes", "Fecha", "Cargo Fijo", "Base", "Intermedia", "Punta", "Cargo Cap"])

    df = df_hist[["anio", "mes_numero", "mes", "cargo", "int_horario", "total"]].copy()
    df["cargo"] = df["cargo"].astype(str).str.strip()
    df["int_horario"] = df["int_horario"].astype(str).str.strip().str.upper()
    df["mes"] = df["mes"].astype(str).str.strip().str.lower()

    rows = []
    for (anio, mes_num), g in df.groupby(["anio", "mes_numero"], sort=True):
        mes_num = int(mes_num)
        anio = int(anio)
        mes_nombre = numero_a_mes(mes_num).capitalize() if 1 <= mes_num <= 12 else g["mes"].iloc[0].capitalize()
        fecha_abrev = f"{MESES_ABREV_POR_NUM[mes_num - 1]}-{str(anio)[-2:]}" if 1 <= mes_num <= 12 else ""

        fijo = g[g["cargo"] == "Fijo"]["total"]
        cargo_fijo = float(fijo.iloc[0]) if len(fijo) else None

        var = g[g["cargo"] == "Variable (Energía)"]
        base_val = intermedia_val = punta_val = None
        for _, r in var.iterrows():
            ih = r["int_horario"]
            if ih == "B":
                base_val = float(r["total"])
            elif ih == "I":
                intermedia_val = float(r["total"])
            elif ih == "P":
                punta_val = float(r["total"])
            elif ih == "SIN DATO" or (pd.notna(ih) and "SIN" in str(ih).upper()):
                if base_val is None:
                    base_val = float(r["total"])

        cap = g[g["cargo"] == "Capacidad"]["total"]
        cargo_cap = float(cap.iloc[0]) if len(cap) else None

        rows.append({
            "Año": anio,
            "Mes": mes_nombre,
            "Fecha": fecha_abrev,
            "Cargo Fijo": cargo_fijo,
            "Base": base_val,
            "Intermedia": intermedia_val,
            "Punta": punta_val,
            "Cargo Cap": cargo_cap,
        })

    return pd.DataFrame(rows)


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
