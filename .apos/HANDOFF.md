# HANDOFF - ADSE 1S-2026

**Actualizacion:** 2026-05-08

## Delta nuevo
- Regla critica nueva:
  - no abrir ni usar mas de una instancia de ETABS 21
  - el usuario reporto riesgo de revoque/bloqueo de licencia si hay mas de una instancia
  - antes de abrir ETABS o correr scripts COM/API, verificar `Get-Process ETABS -ErrorAction SilentlyContinue`
- Se migra continuidad de Edificio 1 a WS2:
  - raiz reportada: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2`
  - ruta corregida para repo/contexto: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\codex_ws2_context`
  - no usar `C:\Users\Civil\Documents\taha` para este flujo
  - paquete nuevo: `transfer/ws2-ed1-etabs21-context/`
- Cambio real:
  - WS1 queda como antecedente
  - WS2 debe auditar el modelo real primero, no continuar a ciegas
  - el usuario reporta que en WS2 ya hubo un avance leve por UI despues de WS1, pero no esta documentado
- Archivos nuevos clave:
  - `ETABS21_REGLA_LICENCIA.md`
  - `transfer/ws2-ed1-etabs21-context/README.md`
  - `transfer/ws2-ed1-etabs21-context/LICENCIA_ETABS21_REGLA_CRITICA.md`
  - `transfer/ws2-ed1-etabs21-context/APOS_X_SYNC_PROTOCOL.md`
  - `transfer/ws2-ed1-etabs21-context/APOS_X_BASE/.apos/`
  - `transfer/ws2-ed1-etabs21-context/HANDOFF_WS2_ED1.md`
  - `transfer/ws2-ed1-etabs21-context/PROMPT_PARA_CODEX_WS2.md`
  - `transfer/ws2-ed1-etabs21-context/CHECKLIST_AUDITORIA_MODELO_ED1.md`
  - `transfer/ws2-ed1-etabs21-context/WS2_COMMANDS.md`
  - `transfer/ws2-ed1-etabs21-context/HECRAS2_ARCHIVOS_ESPERADOS.md`
  - `transfer/ws2-ed1-etabs21-context/FUENTES_PRIORITARIAS_WS2.md`
  - `transfer/ws2-ed1-etabs21-context/ENUNCIADO_CAMBIOS_2026-05-04.md`
  - `docs/Apuntes del Curso 2026-05-08 actualizado.pdf`
  - `transfer/ws2-ed1-etabs21-context/files/00_Apuntes_del_Curso_2026-05-08_actualizado.pdf`
  - `transfer/ws2-ed1-etabs21-context/APUNTES_CAMBIOS_2026-05-08.md`
  - `transfer/ws2-ed1-etabs21-context/PARTE1_ED1_ED2_PROGRAMATICO_2026-05-08.md`
  - `transfer/ws2-ed1-etabs21-context/files/21_GUIA_ED2_ETABS_v21.md`
  - `transfer/ws2-ed1-etabs21-context/files/22_ED2_PARTE1_CANON.md`

## Siguiente accion inmediata
1. En WS2, bajar rama `codex/ws2-ed1-etabs21-context`.
   - clonar dentro de `HECRAS2\codex_ws2_context`
2. Leer `transfer/ws2-ed1-etabs21-context/README.md`.
3. Verificar que no haya mas de una instancia ETABS:
   - `Get-Process ETABS -ErrorAction SilentlyContinue`
4. Identificar los `.EDB` activos de Edificio 1 y Edificio 2 dentro de `HECRAS2`.
5. Crear reporte de auditoria de ambos modelos antes de modificar.
6. Si WS2 actualiza APOS, devolver delta en `transfer/ws2-ed1-etabs21-context/reports/`.

## Delta 2026-05-04
- Se recibio estado externo de Ed.1 en WS ETABS 21.
- El modelo base ya habria sido corregido por API COM antes del bloqueo de licencia.
- Ruta de trabajo al retomar:
  - `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS\prog\Edif1\ED1_PARTE1_COMPLETA_TRABAJO.EDB`
