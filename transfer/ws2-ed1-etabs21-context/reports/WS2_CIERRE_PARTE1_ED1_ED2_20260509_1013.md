# WS2 cierre Parte 1 Edificio 1 y Edificio 2

- Fecha: 2026-05-09 10:13
- Workdir real: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2`
- Carpeta de trabajo nueva: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2`
- ETABS usado: 21.2.0, una sola instancia durante las corridas.
- Estado final ETABS: `NO_ETABS_PROCESS` tras cierre explicito.

## 1. Estado confirmado Edificio 1

Modelo limpio base conservado:

- `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif1\models\ED1_PARTE1_WS2_PROG2_20260508_2213.EDB`

Corrida base dinamica valida:

- reporte: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif1\reports\ED1_PARTE1_PROG2_full_20260509_0630.md`
- `Qmin=737.086 tonf`
- `SEx=740.771 tonf`, `SEy=740.771 tonf`
- ratio final Qmin X/Y = `1.005`
- `.LOG/.OUT` sin `error|warning|failed|unable|could not|not finished|recovering`.

Vigas verificadas por OAPI:

- reporte: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif1\reports\ED1_VIGAS_VISIBILIDAD_20260509_0625.md`
- `320` vigas `VI20/60G30`, `16` por piso, `20` pisos.
- Cardinal Point `2`; se preservan releases torsionales pedidos por profesor.
- La vista 3D que no muestra vigas corresponde a visualizacion/ocultamiento por shells, no a ausencia de vigas.

Matriz de torsion accidental de 6 escenarios ED1:

- Metodo a, rigido:
  - `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif1\models\ED1_PARTE1_WS2_PROG2_RIGID_METHOD_A_20260509_0958.EDB`
- Metodo a, semi-rigido:
  - `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif1\models\ED1_PARTE1_WS2_PROG2_SEMIRIGID_METHOD_A_20260509_0958.EDB`
- Metodo b forma 1 y b forma 2, rigido:
  - `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif1\models\ED1_PARTE1_WS2_PROG2_RIGID_MATRIX_20260509_0943.EDB`
- Metodo b forma 1 y b forma 2, semi-rigido:
  - `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif1\models\ED1_PARTE1_WS2_PROG2_SEMIRIGID_MATRIX_20260509_0943.EDB`

Evidencia metodo a:

- reporte: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif1\reports\ED1_METHOD_A_PROG2_20260509_0958.md`
- fuentes de masa creadas: `MasaXp`, `MasaXm`, `MasaYp`, `MasaYm`
- `MoveMass=Yes`, ratios `+/-0.05` en la direccion correspondiente.
- modales creados: `A_MODAL_MasaXp`, `A_MODAL_MasaXm`, `A_MODAL_MasaYp`, `A_MODAL_MasaYm`
- espectrales metodo a: `A_SEx_Yp`, `A_SEx_Ym`, `A_SEy_Xp`, `A_SEy_Xm`
- `EccenRatio=0` en los espectrales metodo a.
- `15/15` combinaciones metodo a creadas por variante.
- corridas rigida y semi-rigida con `Analyze.RunAnalysis ret=0`.

Evidencia metodo b1/b2:

- reporte: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif1\reports\ED1_TORSION_MATRIX_PROG2_20260509_0943.md`
- b1: torsion estatica por piso calculada desde diferencias de cortes CQC sin excentricidad.
- b2: `SEx_b2`/`SEy_b2` con `EccenRatio=0` y `20` overrides de diafragma por caso.
- b2 aplicado via `DatabaseTables.SetTableForEditingArray`, porque la TLB ETABS 21 instalada expone `GetDiaphragmEccentricityOverride`, pero no `SetDiaphragmEccentricityOverride`.
- rigido b1: gap torsion base vs target aprox. `0.0924%`.
- semi-rigido b1: gap torsion base vs target aprox. `0.0924%`.
- corridas base y final con `Analyze.RunAnalysis ret=0`.

## 2. Estado confirmado Edificio 2

Modelo de trabajo:

- `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif2\models\ED2_PARTE1_WS2_PROG2_20260508_2213.EDB`

Verificacion ejecutada:

- comando: `python .\prog2\Edif2\workbench\ed2_pipeline_active\verify_ed2.py`
- resultado: `PASS`
- `W=5378.458 tonf`
- `W/area=1.018406 tonf/m2`
- `Tx=0.4080 s`, `Ty=0.4080 s`, `Tz=0.3590 s`
- `Cx=Cy=0.14700`, `Cmin=0.07000`, `Cmax=0.14700`
- `Vdx=Vdy=790.633 tonf`
- `EX=EY=779.555 tonf`
- `TEX_WS2=TEY_WS2=1851.152 tonf*m`
- drift CM max `0.000816 < 0.002`
- exceso max `0.000250 < 0.001`
- advertencia vigente: ETABS no expuso CR real; se mantiene placeholder CR documentado.

Evidencia ED2:

- `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif2\reports\ED2_PARTE1_PROG2_audit_20260509_0613.md`
- `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif2\logs\ed2_verify_final_20260508_233545.log`
- `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif2\logs\ed2_audit_20260509_0613.json`

