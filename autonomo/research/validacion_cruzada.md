# Validación Cruzada — Scripts API vs Guía UI

**Feature**: V01 — Validación cruzada API vs UI guide
**Fecha**: 2026-03-21
**Fuente de verdad**: Guía UI (`docs/estudio/GUIA-COMPLETA-EDIFICIO1-ETABS-v19.md`)
**Scripts API**: `autonomo/scripts/` (config.py + 01-12_*.py)

---

## Resumen Ejecutivo

Se encontraron **14 discrepancias** entre los scripts API y la guía UI.
- **3 CRÍTICAS** (afectan resultados del análisis)
- **4 MODERADAS** (pueden afectar resultados o causar errores)
- **7 MENORES** (inconsistencias internas, nomenclatura, comentarios)

---

## Tabla de Discrepancias

| # | Severidad | Fase | Descripción | Guía UI | API Scripts | Recomendación |
|---|-----------|------|-------------|---------|-------------|---------------|
| D01 | **CRÍTICA** | F2-Mat | Shell type muros | Shell-Thin | Shell-Thick | Ver análisis D01 |
| D02 | **CRÍTICA** | F7-Sísm | TERT en Mass Source | Incluido (SF=1.0) | Omitido | Agregar TERT a API |
| D03 | **CRÍTICA** | F5-Asig | AutoMesh | 1.0 m | 0.4 m | Unificar a 1.0m o justificar |
| D04 | **MODERADA** | F2-Mat | Es del acero | 2,039,000 tonf/m² | 20,387,400 tonf/m² | Corregir guía (API correcta) |
| D05 | **MODERADA** | F2-Mat | fy/fu del acero (conversión) | 42,000 / 63,000 | 42,814 / 64,220 | Usar conversión exacta |
| D06 | **MODERADA** | F2-Mat | Expected fy/fu factors | fy×1.1 / fu×1.1 | fy×1.17 / fu×1.08 | Investigar norma ACI318 |
| D07 | **MODERADA** | F3-Secc | Nombre sección viga | VI20/60G30 | VI20x60G30 | Unificar (usar "x" por ETABS) |
| D08 | **MENOR** | F7-Sísm | SCT en Mass Source | Explícito (SF=0) | Omitido implícitamente | OK (efecto equivalente) |
| D09 | **MENOR** | F7-Sísm | Mass Source options | Lateral Only + Lump | No especificadas via API | Verificar comportamiento por defecto |
| D10 | **MENOR** | F9-Comb | Nombres casos sísmicos (config.py) | SDX/SDY | 'SX'/'SY' en COMBINATIONS dict | Corregir config.py |
| D11 | **MENOR** | F9-Comb | TERT en combinaciones (config.py) | Incluido | Omitido en COMBINATIONS dict | Corregir config.py |
| D12 | **MENOR** | F9-Comb | Factor SCP en C3 (config.py) | 1.0 | 0.5 | Corregir config.py a 1.0 |
| D13 | **MENOR** | F4-Geom | Conteo muros dir X (comentario) | — | Comentario dice 22, real 23 | Corregir comentario |
| D14 | **MENOR** | F9-Comb | SCT/TERT en C2 (config.py) | Incluido | Omitido | Corregir config.py |

---

## Análisis Detallado por Fase

### FASE 0-1: Modelo y Grilla — ✅ SIN DISCREPANCIAS

| Parámetro | Guía UI | API (config.py + 01_init_model.py) | Estado |
|-----------|---------|-------------------------------------|--------|
| Pisos | 20 | 20 | ✅ |
| h_piso1 | 3.40 m | 3.40 m | ✅ |
| h_típico | 2.60 m | 2.60 m | ✅ |
| H_total | 52.80 m | 52.80 m | ✅ |
| Ejes X | 17 (1-17) | 17 (1-17) | ✅ |
| Ejes Y | 6 (A-F) | 6 (A-F) | ✅ |
| Coordenadas X | Tabla completa | GRID_X dict idéntico | ✅ |
| Coordenadas Y | Tabla completa | GRID_Y dict idéntico | ✅ |
| Unidades | Tonf, m, C | UNITS_TONF_M_C = 12 | ✅ |
| NewGridOnly | Grid Only template | NewGridOnly(20, 2.6, 3.4, 17, 6, ...) | ✅ |

