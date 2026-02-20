# Current Objective (Archivado)

> **Historia:** HU-6.1 - Captura de datos generales del recibo
> **Feature:** Captura Manual y Exportación de Recibos de Luz CFE
> **Estado:** ✅ Completado

## Métricas de Tiempo
- **Inicio:** 2026-02-20 (zona horaria local)
- **Fin:** 2026-02-20
- **Tiempo de ciclo:** < 1 día

## Objetivo de la Sesión
Implementar Captura de datos generales del recibo. Registrar los datos generales del recibo para identificar de forma única el suministro y el periodo facturado.

## Tareas Completadas
- [x] Mostrar un bloque inicial de captura para datos generales en el tab "Captura de Datos"
- [x] Incluir campo obligatorio: Tarifa (selector reutilizando lista de tarifas del sistema)
- [x] Incluir campo obligatorio: Número de servicio
- [x] Incluir campo obligatorio: Periodo facturado
- [x] Bloquear avance o guardado si falta algún dato obligatorio
- [x] Mostrar mensajes claros cuando falten datos

## Criterios de Aceptación (DoD)
- [x] Los datos generales se capturan en un bloque inicial
- [x] La tarifa es obligatoria
- [x] El número de servicio es obligatorio
- [x] El periodo facturado es obligatorio
- [x] No se permite avanzar si falta algún dato obligatorio

## Decisiones y Notas

### Decisiones Tomadas
- Formulario reutilizable en una función `_render_formulario_datos_generales_recibo(key_suffix)` para evitar duplicar código en las dos ramas del tab (con/sin tarifas seleccionadas arriba).
- Periodo facturado = mes + año (selectores separados); años 2015–2030 para recibos.
- Lista de tarifas desde `get_tarifas_disponibles()` (misma fuente que Feature 1), con opción "Selecciona una tarifa".
- Botón "Guardar recibo" deshabilitado si falta algún obligatorio; al pulsar (cuando completo) se muestra mensaje de que el guardado se implementará en HU-6.5.

### Problemas Encontrados
- (ninguno)

### Trade-offs
- (ninguno)

---

## Resumen de Implementación (Generado por AI)

### Qué se implementó
- Bloque inicial "Datos generales del recibo" en el tab "Captura de Datos" (reemplaza el placeholder del Feature 6).
- Campos obligatorios: Tarifa (selectbox con formato "CÓDIGO - Descripción"), Número de servicio (text_input), Periodo facturado (mes + año con selectboxes).
- Validación: no se permite guardar si falta tarifa, número de servicio, mes o año; mensaje claro con `st.warning`.
- Persistencia del formulario en `st.session_state` (recibo_tarifa, recibo_numero_servicio, recibo_mes, recibo_anio) para mantener valores al cambiar de tab.
- Función helper `_render_formulario_datos_generales_recibo(key_suffix)` usada en ambas ramas (con/sin tarifas seleccionadas) para evitar duplicación y conflictos de keys en Streamlit.

### Decisiones Clave
- **Función con key_suffix:** El tab "Captura de Datos" se renderiza en dos ramas (cuando hay tarifas seleccionadas y cuando no); se usa un helper con `key_suffix` ("", "_alt") para que los widgets tengan keys únicos en cada rama.
- **Periodo = mes + año:** Definido como dos selectores (mes en español, año 2015–2030) para alinearse con recibos CFE típicos.
- **Guardar sin persistencia:** El botón "Guardar recibo" se habilita cuando los datos están completos pero la acción solo muestra un mensaje informativo; la persistencia se implementará en HU-6.5.

### Problemas Resueltos
- (ninguno significativo)

### Archivos Modificados/Creados
- `scripts/app.py` – Inicialización de session_state para recibo_*; función `_render_formulario_datos_generales_recibo()`; reemplazo del placeholder del tab "Captura de Datos" por el formulario en ambas ramas.

### Deuda Técnica / Pendientes Futuros
- HU-6.5 implementará el guardado real (CSV en repo vía GitHub).
- HU-6.2 y siguientes añadirán el bloque de campos variables por tarifa y esquemas bajo demanda.

---

## Referencias
- [BACKLOG.md](.spec/BACKLOG.md) (línea 783)
- [TECH_SPEC.md](.spec/TECH_SPEC.md)
- [Story Card](.spec/story-cards/HU-6.1-captura-datos-generales-recibo.md)

## Pruebas de Aceptación
- [x] **CP-6.1.1:** Sin tarifa seleccionada no se puede continuar al bloque de datos variables
- [x] **CP-6.1.2:** Sin número de servicio no se habilita el botón Guardar
- [x] **CP-6.1.3:** Sin periodo facturado no se permite guardar
- [x] Criterios: bloque inicial visible; tarifa, número de servicio y periodo obligatorios; avance bloqueado si falta alguno
