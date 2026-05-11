# WS2 auditoria estricta de resultados ED1/ED2

- Fecha: `2026-05-09 13:00:31`
- Workspace: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2`
- Criterio: chequeos matematicos independientes con tolerancia estricta; no se acepta PASS con gap de corte basal > 0.5%.

## Edificio 1 - Auditoria estricta

- Modelo base: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif1\models\ED1_PARTE1_WS2_PROG2_20260508_2213.EDB`
- ETABS: `21.2.0`
- W = `10529.793643` tonf
- Qmin = `0.07*W = 737.085555` tonf
- SEx final = `740.770900` tonf; SEy final = `740.771000` tonf
- Ratio final Qmin X/Y = `1.004999888` / `1.005000023`
- Masa modal acumulada 90%: X en modo `7`, Y en modo `8`; al modo final X/Y = `1.0` / `1.0`
- Metodo a: `2` variantes; ambas con `run_ok=True`, 20 mass-source records y 15/15 combos.
- Matriz b1/b2: `2` variantes; corridas base/final OK; gaps torsionales max < `0.5%`.

## Edificio 2 - Auditoria estricta

- Modelo: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif2\models\ED2_PARTE1_WS2_PROG2_20260508_2213.EDB`
- W por reacciones = `5378.457675` tonf
- W usado = `5378.457675` tonf
- Factor escala story weights -> W oficial = `1.014211456`
- Vdx/Vdy = `790.633278` / `790.633278` tonf
- EX/EY reales = `790.633300` / `790.633300` tonf
- TEX/TEY reales = `1877.459200` / `1877.459200` tonf*m
- TEX/TEY objetivo = `1877.459245` / `1877.459245` tonf*m
- Drift CM max = `0.000827` <= `0.002000`
- Exceso drift max = `0.000254` <= `0.001000`
- Filas distribucion estatica = `5`; filas drift = `5`

## Veredicto

**CERRADO NUMERICAMENTE CON OBSERVACIONES DE TRAZABILIDAD**: no quedan fallas matematicas estrictas en los CSV/JSON auditados.

## Observaciones que no debo ocultar

- ED1 ED1_PARTE1_WS2_PROG2_RIGID_METHOD_A_20260509_0958.EDB no conserva archivos .Y* de resultados ETABS.
- ED1 ED1_PARTE1_WS2_PROG2_RIGID_MATRIX_20260509_0943.EDB no conserva archivos .Y* de resultados ETABS.
- ED2 ETABS no expuso CR real; se conserva CR=centro por simetria/placeholder auditado.
- ED2 no conserva archivos .Y* visibles; resultados estan respaldados por CSV/JSON y sesion de analisis.

## Evidencia principal usada

- `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif1\logs\ed1_full_20260509_0630.json`
- `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif1\logs\ed1_torsion_matrix_20260509_0943.json`
- `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif1\logs\ed1_method_a_20260509_0958.json`
- `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif2\results\ed2_summary.json`
- `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif2\results\ed2_static_seed.json`
- `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif2\results\ed2_base_reactions.csv`
- `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif2\results\ed2_static_distribution.csv`

## Accion aplicada en esta auditoria

- ED2 fue corregido para escalar la distribucion estatica desde la masa por piso de ETABS al W oficial por cargas gravitacionales.
- `verify_ed2.py` fue endurecido para fallar con gaps de corte/torsion > 0.5%, y advertir sobre gaps > 0.1%.
- Se creo backup previo de ED2 antes de modificar el EDB.
