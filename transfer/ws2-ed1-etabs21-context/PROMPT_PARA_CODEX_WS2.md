# Prompt para Codex en WS2

Estas trabajando en el proyecto ADSE UCN 1S-2026, Edificio 1, ETABS 21.

## Regla critica

No abras mas de una instancia de ETABS 21.

Antes de abrir ETABS o ejecutar cualquier script COM/API, ejecuta:

```powershell
Get-Process ETABS -ErrorAction SilentlyContinue
```

Si ya existe una instancia, usa esa instancia unica o pide confirmacion antes de cerrar/abrir. No uses dos instancias. No corras dos scripts simultaneos.

## Ruta de trabajo WS2

`C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2`

## Tu tarea inicial

No modifiques el modelo al principio.

Primero audita el estado real del modelo Edificio 1 en WS2 y produce un reporte. El usuario necesita devolver esa data al chat principal para decidir el siguiente paso.

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
   - solo momentos `M2/M3` donde corresponde
   - no liberar axial/corte/torsion
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
- `transfer/ws2-ed1-etabs21-context/HANDOFF_WS2_ED1.md`
- `transfer/ws2-ed1-etabs21-context/CHECKLIST_AUDITORIA_MODELO_ED1.md`
- `transfer/ws2-ed1-etabs21-context/APOS_X_BASE/.apos/STATUS.md`
- `transfer/ws2-ed1-etabs21-context/APOS_X_BASE/.apos/HANDOFF.md`
- `transfer/ws2-ed1-etabs21-context/files/13_GUIA_ED1_ETABS_v21.md`
- `transfer/ws2-ed1-etabs21-context/files/01_Enunciado_Taller.pdf`
- `transfer/ws2-ed1-etabs21-context/files/02_Material_Apoyo_Taller_2026.pdf`

## Output esperado

Devuelve un reporte en markdown con tres secciones:

1. `Estado confirmado`
2. `Dudas / no verificable`
3. `Siguiente accion segura`

No sigas modelando hasta cerrar esa auditoria.

Ademas, si modificas memoria APOS en WS2, devuelve un delta en:

`transfer/ws2-ed1-etabs21-context/reports/WS2_APOS_DELTA_YYYYMMDD_HHMM.md`
