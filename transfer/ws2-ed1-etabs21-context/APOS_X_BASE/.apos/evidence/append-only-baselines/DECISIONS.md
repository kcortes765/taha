# DECISIONS - ADSE 1S-2026

## DEC-001 - Automatizar modelado ETABS via Python COM API
- Fecha: ~2026-02 (retroactiva)
- Decisor: Humano
- Contexto: El taller requiere modelar 2 edificios en ETABS. Hacerlo manual toma horas y es propenso a errores. El alumno tiene experiencia en Python.
- Decision: Pipeline de 13 scripts Python que controlan ETABS 19 via comtypes COM API.
- Alternativas descartadas: modelado manual en ETABS, importar desde CAD.
- Estado: vigente

## DEC-002 - Stack vanilla para App C1
- Fecha: ~2026-02 (retroactiva)
- Decisor: Humano
- Contexto: Se necesitaba una app de estudio para el Control 1 sin setup complejo.
- Decision: HTML + CSS + JS vanilla, Three.js r128, Chart.js 4.4.1, MathJax 3 por CDN.
- Alternativas descartadas: React, Streamlit.
- Estado: vigente

## DEC-003 - Separar pipeline COM en 2 sesiones
- Fecha: 2026-03-05
- Decisor: Claude + Humano
- Contexto: La sesion COM de ETABS 19 moria despues de geometria pesada.
- Decision: `run_all.py` soporta `--fase 1/2/all`; ETABS se reinicia entre fases.
- Estado: vigente

## DEC-004 - Losas modeladas como huella real
- Fecha: 2026-03-10
- Decisor: Claude + Humano
- Contexto: Las losas estaban cubriendo la envolvente completa y distorsionaban masa y CM.
- Decision: modelar paneles que reproduzcan la huella real, no la envolvente.
- Estado: vigente

## DEC-005 - Eje F con muro horizontal de 7.7 m centrado en eje 10
- Fecha: 2026-03-20
- Decisor: 3 IAs + Humano
- Contexto: Habia controversia sobre la configuracion del eje F en Ed.1.
- Decision: fijar un muro central de 7.7 m, no dos stubs laterales.
- Estado: vigente

## DEC-006 - Muros dir Y divididos en bloque sur y norte
- Fecha: 2026-03-20
- Decisor: IA + validacion contra elevaciones
- Contexto: Los muros no cruzan el pasillo C-D.
- Decision: separar MUROS_DIR_Y por bloque, evitando cruzar el pasillo.
- Estado: vigente

## DEC-007 - Geometria requiere auditoria visual antes de fase 2
- Fecha: 2026-03-20
- Decisor: Humano
- Contexto: Varias iteraciones de `config.py` no habian producido una geometria visualmente correcta.
- Decision: no avanzar a fase 2 hasta confirmar geometria visualmente.
- Estado: vigente

## DEC-008 - Cambiar de pipeline COM a modelacion manual en ETABS v19
- Fecha: 2026-03-20
- Decisor: Humano
- Contexto: El pipeline COM tuvo varias iteraciones de geometria sin resultado visual correcto.
- Decision: modelar Ed.1 manualmente en ETABS v19 con guia paso a paso exhaustiva. El pipeline COM se preserva como referencia.
- Estado: vigente

## DEC-009 - Enfoque dual: guia UI + scripts API Python
- Fecha: 2026-03-20
- Decisor: Humano
- Contexto: La guia manual seguia siendo el enfoque principal, pero se queria tambien scripts API como backup y para automatizacion futura.
- Decision: producir ambos entregables.
- Estado: vigente

## DEC-010 - La matriz de 6 casos pertenece solo a Edificio 1
- Fecha: 2026-04-16
- Contexto: Habia confusion entre usuario, compa y otras IAs sobre si la tabla de 6 casos del enunciado tambien aplicaba a Edificio 2.
- Decision: fijar como criterio vigente que la tabla de 6 casos corresponde a Edificio 1. Edificio 2 no repite esa matriz en el enunciado.
- Estado: vigente
- Evidencia: `docs/Enunciado Taller.pdf`; `evidencia/enunciado-ed1-vs-ed2/`

