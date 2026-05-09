# WS2 UCN - Edificio 1 ETABS 21 Context

Paquete de transferencia para continuar Edificio 1 en una segunda workstation UCN (`WS2`) despues de perdida/bloqueo de licencia en la workstation anterior.

Actualizacion 2026-05-08: este paquete tambien incluye fuentes y criterio para resolver programaticamente Parte 1 de Edificio 2. El nombre historico de la carpeta conserva `ed1`, pero el alcance operativo WS2 ahora es `Ed.1 + Ed.2 Parte 1`.

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

Objetivo actual: terminar Edificio 1 Parte 1 primero. Luego asegurar Edificio 2.

La auditoria inicial ya reporto estado base de ambos edificios. Antes de modificar, WS2 debe crear copia limpia fechada del `.EDB` activo y verificar que sigue siendo el mismo estado.

Para Edificio 1 se debe completar:

1. diafragma asignado a areas;
2. patrones y cargas `PP/SCP/SCT/TERP/TERT`;
3. fuente de masa correcta;
4. modal/espectral;
5. torsion accidental y casos/combinaciones;
6. analisis;
7. exportacion de tablas;
8. reporte trazable.

Los releases torsionales de Edificio 1 fueron pedidos por el profesor; no eliminarlos por defecto.

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

Tambien se agregaron los apuntes actualizados:

`files/00_Apuntes_del_Curso_2026-05-08_actualizado.pdf`

Ese archivo debe tener prioridad sobre `docs/Apuntes del Curso.pdf` y sobre el indice cortado antiguo cuando haya conflicto de paginacion.

Para Edificio 2 se agrego:

- `files/21_GUIA_ED2_ETABS_v21.md`
- `files/22_ED2_PARTE1_CANON.md`
- `PARTE1_ED1_ED2_PROGRAMATICO_2026-05-08.md`

Codigo incluido:

- `code/ed1_taller_etabs_legacy/`
- `code/ed2_pipeline_active/`

Ver detalle en `CODIGO_WS2_MANIFEST.md`.

Ver contrato de adaptacion en `WORKBENCH_CODIGO_WS2.md`. WS2 debe usar el codigo como base para iterar y adaptar al `.EDB` real, no como diagnostico pasivo ni como pipeline para correr sin cambios.

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
3. `PROTOCOLO_UN_EDIFICIO_UNA_INSTANCIA.md`
4. `HANDOFF_WS2_ED1.md`
5. `CODIGO_WS2_MANIFEST.md`
6. `WORKBENCH_CODIGO_WS2.md`
7. `PROMPT_EJECUCION_WS2_ED1_PRIMERO.md`
8. `CHECKLIST_AUDITORIA_MODELO_ED1.md`
9. `APOS_X_BASE/.apos/STATUS.md`
10. `FUENTES_PRIORITARIAS_WS2.md`
11. `ENUNCIADO_CAMBIOS_2026-05-04.md`
12. `APUNTES_CAMBIOS_2026-05-08.md`
13. `PARTE1_ED1_ED2_PROGRAMATICO_2026-05-08.md`
14. `files/00_Apuntes_del_Curso_2026-05-08_actualizado.pdf`
15. `files/13_GUIA_ED1_ETABS_v21.md`
16. `files/21_GUIA_ED2_ETABS_v21.md`
17. `files/01_Enunciado_Taller_actualizado_2026-05-04.pdf`
18. `files/02_Material_Apoyo_Taller_2026.pdf`

## Criterio de seguridad

- No correr `run_all.py` del pipeline historico sin auditoria: parte de ese codigo estaba orientado a ETABS 19 y/o a reconstruir desde cero.
- No modificar el modelo antes de guardar una copia local.
- No asumir que el estado WS1 sigue intacto.
- No subir `.EDB` a Git salvo decision explicita con Git LFS.
