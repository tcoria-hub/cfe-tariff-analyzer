# BACKLOG - CFE Tariff Analyzer MVP

> **Última actualización:** 2026-02-20
> **Versión:** 1.0.0

## Estado del Proyecto

- ⏳ Feature 0: Configuración Inicial y ETL
- ✅ Feature 1: Selector Geográfico y de Tarifas
- ✅ Feature 2: Comparativo Diciembre vs Diciembre
- ✅ Feature 3: Análisis de Promedio Anual e Inteligencia Horaria
- ⏳ Feature 4: Operación y Mantenimiento
- ✅ Feature 5: Histórico de Tarifas por Rango de 12 Meses
- ⏳ Feature 6: Captura Manual y Exportación de Recibos de Luz CFE

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

### ✅ Historia de Usuario 1.4: Selector de Año de Análisis

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

### ✅ Historia de Usuario 1.5: Descripción Completa de Tarifa Seleccionada

**Como:** Usuario de la aplicación  
**Quiero:** Ver la descripción completa de la tarifa que he seleccionado  
**Para poder:** Entender claramente qué tipo de tarifa estoy analizando sin memorizar códigos

#### Criterios de Aceptación

1. Al seleccionar una tarifa, se muestra su descripción completa encima de "Resumen de Tarifas"
2. La descripción incluye el nombre completo de la tarifa (ej: "Gran demanda baja tensión")
3. La descripción se actualiza dinámicamente al cambiar la tarifa seleccionada
4. Si no hay tarifa seleccionada, no se muestra descripción
5. El formato visual es claro y destacado (ej: texto en negrita o con estilo informativo)

#### Casos de Prueba

- **CP-1.5.1:** Al seleccionar "GDBT", se muestra "Gran demanda baja tensión" arriba de "Resumen de Tarifas"
- **CP-1.5.2:** Al seleccionar "GDMTH", se muestra "Gran demanda en media tensión horaria"
- **CP-1.5.3:** Al seleccionar "PDBT", se muestra "Pequeña demanda baja tensión"
- **CP-1.5.4:** Al cambiar de tarifa, la descripción se actualiza inmediatamente

**Formato BDD:**

