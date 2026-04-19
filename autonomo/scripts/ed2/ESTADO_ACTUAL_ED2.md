# Estado Actual Ed.2

Fecha de actualizacion: 2026-04-03

## Que quedo activo
- Scripts del pipeline `01` a `12`
- `config_ed2.py`
- `ed2_static_official.py`
- `run_pipeline_ed2.py`
- `diag.py`
- `verify_ed2.py`
- `plot_results_ed2.py`
- `generate_taller_ed2.py`
- `tools/inspect_ta_workspace.py`

## Que se archivo
- Salidas generadas previas en `archive/2026-04-02_pre_validation_snapshot/`
- Motivo: no estaban respaldadas por `.edb` y CSV/JSON reales del flujo oficial

## Estado tecnico actual
- El flujo oficial ya fue rebaselinado al metodo estatico.
- El paquete activo ahora distingue:
  - fuente original
  - referencia derivada
  - evidencia real
- `08-12`, `verify`, `plot` y `generate` quedaron alineados al flujo oficial.

## Riesgos abiertos
- No se ejecutó ETABS en esta sesion, por lo que la validacion viva sigue pendiente.
- El cierre real sigue exigiendo `.edb` + CSV/JSON + PASS de `verify_ed2.py`.

## Siguiente flujo recomendado
1. Correr `python tools/inspect_ta_workspace.py --path C:\\Users\\Civil\\Documents\\ta`
2. En la workstation, correr `python diag.py`
3. Ejecutar `python run_pipeline_ed2.py --phase 1`
4. Guardar `.edb`
5. Ejecutar `python run_pipeline_ed2.py --phase 2`
6. Correr `python verify_ed2.py`
7. Correr `python plot_results_ed2.py`
8. Correr `python generate_taller_ed2.py`
