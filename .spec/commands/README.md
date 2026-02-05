# Comandos de Workflow - CFE Tariff Analyzer

Comandos auxiliares para gestionar el flujo de trabajo con historias de usuario.

> **Nota:** Estos son comandos que se ejecutan con prompts en Cursor, no scripts de shell. Cada comando tiene un archivo `.md` con instrucciones detalladas.

## Comandos Disponibles

### `@start-objective [HU-X.X]`

Inicia trabajo en una Historia de Usuario leyendo la story-card y generando `current_objective.md`.

**Uso:**
```
@start-objective HU-1.2
@start-objective HU-1.2-selector-geografico
@start-objective 1.2
```

**Instrucciones:** Ver `start_objective.md`

**Qué hace:**
1. Busca y lee la story-card correspondiente
2. Extrae: objetivo, tareas, prompt, pruebas de aceptación
3. Busca información del Feature en BACKLOG.md
4. Genera `current_objective.md` con el template mejorado
5. Incluye referencias a BACKLOG.md, spec.md
6. Opcionalmente actualiza el estado en BACKLOG.md a 🔄 En progreso

### `@generate-story-cards [FEATURE_NUM]`

Genera story-cards desde BACKLOG.md para todas las historias de usuario.

**Uso:**
```
@generate-story-cards          # Genera todas las historias
@generate-story-cards 1       # Solo Feature 1
@generate-story-cards 2       # Solo Feature 2
```

**Instrucciones:** Ver `generate_story_cards.md`

**Qué hace:**
1. Lee BACKLOG.md y encuentra todas las Features e Historias
2. Para cada Historia extrae: Como/Quiero/Para poder, Criterios, Casos de prueba
3. Genera un prompt inteligente contextualizado
4. Crea story-card en `.spec/story-cards/HU-X.Y-[slug].md`
5. NO sobrescribe story-cards existentes (las omite)

### `@finish-objective`

Comando para finalizar un objetivo completado.

**Uso:**
```
@finish-objective
```

**Instrucciones:** Ver `finish_objective.md`

**Qué hace:**
1. Marca todas las tareas en `current_objective.md` como completadas
2. Archiva el contenido en `.spec/history/`
3. Actualiza BACKLOG.md marcando la historia como ✅ (Completada)
4. Actualiza CHANGELOG.md
5. Prepara commit
6. Resetea `current_objective.md` para el próximo objetivo

## Estados en BACKLOG.md

Las historias de usuario tienen estados visuales:

- **⏳ Pendiente** - Aún no iniciada
- **🔄 En progreso** - Actualmente en trabajo
- **✅ Completada** - Finalizada

## Workflow Recomendado

### 1. Generar Story Cards (si no existen)

```
@generate-story-cards
```

Esto genera todas las story-cards desde BACKLOG.md.

### 2. Iniciar Nueva Historia

```
@start-objective HU-1.2
```

Esto lee la story-card y genera `current_objective.md`.

### 3. Trabajar en la Historia

- Usar el prompt de `current_objective.md` en Cursor
- Marcar tareas como completadas `[x]` durante el desarrollo
- Agregar notas en la sección "Notas de Implementación"

### 4. Validar Criterios de Aceptación

- Revisar que todos los criterios de DoD estén cumplidos
- Ejecutar pruebas de aceptación
- Verificar casos de prueba (CP-X.X.X)

### 5. Finalizar Historia

```
@finish-objective
```

## Estructura del Proyecto

```
cfe-analisis-app/
├── .spec/                    # Workflow y documentación
│   ├── BACKLOG.md           # Backlog con Features e HUs
│   ├── commands/            # Este directorio (comandos markdown)
│   ├── story-cards/         # Story cards generadas
│   └── history/             # Objetivos completados
├── scripts/                  # Scripts de Python
│   ├── upload_data.py       # ETL para Supabase
│   └── app.py               # Aplicación Streamlit
├── data/                     # Datos fuente (CSVs)
├── PRD.md                    # Product Requirements Document
├── spec.md                   # Technical Specification
├── current_objective.md      # Objetivo actual en progreso
└── CHANGELOG.md              # Historial de cambios
```

## Stack Tecnológico

- **Python 3.10+** - Lenguaje principal
- **Streamlit** - Framework web para dashboards
- **Pandas** - Procesamiento y análisis de datos
- **Plotly Express** - Visualizaciones interactivas
- **Supabase** - Base de datos PostgreSQL en la nube

## Notas Técnicas

Todos los comandos se ejecutan mediante prompts en Cursor siguiendo las instrucciones detalladas en los archivos `.md`.
