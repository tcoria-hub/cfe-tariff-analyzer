# HU-1.3: Selector Dinámico de Tarifas - COMPLETADA

> **Feature:** Feature 1: Selector Geográfico y de Tarifas (Smart Locator)
> **Estado:** ✅ Completada

## Métricas de Tiempo
- **Inicio:** 2026-02-05
- **Fin:** 2026-02-05
- **Tiempo de ciclo:** ~15 minutos

## Objetivo de la Sesión
Implementar Selector Dinámico de Tarifas. Permitir al usuario seleccionar el tipo de tarifa que desea analizar para ver los datos específicos de su contrato eléctrico.

## Tareas Completadas
- [x] Crear selector con todas las tarifas disponibles
- [x] Mostrar código y descripción (ej: "GDMTH - Gran demanda...")
- [x] Habilitar selector cuando hay División seleccionada
- [x] Identificar tipo de tarifa (horaria vs simple)

## Criterios de Aceptación (DoD)
- [x] **CP-1.3.1:** El selector muestra todas las tarifas con código y descripción
- [x] **CP-1.3.2:** Al seleccionar "GDMTH", el sistema identifica que es tarifa horaria
- [x] **CP-1.3.3:** Al seleccionar "PDBT", el sistema identifica que es tarifa simple

---

## Resumen de Implementación (Generado por AI)

### Qué se implementó
- Sección "⚡ Selector de Tarifas" en `app.py`
- `st.multiselect` para selección múltiple de tarifas
- Formato "CÓDIGO - Descripción" para cada opción
- Clasificación automática: tarifas horarias vs simples
- Constante `TARIFAS_HORARIAS` y función `es_tarifa_horaria()`

### Decisiones Clave
- **Selección múltiple:** Se usa `st.multiselect` en lugar de `st.selectbox` porque en la práctica un recibo puede tener más de una tarifa, y el usuario puede querer comparar varias simultáneamente.

### Archivos Modificados/Creados
- `scripts/app.py` - Nueva sección de selector de tarifas
- `scripts/data_loader.py` - Nueva función `es_tarifa_horaria()` y constante `TARIFAS_HORARIAS`

### Deuda Técnica / Pendientes Futuros
- Las gráficas posteriores deberán soportar múltiples tarifas seleccionadas

---

## Referencias
- [BACKLOG.md](.spec/BACKLOG.md) (línea 151)
- [Story Card](.spec/story-cards/HU-1.3-selector-dinamico-tarifas.md)