- Rutas de respaldo:
  - original corregido: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS\prog\Edif1\ED1_01_Grilla_v01.EDB`
  - backup pre-correcciones: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS\prog\Edif1\backups\ED1_01_Grilla_v01_pre_correcciones_20260502_193648.EDB`
- Correcciones reportadas:
  - 320 vigas con `Cardinal Point = 2`
  - offsets automaticos y `Rigid Zone Factor = 0.75`
  - releases limpios solo en `M2/M3`
  - base empotrada en 50 puntos
  - modificadores flexurales de losa `0.25`
- Pendiente vivo:
  - licencia ETABS 21
  - cargas, masa, diafragmas, modal/espectral, torsion, analisis y tablas

## Siguiente accion inmediata 2026-05-04
1. Esperar/reactivar licencia ETABS 21 en la WS.
2. Abrir solo:
   - `ED1_PARTE1_COMPLETA_TRABAJO.EDB`
3. Re-verificar correcciones base antes de modificar:
   - vigas invertidas
   - offsets/rigid zone
   - releases
   - apoyos
   - modificadores de losa
4. Continuar con:
   - diafragmas
   - patrones y cargas
   - mass source
   - modal/espectral
   - torsion accidental / 6 casos
   - analisis y export de tablas

## Delta 2026-05-02
- Se preparo un paquete de transferencia Git para continuar Edificio 1 en la WS UCN:
  - `transfer/ws-u-ed1-ui-context/`
- La carpeta contiene:
  - `files/` con 20 archivos de contexto
  - `README.md`
  - `MANIFEST.md`
  - `WS_U_COMMANDS.md`
  - `PROMPT_BASE_WS_U.md`
- Aclaracion operativa:
  - el modelo ETABS `.EDB` vive en la WS y se trabaja por UI
  - este repo se usa para bajar contexto, guia, material del profesor, normas y codigo
  - no subir `.EDB` al repo sin decidir Git LFS
- Estado actual Ed.1 UI:
  - se esta trabajando desde planta tipo/manual
  - se detecto que la apariencia 3D de vigas invertidas puede confundir
  - criterio canonico: verificar `Insertion Point = 2 - Bottom Center` por asignacion/tablas
  - la casilla `Do not transform frame stiffness for offsets from centroid` queda marcada por alineacion con Lafontaine/profesor

## Siguiente accion inmediata 2026-05-02
1. Empujar rama `codex/ws-u-ed1-ui-context`.
2. En la WS:
   - clonar o actualizar repo
   - hacer checkout de la rama
   - abrir `transfer/ws-u-ed1-ui-context/`
3. Continuar el modelo en ETABS 21 desde el `.EDB` local de la WS, usando la guia `13_GUIA_ED1_ETABS_v21.md`.
4. No volver a aplicar comandos masivos sin checkpoint previo.

## Delta anterior
- Se creo una nueva carpeta operativa para la primera sesion externa de Edificio 1:
  - `review-ia/ed1-gpt55pro-cierre-final-10-sesiones-20x1/01_GEOMETRIA_CANONICA_UI_API_ETABS21/`
- La carpeta trae `20 archivos de contexto + 1 prompt maestro` y un zip opcional:
  - `review-ia/ed1-gpt55pro-cierre-final-10-sesiones-20x1/01_GEOMETRIA_CANONICA_UI_API_ETABS21.zip`
- Foco: congelar o bloquear la geometria canonica del Edificio 1 cruzando enunciado, imagenes, guia UI y scripts ETABS 21.
- Criterio nuevo: GPT-5.5 Pro es recomendado si esta disponible; GPT-5.4 Pro sigue siendo compatible. Image 2.0 queda solo como salida visual posterior, no como fuente tecnica.

## Siguiente accion inmediata anterior
1. Subir los 20 archivos de contexto de `01_GEOMETRIA_CANONICA_UI_API_ETABS21/`.
2. Pegar `21_PROMPT_GPT55PRO_GEOMETRIA_CANONICA_UI_API_ETABS21.md` como prompt maestro.
3. Exigir salida en `GEOM_ED1_PUNTOS`, `GEOM_ED1_TRAMOS`, cambios de guia UI y cambios de codigo ETABS 21.

