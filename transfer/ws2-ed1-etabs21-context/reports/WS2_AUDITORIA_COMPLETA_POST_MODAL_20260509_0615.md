# WS2 auditoria completa post-modal ETABS

- Fecha: 2026-05-09 06:15 America/Santiago
- Workspace: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2`
- Contexto: el usuario observo un modal ETABS `Error in recovering joint assembled mass` que quedo abierto durante horas.
- Criterio aplicado: cerrar la instancia antigua antes de abrir otra, trabajar un edificio a la vez y no confiar solo en `ret=0`.

## 1. Estado operacional ETABS

- Instancia antigua detectada:
  - PID: `23284`
  - Titulo: `ETABS Ultimate 21.2.0 - ED2_PARTE1_WS2_PROG2_20260508_2213 [ACADEMIC LICENSE - NOT FOR COMMERCIAL USE]`
  - Inicio: 2026-05-08 22:21:26
- Accion aplicada:
  - se cerro la instancia antigua por instruccion explicita del usuario antes de abrir otra.
- Estado final:
  - `Get-Process ETABS -ErrorAction SilentlyContinue` queda sin salida; no hay ETABS abierto al cierre de esta auditoria.

## 2. Mecanismo anti-bloqueo agregado

Archivos nuevos/modificados:

- `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\_common\ws2_etabs_watchdog.py`
- `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\_common\ws2_etabs_oapi.py`
- `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif1\workbench\ed1_part1_prog2.py`
- `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif2\workbench\ed2_part1_prog2_audit.py`
- `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif2\workbench\ed2_pipeline_active\config_ed2.py`
- `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif2\workbench\ed2_pipeline_active\11_run_analysis_ed2.py`
- `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif2\workbench\ed2_pipeline_active\ws2_run_extract_ed2.py`

Funcion del mecanismo:

- enumera ventanas visibles de Windows asociadas a ETABS;
- detecta dialogos modales con texto tipo `error`, `warning`, `recovering`, `failed`, `unable`, `license`;
- escribe evidencia en `*_watchdog.json`;
- presiona OK/Enter solo despues de registrar evidencia;
- hace fallar el script si aparece un modal durante `File.OpenFile` o `Analyze.RunAnalysis`.

Validacion de sintaxis:

- `python -m py_compile` OK para watchdog, helper OAPI y wrappers ED1/ED2.

## 3. Documentacion oficial consultada

- CSI API `cAnalyze.DeleteResults`: confirma `DeleteResults(Name, All=True)` para borrar resultados de casos y retorno cero si es exitoso: https://docs.csiamerica.com/help-files/etabs-api-2015/html/c7930302-842a-f789-44cc-abbca8ae223c.htm
- CSI ETABS Help `Set Load Cases to Run`: documenta estados `Not Run`, `Could Not Start`, `Not Finished`, `Finished`, y que el log de analisis se guarda en `.LOG`: https://docs.csiamerica.com/help-files/etabs/Menus/Analyze/Set_Load_Cases_to_Run.htm
- CSI ETABS Help `Last Analysis Run Log`: recomienda revisar estado, warnings y datos del analisis completado: https://docs.csiamerica.com/help-files/etabs/Menus/Analyze/Last_Analysis_Run_Log.htm
- Ayuda local instalada ETABS 21 usada previamente:
  - `C:\Program Files\Computers and Structures\ETABS 21\CSI API ETABS v1.chm`
  - `C:\Program Files\Computers and Structures\ETABS 21\Table and Field Keys.xml`

## 4. Auditoria Edificio 1 post-modal

Modelo auditado:

- `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif1\models\ED1_PARTE1_WS2_PROG2_20260508_2213.EDB`

Auditoria ejecutada:

- Comando: `python .\prog2\Edif1\workbench\ed1_part1_prog2.py --phase audit --allow-start --close-if-started`
- PID usado: `21584`
- ETABS: `21.2.0`
- Reporte: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif1\reports\ED1_PARTE1_PROG2_audit_20260509_0612.md`
- JSON: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif1\logs\ed1_audit_20260509_0612.json`
- Watchdog post-open: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif1\logs\ed1_audit_20260509_0612_post_open_file_once_watchdog.json`
- Watchdog: `events: []`

