# Historia 2.2: Desglose de Variación por Componente

## 🎯 Objetivo de la Sesión
Implementar Desglose de Variación por Componente. Mostrar cómo cada componente de la tarifa contribuyó a la variación total para identificar qué conceptos tuvieron mayor impacto.

## 📝 Current Objective (Copiar a current_objective.md)
- [ ] Crear tabla/gráfica con componentes: Generación, Transmisión, Distribución, CENACE, SCnMEM, Suministro, Capacidad
- [ ] Mostrar para cada componente: valor año N, valor año N-1, variación absoluta, variación %
- [ ] Ordenar componentes por impacto (mayor variación absoluta primero)
- [ ] Distinguir visualmente componentes que subieron vs bajaron

## 🤖 Prompt para Cursor (Composer)

Implementa la Historia de Usuario HU-2.2 del Feature 2: Comparativo Diciembre vs Diciembre.

**Contexto:**
- Proyecto: CFE Tariff Analyzer - App de análisis de tarifas eléctricas
- Feature: Comparativo de Cierre "Diciembre vs Diciembre"
- Referencias: @.spec/BACKLOG.md (HU 2.2), @.spec/TECH_SPEC.md

**Historia de Usuario:**
- **Como:** Analista de costos
- **Quiero:** Ver cómo cada componente de la tarifa contribuyó a la variación total
- **Para poder:** Identificar qué conceptos tuvieron mayor impacto en el incremento

**Criterios de Aceptación:**
1. Se muestra una tabla o gráfica de barras con los componentes: Generación, Transmisión, Distribución, CENACE, SCnMEM, Suministro, Capacidad
2. Para cada componente se muestra: valor año N, valor año N-1, variación absoluta, variación %
3. Los componentes se ordenan por impacto (mayor variación absoluta primero)
4. Se distinguen visualmente los componentes que subieron vs los que bajaron

**Columnas de componentes en fact_tarifas:**
- transmision, distribucion, cenace, suministro, scnmem, generacion, capacidad

**Requisitos Técnicos:**
- Usar plotly.express para gráfica de barras horizontal
- Colores: verde para bajó, rojo para subió
- Ordenar por abs(variación)

**Instrucciones:**
1. Extraer valores de cada componente para dic N y N-1
2. Calcular variaciones
3. Crear visualización ordenada por impacto

## 🧪 Pruebas de Aceptación
- [ ] **CP-2.2.1:** La suma de variaciones por componente coincide con la variación total
- [ ] **CP-2.2.2:** Para tarifas con cargo "Variable (Energía)", se muestran todos los componentes
- [ ] **CP-2.2.3:** Para tarifas con cargo "Capacidad", se muestran solo distribución, generación, capacidad

**Formato BDD:**
```gherkin
Dado que: El usuario visualiza el KPI de variación total
Cuando: Revisa la sección de desglose
Entonces: Ve una gráfica de barras mostrando el impacto de cada componente en la variación
```
