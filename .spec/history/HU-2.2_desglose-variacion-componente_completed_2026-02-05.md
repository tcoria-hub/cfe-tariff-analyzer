# HU-2.2: Desglose de Variación por Componente - COMPLETADA

> **Feature:** Feature 2: Comparativo de Cierre "Diciembre vs Diciembre"
> **Estado:** ✅ Completada
> **Fecha cierre:** 2026-02-05

## Métricas de Tiempo
- **Inicio:** 2026-02-05 18:00
- **Fin:** 2026-02-05 18:45
- **Tiempo de ciclo:** ~45 minutos

## Objetivo de la Sesión
Implementar Desglose de Variación por Componente. Mostrar cómo cada componente de la tarifa contribuyó a la variación total para identificar qué conceptos tuvieron mayor impacto.

## Tareas Completadas
- [x] Crear gráfica con componentes: Generación, Transmisión, Distribución, CENACE, SCnMEM, Suministro
- [x] Mostrar para cada componente: variación absoluta y variación %
- [x] Ordenar componentes por impacto (mayor variación absoluta primero)
- [x] Distinguir visualmente componentes que subieron vs bajaron
- [x] Reorganizar UI con pestañas por tarifa para mejor UX

## Criterios de Aceptación (DoD)
- [x] **CP-2.2.1:** La variación de cada componente se muestra correctamente
- [x] **CP-2.2.2:** Para tarifas con cargo "Variable (Energía)", se muestran todos los componentes disponibles
- [x] **CP-2.2.3:** Los componentes se muestran según disponibilidad en el CSV

---

## Resumen de Implementación (Generado por AI)

### Qué se implementó
- Nueva función `get_componentes_diciembre()` para extraer valores de componentes del CSV
- Nueva función `calcular_variacion_componentes()` para calcular variaciones ordenadas por impacto
- Constantes `COMPONENTES` y `COMPONENTES_NOMBRES` para mapeo de columnas a nombres legibles
- Sección "🔍 Desglose por Componente" con gráficas de barras horizontales
- Para tarifas horarias: 3 gráficas en columnas (Base | Intermedia | Punta)
- Colores: Rojo para incrementos, Verde para decrementos
- **Reorganización de UI con st.tabs()** para mostrar una tarifa a la vez

### Decisiones Clave
- **Pestañas por tarifa**: Se cambió de scroll vertical infinito a pestañas `[DIST] [GDMTH] [GDMTO]` para mejorar la usabilidad cuando se analizan múltiples tarifas
- **Desglose en 3 columnas**: Para tarifas horarias, Base/Intermedia/Punta se muestran lado a lado en lugar de vertical
- **Ordenamiento por impacto**: Los componentes se ordenan por `abs(variación_absoluta)` descendente
- **Componentes dinámicos**: Solo se muestran componentes que tienen valores en el CSV (no se fuerzan todos)

### Problemas Resueltos
- **UI poco legible**: Con 3 tarifas horarias, el scroll era enorme. Solución: pestañas por tarifa
- **Gráficas de desglose ocupaban mucho espacio**: Solución: mostrar los 3 horarios en columnas lado a lado

### Archivos Modificados/Creados
- `scripts/data_loader.py`:
  - Constantes `COMPONENTES`, `COMPONENTES_NOMBRES`
  - Nueva función `get_componentes_diciembre()`
  - Nueva función `calcular_variacion_componentes()`
- `scripts/app.py`:
  - Import de `calcular_variacion_componentes`
  - Reorganización completa con `st.tabs()` por tarifa
  - Sección de desglose por componente con gráficas horizontales
  - Versión actualizada a v1.3.0

### Deuda Técnica / Pendientes Futuros
- Agregar hover más detallado con valores Anterior/Actual en desglose
- Considerar mostrar también desglose de Capacidad (no solo Variable)

## Referencias
- [BACKLOG.md](.spec/BACKLOG.md) (línea 250)
- [TECH_SPEC.md](.spec/TECH_SPEC.md)
- [Story Card](.spec/story-cards/HU-2.2-desglose-variacion-componente.md)
