# JOURNAL - ADSE 1S-2026

## 2026-03-20 - Pivot metodologico y cierre de la etapa COM pura
- Hicimos: auditamos varias iteraciones del modelado ETABS via COM y contrastamos el resultado contra planos y elevaciones.
- Cambio real: el proyecto dejo de asumir que la automatizacion COM, por si sola, podia cerrar la geometria correcta.
- Correccion o descubrimiento: la geometria no estaba suficientemente validada y no tenia sentido seguir avanzando a analisis sin evidencia visual.
- Siguiente paso: congelar decisiones geometricas criticas y dejar explicito que la validacion viva era bloqueante.

## 2026-04-03 - Rebaseline de Ed.2 Parte 1 al flujo estatico oficial
- Hicimos: consolidamos el canon oficial de Ed.2 Parte 1, auditamos guias y scripts, y reescribimos la guia v21 al flujo estatico correcto.
- Cambio real: la referencia activa paso a ser el metodo estatico oficial del curso, apoyado por resultados reales en `results/`.
- Correccion o descubrimiento: memorias y guias antiguas podian servir como apoyo, pero no como verdad tecnica.
- Siguiente paso: ejecutar una corrida real en ETABS 21, extraer resultados y validar con evidencia reproducible.

## 2026-04-16 - Aclaracion Ed.1 vs Ed.2 y paquete de auditoria UI ETABS 21
- Hicimos: releimos el enunciado real, cruzamos correos recientes de Music y armamos un paquete especifico para auditar la guia UI de Ed.2 en ETABS 21.
- Cambio real: quedo resuelto que los 6 casos son de Ed.1 y que Ed.2 mantiene nucleo estatico, pero con modal exigido para primera entrega.
- Correccion o descubrimiento: la confusion no venia del curso sino de mezclar la tabla de Ed.1 con el inicio de Ed.2 y de ignorar el correo del 2026-04-15.
- Siguiente paso: usar el paquete nuevo para auditar la guia UI y luego validar el flujo en ETABS 21 real.

## 2026-04-19 - Endurecimiento del pipeline API Ed.2 para ETABS 21 WS UCN
- Hicimos: corregimos la firma COM de `SetInsertionPoint`, agregamos arranque/apertura de modelo por consola y volvimos la etapa 06 fail-fast con conteos esperados.
- Cambio real: el flujo programatico ya no depende de pasos manuales ambiguos para insertion point, edge constraints ni startup de ETABS.
- Correccion o descubrimiento: el riesgo principal ya no era teorico/normativo, sino operacional ETABS 21 real en la workstation.
- Siguiente paso: correr el pipeline en la WS UCN con ETABS 21 y cerrar `verify_ed2.py` con evidencia real.

## 2026-04-19 - Portabilidad WS y bundle final de 20 archivos
- Hicimos: agregamos `ED2_RUNTIME_ROOT`, un empaquetador de retorno y un generador de bundle corto para la WS o revision externa.
- Cambio real: ahora existe un camino operativo claro para llevar codigo a `C:\Users\Civil\Documents\taha`, correrlo ahi y devolver evidencia empaquetada.
- Correccion o descubrimiento: algunas rutas seguian clavadas a `scripts/ed2/results`; eso ya quedo centralizado.
- Siguiente paso: prueba preliminar en la WS con `ED2_WS_BUNDLE_FINAL`, y solo si falla acudir a GPT Pro.

## 2026-04-19 - Publicacion GitHub del paquete minimo Ed.2
- Hicimos: publicamos un subset limpio del paquete Ed.2 en `https://github.com/kcortes765/taha.git` para que la WS pueda bajar codigo real por git.
- Cambio real: la WS ya no depende de copiar manualmente el bundle en cada iteracion; git pasa a ser el canal principal para codigo.
- Correccion o descubrimiento: el repo remoto existia pero estaba vacio; se resolvio con un commit minimo publicable en `origin/main`.
- Siguiente paso: ejecutar `git fetch / checkout origin/main` en la WS, correr `diag.py` y lanzar la prueba preliminar real.

