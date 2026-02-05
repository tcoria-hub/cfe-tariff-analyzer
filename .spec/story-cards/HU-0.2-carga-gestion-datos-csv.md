# Historia 0.2: Carga y Gestión de Datos desde CSV

> **NOTA:** Esta historia fue modificada el 2026-02-05 para eliminar Supabase del stack.
> Ver sección "Decisiones de Arquitectura" al final.

## 🎯 Objetivo de la Sesión
Implementar la carga de datos desde archivos CSV locales. Crear un módulo de carga de datos reutilizable con cache para optimizar rendimiento.

## 📝 Current Objective (Copiar a current_objective.md)
- [ ] Crear módulo `scripts/data_loader.py` con funciones de carga
- [ ] Implementar carga de `data/01_catalogo_regiones.csv` con normalización
- [ ] Implementar carga de `data/02_tarifas_finales_suministro_basico.csv` con normalización
- [ ] Usar `@st.cache_data` para optimizar rendimiento
- [ ] Integrar carga de datos en `app.py`
- [ ] Verificar que el join entre geografía y tarifas funciona

## 🤖 Prompt para Cursor (Composer)

Implementa la Historia de Usuario HU-0.2 del Feature 0: Configuración Inicial y ETL.

**Contexto:**
- Proyecto: CFE Tariff Analyzer - App de análisis de tarifas eléctricas
- Feature: Configuración Inicial y ETL
- Referencias: @.spec/BACKLOG.md (HU 0.2), @.spec/TECH_SPEC.md

**Historia de Usuario:**
- **Como:** Desarrollador
- **Quiero:** Implementar la carga de datos desde archivos CSV locales
- **Para poder:** Tener los datos disponibles en la aplicación sin dependencias externas

**Criterios de Aceptación:**
1. La app carga automáticamente `data/01_catalogo_regiones.csv` al iniciar
2. La app carga automáticamente `data/02_tarifas_finales_suministro_basico.csv` al iniciar
3. Los nombres de regiones están normalizados (UPPER CASE para match consistente)
4. Existe un módulo `scripts/data_loader.py` con funciones reutilizables
5. Los DataFrames se cachean con `@st.cache_data` para optimizar rendimiento

**Datos fuente:**
- `data/01_catalogo_regiones.csv` - ~2,600 registros (Estado, Municipio, División)
- `data/02_tarifas_finales_suministro_basico.csv` - ~62,000+ registros de tarifas

**Requisitos Técnicos:**
- Crear `scripts/data_loader.py` con funciones:
  - `load_geografia()` → DataFrame con estado, municipio, division (UPPER CASE)
  - `load_tarifas()` → DataFrame con región normalizada (UPPER CASE)
  - `get_estados()` → Lista de estados únicos
  - `get_municipios(estado)` → Lista de municipios para un estado
  - `get_division(estado, municipio)` → División correspondiente
- Usar `@st.cache_data` en todas las funciones de carga
- Limpiar columnas vacías del CSV de geografía
- Manejar valores vacíos en columnas numéricas

**Instrucciones:**
1. Crear `scripts/data_loader.py`
2. Implementar funciones de carga con cache
3. Normalizar datos (regiones a UPPER CASE)
4. Integrar en `app.py` mostrando estadísticas de carga
5. Verificar que los datos se cargan correctamente

## 🧪 Pruebas de Aceptación
- [ ] **CP-0.2.1:** Al iniciar la app, se cargan ~2,600 registros de geografía
- [ ] **CP-0.2.2:** Al iniciar la app, se cargan todos los registros de tarifas (~62,000+)
- [ ] **CP-0.2.3:** El join entre geografía y tarifas por division/region funciona correctamente

## 📋 Decisiones de Arquitectura (2026-02-05)

### Cambio: Eliminación de Supabase

**Decisión:** Usar CSV locales en lugar de Supabase como fuente de datos.

**Razones:**
1. El usuario ya tiene 2 proyectos en Supabase (límite gratuito)
2. Simplifica el despliegue en Streamlit Cloud
3. Los datos se actualizan solo una vez al mes (no requiere BD)
4. La usuaria final no necesita acceso al código, solo a la app

**Implicaciones:**
- Los CSVs viven en el repositorio
- Actualizaciones mensuales vía `st.file_uploader` (historia futura)
- Sin costos de base de datos
- Despliegue más simple

**Trade-offs:**
- (+) Sin costos, sin configuración de BD
- (+) Despliegue instantáneo en Streamlit Cloud
- (-) Datos no persisten entre sesiones si se suben via uploader
- (-) Para persistir cambios, hay que actualizar el repo

**Mitigación del trade-off:**
- Se agregará una historia para que la usuaria pueda subir CSV actualizado
- El desarrollador puede hacer commit del CSV nuevo cuando sea necesario
