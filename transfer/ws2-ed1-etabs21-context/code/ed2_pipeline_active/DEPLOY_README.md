# Deploy Ed.2 en WS UCN

## Estado del paquete
- La carpeta activa es esta misma: `autonomo/scripts/ed2/`
- Los resultados viejos no verificados quedaron archivados en
  `archive/2026-04-02_pre_validation_snapshot/`
- `models/` queda reservado para `.edb` reales
- `results/` queda reservado para CSV y plots obtenidos desde ETABS
- `taller_ed2/` no debe considerarse evidencia valida si no existe `.edb`
  y CSV crudo en `results/`

## Requisitos WS
- ETABS v19 o v21 instalado
- Python 3.8+ con `comtypes`
- Copiar esta carpeta completa al equipo de la U

## Orden recomendado
1. Auditar la carpeta de la workstation:
   `python tools/inspect_ta_workspace.py --path C:\\Users\\Civil\\Documents\\ta`
2. Abrir ETABS manualmente y crear un modelo en blanco
3. Correr `python diag.py`
4. Si el diagnostico esta OK: `python run_pipeline_ed2.py --phase 1`
5. Guardar el `.edb` en `models/`
6. Correr `python run_pipeline_ed2.py --phase 2`
7. Verificar con `python verify_ed2.py`
8. Extraer resultados con `python 12_extract_results_ed2.py`
9. Generar plots desde CSV reales: `python plot_results_ed2.py --csv-only`
10. Generar informe: `python generate_taller_ed2.py --csv-only`

## Criterio minimo para decir "Ed.2 resuelto"
- Existe un `.edb` real en `models/`
- Existen CSV reales en `results/`
- `verify_ed2.py` pasa sin fallas criticas
- El informe y los plots fueron regenerados desde esos resultados