```gherkin
Dado que: El usuario ha seleccionado Estado, Municipio, Año y una Tarifa
Cuando: La pantalla de análisis se renderiza
Entonces: Muestra la descripción completa de la tarifa (ej: "Gran demanda baja tensión") 
Y: La descripción aparece arriba de la sección "Resumen de Tarifas"
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

### ✅ Historia de Usuario 2.1: KPI de Variación Total Diciembre

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

### ✅ Historia de Usuario 2.2: Desglose de Variación por Componente

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

### ✅ Historia de Usuario 2.3: Gráfica Comparativa de Cierres

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

### ✅ Historia de Usuario 3.1: KPI de Promedio Anual

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

### ✅ Historia de Usuario 3.2: Detección Automática de Estructura Horaria

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

### ✅ Historia de Usuario 3.3: Vista Segmentada por Horario (Tarifas Horarias)

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

### ✅ Historia de Usuario 3.4: Gráfica de Tendencia Mensual

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

### ✅ Historia de Usuario 3.5: Vista Consolidada para Tarifas Simples

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

---

## Feature 4: Operación y Mantenimiento ⏳

> **Objetivo:** Permitir la actualización mensual de datos y facilitar la operación continua de la aplicación.

### Historia de Usuario 4.1: Validación y Preview de CSV

**Como:** Administrador del sistema  
**Quiero:** Subir un archivo CSV y validar su formato antes de actualizar  
**Para poder:** Verificar que los datos son correctos antes de cualquier cambio

#### Criterios de Aceptación

1. Existe una sección en el sidebar para "Actualizar Datos"
2. El usuario puede subir un CSV con `st.file_uploader`
3. El sistema valida que el CSV tenga las columnas requeridas
4. Se muestra mensaje de error claro si faltan columnas o hay problemas de formato
5. Si es válido, se muestra preview con:
   - Cantidad de registros
   - Rango de fechas (años/meses)
   - Primeras 10 filas
6. Se muestra botón "Confirmar" (preparación para HU-4.2)

#### Casos de Prueba

- **CP-4.1.1:** Subir CSV válido muestra preview con estadísticas y primeras filas
- **CP-4.1.2:** Subir CSV con columnas faltantes muestra error: "Faltan columnas: X, Y"
- **CP-4.1.3:** Subir archivo no-CSV muestra error de formato
- **CP-4.1.4:** El botón "Confirmar" muestra mensaje informativo (sin persistencia aún)

**Formato BDD:**

```gherkin
Dado que: El administrador accede a la sección de carga de datos
Cuando: Sube un archivo CSV
Entonces: El sistema valida el formato y columnas
Y: Si es válido, muestra preview con estadísticas y datos de muestra
Y: Si es inválido, muestra mensaje de error descriptivo
```

#### Notas Técnicas

- Usar `st.file_uploader(type=['csv'])` 
- Columnas requeridas: `anio`, `mes`, `tarifa`, `region`, `total`
- Usar `st.expander` para la sección de carga (no interferir con UI principal)
- Esta historia NO persiste datos - solo valida y muestra preview

---

### Historia de Usuario 4.2: Persistencia de Datos via GitHub

**Como:** Administrador del sistema  
**Quiero:** Que los datos validados se guarden permanentemente  
**Para poder:** Actualizar la información mensualmente sin acceso al código

**Dependencia:** Requiere HU-4.1 completada

#### Criterios de Aceptación

1. Al confirmar la carga, los datos se guardan en el repositorio GitHub
2. Se usa la API de GitHub para crear un commit automático
3. El commit incluye mensaje descriptivo: "Actualización de tarifas - [fecha]"
4. Se muestra confirmación con:
   - Cantidad de registros agregados
   - Link al commit en GitHub
   - Aviso de re-deploy automático (~2 min)
5. El token de GitHub se almacena de forma segura en Streamlit Secrets

#### Casos de Prueba

- **CP-4.2.1:** Confirmar carga crea commit en GitHub con el CSV actualizado
- **CP-4.2.2:** Sin token configurado, muestra mensaje de error apropiado
- **CP-4.2.3:** Error de API muestra mensaje descriptivo y permite reintentar
- **CP-4.2.4:** Después del re-deploy, los nuevos datos aparecen en la app

**Formato BDD:**

```gherkin
Dado que: El administrador ha validado un CSV (HU-4.1)
Cuando: Hace click en "Confirmar Actualización"
Entonces: El sistema crea un commit en GitHub con los nuevos datos
Y: Muestra confirmación con link al commit
Y: Streamlit Cloud inicia re-deploy automático
```

#### Notas Técnicas

- Usar `PyGithub` o `requests` para la API de GitHub
- Token requiere scope `repo` (lectura/escritura)
- Almacenar token en `st.secrets["GITHUB_TOKEN"]`
- Agregar `PyGithub` a requirements.txt
- El archivo destino es `data/02_tarifas_finales_suministro_basico.csv`

#### Configuración Requerida

1. Crear Personal Access Token en GitHub (Settings > Developer settings > Tokens)
2. Agregar a Streamlit Cloud: Settings > Secrets > `GITHUB_TOKEN = "ghp_xxx..."`

---

### Historia de Usuario 4.3: Gestión de Catálogo de Regiones

**Como:** Administrador del sistema  
**Quiero:** Actualizar el catálogo de municipios y divisiones CFE  
**Para poder:** Agregar nuevos municipios o corregir mapeos incorrectos

#### Criterios de Aceptación

1. Se puede subir un CSV con el catálogo de regiones actualizado
2. El sistema valida formato y columnas requeridas
3. Se muestra comparativo de cambios antes de aplicar
4. Los cambios se persisten via GitHub (reutiliza lógica de HU-4.2)

**Prioridad:** Baja (el catálogo de regiones cambia con poca frecuencia)

---

## FEATURE 5: Histórico de Tarifas por Rango de 12 Meses ✅

### Descripción del Feature

- **Para:** Analista de costos energéticos y usuario final
- **Que:** Necesita consultar el histórico detallado de una tarifa específica en un rango de 12 meses
- **Esta épica:** Provee una vista tabular completa con todos los datos mensuales ordenados cronológicamente
- **Esperamos:** Que el usuario pueda ver la evolución mes a mes de todos los componentes tarifarios en un periodo específico
- **Sabremos que hemos tenido éxito cuando:** El usuario pueda exportar o consultar fácilmente el histórico completo con todos los detalles por mes

---

### ✅ Historia de Usuario 5.1: Tabla Histórica de Tarifas por Rango de 12 Meses

**Como:** Analista de costos energéticos  
**Quiero:** Ver una tabla con el histórico completo de una tarifa y división en un rango de 12 meses calculado desde un mes final seleccionado  
**Para poder:** Analizar la evolución mes a mes de todos los componentes tarifarios en un periodo específico

#### Criterios de Aceptación

1. Se muestra un selector de "Mes Final del Rango" que permite elegir cualquier mes del año seleccionado (enero a diciembre)
2. Al seleccionar un mes final (ej: diciembre 2024), el sistema calcula automáticamente el rango de 12 meses hacia atrás desde ese mes:
   - Si el mes final es diciembre 2024, el rango es enero 2024 - diciembre 2024 (12 meses)
   - Si el mes final es junio 2024, el rango es julio 2023 - junio 2024 (12 meses)
3. **Caso borde - Mes posterior al último disponible:** Si el mes/año seleccionado es posterior al último mes disponible en los datos para esa tarifa+división, el sistema:
   - Detecta automáticamente el último mes disponible
   - Calcula el rango de 12 meses terminando en ese último mes disponible
   - Muestra un mensaje informativo: "Último mes disponible: [mes] [año]. Mostrando histórico de 12 meses hasta esa fecha."
4. **Caso borde - Mes anterior al primero disponible:** Si el mes/año seleccionado es anterior al primer mes disponible en los datos para esa tarifa+división, el sistema:
   - Detecta automáticamente el primer mes disponible
   - Calcula el rango de 12 meses comenzando desde ese primer mes disponible
   - Muestra un mensaje informativo: "Primer mes disponible: [mes] [año]. Mostrando histórico de 12 meses desde esa fecha."
5. Si hay menos de 12 meses disponibles en total, se muestran todos los meses disponibles con un mensaje indicando el rango real
6. Se muestra una tabla ordenada cronológicamente (mes inicial → mes final) con las siguientes columnas:
   - Mes (nombre completo: enero, febrero, etc.)
   - Año
   - Cargo (Fijo, Variable (Energía), Capacidad)
   - Intervalo Horario (si aplica: Base, Intermedia, Punta, o "sin dato")
   - Componentes: Generación, Transmisión, Distribución, CENACE, SCnMEM, Suministro, Capacidad
   - Total
   - Unidades
7. Para tarifas horarias, se muestran filas separadas por cada intervalo horario (Base, Intermedia, Punta) por mes
8. Para tarifas simples, se muestran solo las filas correspondientes (sin segmentación horaria)
9. La tabla es interactiva y permite ordenar por cualquier columna haciendo clic en el encabezado
10. Se muestra el total de registros en el rango seleccionado y el rango de fechas calculado
11. Si algún mes dentro del rango no tiene datos disponibles, se muestra claramente (fila vacía o mensaje)
12. **Exportación a CSV:** Existe un botón "Descargar CSV" que exporta exactamente las filas mostradas en la tabla con todas las columnas, con nombre de archivo: `historico_[tarifa]_[division]_[mes_inicial]_[mes_final].csv`

#### Casos de Prueba

- **CP-5.1.1:** Seleccionar GDMTH, División Baja California, Año 2024, Mes Final: Diciembre → muestra tabla con 12 meses (enero-diciembre 2024), cada mes con 3 filas (Base, Intermedia, Punta) = 36 filas totales
- **CP-5.1.2:** Seleccionar PDBT, División Bajío, Año 2024, Mes Final: Junio → muestra tabla con 12 meses (julio 2023 - junio 2024), cada mes con 2 filas (Fijo, Variable) = 24 filas totales
- **CP-5.1.3:** Seleccionar mes final "Marzo 2024" muestra 12 meses (abril 2023 - marzo 2024)
- **CP-5.1.4:** Si el último mes disponible es septiembre 2024 y el usuario selecciona diciembre 2024, el sistema muestra: "Último mes disponible: septiembre 2024. Mostrando histórico de 12 meses hasta esa fecha." y calcula octubre 2023 - septiembre 2024
- **CP-5.1.5:** Si el primer mes disponible es marzo 2023 y el usuario selecciona enero 2023, el sistema muestra: "Primer mes disponible: marzo 2023. Mostrando histórico de 12 meses desde esa fecha." y calcula marzo 2023 - febrero 2024
- **CP-5.1.6:** Si solo hay 8 meses disponibles (ej: marzo-octubre 2024), se muestran esos 8 meses con mensaje: "Rango disponible: marzo 2024 - octubre 2024 (8 meses)"
- **CP-5.1.7:** La tabla permite ordenar por columna "Total" para identificar el mes con mayor costo
- **CP-5.1.8:** La tabla muestra correctamente los nombres de meses en español (enero, febrero, marzo, etc.)
- **CP-5.1.9:** Al hacer clic en "Descargar CSV", se descarga un archivo con todas las filas de la tabla visible, formato CSV con encoding UTF-8
- **CP-5.1.10:** El nombre del archivo CSV descargado sigue el formato: `historico_GDMTH_BAJA_CALIFORNIA_enero2024_diciembre2024.csv`

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

#### Notas Técnicas

- Usar `st.selectbox` para el selector de mes final con opciones: enero, febrero, marzo, abril, mayo, junio, julio, agosto, septiembre, octubre, noviembre, diciembre
- Crear función helper `mes_a_numero(mes_nombre: str) -> int` para convertir nombre de mes a número (1-12)
- Crear función helper `calcular_rango_12_meses(mes_final: int, año: int, df_tarifas: pd.DataFrame, tarifa: str, division: str) -> tuple` que:
  - Detecta el primer y último mes disponible para la tarifa+división
  - Aplica lógica de casos borde
  - Retorna (mes_inicial, año_inicial, mes_final_ajustado, año_final_ajustado, mensaje_info)
- Usar `st.dataframe` con `use_container_width=True` para la tabla interactiva
- Filtrar datos con: `(df.anio >= año_inicial) & (df.anio <= año_final_ajustado) & (df.mes_numero >= mes_inicial) & (df.mes_numero <= mes_final_ajustado) & (df.region == division) & (df.tarifa == tarifa_seleccionada)`
- Ordenar por: `anio`, `mes_numero`, `cargo`, `int_horario` (si aplica)
- Usar `st.download_button` con `df.to_csv(index=False, encoding='utf-8')` para exportar CSV
- El nombre del archivo debe generarse dinámicamente: `f"historico_{tarifa}_{division}_{mes_inicial_nombre}{año_inicial}_{mes_final_nombre}{año_final}.csv"`
- Manejar casos donde no hay datos para algún mes mostrando mensaje informativo con `st.info()` o `st.warning()`

---

### ✅ Historia de Usuario 5.2: Navegación entre Modos de Análisis

**Como:** Usuario de la aplicación  
**Quiero:** Poder navegar entre diferentes modos de análisis (generar histórico, análisis de comportamiento, captura de datos)  
**Para poder:** Acceder a cada funcionalidad de forma organizada y sin confusión

#### Criterios de Aceptación

1. Se implementa un sistema de navegación que permite cambiar entre diferentes vistas/modos de la aplicación
2. Los modos disponibles son:
   - **"Generar Histórico"** - Vista del Feature 5 (tabla histórica de 12 meses)
   - **"Análisis de Comportamiento"** - Vista existente con gráficas comparativas (Features 2 y 3)
   - **"Captura de Datos de Recibo"** - Vista del Feature 6 (a implementar)
3. La navegación se implementa usando `st.tabs()` o `st.sidebar.radio()` para seleccionar el modo activo
4. Al cambiar de modo, solo se muestra el contenido correspondiente a ese modo (las otras vistas se ocultan)
5. El estado de los selectores (Estado, Municipio, Tarifa, Año) se mantiene entre modos cuando es aplicable
6. La navegación es clara y visible, con iconos o etiquetas descriptivas para cada modo
7. El modo activo se indica visualmente (ej: tab seleccionado o radio button marcado)

#### Casos de Prueba

- **CP-5.2.1:** Al iniciar la aplicación, se muestra el modo "Análisis de Comportamiento" por defecto (vista existente)
- **CP-5.2.2:** Al hacer clic en el tab "Generar Histórico", se oculta la vista de análisis y se muestra la vista del histórico
- **CP-5.2.3:** Al hacer clic en el tab "Análisis de Comportamiento", se oculta la vista del histórico y se muestra la vista de análisis existente
- **CP-5.2.4:** Si el usuario selecciona Estado/Municipio/Tarifa en un modo, al cambiar a otro modo, esos selectores mantienen su valor (si aplican)
- **CP-5.2.5:** El tab "Captura de Datos de Recibo" está visible pero muestra mensaje "Próximamente" o contenido del Feature 6 cuando esté implementado
- **CP-5.2.6:** La navegación funciona correctamente en dispositivos móviles (responsive)

**Formato BDD:**

```gherkin
Dado que: El usuario está en la aplicación
Cuando: Ve la interfaz principal
Entonces: Ve un sistema de navegación con tabs o radio buttons para seleccionar modo
Y: Los modos disponibles son: "Generar Histórico", "Análisis de Comportamiento", "Captura de Datos de Recibo"

