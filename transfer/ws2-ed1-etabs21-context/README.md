# WS2 UCN - Edificio 1 ETABS 21 Context

Paquete de transferencia para continuar Edificio 1 en una segunda workstation UCN (`WS2`) despues de perdida/bloqueo de licencia en la workstation anterior.

Leer primero:

`00_START_AQUI_WS2.md`

## Regla critica antes de todo

No abrir mas de una instancia de ETABS 21.

Esto es obligatorio. El usuario reporto que usar mas de una instancia puede producir revoque/bloqueo de licencia.

Antes de abrir ETABS o correr scripts:

```powershell
Get-Process ETABS -ErrorAction SilentlyContinue
```

Si ya hay una instancia abierta, no abrir otra. Usar esa instancia unica o cerrarla manualmente antes de continuar.

## Ruta WS2

Carpeta raiz esperada:

`C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2`

El repo/contexto debe clonarse dentro de esa raiz, no en `C:\Users\Civil\Documents\taha`:

`C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\codex_ws2_context`

Elementos esperados dentro:

- `auxiliar`
- `Edif1`
- `Edif2`
- `prog`
- `espectro_elastico_Z3SC_CL.txt`
- `mapeo muros.png`
- archivos `MODELO EDIF2.*`

## Estado conocido

Este repo no contiene el `.EDB` vivo de WS2. El modelo debe auditarse directamente en la workstation.

Estado previo conocido de WS1:

- Edificio 1 se estaba trabajando en ETABS 21 por UI.
- La planta tipo fue modelada manualmente: grilla, muros, vigas y losas.
- Hubo correcciones por API reportadas antes del bloqueo de licencia:
  - vigas invertidas con `Cardinal Point = 2`
  - offsets automaticos y `Rigid Zone Factor = 0.75`
  - releases solo de momento `M2/M3` donde correspondia
  - apoyos de base empotrados
  - modificadores flexurales de losa `m11/m22/m12 = 0.25`
- Despues de WS1, el usuario reporto que en WS2 hubo un pequeno avance por UI. Ese avance aun no esta trazado en este repo.

## Objetivo inmediato para WS2

No continuar cargando el modelo a ciegas.

Primero se debe analizar el modelo abierto y devolver evidencia de estado:

1. Ruta exacta del `.EDB` activo.
2. Nombre del modelo abierto en ETABS.
3. Version/build de ETABS 21.
4. Numero de stories.
5. Conteo de muros, vigas, losas, puntos y apoyos.
6. Confirmacion de grilla/ejes.
7. Confirmacion de vigas invertidas por asignacion, no por apariencia 3D.
8. Confirmacion de releases.
9. Confirmacion de insertion points y offsets.
10. Confirmacion de mesh/auto mesh.
11. Confirmacion de diafragmas.
12. Confirmacion de patrones de carga.
13. Confirmacion de cargas aplicadas.
14. Confirmacion de fuente de masa.
15. Confirmacion de modal/espectral/torsion.
16. Lista de diferencias contra el estado WS1.

## Archivos de contexto

La carpeta `files/` trae 20 fuentes del paquete WS1:

- enunciado
- material de apoyo taller
- Lafontaine
- manual ETABS
- NCh433:2026
- normas historicas y carga
- apuntes 02c/02d
- guia ED1 ETABS v21
- estado normativo
- notas de modelado manual
- ejes auxiliares
- validaciones y resultados esperados

Ademas se agrego el enunciado actualizado:

`files/01_Enunciado_Taller_actualizado_2026-05-04.pdf`

Ese archivo debe tener prioridad sobre `files/01_Enunciado_Taller.pdf`.

## APOS-X

Este paquete tambien trae un snapshot del APOS-X local:

`APOS_X_BASE/.apos`

WS2 debe usarlo como memoria inicial si necesita contexto completo. Despues, WS2 registra su propio delta y devuelve reportes en:

`reports/`

El protocolo esta en:

`APOS_X_SYNC_PROTOCOL.md`

## Orden de lectura

1. `LICENCIA_ETABS21_REGLA_CRITICA.md`
2. `APOS_X_SYNC_PROTOCOL.md`
3. `HANDOFF_WS2_ED1.md`
4. `PROMPT_PARA_CODEX_WS2.md`
5. `CHECKLIST_AUDITORIA_MODELO_ED1.md`
6. `APOS_X_BASE/.apos/STATUS.md`
7. `FUENTES_PRIORITARIAS_WS2.md`
8. `ENUNCIADO_CAMBIOS_2026-05-04.md`
9. `files/13_GUIA_ED1_ETABS_v21.md`
10. `files/01_Enunciado_Taller_actualizado_2026-05-04.pdf`
11. `files/02_Material_Apoyo_Taller_2026.pdf`

## Criterio de seguridad

- No correr `run_all.py` del pipeline historico sin auditoria: parte de ese codigo estaba orientado a ETABS 19 y/o a reconstruir desde cero.
- No modificar el modelo antes de guardar una copia local.
- No asumir que el estado WS1 sigue intacto.
- No subir `.EDB` a Git salvo decision explicita con Git LFS.