## 2026-04-19 - Primera corrida WS real: fase 1 PASS, bloqueo en masa por historia
- Hicimos: corrimos `diag.py` y `run_pipeline_ed2.py` en la WS UCN con ETABS 21.2.0.
- Cambio real: ya no hay dudas sobre startup, modelado base ni etapa 06; todo eso paso en la workstation real.
- Correccion o descubrimiento: el bloqueo vivo quedo aislado en `08_seismic_ed2.py`, porque el build del laboratorio no reconoce bajo los nombres esperados la tabla de masa/peso por historia.
- Siguiente paso: bajar el commit `9660ebc`, reintentar solo fase 2 y, si vuelve a fallar, traer `ed2_available_tables.json`.

## 2026-04-19 - Runner cleanfull para la WS
- Hicimos: extendimos `ws_run_ed2.ps1` para el caso real de la WS, donde el repo vive directamente en `C:\Users\Civil\Documents\taha`, la rama buena es `main` y a veces conviene partir desde cero limpio.
- Cambio real: ahora existe una accion `cleanfull` que mata ETABS, limpia artefactos del runtime, actualiza repo y rerun completo sin tener que ir pegando bloques separados.
- Correccion o descubrimiento: la forma anterior seguia muy propensa a errores operativos de copia y a estados mixtos entre sesiones.
- Siguiente paso: usar `cleanfull` si el usuario quiere reset total; si no, seguir con iteraciones cortas sobre `phase 2`.

## 2026-04-19 - Reruns de phase 2 blindados para ETABS 21
- Hicimos: confirmamos en la WS que `Mass Summary by Story` si existe en ETABS 21.2.0 y movimos el foco al error `ret=1` de `SetMassSource_1` en reintentos de `phase 2`.
- Cambio real: `08_seismic_ed2.py` ahora desbloquea el modelo antes de tocar la fuente de masa y cae a `PropMaterial.SetMassSource(...)` si `_1` falla.
- Correccion o descubrimiento: el problema ya no era el nombre de tabla sino el estado del modelo despues de un analisis previo.
- Siguiente paso: hacer pull del commit `fab743d` en la WS y reintentar solo `phase 2`.

## 2026-04-19 - Parser de pesos por historia ampliado para ETABS 21.2.0
- Hicimos: corregimos la deteccion del return code de `SetMassSource_1` y ampliamos `extract_story_weights_from_db()` para aceptar mas variantes de columnas y nombres de historia.
- Cambio real: el paso 08 ya no depende de comparaciones literales tipo `mass x` vs `MassX` ni de que el nombre del piso venga exactamente igual al del script.
- Correccion o descubrimiento: la tabla existia, pero el parser seguia siendo demasiado rigido para el build del laboratorio.
- Siguiente paso: bajar `2f51987` en la WS y reintentar solo `phase 2`.

## 2026-04-19 - Sonda cruda para `Mass Summary by Story`
- Hicimos: agregamos `diag_story_weights_ed2.py` para capturar el resultado bruto de `GetTableForDisplayArray` sobre las tablas candidatas de masa/peso por historia.
- Cambio real: la siguiente iteracion ya no depende de adivinar el layout del tuple que devuelve CSI; ahora podemos parchear con evidencia exacta del build 21.2.0 del laboratorio.
- Correccion o descubrimiento: el parser ya habia agotado las heuristicas razonables sin ver el payload real.
- Siguiente paso: hacer pull de `775b8e8` en la WS y correr la sonda.

## 2026-04-19 - Confirmado formato real `Story, UX, UY, UZ`
- Hicimos: inspeccionamos el JSON de sonda generado en la WS y verificamos el formato exacto de `Mass Summary by Story`.
- Cambio real: el parser ya acepta `UX/UY/UZ` como masas por historia y puede convertirlas a peso multiplicando por `g`.
- Correccion o descubrimiento: el bloqueo no era el tuple de CSI sino que la logica seguia esperando nombres de campo mas verbosos.
- Siguiente paso: hacer pull de `aebb01f` en la WS y reintentar `phase 2`.

## 2026-04-19 - `step 08` cerrado y `CM` derivado desde masas nodales
- Hicimos: confirmamos en la WS que `step 08` ya pasa completo y parcheamos el paquete para derivar `CM` por piso desde `Assembled Joint Masses` cuando el build ETABS 21.2.0 no expone tabla directa de `CM/CR`.
- Cambio real: el bloqueo vivo se movio de pesos por historia a `step 09`, y el pipeline ya no depende de centro geometrico para aplicar el estatico ni para filtrar drift en `CM`.
- Correccion o descubrimiento: el build del laboratorio puede no traer `Centers Of Mass And Rigidity`; eso no invalida el `CM` si se reconstruye desde masas nodales y coordenadas.
- Siguiente paso: hacer pull de `ac4f5f1` en la WS y rerun de `phase 2`.

