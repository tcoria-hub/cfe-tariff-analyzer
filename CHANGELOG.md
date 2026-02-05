# Changelog - CFE Tariff Analyzer

Todos los cambios notables del proyecto serán documentados aquí.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/).

---

## [2026-02-05]

### HU-0.2: Carga y Gestión de Datos desde CSV
**Tiempo de ciclo:** ~45 minutos

#### Implementado
- Módulo `scripts/data_loader.py` con 10 funciones de carga y utilidades
- Normalización de texto (UPPER CASE, sin acentos) para match consistente
- Cache con `@st.cache_data` para optimizar rendimiento
- Estadísticas de carga en `app.py`

#### Decisiones Clave
- **Eliminación de Supabase:** Reemplazado por CSV locales (sin costos, despliegue simple)
- **Normalización de acentos:** BAJÍO → BAJIO para match entre tablas
- **Compatibilidad Python 3.9+:** Uso de `Optional[str]` en lugar de `str | None`

#### Archivos Modificados
- `scripts/data_loader.py` - Nuevo
- `scripts/app.py` - Actualizado con métricas
- `.spec/TECH_SPEC.md`, `.spec/PRD.md`, `README.md` - Sin Supabase
- `requirements.txt` - Eliminado supabase

---

### HU-0.1: Configuración del Entorno de Desarrollo
**Tiempo de ciclo:** ~1 hora

#### Implementado
- `requirements.txt` con dependencias: streamlit, pandas, supabase, plotly, python-dotenv
- `scripts/app.py` con página de bienvenida de la aplicación
- Verificación de `.env.example` y `README.md`

#### Decisiones Clave
- Versiones mínimas (>=) en requirements.txt para flexibilidad
- Agregado python-dotenv para manejo de variables de entorno

#### Archivos Modificados
- `requirements.txt` - Nuevo
- `scripts/app.py` - Nuevo

---

### Inicialización del Proyecto
- Creación de estructura de proyecto
- Definición de BACKLOG.md con 4 Features y 14 Historias de Usuario
- Configuración de workflow con comandos en `.spec/commands/`
- Documentación inicial: PRD.md, spec.md

---

<!-- Nuevas entradas se agregan arriba de esta línea -->
