# Technical Specification: CFE-Tariff-App

## 1. Stack Tecnológico
* **Lenguaje:** Python 3.10+
* **Web Framework:** Streamlit (para la interfaz dinámica).
* **Data Engine:** Pandas (limpieza y agregaciones).
* **Base de Datos:** Supabase (Postgres) para almacenamiento persistente.
* **Gráficos:** Plotly Express.

## 2. Modelo de Datos (Esquema en Supabase)
### Tabla: `dim_geografia`
* `estado` (text)
* `municipio` (text)
* `division` (text) -> Llave de unión con tarifas.

### Tabla: `fact_tarifas`
* `anio` (int)
* `mes` (text)
* `tarifa` (text)
* `region` (text) -> Match con `division`.
* `int_horario` (text) -> [Base, Intermedia, Punta, sin dato].
* `cargo` (text) -> [Fijo, Variable, Capacidad].
* `total` (float)

## 3. Lógica de Negocio (Pseudocódigo)
1.  **Carga:** Al iniciar, la app descarga el catálogo de municipios de Supabase.
2.  **Filtrado:**
    `df_actual = df[(df.anio == selected_year) & (df.region == selected_div) & (df.tarifa == selected_tar)]`
    `df_prev = df[(df.anio == selected_year - 1) ...]`
3.  **Cálculo de Métricas:**
    * `Metric_Dic = (Total_Dic_N / Total_Dic_N-1) - 1`
    * `Metric_Avg = (Mean_N / Mean_N-1) - 1`

## 4. Normalización Necesaria
* Convertir meses ("enero", "febrero"...) a formato título o minúsculas uniforme.
* Asegurar que los nombres de las regiones en `fact_tarifas` coincidan con `dim_geografia` (ej: "BAJA CALIFORNIA" vs "Baja California").