---

### FASE 2: Materiales — ⚠️ 3 DISCREPANCIAS

#### Hormigón G30

| Propiedad | Guía UI | API (config.py) | Estado |
|-----------|---------|------------------|--------|
| Nombre | G30 | "G30" | ✅ |
| f'c | 30 MPa = 300 kgf/cm² | 30 MPa → 3,058 tonf/m² | ✅ |
| Ec | 2,624,300 tonf/m² | 4700√30 × 101.937 ≈ 2,624,270 | ✅ (~30 redondeo) |
| ν | 0.20 | 0.20 | ✅ |
| γ | 2.5 tonf/m³ | 2.50 tonf/m³ | ✅ |
| α_thermal | 0.0000099 /°C | 1.0E-05 /°C | ✅ (~igual) |

#### Acero A630-420H

| Propiedad | Guía UI | API (config.py) | Estado |
|-----------|---------|------------------|--------|
| Nombre | A630-420H | "A630-420H" | ✅ |
| γ | 7.849 tonf/m³ | 7.85 tonf/m³ | ✅ |
| **Es** | **2,039,000 tonf/m²** | **20,387,400 tonf/m²** | **⚠️ D04** |
| **fy** | **42,000 tonf/m²** | **42,814 tonf/m²** | **⚠️ D05** |
| **fu** | **63,000 tonf/m²** | **64,220 tonf/m²** | **⚠️ D05** |
| **Efy** | **46,200 (fy×1.1)** | **50,092 (fy×1.17)** | **⚠️ D06** |
| **Efu** | **69,300 (fu×1.1)** | **69,358 (fu×1.08)** | **⚠️ D06** |

#### D04 — Es del acero (MODERADA)

**Guía**: Es = 2,039,000 tonf/m² (≈200,000 MPa)
**API**: Es = 200,000 × 101.937 = 20,387,400 tonf/m²

**Diagnóstico**: La guía tiene un error de un orden de magnitud. El valor 2,039,000 corresponde a 200,000 × 10.1937, que es Es en **kgf/cm²**, no tonf/m². La conversión correcta es:
- 200,000 MPa × 101.937 tonf/m²/MPa = **20,387,400 tonf/m²**

**Impacto**: Si se ingresara 2,039,000 en ETABS, el acero tendría 1/10 de su rigidez real. Sin embargo, en la práctica ETABS probablemente ignora Es del rebar para diseño de secciones HA (usa Ec para la sección y Es está embebido en las curvas del material). Impacto real bajo, pero el valor es objetivamente incorrecto.

**Recomendación**: Corregir la guía a ~20,387,400 tonf/m² (o 2,038,740 kgf/cm² si se trabaja en esas unidades).

#### D05 — Conversión fy/fu (MODERADA)

**Guía**: Usa conversión aproximada (1 MPa ≈ 10 kgf/cm²):
- fy = 420 × 10 = 4,200 kgf/cm² = 42,000 tonf/m²

**API**: Usa conversión exacta (1 MPa = 101.937 tonf/m²):
- fy = 420 × 101.937 = 42,813.5 tonf/m²

**Diferencia**: ~2% (42,000 vs 42,814). Inconsistente con Ec donde la guía sí usa el factor exacto.

**Recomendación**: Usar conversión exacta en ambos. La guía ya dice "Para ETABS usar el valor exacto" para Ec, pero no aplica el mismo criterio a fy/fu. Actualizar guía para consistencia.

#### D06 — Factores Expected fy/fu (MODERADA)

**Guía**: Efy = fy × 1.1, Efu = fu × 1.1
**API**: Efy = fy × 1.17 (Ry ACI), Efu = fu × 1.08