**Ultima sesion:** 2026-04-20

## Que se hizo
- Se fijo una nueva capa canonica de normativa del curso en:
  - `docs/estudio/00-ESTADO-NORMATIVO-CURSO-2026.md`
- Se dejo asentado que:
  - `NCh433:2026` manda hoy en el curso
  - `NCh433 + DS61` queda como capa historica/parcialmente desactualizada
  - Ed.1 y Ed.2 deben defenderse formalmente con 2026
  - en ambos edificios, para `Zona 3 / Sitio C / Categoria II`, varios parametros principales siguen coincidiendo numericamente con la capa historica
- Se actualizo `docs/estudio/ED2_PARTE1_CANON.md` para reamarrar Edificio 2 a `NCh433:2026`.
- Se absorbio la primera ronda completa de 10 salidas GPT-5.4 Pro de Ed.1 en un nuevo paquete activo de cierre final:
  - `review-ia/ed1-gpt54pro-cierre-final-10-sesiones-20x1/`
- Ese paquete nuevo:
  - mantiene formato estricto `20 contextos + 1 prompt`
  - trae `fuentes-ronda1/` con hallazgos v1 curados
  - reordena las 10 carpetas como frentes de cierre y no como auditorias generales
  - fue validado con `GENERAR_20x1.ps1` y quedo con 10 carpetas de `21 archivos`
- Se redefinio la sesion 9 como:
  - `09_DEMANDAS_MUROS_V2`
  - foco en congelar demandas concurrentes de muros, no detalle final de acero
- Se mantuvo intacto el paquete viejo `review-ia/ed1-gpt54pro-10-sesiones/` y el paquete de primera ronda `review-ia/ed1-gpt54pro-10-sesiones-pro-20x1/` como capas historicas.

## Que cambio
- El paquete activo de Ed.1 ya no es el `20+1` de primera ronda.
- La estrategia actual de Ed.1 pasa a ser:
  - cierre secuencial
  - congelamiento de frentes
  - trazabilidad
  - go/no-go final
- El siguiente agente no debe volver a pedir una auditoria panoramica de Ed.1 si ya tiene el nuevo paquete de cierre.

## Que debe hacer el siguiente agente
1. Usar como punto de entrada:
   - `review-ia/ed1-gpt54pro-cierre-final-10-sesiones-20x1/00_INDICE_20x1.md`
2. Si se va a correr el paquete final con GPT-5.4 Pro, hacerlo en este orden:
   - si el objetivo sigue siendo cerrar Ed.2 Parte 1, usar primero:
     - `review-ia/ed1-gpt54pro-cierre-final-10-sesiones-20x1/00A_CORRIDA_CORTA_PRE_ED2.md`
   - subset obligatorio:
     - `01_GEOMETRIA_V2_CONGELAMIENTO`
     - `02_MASA_CARGAS_Y_HUELLA_V2`
     - `04_KERNEL_SISMICO_ESPECTRO_RSTAR_V2`
     - `05_TORSION_ACCIDENTAL_V2`
     - `06_CASOS_COMBOS_Y_ESCALAS_V2`
     - `10_REDTEAM_GO_NO_GO_FINAL`
   - subset condicional:
     - `03_MODELO_ETABS_HARDENING_V2`
     - `07_CM_CR_DRIFT_TORSION_EVIDENCIA_V2`
     - `08_TRAZABILIDAD_ETABS_CRUDA_V2`
   - no correr `09_DEMANDAS_MUROS_V2` mientras el foco siga en Parte 1
3. Si algun frente alto cambia fuerte:
   - geometria
   - kernel sismico
   - torsion / 6 casos
   entonces no confiar ciegamente en resultados aguas abajo y rerun solo lo necesario.
4. Mantener Ed.2 separado:
   - la capa `ed2_ui_*` sigue vigente como respaldo local
   - el bloqueo COM de drifts/story forces en la WS no se resolvio en esta sesion
