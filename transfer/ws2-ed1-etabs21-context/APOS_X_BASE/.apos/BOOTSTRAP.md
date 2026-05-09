# BOOTSTRAP - ADSE 1S-2026
# Ultima actualizacion: 2026-04-20

## Identidad
Ramo Analisis y Diseno Sismico de Edificios, UCN, 1S-2026.
Taller: Ed.1 muros + Ed.2 marcos.

## Estado operativo real
- Ed.1: ya existen 3 capas de paquete externo y la activa ya no es la original:
  - historica/sobrecargada:
    - `review-ia/ed1-gpt54pro-10-sesiones/`
  - primera ronda en formato plano `20+1`:
    - `review-ia/ed1-gpt54pro-10-sesiones-pro-20x1/`
  - paquete activo de cierre final:
    - `review-ia/ed1-gpt54pro-cierre-final-10-sesiones-20x1/`
  - el paquete activo ya no esta orientado a auditoria general:
    - usa hallazgos v1 curados
    - reorganiza las 10 carpetas como frentes de cierre
    - mantiene exactamente `20 contextos + 1 prompt` por carpeta
    - incluye generador reproducible y `fuentes-ronda1/`
- Ed.2 Parte 1: rebaselinado al metodo estatico oficial.
- Ed.2 Parte 1: sigue siendo estatico en su nucleo, pero la primera entrega ahora exige analisis modal de ambos edificios por correo de Music del 2026-04-15.
- Fuente de verdad: documentos originales del curso en `docs/`.
- Guias, scripts y memorias antiguas: referencias derivadas.
- Paquete activo Ed.2: `autonomo/scripts/ed2/`.
- Pipeline API Ed.2 endurecido para corrida directa en ETABS 21 WS UCN:
  - `autonomo/scripts/ed2/config_ed2.py`
  - `autonomo/scripts/ed2/run_pipeline_ed2.py`
  - `autonomo/scripts/ed2/06_assignments_ed2.py`
  - `autonomo/scripts/ed2/diag.py`
- Repo remoto operativo para la WS:
  - `https://github.com/kcortes765/taha.git`
  - `origin/main` ya contiene el paquete Ed.2 minimo publicable
- Estado vivo WS:
  - `phase 1` PASS
  - `step 08` PASS
  - `step 09` PASS en modo precheck con `CM` geometrico habilitado
  - `step 10` PASS
  - `step 11` PASS cuando se ejecuta directo (`11_run_analysis_ed2.py`)
  - bloqueo vivo actual: `step 12` en ETABS 21.2.0 WS porque COM/DB no expone `Story Forces`, `Joint/Story Drifts` ni tablas `Diaphragm Max Over Avg Drifts` con filas utiles
  - evidencia viva:
    - `autonomo/scripts/ed2/results/ed2_story_forces_probe.json`
    - `autonomo/scripts/ed2/results/ed2_story_drifts_probe.json`
  - conclusion operativa vigente:
    - la WS sirve para precheck parcial hasta base reactions
    - el cierre oficial via API queda bloqueado por capacidad del build, no por parser
    - el cierre practico por UI ya quedo validado en la WS:
      - exports manuales desde ETABS
      - resumen `C:\Users\Civil\Documents\taha\ui_exports_ed2\ed2_ui_summary.md`
      - import local soportado por:
        - `autonomo/scripts/ed2/import_ui_exports_ed2.py`
        - `autonomo/scripts/ed2/plot_ui_results_ed2.py`
- Bundle portable WS / Pro listo:
  - `autonomo/scripts/ed2/transfer/ED2_WS_BUNDLE_FINAL`
  - `autonomo/scripts/ed2/transfer/ED2_WS_BUNDLE_FINAL.zip`
- Paquete nuevo para auditar la guia UI de Ed.2 en ETABS 21:
  - `C:\Seba\seba_os\study\adse_ed2\GUIA_UI_ED2_ETABS21_PAQUETE_PARA_SUBIR`
- Evidencia visual Ed.1 vs Ed.2:
  - `evidencia/enunciado-ed1-vs-ed2/`

## Donde continuar
1. `review-ia/ed1-gpt54pro-cierre-final-10-sesiones-20x1/00_INDICE_20x1.md`
2. `review-ia/ed1-gpt54pro-cierre-final-10-sesiones-20x1/01_GEOMETRIA_V2_CONGELAMIENTO/00_MAPA_DE_CARGA.md`
3. `review-ia/ed1-gpt54pro-cierre-final-10-sesiones-20x1/09_DEMANDAS_MUROS_V2/00_MAPA_DE_CARGA.md`
4. `review-ia/ed1-gpt54pro-cierre-final-10-sesiones-20x1/10_REDTEAM_GO_NO_GO_FINAL/20_PROMPT_GPT54PRO.md`
5. `review-ia/ed1-gpt54pro-cierre-final-10-sesiones-20x1/fuentes-ronda1/00_RESUMEN_RONDA1.md`
6. `docs/Enunciado Taller.pdf`
7. `evidencia/enunciado-ed1-vs-ed2/00_COMPARACION_CLAVE.png`
8. `docs/estudio/ED2_PARTE1_CANON.md`
9. `autonomo/research/ED2_PARTE1_AUDITORIA.md`
10. `docs/estudio/GUIA-EDIFICIO2-MARCOS-ETABS-v21.md`
11. `.apos/NARRATIVE.md`
12. `.apos/JOURNAL.md`

## Memoria historica
- `DECISIONS.md`: ledger de pivots tecnicos y criterios vigentes.
- `JOURNAL.md`: hitos breves de ejecucion.
- `NARRATIVE.md`: historia reconciliada del proyecto y por que el enfoque actual tiene sentido.

## Regla de cierre
Ed.2 Parte 1 solo se considera resuelto cuando existan:
- `.edb` real
- CSV/JSON reales en `autonomo/scripts/ed2/results/`
- `verify_ed2.py` en PASS
- informe y plots regenerados desde esa evidencia

## Warning operativo
- No mezclar los 6 casos de Ed.1 con Ed.2.
- No vender "sin modal" para Ed.2 despues del correo del 2026-04-15: el modal ahora es parte explicita de la primera entrega.
- El cierre tecnico Ed.2 en API ahora depende de ETABS 21 real; no volver a suavizar 06_assignments con fallbacks manuales.
- Para la WS UCN usar `ED2_RUNTIME_ROOT=C:\Users\Civil\Documents\taha` y no escribir artefactos en la carpeta del codigo.
- Sincronizacion vigente:
  - codigo ida local -> WS por git
  - evidencia vuelta WS -> local por `package_transfer_ed2.py` / `ingest_transfer_ed2.py`
  - alternativa UI -> local:
    - traer carpeta o zip `ui_exports_ed2`
    - correr `import_ui_exports_ed2.py`
    - graficar con `plot_ui_results_ed2.py`
- No asumir tabla directa de `Centers Of Mass And Rigidity` en el build del laboratorio; el flujo ahora puede derivar `CM` real desde masas nodales.
- No asumir que seguir parchando aliases de tablas resolvera `Story Forces` o `drifts` en la WS: las sondas ya muestran respuestas vacias desde DB y `Results.StoryDrifts()`.
