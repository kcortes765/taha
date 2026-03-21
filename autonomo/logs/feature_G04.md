# Feature G04 — Corregir guía: drift y verificaciones

## Estado: COMPLETADO
## Fecha: 2026-03-21

## Cambios realizados

### 1. Sección 11.1 — Participación modal (mejorada)
- Agregada subsección **"Verificación de participación modal ≥ 90%"** (NCh433 Art. 6.3.4)
- Procedimiento paso a paso para verificar SumUX ≥ 0.90 y SumUY ≥ 0.90
- Instrucciones para **qué hacer si no se alcanza** (aumentar nº modos en Define > Load Cases > MODAL)
- Regla práctica: 30 modos generalmente suficientes para 20 pisos
- Tabla resumen formato entregable (3.4) con campos para Tx*, Ty*, Tz*, nº modos
- Nota sobre visualización de deformadas modales

### 2. Sección 11.8 — Drift (reescrita completamente)
**Antes**: 24 líneas básicas, sin referencias normativas, procedimiento incompleto.
**Ahora**: ~190 líneas exhaustivas con:

#### Fundamento normativo
- Referencia explícita a NCh433 Art. 5.9
- Fórmulas de ambas condiciones con variables definidas
- Explicación conceptual (Cond.1 = rigidez global, Cond.2 = control torsión)

#### Tablas ETABS clarificadas
- Tabla comparativa de **3 tablas de drift en ETABS v19**:
  - Story Drifts (drift en esquinas, NO en CM)
  - Joint Drifts (drift por nodo — usar para CM)
  - Diaphragm Max Over Avg Drifts (Max, Avg, Ratio por diafragma)
- **Advertencia crítica**: Story Drifts ≠ drift en CM

#### Condición 1 — Procedimiento detallado
- Paso 1: Identificar nodo del CM (View > Set Display Options + Diaphragm Extent)
- Paso 2: Extraer drift en CM (Display > Show Tables > Joint Drifts + filtros)
- Paso 3: Verificar ≤ 0.002 en todos los pisos
- Tabla modelo para llenar resultados
- Nota sobre drifts CQC ya calculados

#### Condición 2 — Procedimiento con dos tablas
- Obtener Max Drift de Diaphragm Max Over Avg Drifts
- Calcular diferencia con Drift CM
- Verificar ≤ 0.001
- Tabla modelo para llenar resultados
- **Método alternativo simplificado**: usar Avg Drift ≈ CM Drift de la misma tabla
- Interpretación del ratio Max/Avg (irregularidad torsional)

#### Gráficos de drift por piso
- **Método 1**: Story Response Plots (Display > Story Response Plots > Max Story Drifts)
  - Con nota de que muestra drift máximo, no en CM
- **Método 2**: Gráfico en Excel (RECOMENDADO)
  - Exportar Joint Drifts filtrado → gráfico XY
  - Ejes, series, línea límite 0.002
  - Diagrama ASCII de ejemplo
  - 6 gráficos totales (1 por caso)

#### Tabla resumen entregable
- Tabla para los 6 casos de análisis: Caso, Diafragma, Torsión, Piso crítico, Drift CM, Cond.1, ΔDrift, Cond.2

#### Qué hacer si no cumple
- Tabla de problemas/soluciones: rigidez insuficiente, torsión excesiva, drift localizado

#### Nota sobre elástico vs. inelástico
- Explicación de espectro elástico vs reducido
- Advertencia de verificar desde combinaciones (Método B) no desde SDX/SDY directos

### 3. Tabla entregables (FASE 13)
- Entregable 3.4 actualizado: incluye "verif. ≥90%"
- Entregable 4.1 actualizado: incluye "Story Response Plots" como fuente

### 4. Checklist final
- Expandido de 7 a 11 items post-análisis
- Participación modal ≥ 90% como item explícito
- Drift Condición 1 y 2 como items separados con descripción
- Drift en ambas direcciones
- Gráficos y tabla resumen como items

### 5. Errores comunes
- 4 errores nuevos agregados:
  1. Usar Story Drifts para Cond. 1 (debe ser Joint Drifts en CM)
  2. Restar desplazamientos manualmente (ETABS ya calcula δ/h)
  3. No verificar participación modal ≥90%
  4. Verificar drift con caso elástico sin reducir

## Fuentes consultadas
- INDICE.md (ubicación de temas drift en apuntes)
- Apuntes 02d líneas 222-223 (condiciones drift NCh433)
- Apuntes 02f líneas 270-271 (indicadores biosísmicos 4 y 5)
- RESUMEN-ADSE-COMPLETO.md (condiciones de drift)
- ETABS-v19-Referencia-Interfaz.md (Story Response Plots, Show Tables)
- ETABS-PYTHON-GITHUB-REPOS.md (APIs StoryDrifts, JointDrifts)
- ETABS-Python-Ecosystem-Research.md (verificación drift en ETABS)
- Web: NCh433 artículos sobre deformaciones, ETABS drift tables, Story Response Plots

## Archivo editado
- `docs/estudio/GUIA-COMPLETA-EDIFICIO1-ETABS-v19.md`