Escenario: Cambiar entre modos
Dado que: El usuario está en el modo "Análisis de Comportamiento"
Cuando: Hace clic en el tab "Generar Histórico"
Entonces: Se oculta la vista de análisis de comportamiento
Y: Se muestra la vista del histórico de 12 meses
Y: Los selectores de Estado/Municipio/Tarifa mantienen sus valores si aplican
```

#### Notas Técnicas

- Usar `st.tabs()` para navegación horizontal en la parte superior, o `st.sidebar.radio()` para navegación en el sidebar
- Estructura recomendada:
  ```python
  modo = st.tabs(["📊 Análisis de Comportamiento", "📋 Generar Histórico", "📥 Captura de Datos"])
  with modo[0]:
      # Vista existente (Features 2 y 3)
  with modo[1]:
      # Vista Feature 5 (histórico)
  with modo[2]:
      # Vista Feature 6 (captura) - placeholder por ahora
  ```
- Mantener los selectores comunes (Estado, Municipio, Tarifa, Año) fuera de los tabs para que sean accesibles desde cualquier modo
- Usar `st.session_state` para mantener el estado de selecciones entre cambios de modo
- Considerar usar iconos de emoji o de biblioteca como `streamlit-option-menu` para mejor UX
- El modo por defecto debe ser "Análisis de Comportamiento" para mantener compatibilidad con usuarios existentes

---

## FEATURE 6: Captura Manual y Exportación de Recibos de Luz CFE

### Descripción del Feature

- **Para:** Usuario capturista y analista
- **Que:** Necesita capturar manualmente la información de recibos de luz CFE y exportar el histórico completo
- **Esta épica:** Permite captura por bloques con campos dinámicos según tarifa, almacenamiento inmutable y exportación a CSV
- **Esperamos:** Que los recibos queden guardados de forma definitiva y se pueda exportar todo el histórico a CSV para análisis externo
- **Sabremos que hemos tenido éxito cuando:** Se puedan capturar recibos de distintas tarifas sin conflicto, sin edición/eliminación posterior, y la exportación incluya todos los registros con campos no aplicables vacíos

**Alcance:** Incluye captura manual por bloques, activación dinámica de campos según tarifa, validaciones mínimas, almacenamiento inmutable y exportación completa a CSV. Excluye consulta visual del histórico, edición/eliminación, cálculos automáticos y OCR.

**Notas de arquitectura (2026-02-20):**
- **Persistencia:** CSV en repositorio (ej. `data/recibos_capturados.csv`) actualizado vía API de GitHub (alineado con HU-4.2).
- **Esquemas por tarifa:** Se construyen bajo demanda: al guardar el primer recibo de una tarifa se deriva y persiste el esquema de campos para esa tarifa; recibos posteriores usan ese formulario.

---

### Epic 6.1 – Captura y Almacenamiento del Recibo

### ✅ Historia de Usuario 6.1: Captura de datos generales del recibo

**Como:** Usuario capturista  
**Quiero:** Registrar los datos generales del recibo  
**Para poder:** Identificar de forma única el suministro y el periodo facturado

#### Criterios de Aceptación

1. Los datos generales se capturan en un bloque inicial
2. La tarifa es obligatoria
3. El número de servicio es obligatorio
4. El periodo facturado es obligatorio
5. No se permite avanzar si falta algún dato obligatorio

#### Casos de Prueba

- **CP-6.1.1:** Sin tarifa seleccionada no se puede continuar al bloque de datos variables
- **CP-6.1.2:** Sin número de servicio no se habilita el botón Guardar
- **CP-6.1.3:** Sin periodo facturado no se permite guardar

---

### ⏳ Historia de Usuario 6.2: Activación dinámica de campos por esquema tarifario

**Como:** Usuario capturista  
**Quiero:** Que el sistema muestre únicamente los campos correspondientes a la tarifa seleccionada  
**Para poder:** Evitar capturar información que no existe en el recibo

#### Criterios de Aceptación

1. Al seleccionar una tarifa, se habilita exclusivamente su bloque de campos
2. Los campos de otras tarifas no son visibles
3. Si se cambia la tarifa antes de guardar, los campos previamente capturados se reinician
4. Cada tarifa define su propio conjunto de campos obligatorios (esquemas construidos bajo demanda)

#### Casos de Prueba

- **CP-6.2.1:** Seleccionar PDBT muestra solo los campos definidos para PDBT
- **CP-6.2.2:** Cambiar de PDBT a GDMTH antes de guardar limpia los campos variables y muestra los de GDMTH
- **CP-6.2.3:** Primera vez que se usa una tarifa: se permite definir campos al capturar y se persiste el esquema

---

### ⏳ Historia de Usuario 6.3: Captura de datos variables según la tarifa

**Como:** Usuario capturista  
**Quiero:** Ingresar los datos específicos del esquema tarifario  
**Para poder:** Reflejar fielmente la información del recibo físico

#### Criterios de Aceptación

1. Todos los campos obligatorios del esquema deben completarse
2. Los campos numéricos solo aceptan valores numéricos
3. Los campos monetarios permiten hasta dos decimales
4. El sistema no realiza cálculos automáticos

#### Casos de Prueba

- **CP-6.3.1:** Campo numérico rechaza texto y muestra error
- **CP-6.3.2:** Campo monetario acepta máximo 2 decimales
- **CP-6.3.3:** No hay cálculo automático de totales ni derivados

---

### ⏳ Historia de Usuario 6.4: Validaciones mínimas antes del guardado

**Como:** Usuario capturista  
**Quiero:** Que el sistema valide la información básica  
**Para poder:** Asegurar consistencia en los datos almacenados

#### Criterios de Aceptación

1. No se permite guardar si existen campos obligatorios vacíos
2. No se aceptan valores negativos
3. El factor de potencia (cuando aplique) debe estar entre 0 y 1
4. Los mensajes de error son claros y por campo

#### Casos de Prueba

- **CP-6.4.1:** Guardar con campo obligatorio vacío muestra error en ese campo
- **CP-6.4.2:** Valor negativo en campo numérico muestra error
- **CP-6.4.3:** Factor de potencia &gt; 1 o &lt; 0 muestra error

---

### ⏳ Historia de Usuario 6.5: Guardado definitivo e inmutable del recibo

**Como:** Usuario capturista  
**Quiero:** Guardar el recibo de forma definitiva  
**Para poder:** Preservar la integridad del histórico

#### Criterios de Aceptación

1. Al guardar, el registro queda almacenado como inmutable
2. No existe opción de edición posterior
3. No existe opción de eliminación
4. Se registra fecha y hora de captura
5. El sistema confirma explícitamente el guardado exitoso

#### Casos de Prueba

- **CP-6.5.1:** Tras guardar se muestra mensaje de confirmación
- **CP-6.5.2:** No hay botón ni flujo para editar o eliminar un recibo guardado
- **CP-6.5.3:** Cada registro incluye timestamp de captura

#### Notas Técnicas

- Persistencia: CSV en repo (`data/recibos_capturados.csv`) vía API de GitHub (reutilizar o extender lógica de HU-4.2)
- Esquemas por tarifa: archivo en repo (ej. `data/04_esquemas_recibo_por_tarifa.json`) que se actualiza bajo demanda al guardar el primer recibo de cada tarifa

---

### Epic 6.2 – Exportación del Histórico

### ⏳ Historia de Usuario 6.6: Exportación completa del histórico a CSV

**Como:** Analista  
**Quiero:** Exportar todos los recibos capturados a un archivo CSV  
**Para poder:** Analizarlos en herramientas externas

**Consideración funcional:** Los recibos no comparten todos los mismos campos; la estructura depende de la tarifa.

#### Criterios de Aceptación

1. El CSV incluye todas las columnas de datos generales
2. El CSV incluye todas las columnas posibles de datos tarifarios (unión de esquemas)
3. Para cada recibo, los campos no aplicables se exportan como valores vacíos
4. El archivo contiene la totalidad de los registros almacenados
5. El formato es compatible con Excel (UTF-8, separador estándar)
6. La exportación no altera la información original

#### Casos de Prueba

- **CP-6.6.1:** Exportar con 0 recibos genera CSV con solo encabezados o mensaje apropiado
- **CP-6.6.2:** Exportar con recibos de varias tarifas genera columnas para todos los campos; celdas no aplicables vacías
- **CP-6.6.3:** El CSV abre correctamente en Excel con caracteres correctos

---

### Reglas Globales del Feature 6

| Regla | Definición |
|-------|------------|
| Captura | 100% manual |
| Estructura de datos | Variable según tarifa (esquemas bajo demanda) |
| Edición posterior | No permitida |
| Eliminación de registros | No permitida |
| Exportación | Histórico completo |
| Formato de salida | CSV |

### Definición de Hecho (DoD)

- Se pueden capturar recibos de distintas tarifas sin conflicto
- Ningún recibo puede modificarse después de guardarse
- La exportación a CSV incluye todos los registros
- Los campos no aplicables se exportan vacíos
- El Feature 6 cumple su objetivo sin dependencias funcionales adicionales

---

## Resumen de Historias

| Feature | HU | Título | Estado |
|---------|-----|--------|--------|
| 0 | 0.1 | Configuración del Entorno de Desarrollo | ✅ |
| 0 | 0.2 | Carga y Gestión de Datos desde CSV | ✅ |
| 1 | 1.1 | Selector de Estado | ✅ |
| 1 | 1.2 | Selector de Municipio con Mapeo a División | ✅ |
| 1 | 1.3 | Selector Dinámico de Tarifas | ✅ |
| 1 | 1.4 | Selector de Año de Análisis | ✅ |
| 1 | 1.5 | Descripción Completa de Tarifa Seleccionada | ✅ |
| 2 | 2.1 | KPI de Variación Total Diciembre | ✅ |
| 2 | 2.2 | Desglose de Variación por Componente | ✅ |
| 2 | 2.3 | Gráfica Comparativa de Cierres | ✅ |
| 3 | 3.1 | KPI de Promedio Anual | ✅ |
| 3 | 3.2 | Detección Automática de Estructura Horaria | ✅ |
| 3 | 3.3 | Vista Segmentada por Horario | ✅ |
| 3 | 3.4 | Gráfica de Tendencia Mensual | ✅ |
| 3 | 3.5 | Vista Consolidada para Tarifas Simples | ✅ |
| 4 | 4.1 | Validación y Preview de CSV | ⏳ |
| 4 | 4.2 | Persistencia de Datos via GitHub | ⏳ |
| 4 | 4.3 | Gestión de Catálogo de Regiones | ⏳ |
| 5 | 5.1 | Tabla Histórica de Tarifas por Rango de 12 Meses | 🔄 |
| 5 | 5.2 | Navegación entre Modos de Análisis | ✅ |
| 6 | 6.1 | Captura de datos generales del recibo | ✅ |
| 6 | 6.2 | Activación dinámica de campos por esquema tarifario | ⏳ |
| 6 | 6.3 | Captura de datos variables según la tarifa | ⏳ |
| 6 | 6.4 | Validaciones mínimas antes del guardado | ⏳ |
| 6 | 6.5 | Guardado definitivo e inmutable del recibo | ⏳ |
| 6 | 6.6 | Exportación completa del histórico a CSV | ⏳ |

**Total:** 26 Historias de Usuario en 7 Features
