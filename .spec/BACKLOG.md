# BACKLOG - CFE Tariff Analyzer MVP

> **Última actualización:** 2026-02-05
> **Versión:** 1.0.0

## Estado del Proyecto

- ⏳ Feature 0: Configuración Inicial y ETL
- ⏳ Feature 1: Selector Geográfico y de Tarifas
- ⏳ Feature 2: Comparativo Diciembre vs Diciembre
- ⏳ Feature 3: Análisis de Promedio Anual e Inteligencia Horaria

---

## FEATURE 0: Configuración Inicial y ETL

### Descripción del Feature

- **Para:** El equipo de desarrollo
- **Que:** Necesita una base de datos configurada y datos cargados
- **Esta épica:** Provee la infraestructura necesaria para el funcionamiento de la app
- **Esperamos:** Reducir el tiempo de consulta y tener datos normalizados
- **Sabremos que hemos tenido éxito cuando:** Los datos estén disponibles en Supabase y la app pueda conectarse

---

### ✅ Historia de Usuario 0.1: Configuración del Entorno de Desarrollo

**Como:** Desarrollador  
**Quiero:** Tener un entorno de desarrollo configurado con todas las dependencias  
**Para poder:** Comenzar a desarrollar la aplicación sin problemas de configuración

#### Criterios de Aceptación

1. Existe un archivo `requirements.txt` con las dependencias: streamlit, pandas, supabase, plotly
2. El entorno virtual se puede crear y activar correctamente
3. Existe un archivo `.env.example` con las variables de entorno necesarias para Supabase
4. El README.md incluye instrucciones de instalación

#### Casos de Prueba

- **CP-0.1.1:** Ejecutar `pip install -r requirements.txt` sin errores
- **CP-0.1.2:** Ejecutar `streamlit run scripts/app.py` muestra página de bienvenida

---

### ✅ Historia de Usuario 0.2: Carga y Gestión de Datos desde CSV

**Como:** Desarrollador  
**Quiero:** Implementar la carga de datos desde archivos CSV locales  
**Para poder:** Tener los datos disponibles en la aplicación sin dependencias externas

#### Criterios de Aceptación

1. La app carga automáticamente `data/01_catalogo_regiones.csv` al iniciar
2. La app carga automáticamente `data/02_tarifas_finales_suministro_basico.csv` al iniciar
3. Los nombres de regiones están normalizados (UPPER CASE para match consistente)
4. Existe un módulo `scripts/data_loader.py` con funciones reutilizables para carga de datos
5. Los DataFrames se cachean con `@st.cache_data` para optimizar rendimiento

#### Casos de Prueba

- **CP-0.2.1:** Al iniciar la app, se cargan ~2,600 registros de geografía
- **CP-0.2.2:** Al iniciar la app, se cargan todos los registros de tarifas (~62,000+)
- **CP-0.2.3:** El join entre geografía y tarifas por division/region funciona correctamente

#### Notas de Arquitectura (Decisión 2026-02-05)

> **Cambio de arquitectura:** Se eliminó Supabase del stack.
> 
> **Razón:** Simplificar despliegue y evitar costos. La usuaria final actualizará 
> datos subiendo un nuevo CSV mensualmente.
> 
> **Nueva arquitectura:**
> - Datos: CSVs en repositorio + `st.file_uploader` para actualizaciones
> - Despliegue: Streamlit Cloud (gratuito)
> - Persistencia: Los CSVs actualizados se guardan en el repo vía PR o manual

---

## FEATURE 1: Selector Geográfico y de Tarifas (Smart Locator)

### Descripción del Feature

- **Para:** Usuario final o analista
- **Que:** Busca consultar tarifas de CFE de su ubicación
- **Esta épica:** Provee selectores intuitivos para filtrar por ubicación y tarifa
- **Esperamos:** Que el usuario llegue a sus datos en máximo 3 clics
- **Sabremos que hemos tenido éxito cuando:** El usuario pueda seleccionar Estado > Municipio > Tarifa en menos de 10 segundos

---

### ✅ Historia de Usuario 1.1: Selector de Estado

