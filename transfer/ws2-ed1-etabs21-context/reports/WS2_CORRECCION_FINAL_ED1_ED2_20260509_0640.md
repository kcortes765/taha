# WS2 correccion final ED1/ED2

- Fecha: 2026-05-09 06:40 America/Santiago
- Workspace: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2`
- Regla aplicada: una sola instancia ETABS a la vez, `Get-Process ETABS -ErrorAction SilentlyContinue` antes de OAPI/UI.

## 1. Problema detectado

Durante la auditoria post-modal se hizo un rerun ED1 para probar watchdog. Esa corrida `20260509_0619` no fue aceptable: el modelo ya venia con escalas espectrales aplicadas y el flujo anterior no borraba resultados antes de cada analisis.

Evidencia de falla:

- Log/JSON descartado: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif1\logs\ed1_run-adjust-export_20260509_0619.json`
- Resultado absurdo:
  - `Qmin=737.086 tonf`
  - `SEx final=18815.609 tonf`
  - `SEy final=18815.532 tonf`
- Decision: la corrida `20260509_0619` queda invalidada para resultados.

## 2. Correccion aplicada en ED1

Se preservo la copia afectada:

- `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif1\models\quarantine_20260509_0630_bad_qmin_scale`

Se repuso el modelo activo ED1 desde la fuente limpia:

- Fuente: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog\Edif1\ED1_PARTE1_COMPLETA_TRABAJO.EDB`
- Activo corregido: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif1\models\ED1_PARTE1_WS2_PROG2_20260508_2213.EDB`

Se corrigio el script:

- `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif1\workbench\ed1_part1_prog2.py`

Cambios:

- `Analyze.DeleteResults("", True)` antes de cada `Analyze.RunAnalysis`.
- Watchdog activo en `RunAnalysis`.
- Guardas Qmin:
  - rechazar amplificaciones excesivas;
  - rechazar ratios finales demasiado altos;
  - retornar error si Qmin falla.

## 3. ED1 resultado valido

Corrida valida:

- Comando: `python .\prog2\Edif1\workbench\ed1_part1_prog2.py --phase full --allow-start --close-if-started`
- Reporte: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif1\reports\ED1_PARTE1_PROG2_full_20260509_0630.md`
- JSON: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif1\logs\ed1_full_20260509_0630.json`
- Export base reactions: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif1\exports\ed1_Base_Reactions_20260509_0630.csv`

Resultado:

- `run_ok_initial=True`
- `rerun_ok=True`
- `qmin.ok=True`
- Exportaciones OK
- `W=10529.794 tonf`
- `Qmin=737.086 tonf`
- Antes de amplificar:
  - `Qx=400.300 tonf`
  - `Qy=426.630 tonf`
- Amplificacion:
  - `amp_x=1.8505`
  - `amp_y=1.7363`
- Final:
  - `SEx=740.771 tonf`
  - `SEy=740.771 tonf`
  - ratio X/Y = `1.005`

Exportaciones ED1 validas:

- modal participating mass ratios
- modal periods and frequencies
- base reactions
- story forces
- story drifts
- mass source
- mass summary by story
- mass summary by diaphragm
- centers of mass and rigidity
- diaphragm center of mass displacements
- joint displacements

Vigas ED1:

- Verificacion: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif1\reports\ED1_VIGAS_VISIBILIDAD_20260509_0625.md`
- Resultado: `320` vigas `VI20/60G30`, todas horizontales, `16` por piso, Cardinal Point `2`.
- Conclusion: la duda visual era de display/extrusion/ocultamiento por shells, no ausencia de vigas.

## 4. ED2 resultado valido

Correccion menor aplicada:

- `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif2\workbench\ed2_pipeline_active\config_ed2.py`

Cambio:

- ahora resuelve por defecto `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif2` como runtime root si existen `models` o `results`.
- `verify_ed2.py` ya no requiere setear manualmente `ED2_RUNTIME_ROOT`.

Verificacion ED2:

- Comando: `python .\prog2\Edif2\workbench\ed2_pipeline_active\verify_ed2.py`
- Resultado: `PASS`

Valores:

- `W=5378.458 tonf`
- `W/area=1.018406 tonf/m2`
- `Tx=0.408 s`
- `Ty=0.408 s`
- `Tz=0.359 s`
- `Cx=Cy=0.147`
- `Vdx=Vdy=790.633 tonf`
- `EX=EY=779.555 tonf`
- `TEX_WS2=TEY_WS2=1851.152 tonf*m`
- Drift CM max `0.000816 < 0.002`
- Exceso torsional max `0.000250 < 0.001`

Warning vigente:

- ETABS no expuso CR real; se conserva CM real con placeholder CR explicito `etabs_cm_table_placeholder_cr_zero`.

## 5. ETABS / watchdog

Estado final:

- `Get-Process ETABS -ErrorAction SilentlyContinue` queda sin salida.
- No queda ETABS abierto.
- Watchdog post-connect/post-open sin eventos en la corrida limpia ED1.
- `.LOG/.OUT` ED1/ED2 revisados sin textos `error`, `warning`, `recovering`, `not finished`, `could not start`.
- Se mantiene advertencia operacional: al cerrar ETABS aparece en consola `Cannot open file ... .Y_`; no queda como modal ni aparece en `.LOG/.OUT`, pero queda registrado como riesgo a vigilar.

## 6. Archivos APOS actualizados

- `.apos/JOURNAL.md`
- `.apos/RISKS.md`
- `.apos/DECISIONS.md`
- `.apos/STATUS.md`
- `.apos/HANDOFF.md`

## 7. Estado final honesto

- ED1: corregido y recalculado desde limpio. Resultado valido `full_20260509_0630`.
- ED2: sigue cerrado con `PASS`; verificador robustecido.
- Copia mala preservada, no usada.
- No se modificaron `.EDB` vivos originales fuera de `prog2`.
- No queda ETABS abierto.

Pendiente academico posible:

- Si la rubrica exige literalmente seis variantes separadas de ED1 como archivos/corridas independientes, eso debe correrse como bloque final aparte sobre copias derivadas. La base dinamica/Qmin de ED1 ya quedo saneada.
