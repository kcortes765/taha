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
4. `transfer/ws2-ed1-etabs21-context/MODO_GOD_WS2.md`
5. `transfer/ws2-ed1-etabs21-context/MODO_GOD_DOCUMENTACION_WS2.md`
6. `transfer/ws2-ed1-etabs21-context/CODIGO_WS2_MANIFEST.md`
7. `transfer/ws2-ed1-etabs21-context/WORKBENCH_CODIGO_WS2.md`
8. `transfer/ws2-ed1-etabs21-context/reports/WS2_REPORTE_PARTE1_ED1_ED2_20260508_2116.md`

Estado operativo:

- WS2 ya instalo APOS-X y audito modelos por OAPI.
- Edificio 1 va primero hasta cerrar Parte 1.
- Edificio 2 queda en espera aunque esta mas avanzado.
- No abrir mas de una instancia ETABS 21.
- No trabajar dos edificios simultaneamente.
- Crear copia limpia fechada antes de modificar cualquier `.EDB`.
- El codigo incluido es base de adaptacion; WS2 debe iterar/adaptar scripts segun el `.EDB` real, no quedarse solo en diagnostico.
- WS2 debe investigar documentacion/norma/apuntes en modo god antes de cada decision tecnica relevante.

Canon importante:

- Los releases torsionales de Edificio 1 fueron pedidos por el profesor.
- No eliminarlos por defecto ni cambiar a la base alternativa solo porque no tiene torsion liberada.

Siguiente accion concreta:

- En WS2, sobre `HECRAS2\prog\Edif1\ED1_PARTE1_COMPLETA_TRABAJO.EDB`, crear backup/copia de trabajo, re-verificar una sola instancia ETABS y completar diafragma, cargas, mass source, casos, combos, analisis y tablas de Parte 1.
# 2026-05-08 - Handoff WS2 prog2 despues de corrida autonoma

- No abrir otra instancia ETABS. Ultima sesion uso PID 23284, ETABS 21.2.0.
- Antes de cualquier OAPI/UI: `Get-Process ETABS -ErrorAction SilentlyContinue`.
- Todo trabajo operativo quedo en `HECRAS2\prog2`.

## Edificio 1
- Modelo copia: `HECRAS2\prog2\Edif1\models\ED1_PARTE1_WS2_PROG2_20260508_2213.EDB`.
- Resultado usable: base dinamica rigida Parte 1, espectro NCh433:2026 via tablas DB, R*/Qmin aplicado.
- Evidencia principal:
  - `HECRAS2\prog2\Edif1\logs\ed1_run-adjust-export_20260508_2247.json`
  - `HECRAS2\prog2\Edif1\reports\ED1_PARTE1_PROG2_run-adjust-export_20260508_2247.md`
- No eliminar releases torsionales.
- Si se exige cierre literal de seis variantes Ed.1, crear copias derivadas y correr variantes una a una.

## Edificio 2
- Modelo copia: `HECRAS2\prog2\Edif2\models\ED2_PARTE1_WS2_PROG2_20260508_2213.EDB`.
- Pipeline usado: `HECRAS2\prog2\Edif2\workbench\ed2_pipeline_active`.
- Wrapper robusto: `ws2_run_extract_ed2.py` porque ETABS expone algunas tablas de resultados solo si `RunAnalysis` y extraccion ocurren en la misma sesion COM.
- Patrones torsionales WS2:
  - `TEX_WS2`
  - `TEY_WS2`
- No reutilizar `TEX/TEY` historicos del modelo para WS2: arrastran estado interno que contamina resultados.
- Verificador final:
  - `HECRAS2\prog2\Edif2\logs\ed2_verify_final_20260508_233545.log`
  - estado `PASS`

# 2026-05-09 - Handoff post-modal ETABS

- La instancia ETABS antigua PID 23284 fue cerrada por instruccion del usuario despues de detectar modal `Error in recovering joint assembled mass`.
- No queda proceso `ETABS` vivo al final de la auditoria post-modal.
- Se agrego mecanismo anti-bloqueo:
  - `HECRAS2\prog2\_common\ws2_etabs_watchdog.py`
  - `HECRAS2\prog2\_common\ws2_etabs_oapi.py`
- Scripts/parches relevantes:
  - `HECRAS2\prog2\Edif1\workbench\ed1_part1_prog2.py`
  - `HECRAS2\prog2\Edif2\workbench\ed2_part1_prog2_audit.py`
  - `HECRAS2\prog2\Edif2\workbench\ed2_pipeline_active\config_ed2.py`
  - `HECRAS2\prog2\Edif2\workbench\ed2_pipeline_active\11_run_analysis_ed2.py`
  - `HECRAS2\prog2\Edif2\workbench\ed2_pipeline_active\ws2_run_extract_ed2.py`
