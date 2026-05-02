# STATUS - ADSE 1S-2026
Ultima actualizacion: 2026-05-02

## Progreso

### Transferencia WS UCN Ed.1 UI/API
- Estado: paquete Git preparado.
- Ruta activa:
  - `transfer/ws-u-ed1-ui-context/`
- Contenido:
  - 20 archivos de contexto en `transfer/ws-u-ed1-ui-context/files/`
  - README operativo
  - manifest de fuentes
  - comandos para clonar/actualizar en WS
  - prompt base para asistencia en la WS
- Criterio operativo:
  - el modelo `.EDB` vivo se trabaja en la WS UCN, no en este repo
  - este repo pasa contexto, guia UI, normas, apuntes y codigo
  - no versionar `.EDB` salvo decision explicita con Git LFS
- Estado del modelado UI Ed.1:
  - planta tipo en ETABS trabajada manualmente
  - grillas, muros, vigas y losas ya fueron abordados
  - vigas invertidas deben verificarse por asignacion (`Cardinal Point = 2 - Bottom Center`), no solo por apariencia 3D
  - `Do not transform frame stiffness for offsets from centroid` debe quedar marcado, segun Lafontaine/profesor

### Estado normativo del curso
- Estado: rebaselinado.
- Criterio vigente:
  - la base normativa del curso pasa a ser `NCh433:2026`
  - la capa `NCh433 + DS61` queda historica/parcialmente desactualizada
  - esto ya quedo fijado en:
    - `docs/estudio/00-ESTADO-NORMATIVO-CURSO-2026.md`
- Evidencia cruda usada:
  - `materiales_fuente/sismo/correo/emails.json`
  - `app transcripciones/Academico/2026-2/Sismo/02_processed/transcripts/transcript_3d9ff0eeb61c.clean.txt`
  - `materiales_fuente/sismo/Normas Curso/Normas a Utilizar en Curso/NCh433-2026 para Curso.pdf`
- Impacto practico:
  - Ed.1 y Ed.2 deben defenderse formalmente con `NCh433:2026`
  - para `Zona 3 / Sitio C / Categoria II`, los parametros principales siguen coincidiendo numericamente con la capa historica del repo
  - por eso el cambio fuerte es de base canonica y criterio, no necesariamente de numeros en ambos edificios

### Paquetes GPT-5.4 Pro Ed.1
- Estado: listos y migrados a una ronda final de cierre.
- Ruta:
  - nueva sesion 1 actualizada GPT-5.5/5.4 Pro: `review-ia/ed1-gpt55pro-cierre-final-10-sesiones-20x1/01_GEOMETRIA_CANONICA_UI_API_ETABS21/`
  - canonica activa de cierre: `review-ia/ed1-gpt54pro-cierre-final-10-sesiones-20x1/`
  - primera ronda `20+1`: `review-ia/ed1-gpt54pro-10-sesiones-pro-20x1/`
  - historica/sobrecargada: `review-ia/ed1-gpt54pro-10-sesiones/`
- Resultado real:
  - existe una nueva carpeta 2026-04-23 para correr primero geometria canonica Ed.1 con cruce guia UI / codigo ETABS 21:
    - `01_GEOMETRIA_CANONICA_UI_API_ETABS21` -> 20 contextos + 1 prompt
    - zip: `01_GEOMETRIA_CANONICA_UI_API_ETABS21.zip`
  - 10 carpetas planas y curadas para cierre final de Edificio 1
  - cada carpeta activa cumple exactamente `20 archivos de contexto + 1 prompt`
  - existe indice raiz:
    - `review-ia/ed1-gpt54pro-cierre-final-10-sesiones-20x1/00_INDICE_20x1.md`
  - existe generador reproducible:
    - `review-ia/ed1-gpt54pro-cierre-final-10-sesiones-20x1/GENERAR_20x1.ps1`
  - existe capa comun de hallazgos v1 curados:
    - `review-ia/ed1-gpt54pro-cierre-final-10-sesiones-20x1/fuentes-ronda1/`
  - cobertura por sesion final:
    - `01_GEOMETRIA_V2_CONGELAMIENTO` -> 21 archivos
    - `02_MASA_CARGAS_Y_HUELLA_V2` -> 21 archivos
    - `03_MODELO_ETABS_HARDENING_V2` -> 21 archivos
    - `04_KERNEL_SISMICO_ESPECTRO_RSTAR_V2` -> 21 archivos
    - `05_TORSION_ACCIDENTAL_V2` -> 21 archivos
    - `06_CASOS_COMBOS_Y_ESCALAS_V2` -> 21 archivos
    - `07_CM_CR_DRIFT_TORSION_EVIDENCIA_V2` -> 21 archivos
    - `08_TRAZABILIDAD_ETABS_CRUDA_V2` -> 21 archivos
    - `09_DEMANDAS_MUROS_V2` -> 21 archivos
    - `10_REDTEAM_GO_NO_GO_FINAL` -> 21 archivos
