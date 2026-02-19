# Changelog - CFE Tariff Analyzer

Todos los cambios notables del proyecto serán documentados aquí.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/).

---

## [2026-02-19]

### HU-5.1: Tabla Histórica de Tarifas por Rango de 12 Meses
**Tiempo de ciclo:** ~1 día (~26 horas)

#### Implementado
- Selector "Mes Final del Rango" (enero–diciembre) en tab Generar Histórico.
- Funciones helper: `mes_a_numero`, `numero_a_mes`, `calcular_rango_12_meses` con casos borde (mes posterior/al anterior al rango disponible, menos de 12 meses).
- Columna `mes_numero` en carga de tarifas; tabla pivotada una fila por mes con columnas: Año, Mes, Fecha (abrev.), Cargo Fijo, Base, Intermedia, Punta, Cargo Cap.
- Formato numérico: 2 decimales + miles (Fijo/Cap), 4 decimales (Base/Intermedia/Punta).
- Botón "Descargar CSV" que exporta la vista mostrada con nombre dinámico.

#### Decisiones clave
- Vista pivotada para legibilidad (referencia tipo hoja de cálculo); CSV exporta exactamente lo mostrado.
- `MESES_ABREV_POR_NUM` para no colisionar con el dict `MESES_ABREV` usado en gráficas.

#### Archivos modificados
- `scripts/data_loader.py` – `mes_a_numero`, `numero_a_mes`, `calcular_rango_12_meses`, `pivotar_historico_por_mes`, `MESES_ABREV_POR_NUM`, `mes_numero` en load_tarifas.
- `scripts/app.py` – Tab Generar Histórico: selector mes final, pivot, formato, column_config, download CSV.

---

## [2026-02-18]

### HU-5.2: Navegación entre Modos de Análisis
**Tiempo de ciclo:** ~2 horas

#### Implementado
- Navegación con tres tabs: Análisis de Comportamiento, Generar Histórico, Captura de Datos de Recibo.
- Selectores comunes (Estado, Municipio, Tarifa, Año) fuera de los tabs para acceso desde cualquier modo.
- Persistencia de selecciones entre modos con `st.session_state`.
- Contenido existente (Features 2 y 3) dentro del tab "Análisis de Comportamiento".
- Placeholders para Generar Histórico (HU-5.1) y Captura de Datos (Feature 6).

#### Decisiones Clave
- Tabs en área principal para no ocultar selectores; en HU-5.1 se podrá revisar si el selector mes/año del histórico va dentro del tab o común.
- Resumen y tabs solo cuando hay tarifas seleccionadas; corrección de flujo if/else y de indentación del bloque de análisis.

#### Archivos Modificados
- `scripts/app.py` – Navegación con tabs, session_state para selectores, refactor de flujo e indentación.

---

## [2026-02-06]

### HU-1.5: Descripción Completa de Tarifa Seleccionada
**Tiempo de ciclo:** ~15 minutos

#### Implementado
- Descripción completa de la tarifa visible arriba de "Resumen de Tarifas"
- Diccionario `tarifa_descripcion` para mapeo de código a descripción
- Componente visual con `st.info()` mostrando "**CÓDIGO** — Descripción"
- Actualización dinámica al cambiar de tarifa

#### Decisiones Clave
- **Reutilización de datos existentes:** Se aprovechó la columna `descripcion` del DataFrame existente
- **Formato visual:** `st.info()` elegido sobre `st.markdown()` para mayor visibilidad

#### Archivos Modificados
- `scripts/app.py` - Diccionario `tarifa_descripcion` y `st.info()` con descripción

---

## [2026-02-05]

### HU-3.5: Vista Consolidada para Tarifas Simples
**Tiempo de ciclo:** ~10 minutos

#### Implementado
- KPI de Cargo Fijo Promedio para tarifas simples ($/mes)
- KPI de Cargo Variable Promedio ($/kWh) en 2 columnas
- Eliminada sección "Ver detalles de los datos"

#### Decisiones Clave
- **Formato diferenciado**: Cargo Fijo en $/mes, Variable en $/kWh
- **Limpieza de UI**: Removida tabla de debug que mostraba datos crudos

#### Archivos Modificados
- `scripts/app.py` - 2 KPIs para tarifas simples, versión v1.6.0

---

### 🎉 FEATURE 3 COMPLETADO
Feature 3 "Análisis de Promedio Anual e Inteligencia Horaria" 100% implementado (5/5 historias)

---

### HU-3.3: Vista Segmentada por Horario
**Tiempo de ciclo:** ~5 minutos

#### Implementado
- Leyenda de horarios típicos con `st.caption`
- Nota: La funcionalidad principal (3 KPIs) ya existía desde HU-3.1

#### Decisiones Clave
- **Reutilización**: Se aprovechó código de HU-3.1 (3 columnas con st.metric)
- **Formato de leyenda**: "Base (0:00-6:00) | Intermedia (6:00-18:00, 22:00-0:00) | Punta (18:00-22:00)"

