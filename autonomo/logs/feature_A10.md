# Feature A10 — 09_torsion.py (3 métodos, 6 casos)

## Estado: COMPLETADO

## Archivo generado
- `autonomo/scripts/09_torsion.py` (~750 líneas)

## Qué implementa

Script Python + comtypes para configurar torsión accidental en ETABS v19 según NCh433 Art. 6.3.4.

### Método A — Desplazar CM ±5%
- 4 casos NL Static auxiliares (AUX_PX, AUX_MX, AUX_PY, AUX_MY)
- 4 casos Modal Eigen con masa desplazada (Modal_PX, Modal_MX, Modal_PY, Modal_MY)
- 4 casos Response Spectrum con modales desplazados (SDX_aPY, SDX_aMY, SDY_aPX, SDY_aMX)
- **Limitación**: SetMassSource_1 NO soporta parámetro "Adjust Diaphragm Lateral Mass". Se documentan instrucciones manuales para configurar las Mass Sources en GUI.

### Método B-F1 — Momentos estáticos
- Crea load patterns TEX, TEY (tipo Quake, SWM=0)
- Intenta extraer story shears del modelo analizado (Results.StoryForces)
- Fallback: distribución triangular invertida aproximada (método estático)
- Computa Mtk = Fk × ek por piso (NCh433 Art. 6.3.4)
- Aplica momentos Mz vía PointObj.SetLoadForce en un joint por piso
- Crea casos Static Linear para TEX, TEY
- Combinaciones: SDX ± TEX, SDY ± TEY

### Método B-F2 — Excentricidad por piso (más simple)
- Crea SDTX y SDTY con SetEccentricity(0.05) — 5% uniforme
- ETABS genera internamente ±5% sub-cases (envelope)
- **Completamente API-programable**, sin pasos manuales
- Documenta opción de excentricidad variable por piso en GUI

### Funcionalidades adicionales
- `compute_eccentricity_table()` — tabla completa ek por piso (NCh433 Art. 6.3.4)
- `compute_approx_story_forces()` — fuerzas aproximadas sin análisis previo
- `create_torsion_combinations()` — combos NCh3171 para cada método
- `verify_torsion_cases()` — verificación de casos creados
- CLI con `--method a|b1|b2|all`, `--combos`, `--table-only`

## COM Signatures usadas
- `LoadCases.StaticNonlinear.SetCase(Name)` — auxiliares NL
- `LoadCases.ModalEigen.SetCase/SetNumberModes/SetParameters/SetInitialCase` — modales
- `LoadCases.ResponseSpectrum.SetCase/SetLoads/SetModalCase/SetEccentricity` — espectro
- `LoadCases.StaticLinear.SetCase/SetLoads` — estáticos
- `LoadPatterns.Add(Name, Type, SWM, AddCase)` — patrones
- `PointObj.GetNameList/GetCoordCartesian/SetLoadForce` — momentos por piso
- `RespCombo.Add/SetCaseList` — combinaciones

## Fuentes consultadas
- NCh433 Mod 2009 Art. 6.3.4 (excentricidad accidental)
- DS61 Tabla 12.3 (parámetros suelo)
- Material Apoyo Taller 2026 Sección H (3 métodos torsión)
- autonomo/research/com_signatures.md
- autonomo/research/etabs_api_reference.md

## Patrón del pipeline
Sigue convenciones de 08_seismic.py: docstring extenso, COM signatures documentadas, check_ret en cada llamada, logging detallado, verificación al final.

## 6 casos del taller
| Caso | Método | Diafragma |
|------|--------|-----------|
| 1 | A (shift CM) | Rígido |
| 2 | B-F1 (momentos) | Rígido |
| 3 | B-F2 (eccentricidad) | Rígido |
| 4 | A (shift CM) | Semi-rígido |
| 5 | B-F1 (momentos) | Semi-rígido |
| 6 | B-F2 (eccentricidad) | Semi-rígido |