Estado confirmado:

- Stories: 20
- Alturas: primer piso 3.4 m; restantes 2.6 m; total 52.8 m
- Areas: 880
- Frames: 320
- Points: 1370
- Muros/losas:
  - `MHA30G30`: 260
  - `MHA20G30`: 320
  - `Losa15G30`: 300
- Diafragma losas: `D1` en 300 losas
- Vigas: `VI20/60G30`: 320
- Apoyos base: 50 empotrados
- Load patterns auditados: `Dead`, `Live`, `PP`, `TERP`, `TERT`, `SCP`, `SCT`, `TorX+`, `TorX-`, `TorY+`, `TorY-`, `~LLRF`, `~SExECC`, `~SEyECC`
- Combos ED1 presentes: 11 combos `ED1_*`

Resultado Parte 1 existente:

- Reporte final previo: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif1\reports\ED1_PARTE1_PROG2_run-adjust-export_20260508_2247.md`
- JSON final previo: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif1\logs\ed1_run-adjust-export_20260508_2247.json`
- Verificador JSON post-modal:
  - `run_ok_initial=True`
  - `rerun_ok=True`
  - `qmin.ok=True`
  - `exportsOk=True`
- `Analyze.RunAnalysis ret=0`
- `Tx=1.105 s`, `Ty=1.094 s`
- `R*x=8.8673`, `R*y=8.8449`
- `W=10529.794 tonf`
- `Qmin=737.086 tonf`
- Final Qmin:
  - `SEx=740.771 tonf`
  - `SEy=740.771 tonf`
- Exportaciones completas:
  - modal mass, periods, base reactions, story forces, story drifts, mass source, mass by story/diaphragm, CM/CR, diaphragm CM displacements, joint displacements.
- `.LOG` del modelo:
  - estabilidad lineal con `NUMBER OF NEGATIVE EIGENVALUES = 0, OK`;
  - no se encontraron textos `error`, `warning`, `recovering`, `not finished` en `.LOG/.OUT`.

Advertencia Edificio 1:

- Al cerrar ETABS tras la auditoria, la consola imprimio:
  - `Cannot open file`
  - `BufferFileIn::BufferFileIn(): fileName = ...ED1_PARTE1_WS2_PROG2_20260508_2213.Y_`
- No hubo modal, el watchdog quedo sin eventos y `.LOG/.OUT` no registran error. Queda como riesgo operacional, no como falla confirmada de calculo.
- Sigue pendiente honesto: si el profesor exige literalmente seis variantes ED1 como entregables separados, faltaria materializarlas y exportarlas una a una.

## 5. Auditoria Edificio 2 post-modal

Modelo auditado:

- `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif2\models\ED2_PARTE1_WS2_PROG2_20260508_2213.EDB`

Auditoria ejecutada:

