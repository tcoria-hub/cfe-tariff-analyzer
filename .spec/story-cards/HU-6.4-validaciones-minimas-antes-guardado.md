# Historia 6.4: Validaciones mínimas antes del guardado

## 🎯 Objetivo de la Sesión
Implementar Validaciones mínimas antes del guardado. Que el sistema valide la información básica para asegurar consistencia en los datos almacenados.

## 📝 Current Objective (Copiar a current_objective.md)
- [ ] Impedir guardar si hay campos obligatorios vacíos (datos generales + campos variables del esquema)
- [ ] Validar que no se acepten valores negativos en campos numéricos/monetarios
- [ ] Validar factor de potencia en rango [0, 1] cuando el campo aplique
- [ ] Mostrar mensajes de error claros y por campo (junto a cada input o agrupados por sección)
- [ ] Ejecutar validaciones al pulsar Guardar y opcionalmente en tiempo real en inputs

## 🤖 Prompt para Cursor (Composer)

Implementa la Historia de Usuario HU-6.4 del Feature 6: Captura Manual y Exportación de Recibos de Luz CFE.

**Contexto:**
- Proyecto: CFE Tariff Analyzer
- Feature: Captura Manual y Exportación de Recibos de Luz CFE
- Referencias: @.spec/BACKLOG.md (HU 6.4), @.spec/TECH_SPEC.md

**Historia de Usuario:**
- **Como:** Usuario capturista
- **Quiero:** Que el sistema valide la información básica
- **Para poder:** Asegurar consistencia en los datos almacenados

**Criterios de Aceptación:**
1. No se permite guardar si existen campos obligatorios vacíos
2. No se aceptan valores negativos
3. El factor de potencia (cuando aplique) debe estar entre 0 y 1
4. Los mensajes de error son claros y por campo

**Requisitos Técnicos:**
- Validar antes de llamar a la lógica de guardado (HU-6.5). Usar st.error o mensajes junto a cada campo
- Para numéricos/monetarios: min_value=0 (o validación explícita si se permite 0)
- Para campo “factor de potencia”: min_value=0, max_value=1
- No guardar si validación falla; mostrar qué campos tienen error

**Instrucciones:**
1. Revisar criterios de aceptación y casos de prueba en BACKLOG.md (HU 6.4)
2. Añadir capa de validación al flujo de captura (al enviar formulario)
3. Mostrar errores por campo o listados de forma clara
4. Mantener consistencia con app.py y con HU-6.1, 6.2, 6.3

## 🧪 Pruebas de Aceptación
- [ ] **CP-6.4.1:** Guardar con campo obligatorio vacío muestra error en ese campo
- [ ] **CP-6.4.2:** Valor negativo en campo numérico muestra error
- [ ] **CP-6.4.3:** Factor de potencia > 1 o < 0 muestra error
- [ ] Criterios: no guardar con obligatorios vacíos; no negativos; factor de potencia 0–1; mensajes claros por campo