**Como:** Usuario de la aplicación  
**Quiero:** Seleccionar mi estado de la República Mexicana  
**Para poder:** Filtrar los municipios disponibles en mi zona

#### Criterios de Aceptación

1. Se muestra un `st.selectbox` con todos los estados únicos del catálogo
2. Los estados están ordenados alfabéticamente
3. Existe una opción por defecto "Selecciona un estado"
4. Al cambiar el estado, se actualiza el selector de municipios

#### Casos de Prueba

- **CP-1.1.1:** El selector muestra 32 estados de la República
- **CP-1.1.2:** Al seleccionar "AGUASCALIENTES", el selector de municipios muestra 11 opciones
- **CP-1.1.3:** Al seleccionar "BAJA CALIFORNIA", el selector de municipios muestra 5 opciones

**Formato BDD:**

```gherkin
Dado que: El usuario está en la página principal
Cuando: Hace clic en el selector de Estado
Entonces: Ve una lista de 32 estados ordenados alfabéticamente
```

---

### ✅ Historia de Usuario 1.2: Selector de Municipio con Mapeo a División

**Como:** Usuario de la aplicación  
**Quiero:** Seleccionar mi municipio después de elegir el estado  
**Para poder:** Que el sistema identifique automáticamente mi División de CFE

#### Criterios de Aceptación

1. El selector de municipios se habilita solo cuando hay un estado seleccionado
2. Los municipios mostrados corresponden únicamente al estado seleccionado
3. Al seleccionar un municipio, se almacena internamente la División de CFE correspondiente
4. El nombre de la División se muestra como información al usuario (ej: "División: BAJÍO")

#### Casos de Prueba

- **CP-1.2.1:** Seleccionar estado "AGUASCALIENTES" y municipio "CALVILLO" muestra División "BAJÍO"
- **CP-1.2.2:** Seleccionar estado "BAJA CALIFORNIA" y municipio "MEXICALI" muestra División "BAJA CALIFORNIA"
- **CP-1.2.3:** El selector de municipio está deshabilitado si no hay estado seleccionado

**Formato BDD:**

```gherkin
Dado que: El usuario ha seleccionado el estado "AGUASCALIENTES"
Cuando: Selecciona el municipio "CALVILLO"
Entonces: El sistema muestra "División: BAJÍO" y almacena esta división para filtrar tarifas
```

---

### ✅ Historia de Usuario 1.3: Selector Dinámico de Tarifas

**Como:** Usuario de la aplicación  
**Quiero:** Seleccionar el tipo de tarifa que deseo analizar  
**Para poder:** Ver los datos específicos de mi contrato eléctrico

#### Criterios de Aceptación

1. Se muestra un `st.selectbox` con todas las tarifas disponibles en el sistema
2. Las tarifas muestran código y descripción (ej: "GDMTH - Gran demanda en media tensión horaria")
3. El selector se habilita cuando hay una División seleccionada
4. Las tarifas disponibles son: DB1, DB2, PDBT, GDBT, RABT, RAMT, APBT, APMT, GDMTO, GDMTH, DIST, DIT

#### Casos de Prueba

- **CP-1.3.1:** El selector muestra todas las tarifas con código y descripción
- **CP-1.3.2:** Al seleccionar "GDMTH", el sistema identifica que es tarifa horaria
- **CP-1.3.3:** Al seleccionar "PDBT", el sistema identifica que es tarifa simple (sin horarios)

**Formato BDD:**

```gherkin
Dado que: El usuario ha seleccionado Estado y Municipio
Cuando: Hace clic en el selector de Tarifas
Entonces: Ve una lista de tarifas con formato "CÓDIGO - Descripción"
```

---

### ⏳ Historia de Usuario 1.4: Selector de Año de Análisis

**Como:** Usuario de la aplicación  
**Quiero:** Seleccionar el año que deseo analizar  
**Para poder:** Comparar ese año contra el año anterior

#### Criterios de Aceptación

1. Se muestra un `st.selectbox` con los años disponibles en los datos
2. El año mínimo seleccionable es 2018 (para poder comparar con 2017)
3. El año máximo es el último disponible en la base de datos
4. Al seleccionar un año, se calcula automáticamente el año comparativo (año - 1)

