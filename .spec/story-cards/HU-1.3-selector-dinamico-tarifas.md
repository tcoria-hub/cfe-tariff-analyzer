# Historia 1.3: Selector Dinámico de Tarifas

## 🎯 Objetivo de la Sesión
Implementar Selector Dinámico de Tarifas. Permitir al usuario seleccionar el tipo de tarifa que desea analizar para ver los datos específicos de su contrato eléctrico.

## 📝 Current Objective (Copiar a current_objective.md)
- [ ] Crear `st.selectbox` con todas las tarifas disponibles
- [ ] Mostrar código y descripción (ej: "GDMTH - Gran demanda en media tensión horaria")
- [ ] Habilitar selector cuando hay División seleccionada
- [ ] Incluir tarifas: DB1, DB2, PDBT, GDBT, RABT, RAMT, APBT, APMT, GDMTO, GDMTH, DIST, DIT

## 🤖 Prompt para Cursor (Composer)

Implementa la Historia de Usuario HU-1.3 del Feature 1: Selector Geográfico y de Tarifas.

**Contexto:**
- Proyecto: CFE Tariff Analyzer - App de análisis de tarifas eléctricas
- Feature: Selector Geográfico y de Tarifas (Smart Locator)
- Referencias: @.spec/BACKLOG.md (HU 1.3), @.spec/TECH_SPEC.md

**Historia de Usuario:**
- **Como:** Usuario de la aplicación
- **Quiero:** Seleccionar el tipo de tarifa que deseo analizar
- **Para poder:** Ver los datos específicos de mi contrato eléctrico

**Criterios de Aceptación:**
1. Se muestra un `st.selectbox` con todas las tarifas disponibles en el sistema
2. Las tarifas muestran código y descripción (ej: "GDMTH - Gran demanda en media tensión horaria")
3. El selector se habilita cuando hay una División seleccionada
4. Las tarifas disponibles son: DB1, DB2, PDBT, GDBT, RABT, RAMT, APBT, APMT, GDMTO, GDMTH, DIST, DIT

**Requisitos Técnicos:**
- Consultar tarifas únicas de fact_tarifas con su descripción
- Formatear opciones como "CÓDIGO - Descripción"
- Usar st.session_state para almacenar selección

**Instrucciones:**
1. Obtener lista de tarifas únicas con descripción
2. Crear selectbox con formato legible
3. Almacenar tarifa seleccionada para queries posteriores

## 🧪 Pruebas de Aceptación
- [ ] **CP-1.3.1:** El selector muestra todas las tarifas con código y descripción
- [ ] **CP-1.3.2:** Al seleccionar "GDMTH", el sistema identifica que es tarifa horaria
- [ ] **CP-1.3.3:** Al seleccionar "PDBT", el sistema identifica que es tarifa simple (sin horarios)

**Formato BDD:**
```gherkin
Dado que: El usuario ha seleccionado Estado y Municipio
Cuando: Hace clic en el selector de Tarifas
Entonces: Ve una lista de tarifas con formato "CÓDIGO - Descripción"
```
