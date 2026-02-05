# Historia 2.1: KPI de Variación Total Diciembre

## 🎯 Objetivo de la Sesión
Implementar KPI de Variación Total Diciembre. Mostrar el porcentaje de variación del total de diciembre año N vs año N-1 para conocer rápidamente el incremento o decremento anual.

## 📝 Current Objective (Copiar a current_objective.md)
- [ ] Crear tarjeta `st.metric` con valor total de diciembre del año seleccionado
- [ ] Calcular y mostrar delta (variación %) respecto al año anterior
- [ ] Configurar colores: rojo/alza para incremento, verde/baja para decremento
- [ ] Manejar caso de "Datos no disponibles" si falta información

## 🤖 Prompt para Cursor (Composer)

Implementa la Historia de Usuario HU-2.1 del Feature 2: Comparativo Diciembre vs Diciembre.

**Contexto:**
- Proyecto: CFE Tariff Analyzer - App de análisis de tarifas eléctricas
- Feature: Comparativo de Cierre "Diciembre vs Diciembre"
- Referencias: @.spec/BACKLOG.md (HU 2.1), @.spec/TECH_SPEC.md

**Historia de Usuario:**
- **Como:** Analista de costos
- **Quiero:** Ver el porcentaje de variación del total de diciembre año N vs año N-1
- **Para poder:** Conocer rápidamente el incremento o decremento anual

**Criterios de Aceptación:**
1. Se muestra una tarjeta `st.metric` con el valor total de diciembre del año seleccionado
2. Se muestra el delta (variación %) respecto al año anterior
3. El delta es positivo (rojo/alza) si hubo incremento, negativo (verde/baja) si hubo decremento
4. Si no existen datos de diciembre para algún año, se muestra mensaje de "Datos no disponibles"

**Fórmula de cálculo:**
```python
variacion_pct = ((total_dic_N / total_dic_N-1) - 1) * 100
```

**Requisitos Técnicos:**
- Usar st.metric con parámetros value y delta
- Configurar delta_color="inverse" para que alza sea rojo
- Filtrar por mes="diciembre", tarifa, region, año

**Instrucciones:**
1. Filtrar datos de diciembre para año N y N-1
2. Calcular totales y variación
3. Renderizar st.metric con formato adecuado

## 🧪 Pruebas de Aceptación
- [ ] **CP-2.1.1:** Para GDMTH, División Bajío, año 2024, el KPI muestra el total de dic-2024 vs dic-2023
- [ ] **CP-2.1.2:** La variación % se calcula como: ((total_dic_N / total_dic_N-1) - 1) * 100
- [ ] **CP-2.1.3:** Si total_dic_2023 = 1.00 y total_dic_2024 = 1.05, el delta muestra +5.0%

**Formato BDD:**
```gherkin
Dado que: El usuario ha seleccionado División "BAJÍO", Tarifa "GDMTH", Año 2024
Cuando: El sistema carga los datos
Entonces: Muestra una tarjeta con "Total Diciembre: $X.XX" y delta "+Y.Y%"
```
