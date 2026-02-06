# HU-3.4: Gráfica de Tendencia Mensual - COMPLETADA

> **Feature:** Feature 3: Análisis de Promedio Anual e Inteligencia Horaria
> **Estado:** ✅ Completada
> **Fecha cierre:** 2026-02-05

## Métricas de Tiempo
- **Inicio:** 2026-02-05 19:00
- **Fin:** 2026-02-05 19:30
- **Tiempo de ciclo:** ~30 minutos

## Objetivo de la Sesión
Implementar Gráfica de Tendencia Mensual. Mostrar una gráfica de líneas con la evolución mensual de ambos años para identificar patrones estacionales y anomalías.

## Tareas Completadas
- [x] Crear gráfica de líneas con eje X = meses (Ene-Dic), eje Y = valor total
- [x] Mostrar dos líneas: año seleccionado y año anterior
- [x] Usar colores distintivos con leyenda clara
- [x] Implementar hover con mes y valor exacto

## Criterios de Aceptación (DoD)
- [x] **CP-3.4.1:** La gráfica muestra puntos por cada mes disponible
- [x] **CP-3.4.2:** Si un mes no tiene datos, no aparece en la línea
- [x] **CP-3.4.3:** El orden de meses es cronológico: Enero → Diciembre

---

## Resumen de Implementación (Generado por AI)

### Qué se implementó
- Constantes `MESES_ORDEN` y `MESES_ABREV` para ordenamiento y etiquetas
- Función `get_tendencia_mensual()` para obtener valores mes a mes
- Función `get_datos_tendencia_comparativa()` para preparar datos de Plotly
- Sección "📈 Tendencia Mensual" en cada pestaña de tarifa
- Para tarifas horarias: 3 gráficas en columnas (Base | Intermedia | Punta)
- Para tarifas simples: una sola gráfica de tendencia
- Gráfica de líneas con marcadores y hover interactivo
- Colores: Azul (año anterior), Rojo (año actual)

### Decisiones Clave
- **Ordenamiento por Mes_Num**: Se usa un campo numérico para ordenar correctamente los meses
- **Meses faltantes**: Si un mes no tiene datos, simplemente no aparece (la línea salta)
- **3 columnas para horarias**: Consistente con el desglose por componente

### Archivos Modificados/Creados
- `scripts/data_loader.py`:
  - Constantes `MESES_ORDEN`, `MESES_ABREV`
  - Nueva función `get_tendencia_mensual()`
  - Nueva función `get_datos_tendencia_comparativa()`
- `scripts/app.py`:
  - Import de `get_datos_tendencia_comparativa`
  - Sección "📈 Tendencia Mensual" con gráficas de líneas
  - Versión actualizada a v1.4.0

### Deuda Técnica / Pendientes Futuros
- Agregar promedio anual como línea horizontal de referencia
- Considerar mostrar también tendencia de Capacidad

## Referencias
- [BACKLOG.md](.spec/BACKLOG.md) (línea 391)
- [Story Card](.spec/story-cards/HU-3.4-grafica-tendencia-mensual.md)