## 2026-04-20 - Paquetes externos Ed.1 para 10 sesiones GPT-5.4 Pro
- Hicimos: creamos `review-ia/ed1-gpt54pro-10-sesiones/` y poblamos 10 carpetas autosuficientes para auditoria profunda de Edificio 1.
- Cambio real: Ed.1 ya no depende de un solo prompt o de contexto suelto; ahora tiene un paquete estructurado por tema con fuentes del curso, memorias, evidencia y codigo relevante.
- Correccion o descubrimiento: para una auditoria externa seria, el repo necesitaba declarar mejor que partes son canonicas, historicas o dudosas, y no seguir mandando paquetes delgados.
- Siguiente paso: correr las 10 sesiones, consolidar hallazgos y convertirlos en decisiones canonicas del repo.

## 2026-04-20 - Reempaque final Ed.1 en formato plano 20+1
- Hicimos: rehicimos el paquete externo de Ed.1 en `review-ia/ed1-gpt54pro-10-sesiones-pro-20x1/` con 10 carpetas planas y exactamente `20 contextos + 1 prompt` por sesion.
- Cambio real: el paquete dejo de ser solo "autosuficiente" y paso a ser directamente cargable en GPT-5.4 Pro sin arboles ni sobrecarga de 50+ archivos por carpeta.
- Correccion o descubrimiento: el paquete anterior servia como archivo rico, pero no como formato final de ingestion. El canonicamente utilizable ahora es el `20+1`.
- Siguiente paso: usar estas 10 carpetas para correr las sesiones y consolidar hallazgos duros de Edificio 1.

## 2026-04-20 - Sesion 1 de Ed.1 endurecida por mala lectura de planta
- Hicimos: corregimos `01_GEOMETRIA_CANONICA` en el paquete `20+1` para que parta desde la sospecha explicita de que la planta asimetrica fue mal leida antes.
- Cambio real: la sesion 1 ya no audita la geometria heredada como si fuera neutral; ahora obliga a detectar espejos, repeticiones y simplificaciones falsas por intuicion visual.
- Correccion o descubrimiento: `03_EDIFICIO1_GEOMETRIA_COMPLETA.md` ya no debe leerse como resumen confiable, sino como material sospechoso a refutar o corregir.
- Siguiente paso: correr esa sesion antes de confiar en cualquier cierre de masa, torsion o drift de Ed.1.

## 2026-04-20 - La WS Ed.2 se atasca en capacidad COM real, no en aliases
- Hicimos: corrimos `11_run_analysis_ed2.py`, `12_extract_results_ed2.py` y probes dedicados de `Story Forces` y `drifts` sobre ETABS 21.2.0 en la WS UCN.
- Cambio real: quedo demostrado que el build si entrega reacciones basales reales, pero no expone `Story Forces` ni `drifts` con filas utiles por COM/DB/API.
- Correccion o descubrimiento: ya no corresponde seguir parchando parsers como si fuera un tema de columnas o nombres de tabla; la limitacion es del build/entorno WS.
- Siguiente paso: decidir entre cerrar Ed.2 WS como precheck parcial o armar una ruta de export manual UI/import offline para drifts y tablas faltantes.

## 2026-04-20 - Cierre UI de Ed.2 e import local separado
- Hicimos: guiamos la exportacion manual UI desde ETABS 21.2.0, consolidamos `ed2_ui_summary.md` en la WS y agregamos en el repo un importador + graficador para esos exports.
- Cambio real: Ed.2 ya tiene una ruta practica de cierre y analisis local aunque COM siga bloqueado en la WS.
- Correccion o descubrimiento: la separacion correcta es distinguir el paquete oficial por API del respaldo `ed2_ui_*`.
- Siguiente paso: traer `ui_exports_ed2` al repo local, correr `import_ui_exports_ed2.py` y luego `plot_ui_results_ed2.py`.