- Comando: `python .\prog2\Edif2\workbench\ed2_part1_prog2_audit.py --allow-start --close-if-started`
- PID usado: `20844`
- ETABS: `21.2.0`
- Reporte: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif2\reports\ED2_PARTE1_PROG2_audit_20260509_0613.md`
- JSON: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif2\logs\ed2_audit_20260509_0613.json`
- Watchdog post-open: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif2\logs\ed2_audit_20260509_0613_post_open_file_once_watchdog.json`
- Watchdog: `events: []`

Estado confirmado:

- Stories: 5
- Alturas: 3.5 m + 4 x 3.0 m; total 15.5 m
- Areas: 130
- Frames: 480
- Points: 241
- Losas: `L17G25`: 130
- Diafragma: `D1` en 130 areas
- Frames:
  - columnas: 180
  - vigas X: 150
  - vigas Y: 150
- Secciones:
  - `C70x70G25`: 72
  - `C65x65G25`: 108
  - `V50x70G25`: 120
  - `V45x70G25`: 180
- Apoyos base: 36 empotrados
- Load patterns: `PP`, `TERT`, `TERP`, `SCP`, `SCT`, `TEX`, `TEY`, `SDX`, `SDY`, `EX`, `EY`, `~LLRF`, `TEX_WS2`, `TEY_WS2`
- Response combos: 47
- Tablas exportadas en auditoria: stories, grids, materiales, frame assignments, diaphragm assignments, restraints, load patterns, load cases summary, combos, mass source.

Resultado Parte 1 existente:

- Verificador final: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif2\logs\ed2_verify_final_20260508_233545.log`
- Estado: `PASS`
- Verificador re-ejecutado post-modal con `ED2_RUNTIME_ROOT=...\prog2\Edif2`: `PASS`
- Summary: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif2\results\ed2_summary.json`
- `analysis_return_code=0`
- `W=5378.458 tonf`
- `W/area=1.018406 tonf/m2`
- `Tx=0.408 s`, `Ty=0.408 s`, `Tz=0.359 s`
- `Cx=Cy=0.147`
- `Vdx=Vdy=790.633 tonf`
- `EX=EY=779.555 tonf`
- `TEX_WS2=TEY_WS2=1851.152 tonf*m`
- Drift CM max: `0.000816 < 0.002`
- Exceso torsional max: `0.000250 < 0.001`
- `.LOG` del modelo:
  - estabilidad lineal con `NUMBER OF NEGATIVE EIGENVALUES = 0, OK`;
  - `ANALYSIS COMPLETE` el 2026-05-08 23:34:29;
  - no se encontraron textos `error`, `warning`, `recovering`, `not finished` en `.LOG/.OUT`.

Advertencia Edificio 2:

- Al cerrar ETABS tras la auditoria, la consola imprimio:
  - `Cannot open file`
  - `BufferFileIn::BufferFileIn(): fileName = ...ED2_PARTE1_WS2_PROG2_20260508_2213.Y_`
- No hubo modal, el watchdog quedo sin eventos y `.LOG/.OUT` no registran error.
- CR real sigue no expuesto por ETABS; se conserva warning del verificador: CM real, CR placeholder explicito `etabs_cm_table_placeholder_cr_zero`.

## 6. Cambios APOS registrados

Archivos APOS actualizados append-only:

- `.apos/JOURNAL.md`
- `.apos/RISKS.md`
- `.apos/DECISIONS.md`
- `.apos/STATUS.md`
- `.apos/HANDOFF.md`

Riesgos nuevos:

- `R-20260509-ETABS-MODAL-BLOQUEANTE`
- `R-20260509-ETABS-Y-TEMPORAL`

## 7. Conclusion tecnica

- La sospecha del usuario era valida: una instancia ETABS quedo bloqueada por modal y no debia asumirse que todo estaba sano solo porque habia logs previos.
- Se corrigio el flujo con un mecanismo real de deteccion de modales.
- La reapertura auditada de ED1 y ED2 desde `prog2` no reprodujo el modal `Error in recovering joint assembled mass`.
- ED1 y ED2 mantienen evidencia de analisis/exportacion previa; ED2 queda con `PASS`; ED1 queda con Parte 1 base dinamica/Qmin cerrada, salvo la matriz formal de seis variantes si la rubrica la exige literalmente.
- No queda instancia ETABS abierta al final.

## 8. Siguiente accion segura

1. No abrir ETABS manualmente y script al mismo tiempo.
2. Antes de cualquier OAPI: `Get-Process ETABS -ErrorAction SilentlyContinue`.
3. Si aparece otra vez `Error in recovering joint assembled mass`, detener cierre, conservar captura/log, borrar resultados en copia con API oficial `Analyze.DeleteResults("", True)` si se confirma disponible en ETABS 21, rerun y verificar `.LOG/.OUT`.
4. Para cerrar ED1 sin ambiguedad academica: crear variantes derivadas en `prog2\Edif1` y correr/exportar una por una con watchdog activo.