## DEC-011 - El correo del 2026-04-15 amplia la primera entrega con modal para ambos edificios
- Fecha: 2026-04-16
- Contexto: La lectura corta de Ed.2 se estaba simplificando como "estatico y sin modal", pero Music envio un aviso posterior precisando la primera entrega.
- Decision: mantener que Ed.2 Parte 1 sigue con nucleo estatico, pero incorporar como exigencia vigente de la primera entrega el analisis modal de ambos edificios para masas equivalentes y `Tx`, `Ty`, `Tz`.
- Estado: vigente
- Evidencia: correo de Music del 2026-04-15 citado en sesion; paquete `GUIA_UI_ED2_ETABS21_PAQUETE_PARA_SUBIR`

## DEC-012 - El pipeline API Ed.2 se cierra primero para ETABS 21 WS UCN, no para v19/v21 generico
- Fecha: 2026-04-19
- Contexto: El flujo Ed.2 ya estaba conceptualmente bien, pero todavia arrastraba ambiguedades operacionales de compatibilidad antigua y una llamada COM incorrecta en `SetInsertionPoint`.
- Decision: endurecer el pipeline al caso real de uso: ETABS 21 en la workstation UCN, con arranque por consola, apertura explicita de `.edb` y falla temprana cuando la etapa 06 no completa sus asignaciones.
- Estado: vigente
- Evidencia: `autonomo/scripts/ed2/config_ed2.py`, `autonomo/scripts/ed2/run_pipeline_ed2.py`, `autonomo/scripts/ed2/06_assignments_ed2.py`, `autonomo/scripts/ed2/diag.py`

## DEC-013 - El intercambio WS <-> local se estandariza via runtime root y bundles cortos
- Fecha: 2026-04-19
- Contexto: La ejecucion real ocurrira en `C:\Users\Civil\Documents\taha` en la WS UCN y los resultados deben volver a este repo o, si hace falta, a una revision externa.
- Decision: usar `ED2_RUNTIME_ROOT` para redirigir artefactos de corrida y agregar dos scripts dedicados: `prepare_ws_bundle_ed2.py` para enviar un bundle de 20 archivos y `package_transfer_ed2.py` para traer de vuelta un zip con evidencia reproducible.
- Estado: vigente
- Evidencia: `autonomo/scripts/ed2/config_ed2.py`, `autonomo/scripts/ed2/package_transfer_ed2.py`, `autonomo/scripts/ed2/prepare_ws_bundle_ed2.py`, `autonomo/scripts/ed2/transfer/ED2_WS_BUNDLE_FINAL`

## DEC-014 - La sincronizacion principal WS <-> local pasa a git para codigo y transfer para resultados
- Fecha: 2026-04-19
- Contexto: El usuario necesita correr Ed.2 tanto en este PC como en la workstation UCN sin duplicar bundles manuales en cada iteracion. El repo remoto `kcortes765/taha` existia pero estaba vacio.
- Decision: publicar un subset minimo y limpio del paquete Ed.2 en `origin/main` de `https://github.com/kcortes765/taha.git` y usarlo como canal principal de codigo hacia la WS. Mantener `ED2_WS_BUNDLE_FINAL.zip` solo como fallback o artefacto para revision externa.
- Estado: vigente
- Evidencia: commit `164eac1 Add Edificio 2 ETABS 21 API package`; `git push -u origin HEAD:main`; `autonomo/scripts/ed2/package_transfer_ed2.py`; `autonomo/scripts/ed2/ingest_transfer_ed2.py`

