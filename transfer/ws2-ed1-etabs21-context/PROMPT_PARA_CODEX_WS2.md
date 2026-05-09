# Prompt para Codex en WS2

Estas trabajando en el proyecto ADSE UCN 1S-2026, Parte 1 de Edificio 1 y Edificio 2, ETABS 21.

## Regla critica

No abras mas de una instancia de ETABS 21.

Antes de abrir ETABS o ejecutar cualquier script COM/API, ejecuta:

```powershell
Get-Process ETABS -ErrorAction SilentlyContinue
```

Si ya existe una instancia, usa esa instancia unica o pide confirmacion antes de cerrar/abrir. No uses dos instancias. No corras dos scripts simultaneos.

## Ruta de trabajo WS2

`C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2`

## Ruta del repo/contexto

No uses `C:\Users\Civil\Documents\taha` para este caso.

Clona el repo dentro de la raiz real `HECRAS2`:

```powershell
cd "C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2"
git clone https://github.com/kcortes765/taha.git codex_ws2_context
cd "C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\codex_ws2_context"
git fetch origin
git checkout codex/ws2-ed1-etabs21-context
```

Si ya existe:

```powershell
cd "C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\codex_ws2_context"
git fetch origin
git checkout codex/ws2-ed1-etabs21-context
git pull --ff-only origin codex/ws2-ed1-etabs21-context
```

## Tu tarea inicial

Este prompt queda como auditoria base. Para ejecucion actual usa tambien:

`transfer/ws2-ed1-etabs21-context/PROMPT_EJECUCION_WS2_ED1_PRIMERO.md`

La auditoria inicial ya fue reportada. Ahora la prioridad es Edificio 1 primero, desde copia limpia fechada, hasta cerrar Parte 1. Edificio 2 se atiende despues.

## Lo que debes encontrar

1. Ruta exacta del `.EDB` activo de Edificio 1.
2. Si existe `ED1_PARTE1_COMPLETA_TRABAJO.EDB` en `HECRAS2\prog\Edif1`.
3. Si existen backups locales.
4. Version/build de ETABS 21.
5. Numero de stories y alturas.
6. Conteo de muros, vigas, losas, joints y apoyos.
7. Confirmacion de que grillas/ejes coinciden con el enunciado/contexto.
8. Confirmacion de vigas invertidas por asignacion:
   - `Cardinal Point = 2 - Bottom Center`
   - `Do not transform frame stiffness for offsets from centroid` marcado
9. Confirmacion de releases:
   - releases de momento y torsion donde corresponde segun criterio del profesor
   - no liberar axial/corte indebida
   - no eliminar releases torsionales de Edificio 1 por defecto
10. Confirmacion de apoyos de base.
11. Confirmacion de modificadores de losa:
   - `m11/m22/m12 = 0.25` para `Losa15G30`
12. Confirmacion de mesh/auto mesh.
13. Confirmacion de diafragmas.
14. Confirmacion de cargas `PP/SCP/SCT/TERP/TERT`.
15. Confirmacion de fuente de masa.
16. Confirmacion de modal/espectral/torsion.

## Archivos de contexto

Lee primero:

- `transfer/ws2-ed1-etabs21-context/README.md`
- `transfer/ws2-ed1-etabs21-context/LICENCIA_ETABS21_REGLA_CRITICA.md`
- `transfer/ws2-ed1-etabs21-context/APOS_X_SYNC_PROTOCOL.md`
- `transfer/ws2-ed1-etabs21-context/PROTOCOLO_UN_EDIFICIO_UNA_INSTANCIA.md`
- `transfer/ws2-ed1-etabs21-context/HANDOFF_WS2_ED1.md`
- `transfer/ws2-ed1-etabs21-context/CODIGO_WS2_MANIFEST.md`
- `transfer/ws2-ed1-etabs21-context/PROMPT_EJECUCION_WS2_ED1_PRIMERO.md`
- `transfer/ws2-ed1-etabs21-context/CHECKLIST_AUDITORIA_MODELO_ED1.md`
- `transfer/ws2-ed1-etabs21-context/APOS_X_BASE/.apos/STATUS.md`
- `transfer/ws2-ed1-etabs21-context/APOS_X_BASE/.apos/HANDOFF.md`
- `transfer/ws2-ed1-etabs21-context/FUENTES_PRIORITARIAS_WS2.md`
- `transfer/ws2-ed1-etabs21-context/ENUNCIADO_CAMBIOS_2026-05-04.md`
- `transfer/ws2-ed1-etabs21-context/APUNTES_CAMBIOS_2026-05-08.md`
- `transfer/ws2-ed1-etabs21-context/PARTE1_ED1_ED2_PROGRAMATICO_2026-05-08.md`
- `transfer/ws2-ed1-etabs21-context/files/13_GUIA_ED1_ETABS_v21.md`
- `transfer/ws2-ed1-etabs21-context/files/21_GUIA_ED2_ETABS_v21.md`
- `transfer/ws2-ed1-etabs21-context/files/01_Enunciado_Taller_actualizado_2026-05-04.pdf`
- `transfer/ws2-ed1-etabs21-context/files/00_Apuntes_del_Curso_2026-05-08_actualizado.pdf`
- `transfer/ws2-ed1-etabs21-context/files/02_Material_Apoyo_Taller_2026.pdf`

## Output esperado

Devuelve un reporte en markdown con tres secciones:

1. `Estado confirmado`
2. `Dudas / no verificable`
3. `Siguiente accion segura`

No sigas modelando hasta cerrar esa auditoria.

El reporte debe cubrir ambos edificios. Edificio 1 y Edificio 2 no tienen el mismo flujo: Ed.1 conserva la matriz de 6 casos; Ed.2 no la hereda y mantiene nucleo estatico con modal/checks segun curso.

Ademas, si modificas memoria APOS en WS2, devuelve un delta en:

`transfer/ws2-ed1-etabs21-context/reports/WS2_APOS_DELTA_YYYYMMDD_HHMM.md`
