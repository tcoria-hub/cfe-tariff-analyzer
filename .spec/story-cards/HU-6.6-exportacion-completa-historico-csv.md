# Historia 6.6: Exportación completa del histórico a CSV

## 🎯 Objetivo de la Sesión
Implementar Exportación completa del histórico a CSV. Exportar todos los recibos capturados a un archivo CSV para analizarlos en herramientas externas.

## 📝 Current Objective (Copiar a current_objective.md)
- [ ] Leer todos los registros de data/recibos_capturados.csv (o de la fuente que use la app tras carga)
- [ ] Construir CSV con todas las columnas de datos generales + unión de todas las columnas posibles de datos tarifarios (de todos los esquemas)
- [ ] Para cada recibo, rellenar solo las columnas que apliquen a su tarifa; el resto dejarlas vacías
- [ ] Incluir la totalidad de los registros almacenados; formato compatible con Excel (UTF-8, separador estándar)
- [ ] Ofrecer botón "Exportar histórico a CSV" o similar; descarga con st.download_button sin alterar datos originales
- [ ] Nombre de archivo sugerido: ej. recibos_historico_YYYYMMDD.csv

## 🤖 Prompt para Cursor (Composer)

Implementa la Historia de Usuario HU-6.6 del Feature 6: Captura Manual y Exportación de Recibos de Luz CFE.

**Contexto:**
- Proyecto: CFE Tariff Analyzer
- Feature: Captura Manual y Exportación de Recibos de Luz CFE
- Referencias: @.spec/BACKLOG.md (HU 6.6), @.spec/TECH_SPEC.md

**Historia de Usuario:**
- **Como:** Analista
- **Quiero:** Exportar todos los recibos capturados a un archivo CSV
- **Para poder:** Analizarlos en herramientas externas

**Consideración:** Los recibos no comparten todos los mismos campos; la estructura depende de la tarifa.

**Criterios de Aceptación:**
1. El CSV incluye todas las columnas de datos generales
2. El CSV incluye todas las columnas posibles de datos tarifarios (unión de esquemas)
3. Para cada recibo, los campos no aplicables se exportan como valores vacíos
4. El archivo contiene la totalidad de los registros almacenados
5. El formato es compatible con Excel (UTF-8, separador estándar)
6. La exportación no altera la información original

**Requisitos Técnicos:**
- Fuente de datos: mismo CSV o estructura que usa la app para recibos (data/recibos_capturados.csv o carga en memoria)
- Construir DataFrame con columnas = datos generales + unión de todos los campos de todos los esquemas (data/04_esquemas_recibo_por_tarifa o equivalente). Para cada fila, rellenar solo columnas de su tarifa; resto vacío
- Exportar con pandas: to_csv(index=False, encoding='utf-8'). st.download_button para descarga
- No modificar el archivo origen; solo lectura y generación de archivo de salida

**Instrucciones:**
1. Revisar criterios de aceptación y casos de prueba en BACKLOG.md (HU 6.6)
2. Implementar función que lea recibos y esquemas, construya el DataFrame ancho y genere CSV
3. Añadir botón de exportación en el tab Captura de Datos (o sección visible cuando hay recibos)
4. Mantener consistencia con app.py y con estructura de recibos y esquemas de HUs 6.1–6.5

## 🧪 Pruebas de Aceptación
- [ ] **CP-6.6.1:** Exportar con 0 recibos genera CSV con solo encabezados o mensaje apropiado
- [ ] **CP-6.6.2:** Exportar con recibos de varias tarifas genera columnas para todos los campos; celdas no aplicables vacías
- [ ] **CP-6.6.3:** El CSV abre correctamente en Excel con caracteres correctos
- [ ] Criterios: columnas generales + todas las tarifarias; vacíos donde no aplica; todos los registros; UTF-8; sin alterar origen