## DEC-015 - La validacion WS se hace por etapas y no se fuerza fallback analitico para cerrar Ed.2
- Fecha: 2026-04-19
- Contexto: La corrida viva en la WS UCN ya confirmo que fase 1 cierra en ETABS 21, pero `step 08` no encuentra la tabla real de masa por historia del build del laboratorio.
- Decision: mantener el criterio estricto de no cerrar Ed.2 con pesos analiticos. En su lugar, endurecer la deteccion de tablas (`GetAvailableTables`, nombres fuzzy y `group=''`/`All`) y generar `ed2_available_tables.json` cuando el build no expone el nombre esperado.
- Estado: vigente
- Evidencia: `9660ebc Harden ETABS 21 story weight table detection`; log WS 2026-04-19 con `phase 1` PASS y fallo acotado a `08_seismic_ed2.py`

## DEC-016 - Los reruns de `phase 2` deben asumir modelo bloqueado y tolerar fallback de Mass Source
- Fecha: 2026-04-19
- Contexto: En la WS UCN, despues de correr un modal auxiliar, ETABS deja el modelo bloqueado. Al relanzar `phase 2` sobre la misma sesion, `PropMaterial.SetMassSource_1` devolvio `ret=1` aunque la tabla `Mass Summary by Story` si existia en el build 21.2.0.
- Decision: endurecer `08_seismic_ed2.py` para desbloquear explicitamente el modelo antes de reconfigurar la fuente de masa y usar `PropMaterial.SetMassSource(...)` como fallback si `_1` falla.
- Estado: vigente
- Evidencia: commit `fab743d Harden ETABS 21 mass source reruns`; log WS 2026-04-19 con `ret=1` en `PropMaterial.SetMassSource_1`

## DEC-017 - La lectura de pesos por historia debe normalizar campos y nombres de piso del build ETABS 21
- Fecha: 2026-04-19
- Contexto: En la WS UCN se confirmo que la tabla `Mass Summary by Story` existe, pero el parser seguia fallando por depender de strings demasiado literales para columnas y nombres de historia.
- Decision: ampliar `extract_story_weights_from_db()` para normalizar tokens de campo (`MassX`, `Mass X`, `UX Mass`, etc.) y tambien los nombres de historia antes de validar contra `STORY_NAMES`.
- Estado: vigente
- Evidencia: commit `2f51987 Broaden ETABS 21 story weight parsing`

## DEC-018 - La siguiente iteracion de tabla de pesos se hace con payload crudo de CSI, no con mas heuristicas ciegas
- Fecha: 2026-04-19
- Contexto: Incluso tras ampliar la normalizacion de campos, `step 08` siguio sin poder convertir `Mass Summary by Story` en 5 pesos validos de historia en la WS UCN.
- Decision: agregar una sonda dedicada (`diag_story_weights_ed2.py`) para capturar el resultado bruto de `GetTableForDisplayArray` sobre las tablas candidatas y parchear el parser solo con evidencia del build real.
- Estado: vigente
- Evidencia: commit `775b8e8 Add ETABS story weight probe`

## DEC-019 - El build ETABS 21.2.0 del laboratorio expone masas por historia como UX/UY/UZ
- Fecha: 2026-04-19
- Contexto: La sonda cruda del laboratorio mostro que `Mass Summary by Story` devuelve campos `Story, UX, UY, UZ`, no `MassX`, `UX Mass` ni variantes mas largas.
- Decision: aceptar explicitamente `UX`, `UY` y `UZ` como campos validos de masa translacional en `extract_story_weights_from_db()`.
- Estado: vigente
- Evidencia: `ed2_story_weight_probe.json` pegado desde la WS; commit `aebb01f Accept UX UY UZ story mass fields`

## DEC-020 - Si el build no expone `CM/CR`, el pipeline usa `CM` real desde masas nodales y degrada `CR` de forma explicita
- Fecha: 2026-04-19
- Contexto: Despues de cerrar `step 08`, la WS UCN mostro que el build ETABS 21.2.0 no expone una tabla directa de `Centers Of Mass And Rigidity`, bloqueando `step 09` aunque el modelo ya tenia pesos por historia reales.
- Decision: derivar `CM` por piso desde `Assembled Joint Masses` + coordenadas de joints y usar ese `CM` como referencia para el estatico y para drift. Si `CR` sigue sin existir en ETABS, exportar un placeholder trazado y bajar esa condicion a warning en `verify_ed2.py`, en vez de tratarla como error operacional de corrida.
- Estado: vigente
- Evidencia: log WS con fallo en `09_torsion_ed2.py`; commit `ac4f5f1 Derive story CM from ETABS joint masses`

