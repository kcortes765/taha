# Workbench codigo WS2 - adaptar sobre el modelo real

Fecha: 2026-05-08

## Proposito

El codigo incluido en `code/` no es una instruccion para correr pipelines completos a ciegas.

Es una base tecnica para que la IA de WS2:

1. lea el codigo actual;
2. entienda firmas OAPI, convenciones, patrones de cargas, espectros, torsion, combos y extraccion;
3. lo adapte al estado real del `.EDB` abierto en WS2;
4. construya scripts incrementales nuevos si hace falta;
5. cierre Parte 1 de Edificio 1 primero;
6. despues asegure Edificio 2.

## Regla dura

Antes de cualquier script:

```powershell
Get-Process ETABS -ErrorAction SilentlyContinue
```

Una instancia ETABS 21. Un edificio activo. Un script a la vez.

## Regla documental y anti-cierre OAPI

Antes de adaptar una llamada OAPI sensible, y siempre que aparezca un error ETABS/COM/API, WS2 debe investigar primero documentacion oficial CSI/ETABS o ayuda local instalada de ETABS 21.

Ademas, ningun helper OAPI debe cerrar ETABS por defecto:

- si el script se adjunto a una instancia existente, no llamar `ApplicationExit`;
- si el script creo la instancia, registrar `started_by_script=True`;
- solo cerrar con `ApplicationExit(False)` si `started_by_script=True` y el cierre fue solicitado;
- si hay multiples instancias, no usar `GetObject()` ambiguo: usar `GetObjectProcess` con PID confirmado o detenerse.

Ver reporte:

```text
reports/WS2_ETABS_OAPI_SESSION_SAFETY_20260508_2205.md
```

## Como usar el codigo Edificio 1

Base:

```text
transfer/ws2-ed1-etabs21-context/code/ed1_taller_etabs_legacy/
```

Usar como referencia:

- `config.py`: parametros, unidades, grillas, cargas, espectro, nombres.
- `OAPI_SIGNATURES.md`: firmas COM/OAPI ya investigadas.
- `06_loads.py`: patrones y logica de cargas.
- `07_diaphragm_supports.py`: diafragma, apoyos y asignaciones.
- `07c_automesh.py`: criterio de mesh.
- `08_spectrum_cases.py`: casos espectrales.
- `09_torsion_cases.py`: torsion accidental.
- `10_save_run.py`: guardado/corrida.
- `11_adjust_Rstar.py`: ajustes y chequeos de corte si aplica.
- `12_results.py`: extraccion de resultados/tablas.
- `diag.py`: diagnostico de entorno/OAPI.

No usar directamente sin adaptar:

- `run_all.py`
- `01_init_model.py`
- scripts de geometria que reconstruyan el edificio desde cero

Razon: Edificio 1 ya tiene geometria hecha por UI en WS2. El trabajo correcto ahora no es regenerar geometria, sino completar Parte 1 sobre una copia limpia del `.EDB` real.

## Como debe iterar WS2

Crear una carpeta local de trabajo para scripts adaptados, por ejemplo:

```text
C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog\Edif1\ws2_code_workbench
```

Dentro de esa carpeta, crear scripts incrementales con nombres claros:

```text
00_guard_single_etabs.ps1
01_audit_ed1_current.py
02_prepare_ed1_work_copy.ps1
03_assign_ed1_diaphragm.py
04_define_ed1_load_patterns.py
05_apply_ed1_loads.py
06_define_ed1_mass_source.py
07_define_ed1_modal_spectral.py
08_define_ed1_torsion_combos.py
09_run_ed1_analysis.py
10_export_ed1_results.py
11_verify_ed1_part1.py
```

No es obligatorio usar exactamente esos nombres, pero si es obligatorio separar por bloques verificables.

## Contrato por bloque

Cada script debe:

- conectarse solo a la instancia ETABS valida;
- abrir o adjuntarse a la copia limpia de trabajo, no al original;
- aplicar un grupo pequeno de cambios;
- guardar solo si la validacion del bloque pasa;
- emitir un log `.md` o `.json` con:
  - ruta del modelo;
  - build ETABS;
  - cambios aplicados;
  - conteos antes/despues;
  - tablas consultadas;
  - errores OAPI;
  - siguiente accion.

## Edificio 1: objetivo programatico

Completar sobre:

```text
HECRAS2\prog\Edif1\ED1_PARTE1_COMPLETA_TRABAJO.EDB
```

Primero copiar a una version de trabajo fechada. Despues:

1. re-auditar estado base;
2. preservar releases torsionales pedidos por el profesor;
3. asignar diafragma `D1` donde corresponda;
4. definir `PP`, `SCP`, `SCT`, `TERP`, `TERT`;
5. aplicar cargas segun enunciado actualizado;
6. definir mass source sin duplicar peso propio;
7. definir modal/espectral con NCh433:2026 del curso;
8. definir torsion accidental y combinaciones Ed.1;
9. correr analisis;
10. exportar tablas;
11. verificar Parte 1.

## Edificio 2: uso posterior

Base:

```text
transfer/ws2-ed1-etabs21-context/code/ed2_pipeline_active/
```

Edificio 2 ya tiene pipeline mas maduro. Aun asi:

- no correr antes de cerrar Edificio 1;
- no asumir que el `.EDB` actual coincide 100% con el pipeline;
- auditar 130 losas vs canon nominal 125 panos;
- revisar `TEX/TEY/SDX/SDY`;
- revisar combos contra enunciado;
- usar el pipeline como base adaptable.

## Que debe devolver WS2

WS2 debe devolver:

- scripts adaptados creados o modificados;
- reporte de ejecucion Ed.1;
- tablas exportadas o rutas;
- lista de errores y decisiones;
- si cambia codigo, commit o patch claro;
- delta APOS si corresponde.

La salida minima aceptable no es solo diagnostico. El diagnostico es el paso cero para poder modificar con seguridad.

