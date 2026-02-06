# Changelog - CFE Tariff Analyzer

Todos los cambios notables del proyecto serán documentados aquí.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/).

---

## [2026-02-05]

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
