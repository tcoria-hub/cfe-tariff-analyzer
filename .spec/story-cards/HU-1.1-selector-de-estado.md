# Historia 1.1: Selector de Estado

## 🎯 Objetivo de la Sesión
Implementar Selector de Estado. Permitir al usuario seleccionar su estado de la República Mexicana para filtrar los municipios disponibles en su zona.

## 📝 Current Objective (Copiar a current_objective.md)
- [ ] Crear `st.selectbox` con todos los estados únicos del catálogo
- [ ] Ordenar estados alfabéticamente
- [ ] Agregar opción por defecto "Selecciona un estado"
- [ ] Implementar actualización del selector de municipios al cambiar estado

## 🤖 Prompt para Cursor (Composer)

Implementa la Historia de Usuario HU-1.1 del Feature 1: Selector Geográfico y de Tarifas.

**Contexto:**
- Proyecto: CFE Tariff Analyzer - App de análisis de tarifas eléctricas
- Feature: Selector Geográfico y de Tarifas (Smart Locator)
- Referencias: @.spec/BACKLOG.md (HU 1.1), @.spec/TECH_SPEC.md

**Historia de Usuario:**
- **Como:** Usuario de la aplicación
- **Quiero:** Seleccionar mi estado de la República Mexicana
- **Para poder:** Filtrar los municipios disponibles en mi zona

**Criterios de Aceptación:**
1. Se muestra un `st.selectbox` con todos los estados únicos del catálogo
2. Los estados están ordenados alfabéticamente
3. Existe una opción por defecto "Selecciona un estado"
4. Al cambiar el estado, se actualiza el selector de municipios

**Requisitos Técnicos:**
- Stack: Python 3.10+ (Streamlit), Pandas, Supabase
- Usar st.selectbox para el selector
- Consultar tabla `dim_geografia` de Supabase
- Usar st.session_state para mantener selección

**Instrucciones:**
1. Conectar a Supabase y obtener estados únicos
2. Crear selectbox con placeholder
3. Implementar callback para actualizar municipios
4. Mantener consistencia con código existente

## 🧪 Pruebas de Aceptación
- [ ] **CP-1.1.1:** El selector muestra 32 estados de la República
- [ ] **CP-1.1.2:** Al seleccionar "AGUASCALIENTES", el selector de municipios muestra 11 opciones
- [ ] **CP-1.1.3:** Al seleccionar "BAJA CALIFORNIA", el selector de municipios muestra 5 opciones

**Formato BDD:**
```gherkin
Dado que: El usuario está en la página principal
Cuando: Hace clic en el selector de Estado
Entonces: Ve una lista de 32 estados ordenados alfabéticamente
```