5. Cuando use guias o resumentes del repo:
   - filtrar primero con `docs/estudio/00-ESTADO-NORMATIVO-CURSO-2026.md`
   - no asumir que una referencia a `DS61` sigue siendo canon del curso

## Que no debe asumir
- No asumir que `review-ia/ed1-gpt54pro-10-sesiones-pro-20x1/` sigue siendo el paquete activo; ahora es baseline de primera ronda.
- No asumir que la sesion 9 de Ed.1 ya permite detalle de armaduras; primero deben congelarse demandas concurrentes.
- No asumir que un hallazgo v1 sea canon solo porque esta escrito; el paquete nuevo lo trata como baseline a confirmar o refutar.
- No mezclar cierres Ed.1 con el trabajo pendiente de Ed.2.

## Contexto minimo para retomar
1. `.apos/BOOTSTRAP.md`
2. `.apos/STATUS.md`
3. `.apos/DECISIONS.md`
4. `.apos/JOURNAL.md`
5. `review-ia/ed1-gpt54pro-cierre-final-10-sesiones-20x1/00_INDICE_20x1.md`
6. `review-ia/ed1-gpt54pro-cierre-final-10-sesiones-20x1/fuentes-ronda1/00_RESUMEN_RONDA1.md`
7. `review-ia/ed1-gpt54pro-cierre-final-10-sesiones-20x1/fuentes-ronda1/01_BLOQUEOS_Y_DEPENDENCIAS.md`
8. `review-ia/ed1-gpt54pro-cierre-final-10-sesiones-20x1/09_DEMANDAS_MUROS_V2/00_MAPA_DE_CARGA.md`
9. `review-ia/ed1-gpt54pro-cierre-final-10-sesiones-20x1/10_REDTEAM_GO_NO_GO_FINAL/20_PROMPT_GPT54PRO.md`
10. `docs/estudio/00-ESTADO-NORMATIVO-CURSO-2026.md`
11. `review-ia/ed1-gpt54pro-cierre-final-10-sesiones-20x1/00A_CORRIDA_CORTA_PRE_ED2.md`

## Actualizacion 2026-05-08 noche - WS2 ejecucion Ed.1 primero

El siguiente agente debe partir de:

1. `transfer/ws2-ed1-etabs21-context/00_START_AQUI_WS2.md`
2. `transfer/ws2-ed1-etabs21-context/PROTOCOLO_UN_EDIFICIO_UNA_INSTANCIA.md`
3. `transfer/ws2-ed1-etabs21-context/PROMPT_EJECUCION_WS2_ED1_PRIMERO.md`
4. `transfer/ws2-ed1-etabs21-context/CODIGO_WS2_MANIFEST.md`
5. `transfer/ws2-ed1-etabs21-context/WORKBENCH_CODIGO_WS2.md`
6. `transfer/ws2-ed1-etabs21-context/reports/WS2_REPORTE_PARTE1_ED1_ED2_20260508_2116.md`

Estado operativo:

- WS2 ya instalo APOS-X y audito modelos por OAPI.
- Edificio 1 va primero hasta cerrar Parte 1.
- Edificio 2 queda en espera aunque esta mas avanzado.
- No abrir mas de una instancia ETABS 21.
- No trabajar dos edificios simultaneamente.
- Crear copia limpia fechada antes de modificar cualquier `.EDB`.
- El codigo incluido es base de adaptacion; WS2 debe iterar/adaptar scripts segun el `.EDB` real, no quedarse solo en diagnostico.

Canon importante:

- Los releases torsionales de Edificio 1 fueron pedidos por el profesor.
- No eliminarlos por defecto ni cambiar a la base alternativa solo porque no tiene torsion liberada.

Siguiente accion concreta:

- En WS2, sobre `HECRAS2\prog\Edif1\ED1_PARTE1_COMPLETA_TRABAJO.EDB`, crear backup/copia de trabajo, re-verificar una sola instancia ETABS y completar diafragma, cargas, mass source, casos, combos, analisis y tablas de Parte 1.