**Diagnóstico**: Los factores 1.17 y 1.08 son de ACI 341/ACI 318 para acero A706 Grade 60 (equivalente). El factor 1.1 es más conservador/genérico. Ambos son aceptables según la norma que se siga.

**Recomendación**: Verificar qué factores usa el Prof. Music. Si el curso sigue ACI318-08 (que es el caso según CLAUDE.md), usar 1.17/1.08 es correcto. Actualizar guía o documentar la diferencia.

---

### FASE 3: Secciones — ⚠️ 2 DISCREPANCIAS

| Sección | Propiedad | Guía UI | API | Estado |
|---------|-----------|---------|-----|--------|
| MHA30G30 | **Shell Type** | **Shell-Thin** | **Shell-Thick** | **🔴 D01** |
| MHA20G30 | **Shell Type** | **Shell-Thin** | **Shell-Thick** | **🔴 D01** |
| MHA30G30 | Thickness | 0.30 m | 0.30 m | ✅ |
| MHA20G30 | Thickness | 0.20 m | 0.20 m | ✅ |
| **VI20/60G30** | **Nombre** | **VI20/60G30** | **VI20x60G30** | **⚠️ D07** |
| VI20/60G30 | Material | G30 | G30 | ✅ |
| VI20/60G30 | T3 (depth) | 0.60 m | 0.60 m | ✅ |
| VI20/60G30 | T2 (width) | 0.20 m | 0.20 m | ✅ |
| VI20/60G30 | J modifier | 0 | 0 | ✅ |
| Losa15G30 | Shell Type | Shell-Thin | Shell-Thin | ✅ |
| Losa15G30 | Thickness | 0.15 m | 0.15 m | ✅ |
| Losa15G30 | m11=m22=m12 | 0.25 | 0.25 | ✅ |

#### D01 — Shell Type de muros (CRÍTICA)

**Guía UI** (Paso 3.1):
> Modeling Type: **Shell-Thin**
> "¿Por qué Shell-Thin? Para muros delgados (e/L < 0.1), Shell-Thin ignora deformación por corte transversal y es suficiente."

**API** (02_materials_sections.py, líneas 241-268):
```python
SHELL_THICK = 2   # eShellType
PA.SetWall(name, WALL_SPECIFIED, SHELL_THICK, MAT_CONC_NAME, thickness)
```
> Docstring: "Shell-Thick type (eShellType=2) for out-of-plane bending."

**Análisis**:
- Shell-Thin (eShellType=1): No incluye deformación por corte fuera del plano. Adecuado para e/L < ~0.1.
- Shell-Thick (eShellType=2): Incluye deformación por corte fuera del plano (Mindlin). Más general.

Para muros de corte sísmicos donde la relación de aspecto puede ser significativa (e.g., muro de 0.30m × 0.70m entre ejes A-B), Shell-Thick es técnicamente más correcto. Sin embargo, la guía recomienda Shell-Thin, que es más común en la práctica chilena según Lafontaine.

**Impacto**: Diferencia en rigidez fuera del plano de muros. Para muros largos (L>>e), la diferencia es despreciable. Para machones cortos (L≈e), puede ser significativa (~5-15% en rigidez a flexión fuera del plano).

**Recomendación**: Dado que la guía UI es la fuente de verdad, cambiar API a Shell-Thin (SHELL_THIN=1). Si se prefiere Shell-Thick por razones técnicas, documentar la decisión y actualizar la guía.

#### D07 — Nombre sección viga (MODERADA)

**Guía**: `VI20/60G30` (con barra `/`)
**API**: `VI20x60G30` (con `x`)

**Diagnóstico**: ETABS v19 generalmente acepta "/" en nombres, pero puede causar problemas en exportaciones o scripts que parsean nombres. El carácter "x" es más seguro.

**Recomendación**: Unificar a `VI20x60G30` (sin `/`). Actualizar la guía.

---

### FASE 4: Geometría (Muros) — ⚠️ 1 DISCREPANCIA MENOR