## 2026-04-20 - Ed.1 migrado a paquete de cierre final basado en hallazgos v1
- Hicimos: sintetizamos la primera ronda completa de 10 sesiones Ed.1 en `fuentes-ronda1/` y armamos un nuevo paquete activo `review-ia/ed1-gpt54pro-cierre-final-10-sesiones-20x1/`.
- Cambio real: Ed.1 ya no se trabaja con una segunda ronda generica; ahora cada carpeta busca congelar un frente concreto y salir con evidencia, bloqueos y siguiente accion minima.
- Correccion o descubrimiento: el punto 9 no debe entrar como diseno detallado de muros, sino como congelamiento de demandas concurrentes antes del detalle.
- Siguiente paso: correr el paquete final en orden, empezando por `01_GEOMETRIA_V2_CONGELAMIENTO` y llegando a `10_REDTEAM_GO_NO_GO_FINAL` solo cuando existan cierres reales aguas abajo.

## 2026-04-20 - Base normativa del curso fijada en NCh433:2026
- Hicimos: auditamos correos, transcripciones y la copia local de `NCh433-2026 para Curso.pdf`, y lo convertimos en una nota canonica del repo:
  - `docs/estudio/00-ESTADO-NORMATIVO-CURSO-2026.md`
- Cambio real: el repo ya no debe seguir tratando `NCh433 + DS61` como norma vigente del curso.
- Correccion o descubrimiento:
  - hubo una etapa de transicion a inicios de marzo
  - pero desde `2026-03-27` / `2026-04-02` el curso migro de hecho a `NCh433:2026`
  - Ed.1 y Ed.2 mantienen varios parametros numericos principales para `Zona 3 / Sitio C / Categoria II`, asi que el cambio fuerte esta en la base formal y en criterios como sitio, diafragmas, torsion y drift
- Siguiente paso:
  - filtrar las guias largas viejas con la nota canonica nueva
  - seguir rebaselinando Ed.2 y Ed.1 contra `NCh433:2026`

## 2026-04-20 - Ed.1 queda preparado para un rerun corto antes de volver a Ed.2
- Hicimos: diseniamos una corrida corta pre-Ed.2 para `review-ia/ed1-gpt54pro-cierre-final-10-sesiones-20x1/` y la dejamos guardada en `00A_CORRIDA_CORTA_PRE_ED2.md`.
- Cambio real: Ed.1 ya no debe rerunearse entero antes de seguir con Ed.2 Parte 1; ahora el subset obligatorio es `01, 02, 04, 05, 06 y 10`.
- Correccion o descubrimiento:
  - la sesion 1 necesitaba forzar imagen -> puntos/tramos geometricos
  - la sesion 4 seguia desactualizada porque todavia usaba `NCh433 + DS61` como base fuerte
  - la sesion 4 ya fue rebaselinada contra `NCh433:2026` con el archivo local del curso
- Siguiente paso:
  - correr ese rerun corto
  - usar la sesion 10 para decidir si se pasa directo a ETABS/ejecucion o si se abre solo un frente extra de Ed.1

## 2026-04-20 - Auditoria de autosuficiencia por carpeta en la corrida corta de Ed.1
- Hicimos: auditamos las 6 carpetas del rerun corto como unidades reales de upload, verificando conteo `20 contextos + 1 prompt`, independencia entre corridas y suficiencia minima de contexto.
- Cambio real: se confirmo que `01`, `04`, `05`, `06` y `10` ya podian subirse como corridas autosuficientes; `02` tenia un hueco porque cargaba un resumen normativo viejo `NCh433 + DS61`.
- Correccion o descubrimiento:
  - `02_MASA_CARGAS_Y_HUELLA_V2` fue parchada para reemplazar `18_PARAMETROS_SISMICOS_Y_NORMATIVA.md` por `18_ESTADO_NORMATIVO_CURSO_2026.md`
  - se actualizaron su `00_MAPA_DE_CARGA.md` y `20_PROMPT_GPT54PRO.md`
  - no quedaron referencias explicitas del tipo "adjuntar salida de la sesion anterior" en los prompts de las 6 corridas
- Siguiente paso:
  - tratar las 6 carpetas como corridas de upload independientes
  - no volver a meter dependencias entre carpetas salvo que el contexto comun ya vaya copiado dentro de la carpeta misma

