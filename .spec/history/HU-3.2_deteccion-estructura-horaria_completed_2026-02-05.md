# HU-3.2: Detección Automática de Estructura Horaria - COMPLETADA

> **Feature:** Feature 3: Análisis de Promedio Anual e Inteligencia Horaria
> **Estado:** ✅ Completada
> **Fecha cierre:** 2026-02-05

## Métricas de Tiempo
- **Inicio:** Implementada durante HU-1.3 (selector de tarifas)
- **Fin:** 2026-02-05
- **Tiempo de ciclo:** N/A (implementada como parte de otras historias)

## Objetivo de la Sesión
Identificar automáticamente si la tarifa seleccionada tiene cargos horarios para adaptar la interfaz.

## Tareas Completadas
- [x] Definir constante TARIFAS_HORARIAS con códigos de tarifas horarias
- [x] Crear función es_tarifa_horaria() para clasificación
- [x] Clasificar tarifas al seleccionarlas en el multiselect
- [x] Adaptar vistas según tipo de tarifa (horaria vs simple)

## Criterios de Aceptación (DoD)
- [x] **CP-3.2.1:** Seleccionar "GDMTH" activa vista horaria (Base, Intermedia, Punta)
- [x] **CP-3.2.2:** Seleccionar "PDBT" muestra vista simple (sin segmentación horaria)
- [x] **CP-3.2.3:** Seleccionar "DIST" activa vista horaria (tiene B, I, P)

---

## Resumen de Implementación (Generado por AI)

### Qué se implementó
- Constante `TARIFAS_HORARIAS = {"GDMTH", "DIST", "DIT"}` en data_loader.py
- Función `es_tarifa_horaria(tarifa: str) -> bool` que verifica si la tarifa está en el set
- Clasificación automática en app.py al seleccionar tarifas
- Mensajes informativos "⏰ Horarias: ..." y "📊 Simples: ..."
- Vistas diferenciadas en todas las secciones (tabla, gráficas, desglose, tendencia)

### Decisiones Clave
- **Set estático vs detección dinámica**: Se optó por un set predefinido de tarifas horarias en lugar de consultar el CSV, por simplicidad y rendimiento
- **Clasificación visual**: Se muestra al usuario qué tarifas son horarias vs simples al seleccionarlas

### Archivos Modificados
- `scripts/data_loader.py` - Constante TARIFAS_HORARIAS y función es_tarifa_horaria()
- `scripts/app.py` - Clasificación y visualización diferenciada

## Referencias
- [BACKLOG.md](.spec/BACKLOG.md) (línea 341)
