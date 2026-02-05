# Historia 3.2: Detección Automática de Estructura Horaria

## 🎯 Objetivo de la Sesión
Implementar Detección Automática de Estructura Horaria. El sistema debe identificar automáticamente si la tarifa seleccionada tiene cargos horarios para adaptar la interfaz.

## 📝 Current Objective (Copiar a current_objective.md)
- [ ] Detectar valores en columna `int_horario`: B (Base), I (Intermedia), P (Punta)
- [ ] Marcar tarifa como "horaria" si tiene registros con B, I, P
- [ ] Marcar tarifa como "simple" si solo tiene "sin dato"
- [ ] Implementar detección automática al seleccionar tarifa

## 🤖 Prompt para Cursor (Composer)

Implementa la Historia de Usuario HU-3.2 del Feature 3: Análisis de Promedio Anual e Inteligencia Horaria.

**Contexto:**
- Proyecto: CFE Tariff Analyzer - App de análisis de tarifas eléctricas
- Feature: Análisis de Promedio Anual e Inteligencia Horaria
- Referencias: @.spec/BACKLOG.md (HU 3.2), @.spec/TECH_SPEC.md

**Historia de Usuario:**
- **Como:** Sistema
- **Quiero:** Identificar automáticamente si la tarifa seleccionada tiene cargos horarios
- **Para poder:** Adaptar la interfaz y mostrar desgloses por Base, Intermedia y Punta

**Criterios de Aceptación:**
1. El sistema detecta valores en la columna `int_horario`: B (Base), I (Intermedia), P (Punta)
2. Si la tarifa tiene registros con B, I, P → se marca como "tarifa horaria"
3. Si la tarifa solo tiene "sin dato" en int_horario → se marca como "tarifa simple"
4. La detección ocurre automáticamente al seleccionar la tarifa

**Lógica de detección:**
```python
horarios_unicos = df[df.tarifa == selected]['int_horario'].unique()
es_horaria = any(h in ['B', 'I', 'P'] for h in horarios_unicos)
```

**Requisitos Técnicos:**
- Consultar int_horario para la tarifa seleccionada
- Almacenar resultado en st.session_state
- Usar para condicionar renderizado de componentes

**Instrucciones:**
1. Al cambiar tarifa, consultar int_horario únicos
2. Determinar tipo de tarifa
3. Almacenar flag para uso en otras historias

## 🧪 Pruebas de Aceptación
- [ ] **CP-3.2.1:** Seleccionar "GDMTH" activa vista horaria (Base, Intermedia, Punta)
- [ ] **CP-3.2.2:** Seleccionar "PDBT" muestra vista simple (sin segmentación horaria)
- [ ] **CP-3.2.3:** Seleccionar "DIST" activa vista horaria (tiene B, I, P)

**Formato BDD:**
```gherkin
Dado que: El usuario selecciona tarifa "GDMTH"
Cuando: El sistema analiza la estructura de datos
Entonces: Identifica int_horario = [B, I, P] y activa modo "tarifa horaria"
```
