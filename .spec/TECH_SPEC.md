# Technical Specification: CFE-Tariff-App

## 1. Stack Tecnológico
* **Lenguaje:** Python 3.10+
* **Web Framework:** Streamlit (para la interfaz dinámica).
* **Data Engine:** Pandas (limpieza y agregaciones).
* **Almacenamiento:** Archivos CSV locales en el repositorio.
* **Gráficos:** Plotly Express.
* **Despliegue:** Streamlit Cloud (gratuito).

## 2. Modelo de Datos (DataFrames en Memoria)

### DataFrame: `df_geografia`
Cargado desde `data/01_catalogo_regiones.csv`
* `estado` (str) - Nombre del estado en UPPER CASE
* `municipio` (str) - Nombre del municipio en UPPER CASE
* `division` (str) - División de CFE en UPPER CASE (llave de unión con tarifas)

### DataFrame: `df_tarifas`
Cargado desde `data/02_tarifas_finales_suministro_basico.csv`
* `anio` (int) - Año del registro
* `mes` (str) - Mes en minúsculas (enero, febrero, etc.)
* `tarifa` (str) - Código de tarifa (GDMTH, PDBT, etc.)
* `descripcion` (str) - Descripción de la tarifa
* `int_horario` (str) - Intervalo horario [B, I, P, sin dato]
* `cargo` (str) - Tipo de cargo [Fijo, Variable (Energía), Capacidad]
* `unidades` (str) - Unidades de medida
* `region` (str) - Región/División en UPPER CASE (match con df_geografia.division)
* `transmision`, `distribucion`, `cenace`, `suministro`, `scnmem`, `generacion`, `capacidad` (float) - Componentes de la tarifa
* `total` (float) - Suma total de componentes

## 3. Arquitectura de Datos

```
┌─────────────────────────────────────────────────────────┐
│                    Streamlit Cloud                       │
│  ┌─────────────────────────────────────────────────┐    │
│  │                   app.py                         │    │
│  │  ┌─────────────┐    ┌─────────────────────────┐ │    │
│  │  │ data_loader │───▶│ df_geografia, df_tarifas │ │    │
│  │  │   (cached)  │    │     (in-memory)         │ │    │
│  │  └─────────────┘    └─────────────────────────┘ │    │
│  └─────────────────────────────────────────────────┘    │
│                           │                              │
│                           ▼                              │
│  ┌─────────────────────────────────────────────────┐    │
│  │                  data/                           │    │
│  │  • 01_catalogo_regiones.csv (~2,600 registros)  │    │
│  │  • 02_tarifas_finales_suministro_basico.csv     │    │
│  │    (~62,000+ registros)                          │    │
│  └─────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

## 4. Flujo de Actualización de Datos (Mensual)

La usuaria final actualiza tarifas así:
1. Obtiene nuevo CSV de tarifas (mismo formato)
2. Usa `st.file_uploader` en la app para subir el archivo
3. La app valida el formato y muestra preview
4. Los nuevos datos se agregan/actualizan en memoria
5. (Opcional) El desarrollador actualiza el CSV en el repo para persistencia

## 5. Lógica de Negocio (Pseudocódigo)

```python
# 1. Carga con cache
@st.cache_data
def load_geografia():
    df = pd.read_csv('data/01_catalogo_regiones.csv')
    df.columns = ['estado', 'municipio', 'division']
    df = df[['estado', 'municipio', 'division']]  # Eliminar columnas vacías
    df = df.apply(lambda x: x.str.upper().str.strip())
    return df

@st.cache_data
def load_tarifas():
    df = pd.read_csv('data/02_tarifas_finales_suministro_basico.csv')
    df['region'] = df['region'].str.upper().str.strip()
    return df

# 2. Filtrado
df_actual = df_tarifas[
    (df_tarifas.anio == selected_year) & 
    (df_tarifas.region == selected_div) & 
    (df_tarifas.tarifa == selected_tar)
]
df_prev = df_tarifas[
    (df_tarifas.anio == selected_year - 1) & 
    (df_tarifas.region == selected_div) & 
    (df_tarifas.tarifa == selected_tar)
]

# 3. Cálculo de Métricas
Metric_Dic = (Total_Dic_N / Total_Dic_N-1) - 1
Metric_Avg = (Mean_N / Mean_N-1) - 1
```

## 6. Normalización de Datos

* Regiones/Divisiones: Convertir a UPPER CASE para match consistente
* Meses: Mantener en minúsculas (enero, febrero, etc.) como vienen en el CSV
* Valores numéricos: Manejar valores vacíos como NaN
