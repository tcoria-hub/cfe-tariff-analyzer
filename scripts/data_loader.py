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
