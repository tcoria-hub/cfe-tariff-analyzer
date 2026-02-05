Comando: @start-objective [HU-X.X]

"Cuando te pida ejecutar este comando con una Historia de Usuario (ej: @start-objective HU-1.2), realiza las siguientes acciones en orden:

**1. Identificar Story Card:**
- Busca el archivo story-card correspondiente en `.spec/story-cards/` que coincida con el identificador proporcionado.
- Acepta formatos: `HU-1.2`, `HU-1.2-selector-geografico`, o solo `1.2`.
- Si no encuentras el archivo exacto, busca por coincidencia parcial del nombre.

**2. Leer Story Card:**
- Lee el archivo story-card completo.
- Extrae las siguientes secciones:
  - 🎯 Objetivo de la Sesión
  - 📝 Current Objective (lista de tareas)
  - 🤖 Prompt para Cursor
  - 🧪 Pruebas de Aceptación

**3. Buscar Información en BACKLOG.md:**
- Identifica la sección de la Historia de Usuario en `.spec/BACKLOG.md` usando el patrón `### [estado] Historia de Usuario X.X:`.
- Extrae el número de línea donde comienza la historia.
- Identifica el Feature al que pertenece (busca hacia arriba hasta encontrar `## FEATURE X:`).
- Extrae el nombre completo del Feature.

**4. Generar current_objective.md:**
- Usa el template estructurado con las siguientes secciones:

```markdown
# Current Objective

> **Historia:** HU-X.X - [Título]
> **Feature:** [Nombre del Feature]
> **Estado:** 🔄 En progreso

## Métricas de Tiempo
- **Inicio:** YYYY-MM-DD HH:MM (zona horaria local)
- **Fin:** (pendiente)
- **Tiempo de ciclo:** (pendiente)

## Objetivo de la Sesión
[Copiado desde story-card]

## Tareas Pendientes
- [ ] Tarea 1
- [ ] Tarea 2
...

## Criterios de Aceptación (DoD)
- [ ] Criterio 1
- [ ] Criterio 2
...

## Decisiones y Notas
<!-- Documentar aquí durante el desarrollo -->
### Decisiones Tomadas
- (ninguna aún)

### Problemas Encontrados
- (ninguno aún)

### Trade-offs
- (ninguno aún)

## Referencias
- [BACKLOG.md](.spec/BACKLOG.md) (línea X)
- [TECH_SPEC.md](.spec/TECH_SPEC.md)
- [Story Card](.spec/story-cards/HU-X.X-slug.md)

## Prompt para Cursor
[Copiado completo desde story-card]
```

**5. Actualizar Estado en BACKLOG.md (Opcional):**
- Si la historia está marcada como ⏳ Pendiente, puedes cambiarla a 🔄 En progreso.
- Esto es opcional y puede hacerse manualmente.

**6. Confirmación:**
- Muestra un resumen de lo generado:
  - Historia identificada
  - Feature al que pertenece
  - Story Card utilizada
  - Línea en BACKLOG.md
  - Fecha/hora de inicio registrada
  - Archivo current_objective.md generado

**Notas importantes:**
- Si la story-card no existe, informa al usuario y sugiere usar @generate-story-cards primero.
- Si hay múltiples story-cards que coinciden, pregunta cuál usar o usa la más reciente.
- Mantén el formato y estructura del template de current_objective.md.
- Las tareas deben ser específicas y accionables.
- La fecha de inicio se usa para calcular el tiempo de ciclo al finalizar."
