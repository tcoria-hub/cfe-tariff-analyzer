# CFE Tariff Analyzer

Aplicación web interactiva para el análisis de tarifas de CFE (Comisión Federal de Electricidad) en México.

## Descripción

Esta herramienta permite a usuarios finales y analistas:
- Consultar tarifas eléctricas por ubicación geográfica (Estado → Municipio → División CFE)
- Comparar costos de cierre anual (Diciembre vs Diciembre)
- Analizar promedios anuales con detección automática de estructura horaria
- Visualizar tendencias mensuales y desglose por componentes tarifarios

## Stack Tecnológico

- **Python 3.10+** - Lenguaje principal
- **Streamlit** - Framework web para dashboards
- **Pandas** - Procesamiento y análisis de datos
- **Plotly Express** - Visualizaciones interactivas
- **Streamlit Cloud** - Despliegue gratuito

## Instalación

```bash
# Clonar repositorio
git clone <repo-url>
cd cfe-analisis-app

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

## Uso

```bash
# Ejecutar aplicación
streamlit run scripts/app.py
```

## Estructura del Proyecto

```
cfe-analisis-app/
├── .spec/                    # Documentación y workflow
│   ├── PRD.md               # Product Requirements Document
│   ├── TECH_SPEC.md         # Especificación técnica
│   ├── BACKLOG.md           # Backlog con Features e Historias de Usuario
│   ├── commands/            # Comandos de workflow (prompts para Cursor)
│   ├── story-cards/         # Story cards generadas
│   └── history/             # Objetivos completados
├── scripts/                  # Scripts de Python
│   ├── app.py               # Aplicación Streamlit principal
│   └── upload_data.py       # ETL para carga a Supabase
├── data/                     # Datos fuente
│   ├── 01_catalogo_regiones.csv      # ~2,600 municipios con división CFE
│   └── 02_tarifas_finales_suministro_basico.csv  # Histórico de tarifas
├── current_objective.md      # Objetivo de trabajo actual
├── CHANGELOG.md              # Historial de cambios
└── README.md                 # Este archivo
```

## Workflow de Desarrollo

Este proyecto utiliza un flujo basado en Historias de Usuario. Ver `.spec/commands/README.md` para detalles.

```bash
# Generar story cards desde el backlog
@generate-story-cards

# Iniciar trabajo en una historia
@start-objective HU-1.1

# Finalizar historia completada
@finish-objective
```

## Documentación

- [PRD - Requisitos del Producto](.spec/PRD.md)
- [Especificación Técnica](.spec/TECH_SPEC.md)
- [Backlog de Historias](.spec/BACKLOG.md)

## Tarifas Soportadas

| Código | Descripción |
|--------|-------------|
| DB1, DB2 | Doméstico baja tensión |
| PDBT | Pequeña demanda baja tensión |
| GDBT | Gran demanda baja tensión |
| GDMTO | Gran demanda media tensión ordinaria |
| GDMTH | Gran demanda media tensión horaria |
| DIST, DIT | Demanda industrial |
| RABT, RAMT | Riego agrícola |
| APBT, APMT | Alumbrado público |

## Licencia

Proyecto personal - Uso interno.
