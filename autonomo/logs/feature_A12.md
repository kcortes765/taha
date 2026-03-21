# Feature A12 — 11_run_analysis.py (Analysis + Validation)

## Estado: COMPLETADO

## Archivo generado
- `autonomo/scripts/11_run_analysis.py` (~650 líneas)

## Descripción
Script completo para ejecutar análisis ETABS y validar resultados del Edificio 1 (20 pisos, muros HA).

## Estructura del script (6 pasos)

### Step 1: Pre-flight checks
- Verifica que el modelo tenga file path (requerido por RunAnalysis)
- Cuenta elementos (frames, areas, points)
- Verifica existencia de load cases requeridos (Modal, PP, TERP, TERT, SCP, SCT, SDX, SDY)
- Desbloquea modelo si estaba locked de análisis previo

### Step 2: Configure Active DOF
- `Analyze.SetActiveDOF([True]*6)` — 6 DOF activos para análisis 3D completo

### Step 3: Set run case flags
- `Analyze.SetRunCaseFlag("", False, True)` — desactiva todos
- Activa solo los casos necesarios (incluye SDTX/SDTY si existen)

### Step 4: Run Analysis
- `Analyze.RunAnalysis()` — ejecuta el análisis
- Maneja excepciones y timeout
- Reporta tiempo de ejecución

### Step 5: Post-analysis validation (4 sub-pasos)

**5a: Peso total**
- Extrae base reactions para PP, TERP, SCP via `Results.BaseReac`
- Calcula peso sísmico: PP + TERP + 0.25×SCP
- Valida contra ~9,368 tonf (468 m² × 20p × 1 tonf/m²) con ±20% tolerancia
- Reporta peso/área (regla Lafontaine ≈ 1.0 tonf/m²)

**5b: Resultados modales**
- Extrae via `DatabaseTables.GetTableForDisplayArray("Modal Participating Mass Ratios")`
  (porque Results.ModalPeriod y ModalParticipatingMassRatios no están documentados)
- Parsing robusto de campos (maneja múltiples formatos de resultado comtypes)
- Valida T1 ∈ [1.0, 1.3] s (rango esperado) y [0.5, 2.5] s (rango plausible)
- Valida ΣUX, ΣUY ≥ 90% (NCh433 Art. 6.3.6.2)
- Detecta si valores son ratios (0-1) o porcentajes (0-100)
- Calcula R*(T*) usando calc_R_star de config.py
- Imprime tabla de primeros 10 modos con periodos y participación

**5c: Story drifts**
- Extrae via `Results.StoryDrifts()` (12 output args)
- Selecciona SDX, SDY, SDTX, SDTY para output
- Valida drift ≤ 0.002 (NCh433 Art. 5.9.2)
- Imprime tabla de max drift por caso/dirección
- Imprime perfil de drift (cada 5 pisos + tope + base)

**5d: Base reactions (sanity check)**
- Extrae Vx, Vy para SDX y SDY
- Calcula Cmin y Qmin como referencia
- Reporta ratios V/Qmin

### Step 6: Summary
- Resumen completo con todas las validaciones
- Estado overall: PASS si todo OK, FAIL con detalle de warnings

## Firmas COM verificadas
- `Analyze.SetActiveDOF(DOF)` — 1 arg, bool[6]
- `Analyze.SetRunCaseFlag(Name, Run, All)` — 3 args
- `Analyze.RunAnalysis()` — 0 args
- `Results.Setup.DeselectAllCasesAndCombosForOutput()` — 0 args
- `Results.Setup.SetCaseSelectedForOutput(CaseName)` — 1 arg
- `Results.BaseReac(...)` — 13 output args
- `Results.StoryDrifts(...)` — 11 output args
- `DatabaseTables.GetTableForDisplayArray(...)` — 7 args

## Uso
```bash
python 11_run_analysis.py                      # Run completo
python 11_run_analysis.py --skip-run           # Solo extraer resultados
python 11_run_analysis.py --cases Modal SDX SDY  # Casos específicos
```

## Constantes de validación (desde config.py)
- Peso esperado: ~9,368 tonf (PESO_ESPERADO_TONF)
- Drift límite: 0.002 (DRIFT_LIMITE)
- T1 esperado: 1.0–1.3 s
- Participación modal: ≥ 90%
- R*, Cmin calculados con fórmulas verificadas

## Decisiones de diseño
1. **DatabaseTables para modal** — Results.ModalPeriod no documentado en research, DatabaseTables sí
2. **Parsing robusto** — Múltiples estrategias para encontrar fields/data en respuesta comtypes
3. **Tolerancia peso ±20%** — Amplia porque el modelo puede tener variaciones legítimas
4. **Drift profile selectivo** — Muestra cada 5 pisos para no saturar el log
5. **--skip-run flag** — Permite re-extraer resultados sin re-correr análisis
6. **Exit code** — sys.exit(0) si todo OK, sys.exit(1) si hay fallas