- Criterio vigente:
  - el paquete viejo `review-ia/ed1-gpt54pro-10-sesiones/` queda solo como archivo historico
  - el paquete `review-ia/ed1-gpt54pro-10-sesiones-pro-20x1/` queda como baseline de primera ronda
  - el paquete activo `review-ia/ed1-gpt54pro-cierre-final-10-sesiones-20x1/` es el que debe usarse ahora
  - cada carpeta activa esta orientada a congelar un frente, no a repetir una auditoria panoramica
  - la sesion `09_DEMANDAS_MUROS_V2` ya no es "diseno detallado" sino congelamiento de demandas concurrentes
  - la sesion `10_REDTEAM_GO_NO_GO_FINAL` es veredicto tecnico, no resumen amable

### Aclaracion oficial Ed.1 vs Ed.2
- Estado: resuelta contra el enunciado real y correos recientes de Music.
- Confirmado:
  - los 6 casos pertenecen a Ed.1
  - Ed.2 no repite esa tabla
  - Ed.2 sigue con nucleo estatico en Parte 1
  - la primera entrega ahora exige analisis modal de ambos edificios
- Evidencia lista:
  - `evidencia/enunciado-ed1-vs-ed2/`

### Material de estudio
- Completo.

### Guias ETABS UI
- Ed.1: completa.
- Ed.2: rebaselinada al flujo estatico oficial.
- Ed.2 ETABS 21: paquete de auditoria listo para otra IA en:
  - `C:\Seba\seba_os\study\adse_ed2\GUIA_UI_ED2_ETABS21_PAQUETE_PARA_SUBIR`

### Pipeline Ed.2 COM
- Estado: rebaselinado al flujo oficial estatico Parte 1 y endurecido para corrida directa por consola en ETABS 21.
- Documentos activos:
  - `docs/estudio/00-ESTADO-NORMATIVO-CURSO-2026.md`
  - `docs/estudio/ED2_PARTE1_CANON.md`
  - `autonomo/research/ED2_PARTE1_AUDITORIA.md`
  - `docs/estudio/GUIA-EDIFICIO2-MARCOS-ETABS-v21.md`
- Codigo activo:
  - `autonomo/scripts/ed2/config_ed2.py`
  - `autonomo/scripts/ed2/run_pipeline_ed2.py`
  - `autonomo/scripts/ed2/06_assignments_ed2.py`
  - `autonomo/scripts/ed2/diag.py`
  - `autonomo/scripts/ed2/08_seismic_ed2.py`
  - `autonomo/scripts/ed2/09_torsion_ed2.py`
  - `autonomo/scripts/ed2/10_combinations_ed2.py`
  - `autonomo/scripts/ed2/11_run_analysis_ed2.py`
  - `autonomo/scripts/ed2/12_extract_results_ed2.py`
- Cierre pendiente: decidir entre
  - ruta A: aceptar la WS solo como precheck parcial
  - ruta B: export manual UI de drifts/tablas desde ETABS e importarlas offline para cerrar paquete
- Estado nuevo:
  - la ruta B ya quedo operativa
  - la WS ya produjo un cierre UI util con:
    - `Base Reactions`
    - `Story Forces`
    - `Joint Drifts`
    - `Story Drifts`
    - `Story Max Over Avg Drifts`
  - resumen WS:
    - `C:\Users\Civil\Documents\taha\ui_exports_ed2\ed2_ui_summary.md`
  - import local y graficacion ya ejecutados en:
    - `autonomo/scripts/ed2/import_ui_exports_ed2.py`
    - `autonomo/scripts/ed2/plot_ui_results_ed2.py`
  - resultados locales listos en:
    - `autonomo/scripts/ed2/results/ed2_ui_summary.md`
    - `autonomo/scripts/ed2/results/ed2_ui_summary.json`
    - `autonomo/scripts/ed2/results/ui_plots/`
