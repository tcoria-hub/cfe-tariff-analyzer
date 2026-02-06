# HU-3.1: KPI de Promedio Anual - Completada

> **Historia:** HU-3.1 - KPI de Promedio Anual
> **Feature:** Feature 3: Análisis de Promedio Anual e Inteligencia Horaria
> **Estado:** ✅ Completado

## Métricas de Tiempo
- **Inicio:** 2026-02-05 19:45
- **Fin:** 2026-02-05 20:05
- **Tiempo de ciclo:** ~20 minutos

## Objetivo de la Sesión
Implementar KPI de Promedio Anual. Mostrar el promedio mensual del año seleccionado vs el año anterior para entender la tendencia general del costo energético.

## Tareas Completadas
- [x] Calcular media aritmética de todos los meses disponibles del año seleccionado
- [x] Comparar contra la media del mismo periodo del año anterior
- [x] Mostrar `st.metric` con promedio y delta %
- [x] Manejar caso de años con diferente número de meses disponibles

## Criterios de Aceptación (DoD)
- [x] **CP-3.1.1:** Si año 2024 tiene datos de ene-dic y 2023 igual, se promedian los 12 meses
- [x] **CP-3.1.2:** Si año 2024 tiene datos de ene-sep, se compara contra ene-sep de 2023
- [x] **CP-3.1.3:** El cálculo es: promedio_N = mean(total para todos los meses de año N)

## Decisiones y Notas
### Decisiones Tomadas
- Se usa comparación justa: solo meses que existen en ambos años
- Para tarifas horarias, se muestran 3 KPIs (Base, Intermedia, Punta) en columnas
- El tooltip (help) muestra cantidad de meses comparados y valor anterior

### Problemas Encontrados
- (ninguno)

### Trade-offs
- (ninguno)

## Resumen de Implementación (Generado por AI)

### Qué se implementó
- Función `calcular_promedio_anual()` para calcular media aritmética de meses disponibles
- Función `calcular_variacion_promedio_anual()` para comparar promedios entre dos años
- Sección "📊 Promedio Anual" en la UI con `st.metric`
- Para tarifas horarias: 3 KPIs en columnas (Base, Intermedia, Punta)
- Para tarifas simples: 1 KPI para Variable (Energía)

### Decisiones Clave
- **Comparación justa**: Solo se comparan meses que existen en ambos años
- **Tooltip informativo**: Muestra cantidad de meses comparados y valor anterior
- **delta_color="inverse"**: Incrementos en rojo (malo), decrementos en verde (bueno)
- **Ubicación**: KPI se muestra antes de la gráfica de tendencia mensual

### Problemas Resueltos
- (ninguno - implementación directa)

### Archivos Modificados/Creados
- `scripts/data_loader.py` - Nuevas funciones para cálculo de promedios (líneas 697-801)
- `scripts/app.py` - Sección KPI de promedio anual (líneas 508-551), versión v1.5.0

### Deuda Técnica / Pendientes Futuros
- Posible mejora: mostrar gráfica de comparación de promedios históricos (múltiples años)

## Referencias
- [BACKLOG.md](../.spec/BACKLOG.md)
- [TECH_SPEC.md](../.spec/TECH_SPEC.md)
- [Story Card](../story-cards/HU-3.1-kpi-promedio-anual.md)