## 3. Archivos .EDB encontrados y activos

Originales vivos no versionados:

- ED1 original: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog\Edif1\ED1_PARTE1_COMPLETA_TRABAJO.EDB`
- ED2 original: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\Edif2\Edificio2_Estatico con carga sismica.EDB`

Copias activas de trabajo:

- ED1 base limpio prog2: `...\prog2\Edif1\models\ED1_PARTE1_WS2_PROG2_20260508_2213.EDB`
- ED2 prog2: `...\prog2\Edif2\models\ED2_PARTE1_WS2_PROG2_20260508_2213.EDB`

Copias derivadas ED1 para cierre:

- `ED1_PARTE1_WS2_PROG2_RIGID_METHOD_A_20260509_0958.EDB`
- `ED1_PARTE1_WS2_PROG2_SEMIRIGID_METHOD_A_20260509_0958.EDB`
- `ED1_PARTE1_WS2_PROG2_RIGID_MATRIX_20260509_0943.EDB`
- `ED1_PARTE1_WS2_PROG2_SEMIRIGID_MATRIX_20260509_0943.EDB`

## 4. Que cambio respecto al estado WS1

- Se creo `prog2` como workspace nuevo por edificio.
- Se dejo el modelo ED1 base limpio y una copia contaminada en cuarentena.
- Se agrego watchdog ETABS para detectar/dialogar bloqueos en `OpenFile` y `RunAnalysis`.
- Se corrigio helper OAPI para no caer por estado watchdog inexistente.
- Se completo ED1 con casos programaticos metodo a, b1 y b2, en diafragma rigido y semi-rigido.
- Se corrigio b2 usando tabla oficial ETABS `Load Case Definitions - Response Spectrum`.
- Se revalido ED2 con `PASS`.

## 5. Que falta para Parte 1 Edificio 1

Desde ETABS/API, queda ejecutado y exportado lo pedible del nucleo de Parte 1:

- modelo base dinamico;
- metodo a rigido/semi-rigido;
- metodo b forma 1 rigido/semi-rigido;
- metodo b forma 2 rigido/semi-rigido;
- combinaciones y tablas de resultados exportadas.

Pendientes no estructurales:

- armar informe docente final con capturas/tablas seleccionadas;
- si el profesor exige screenshots UI de cada ventana, capturarlas manualmente desde las copias ya creadas;
- revisar si desea CR real en ED2/ED1 por otro procedimiento, porque ETABS no lo expuso directamente en el flujo actual.

## 6. Que falta para Parte 1 Edificio 2

ED2 queda verificado para Parte 1 estatica y checks del curso. Pendiente solo:

- informe docente final;
- decision sobre como presentar CR cuando ETABS no lo expone como tabla real.

## 7. Riesgos tecnicos

- No abrir dos ETABS: se mantuvo una sola instancia.
- ETABS puede imprimir `Cannot open file ... .Y_` al cerrar por API; no aparecio en `.LOG/.OUT`, pero sigue como riesgo operacional.
- `Diaphragm.SetDiaphragm` devuelve `ret=1`, aunque la tabla exportada confirma `Rigid`/`Semi-Rigid`; por eso se verifica por tabla.
- En metodo a, la tabla visible de Mass Source omite `SCT=0`; el import inicial uso 20 registros, pero ETABS muestra 15 porque descarta/oculta multiplicadores cero.
- ED2 CR real no expuesto por ETABS; se conserva placeholder documentado, no se inventa.

## 8. Siguiente accion segura

1. No tocar originales.
2. Usar las copias `prog2` como fuente de entrega.
3. Para revisar visualmente, abrir solo una copia a la vez en la instancia ETABS existente o cerrar antes de cambiar.
4. Construir informe final desde tablas exportadas y reportes citados.

## 9. Evidencia usada

- `C:\Program Files\Computers and Structures\ETABS 21\CSiAPIv1.tlb`
- `C:\Program Files\Computers and Structures\ETABS 21\Table and Field Keys.xml`
- `C:\Program Files\Computers and Structures\ETABS 21\CSI API ETABS v1.chm`
- `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif1\logs\ed1_method_a_20260509_0958.log`
- `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif1\logs\ed1_torsion_matrix_20260509_0943.log`
- `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif1\reports\ED1_METHOD_A_PROG2_20260509_0958.md`
- `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif1\reports\ED1_TORSION_MATRIX_PROG2_20260509_0943.md`
- `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif2\logs\ed2_verify_final_20260508_233545.log`

## 10. Auditoria final post-cierre

- `Select-String` sobre `.LOG/.OUT` finales ED1 metodo a y b1/b2 no encontro patrones `error|warning|failed|unable|could not|not finished|recovering`.
- `python -m py_compile` OK para:
  - `prog2\Edif1\workbench\ed1_method_a_prog2.py`
  - `prog2\Edif1\workbench\ed1_torsion_matrix_prog2.py`
  - `prog2\_common\ws2_etabs_oapi.py`
  - `prog2\_common\ws2_etabs_watchdog.py`
- `APOS lint: OK`.
- `Get-Process ETABS -ErrorAction SilentlyContinue`: sin procesos al cierre.
