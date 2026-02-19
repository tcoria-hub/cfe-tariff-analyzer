# Historia 5.2: Navegación entre Modos de Análisis

## 🎯 Objetivo de la Sesión
Implementar Navegación entre Modos de Análisis. Poder navegar entre diferentes modos de análisis (generar histórico, análisis de comportamiento, captura de datos) para acceder a cada funcionalidad de forma organizada y sin confusión.

## 📝 Current Objective (Copiar a current_objective.md)
- [ ] Implementar sistema de navegación usando `st.tabs()` o `st.sidebar.radio()` para seleccionar modo activo
- [ ] Crear tab/modo "Generar Histórico" para vista del Feature 5 (tabla histórica de 12 meses)
- [ ] Crear tab/modo "Análisis de Comportamiento" para vista existente con gráficas comparativas (Features 2 y 3)
- [ ] Crear tab/modo "Captura de Datos de Recibo" como placeholder para Feature 6 (a implementar)
- [ ] Implementar lógica para mostrar solo el contenido del modo activo (ocultar otras vistas)
- [ ] Mantener estado de selectores (Estado, Municipio, Tarifa, Año) entre modos usando `st.session_state`
- [ ] Colocar selectores comunes fuera de los tabs para que sean accesibles desde cualquier modo
- [ ] Agregar iconos o etiquetas descriptivas para cada modo (ej: 📊, 📋, 📥)
- [ ] Indicar visualmente el modo activo (tab seleccionado o radio button marcado)
- [ ] Establecer "Análisis de Comportamiento" como modo por defecto para mantener compatibilidad

## 🤖 Prompt para Cursor (Composer)

Implementa la Historia de Usuario HU-5.2 del Feature 5: Histórico de Tarifas por Rango de 12 Meses.

**Contexto:**
- Proyecto: CFE Tariff Analyzer - App de análisis de tarifas eléctricas
- Feature: Histórico de Tarifas por Rango de 12 Meses
- Referencias: @.spec/BACKLOG.md (HU 5.2), @.spec/TECH_SPEC.md

**Historia de Usuario:**
- **Como:** Usuario de la aplicación
- **Quiero:** Poder navegar entre diferentes modos de análisis (generar histórico, análisis de comportamiento, captura de datos)
- **Para poder:** Acceder a cada funcionalidad de forma organizada y sin confusión

**Criterios de Aceptación:**
1. Se implementa un sistema de navegación que permite cambiar entre diferentes vistas/modos de la aplicación
2. Los modos disponibles son:
   - **"Generar Histórico"** - Vista del Feature 5 (tabla histórica de 12 meses)
   - **"Análisis de Comportamiento"** - Vista existente con gráficas comparativas (Features 2 y 3)
   - **"Captura de Datos de Recibo"** - Vista del Feature 6 (a implementar)
3. La navegación se implementa usando `st.tabs()` o `st.sidebar.radio()` para seleccionar el modo activo
4. Al cambiar de modo, solo se muestra el contenido correspondiente a ese modo (las otras vistas se ocultan)
5. El estado de los selectores (Estado, Municipio, Tarifa, Año) se mantiene entre modos cuando es aplicable
6. La navegación es clara y visible, con iconos o etiquetas descriptivas para cada modo
7. El modo activo se indica visualmente (ej: tab seleccionado o radio button marcado)

**Requisitos Técnicos:**
- Stack: Python 3.10+ (Streamlit), Pandas para ETL, Plotly Express para gráficas
- Componentes Streamlit: `st.tabs()` o `st.sidebar.radio()`, `st.session_state`
- Estructura recomendada:
  ```python
  modo = st.tabs(["📊 Análisis de Comportamiento", "📋 Generar Histórico", "📥 Captura de Datos"])
  with modo[0]:
      # Vista existente (Features 2 y 3)
  with modo[1]:
      # Vista Feature 5 (histórico)
  with modo[2]:
      # Vista Feature 6 (captura) - placeholder por ahora
  ```
- Mantener los selectores comunes (Estado, Municipio, Tarifa, Año) fuera de los tabs para que sean accesibles desde cualquier modo
- Usar `st.session_state` para mantener el estado de selecciones entre cambios de modo
- El modo por defecto debe ser "Análisis de Comportamiento" para mantener compatibilidad con usuarios existentes

**Instrucciones:**
1. Revisar criterios de aceptación y casos de prueba en BACKLOG.md (HU 5.2)
2. Revisar código existente en `scripts/app.py` para entender la estructura actual de la aplicación
3. Refactorizar la aplicación para separar las vistas en modos/tabs
4. Mover selectores comunes (Estado, Municipio, Tarifa, Año) fuera de los tabs
5. Implementar lógica de navegación con `st.tabs()` o `st.sidebar.radio()`
6. Envolver el contenido existente (Features 2 y 3) en el tab "Análisis de Comportamiento"
7. Crear tab "Generar Histórico" como placeholder (se implementará con HU-5.1)
8. Crear tab "Captura de Datos de Recibo" con mensaje "Próximamente" o placeholder para Feature 6
9. Usar `st.session_state` para mantener selecciones entre cambios de modo
10. Establecer "Análisis de Comportamiento" como modo por defecto
11. Mantener consistencia con código existente y no romper funcionalidad actual
12. Consultar @.spec/PRD.md y @.spec/TECH_SPEC.md si hay dudas

## 🧪 Pruebas de Aceptación
- [ ] **CP-5.2.1:** Al iniciar la aplicación, se muestra el modo "Análisis de Comportamiento" por defecto (vista existente)
- [ ] **CP-5.2.2:** Al hacer clic en el tab "Generar Histórico", se oculta la vista de análisis y se muestra la vista del histórico
- [ ] **CP-5.2.3:** Al hacer clic en el tab "Análisis de Comportamiento", se oculta la vista del histórico y se muestra la vista de análisis existente
- [ ] **CP-5.2.4:** Si el usuario selecciona Estado/Municipio/Tarifa en un modo, al cambiar a otro modo, esos selectores mantienen su valor (si aplican)
- [ ] **CP-5.2.5:** El tab "Captura de Datos de Recibo" está visible pero muestra mensaje "Próximamente" o contenido del Feature 6 cuando esté implementado
- [ ] **CP-5.2.6:** La navegación funciona correctamente en dispositivos móviles (responsive)

**Formato BDD:**
```gherkin
Dado que: El usuario está en la aplicación
Cuando: Ve la interfaz principal
Entonces: Ve un sistema de navegación con tabs o radio buttons para seleccionar modo
Y: Los modos disponibles son: "Generar Histórico", "Análisis de Comportamiento", "Captura de Datos de Recibo"

Escenario: Cambiar entre modos
Dado que: El usuario está en el modo "Análisis de Comportamiento"
Cuando: Hace clic en el tab "Generar Histórico"
Entonces: Se oculta la vista de análisis de comportamiento
Y: Se muestra la vista del histórico de 12 meses
Y: Los selectores de Estado/Municipio/Tarifa mantienen sus valores si aplican
```
