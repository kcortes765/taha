# Feature A14 — run_pipeline.py (master pipeline script)

## Estado: COMPLETADO

## Archivo creado
- `autonomo/scripts/run_pipeline.py` (~400 LOC)

## Funcionalidad implementada

### Ejecucion del pipeline completo
- Ejecuta los 12 scripts en orden (01_init → 12_extract)
- Cada script corre como subprocess independiente (aislacion COM)
- 2 segundos de pausa entre steps para estabilidad COM

### 2 fases COM separadas
- **Fase 1** (steps 1-7): Geometria — init, materiales, muros, vigas, losas, assignments, cargas
- **Fase 2** (steps 8-12): Analisis — espectro, torsion, combos, run, resultados
- Checkpoint entre fases: guarda .edb + pausa para reiniciar ETABS (evita crash COM)

### Modos de operacion
- `--dry-run`: muestra plan de ejecucion sin ejecutar nada
- `--from N`: retoma desde paso N (1-12)
- `--to N`: detiene despues del paso N
- `--phase 1|2`: solo fase 1 o solo fase 2
- `--no-checkpoint`: salta pausa entre fases
- `--log FILE`: ruta custom para log

### Manejo de errores
- Verifica existencia de todos los scripts antes de iniciar
- Si un paso falla (exit code != 0): reporta error + aborta limpiamente
- Muestra ultimas 10 lineas de stdout/stderr del script fallido
- Sugiere comando para retomar: `--from N`
- Timeout de 10 min por paso (subprocess.TimeoutExpired)

### Logging
- Consola: timestamps + mensajes INFO
- Archivo: log completo (DEBUG) con stdout/stderr de cada script
- Log auto-generado con timestamp (pipeline_YYYYMMDD_HHMMSS.log)

### Resumen final
- Tabla con status/tiempo de cada paso
- Conteo succeeded/failed
- Proximos pasos si todo OK (revisar drift, T1, peso)

## Verificacion
- `--help` muestra ayuda completa con ejemplos
- `--dry-run` ejecuta correctamente (12 pasos, checkpoint, summary)
- `--from 8` resume correctamente desde Phase 2
- `--phase 1` filtra solo steps 1-7
- Validacion de rango (`--from > --to` da error)

## Lecciones COM incorporadas
- Subprocess por step → aislacion COM natural
- Checkpoint entre fases → session fresca para analisis
- Instrucciones claras: cerrar/reabrir ETABS entre fases
- No usa CreateObject (cada script usa GetActiveObject via config.connect())