- Cambio reciente:
  - `connect()` ya soporta create/open model por env
  - `run_pipeline_ed2.py` ya soporta `--create-if-missing` y `--model`
  - `06_assignments_ed2.py` ya falla duro si la etapa post-geometria queda incompleta
  - `ED2_RUNTIME_ROOT` ya permite correr en `C:\Users\Civil\Documents\taha`
  - existe `package_transfer_ed2.py` para traer evidencia de vuelta
  - existe `prepare_ws_bundle_ed2.py` y bundle final de 20 archivos
  - el subset minimo Ed.2 ya esta publicado en `https://github.com/kcortes765/taha.git` (`origin/main`)
  - fase 1 ya paso completa en la WS UCN
  - el bloqueo vivo quedo acotado a `08_seismic_ed2.py`: tabla de masa/peso por historia en ETABS 21
  - se empujo un parche adicional para deteccion tolerante de tablas y dump `ed2_available_tables.json`
  - existe runner WS `autonomo/scripts/ed2/tools/ws_run_ed2.ps1` con accion `cleanfull` para matar ETABS, limpiar runtime, actualizar repo y rerun completo
  - la tabla real `Mass Summary by Story` ya fue confirmada en el build ETABS 21.2.0 de la WS
  - `step 08` ya pasa completo en la WS UCN:
    - `Mass Source OK via SetMassSource_1`
    - `Story weights source: Mass Summary by Story`
  - el bloqueo vivo de `step 09` por `CM/CR` ya se destrabo solo para precheck:
    - `step 09` PASS con `CM` geometrico habilitado cuando el build no expone `CM/CR`
  - `step 10` PASS en la WS
  - `step 11` PASS cuando se ejecuta directo (`11_run_analysis_ed2.py`)
  - `step 12` queda bloqueado por capacidad del build ETABS 21.2.0 WS:
    - `Story Forces` por DB devuelve vacio / `ret=1` o `-96`
    - `Joint Drifts`, `Story Drifts`, `Diaphragm Max Over Avg Drifts` y familia relacionada devuelven vacio
    - `SapModel.Results.StoryDrifts()` tambien devuelve arreglos vacios
  - se agregaron probes dedicados:
    - `autonomo/scripts/ed2/diag_story_forces_ed2.py`
    - `autonomo/scripts/ed2/diag_story_drifts_ed2.py`
  - se agrego fallback explicito solo de precheck para `Story Forces`:
    - `12_extract_results_ed2.py --allow-theoretical-story-forces-fallback`
  - ultimo commit operativo publicado: `504035f Add ED2 story drifts probe`

### Pendientes
- Correr la corrida corta pre-Ed.2 de Ed.1 sobre el paquete:
  - `review-ia/ed1-gpt54pro-cierre-final-10-sesiones-20x1/00A_CORRIDA_CORTA_PRE_ED2.md`
- Ejecutar primero las sesiones obligatorias de Ed.1:
  - `01_GEOMETRIA_V2_CONGELAMIENTO`
  - `02_MASA_CARGAS_Y_HUELLA_V2`
  - `04_KERNEL_SISMICO_ESPECTRO_RSTAR_V2`
  - `05_TORSION_ACCIDENTAL_V2`
  - `06_CASOS_COMBOS_Y_ESCALAS_V2`
  - `10_REDTEAM_GO_NO_GO_FINAL`
- Consolidar que frentes quedan realmente congelados y cuales requieren rerun puntual.
- Convertir los hallazgos de cierre de Ed.1 en decisiones canonicas del repo.
- Validar en corrida real ETABS 21 el flujo Ed.2 via API en la WS UCN
- Decidir si Ed.2 WS se cierra como precheck parcial o si se arma una ruta de import manual UI para drifts
- Confirmar que la WS pueda bajar `origin/main` y correr `diag.py` sin bundle manual
- Auditar a fuego la guia UI de Ed.2 para ETABS 21 con el paquete nuevo
- Cruce final UI/API contra la misma corrida real
- Ed.2 Parte 2: diseno de marcos
- Ed.1: modelacion en ETABS

### Lecciones criticas
- Si el objetivo inmediato es volver a Ed.2 Parte 1, no rerun completo Ed.1: usar la corrida corta y cortar cuando la sesion 10 diga que ya solo falta ETABS crudo.
- La imagen de planta del enunciado en Ed.1 no debe quedar como adorno; debe forzar salida en puntos y tramos auditables.
- No tratar `NCh433 + DS61` como norma vigente del curso despues del cambio de 2026.
- Si un numero historico coincide con 2026, se puede conservar el numero, pero no la justificacion vieja.
- No tratar memorias previas ni guias viejas como verdad tecnica.
- No tratar la primera ronda GPT-5.4 Pro de Ed.1 como paquete final de cierre; ya fue absorbida en una segunda ronda mas dura.
- Ed.2 Parte 1 oficial es estatico, no modal-espectral.
- Ed.2 no hereda la matriz de 6 casos de Ed.1.
- El correo del 2026-04-15 amplia la primera entrega: modal de ambos edificios, sin cambiar el nucleo estatico de Ed.2.
- El riesgo mas concreto del pipeline era operacional ETABS 21, no conceptual: firma COM, startup y fallbacks blandos.
- El roundtrip de datos WS <-> local debe pasar por `transfer/`, no por copias manuales dispersas.
- El roundtrip correcto ahora es:
  - codigo por git
  - evidencia por `transfer/`
- El estado "resuelto" exige evidencia local reproducible.
- En el build 21.2.0 del laboratorio, no se puede asumir que exista tabla directa de `CM/CR`; el pipeline debe poder derivar `CM` real desde masas nodales.
- En el build 21.2.0 del laboratorio, tampoco se puede asumir que `Story Forces` ni `drifts` sean accesibles por COM/DB aunque el analisis si corra y entregue base reactions.
- Cuando la UI si expone las tablas, la forma correcta es importarlas como capa separada `ed2_ui_*`, no disfrazarlas como resultados oficiales por COM.