## DEC-021 - Edificio 1 se audita externamente con 10 paquetes autosuficientes de GPT-5.4 Pro
- Fecha: 2026-04-20
- Contexto: El usuario necesita una revision final dura de Edificio 1 y no acepta carpetas delgadas ni prompts aislados. Hace falta que cada sesion externa tenga suficiente contexto real para detectar contradicciones, no solo para resumirlas.
- Decision: crear `review-ia/ed1-gpt54pro-10-sesiones/` con 10 carpetas separadas, una por sesion, cada una poblada con:
  - dossier comun y estado actual
  - fuentes del curso
  - memoria `.apos/`
  - frente operativo `taller-etabs/`
  - frente historico `autonomo/scripts/`
  - research, evidencia y contexto sintetico
- Estado: vigente
- Evidencia:
  - `review-ia/ed1-gpt54pro-10-sesiones/00_INDICE_PAQUETES.md`
  - `review-ia/ed1-gpt54pro-10-sesiones/00_DOSSIER_ED1_2026-04-20.md`
  - `review-ia/ed1-gpt54pro-10-sesiones/01_GEOMETRIA_CANONICA/`
  - `review-ia/ed1-gpt54pro-10-sesiones/10_REDTEAM_COMISION_FINAL/`

## DEC-022 - La WS ETABS 21.2.0 se trata como precheck parcial mientras COM no exponga Story Forces ni drifts
- Fecha: 2026-04-20
- Contexto: Tras cerrar `step 11` en la WS UCN, las sondas mostraron que `Story Forces`, `Joint Drifts`, `Story Drifts`, `Diaphragm Max Over Avg Drifts` y `Results.StoryDrifts()` no devuelven filas utiles desde COM/DB en el build ETABS 21.2.0 del laboratorio, aunque si existen reacciones basales reales.
- Decision: dejar de tratar este bloqueo como un problema de naming/parser. Mantener solo fallbacks de precheck explicitamente rotulados (`CM` geometrico, `Story Forces` teorico) y no inventar fallback para drifts. El cierre oficial via API queda bloqueado hasta tener:
  - export manual UI/import offline
  - o un build/entorno que si exponga drifts y fuerzas por historia via COM
- Estado: vigente
- Evidencia:
  - `autonomo/scripts/ed2/results/ed2_story_forces_probe.json`
  - `autonomo/scripts/ed2/results/ed2_story_drifts_probe.json`
  - `autonomo/scripts/ed2/diag_story_forces_ed2.py`
  - `autonomo/scripts/ed2/diag_story_drifts_ed2.py`
  - commits `6affb88`, `504035f`

## DEC-023 - Ed.2 admite una capa local `ed2_ui_*` para importar resultados exportados manualmente desde la UI
- Fecha: 2026-04-20
- Contexto: La WS ETABS 21.2.0 ya demostro que la UI si expone `Story Forces` y `drifts`, aunque COM/DB no entregue esas tablas con filas utiles.
- Decision: agregar una via separada de import local y graficacion:
  - `autonomo/scripts/ed2/import_ui_exports_ed2.py`
  - `autonomo/scripts/ed2/plot_ui_results_ed2.py`
  Los resultados se guardan como `ed2_ui_*` y no reemplazan el paquete oficial por COM.
- Estado: vigente
- Evidencia:
  - `C:\Users\Civil\Documents\taha\ui_exports_ed2\ed2_ui_summary.md`
  - `autonomo/scripts/ed2/results/README.md`