- Auditorias post-modal:
  - ED1: `HECRAS2\prog2\Edif1\reports\ED1_PARTE1_PROG2_audit_20260509_0612.md`
  - ED2: `HECRAS2\prog2\Edif2\reports\ED2_PARTE1_PROG2_audit_20260509_0613.md`
- Advertencia a conservar:
  - ETABS imprimio `Cannot open file ... .Y_` al cerrar ambas auditorias. No hubo evento watchdog ni error en `.LOG/.OUT`, pero si vuelve como modal debe tratarse como bloqueo duro y no como ruido.

# 2026-05-09 - Handoff correccion ED1/ED2

- No usar como resultado ED1 la corrida `ed1_run-adjust-export_20260509_0619`: quedo contaminada por escalamiento Qmin absurdo.
- Copia contaminada preservada en:
  - `HECRAS2\prog2\Edif1\models\quarantine_20260509_0630_bad_qmin_scale`
- Resultado ED1 valido:
  - `HECRAS2\prog2\Edif1\reports\ED1_PARTE1_PROG2_full_20260509_0630.md`
  - `HECRAS2\prog2\Edif1\logs\ed1_full_20260509_0630.json`
  - `HECRAS2\prog2\Edif1\exports\ed1_Base_Reactions_20260509_0630.csv`
- Guardas ED1 nuevas:
  - `Analyze.DeleteResults("", True)` antes de cada analisis;
  - rechazo de amplificaciones Qmin absurdas;
  - rechazo de ratio final Qmin demasiado alto.
- Resultado ED1 limpio:
  - `Qmin=737.086 tonf`;
  - `SEx=740.771 tonf`;
  - `SEy=740.771 tonf`;
  - ratio final `1.005`.
- ED2:
  - `verify_ed2.py` pasa sin configurar `ED2_RUNTIME_ROOT`.
  - estado sigue `PASS`.

# 2026-05-09 - Handoff cierre ampliado ED1/ED2

- Regla operacional:
  - mantener una sola instancia ETABS 21;
  - antes de abrir/usar OAPI ejecutar `Get-Process ETABS -ErrorAction SilentlyContinue`;
  - no correr dos scripts COM en paralelo.
- ED1 base limpia:
  - `HECRAS2\prog2\Edif1\models\ED1_PARTE1_WS2_PROG2_20260508_2213.EDB`.
- ED1 usar para entrega Parte 1:
  - metodo a rigido: `HECRAS2\prog2\Edif1\models\ED1_PARTE1_WS2_PROG2_RIGID_METHOD_A_20260509_0958.EDB`;
  - metodo a semi-rigido: `HECRAS2\prog2\Edif1\models\ED1_PARTE1_WS2_PROG2_SEMIRIGID_METHOD_A_20260509_0958.EDB`;
  - b1/b2 rigido: `HECRAS2\prog2\Edif1\models\ED1_PARTE1_WS2_PROG2_RIGID_MATRIX_20260509_0943.EDB`;
  - b1/b2 semi-rigido: `HECRAS2\prog2\Edif1\models\ED1_PARTE1_WS2_PROG2_SEMIRIGID_MATRIX_20260509_0943.EDB`.
- ED1 reportes:
  - `HECRAS2\prog2\Edif1\reports\ED1_METHOD_A_PROG2_20260509_0958.md`;
  - `HECRAS2\prog2\Edif1\reports\ED1_TORSION_MATRIX_PROG2_20260509_0943.md`;
  - `HECRAS2\prog2\Edif1\reports\ED1_PARTE1_PROG2_full_20260509_0630.md`.
- ED2:
  - modelo: `HECRAS2\prog2\Edif2\models\ED2_PARTE1_WS2_PROG2_20260508_2213.EDB`;
  - verificador: `HECRAS2\prog2\Edif2\workbench\ed2_pipeline_active\verify_ed2.py`;
  - estado: `PASS`, con warning CR real no expuesto.
- Reporte consolidado:
  - `transfer\ws2-ed1-etabs21-context\reports\WS2_CIERRE_PARTE1_ED1_ED2_20260509_1013.md`.

# 2026-05-09 - Handoff auditoria estricta resultados

