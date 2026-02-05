# Historia 1.2: Selector de Municipio con Mapeo a División

## 🎯 Objetivo de la Sesión
Implementar Selector de Municipio con Mapeo a División. Permitir al usuario seleccionar su municipio para que el sistema identifique automáticamente su División de CFE.

## 📝 Current Objective (Copiar a current_objective.md)
- [ ] Habilitar selector de municipios solo cuando hay estado seleccionado
- [ ] Filtrar municipios por estado seleccionado
- [ ] Almacenar internamente la División de CFE correspondiente al municipio
- [ ] Mostrar nombre de División al usuario (ej: "División: BAJÍO")

## 🤖 Prompt para Cursor (Composer)

Implementa la Historia de Usuario HU-1.2 del Feature 1: Selector Geográfico y de Tarifas.

**Contexto:**
- Proyecto: CFE Tariff Analyzer - App de análisis de tarifas eléctricas
- Feature: Selector Geográfico y de Tarifas (Smart Locator)
- Referencias: @.spec/BACKLOG.md (HU 1.2), @.spec/TECH_SPEC.md

**Historia de Usuario:**
- **Como:** Usuario de la aplicación
- **Quiero:** Seleccionar mi municipio después de elegir el estado
- **Para poder:** Que el sistema identifique automáticamente mi División de CFE

**Criterios de Aceptación:**
1. El selector de municipios se habilita solo cuando hay un estado seleccionado
2. Los municipios mostrados corresponden únicamente al estado seleccionado
3. Al seleccionar un municipio, se almacena internamente la División de CFE correspondiente
4. El nombre de la División se muestra como información al usuario (ej: "División: BAJÍO")

**Requisitos Técnicos:**
- Usar st.selectbox con disabled=True cuando no hay estado
- Consultar dim_geografia filtrando por estado
- Usar st.session_state para almacenar división
- Mostrar división con st.info o st.caption

**Instrucciones:**
1. Crear selectbox de municipios dependiente del estado
2. Implementar lookup de división al seleccionar municipio
3. Mostrar feedback visual de la división detectada
4. Preparar división para filtrar tarifas

## 🧪 Pruebas de Aceptación
- [ ] **CP-1.2.1:** Seleccionar estado "AGUASCALIENTES" y municipio "CALVILLO" muestra División "BAJÍO"
- [ ] **CP-1.2.2:** Seleccionar estado "BAJA CALIFORNIA" y municipio "MEXICALI" muestra División "BAJA CALIFORNIA"
- [ ] **CP-1.2.3:** El selector de municipio está deshabilitado si no hay estado seleccionado

**Formato BDD:**
```gherkin
Dado que: El usuario ha seleccionado el estado "AGUASCALIENTES"
Cuando: Selecciona el municipio "CALVILLO"
Entonces: El sistema muestra "División: BAJÍO" y almacena esta división para filtrar tarifas
```