## DEC-024 - El paquete canonico de revision externa Ed.1 pasa a formato plano `20+1`
- Fecha: 2026-04-20
- Contexto: El primer paquete externo de Ed.1 (`review-ia/ed1-gpt54pro-10-sesiones/`) quedo rico en contexto, pero malo para ingestion real en GPT-5.4 Pro porque cada carpeta tenia 50+ archivos y un arbol anidado innecesario.
- Decision: congelar como paquete canonico de upload:
  - `review-ia/ed1-gpt54pro-10-sesiones-pro-20x1/`
  con estas reglas:
  - 10 carpetas tematicas
  - exactamente `20 archivos de contexto + 1 prompt` por carpeta
  - estructura plana
  - indice raiz en `00_INDICE_20x1.md`
  - generacion reproducible via `GENERAR_20x1.ps1`
  El paquete viejo se conserva solo como referencia historica/sobrecargada.
- Estado: vigente
- Evidencia:
  - `review-ia/ed1-gpt54pro-10-sesiones-pro-20x1/00_INDICE_20x1.md`
  - `review-ia/ed1-gpt54pro-10-sesiones-pro-20x1/GENERAR_20x1.ps1`
  - `review-ia/ed1-gpt54pro-10-sesiones-pro-20x1/01_GEOMETRIA_CANONICA/`
  - `review-ia/ed1-gpt54pro-10-sesiones-pro-20x1/10_REDTEAM_COMISION_FINAL/`
  - `autonomo/scripts/ed2/import_ui_exports_ed2.py`
  - `autonomo/scripts/ed2/plot_ui_results_ed2.py`

## DEC-025 - Ed.1 migra a un paquete activo de cierre final construido sobre hallazgos v1
- Fecha: 2026-04-20
- Contexto: La primera ronda `20+1` de Ed.1 ya produjo hallazgos suficientes para dejar de repetir auditorias panoramicas. Faltaba transformar esas respuestas en un segundo set de carpetas orientadas a cierre, congelamiento y go/no-go.
- Decision: adoptar como paquete activo para Ed.1:
  - `review-ia/ed1-gpt54pro-cierre-final-10-sesiones-20x1/`
  con estas reglas:
  - usa `fuentes-ronda1/` como capa comun de hallazgos v1 curados
  - mantiene exactamente `20 archivos de contexto + 1 prompt` por carpeta
  - reordena las 10 sesiones como frentes de cierre (`V2`, hardening, trazabilidad, demandas, go/no-go)
  - deja el paquete `review-ia/ed1-gpt54pro-10-sesiones-pro-20x1/` como baseline de primera ronda, no como paquete activo
- Estado: vigente
- Supersede: DEC-024 para la ruta activa de upload/cierre de Ed.1
- Evidencia:
  - `review-ia/ed1-gpt54pro-cierre-final-10-sesiones-20x1/00_INDICE_20x1.md`
  - `review-ia/ed1-gpt54pro-cierre-final-10-sesiones-20x1/GENERAR_20x1.ps1`
  - `review-ia/ed1-gpt54pro-cierre-final-10-sesiones-20x1/fuentes-ronda1/00_RESUMEN_RONDA1.md`
  - `review-ia/ed1-gpt54pro-cierre-final-10-sesiones-20x1/09_DEMANDAS_MUROS_V2/`
  - `review-ia/ed1-gpt54pro-cierre-final-10-sesiones-20x1/10_REDTEAM_GO_NO_GO_FINAL/`

## DEC-026 - La base normativa del curso migra a NCh433:2026 y las capas DS61 pasan a historicas
- Fecha: 2026-04-20
- Contexto: El repo seguia mezclando documentos derivados que declaraban `NCh433:1996 Mod.2009 + DS61` como norma vigente del curso, pero la evidencia cruda del propio curso muestra una migracion efectiva a `NCh433:2026` entre el 2026-03-27 y el 2026-04-02.
- Decision:
  - fijar `NCh433:2026` como base normativa vigente del curso
  - tratar `NCh433 + DS61` como capa historica o parcialmente desactualizada para curso/taller
  - mantener los valores numericos que coincidan con 2026 solo cuando se citen ahora contra `NCh433:2026`
  - aplicar esta regla tanto a Ed.1 como a Ed.2
