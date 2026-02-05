Comando: @generate-story-cards [FEATURE_NUM]

"Cuando te pida ejecutar este comando (ej: @generate-story-cards o @generate-story-cards 1), realiza las siguientes acciones en orden:

**1. Leer BACKLOG.md:**
- Lee el archivo completo `.spec/BACKLOG.md`.
- Si se proporciona un número de Feature (ej: `1`), filtra solo ese Feature. Si no, procesa todos los Features.

**2. Identificar Features e Historias:**
- Encuentra todas las secciones `## FEATURE X:` y extrae el número y nombre de cada Feature.
- Para cada Feature, encuentra todas las Historias de Usuario con patrón `### [estado] Historia de Usuario X.Y:`.
- Extrae para cada Historia:
  - Número de Feature (X) y número de Historia (Y) → HU-X.Y
  - Estado (⏳, 🔄, ✅)
  - Título completo
  - Sección **Como:** (rol del usuario)
  - Sección **Quiero:** (acción deseada)
  - Sección **Para poder:** (beneficio/objetivo)
  - Sección **Criterios de Aceptación:** (lista completa)
  - Sección **Casos de Prueba:** (si existe)

**3. Para cada Historia de Usuario encontrada:**

**a. Verificar si ya existe story-card:**
- Busca en `.spec/story-cards/` si existe un archivo `HU-X.Y-[slug].md`.
- Si existe, omite esta historia y continúa con la siguiente.
- Si no existe, procede a generarla.

**b. Generar nombre de archivo:**
- Crea un slug desde el título de la historia:
  - Convertir a minúsculas
  - Reemplazar caracteres especiales (á→a, é→e, ñ→n, etc.)
  - Reemplazar espacios y caracteres no alfanuméricos con guiones
  - Limitar a 50 caracteres
- Formato: `HU-X.Y-[slug].md`
- Ejemplo: `HU-1.2-selector-de-estado-y-municipio.md`

**c. Generar Objetivo de la Sesión:**
- Formato: "Implementar [Título]. [Quiero] [Para poder]"
- Ejemplo: "Implementar Selector de Estado y Municipio. Seleccionar mi ubicación geográfica para ver tarifas de mi división CFE"

**d. Generar Tareas (Current Objective):**
- Convertir cada criterio de aceptación en una tarea.
- Formato: `- [ ] [texto del criterio]`
- Si no hay criterios claros, usar: "- [ ] Implementar funcionalidad según criterios de aceptación"

**e. Generar Prompt para Cursor:**
- Crear un prompt inteligente que incluya:
  - Referencia a @.spec/BACKLOG.md (HU X.Y)
  - Referencia a @.spec/TECH_SPEC.md
  - Contexto del Feature (nombre completo)
  - Historia de Usuario completa (Como/Quiero/Para poder)
  - Lista de Criterios de Aceptación
  - Requisitos Técnicos:
    - Stack: Python 3.10+ (Streamlit), Pandas para ETL, Plotly Express para gráficas, Supabase (PostgreSQL)
    - Diseño Dashboard-first con enfoque en métricas y KPIs
    - Componentes Streamlit: st.selectbox, st.metric, st.columns, st.plotly_chart
    - Datos en `data/` (CSVs de catálogo y tarifas)
  - Instrucciones de implementación:
    1. Revisar criterios de aceptación y casos de prueba en BACKLOG.md
    2. Implementar siguiendo patrones de Streamlit
    3. Cumplir validaciones y reglas de negocio
    4. Mantener consistencia con código existente
    5. Consultar @.spec/PRD.md y @.spec/TECH_SPEC.md si hay dudas

**f. Generar Pruebas de Aceptación:**
- Combinar Criterios de Aceptación y Casos de Prueba.
- Si no hay casos de prueba, usar solo los criterios.
- Si no hay ninguno, usar: "Verificar que se cumplen todos los criterios de aceptación"

**4. Escribir Story Card:**
- Crear archivo en `.spec/story-cards/HU-X.Y-[slug].md`.
- Estructura del archivo:
  ```markdown
  # Historia X.Y: [Título]
  
  ## 🎯 Objetivo de la Sesión
  [Objetivo generado]
  
  ## 📝 Current Objective (Copiar a current_objective.md)
  [Lista de tareas]
  
  ## 🤖 Prompt para Cursor (Composer)
  [Prompt generado]
  
  ## 🧪 Pruebas de Aceptación
  [Criterios y casos de prueba]
  ```

**5. Resumen Final:**
- Mostrar estadísticas:
  - Total de historias procesadas
  - Story-cards generadas (nuevas)
  - Story-cards omitidas (ya existían)
  - Si se filtró por Feature, indicar cuál

**Notas importantes:**
- NO sobrescribir story-cards existentes. Si ya existe, omitir y continuar.
- Los prompts deben ser contextualizados y específicos para cada historia.
- Mantener consistencia con el formato de story-cards existentes.
- Si una historia no tiene todos los campos (Como/Quiero/Para poder), usar los disponibles.
- El slug debe ser legible pero conciso (máximo 50 caracteres)."
