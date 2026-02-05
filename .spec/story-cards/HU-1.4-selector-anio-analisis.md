# Historia 1.4: Selector de Año de Análisis

## 🎯 Objetivo de la Sesión
Implementar Selector de Año de Análisis. Permitir al usuario seleccionar el año que desea analizar para comparar contra el año anterior.

## 📝 Current Objective (Copiar a current_objective.md)
- [ ] Crear `st.selectbox` con años disponibles en los datos
- [ ] Establecer año mínimo como 2018 (para comparar con 2017)
- [ ] Detectar año máximo disponible en la base de datos
- [ ] Calcular automáticamente año comparativo (año - 1)

## 🤖 Prompt para Cursor (Composer)

Implementa la Historia de Usuario HU-1.4 del Feature 1: Selector Geográfico y de Tarifas.

**Contexto:**
- Proyecto: CFE Tariff Analyzer - App de análisis de tarifas eléctricas
- Feature: Selector Geográfico y de Tarifas (Smart Locator)
- Referencias: @.spec/BACKLOG.md (HU 1.4), @.spec/TECH_SPEC.md

**Historia de Usuario:**
- **Como:** Usuario de la aplicación
- **Quiero:** Seleccionar el año que deseo analizar
- **Para poder:** Comparar ese año contra el año anterior

**Criterios de Aceptación:**
1. Se muestra un `st.selectbox` con los años disponibles en los datos
2. El año mínimo seleccionable es 2018 (para poder comparar con 2017)
3. El año máximo es el último disponible en la base de datos
4. Al seleccionar un año, se calcula automáticamente el año comparativo (año - 1)

**Requisitos Técnicos:**
- Consultar años únicos de fact_tarifas
- Filtrar años >= 2018
- Mostrar año comparativo como información adicional
- Usar st.session_state para ambos años

**Instrucciones:**
1. Obtener rango de años disponibles
2. Crear selectbox con años válidos
3. Mostrar mensaje "Comparando con [año-1]"

## 🧪 Pruebas de Aceptación
- [ ] **CP-1.4.1:** El selector muestra años desde 2018 hasta el año más reciente
- [ ] **CP-1.4.2:** Seleccionar 2024 establece año comparativo como 2023
- [ ] **CP-1.4.3:** El año 2017 no está disponible para selección (no hay año anterior)

**Formato BDD:**
```gherkin
Dado que: El usuario ha completado los selectores anteriores
Cuando: Selecciona el año "2024"
Entonces: El sistema establece 2024 como año de análisis y 2023 como año de comparación
```