#### Archivos Modificados
- `scripts/app.py` - Leyenda de horarios, versión v1.5.1

---

### HU-3.1: KPI de Promedio Anual
**Tiempo de ciclo:** ~20 minutos

#### Implementado
- Función `calcular_promedio_anual()` para calcular media aritmética de meses disponibles
- Función `calcular_variacion_promedio_anual()` para comparar promedios entre dos años
- Sección "📊 Promedio Anual" en la UI con `st.metric`
- Para tarifas horarias: 3 KPIs en columnas (Base, Intermedia, Punta)
- Para tarifas simples: 1 KPI para Variable (Energía)

#### Decisiones Clave
- **Comparación justa**: Solo se comparan meses que existen en ambos años
- **Tooltip informativo**: Muestra cantidad de meses comparados y valor anterior
- **delta_color="inverse"**: Incrementos en rojo (malo), decrementos en verde (bueno)

#### Archivos Modificados
- `scripts/data_loader.py` - Nuevas funciones para cálculo de promedios
- `scripts/app.py` - Sección KPI de promedio anual, versión v1.5.0

---

### HU-3.4: Gráfica de Tendencia Mensual
**Tiempo de ciclo:** ~30 minutos

#### Implementado
- Funciones `get_tendencia_mensual()` y `get_datos_tendencia_comparativa()` en data_loader.py
- Constantes `MESES_ORDEN` y `MESES_ABREV` para ordenamiento
- Sección "📈 Tendencia Mensual" con gráficas de líneas
- Para tarifas horarias: 3 gráficas en columnas (Base | Intermedia | Punta)
- Para tarifas simples: una sola gráfica
- Colores: Azul (año anterior), Rojo (año actual)
- Marcadores + hover interactivo

#### Archivos Modificados
- `scripts/data_loader.py` - Funciones de tendencia mensual
- `scripts/app.py` - Sección de gráficas de líneas, versión v1.4.0

---

### HU-3.2: Detección Automática de Estructura Horaria
**Tiempo de ciclo:** N/A (implementada previamente en HU-1.3)

#### Ya implementado
- Constante `TARIFAS_HORARIAS = {"GDMTH", "DIST", "DIT"}`
- Función `es_tarifa_horaria()` para clasificación
- Vistas diferenciadas en toda la app según tipo de tarifa

---

### HU-2.2: Desglose de Variación por Componente
**Tiempo de ciclo:** ~45 minutos

#### Implementado
- Funciones `get_componentes_diciembre()` y `calcular_variacion_componentes()` en data_loader.py
- Sección "🔍 Desglose por Componente" con gráficas de barras horizontales
- Ordenamiento por impacto (mayor variación absoluta primero)
- Colores: Rojo (subió), Verde (bajó)
- **Reorganización de UI con pestañas** `[DIST] [GDMTH] [GDMTO]` por tarifa
- Desglose de tarifas horarias en 3 columnas (Base | Intermedia | Punta)

#### Decisiones Clave
- **Pestañas por tarifa**: Para evitar scroll infinito con múltiples tarifas
- **Componentes dinámicos**: Solo se muestran los que tienen datos en el CSV

#### Archivos Modificados
- `scripts/data_loader.py` - Nuevas funciones y constantes de componentes
- `scripts/app.py` - Pestañas st.tabs(), sección de desglose, versión v1.3.0

---

### 🎉 FEATURE 2 COMPLETADO
Feature 2 "Comparativo Diciembre vs Diciembre" 100% implementado (3/3 historias)

---

### HU-2.3: Gráfica Comparativa de Cierres
**Tiempo de ciclo:** ~1 hora

#### Implementado
- Gráfica de barras agrupadas con Plotly Express para comparar dic año N vs año N-1
- Dos gráficas separadas por unidad: Variable ($/kWh) y Capacidad ($/kW)
- Colores distintivos: Azul (año anterior), Rojo (año actual)
- Hover interactivo con valores exactos
- Etiquetas de valores sobre cada barra

#### Decisiones Clave
- **Gráficas separadas**: Para evitar escalas incompatibles ($/kWh ~$2 vs $/kW ~$400)
- **Proporción 3:1**: Variable ocupa más espacio por tener más conceptos

#### Archivos Modificados
- `scripts/app.py` - Gráfica comparativa con Plotly Express, versión v1.2.0

---

### HU-2.1: KPI de Variación Total Diciembre
**Tiempo de ciclo:** ~1 hora

#### Implementado
- Sección "📊 Comparativo Diciembre vs Diciembre" con tabla comparativa
- Columnas: Concepto, Dic Año Anterior, Dic Año Actual, Variación %, Unidad
- Desglose por horario (Base, Intermedia, Punta) para tarifas horarias
- Cargo de Capacidad ($/kW) para todas las tarifas
- Indicadores visuales de variación (🔴 incremento, 🟢 decremento)
- Warning cuando el año seleccionado puede no tener diciembre completo
- Validación contra datos de Excel/Power BI (DIST, Baja California Sur)