- Regla operacional:
  - antes de cualquier OAPI/UI ejecutar `Get-Process ETABS -ErrorAction SilentlyContinue`;
  - no abrir segunda instancia ETABS;
  - al cierre de esta auditoria no queda proceso ETABS vivo.
- ED2 fue corregido despues del reporte `WS2_CIERRE_PARTE1_ED1_ED2_20260509_1013.md`.
- Usar como cierre numerico ED2:
  - modelo: `HECRAS2\prog2\Edif2\models\ED2_PARTE1_WS2_PROG2_20260508_2213.EDB`;
  - `W=5378.457675 tonf`;
  - `EX=EY=790.633300 tonf`;
  - `TEX_WS2=TEY_WS2=1877.459200 tonf*m`;
  - `verify_ed2.py`: `PASS` con criterio estricto.
- No usar como cierre final los valores anteriores `EX/EY=779.555 tonf`; quedan como historicos.
- Reporte final de auditoria estricta:
  - `transfer\ws2-ed1-etabs21-context\reports\WS2_AUDITORIA_RESULTADOS_ESTRICTA_20260509_1257.md`.
- Observaciones:
  - CR real no fue expuesto por ETABS; por simetria del modelo se conserva centro como referencia auditada.
  - Si se requiere abrir resultados en UI, revisar que ETABS pueda regenerar/resultados en sesion; la evidencia numerica oficial esta exportada en CSV/JSON.

# 2026-05-09 - Handoff auditoria tipo dios cerrada

- Reporte final:
  - `transfer\ws2-ed1-etabs21-context\reports\WS2_AUDITORIA_TIPO_DIOS_20260509_1424.md`
  - veredicto: `CERRADO`.
- Regla ETABS vigente:
  - ejecutar `Get-Process ETABS -ErrorAction SilentlyContinue` antes de cualquier OAPI/UI;
  - no abrir segunda instancia;
  - usar `--close-if-started` cuando un runner pueda crear ETABS.
- ED1:
  - modelo activo: `HECRAS2\prog2\Edif1\models\ED1_PARTE1_WS2_PROG2_20260508_2213.EDB`;
  - backup bueno para restaurar: `HECRAS2\prog2\Edif1\backups\ED1_PARTE1_WS2_PROG2_20260508_2213_pre_god_verify_20260509_135922.EDB`;
  - exportaciones finales: `HECRAS2\prog2\Edif1\exports\*_20260509_1411.csv`;
  - abrir/resultados: preferir reanalizar y exportar con `--no-final-save` para evitar fragilidad `.Y_`/`miOpen`.
- ED2:
  - modelo activo: `HECRAS2\prog2\Edif2\models\ED2_PARTE1_WS2_PROG2_20260508_2213.EDB`;
  - resultados finales: `HECRAS2\prog2\Edif2\results\ed2_summary.json` y CSV asociados `20260509_1418`;
  - usar `ws2_run_extract_ed2.py --no-final-save --close-if-started` para nueva verificacion.
- Notas no bloqueantes:
  - ED1 combos ULS tienen drift max `0.002089`; el chequeo NCh de drift se cerro con casos sismicos max `0.001353`;
  - ED2 CR no fue expuesto por tabla ETABS, pero por simetria exacta se justifica `CM=CR=(16.25,16.25)`.

# 2026-05-09 - Handoff visuales informe final

- Usar como paquete visual principal:
  - `transfer\ws2-ed1-etabs21-context\reports\visuals\WS2_VISUALES_TIPO_DIOS_20260509_1718\README_VISUALES_INFORME.md`.
- Excel editable:
  - `transfer\ws2-ed1-etabs21-context\reports\visuals\WS2_VISUALES_TIPO_DIOS_20260509_1718\WS2_graficos_editables_20260509_1718.xlsx`.
- Figuras recomendadas para insertar en informe:
  - `00_tablero_ejecutivo.svg`;
  - `01_ed1_corte_basal_qmin.svg`;
  - `04_ed1_drift_casos_sismicos.svg`;
  - `08_ed2_corte_estatico.svg`;
  - `09_ed2_distribucion_fuerzas.svg`;
  - `11_ed2_drift_cm_exceso.svg`;
  - `15_matriz_trazabilidad.svg`.
- Script reproducible:
  - `HECRAS2\prog2\_common\generate_report_visuals.py`.

# 2026-05-09 - Handoff visuales pulidos finales

- Usar como paquete visual principal:
  - `transfer\ws2-ed1-etabs21-context\reports\visuals\WS2_VISUALES_TIPO_DIOS_20260509_1756`.
