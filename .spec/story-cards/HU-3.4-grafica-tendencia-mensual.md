# Historia 3.4: Gráfica de Tendencia Mensual

## 🎯 Objetivo de la Sesión
Implementar Gráfica de Tendencia Mensual. Mostrar una gráfica de líneas con la evolución mensual de ambos años para identificar patrones estacionales y anomalías.

## 📝 Current Objective (Copiar a current_objective.md)
- [ ] Crear gráfica de líneas con eje X = meses (Ene-Dic), eje Y = valor total
- [ ] Mostrar dos líneas: año seleccionado y año anterior
- [ ] Usar colores distintivos con leyenda clara
- [ ] Implementar hover con mes y valor exacto

## 🤖 Prompt para Cursor (Composer)

Implementa la Historia de Usuario HU-3.4 del Feature 3: Análisis de Promedio Anual e Inteligencia Horaria.

**Contexto:**
- Proyecto: CFE Tariff Analyzer - App de análisis de tarifas eléctricas
- Feature: Análisis de Promedio Anual e Inteligencia Horaria
- Referencias: @.spec/BACKLOG.md (HU 3.4), @.spec/TECH_SPEC.md

**Historia de Usuario:**
- **Como:** Analista de costos
- **Quiero:** Ver una gráfica de líneas con la evolución mensual de ambos años
- **Para poder:** Identificar patrones estacionales y anomalías

**Criterios de Aceptación:**
1. Se muestra gráfica de líneas con eje X = meses (Ene-Dic), eje Y = valor total
2. Dos líneas: año seleccionado y año anterior
3. Las líneas usan colores distintivos con leyenda clara
4. Hover sobre puntos muestra mes y valor exacto

**Orden de meses:**
```python
MESES_ORDEN = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
               'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
```

**Requisitos Técnicos:**
- Usar plotly.express.line
- Ordenar meses cronológicamente
- Configurar hover template
- Manejar meses faltantes (gaps en línea)

**Instrucciones:**
1. Preparar datos con mes ordenado
2. Crear líneas por año
3. Configurar interactividad y estilos

## 🧪 Pruebas de Aceptación
- [ ] **CP-3.4.1:** La gráfica muestra 12 puntos por año (uno por mes)
- [ ] **CP-3.4.2:** Si un mes no tiene datos, la línea se interrumpe o muestra null
- [ ] **CP-3.4.3:** El orden de meses es cronológico: Enero → Diciembre

**Formato BDD:**
```gherkin
Dado que: El usuario ha seleccionado filtros completos
Cuando: Se renderiza la sección de análisis
Entonces: Ve una gráfica de líneas comparando tendencia mensual de ambos años
```