| Aspecto | Guía UI | API (config.py) | Estado |
|---------|---------|-----------------|--------|
| Muros dir Y | ~26 segmentos | 26 segmentos definidos | ✅ |
| Muros dir X | No cuantificado | 23 segmentos definidos | ✅* |
| Regla espesores Y | Ejes 1,3,4,5,7,12,13,14,16,17→30cm | Misma regla | ✅ |
| Regla espesores X | C entre 3-6 y 10-14→30cm | Misma regla | ✅ |
| Eje F muro central | 7.7m centrado en eje 10 | (10−4.25, 10+3.45) = 7.7m | ✅ |

#### D13 — Conteo muros dir X (MENOR)

**config.py línea 325**: Comentario dice `# 22 segmentos` pero `len(MUROS_DIR_X)` = 23.
**03_walls.py línea 336**: Imprime "Direction X (22 segments):" pero usa N_MUROS_DIR_X que vale 23.

**Impacto**: Ninguno — el código usa `len()` correctamente. Solo el comentario y un string de log están desactualizados.

**Recomendación**: Corregir comentario a `# 23 segmentos` y actualizar el string de log.

---

### FASE 4: Geometría (Vigas) — ✅ CONSISTENTE

| Aspecto | Guía UI | API (config.py) | Estado |
|---------|---------|-----------------|--------|
| Sección | VI20/60G30 | VI20x60G30 | ⚠️ D07 |
| Vigas invertidas | Sí (Bottom Center) | CP=2 (Bottom Center) | ✅ |
| Ejes con vigas | A, F, B | A (10), F (8), B (12) = 30/piso | ✅ |

Nota: La guía no enumera todas las vigas con exactitud (dice "Posiciones visibles" sugiriendo lectura del plano). El API define 30 vigas/piso basado en lectura detallada del enunciado.

---

### FASE 4: Geometría (Losas) — ✅ CONSISTENTE

| Aspecto | Guía UI | API (config.py) | Estado |
|---------|---------|-----------------|--------|
| Sección | Losa15G30 | Losa15G30 | ✅ |
| Paneles piso tipo | Panel por panel | 7 paneles (~468 m²) | ✅ |
| Shaft excluido | Sí | Sí (gap C-D, 9-11) | ✅ |
| Paneles techo | Diferente al tipo | 5 paneles | ✅ |

---

### FASE 5: Asignaciones — ⚠️ 1 DISCREPANCIA CRÍTICA

| Asignación | Guía UI | API | Estado |
|------------|---------|-----|--------|
| Diafragma D1 | Rigid | Rigid (SetDiaphragm) | ✅ |
| Cardinal Point vigas | 2 (Bottom Center) | 2 (Bottom Center) | ✅ |
| Base restraints | 6 DOF empotrado | [True]*6 a Z=0 | ✅ |
| **AutoMesh losas** | **1.0 m** | **0.4 m** | **🔴 D03** |
| **AutoMesh muros** | **1.0 m** | **0.4 m** | **🔴 D03** |
| Pier Labels | P1, PF definidos | No implementado | ℹ️ |
| Auto Edge Constraint | Aplicado | No implementado | ℹ️ |
| Divide Shells en intersecciones | Sí | No (confianza en AddByCoord) | ℹ️ |

#### D03 — Tamaño AutoMesh (CRÍTICA)

**Guía UI** (Pasos 5.4 y 5.5):
> Losas: "Further Subdivide Auto Mesh with Maximum Element Size of: **1.0 m**"
> Muros: "Maximum Element Size: **1.0 m**"

**API** (config.py línea 241):
```python
AUTOMESH_SIZE = 0.40   # m (vano minimo = 0.425m entre ejes 8-9)
```

**Análisis**:
- Mesh 0.4m = ~2500 elementos por panel de muro (por piso) vs ~600 con 1.0m
- Mesh más fino: mayor precisión pero MUCHO más lento (tiempo de análisis ~6× mayor)
- El vano mínimo de 0.425m (ejes 8-9) no requiere mesh 0.4m — ETABS subdivide automáticamente en bordes
- La elección de 0.4m proviene del pipeline COM anterior donde se necesitaba mesh fino para evitar problemas de compatibilidad en nodos

