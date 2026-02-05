# Historia 3.5: Vista Consolidada para Tarifas Simples

## 🎯 Objetivo de la Sesión
Implementar Vista Consolidada para Tarifas Simples. Mostrar los datos agrupados sin segmentación horaria para tarifas que no tienen periodos Base/Intermedia/Punta.

## 📝 Current Objective (Copiar a current_objective.md)
- [ ] Para tarifas sin horarios, mostrar solo: Cargo Fijo y Cargo Variable
- [ ] Ocultar columnas de Base/Intermedia/Punta
- [ ] Mostrar KPIs de promedio general del cargo variable
- [ ] Mostrar gráfica de tendencia con una sola línea por año (total)

## 🤖 Prompt para Cursor (Composer)

Implementa la Historia de Usuario HU-3.5 del Feature 3: Análisis de Promedio Anual e Inteligencia Horaria.

**Contexto:**
- Proyecto: CFE Tariff Analyzer - App de análisis de tarifas eléctricas
- Feature: Análisis de Promedio Anual e Inteligencia Horaria
- Referencias: @.spec/BACKLOG.md (HU 3.5), @.spec/TECH_SPEC.md

**Historia de Usuario:**
- **Como:** Usuario con tarifa simple (sin horarios)
- **Quiero:** Ver los datos agrupados sin segmentación horaria
- **Para poder:** Tener una vista limpia y sin información irrelevante

**Criterios de Aceptación:**
1. Para tarifas sin horarios, se muestra solo: Cargo Fijo y Cargo Variable
2. No se muestran columnas de Base/Intermedia/Punta
3. Los KPIs muestran promedio general del cargo variable
4. La gráfica de tendencia muestra una sola línea por año (total)

**Lógica condicional:**
```python
if not es_tarifa_horaria:
    # Mostrar vista simplificada
    # 2 KPIs: Fijo y Variable
    # 1 línea de tendencia por año
```

**Requisitos Técnicos:**
- Usar flag de HU-3.2 para condicionar vista
- Filtrar por cargo = 'Fijo' o 'Variable (Energía)'
- Simplificar gráficas y métricas

**Instrucciones:**
1. Verificar que tarifa es simple
2. Filtrar datos por tipo de cargo
3. Renderizar vista simplificada

## 🧪 Pruebas de Aceptación
- [ ] **CP-3.5.1:** Para tarifa PDBT, la interfaz no muestra sección de "Análisis por Horario"
- [ ] **CP-3.5.2:** Solo se muestran 2 KPIs: Cargo Fijo Promedio, Cargo Variable Promedio
- [ ] **CP-3.5.3:** La gráfica de tendencia usa el valor `total` sin desagregar
