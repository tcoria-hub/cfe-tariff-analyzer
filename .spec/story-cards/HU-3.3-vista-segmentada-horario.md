# Historia 3.3: Vista Segmentada por Horario (Tarifas Horarias)

## 🎯 Objetivo de la Sesión
Implementar Vista Segmentada por Horario. Mostrar métricas separadas para Base, Intermedia y Punta para identificar en qué periodo horario hay mayor impacto de costos.

## 📝 Current Objective (Copiar a current_objective.md)
- [ ] Crear 3 columnas con `st.metric`: Base, Intermedia, Punta
- [ ] Mostrar promedio del periodo y variación vs año anterior en cada columna
- [ ] Incluir leyenda explicando horarios típicos de cada periodo
- [ ] Condicionar vista solo para tarifas identificadas como "horarias"

## 🤖 Prompt para Cursor (Composer)

Implementa la Historia de Usuario HU-3.3 del Feature 3: Análisis de Promedio Anual e Inteligencia Horaria.

**Contexto:**
- Proyecto: CFE Tariff Analyzer - App de análisis de tarifas eléctricas
- Feature: Análisis de Promedio Anual e Inteligencia Horaria
- Referencias: @.spec/BACKLOG.md (HU 3.3), @.spec/TECH_SPEC.md

**Historia de Usuario:**
- **Como:** Analista de tarifas horarias
- **Quiero:** Ver métricas separadas para Base, Intermedia y Punta
- **Para poder:** Identificar en qué periodo horario hay mayor impacto de costos

**Criterios de Aceptación:**
1. Se muestran 3 columnas con `st.metric`: Base, Intermedia, Punta
2. Cada columna muestra el promedio del periodo y su variación vs año anterior
3. Se incluye una leyenda explicando los horarios típicos de cada periodo
4. Esta vista solo se muestra para tarifas identificadas como "horarias"

**Horarios típicos (referencia):**
- Base: 0:00 - 6:00
- Intermedia: 6:00 - 18:00, 22:00 - 0:00
- Punta: 18:00 - 22:00

**Requisitos Técnicos:**
- Usar st.columns(3) para layout
- Filtrar por int_horario = 'B', 'I', 'P'
- Calcular promedio y delta por periodo
- Usar st.caption para leyenda

**Instrucciones:**
1. Verificar que tarifa es horaria
2. Calcular métricas por periodo
3. Renderizar 3 columnas con st.metric

## 🧪 Pruebas de Aceptación
- [ ] **CP-3.3.1:** Para GDMTH, se muestran 3 KPIs: Prom. Base, Prom. Intermedia, Prom. Punta
- [ ] **CP-3.3.2:** Cada KPI tiene su propio cálculo de variación independiente
- [ ] **CP-3.3.3:** Si un periodo no tiene datos, se muestra "N/A"
