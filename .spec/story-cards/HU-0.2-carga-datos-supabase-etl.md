# Historia 0.2: Carga de Datos a Supabase (ETL)

## 🎯 Objetivo de la Sesión
Implementar Carga de Datos a Supabase (ETL). Cargar los CSVs de catálogo y tarifas a Supabase para tener una fuente de datos persistente y consultable.

## 📝 Current Objective (Copiar a current_objective.md)
- [ ] Crear tabla `dim_geografia` con columnas: estado, municipio, division
- [ ] Crear tabla `fact_tarifas` con todas las columnas del CSV
- [ ] Normalizar nombres de regiones (case-insensitive match entre tablas)
- [ ] Implementar script `upload_data.py` idempotente (sin duplicados)
- [ ] Verificar que el join entre tablas funciona correctamente

## 🤖 Prompt para Cursor (Composer)

Implementa la Historia de Usuario HU-0.2 del Feature 0: Configuración Inicial y ETL.

**Contexto:**
- Proyecto: CFE Tariff Analyzer - App de análisis de tarifas eléctricas
- Feature: Configuración Inicial y ETL
- Referencias: @.spec/BACKLOG.md (HU 0.2), @.spec/TECH_SPEC.md

**Historia de Usuario:**
- **Como:** Desarrollador
- **Quiero:** Cargar los CSVs de catálogo y tarifas a Supabase
- **Para poder:** Tener una fuente de datos persistente y consultable

**Criterios de Aceptación:**
1. Existe tabla `dim_geografia` con columnas: estado, municipio, division
2. Existe tabla `fact_tarifas` con columnas: anio, mes, tarifa, descripcion, int_horario, cargo, unidades, region, transmision, distribucion, cenace, suministro, scnmem, generacion, capacidad, total
3. Los nombres de regiones están normalizados (case-insensitive match entre tablas)
4. El script `upload_data.py` es idempotente (puede ejecutarse múltiples veces sin duplicar)

**Datos fuente:**
- `data/01_catalogo_regiones.csv` - ~2,600 registros de Estado, Municipio, División
- `data/02_tarifas_finales_suministro_basico.csv` - Histórico de tarifas

**Requisitos Técnicos:**
- Usar biblioteca `supabase-py` para conexión
- Leer credenciales desde variables de entorno (.env)
- Implementar upsert o delete+insert para idempotencia
- Normalizar: convertir regiones a UPPER CASE para match consistente

**Instrucciones:**
1. Crear script `scripts/upload_data.py`
2. Leer CSVs con pandas
3. Normalizar datos (regiones, meses)
4. Conectar a Supabase y subir datos
5. Verificar con queries de prueba

## 🧪 Pruebas de Aceptación
- [ ] **CP-0.2.1:** Consultar `dim_geografia` retorna ~2,600 registros
- [ ] **CP-0.2.2:** Consultar `fact_tarifas` retorna todos los registros del CSV
- [ ] **CP-0.2.3:** Join entre tablas por division/region funciona correctamente