#### Casos de Prueba

- **CP-1.4.1:** El selector muestra años desde 2018 hasta el año más reciente
- **CP-1.4.2:** Seleccionar 2024 establece año comparativo como 2023
- **CP-1.4.3:** El año 2017 no está disponible para selección (no hay año anterior)

**Formato BDD:**

```gherkin
Dado que: El usuario ha completado los selectores anteriores
Cuando: Selecciona el año "2024"
Entonces: El sistema establece 2024 como año de análisis y 2023 como año de comparación
```

---

## FEATURE 2: Comparativo de Cierre "Diciembre vs Diciembre"

### Descripción del Feature

- **Para:** Analista de costos energéticos
- **Que:** Necesita comparar el cierre anual de tarifas
- **Esta épica:** Provee un comparativo detallado de diciembre año N vs diciembre año N-1
- **Esperamos:** Identificar el incremento real de costos al cierre del año
- **Sabremos que hemos tenido éxito cuando:** Los cálculos de variación coincidan con los datos crudos del CSV

---

### ⏳ Historia de Usuario 2.1: KPI de Variación Total Diciembre

**Como:** Analista de costos  
**Quiero:** Ver el porcentaje de variación del total de diciembre año N vs año N-1  
**Para poder:** Conocer rápidamente el incremento o decremento anual

#### Criterios de Aceptación

1. Se muestra una tarjeta `st.metric` con el valor total de diciembre del año seleccionado
2. Se muestra el delta (variación %) respecto al año anterior
3. El delta es positivo (rojo/alza) si hubo incremento, negativo (verde/baja) si hubo decremento
4. Si no existen datos de diciembre para algún año, se muestra mensaje de "Datos no disponibles"

#### Casos de Prueba

- **CP-2.1.1:** Para GDMTH, División Bajío, año 2024, el KPI muestra el total de dic-2024 vs dic-2023
- **CP-2.1.2:** La variación % se calcula como: ((total_dic_N / total_dic_N-1) - 1) * 100
- **CP-2.1.3:** Si total_dic_2023 = 1.00 y total_dic_2024 = 1.05, el delta muestra +5.0%

**Formato BDD:**

```gherkin
Dado que: El usuario ha seleccionado División "BAJÍO", Tarifa "GDMTH", Año 2024
Cuando: El sistema carga los datos
Entonces: Muestra una tarjeta con "Total Diciembre: $X.XX" y delta "+Y.Y%"
```

---

### ⏳ Historia de Usuario 2.2: Desglose de Variación por Componente

**Como:** Analista de costos  
**Quiero:** Ver cómo cada componente de la tarifa contribuyó a la variación total  
**Para poder:** Identificar qué conceptos tuvieron mayor impacto en el incremento

#### Criterios de Aceptación

1. Se muestra una tabla o gráfica de barras con los componentes: Generación, Transmisión, Distribución, CENACE, SCnMEM, Suministro, Capacidad
2. Para cada componente se muestra: valor año N, valor año N-1, variación absoluta, variación %
3. Los componentes se ordenan por impacto (mayor variación absoluta primero)
4. Se distinguen visualmente los componentes que subieron vs los que bajaron

#### Casos de Prueba

- **CP-2.2.1:** La suma de variaciones por componente coincide con la variación total
- **CP-2.2.2:** Para tarifas con cargo "Variable (Energía)", se muestran todos los componentes
- **CP-2.2.3:** Para tarifas con cargo "Capacidad", se muestran solo distribución, generación, capacidad

**Formato BDD:**

```gherkin
Dado que: El usuario visualiza el KPI de variación total
Cuando: Revisa la sección de desglose
Entonces: Ve una gráfica de barras mostrando el impacto de cada componente en la variación
```

---

### ⏳ Historia de Usuario 2.3: Gráfica Comparativa de Cierres

**Como:** Analista de costos  
**Quiero:** Ver una gráfica de barras comparando diciembre de ambos años  
**Para poder:** Visualizar fácilmente la diferencia entre periodos