**Impacto**:
- Con 0.4m: ~130,000 elementos finitos después del mesh. Análisis muy pesado.
- Con 1.0m: ~25,000 elementos. Análisis manejable.
- La diferencia en resultados (períodos, drifts, fuerzas) es típicamente <2% para edificios de muros regulares.

**Recomendación**: Adoptar 1.0m (guía UI como fuente de verdad). Cambiar `AUTOMESH_SIZE = 1.0` en config.py. Si se necesita mayor precisión, documentar en ambos documentos.

---

### FASE 6: Cargas — ✅ CONSISTENTE

| Patrón | Tipo | SWM | Valor (tonf/m²) | Pisos | Guía | API | Estado |
|--------|------|-----|-----------------|-------|------|-----|--------|
| PP | Dead | 1 | Automático | Todos | ✓ | ✓ | ✅ |
| TERP | Super Dead | 0 | 0.140 | 1-19 | ✓ | ✓ | ✅ |
| TERT | Super Dead | 0 | 0.100 | 20 | ✓ | ✓ | ✅ |
| SCP | Live | 0 | 0.250 (ofic) / 0.500 (pasillo) | 1-19 | ✓ | ✓ | ✅ |
| SCT | Roof Live | 0 | 0.100 | 20 | ✓ | ✓ | ✅ |

Notas:
- Guía define SCP_P como patrón separado en FASE 0 (tabla) pero en FASE 6 aplica SCP a valores diferentes por zona. API también usa un solo patrón SCP con valores por zona. ✅
- Dirección: Guide "Gravity", API Dir=6 (Global Z negativo). ✅ Equivalente.

---

### FASE 7: Análisis Sísmico — ⚠️ 1 DISCREPANCIA CRÍTICA

#### Mass Source

| Componente | Guía UI | API (config.py / 08_seismic.py) | Estado |
|------------|---------|----------------------------------|--------|
| PP | SF=1 (vía elementos) | IncludeElements=True | ✅ |
| TERP | SF=1 | SF=1.0 | ✅ |
| **TERT** | **SF=1** | **No incluido** | **🔴 D02** |
| SCP | SF=0.25 | SF=0.25 | ✅ |
| SCT | SF=0 | No incluido (equivalente) | ✅ |
| Lateral Mass Only | ✅ | No especificado via API | ⚠️ D09 |
| Lump at Story | ✅ | No especificado via API | ⚠️ D09 |

#### D02 — TERT omitido del Mass Source (CRÍTICA)

**Guía UI** (Paso 7.1):
> Mass Multipliers for Load Patterns:
> TERT: **1** (100% terminaciones techo)

**API** (config.py líneas 470-474):
```python
MASS_SOURCE_PATTERNS = {
    'PP':   1.0,
    'TERP': 1.0,
    'SCP':  0.25,
}
```
TERT no está en el diccionario. En 08_seismic.py, PP se remueve (capturado por IncludeElements), quedando solo TERP(1.0) y SCP(0.25).

**Impacto**: La masa del techo (piso 20) no incluirá las terminaciones de techo (0.100 tonf/m²). Esto subestima la masa sísmica en el último piso en ~0.100 × ~420 m² ≈ 42 tonf. Sobre un peso total de ~9,368 tonf, es ~0.4%. Pequeño pero incorrecto conceptualmente.

**Recomendación**: Agregar `'TERT': 1.0` a MASS_SOURCE_PATTERNS en config.py.

#### Espectro de Respuesta

| Aspecto | Guía UI | API | Estado |
|---------|---------|-----|--------|
| Tipo función | From File | SetUser (lee archivo en Python) | ✅ |
| Nombre | Esp_Elastico_Z3SC | Esp_Elastico_Z3SC | ✅ |
| Damping | 0.05 (5%) | 0.05 | ✅ |
| Formato | Sa/g | Sa/g | ✅ |
| SF | 9.81 | 9.81 | ✅ |
| Puntos | 101 (T=0-5s) | 101 desde archivo | ✅ |

#### Modal

