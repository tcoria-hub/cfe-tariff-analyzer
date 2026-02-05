# Historia 2.3: Gráfica Comparativa de Cierres

## 🎯 Objetivo de la Sesión
Implementar Gráfica Comparativa de Cierres. Mostrar una gráfica de barras comparando diciembre de ambos años para visualizar fácilmente la diferencia entre periodos.

## 📝 Current Objective (Copiar a current_objective.md)
- [ ] Crear gráfica de barras agrupadas: una barra para dic año N, otra para dic año N-1
- [ ] Configurar eje Y con valor total en pesos
- [ ] Permitir comparar múltiples cargos (Fijo, Variable, Capacidad) si aplican
- [ ] Usar colores distintivos para cada año

## 🤖 Prompt para Cursor (Composer)

Implementa la Historia de Usuario HU-2.3 del Feature 2: Comparativo Diciembre vs Diciembre.

**Contexto:**
- Proyecto: CFE Tariff Analyzer - App de análisis de tarifas eléctricas
- Feature: Comparativo de Cierre "Diciembre vs Diciembre"
- Referencias: @.spec/BACKLOG.md (HU 2.3), @.spec/TECH_SPEC.md

**Historia de Usuario:**
- **Como:** Analista de costos
- **Quiero:** Ver una gráfica de barras comparando diciembre de ambos años
- **Para poder:** Visualizar fácilmente la diferencia entre periodos

**Criterios de Aceptación:**
1. Se muestra gráfica de barras agrupadas: una barra para dic año N, otra para dic año N-1
2. El eje Y muestra el valor total en pesos
3. Se pueden comparar múltiples cargos (Fijo, Variable, Capacidad) si aplican
4. La gráfica usa colores distintivos para cada año

**Requisitos Técnicos:**
- Usar plotly.express.bar con barmode="group"
- Agrupar por tipo de cargo
- Colores distintivos por año
- Hover con valores exactos

**Instrucciones:**
1. Preparar datos con cargo, año, total
2. Crear gráfica agrupada
3. Configurar interactividad

## 🧪 Pruebas de Aceptación
- [ ] **CP-2.3.1:** Para tarifa GDMTH, se muestran 4 barras: Fijo, Variable-Base, Variable-Intermedia, Variable-Punta
- [ ] **CP-2.3.2:** Para tarifa PDBT, se muestran 2 barras: Fijo y Variable
- [ ] **CP-2.3.3:** La gráfica es interactiva (hover muestra valores exactos)
