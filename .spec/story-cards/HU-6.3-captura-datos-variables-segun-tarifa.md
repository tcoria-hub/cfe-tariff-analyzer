# Historia 6.3: Captura de datos variables según la tarifa

## 🎯 Objetivo de la Sesión
Implementar Captura de datos variables según la tarifa. Ingresar los datos específicos del esquema tarifario para reflejar fielmente la información del recibo físico.

## 📝 Current Objective (Copiar a current_objective.md)
- [ ] Renderizar campos del esquema de la tarifa seleccionada (tipos: numérico, monetario, texto, factor de potencia)
- [ ] Asegurar que todos los campos obligatorios del esquema deban completarse antes de guardar
- [ ] Campos numéricos: solo aceptar valores numéricos (validación y tipo de input)
- [ ] Campos monetarios: permitir hasta dos decimales
- [ ] No implementar cálculos automáticos (totales, derivados); solo captura
- [ ] Usar st.number_input con format o validación para monetarios (2 decimales)

## 🤖 Prompt para Cursor (Composer)

Implementa la Historia de Usuario HU-6.3 del Feature 6: Captura Manual y Exportación de Recibos de Luz CFE.

**Contexto:**
- Proyecto: CFE Tariff Analyzer
- Feature: Captura Manual y Exportación de Recibos de Luz CFE
- Referencias: @.spec/BACKLOG.md (HU 6.3), @.spec/TECH_SPEC.md

**Historia de Usuario:**
- **Como:** Usuario capturista
- **Quiero:** Ingresar los datos específicos del esquema tarifario
- **Para poder:** Reflejar fielmente la información del recibo físico

**Criterios de Aceptación:**
1. Todos los campos obligatorios del esquema deben completarse
2. Los campos numéricos solo aceptan valores numéricos
3. Los campos monetarios permiten hasta dos decimales
4. El sistema no realiza cálculos automáticos

**Requisitos Técnicos:**
- Construir formulario dinámico a partir del esquema de la tarifa (HU-6.2). Tipos de campo: numérico, monetario (2 decimales), texto, factor de potencia (0–1)
- st.number_input con min_value/max_value/step según tipo; para monetarios step=0.01 o format que limite a 2 decimales
- No añadir lógica de suma ni cálculos; solo captura y validación de formato
- Integrar con bloque de datos generales (HU-6.1) y con esquemas bajo demanda (HU-6.2)

**Instrucciones:**
1. Revisar criterios de aceptación y casos de prueba en BACKLOG.md (HU 6.3)
2. Implementar inputs por tipo de campo según esquema
3. Validar tipos en front (y opcionalmente antes de guardar)
4. Mantener consistencia con app.py

## 🧪 Pruebas de Aceptación
- [ ] **CP-6.3.1:** Campo numérico rechaza texto y muestra error
- [ ] **CP-6.3.2:** Campo monetario acepta máximo 2 decimales
- [ ] **CP-6.3.3:** No hay cálculo automático de totales ni derivados
- [ ] Criterios: obligatorios completos; numéricos solo números; monetarios 2 decimales; sin cálculos