#### Criterios de Aceptación

1. Se muestra gráfica de barras agrupadas: una barra para dic año N, otra para dic año N-1
2. El eje Y muestra el valor total en pesos
3. Se pueden comparar múltiples cargos (Fijo, Variable, Capacidad) si aplican
4. La gráfica usa colores distintivos para cada año

#### Casos de Prueba

- **CP-2.3.1:** Para tarifa GDMTH, se muestran 4 barras: Fijo, Variable-Base, Variable-Intermedia, Variable-Punta
- **CP-2.3.2:** Para tarifa PDBT, se muestran 2 barras: Fijo y Variable
- **CP-2.3.3:** La gráfica es interactiva (hover muestra valores exactos)

---

## FEATURE 3: Análisis de Promedio Anual e Inteligencia Horaria

### Descripción del Feature

- **Para:** Analista de costos y tomador de decisiones
- **Que:** Necesita entender el comportamiento promedio anual y por horarios
- **Esta épica:** Provee análisis de promedios y detección automática de estructura horaria
- **Esperamos:** Dar visibilidad al comportamiento real del costo a lo largo del año
- **Sabremos que hemos tenido éxito cuando:** La interfaz se adapte automáticamente si la tarifa tiene o no cargos horarios

---

### ⏳ Historia de Usuario 3.1: KPI de Promedio Anual

**Como:** Analista de costos  
**Quiero:** Ver el promedio mensual del año seleccionado vs el año anterior  
**Para poder:** Entender la tendencia general del costo energético

#### Criterios de Aceptación

1. Se calcula la media aritmética de todos los meses disponibles del año seleccionado
2. Se compara contra la media del mismo periodo del año anterior
3. Se muestra `st.metric` con el promedio y delta %
4. Si un año tiene menos meses disponibles, se comparan solo los meses coincidentes

#### Casos de Prueba

- **CP-3.1.1:** Si año 2024 tiene datos de ene-dic y 2023 igual, se promedian los 12 meses
- **CP-3.1.2:** Si año 2024 tiene datos de ene-sep, se compara contra ene-sep de 2023
- **CP-3.1.3:** El cálculo es: promedio_N = mean(total para todos los meses de año N)

**Formato BDD:**

```gherkin
Dado que: El usuario ha seleccionado una tarifa y año
Cuando: El sistema calcula métricas
Entonces: Muestra "Promedio Anual: $X.XX" con delta vs año anterior
```

---

### ⏳ Historia de Usuario 3.2: Detección Automática de Estructura Horaria

**Como:** Sistema  
**Quiero:** Identificar automáticamente si la tarifa seleccionada tiene cargos horarios  
**Para poder:** Adaptar la interfaz y mostrar desgloses por Base, Intermedia y Punta

#### Criterios de Aceptación

1. El sistema detecta valores en la columna `int_horario`: B (Base), I (Intermedia), P (Punta)
2. Si la tarifa tiene registros con B, I, P → se marca como "tarifa horaria"
3. Si la tarifa solo tiene "sin dato" en int_horario → se marca como "tarifa simple"
4. La detección ocurre automáticamente al seleccionar la tarifa

#### Casos de Prueba

- **CP-3.2.1:** Seleccionar "GDMTH" activa vista horaria (Base, Intermedia, Punta)
- **CP-3.2.2:** Seleccionar "PDBT" muestra vista simple (sin segmentación horaria)
- **CP-3.2.3:** Seleccionar "DIST" activa vista horaria (tiene B, I, P)

**Formato BDD:**

```gherkin
Dado que: El usuario selecciona tarifa "GDMTH"
Cuando: El sistema analiza la estructura de datos
Entonces: Identifica int_horario = [B, I, P] y activa modo "tarifa horaria"
```

---

### ⏳ Historia de Usuario 3.3: Vista Segmentada por Horario (Tarifas Horarias)

**Como:** Analista de tarifas horarias  
**Quiero:** Ver métricas separadas para Base, Intermedia y Punta  
**Para poder:** Identificar en qué periodo horario hay mayor impacto de costos