## 2026-04-23 - Nueva sesion 1 Ed.1 para geometria canonica UI/API ETABS 21
- Hicimos: creamos `review-ia/ed1-gpt55pro-cierre-final-10-sesiones-20x1/01_GEOMETRIA_CANONICA_UI_API_ETABS21/` con 20 archivos de contexto y 1 prompt maestro.
- Cambio real: la primera corrida externa de Ed.1 queda reorientada a congelar geometria canonica, no solo a repetir la auditoria v2 anterior.
- Correccion o descubrimiento: Image 2.0 debe usarse despues como compilador visual de la geometria cerrada, no como fuente tecnica para inferir dimensiones.
- Siguiente paso: subir los 20 contextos y pegar `21_PROMPT_GPT55PRO_GEOMETRIA_CANONICA_UI_API_ETABS21.md`; no avanzar a masa/cargas si la salida no congela `GEOM_ED1_PUNTOS` y `GEOM_ED1_TRAMOS`.

## 2026-04-30 23:43 - Preparacion APOS-X

Marker: APOS-X-MIGRATION-20260430

### Objetivo
Preparar el proyecto para continuidad APOS-X v1.0.

### Acciones
- Se aseguro estructura `.apos/` completa.
- Se agregaron archivos faltantes sin borrar memoria previa.
- Se actualizo `INDEX.md` como mapa de lectura.

### Archivos revisados
- `.apos/`

### Archivos modificados
- C:\Seba\1° Sem. 2026 - UCN\.apos\evidence\commands
- C:\Seba\1° Sem. 2026 - UCN\.apos\evidence\harness-runs
- C:\Seba\1° Sem. 2026 - UCN\.apos\evidence\test-runs
- C:\Seba\1° Sem. 2026 - UCN\.apos\evidence\research-artifacts
- C:\Seba\1° Sem. 2026 - UCN\.apos\research
- C:\Seba\1° Sem. 2026 - UCN\.apos\transfers
- C:\Seba\1° Sem. 2026 - UCN\.apos\transfers\raw
- C:\Seba\1° Sem. 2026 - UCN\.apos\snapshots
- C:\Seba\1° Sem. 2026 - UCN\.apos\cache
- C:\Seba\1° Sem. 2026 - UCN\.apos\README.md
- C:\Seba\1° Sem. 2026 - UCN\.apos\QUALITY.md
- C:\Seba\1° Sem. 2026 - UCN\.apos\INDEX.md
- C:\Seba\1° Sem. 2026 - UCN\.apos\MODULES.md
- C:\Seba\1° Sem. 2026 - UCN\.apos\RISKS.md
- C:\Seba\1° Sem. 2026 - UCN\.apos\CONTEXT_POLICY.md
- C:\Seba\1° Sem. 2026 - UCN\.apos\RESEARCH_LOG.md
- C:\Seba\1° Sem. 2026 - UCN\.apos\research\INDEX.md
- C:\Seba\1° Sem. 2026 - UCN\.apos\transfers\INDEX.md
- C:\Seba\1° Sem. 2026 - UCN\.apos\snapshots\README.md
- C:\Seba\1° Sem. 2026 - UCN\.apos\evidence\README.md
- C:\Seba\1° Sem. 2026 - UCN\.apos\cache\.gitkeep
- C:\Seba\1° Sem. 2026 - UCN\.apos\transfers\raw\.gitkeep
- C:\Seba\1° Sem. 2026 - UCN\.apos\.gitignore
- C:\Seba\1° Sem. 2026 - UCN\.apos\DECISIONS.md
- C:\Seba\1° Sem. 2026 - UCN\.apos\SOURCES.md

### Comandos importantes
```text
apos_migrate_project.py
```

### Resultados
- Proyecto listo para `/retomar` y `/guardar` con contrato APOS-X.

### Errores / bloqueos
- Ninguno registrado por la migracion.

### Proximos pasos
- Ejecutar `apos_lint.py`.
- Completar estado especifico del proyecto en la proxima sesion real.

### Advertencias metodologicas
- No se modificaron skills globales, hooks ni `.system`.

## 2026-05-02 - Paquete Git para WS UCN Ed.1 UI/API
- Hicimos: se preparo una carpeta de transferencia para continuar Edificio 1 en la workstation UCN con ETABS 21.
- Cambio real: el modelo `.EDB` queda declarado como artefacto local de la WS; el repo solo transporta contexto, guia, normas, apuntes y codigo.
- Archivos nuevos:
  - `transfer/ws-u-ed1-ui-context/README.md`
  - `transfer/ws-u-ed1-ui-context/MANIFEST.md`
  - `transfer/ws-u-ed1-ui-context/WS_U_COMMANDS.md`
  - `transfer/ws-u-ed1-ui-context/PROMPT_BASE_WS_U.md`
  - `transfer/ws-u-ed1-ui-context/files/` con 20 contextos
