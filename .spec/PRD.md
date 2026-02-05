# Product Requirements Document (PRD): CFE Tariff Analyzer MVP

## 1. Visión del Proyecto
Desarrollar una aplicación web interactiva que automatice el análisis de tarifas de CFE, permitiendo a usuarios finales y analistas entender variaciones de costos basándose en su ubicación geográfica exacta y el comportamiento histórico de los componentes tarifarios.

## 2. Objetivos de Negocio
* **Precisión:** Eliminar el procesamiento manual de datos para evitar errores de cálculo en comparativas interanuales.
* **Escalabilidad:** Mantener un histórico actualizado en la nube (Supabase) que permita consultas instantáneas de cualquier tarifa del catálogo CFE.
* **Decisión Informada:** Proveer KPIs claros sobre el incremento real del costo energético (promedios vs cierres).

## 3. Características del MVP (Alcance)

### Feature 1: Selector Geográfico y de Tarifas (Smart Locator)
* **Entrada de Usuario:** Selectores anidados de `Estado` -> `Municipio`.
* **Lógica Interna:** Mapeo automático del municipio seleccionado a la `División` de CFE correspondiente (usando el catálogo de ~2,600 registros).
* **Filtro de Tarifas:** Selector dinámico que carga **todas** las tarifas disponibles en el CSV (GDMTH, GDMTO, DIST, PDBT, RABT, etc.).
* **Filtro Temporal:** Selección del `Año de Análisis` (base para comparar contra el `Año n-1`).

### Feature 2: Comparativo de Cierre "Diciembre vs Diciembre"
* **Cálculo:** Comparación del valor `total` de diciembre del año seleccionado vs diciembre del año anterior.
* **Desglose de Conceptos:** Visualización del impacto de cada componente (Generación, Transmisión, Distribución, Cenace, SCnMEM, Suministro y Capacidad) en la variación total.
* **Indicador:** Porcentaje de incremento o decremento nominal.

### Feature 3: Análisis de Promedio Anual e Inteligencia Horaria
* **Cálculo de Promedio:** Media aritmética de los meses disponibles del año seleccionado vs el mismo periodo del año anterior.
* **Detección Automática de Estructura:**
    * **Tarifas Horarias (ej. GDMTH):** El sistema identifica cargos por periodos `Base`, `Intermedia` y `Punta` y genera comparativas segmentadas por estos horarios.
    * **Tarifas Simples (ej. DIST, PDBT):** El sistema agrupa los cargos fijos y variables sin división horaria.
* **Visualización:** * **KPI Cards:** Tarjetas con la tendencia (alza/baja) del promedio anual.
    * **Gráfica de Tendencia:** Línea de tiempo (Ene-Dic) que compara visualmente ambos años.

## 4. Lineamientos Técnicos
* **Stack:** Python (Pandas + Streamlit + Plotly).
* **Persistencia:** Archivos CSV en el repositorio. Sin base de datos externa.
* **Despliegue:** Streamlit Cloud (gratuito, conectado a GitHub).
* **Actualización de datos:** La usuaria puede subir un nuevo CSV de tarifas mensualmente vía `st.file_uploader`.
* **Integración:** El sistema normaliza los nombres de las regiones/divisiones (UPPER CASE) para match consistente.

## 5. Criterios de Aceptación
1. El usuario puede llegar a sus datos de tarifa con máximo 3 clics (Estado > Municipio > Tarifa).
2. Los cálculos de variación (%) deben coincidir con los datos crudos del CSV original.
3. La interfaz debe adaptarse visualmente si la tarifa seleccionada no contiene cargos de "Punta" o "Intermedia".