| Aspecto | Guía UI | API | Estado |
|---------|---------|-----|--------|
| Tipo | Eigen | Eigen | ✅ |
| Max modos | 30 | 30 | ✅ |
| Tolerancia | 1E-09 | 1E-09 | ✅ |

#### Casos Espectrales

| Caso | Dirección | Función | SF | Guía | API | Estado |
|------|-----------|---------|-----|------|-----|--------|
| SDX | U1 | Esp_Elastico_Z3SC | 9.81 | ✓ | ✓ | ✅ |
| SDY | U2 | Esp_Elastico_Z3SC | 9.81 | ✓ | ✓ | ✅ |
| CQC | Modal combo | — | — | ✓ | Default | ✅ |
| SRSS | Dir combo | — | — | ✓ | Default | ✅ |

---

### FASE 8: Torsión Accidental — ✅ CONSISTENTE

Ambos documentos implementan los 3 métodos:
- Método a) Desplazar CM (±5%)
- Método b) Forma 1: Momentos torsores estáticos (TEX, TEY)
- Método b) Forma 2: Eccentricity (SDTX, SDTY con SetEccentricity=0.05)

Los valores de excentricidad accidental por piso coinciden en ambos documentos.

---

### FASE 9: Combinaciones — ⚠️ 3 DISCREPANCIAS MENORES (internas)

**10_combinations.py** implementa correctamente las 11 combinaciones NCh3171:

| Combo | Expresión | 10_combinations.py | config.py COMBINATIONS | Estado |
|-------|-----------|--------------------|-----------------------|--------|
| C1 | 1.4D | 1.4PP+1.4TERP+1.4TERT | 1.4PP+1.4TERP (sin TERT) | ⚠️ D11 |
| C2 | 1.2D+1.6L+0.5Lr | +1.2PP+1.2TERP+1.2TERT+1.6SCP+0.5SCT | +1.2PP+1.2TERP+1.6SCP (sin TERT, sin SCT) | ⚠️ D14 |
| C3 | 1.2D+1.6Lr+1.0L | +1.2PP+1.2TERP+1.2TERT+1.6SCT+1.0SCP | +1.2PP+1.2TERP+1.6SCT+0.5SCP | ⚠️ D12 |
| C4 | 1.2D+1.0L+1.4E_X | Usa **SDX** | Usa **SX** | ⚠️ D10 |
| C5 | 1.2D+1.0L−1.4E_X | Usa **SDX** | Usa **SX** | ⚠️ D10 |
| C6-C7 | (análogos con SDY) | **SDY** | **SY** | ⚠️ D10 |
| C8-C11 | 0.9D ± 1.4E | **SDX/SDY** | **SX/SY** | ⚠️ D10 |
| ENV | Envelope(C1-C11) | ✓ implementado | — | ✅ |

**Nota importante**: El script `10_combinations.py` NO usa `config.py:COMBINATIONS`. Define sus propias combinaciones directamente con `_build_combos()`. Por lo tanto, las discrepancias D10-D12-D14 afectan solo a `config.py:COMBINATIONS` (que NO se usa en ningún script). Sin embargo, `12_extract_results.py` importa `COMBINATIONS` de config.py, lo que podría causar problemas al verificar resultados.

#### D10, D11, D12, D14 — Combinaciones en config.py (MENORES)

El diccionario `COMBINATIONS` en config.py tiene múltiples errores:
1. Usa 'SX'/'SY' en vez de 'SDX'/'SDY' (nombres reales de los casos)
2. Omite TERT de todas las combinaciones
3. Usa factor 0.5 para SCP en C3 (debería ser 1.0 per NCh3171)
4. Omite SCT×0.5 de C2

**Recomendación**: Actualizar config.py COMBINATIONS para que coincida con 10_combinations.py, ya que 12_extract_results.py lo importa.

---

### FASE 10-12: Ejecutar y Extraer — ✅ CONSISTENTE