#### Decisiones Clave
- **Cargo específico "Variable (Energía)":** Solo se muestra en $/kWh, sin sumar cargos con unidades diferentes
- **Tabla vs Métricas:** Formato tabular para mostrar año anterior y actual lado a lado
- **Capacidad separada:** Se incluye como concepto adicional en $/kW

#### Archivos Modificados
- `scripts/data_loader.py` - Nuevas funciones: `get_cargo_variable_diciembre()`, `get_cargo_capacidad_diciembre()`, `get_cargos_diciembre_por_horario()`
- `scripts/app.py` - Nueva sección de comparativo diciembre

---

### HU-1.4: Selector de Año de Análisis
**Tiempo de ciclo:** ~10 minutos

#### Implementado
- Sección "📅 Selector de Año" con años disponibles (2018-2025)
- Cálculo automático de año comparativo (año - 1)
- Resumen de selección completa (División, Tarifas, Periodo)
- Versión actualizada a v1.0.0

#### Decisiones Clave
- **Default al año más reciente:** Selector inicia con último año disponible

#### Archivos Modificados
- `scripts/app.py` - Selector de año y resumen

---

### 🎉 FEATURE 1 COMPLETADO
Feature 1 "Selector Geográfico y de Tarifas" 100% implementado (4/4 historias)

---

### HU-1.3: Selector Dinámico de Tarifas
**Tiempo de ciclo:** ~15 minutos

#### Implementado
- Sección "⚡ Selector de Tarifas" con `st.multiselect`
- Formato "CÓDIGO - Descripción" para cada tarifa
- Clasificación automática: tarifas horarias vs simples
- Función `es_tarifa_horaria()` y constante `TARIFAS_HORARIAS`

#### Decisiones Clave
- **Selección múltiple:** `st.multiselect` permite elegir varias tarifas simultáneamente

#### Archivos Modificados
- `scripts/app.py` - Selector de tarifas
- `scripts/data_loader.py` - `es_tarifa_horaria()`, `TARIFAS_HORARIAS`

---

### HU-1.2: Selector de Municipio con Mapeo a División
**Nota:** Implementada junto con HU-1.1 (funcionalidad incluida en el flujo Estado → Municipio → División)

---

### HU-1.1: Selector de Estado
**Tiempo de ciclo:** ~20 minutos

#### Implementado
- Sección "📍 Selector Geográfico" con selectores Estado → Municipio → División
- Selector de Estado con 32 opciones ordenadas alfabéticamente + placeholder
- Selector de Municipio dinámico filtrado por estado seleccionado
- Selector de División cuando un municipio tiene múltiples opciones (ej: CDMX)
- Nueva función `get_divisiones()` en `data_loader.py`

#### Decisiones Clave
- **Múltiples divisiones:** Algunos municipios pertenecen a 2+ divisiones CFE → selector adicional
- **UX progresivo:** Selectores se habilitan conforme se completa la selección anterior

#### Archivos Modificados
- `scripts/app.py` - Selectores geográficos
- `scripts/data_loader.py` - Nueva función `get_divisiones()`

---

### HU-0.2: Carga y Gestión de Datos desde CSV
**Tiempo de ciclo:** ~45 minutos

#### Implementado
- Módulo `scripts/data_loader.py` con 10 funciones de carga y utilidades
- Normalización de texto (UPPER CASE, sin acentos) para match consistente
- Cache con `@st.cache_data` para optimizar rendimiento
- Estadísticas de carga en `app.py`

#### Decisiones Clave
- **Eliminación de Supabase:** Reemplazado por CSV locales (sin costos, despliegue simple)
- **Normalización de acentos:** BAJÍO → BAJIO para match entre tablas
- **Compatibilidad Python 3.9+:** Uso de `Optional[str]` en lugar de `str | None`

#### Archivos Modificados
- `scripts/data_loader.py` - Nuevo
- `scripts/app.py` - Actualizado con métricas
- `.spec/TECH_SPEC.md`, `.spec/PRD.md`, `README.md` - Sin Supabase
- `requirements.txt` - Eliminado supabase

---

### HU-0.1: Configuración del Entorno de Desarrollo
**Tiempo de ciclo:** ~1 hora

#### Implementado
- `requirements.txt` con dependencias: streamlit, pandas, supabase, plotly, python-dotenv
- `scripts/app.py` con página de bienvenida de la aplicación
- Verificación de `.env.example` y `README.md`

#### Decisiones Clave
- Versiones mínimas (>=) en requirements.txt para flexibilidad
- Agregado python-dotenv para manejo de variables de entorno

#### Archivos Modificados
- `requirements.txt` - Nuevo
- `scripts/app.py` - Nuevo

---

### Inicialización del Proyecto
- Creación de estructura de proyecto
- Definición de BACKLOG.md con 4 Features y 14 Historias de Usuario
- Configuración de workflow con comandos en `.spec/commands/`
- Documentación inicial: PRD.md, spec.md

---

<!-- Nuevas entradas se agregan arriba de esta línea -->
