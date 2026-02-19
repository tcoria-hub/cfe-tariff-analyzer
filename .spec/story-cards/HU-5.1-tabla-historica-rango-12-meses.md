# Historia 5.1: Tabla Histórica de Tarifas por Rango de 12 Meses

## 🎯 Objetivo de la Sesión
Implementar Tabla Histórica de Tarifas por Rango de 12 Meses. Ver una tabla con el histórico completo de una tarifa y división en un rango de 12 meses calculado desde un mes final seleccionado para analizar la evolución mes a mes de todos los componentes tarifarios en un periodo específico.

## 📝 Current Objective (Copiar a current_objective.md)
- [ ] Crear selector de "Mes Final del Rango" con opciones enero a diciembre
- [ ] Implementar función `mes_a_numero()` para convertir nombre de mes a número (1-12)
- [ ] Implementar función `calcular_rango_12_meses()` que detecta primer/último mes disponible y aplica casos borde
- [ ] Manejar caso borde: mes posterior al último disponible (detectar último mes, calcular 12 meses hacia atrás, mostrar mensaje)
- [ ] Manejar caso borde: mes anterior al primero disponible (detectar primer mes, calcular 12 meses hacia adelante, mostrar mensaje)
- [ ] Manejar caso: menos de 12 meses disponibles (mostrar todos con mensaje del rango real)
- [ ] Crear tabla ordenada cronológicamente con columnas: Mes, Año, Cargo, Intervalo Horario, Componentes (Generación, Transmisión, Distribución, CENACE, SCnMEM, Suministro, Capacidad), Total, Unidades
- [ ] Mostrar filas separadas por intervalo horario (Base, Intermedia, Punta) para tarifas horarias
- [ ] Mostrar solo filas correspondientes sin segmentación horaria para tarifas simples
- [ ] Implementar tabla interactiva con `st.dataframe` que permita ordenar por columnas
- [ ] Mostrar total de registros y rango de fechas calculado
- [ ] Manejar meses sin datos disponibles (mostrar fila vacía o mensaje)
- [ ] Implementar botón "Descargar CSV" con `st.download_button` que exporte todas las filas visibles
- [ ] Generar nombre de archivo dinámico: `historico_[tarifa]_[division]_[mes_inicial]_[mes_final].csv`

## 🤖 Prompt para Cursor (Composer)

Implementa la Historia de Usuario HU-5.1 del Feature 5: Histórico de Tarifas por Rango de 12 Meses.

**Contexto:**
- Proyecto: CFE Tariff Analyzer - App de análisis de tarifas eléctricas
- Feature: Histórico de Tarifas por Rango de 12 Meses
- Referencias: @.spec/BACKLOG.md (HU 5.1), @.spec/TECH_SPEC.md

**Historia de Usuario:**
- **Como:** Analista de costos energéticos
- **Quiero:** Ver una tabla con el histórico completo de una tarifa y división en un rango de 12 meses calculado desde un mes final seleccionado
- **Para poder:** Analizar la evolución mes a mes de todos los componentes tarifarios en un periodo específico

**Criterios de Aceptación:**
1. Se muestra un selector de "Mes Final del Rango" que permite elegir cualquier mes del año seleccionado (enero a diciembre)
2. Al seleccionar un mes final (ej: diciembre 2024), el sistema calcula automáticamente el rango de 12 meses hacia atrás desde ese mes
3. **Caso borde - Mes posterior al último disponible:** Detecta automáticamente el último mes disponible, calcula el rango de 12 meses terminando en ese último mes, muestra mensaje informativo
4. **Caso borde - Mes anterior al primero disponible:** Detecta automáticamente el primer mes disponible, calcula el rango de 12 meses comenzando desde ese primer mes, muestra mensaje informativo
5. Si hay menos de 12 meses disponibles en total, se muestran todos los meses disponibles con un mensaje indicando el rango real
6. Se muestra una tabla ordenada cronológicamente con columnas: Mes, Año, Cargo, Intervalo Horario, Componentes, Total, Unidades
7. Para tarifas horarias, se muestran filas separadas por cada intervalo horario (Base, Intermedia, Punta) por mes
8. Para tarifas simples, se muestran solo las filas correspondientes (sin segmentación horaria)
9. La tabla es interactiva y permite ordenar por cualquier columna haciendo clic en el encabezado
10. Se muestra el total de registros en el rango seleccionado y el rango de fechas calculado
11. Si algún mes dentro del rango no tiene datos disponibles, se muestra claramente (fila vacía o mensaje)
12. **Exportación a CSV:** Existe un botón "Descargar CSV" que exporta exactamente las filas mostradas en la tabla con todas las columnas

