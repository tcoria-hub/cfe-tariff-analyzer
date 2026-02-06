# Historia 1.5: Descripción Completa de Tarifa Seleccionada

## 🎯 Objetivo de la Sesión
Implementar Descripción Completa de Tarifa Seleccionada. Mostrar la descripción completa de la tarifa seleccionada para que el usuario entienda claramente qué tipo de tarifa está analizando sin memorizar códigos.

## 📝 Current Objective (Copiar a current_objective.md)
- [ ] Mostrar descripción completa de la tarifa encima de "Resumen de Tarifas"
- [ ] Incluir el nombre completo de la tarifa (ej: "Gran demanda baja tensión")
- [ ] Actualizar descripción dinámicamente al cambiar la tarifa seleccionada
- [ ] No mostrar descripción si no hay tarifa seleccionada
- [ ] Aplicar formato visual claro y destacado (negrita o estilo informativo)

## 🤖 Prompt para Cursor (Composer)

Implementa la Historia de Usuario HU-1.5 del Feature 1: Selector Geográfico y de Tarifas.

**Contexto:**
- Proyecto: CFE Tariff Analyzer - App de análisis de tarifas eléctricas
- Feature: Selector Geográfico y de Tarifas (Smart Locator)
- Referencias: @.spec/BACKLOG.md (HU 1.5), @.spec/TECH_SPEC.md

**Historia de Usuario:**
- **Como:** Usuario de la aplicación
- **Quiero:** Ver la descripción completa de la tarifa que he seleccionado
- **Para poder:** Entender claramente qué tipo de tarifa estoy analizando sin memorizar códigos

**Criterios de Aceptación:**
1. Al seleccionar una tarifa, se muestra su descripción completa encima de "Resumen de Tarifas"
2. La descripción incluye el nombre completo de la tarifa (ej: "Gran demanda baja tensión")
3. La descripción se actualiza dinámicamente al cambiar la tarifa seleccionada
4. Si no hay tarifa seleccionada, no se muestra descripción
5. El formato visual es claro y destacado (ej: texto en negrita o con estilo informativo)

**Catálogo de Tarifas (código → descripción):**
- DB1 → Doméstica de bajo consumo
- DB2 → Doméstica de alto consumo
- PDBT → Pequeña demanda baja tensión
- GDBT → Gran demanda baja tensión
- RABT → Riego agrícola baja tensión
- RAMT → Riego agrícola media tensión
- APBT → Alumbrado público baja tensión
- APMT → Alumbrado público media tensión
- GDMTO → Gran demanda en media tensión ordinaria
- GDMTH → Gran demanda en media tensión horaria
- DIST → Demanda industrial en subtransmisión
- DIT → Demanda industrial en transmisión

**Requisitos Técnicos:**
- Stack: Python 3.10+ (Streamlit), Pandas
- Usar `st.info()`, `st.markdown()` o similar para mostrar la descripción
- La descripción debe aparecer arriba de la sección "Resumen de Tarifas"
- Mantener consistencia con el estilo visual existente

**Instrucciones:**
1. Revisar dónde se renderiza "Resumen de Tarifas" en el código actual
2. Agregar un diccionario o función que mapee código de tarifa a descripción completa
3. Mostrar la descripción cuando hay tarifa seleccionada
4. Asegurar que se actualiza al cambiar de tarifa

## 🧪 Pruebas de Aceptación
- [ ] **CP-1.5.1:** Al seleccionar "GDBT", se muestra "Gran demanda baja tensión" arriba de "Resumen de Tarifas"
- [ ] **CP-1.5.2:** Al seleccionar "GDMTH", se muestra "Gran demanda en media tensión horaria"
- [ ] **CP-1.5.3:** Al seleccionar "PDBT", se muestra "Pequeña demanda baja tensión"
- [ ] **CP-1.5.4:** Al cambiar de tarifa, la descripción se actualiza inmediatamente

**Formato BDD:**
```gherkin
Dado que: El usuario ha seleccionado Estado, Municipio, Año y una Tarifa
Cuando: La pantalla de análisis se renderiza
Entonces: Muestra la descripción completa de la tarifa (ej: "Gran demanda baja tensión")
Y: La descripción aparece arriba de la sección "Resumen de Tarifas"
```