- Carpeta separada por uso:
  - `transfer\ws2-ed1-etabs21-context\reports\visuals\WS2_VISUALES_TIPO_DIOS_20260509_1756\por_categoria`.
- Para pegar directo en informe:
  - usar `png_2x`, resolucion `3200 x 2000 px`.
- Para editar vectorialmente:
  - usar los `.svg` del paquete o de cada carpeta `por_categoria\*\svg`.
- Graficos nuevos recomendados por la observacion del profesor:
  - `16_ed1_corredor_normativo_derivas`;
  - `17_ed2_corredor_normativo_derivas`.
- ZIPs:
  - `WS2_VISUALES_TIPO_DIOS_20260509_1756_PNG_2X.zip`;
  - `WS2_VISUALES_TIPO_DIOS_20260509_1756_POR_CATEGORIA.zip`.

# 2026-05-09 - Handoff visuales sin solapamiento

- Usar como paquete visual vigente:
  - `transfer\ws2-ed1-etabs21-context\reports\visuals\WS2_VISUALES_TIPO_DIOS_20260509_2221`.
- Motivo:
  - reemplaza al paquete `1756` para insercion en informe porque corrige solapamientos visuales residuales.
- Para pegar directo en informe:
  - usar `png_2x`, todos `3200 x 2000 px`.
- Para escoger por tipo de entrega:
  - `por_categoria\01_obligatorios_directos`;
  - `por_categoria\02_obligatorios_mejorados`;
  - `por_categoria\03_modo_pro_complementarios`.
- Para editar vectorialmente:
  - usar los `.svg` ubicados en la raiz del paquete `2221`.
- ZIPs:
  - `WS2_VISUALES_TIPO_DIOS_20260509_2221_PNG_2X.zip`;
  - `WS2_VISUALES_TIPO_DIOS_20260509_2221_POR_CATEGORIA.zip`.
- Validacion visual:
  - `00_tablero_ejecutivo` OK, notas dentro de tarjeta;
  - `01_ed1_corte_basal_qmin` OK, `Qmin` en badge;
  - `03_ed1_espectro_periodos` OK, `Tx/Ty` separado;
  - `14_comparativo_utilizacion` OK, `limite/objetivo` en badge;
  - hoja de contacto `contact_sheet_png.png` generada.

# 2026-05-09 - Handoff visuales finales con Tx/Ty etiquetado

- Usar como paquete visual vigente:
  - `transfer\ws2-ed1-etabs21-context\reports\visuals\WS2_VISUALES_TIPO_DIOS_20260509_2255`.
- Cambio clave:
  - `03_ed1_espectro_periodos` identifica lineas por color:
    - naranja: `Tx / modo X = 1.105 s`;
    - verde: `Ty / modo Y = 1.094 s`.
- Carpetas por categoria, con PNG y SVG:
  - `por_categoria\01_obligatorios_directos`;
  - `por_categoria\02_obligatorios_mejorados`;
  - `por_categoria\03_modo_pro_complementarios`.
- ZIP recomendado:
  - `WS2_VISUALES_TIPO_DIOS_20260509_2255_POR_CATEGORIA_PNG_SVG.zip`.

# 2026-05-09 - Handoff visuales vigentes en prog2

- Usar como paquete visual vigente:
  - `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\reportes\visuales_informe\WS2_VISUALES_TIPO_DIOS_20260509_2320`.
- Motivo:
  - reemplaza los paquetes anteriores ubicados bajo `codex_ws2_context`; el usuario pidió que la base ordenada quedara solo en `prog2`.
- Texto:
  - títulos, subtítulos, notas y README quedaron con acentos y ñ donde correspondía.
- Para pegar directo en informe:
  - usar `png_2x`, todos en `3200 x 2000 px`.
- Para escoger por tipo de entrega:
  - `por_categoria\01_obligatorios_directos`;
  - `por_categoria\02_obligatorios_mejorados`;
  - `por_categoria\03_modo_pro_complementarios`.
- Para edición vectorial:
  - usar los `.svg` ubicados en la raíz del paquete o dentro de cada carpeta por categoría.
- ZIPs recomendados:
  - `WS2_VISUALES_TIPO_DIOS_20260509_2320_PNG_2X.zip`;
  - `WS2_VISUALES_TIPO_DIOS_20260509_2320_POR_CATEGORIA_PNG_SVG.zip`.