- Estado: vigente
- Evidencia:
  - `materiales_fuente/sismo/correo/emails.json` (avisos 2026-03-27, 2026-03-29 y 2026-04-02)
  - `app transcripciones/Academico/2026-2/Sismo/02_processed/transcripts/transcript_3d9ff0eeb61c.clean.txt`
  - `materiales_fuente/sismo/Normas Curso/Normas a Utilizar en Curso/NCh433-2026 para Curso.pdf`
  - `docs/estudio/00-ESTADO-NORMATIVO-CURSO-2026.md`

## DEC-027 - La corrida inmediata de Ed.1 antes de volver a Ed.2 se reduce a un rerun corto y geometria con imagen obligatoria
- Fecha: 2026-04-20
- Contexto: El paquete activo de cierre de Ed.1 seguia util, pero habia quedado con dos problemas practicos para la siguiente vuelta: la sesion 1 no forzaba explictamente imagen -> puntos/tramos y la sesion 4 seguia anclada a `NCh433 + DS61` como capa normativa fuerte.
- Decision:
  - fijar una corrida corta pre-Ed.2 para Ed.1 en `review-ia/ed1-gpt54pro-cierre-final-10-sesiones-20x1/00A_CORRIDA_CORTA_PRE_ED2.md`
  - correr obligatoriamente solo `01, 02, 04, 05, 06 y 10`
  - tratar `03, 07 y 08` como sesiones condicionales
  - prohibir `09` mientras el objetivo inmediato siga siendo Parte 1
  - endurecer la sesion 1 para exigir `GEOM_ED1_V2_PUNTOS` y `GEOM_ED1_V2_TRAMOS` a partir de la imagen del enunciado
  - rebaselinar la sesion 4 contra `NCh433:2026` con el archivo local del curso y la nota canonica del repo
- Estado: vigente
- Evidencia:
  - `review-ia/ed1-gpt54pro-cierre-final-10-sesiones-20x1/00A_CORRIDA_CORTA_PRE_ED2.md`
  - `review-ia/ed1-gpt54pro-cierre-final-10-sesiones-20x1/01_GEOMETRIA_V2_CONGELAMIENTO/20_PROMPT_GPT54PRO.md`
  - `review-ia/ed1-gpt54pro-cierre-final-10-sesiones-20x1/04_KERNEL_SISMICO_ESPECTRO_RSTAR_V2/00_MAPA_DE_CARGA.md`
  - `review-ia/ed1-gpt54pro-cierre-final-10-sesiones-20x1/04_KERNEL_SISMICO_ESPECTRO_RSTAR_V2/20_PROMPT_GPT54PRO.md`
  - `review-ia/ed1-gpt54pro-cierre-final-10-sesiones-20x1/04_KERNEL_SISMICO_ESPECTRO_RSTAR_V2/17_ESTADO_NORMATIVO_CURSO_2026.md`
  - `review-ia/ed1-gpt54pro-cierre-final-10-sesiones-20x1/04_KERNEL_SISMICO_ESPECTRO_RSTAR_V2/18_NCH433_2026_PARA_CURSO.pdf`

## DEC-028 - En los paquetes GPT-5.4 Pro cada carpeta sigue siendo una corrida autosuficiente
- Fecha: 2026-04-20
- Contexto: En la definicion inicial de la corrida corta pre-Ed.2 se deslizaron dependencias entre sesiones del tipo "adjuntar salida de la sesion anterior", lo que rompe la regla real de upload por carpeta.
- Decision:
  - reafirmar que cada carpeta de `review-ia/...20x1/` representa una corrida autosuficiente e independiente
  - permitir contexto comun solo si ya viene copiado dentro de la misma carpeta
  - prohibir dependencias duras de una corrida sobre outputs generados por otra para poder arrancar
- Estado: vigente
- Evidencia:
  - `review-ia/ed1-gpt54pro-cierre-final-10-sesiones-20x1/00_INDICE_20x1.md`
  - `review-ia/ed1-gpt54pro-cierre-final-10-sesiones-20x1/00A_CORRIDA_CORTA_PRE_ED2.md`
