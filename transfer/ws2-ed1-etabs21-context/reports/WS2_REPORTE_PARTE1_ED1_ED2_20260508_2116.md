# Reporte recibido desde WS2 - estado Edificio 1 y Edificio 2

Fecha reportada: 2026-05-08 21:16 aprox.

## APOS-X en WS2

Paquete recibido:

```text
C:\Users\Civil\Downloads\APOS-X-v1.0 (1).zip
```

Carpeta de trabajo:

```text
C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\_apos_x_work\APOS-X-v1.0_20260508_211010\APOS-X-v1.0
```

Instalado en:

```text
C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\apos-system
```

Verificaciones:

- `VERIFY_PACKAGE.ps1`: `PACKAGE OK`.
- Unit evals: OK, 11 tests.
- `apos_lint.py`: OK en ambos proyectos.
- `apos_append_guard.py`: OK en ambos proyectos.
- `apos-run` bloquea `python run_production.py --pilot --prod`: OK.

Proyectos preparados:

```text
C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\codex_ws2_context
C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog\Edif1\contexto_git
```

No se preparo raiz `HECRAS2` porque no tenia `.apos`, `.agents\skills` ni README propio. No se preparo `APOS_X_BASE` porque parece plantilla/base de transferencia.

Backup:

```text
C:\Users\Civil\APOS-X-backups\apos-x-recipient-20260508-211244
```

Reporte APOS:

```text
C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\APOS_X_FINAL_REPORT_20260508_2113.md
```

## Regla ETABS aplicada en WS2

Antes de OAPI se ejecuto:

```powershell
Get-Process ETABS -ErrorAction SilentlyContinue
```

No habia instancia abierta. Se abrio una sola instancia ETABS 21, sin analisis y sin guardar cambios. Al final no quedo proceso ETABS abierto.

## Edificio 1

Modelo activo probable:

```text
C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog\Edif1\ED1_PARTE1_COMPLETA_TRABAJO.EDB
```

Confirmado por OAPI:

- ETABS 21.2.0; ejecutable build 21.2.0.3353.
- Stories: 20.
- Alturas: piso 1 = 3.4 m; 19 pisos = 2.6 m; altura total = 52.8 m.
- Grillas: 41 lineas, consistente con 33 X + 8 Y.
- Objetos: 1350 puntos, 320 frames, 880 areas.
- Muros: `MHA30G30` = 260 areas; `MHA20G30` = 320 areas.
- Losas: `Losa15G30` = 300 areas.
- Vigas: 320 `VI20/60G30`.
- Vigas invertidas: 320/320 con `Cardinal Point = 2 - Bottom Center`.
- `Do not transform frame stiffness for offsets from centroid`: confirmado.
- Offsets vigas: Auto, `RigidFact = 0.75`.
- Apoyos base: 50 empotrados completos.
- Modificadores `Losa15G30`: `m11/m22/m12 = 0.25`.
- Mesh/auto mesh: presente.

Releases reportados:

- `TI, M2I, M3I`: 180 frames.
- `TJ, M2J, M3J`: 100 frames.
- `TI, M2I, M3I, M2J, M3J`: 40 frames.
- Sin release: 0.

Correccion de canon posterior: el usuario aclaro que los releases torsionales fueron pedidos por el profesor. Por lo tanto, no son un error automatico. Se deben preservar y documentar salvo instruccion explicita contraria.

Falta Edificio 1:

- Diafragma `D1` existe pero no esta asignado a areas.
- Cargas solo `Dead` y `Live`; faltan `PP/SCP/SCT/TERP/TERT`.
- Mass source no corresponde al curso.
- Solo casos `Dead`, `Live`, `Modal`.
- Faltan espectrales/torsion/combinaciones.
- No hay resultados validos.

Base alternativa:

```text
C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog\Edif1\ED1_01_Grilla_v01.EDB
```

Esa base tiene releases sin torsion, pero tambien falta completar cargas, diafragmas, casos y combinaciones. No cambiar a esa base solo porque no tiene releases torsionales.

## Edificio 2

Modelo activo probable:

```text
C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\Edif2\Edificio2_Estatico con carga sismica.EDB
```

Confirmado por OAPI:

- ETABS 21.2.0; build 21.2.0.3353.
- Stories: 5.
- Alturas: piso 1 = 3.5 m; cuatro pisos = 3.0 m; altura total = 15.5 m.
- Grillas: 12 lineas, 6 X + 6 Y.
- Objetos: 261 puntos, 480 frames, 130 areas.
- Columnas: `C70x70G25` = 72; `C65x65G25` = 108; total 180.
- Vigas: `V50x70G25` = 120; `V45x70G25` = 180; total 300.
- Losas: `L17G25` = 130 areas.
- Diafragma: `D1` rigido asignado a 130 areas.
- Apoyos base: 36 empotrados completos.
- Releases: ninguna en 480 frames.
- Offsets: Auto, `RigidFact = 0.75`.
- Cargas: `PP`, `TERT`, `TERP`, `SCP`, `SCT`, `TEX`, `TEY`, `SDX`, `SDY` y auxiliares.
- Mass source: `PP + TERP + TERT + 0.25*SCP + 0.25*SCT`.
- Combinaciones: 20, incluyendo `Peso_Sismico` y `Combo 1` a `Combo 19`.

Falta Edificio 2:

- No hay `LOG/OUT` del archivo activo con carga sismica.
- No hay resultados confirmados.
- Revisar por que hay 130 losas cuando el canon nominal sugiere 125 panos.
- Revisar contenido numerico de `TEX/TEY/SDX/SDY`.
- Mapear nombres actuales a metodo estatico Parte 1.
- Revisar combinaciones `Combo N` contra enunciado.

## Conclusion operativa actualizada

Edificio 1 va primero. No esta listo para analisis porque faltan diafragma asignado, cargas, mass source, casos espectrales/torsion, combinaciones y resultados. Los releases torsionales no se deben eliminar por defecto porque fueron pedido del profesor.

Edificio 2 esta mas cerca de Parte 1, pero queda bloqueado hasta cerrar Edificio 1. Cuando toque Edificio 2, se debe auditar tabla por tabla antes de correr analisis.