- Validación visual:
  - `00_tablero_ejecutivo` OK;
  - `03_ed1_espectro_periodos` OK, con leyenda Tx/Ty explícita;
  - `16_ed1_corredor_normativo_derivas` OK, con límite normativo y holgura legibles.
- Nota:
  - no se abrió ETABS ni se modificó ningún modelo `.EDB`.

# 2026-05-11 - Handoff modelos clase pre-espectro

- Carpeta de entrega:
  - `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\CLASE_PRE_ESPECTRO_20260511_1356`.
- Abrir para clase:
  - ED1: `Edificio_1\models\ED1_CLASE_PRE_ESPECTRO_20260511.EDB`;
  - ED2: `Edificio_2\models\ED2_CLASE_PRE_ESPECTRO_20260511.EDB`.
- ED1 está justo antes de:
  - definición de espectro;
  - casos `SEx/SEy/SEx_b2/SEy_b2`;
  - torsión;
  - combinaciones dinámicas;
  - análisis espectral.
- ED2 está justo antes de:
  - `EX/EY`;
  - `TEX/TEY`;
  - combinaciones;
  - análisis sísmico final.
- Nota operacional:
  - usar una sola instancia ETABS 21;
  - si la instancia actual sigue abierta, usarla o cerrarla manualmente antes de abrir otra.

# 2026-05-11 - Handoff descarga desde laptop

- Rama a descargar:
  - `codex/ws2-ed1-etabs21-context`.
- Paquete recomendado:
  - `transfer\ws2-ed1-etabs21-context\CLASS_PRE_ESPECTRO_20260511_1356.zip`.
- Carpeta equivalente sin comprimir:
  - `transfer\ws2-ed1-etabs21-context\class_pre_espectro_20260511_1356`.
- Modelos dentro del paquete:
  - `Edificio_1\models\ED1_CLASE_PRE_ESPECTRO_20260511.EDB`;
  - `Edificio_2\models\ED2_CLASE_PRE_ESPECTRO_20260511.EDB`.
- Leer primero:
  - `RESUMEN_MODELOS_CLASE_PRE_ESPECTRO_20260511.md`;
  - `README_CLASE_PRE_ESPECTRO.md`.

# 2026-05-11 - Handoff final Git/APOS

- Para descargar desde laptop, usar rama:
  - `codex/ws2-ed1-etabs21-context`.
- Paquete principal de clase:
  - `transfer\ws2-ed1-etabs21-context\CLASS_PRE_ESPECTRO_20260511_1356.zip`.
- Carpeta equivalente:
  - `transfer\ws2-ed1-etabs21-context\class_pre_espectro_20260511_1356`.
- Visuales finales de informe:
  - `transfer\ws2-ed1-etabs21-context\reports\visuals\WS2_VISUALES_TIPO_DIOS_20260509_2320`;
  - `transfer\ws2-ed1-etabs21-context\reports\visuals\WS2_VISUALES_TIPO_DIOS_20260509_2320_PNG_2X.zip`;
  - `transfer\ws2-ed1-etabs21-context\reports\visuals\WS2_VISUALES_TIPO_DIOS_20260509_2320_POR_CATEGORIA_PNG_SVG.zip`.
- Validación local previa a push:
  - `APOS lint: OK`;
  - sin `_edge_profile` en staged.

# 2026-05-11 - Descarga desde laptop lista

- Rama remota actualizada:
  - `origin/codex/ws2-ed1-etabs21-context`.
- Commit principal con el paquete:
  - `3e7d199 Add WS2 class package and final APOS handoff`.
- En laptop, descargar la rama y revisar:
  - `transfer\ws2-ed1-etabs21-context\CLASS_PRE_ESPECTRO_20260511_1356.zip`;
  - `transfer\ws2-ed1-etabs21-context\class_pre_espectro_20260511_1356`;
  - `transfer\ws2-ed1-etabs21-context\reports\visuals\WS2_VISUALES_TIPO_DIOS_20260509_2320`.

# 2026-05-11 - Handoff paquete final Parte 1

- Además del paquete de clase, descargar para contexto completo:
  - `transfer\ws2-ed1-etabs21-context\P1_FINAL_MODELOS_RESULTADOS_20260511_1431.zip`.
- Carpeta equivalente:
  - `transfer\ws2-ed1-etabs21-context\p1_final_20260511_1431`.
- Modelos activos:
  - ED1: `E1\models\ED1_PARTE1_WS2_PROG2_20260508_2213.EDB`.
  - ED2: `E2\models\ED2_PARTE1_WS2_PROG2_20260508_2213.EDB`.
