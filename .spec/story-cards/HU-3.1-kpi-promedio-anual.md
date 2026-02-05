# Historia 3.1: KPI de Promedio Anual

## 🎯 Objetivo de la Sesión
Implementar KPI de Promedio Anual. Mostrar el promedio mensual del año seleccionado vs el año anterior para entender la tendencia general del costo energético.

## 📝 Current Objective (Copiar a current_objective.md)
- [ ] Calcular media aritmética de todos los meses disponibles del año seleccionado
- [ ] Comparar contra la media del mismo periodo del año anterior
- [ ] Mostrar `st.metric` con promedio y delta %
- [ ] Manejar caso de años con diferente número de meses disponibles

## 🤖 Prompt para Cursor (Composer)

Implementa la Historia de Usuario HU-3.1 del Feature 3: Análisis de Promedio Anual e Inteligencia Horaria.

**Contexto:**
- Proyecto: CFE Tariff Analyzer - App de análisis de tarifas eléctricas
- Feature: Análisis de Promedio Anual e Inteligencia Horaria
- Referencias: @.spec/BACKLOG.md (HU 3.1), @.spec/TECH_SPEC.md

**Historia de Usuario:**
- **Como:** Analista de costos
- **Quiero:** Ver el promedio mensual del año seleccionado vs el año anterior
- **Para poder:** Entender la tendencia general del costo energético

**Criterios de Aceptación:**
1. Se calcula la media aritmética de todos los meses disponibles del año seleccionado
2. Se compara contra la media del mismo periodo del año anterior
3. Se muestra `st.metric` con el promedio y delta %
4. Si un año tiene menos meses disponibles, se comparan solo los meses coincidentes

**Fórmula:**
```python
promedio_N = df[df.anio == N]['total'].mean()
promedio_N1 = df[df.anio == N-1]['total'].mean()
variacion = ((promedio_N / promedio_N1) - 1) * 100
```

**Requisitos Técnicos:**
- Usar pandas mean() para cálculo
- Considerar solo meses que existen en ambos años para comparación justa
- Mostrar número de meses usados en el cálculo

**Instrucciones:**
1. Filtrar datos por año, región, tarifa
2. Calcular promedios
3. Renderizar st.metric

## 🧪 Pruebas de Aceptación
- [ ] **CP-3.1.1:** Si año 2024 tiene datos de ene-dic y 2023 igual, se promedian los 12 meses
- [ ] **CP-3.1.2:** Si año 2024 tiene datos de ene-sep, se compara contra ene-sep de 2023
- [ ] **CP-3.1.3:** El cálculo es: promedio_N = mean(total para todos los meses de año N)

**Formato BDD:**
```gherkin
Dado que: El usuario ha seleccionado una tarifa y año
Cuando: El sistema calcula métricas
Entonces: Muestra "Promedio Anual: $X.XX" con delta vs año anterior
```
