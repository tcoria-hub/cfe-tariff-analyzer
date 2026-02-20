# Historia 6.5: Guardado definitivo e inmutable del recibo

## 🎯 Objetivo de la Sesión
Implementar Guardado definitivo e inmutable del recibo. Guardar el recibo de forma definitiva para preservar la integridad del histórico.

## 📝 Current Objective (Copiar a current_objective.md)
- [ ] Al confirmar guardado, persistir el registro en data/recibos_capturados.csv (append) vía API de GitHub
- [ ] Incluir en cada registro: datos generales + campos variables + fecha y hora de captura (timestamp)
- [ ] No ofrecer flujo ni UI para editar o eliminar recibos ya guardados
- [ ] Tras guardado exitoso mostrar confirmación explícita (mensaje de éxito)
- [ ] Si es la primera vez que se usa la tarifa, persistir también el esquema en data/04_esquemas_recibo_por_tarifa.json (o CSV) vía mismo mecanismo de repo
- [ ] Reutilizar o extender lógica de persistencia por GitHub (HU-4.2): token en st.secrets, commit al repo

## 🤖 Prompt para Cursor (Composer)

Implementa la Historia de Usuario HU-6.5 del Feature 6: Captura Manual y Exportación de Recibos de Luz CFE.

**Contexto:**
- Proyecto: CFE Tariff Analyzer
- Feature: Captura Manual y Exportación de Recibos de Luz CFE
- Referencias: @.spec/BACKLOG.md (HU 6.5), @.spec/TECH_SPEC.md

**Historia de Usuario:**
- **Como:** Usuario capturista
- **Quiero:** Guardar el recibo de forma definitiva
- **Para poder:** Preservar la integridad del histórico

**Criterios de Aceptación:**
1. Al guardar, el registro queda almacenado como inmutable
2. No existe opción de edición posterior
3. No existe opción de eliminación
4. Se registra fecha y hora de captura
5. El sistema confirma explícitamente el guardado exitoso

**Requisitos Técnicos:**
- Persistencia: CSV en repo (`data/recibos_capturados.csv`) actualizado vía API de GitHub (reutilizar o extender lógica de HU-4.2). PyGithub o requests; token en st.secrets.
- Cada fila del CSV: columnas de datos generales (tarifa, numero_servicio, periodo, etc.) + columnas variables según esquema + columna timestamp_captura
- Esquemas bajo demanda: si es primer recibo de una tarifa, actualizar también `data/04_esquemas_recibo_por_tarifa.json` (o equivalente) en el mismo commit
- No implementar pantallas de edición ni eliminación de registros
- Tras guardado: st.success o mensaje claro y opcionalmente limpiar formulario para nueva captura

**Instrucciones:**
1. Revisar criterios de aceptación y casos de prueba en BACKLOG.md (HU 6.5)
2. Implementar flujo de guardado: validaciones (HU-6.4) → construir fila → append a CSV (y opcionalmente actualizar esquema) → commit al repo
3. Añadir timestamp de captura en zona horaria local o UTC según convención del proyecto
4. Consultar implementación de HU-4.2 si existe para reutilizar cliente GitHub
5. Mantener consistencia con app.py y TECH_SPEC

## 🧪 Pruebas de Aceptación
- [ ] **CP-6.5.1:** Tras guardar se muestra mensaje de confirmación
- [ ] **CP-6.5.2:** No hay botón ni flujo para editar o eliminar un recibo guardado
- [ ] **CP-6.5.3:** Cada registro incluye timestamp de captura
- [ ] Criterios: almacenamiento inmutable; sin edición/eliminación; timestamp; confirmación explícita
