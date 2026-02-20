# Historia 6.2: Activación dinámica de campos por esquema tarifario

## 🎯 Objetivo de la Sesión
Implementar Activación dinámica de campos por esquema tarifario. Que el sistema muestre únicamente los campos correspondientes a la tarifa seleccionada para evitar capturar información que no existe en el recibo.

## 📝 Current Objective (Copiar a current_objective.md)
- [ ] Cargar/definir esquemas por tarifa (archivo ej. data/04_esquemas_recibo_por_tarifa.json o CSV)
- [ ] Al seleccionar una tarifa, mostrar solo el bloque de campos de esa tarifa
- [ ] Ocultar campos de otras tarifas
- [ ] Si el usuario cambia la tarifa antes de guardar, reiniciar los campos variables capturados
- [ ] Soportar esquemas construidos bajo demanda: primera vez que se usa una tarifa permitir definir/capturar campos y persistir el esquema
- [ ] Respetar conjunto de campos obligatorios por tarifa según esquema

## 🤖 Prompt para Cursor (Composer)

Implementa la Historia de Usuario HU-6.2 del Feature 6: Captura Manual y Exportación de Recibos de Luz CFE.

**Contexto:**
- Proyecto: CFE Tariff Analyzer
- Feature: Captura Manual y Exportación de Recibos de Luz CFE
- Referencias: @.spec/BACKLOG.md (HU 6.2), @.spec/TECH_SPEC.md

**Historia de Usuario:**
- **Como:** Usuario capturista
- **Quiero:** Que el sistema muestre únicamente los campos correspondientes a la tarifa seleccionada
- **Para poder:** Evitar capturar información que no existe en el recibo

**Criterios de Aceptación:**
1. Al seleccionar una tarifa, se habilita exclusivamente su bloque de campos
2. Los campos de otras tarifas no son visibles
3. Si se cambia la tarifa antes de guardar, los campos previamente capturados se reinician
4. Cada tarifa define su propio conjunto de campos obligatorios (esquemas construidos bajo demanda)

**Requisitos Técnicos:**
- Esquemas por tarifa: almacenar en repo (ej. data/04_esquemas_recibo_por_tarifa.json). Si no existe esquema para una tarifa, permitir captura “primera vez” y al guardar persistir el esquema derivado
- Mostrar/ocultar bloques de campos según tarifa seleccionada en datos generales
- Al cambiar tarifa en el bloque inicial, limpiar session_state o estado de los campos variables y re-renderizar solo los campos de la nueva tarifa
- Componentes Streamlit: st.selectbox, st.text_input, st.number_input según tipo de campo en esquema

**Instrucciones:**
1. Revisar criterios de aceptación y casos de prueba en BACKLOG.md (HU 6.2)
2. Implementar lógica de esquemas por tarifa (lectura/escritura del archivo de esquemas)
3. Implementar bloque dinámico de campos en el tab Captura de Datos
4. Mantener consistencia con app.py y con HU-6.1 (bloque de datos generales ya existente)

## 🧪 Pruebas de Aceptación
- [ ] **CP-6.2.1:** Seleccionar PDBT muestra solo los campos definidos para PDBT
- [ ] **CP-6.2.2:** Cambiar de PDBT a GDMTH antes de guardar limpia los campos variables y muestra los de GDMTH
- [ ] **CP-6.2.3:** Primera vez que se usa una tarifa: se permite definir campos al capturar y se persiste el esquema
- [ ] Criterios: un solo bloque de campos visible por tarifa; cambio de tarifa reinicia campos; obligatoriedad por esquema
