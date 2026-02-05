# HU-2.1: KPI de Variación Total Diciembre - COMPLETADA

> **Feature:** Feature 2: Comparativo de Cierre "Diciembre vs Diciembre"
> **Estado:** ✅ Completada
> **Fecha cierre:** 2026-02-05

## Métricas de Tiempo
- **Inicio:** 2026-02-05 15:30 (aprox)
- **Fin:** 2026-02-05 16:30 (aprox)
- **Tiempo de ciclo:** ~1 hora

## Objetivo de la Sesión
Implementar KPI de Variación Total Diciembre. Mostrar el porcentaje de variación del total de diciembre año N vs año N-1 para conocer rápidamente el incremento o decremento anual.

## Tareas Completadas
- [x] Crear tarjeta `st.metric` con valor total de diciembre del año seleccionado
- [x] Calcular y mostrar delta (variación %) respecto al año anterior
- [x] Configurar colores: rojo/alza para incremento, verde/baja para decremento
- [x] Manejar caso de "Datos no disponibles" si falta información
- [x] Mostrar tarifas del año anterior (adicional al requerimiento original)
- [x] Incluir cargo de Capacidad (adicional al requerimiento original)

## Criterios de Aceptación (DoD)
- [x] **CP-2.1.1:** Para GDMTH, División Bajío, año 2024, el KPI muestra total dic-2024 vs dic-2023
- [x] **CP-2.1.2:** Variación % = ((total_dic_N / total_dic_N-1) - 1) * 100
- [x] **CP-2.1.3:** Si total_dic_2023 = 1.00 y total_dic_2024 = 1.05, delta = +5.0%

---

## Resumen de Implementación (Generado por AI)

### Qué se implementó
- Sección "📊 Comparativo Diciembre vs Diciembre" en la app
- Tabla comparativa con columnas: Concepto, Dic Año Anterior, Dic Año Actual, Variación %, Unidad
- Para tarifas horarias (GDMTH, DIST, DIT): desglose por Base, Intermedia, Punta + Capacidad
- Para tarifas simples: Variable (Energía) + Capacidad
- Indicadores visuales de variación (🔴 incremento, 🟢 decremento)
- Warning cuando se selecciona el año más reciente (datos de diciembre pueden no existir)
- Mensaje específico cuando faltan datos ("No hay dic-YYYY")

### Decisiones Clave
- **Cargo específico "Variable (Energía)"**: Solo se muestra este cargo en $/kWh, no se suman otros cargos con unidades diferentes
- **Capacidad separada**: Se muestra en $/kW como concepto independiente
- **Tabla vs Métricas**: Se cambió de `st.metric` individual a formato de tabla para mostrar año anterior, año actual y variación en columnas
- **Validación contra Power BI**: Se verificó que los valores coincidieran con el Excel fuente (DIST, Baja California Sur, 2020-2021)

### Problemas Resueltos
- **Suma incorrecta de cargos**: La función original `get_total_diciembre` sumaba valores con unidades diferentes ($/kWh, $/kW, $/mes). Se creó `get_cargo_variable_diciembre` para obtener solo "Variable (Energía)" filtrado por horario
- **Discrepancia con Power BI**: Se identificó que Power BI mostraba métricas pre-procesadas; los datos crudos del CSV coinciden con la app
- **Datos 2025 incompletos**: El CSV solo tiene datos hasta septiembre 2025; se agregó warning al usuario

### Archivos Modificados/Creados
- `scripts/data_loader.py`:
  - Nueva función `get_cargo_variable_diciembre()` - obtiene cargo Variable filtrado por horario
  - Nueva función `get_cargo_capacidad_diciembre()` - obtiene cargo Capacidad
  - Modificado `get_cargos_diciembre_por_horario()` - incluye capacidad
  - Modificado `calcular_variacion_diciembre()` - calcula variación por cargo
- `scripts/app.py`:
  - Nueva sección "📊 Comparativo Diciembre vs Diciembre"
  - Tabla comparativa con Dic anterior, Dic actual, Variación, Unidad
  - Manejo de datos faltantes con mensajes específicos

### Deuda Técnica / Pendientes Futuros
- Mejorar visualización de la tabla (considerar st.dataframe con estilos)
- Agregar gráfica de barras comparativa (HU-2.3)
- Mostrar desglose por componente (generación, transmisión, etc.) (HU-2.2)

## Referencias
- [BACKLOG.md](.spec/BACKLOG.md) (línea 221)
- [TECH_SPEC.md](.spec/TECH_SPEC.md)
