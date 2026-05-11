# WS2 auditoria tipo dios ED1/ED2

- Fecha: `2026-05-09 14:24:40`
- Workspace: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2`
- Veredicto: **CERRADO**

## Fuentes de control

- Curso: enunciado 2026-05-04, apuntes 2026-05-08, NCh433:2026, guia ED1, canon ED2.
- API ETABS: OAPI local `CSI API ETABS v1.chm`, `CSiAPIv1.tlb`, `Table and Field Keys.xml`; se uso una instancia por vez.
- Consulta web oficial CSI realizada para patron OAPI/FAQ; en errores se prioriza documentacion CSI oficial y artefactos locales.

## Checks

## Preflight
- [OK] single ETABS rule final state: Get-Process ETABS => none
### Edificio 1
- [OK] ETABS/open-check: audit copy opened with ETABS 21.2.0; source C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif1\logs\ed1_audit_20260509_1415.json
- [OK] stories/heights: {'names': ['Story1', 'Story2', 'Story3', 'Story4', 'Story5', 'Story6', 'Story7', 'Story8', 'Story9', 'Story10', 'Story11', 'Story12', 'Story13', 'Story14', 'Story15', 'Story16', 'Story17', 'Story18', 'Story19', 'Story20'], 'elevations': [3.4, 6.0, 8.6, 11.200000000000001, 13.8, 16.4, 19.0, 21.6, 24.2, 26.8, 29.400000000000002, 32.0, 34.6, 37.2, 39.800000000000004, 42.4, 45.0, 47.6, 50.2, 52.800000000000004], 'heights': [3.4, 2.6, 2.6, 2.6, 2.6, 2.6, 2.6, 2.6, 2.6, 2.6, 2.6, 2.6, 2.6, 2.6, 2.6, 2.6, 2.6, 2.6, 2.6, 2.6], 'count': 20}
- [OK] area/frame counts: {'areas': 880, 'frames': 320, 'points': 1370}
- [OK] slab/wall/frame properties: areas={'MHA30G30': 260, 'MHA20G30': 320, 'Losa15G30': 300}; frames={'VI20/60G30': 320}
- [OK] base supports fixed: {'(True, True, True, True, True, True)': 50}
- [OK] Qmin independent: W=10529.793643, Qmin=737.085555
- [OK] SEx/SEy >= 1.005 Qmin: SEx=740.770900, SEy=740.771000, target=740.770983, tol=0.001
- [OK] b2 shear preserved: SEx_b2=740.770900, SEy_b2=740.771000
- [OK] modal 90 percent mass: X mode=7, Y mode=8, final SumUX=1, SumUY=1
- [OK] drift seismic cases <= 0.002: {'max': 0.001353, 'case': 'SEy', 'story': 'Story17', 'label': '1', 'drift_x': 0.000126, 'drift_y': 0.001353}
- [OK] diaphragm max/avg seismic <= 0.002: {'max': 0.001353, 'avg': 0.001182, 'ratio': 1.144, 'case': 'SEy', 'story': 'Story17', 'item': 'Diaph D1 Y', 'label': '2'}
- [OK] ULS combo drift trace: {'max': 0.002089, 'case': 'ED1_DYN_YP', 'story': 'Story17', 'label': '1', 'drift_x': 0.000149, 'drift_y': 0.002089}; not used as base NCh drift check
- [OK] Metodo a variants: variants=2
- [OK] Matriz b1/b2 torsion: variants=2, max_gap=0.092424%
### Edificio 2
- [OK] ETABS same-session run/extract: version=21.2.0
- [OK] W gravity independent: W=5378.457675
- [OK] C formula clamp: raw=0.189259, C=0.147000, Cmin=0.070000, Cmax=0.147000
- [OK] Vd vs base reactions: Vd=790.633278, EX=790.633300, EY=790.633300
- [OK] static distribution Ak/Fx/Mt: ak_gap=3.45e-07, fx_gap=0.0004, mt_gap=0.0005
- [OK] floor force sums: sumFx=790.633000, Vd=790.633278
- [OK] overturning moment: sum(Fz)=8954.031500, base My=8954.036400
- [OK] torsion moment: sumMt=1877.459000, TEX=1877.459200
- [OK] story force table source: rows=10
- [OK] drift CM/excess: CM=0.000827, excess=0.000254
- [OK] first three modal directions: [{'mode': 1, 'period': 0.408, 'dominant': 'Y', 'ux': 9.327e-07, 'uy': 0.8669, 'rz': 0.0}, {'mode': 2, 'period': 0.408, 'dominant': 'X', 'ux': 0.8669, 'uy': 9.327e-07, 'rz': 0.0}, {'mode': 3, 'period': 0.359, 'dominant': 'RZ', 'ux': 0.0, 'uy': 0.0, 'rz': 0.8681}]
- [OK] torsion applied as force couples: count=10
- [OK] CM/CR analytical symmetry: ETABS CR table not exposed; symmetric ED2 gives CM=CR=(16.25,16.25); source=etabs_cm_table_placeholder_cr_zero
### Codigo y APOS
- [OK] py_compile audited scripts
- [OK] verify_ed2.py: PASS
- [OK] APOS lint: APOS lint: OK

## Observaciones abiertas

- Sin observaciones abiertas.

## Notas no bloqueantes

- ED1 ULS combo drift: max=0.002089; drift NCh check uses SEx/SEy/SEx_b2/SEy_b2, not ULS design combos
- ED2 CR table: ETABS did not expose a real CR table; CR is justified analytically by exact plan/stiffness symmetry and kept explicit in CSV

## Fallas

- No quedan fallas numericas/conceptuales/codigo bajo la evidencia auditada.

## Evidencia usada

- ED1 base reactions: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif1\exports\ed1_Base_Reactions_20260509_1411.csv`
- ED1 joint drifts: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif1\exports\ed1_Joint_Drifts_20260509_1411.csv`
- ED1 diaphragm max/avg drifts: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif1\exports\ed1_Diaphragm_Max_Over_Avg_Drifts_20260509_1411.csv`
- ED1 open-check audit JSON: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif1\logs\ed1_audit_20260509_1415.json`
- ED2 summary: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif2\results\ed2_summary.json`
- ED2 static seed: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif2\results\ed2_static_seed.json`
- ED2 static distribution: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif2\results\ed2_static_distribution.csv`
- ED2 base reactions: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif2\results\ed2_base_reactions.csv`
- Strict audit: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\codex_ws2_context\transfer\ws2-ed1-etabs21-context\reports\WS2_AUDITORIA_RESULTADOS_ESTRICTA_20260509_1418.md`