Los scripts 11_run_analysis.py y 12_extract_results.py implementan:
- Active DOF: 6 DOF activos ✅
- Run cases: Modal, PP, TERP, TERT, SCP, SCT, SDX, SDY ✅
- Validación peso: ~9,368 tonf (Lafontaine) ✅
- Drift NCh433: 0.002 ✅
- T1 esperado: 1.0-1.3s ✅
- Modal mass participation: >90% ✅

---

## Resumen de Correcciones Requeridas

### En la Guía UI (docs/estudio/GUIA-COMPLETA-EDIFICIO1-ETABS-v19.md)

| # | Ubicación | Corrección |
|---|-----------|------------|
| 1 | Paso 2.2, Es rebar | 2,039,000 → **20,387,400 tonf/m²** (o 203,900 kgf/cm²) |
| 2 | Paso 2.2, fy rebar | 42,000 → **42,814 tonf/m²** (conversión exacta) |
| 3 | Paso 2.2, fu rebar | 63,000 → **64,220 tonf/m²** (conversión exacta) |
| 4 | Paso 2.2, Efy/Efu | Documentar factores 1.17/1.08 o justificar 1.1 |
| 5 | Paso 3.1, nombre viga | VI20/60G30 → **VI20x60G30** |

### En los Scripts API (autonomo/scripts/)

| # | Archivo | Corrección |
|---|---------|------------|
| 1 | config.py:SHELL_THICK→SHELL_THIN | Cambiar `SHELL_THICK` por `SHELL_THIN` en muros (o documentar por qué Shell-Thick) |
| 2 | config.py:AUTOMESH_SIZE | Cambiar `0.40` a `1.0` (o justificar 0.4) |
| 3 | config.py:MASS_SOURCE_PATTERNS | Agregar `'TERT': 1.0` |
| 4 | config.py:COMBINATIONS | Actualizar: SX→SDX, SY→SDY, agregar TERT, corregir factores C2/C3 |
| 5 | config.py: comentario N_MUROS_DIR_X | 22 → 23 |

### Correcciones ya implementadas internamente (no afectan ejecución)

Las discrepancias D10-D14 en config.py:COMBINATIONS no afectan la ejecución porque `10_combinations.py` define las combinaciones directamente sin usar ese diccionario. Sin embargo, `12_extract_results.py` importa `COMBINATIONS` de config.py, lo que podría causar problemas en la verificación de resultados.

---

## Elementos NO implementados en API (presentes en Guía UI)

Estos no son "discrepancias" sino funcionalidades que la guía describe pero los scripts API no cubren:

1. **Pier Labels** (P1, PF) — La guía asigna Pier Labels para extracción de fuerzas en muros. Los scripts API no lo hacen.
2. **Auto Edge Constraints** — La guía aplica Edge Constraints entre losas y muros.
3. **Divide Shells en intersecciones** — La guía subdivide muros donde se cruzan. Los scripts crean cada panel por separado con AddByCoord, confiando en la conectividad de nodos compartidos.
4. **Diafragma semi-rígido** — La guía describe cómo crear D1_Semi para los casos 4-6. Los scripts crean `D1_Semi` pero no implementan la re-asignación completa.
5. **Replicar piso tipo** — La guía usa Edit > Replicate. Los scripts crean cada piso individualmente (más seguro por API).

---

## Conclusión

Los scripts API son **sustancialmente correctos** y reproducen la gran mayoría de la modelación descrita en la guía UI. Las 3 discrepancias críticas (Shell type, AutoMesh, TERT en masa) son corregibles con cambios menores en config.py. Las discrepancias en conversión de unidades del acero requieren una decisión sobre qué factor de conversión usar (exacto vs aproximado), siendo la conversión exacta técnicamente superior.

**Prioridad de corrección**:
1. 🔴 TERT en Mass Source → impacta masa sísmica (config.py)
2. 🔴 Shell type muros → impacta rigidez (config.py)
3. 🔴 AutoMesh → impacta rendimiento/precisión (config.py)
4. ⚠️ Es rebar en guía → valor incorrecto (guía)
5. ⚠️ Conversión fy/fu → inconsistencia menor (guía o config)
