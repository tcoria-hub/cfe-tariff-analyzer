Comando: @finish-objective

"Cuando te pida ejecutar este comando, realiza las siguientes acciones en orden:

**1. Verificar Completitud:**
- Lee current_objective.md y verifica que todas las tareas estén marcadas como completadas [x].
- Si hay tareas pendientes, pregunta si:
  a) Se deben marcar como completadas
  b) Se requiere trabajo adicional antes de cerrar
  c) Se deben mover a una historia futura

**2. Calcular Tiempo de Ciclo:**
- Extrae la fecha de inicio de la sección "Métricas de Tiempo" en current_objective.md.
- Calcula el tiempo transcurrido hasta ahora.
- Actualiza current_objective.md con:
  - **Fecha fin:** YYYY-MM-DD HH:MM
  - **Tiempo de ciclo:** X horas / X días

**3. Generar Resumen AI:**
- Analiza el historial de la conversación actual relacionada con esta historia.
- Genera un resumen estructurado que incluya:

```markdown
## Resumen de Implementación (Generado por AI)

### Qué se implementó
- [Lista de funcionalidades/cambios principales]

### Decisiones Clave
- [Decisiones técnicas o de diseño tomadas durante la conversación]
- [Por qué se eligió X sobre Y]

### Problemas Resueltos
- [Problema]: [Cómo se resolvió]

### Archivos Modificados/Creados
- [Lista de archivos con descripción breve del cambio]

### Deuda Técnica / Pendientes Futuros
- [Items que quedaron fuera del alcance o para mejorar después]
```

- Agrega este resumen a la sección "Decisiones y Notas" de current_objective.md.

**4. Archivar:**
- Crea un nuevo archivo en `.spec/history/` con el patrón:
  `HU-X.X_[slug]_completed_YYYY-MM-DD.md`
- El archivo debe contener:
  - Todo el contenido de current_objective.md
  - El resumen AI generado
  - Tiempo de ciclo final

**5. Actualizar Backlog:**
- Busca en `.spec/BACKLOG.md` la sección correspondiente.
- Cambia el estado a: `### ✅ Historia de Usuario X.X: Título`
- Si todas las HUs de un FEATURE están ✅, marca el Feature como completado en "Estado del Proyecto".

**6. Actualizar Changelog:**
- Añade entrada en CHANGELOG.md con formato:

```markdown
## [YYYY-MM-DD]

### HU-X.X: [Título de la Historia]
**Tiempo de ciclo:** X horas

#### Implementado
- [Resumen de funcionalidades]

#### Decisiones Clave
- [Decisiones más importantes]

#### Archivos Modificados
- `path/to/file.py` - [descripción]
```

**7. Preparar Commit:**
- Añade al staging:
  - current_objective.md
  - .spec/history/HU-X.X_*_completed.md
  - .spec/BACKLOG.md
  - CHANGELOG.md
  - Archivos de implementación (scripts/, etc.)
- Genera mensaje de commit:
  ```
  feat(HU-X.X): [Título corto]
  
  - [Puntos principales del resumen]
  
  Tiempo de ciclo: X horas
  ```
- Ejecuta el commit (push manual por el usuario).

**8. Reset:**
- Deja current_objective.md listo para el próximo objetivo:

```markdown
# Current Objective

> Sin objetivo activo. Usa `@start-objective HU-X.X` para iniciar una nueva historia.

## Estado
⏳ Esperando nuevo objetivo

## Métricas Acumuladas
| Historia | Tiempo de Ciclo | Fecha |
|----------|-----------------|-------|
| HU-X.X   | X horas         | YYYY-MM-DD |

## Referencias
- [BACKLOG.md](.spec/BACKLOG.md)
- [TECH_SPEC.md](.spec/TECH_SPEC.md)
- [PRD.md](.spec/PRD.md)
```

**Notas importantes:**
- El resumen AI debe capturar las decisiones discutidas en el chat, no solo los cambios de código.
- Si no hay información suficiente en el chat, pide al usuario que complete la sección "Decisiones y Notas".
- El tiempo de ciclo es importante para métricas de velocidad del equipo.
- El mensaje de commit debe seguir conventional commits."
