# Current Objective (Archivado)

> **Historia:** HU-5.1 - Tabla Histórica de Tarifas por Rango de 12 Meses
> **Feature:** Feature 5: Histórico de Tarifas por Rango de 12 Meses
> **Estado:** ✅ Completado
> **Archivado:** 2026-02-19

## Métricas de Tiempo
- **Inicio:** 2026-02-18 16:00
- **Fin:** 2026-02-19 18:00
- **Tiempo de ciclo:** ~1 día (~26 horas)

## Objetivo de la Sesión
Implementar Tabla Histórica de Tarifas por Rango de 12 Meses. Ver una tabla con el histórico completo de una tarifa y división en un rango de 12 meses calculado desde un mes final seleccionado para analizar la evolución mes a mes de todos los componentes tarifarios en un periodo específico.

## Tareas (todas completadas)
- [x] Selector "Mes Final del Rango", helpers `mes_a_numero`/`calcular_rango_12_meses`, casos borde, tabla pivotada, formato numérico, exportación CSV.

## Criterios de Aceptación (DoD)
- [x] Todos cumplidos (selector, rango 12 meses, casos borde, tabla cronológica, tarifas horarias/simples, interactiva, total y rango, CSV con nombre dinámico).

## Resumen de Implementación (Generado por AI)

### Qué se implementó
- Selector "Mes Final del Rango" (enero–diciembre) en el tab Generar Histórico.
- Funciones helper: `mes_a_numero`, `numero_a_mes`, `calcular_rango_12_meses` con casos borde.
- Columna `mes_numero` en `load_tarifas()`.
- Tabla pivotada: una fila por (Año, Mes) con Año, Mes, Fecha (ene-24), Cargo Fijo, Base, Intermedia, Punta, Cargo Cap.
- Formato numérico: 2 decimales + miles (Fijo/Cap), 4 decimales (Base/Intermedia/Punta).
- `pivotar_historico_por_mes()`, `MESES_ABREV_POR_NUM` para evitar conflicto con dict de gráficas.
- Botón "Descargar CSV" exportando la vista mostrada con nombre dinámico.

### Decisiones clave
- Vista pivotada para legibilidad; CSV = lo mostrado.
- Ordenar antes de renombrar; filtro sin modificar DataFrame global.

### Problemas resueltos
- KeyError 'anio': ordenar antes del rename.
- KeyError: 2 en MESES_ABREV: lista renombrada a MESES_ABREV_POR_NUM.

### Archivos modificados
- `scripts/data_loader.py`: helpers, mes_numero, calcular_rango_12_meses, pivotar_historico_por_mes, MESES_ABREV_POR_NUM.
- `scripts/app.py`: tab Generar Histórico con selector, pivot, formato, column_config, download CSV.

### Deuda técnica / pendientes
- Ninguna crítica. Opcional: filas alternas (tabla HTML).
