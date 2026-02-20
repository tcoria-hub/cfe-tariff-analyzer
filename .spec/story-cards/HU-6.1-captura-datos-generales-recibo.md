# Historia 6.1: Captura de datos generales del recibo

## 🎯 Objetivo de la Sesión
Implementar Captura de datos generales del recibo. Registrar los datos generales del recibo para identificar de forma única el suministro y el periodo facturado.

## 📝 Current Objective (Copiar a current_objective.md)
- [ ] Mostrar un bloque inicial de captura para datos generales en el tab "Captura de Datos"
- [ ] Incluir campo obligatorio: Tarifa (selector reutilizando lista de tarifas del sistema)
- [ ] Incluir campo obligatorio: Número de servicio
- [ ] Incluir campo obligatorio: Periodo facturado
- [ ] Bloquear avance o guardado si falta algún dato obligatorio
- [ ] Mostrar mensajes claros cuando falten datos

## 🤖 Prompt para Cursor (Composer)

Implementa la Historia de Usuario HU-6.1 del Feature 6: Captura Manual y Exportación de Recibos de Luz CFE.

**Contexto:**
- Proyecto: CFE Tariff Analyzer
- Feature: Captura Manual y Exportación de Recibos de Luz CFE (estructura variable por tarifa)
- Referencias: @.spec/BACKLOG.md (HU 6.1), @.spec/TECH_SPEC.md

**Historia de Usuario:**
- **Como:** Usuario capturista
- **Quiero:** Registrar los datos generales del recibo
- **Para poder:** Identificar de forma única el suministro y el periodo facturado

**Criterios de Aceptación:**
1. Los datos generales se capturan en un bloque inicial
2. La tarifa es obligatoria
3. El número de servicio es obligatorio
4. El periodo facturado es obligatorio
5. No se permite avanzar si falta algún dato obligatorio

**Requisitos Técnicos:**
- Stack: Python 3.10+, Streamlit, Pandas. Persistencia: CSV en repo vía GitHub (Feature 4). Esquemas por tarifa: bajo demanda.
- Implementar en el tab "Captura de Datos" (modo_tabs[2] en app.py); reemplazar el placeholder actual
- Reutilizar lista de tarifas existente (misma fuente que selector de tarifas del Feature 1)
- Usar st.selectbox para tarifa, st.text_input para número de servicio, y selector o inputs para periodo facturado (mes/año o rango según definición)
- No permitir enviar/guardar si tarifa, número de servicio o periodo están vacíos

**Instrucciones:**
1. Revisar criterios de aceptación y casos de prueba en BACKLOG.md (HU 6.1)
2. Implementar el bloque de datos generales dentro del tab de Captura de Datos
3. Mantener consistencia con código existente en scripts/app.py
4. Consultar @.spec/PRD.md y @.spec/TECH_SPEC.md si hay dudas

## 🧪 Pruebas de Aceptación
- [ ] **CP-6.1.1:** Sin tarifa seleccionada no se puede continuar al bloque de datos variables
- [ ] **CP-6.1.2:** Sin número de servicio no se habilita el botón Guardar
- [ ] **CP-6.1.3:** Sin periodo facturado no se permite guardar
- [ ] Criterios: bloque inicial visible; tarifa, número de servicio y periodo obligatorios; avance bloqueado si falta alguno