#### Criterios de Aceptación

1. Se muestran 3 columnas con `st.metric`: Base, Intermedia, Punta
2. Cada columna muestra el promedio del periodo y su variación vs año anterior
3. Se incluye una leyenda explicando los horarios típicos de cada periodo
4. Esta vista solo se muestra para tarifas identificadas como "horarias"

#### Casos de Prueba

- **CP-3.3.1:** Para GDMTH, se muestran 3 KPIs: Prom. Base, Prom. Intermedia, Prom. Punta
- **CP-3.3.2:** Cada KPI tiene su propio cálculo de variación independiente
- **CP-3.3.3:** Si un periodo no tiene datos, se muestra "N/A"

---

### ⏳ Historia de Usuario 3.4: Gráfica de Tendencia Mensual

**Como:** Analista de costos  
**Quiero:** Ver una gráfica de líneas con la evolución mensual de ambos años  
**Para poder:** Identificar patrones estacionales y anomalías

#### Criterios de Aceptación

1. Se muestra gráfica de líneas con eje X = meses (Ene-Dic), eje Y = valor total
2. Dos líneas: año seleccionado y año anterior
3. Las líneas usan colores distintivos con leyenda clara
4. Hover sobre puntos muestra mes y valor exacto

#### Casos de Prueba

- **CP-3.4.1:** La gráfica muestra 12 puntos por año (uno por mes)
- **CP-3.4.2:** Si un mes no tiene datos, la línea se interrumpe o muestra null
- **CP-3.4.3:** El orden de meses es cronológico: Enero → Diciembre

**Formato BDD:**

```gherkin
Dado que: El usuario ha seleccionado filtros completos
Cuando: Se renderiza la sección de análisis
Entonces: Ve una gráfica de líneas comparando tendencia mensual de ambos años
```

---

### ⏳ Historia de Usuario 3.5: Vista Consolidada para Tarifas Simples

**Como:** Usuario con tarifa simple (sin horarios)  
**Quiero:** Ver los datos agrupados sin segmentación horaria  
**Para poder:** Tener una vista limpia y sin información irrelevante

#### Criterios de Aceptación

1. Para tarifas sin horarios, se muestra solo: Cargo Fijo y Cargo Variable
2. No se muestran columnas de Base/Intermedia/Punta
3. Los KPIs muestran promedio general del cargo variable
4. La gráfica de tendencia muestra una sola línea por año (total)

#### Casos de Prueba

- **CP-3.5.1:** Para tarifa PDBT, la interfaz no muestra sección de "Análisis por Horario"
- **CP-3.5.2:** Solo se muestran 2 KPIs: Cargo Fijo Promedio, Cargo Variable Promedio
- **CP-3.5.3:** La gráfica de tendencia usa el valor `total` sin desagregar

---

## Resumen de Historias

| Feature | HU | Título | Estado |
|---------|-----|--------|--------|
| 0 | 0.1 | Configuración del Entorno de Desarrollo | ✅ |
| 0 | 0.2 | Carga y Gestión de Datos desde CSV | ✅ |
| 1 | 1.1 | Selector de Estado | ✅ |
| 1 | 1.2 | Selector de Municipio con Mapeo a División | ✅ |
| 1 | 1.3 | Selector Dinámico de Tarifas | ✅ |
| 1 | 1.4 | Selector de Año de Análisis | ⏳ |
| 2 | 2.1 | KPI de Variación Total Diciembre | ⏳ |
| 2 | 2.2 | Desglose de Variación por Componente | ⏳ |
| 2 | 2.3 | Gráfica Comparativa de Cierres | ⏳ |
| 3 | 3.1 | KPI de Promedio Anual | ⏳ |
| 3 | 3.2 | Detección Automática de Estructura Horaria | ⏳ |
| 3 | 3.3 | Vista Segmentada por Horario | ⏳ |
| 3 | 3.4 | Gráfica de Tendencia Mensual | ⏳ |
| 3 | 3.5 | Vista Consolidada para Tarifas Simples | ⏳ |

**Total:** 14 Historias de Usuario en 4 Features