## Notas de robustez ETABS

- Se reforzo el watchdog para capturar dialogos `Warning/Error` con texto `miOpen`.
- Se preservaron EDB fallidos por `Qmin guard` y `miOpen`; el modelo Ed1 activo fue restaurado desde backup bueno.
- Ed1 se verifico con `--no-final-save` para no reescribir el EDB despues de analisis; los resultados quedan en CSV/JSON.
- Ed2 se verifico sobre copia open-check y el runner ahora soporta `--close-if-started`.

## Salidas de herramientas

### verify_ed2.py

```text
ED2 Parte 1 - Verificacion oficial
W = 5378.458 tonf
W/area = 1.018406 tonf/m2
Tx = 0.4080 s | Ty = 0.4080 s | Tz = 0.3590 s
Cx = 0.14700 | Cy = 0.14700 | Cmin = 0.07000 | Cmax = 0.14700
Vdx = 790.633 tonf | EX real = 790.633 tonf
Vdy = 790.633 tonf | EY real = 790.633 tonf
Drift CM max = 0.000827 | limite CM = 0.002000
Drift punto max = 0.000827 | Exceso max = 0.000254 | limite exceso = 0.001000
Story weights source = etabs_table
Story weights file = ed2_story_weights.csv
Story weights scaled to gravity W = True | scale = 1.01421146
Story Forces source = etabs_table
Drift CM source = nearest_cm_table
Drift excess source = paired_combo_cm
CM/CR source = etabs_cm_table_placeholder_cr_zero | real CR = False
ETABS = 21.2.0 | major = 21 | strict = True
Torsion force_couple = 10 | nodal fallback = 0
TEX Mz real/target = 1877.459 / 1877.459
TEY Mz real/target = 1877.459 / 1877.459
CM/CR stories = 5 | within plan = True | nonzero CR = False
First three modes OK = True
WARNINGS
  - ETABS no expuso CR real; se exporto CM con placeholder CR explicito (etabs_cm_table_placeholder_cr_zero)
PASS
```

### APOS lint

```text
APOS lint: OK
```