- Correccion o descubrimiento:
  - la apariencia 3D de vigas invertidas en ETABS puede inducir error
  - la verificacion valida es por `Assign > Frame > Insertion Point...`, tablas/asignaciones y vistas limpias
  - `Cardinal Point = 2 - Bottom Center` y `Do not transform...` marcado quedan como criterio alineado con Lafontaine/profesor
- Siguiente paso:
  - crear/pushear rama `codex/ws-u-ed1-ui-context`
  - en WS ejecutar `git fetch`, `git checkout codex/ws-u-ed1-ui-context`
  - seguir desde `transfer/ws-u-ed1-ui-context/README.md`

## 2026-05-04 - Estado externo WS Ed.1 antes de bloqueo de licencia
- Hicimos: se registro el reporte de otra IA/correo sobre el estado del modelo Edificio 1 en la WS UCN.
- Cambio real: la ruta activa para continuar Parte 1 queda fijada en:
  - `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS\prog\Edif1\ED1_PARTE1_COMPLETA_TRABAJO.EDB`
- Correccion o descubrimiento:
  - el modelo base habria quedado corregido por API COM en ETABS 21 antes del bloqueo de licencia
  - la automatizacion fallo despues, no durante las correcciones base
  - correcciones reportadas: vigas invertidas, offsets, rigid zone, releases, apoyos base y modificadores de losa
- Bloqueo:
  - licencia ETABS 21 no disponible
  - no hay ETABS corriendo
- Siguiente paso:
  - cuando vuelva la licencia, re-verificar correcciones base y continuar con diafragmas, cargas, mass source, modal/espectral, torsion, analisis y exportacion

## 2026-05-08 - Handoff WS2 Ed.1 y regla critica ETABS 21
- Hicimos: se creo una rama/paquete de transferencia para continuar Edificio 1 en una segunda workstation UCN.
- Cambio real:
  - WS2 usa raiz `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2`
  - se registro como regla critica que no se puede usar mas de una instancia de ETABS 21
  - se exige auditoria inicial del `.EDB` antes de modificar
- Archivos nuevos:
  - `ETABS21_REGLA_LICENCIA.md`
  - `transfer/ws2-ed1-etabs21-context/README.md`
  - `transfer/ws2-ed1-etabs21-context/LICENCIA_ETABS21_REGLA_CRITICA.md`
  - `transfer/ws2-ed1-etabs21-context/HANDOFF_WS2_ED1.md`
  - `transfer/ws2-ed1-etabs21-context/PROMPT_PARA_CODEX_WS2.md`
  - `transfer/ws2-ed1-etabs21-context/CHECKLIST_AUDITORIA_MODELO_ED1.md`
  - `transfer/ws2-ed1-etabs21-context/WS2_COMMANDS.md`
  - `transfer/ws2-ed1-etabs21-context/HECRAS2_ARCHIVOS_ESPERADOS.md`
- Bloqueo/advertencia:
  - el usuario reporta avance leve en WS2 por UI posterior a WS1, pero aun no hay reporte trazado
- Siguiente paso:
  - bajar rama `codex/ws2-ed1-etabs21-context` en WS2
  - verificar una sola instancia de ETABS
  - auditar modelo y devolver reporte

## 2026-05-08 - APOS-X dual local/WS2
- Hicimos: se agrego un snapshot del APOS-X local al paquete WS2 y un protocolo de sincronizacion.
- Cambio real:
  - WS2 tendra su propio APOS operativo basado en `APOS_X_BASE/.apos`
  - este APOS local sigue como coordinador/canon de decisiones
  - los estados se conectan por reportes/deltas, no por memoria implicita
- Archivos nuevos:
  - `transfer/ws2-ed1-etabs21-context/APOS_X_SYNC_PROTOCOL.md`
  - `transfer/ws2-ed1-etabs21-context/APOS_X_BASE/.apos/`
  - `transfer/ws2-ed1-etabs21-context/APOS_X_BASE/README.md`
  - `transfer/ws2-ed1-etabs21-context/reports/README.md`
- Siguiente paso:
  - al recibir reporte WS2, absorberlo con append-only en `.apos/STATUS.md`, `.apos/JOURNAL.md`, `.apos/DECISIONS.md`, `.apos/RISKS.md` y `.apos/OPEN_QUESTIONS.md` segun corresponda.