**Requisitos Técnicos:**
- Stack: Python 3.10+ (Streamlit), Pandas para ETL, Plotly Express para gráficas
- Datos en `data/02_tarifas_finales_suministro_basico.csv`
- Componentes Streamlit: `st.selectbox`, `st.dataframe`, `st.download_button`, `st.info()`, `st.warning()`
- Crear función helper `mes_a_numero(mes_nombre: str) -> int` para convertir nombre de mes a número (1-12)
- Crear función helper `calcular_rango_12_meses(mes_final: int, año: int, df_tarifas: pd.DataFrame, tarifa: str, division: str) -> tuple` que detecta primer/último mes disponible, aplica lógica de casos borde, retorna (mes_inicial, año_inicial, mes_final_ajustado, año_final_ajustado, mensaje_info)
- Filtrar datos con: `(df.anio >= año_inicial) & (df.anio <= año_final_ajustado) & (df.mes_numero >= mes_inicial) & (df.mes_numero <= mes_final_ajustado) & (df.region == division) & (df.tarifa == tarifa_seleccionada)`
- Ordenar por: `anio`, `mes_numero`, `cargo`, `int_horario` (si aplica)
- Usar `st.download_button` con `df.to_csv(index=False, encoding='utf-8')` para exportar CSV
- Generar nombre de archivo dinámico: `f"historico_{tarifa}_{division}_{mes_inicial_nombre}{año_inicial}_{mes_final_nombre}{año_final}.csv"`

**Instrucciones:**
1. Revisar criterios de aceptación y casos de prueba en BACKLOG.md (HU 5.1)
2. Implementar funciones helper para conversión de meses y cálculo de rangos con casos borde
3. Crear selector de mes final del rango
4. Implementar lógica de filtrado y ordenamiento de datos
5. Crear tabla interactiva con `st.dataframe` mostrando todas las columnas requeridas
6. Implementar botón de exportación a CSV con nombre de archivo dinámico
7. Manejar casos borde y mostrar mensajes informativos apropiados
8. Mantener consistencia con código existente en `scripts/app.py` y `scripts/data_loader.py`
9. Consultar @.spec/PRD.md y @.spec/TECH_SPEC.md si hay dudas sobre estructura de datos

## 🧪 Pruebas de Aceptación
- [ ] **CP-5.1.1:** Seleccionar GDMTH, División Baja California, Año 2024, Mes Final: Diciembre → muestra tabla con 12 meses (enero-diciembre 2024), cada mes con 3 filas (Base, Intermedia, Punta) = 36 filas totales
- [ ] **CP-5.1.2:** Seleccionar PDBT, División Bajío, Año 2024, Mes Final: Junio → muestra tabla con 12 meses (julio 2023 - junio 2024), cada mes con 2 filas (Fijo, Variable) = 24 filas totales
- [ ] **CP-5.1.3:** Seleccionar mes final "Marzo 2024" muestra 12 meses (abril 2023 - marzo 2024)
- [ ] **CP-5.1.4:** Si el último mes disponible es septiembre 2024 y el usuario selecciona diciembre 2024, el sistema muestra: "Último mes disponible: septiembre 2024. Mostrando histórico de 12 meses hasta esa fecha." y calcula octubre 2023 - septiembre 2024
- [ ] **CP-5.1.5:** Si el primer mes disponible es marzo 2023 y el usuario selecciona enero 2023, el sistema muestra: "Primer mes disponible: marzo 2023. Mostrando histórico de 12 meses desde esa fecha." y calcula marzo 2023 - febrero 2024
- [ ] **CP-5.1.6:** Si solo hay 8 meses disponibles (ej: marzo-octubre 2024), se muestran esos 8 meses con mensaje: "Rango disponible: marzo 2024 - octubre 2024 (8 meses)"
- [ ] **CP-5.1.7:** La tabla permite ordenar por columna "Total" para identificar el mes con mayor costo
- [ ] **CP-5.1.8:** La tabla muestra correctamente los nombres de meses en español (enero, febrero, marzo, etc.)
- [ ] **CP-5.1.9:** Al hacer clic en "Descargar CSV", se descarga un archivo con todas las filas de la tabla visible, formato CSV con encoding UTF-8
- [ ] **CP-5.1.10:** El nombre del archivo CSV descargado sigue el formato: `historico_GDMTH_BAJA_CALIFORNIA_enero2024_diciembre2024.csv`

**Formato BDD:**
```gherkin
Dado que: El usuario ha seleccionado Estado "BAJA CALIFORNIA", Municipio "MEXICALI", Tarifa "GDMTH", Año 2024
Cuando: Selecciona "Mes Final del Rango: Diciembre"
Entonces: El sistema calcula el rango de 12 meses (enero 2024 - diciembre 2024)
Y: Muestra una tabla con 12 meses ordenados cronológicamente
Y: Cada mes muestra 3 filas correspondientes a Base, Intermedia y Punta
Y: Las filas están ordenadas cronológicamente (enero primero, diciembre último)
Y: La tabla muestra todas las columnas: Mes, Año, Cargo, Intervalo Horario, Componentes, Total, Unidades
Y: Existe un botón "Descargar CSV" que exporta la tabla completa

Escenario: Mes posterior al último disponible
Dado que: El último mes disponible para GDMTH en Baja California es septiembre 2024
Cuando: El usuario selecciona "Mes Final: Diciembre 2024"
Entonces: El sistema detecta que septiembre 2024 es el último mes disponible
Y: Muestra mensaje informativo sobre el ajuste
Y: Calcula el rango de 12 meses terminando en septiembre 2024 (octubre 2023 - septiembre 2024)

Escenario: Mes anterior al primero disponible
Dado que: El primer mes disponible para PDBT en Bajío es marzo 2023
Cuando: El usuario selecciona "Mes Final: Enero 2023"
Entonces: El sistema detecta que marzo 2023 es el primer mes disponible
Y: Muestra mensaje informativo sobre el ajuste
Y: Calcula el rango de 12 meses comenzando en marzo 2023 (marzo 2023 - febrero 2024)
```
