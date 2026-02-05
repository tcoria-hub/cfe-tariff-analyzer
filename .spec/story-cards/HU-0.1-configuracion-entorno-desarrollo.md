# Historia 0.1: Configuración del Entorno de Desarrollo

## 🎯 Objetivo de la Sesión
Implementar Configuración del Entorno de Desarrollo. Tener un entorno de desarrollo configurado con todas las dependencias para comenzar a desarrollar la aplicación sin problemas de configuración.

## 📝 Current Objective (Copiar a current_objective.md)
- [ ] Crear archivo `requirements.txt` con dependencias: streamlit, pandas, supabase, plotly
- [ ] Verificar que el entorno virtual se puede crear y activar correctamente
- [ ] Crear archivo `.env.example` con variables de entorno para Supabase
- [ ] Verificar que README.md incluye instrucciones de instalación

## 🤖 Prompt para Cursor (Composer)

Implementa la Historia de Usuario HU-0.1 del Feature 0: Configuración Inicial y ETL.

**Contexto:**
- Proyecto: CFE Tariff Analyzer - App de análisis de tarifas eléctricas
- Feature: Configuración Inicial y ETL
- Referencias: @.spec/BACKLOG.md (HU 0.1), @.spec/TECH_SPEC.md

**Historia de Usuario:**
- **Como:** Desarrollador
- **Quiero:** Tener un entorno de desarrollo configurado con todas las dependencias
- **Para poder:** Comenzar a desarrollar la aplicación sin problemas de configuración

**Criterios de Aceptación:**
1. Existe un archivo `requirements.txt` con las dependencias: streamlit, pandas, supabase, plotly
2. El entorno virtual se puede crear y activar correctamente
3. Existe un archivo `.env.example` con las variables de entorno necesarias para Supabase
4. El README.md incluye instrucciones de instalación

**Requisitos Técnicos:**
- Stack: Python 3.10+ (Streamlit), Pandas para ETL, Plotly Express para gráficas, Supabase (PostgreSQL)
- Componentes Streamlit: st.selectbox, st.metric, st.columns, st.plotly_chart
- Datos en `data/` (CSVs de catálogo y tarifas)

**Instrucciones:**
1. Revisar criterios de aceptación y casos de prueba en BACKLOG.md
2. Crear requirements.txt con versiones específicas
3. Crear .env.example con SUPABASE_URL y SUPABASE_KEY
4. Verificar que README.md tiene instrucciones claras
5. Consultar @.spec/PRD.md y @.spec/TECH_SPEC.md si hay dudas

## 🧪 Pruebas de Aceptación
- [ ] **CP-0.1.1:** Ejecutar `pip install -r requirements.txt` sin errores
- [ ] **CP-0.1.2:** Ejecutar `streamlit run scripts/app.py` muestra página de bienvenida
