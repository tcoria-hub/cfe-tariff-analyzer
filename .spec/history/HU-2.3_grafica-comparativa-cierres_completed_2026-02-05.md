# HU-2.3: Gráfica Comparativa de Cierres - COMPLETADA

> **Feature:** Feature 2: Comparativo de Cierre "Diciembre vs Diciembre"
> **Estado:** ✅ Completada
> **Fecha cierre:** 2026-02-05

## Métricas de Tiempo
- **Inicio:** 2026-02-05 16:45
- **Fin:** 2026-02-05 17:50
- **Tiempo de ciclo:** ~1 hora

## Objetivo de la Sesión
Implementar Gráfica Comparativa de Cierres. Mostrar una gráfica de barras comparando diciembre de ambos años para visualizar fácilmente la diferencia entre periodos.

## Tareas Completadas
- [x] Crear gráfica de barras agrupadas: una barra para dic año N, otra para dic año N-1
- [x] Configurar eje Y con valor total en pesos
- [x] Permitir comparar múltiples cargos (Variable por horario, Capacidad)
- [x] Usar colores distintivos para cada año
- [x] Separar gráficas por unidad ($/kWh vs $/kW) para escalas legibles

## Criterios de Aceptación (DoD)
- [x] **CP-2.3.1:** Para tarifa horaria, se muestran barras: Base, Intermedia, Punta + Capacidad
- [x] **CP-2.3.2:** Para tarifa simple, se muestran barras: Variable + Capacidad
- [x] **CP-2.3.3:** La gráfica es interactiva (hover muestra valores exactos)

---

## Resumen de Implementación (Generado por AI)

### Qué se implementó
- Gráfica de barras agrupadas con Plotly Express (`barmode="group"`)
- Dos gráficas separadas por unidad para escalas legibles:
  - Gráfica principal (75% ancho): Variable en $/kWh (Base, Intermedia, Punta)
  - Gráfica secundaria (25% ancho): Capacidad en $/kW
- Colores consistentes por año: Azul (#636EFA) para año anterior, Rojo (#EF553B) para año actual
- Etiquetas de valores sobre cada barra (`text_auto`)
- Hover interactivo con valores exactos (4 decimales para $/kWh, 2 para $/kW)
- Integración debajo de cada tabla comparativa de HU-2.1

### Decisiones Clave
- **Gráficas separadas vs facetas**: Se optó por dos gráficas independientes en lugar de facetas de Plotly, para evitar mostrar categorías vacías en cada panel
- **Proporción 3:1**: La gráfica de Variable ocupa más espacio porque tiene más conceptos (Base, Intermedia, Punta)
- **Leyenda única**: Solo la gráfica de Variable muestra leyenda (la de Capacidad no la repite)

### Problemas Resueltos
- **Escalas incompatibles**: Capacidad (~$230-430) vs Variable (~$1-4) hacía barras de Variable invisibles. Solución: gráficas separadas con escalas independientes
- **Columnas vacías en facetas**: Al usar `facet_col`, Plotly mostraba todas las categorías en ambos paneles. Solución: usar `st.columns` con gráficas separadas

### Archivos Modificados/Creados
- `scripts/app.py`:
  - Import de `plotly.express as px` y `pandas as pd`
  - Nueva sección de gráfica comparativa debajo de cada tabla de tarifa
  - Lógica para separar datos por unidad ($/kWh vs $/kW)
  - Dos gráficas con `st.columns([3, 1])`
  - Versión actualizada a v1.2.0

### Deuda Técnica / Pendientes Futuros
- Considerar agregar gráfica de variación porcentual (barras de delta %)
- Posible consolidación de múltiples tarifas en una sola gráfica comparativa

## Referencias
- [BACKLOG.md](.spec/BACKLOG.md) (línea 279)
- [TECH_SPEC.md](.spec/TECH_SPEC.md)
- [Story Card](.spec/story-cards/HU-2.3-grafica-comparativa-cierres.md)
