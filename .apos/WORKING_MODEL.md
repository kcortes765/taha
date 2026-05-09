# WORKING MODEL - ADSE 1S-2026

## Thread: Edificio 1 + Edificio 2 WS2 ETABS 21 Parte 1 (ACTIVO)
- Estado actual: continuidad de Parte 1 de Edificio 1 y Edificio 2 pasa a una segunda workstation UCN (`WS2`) porque la WS anterior perdio/bloqueo licencia de ETABS 21.
- Regla critica: no abrir ni usar mas de una instancia de ETABS 21. Verificar `Get-Process ETABS -ErrorAction SilentlyContinue` antes de abrir ETABS o correr scripts COM/API.
- Ruta WS2 reportada:
  - `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2`
- Ruta corregida para clonar repo/contexto:
  - `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\codex_ws2_context`
- No usar para WS2:
  - `C:\Users\Civil\Documents\taha`
- Paquete de contexto activo:
  - `transfer/ws2-ed1-etabs21-context/`
- Enunciado prioritario WS2:
  - `transfer/ws2-ed1-etabs21-context/files/01_Enunciado_Taller_actualizado_2026-05-04.pdf`
  - cambio detectado: agrega `En ambos considerar no aglomeracion de personas.`
- Apuntes prioritarios WS2:
  - `transfer/ws2-ed1-etabs21-context/files/00_Apuntes_del_Curso_2026-05-08_actualizado.pdf`
  - 344 paginas, reemplaza al PDF viejo de 321 paginas como fuente de curso
- Fuentes Ed.2 agregadas:
  - `transfer/ws2-ed1-etabs21-context/files/21_GUIA_ED2_ETABS_v21.md`
  - `transfer/ws2-ed1-etabs21-context/files/22_ED2_PARTE1_CANON.md`
- Primer objetivo:
  - auditar los `.EDB` activos de Ed.1 y Ed.2 en WS2 y devolver reporte de estado antes de modificar
  - no continuar cargas/masa/analisis hasta saber exactamente que avance UI se hizo en WS2
- Evidencia:
  - `ETABS21_REGLA_LICENCIA.md`
  - `transfer/ws2-ed1-etabs21-context/README.md`
  - `transfer/ws2-ed1-etabs21-context/HANDOFF_WS2_ED1.md`
  - `transfer/ws2-ed1-etabs21-context/CHECKLIST_AUDITORIA_MODELO_ED1.md`
  - `transfer/ws2-ed1-etabs21-context/APUNTES_CAMBIOS_2026-05-08.md`
  - `transfer/ws2-ed1-etabs21-context/PARTE1_ED1_ED2_PROGRAMATICO_2026-05-08.md`
- Ultima actualizacion: 2026-05-08

## Thread: Paquetes GPT-5.4 Pro Edificio 1 (ACTIVO)
- Estado actual: existe un paquete real de 10 carpetas autosuficientes para auditar Edificio 1 con sesiones largas y separadas de GPT-5.4 Pro.
- Ruta:
  - `review-ia/ed1-gpt54pro-10-sesiones/`
- Delta reciente:
  - se crearon dossiers comunes nuevos para estado actual, cambios de correos y canon vs historico vs dudoso
  - se poblaron las 10 carpetas con hardlinks a fuentes reales del curso y del proyecto
  - cada carpeta quedo con codigo del frente operativo `taller-etabs`, codigo historico `autonomo/scripts`, memorias `.apos/` y material del profesor
- Pendiente:
  - correr las 10 sesiones
  - consolidar contradicciones y decisiones nuevas
  - usar esos hallazgos para congelar mejor Ed.1
- Ultima actualizacion: 2026-04-20

## Thread: Edificio 2 Parte 1 - alcance oficial y flujo tecnico (ACTIVO)
- Estado actual: Ed.2 esta fijado como metodo estatico en su nucleo para Parte 1, con modal auxiliar ahora exigido para primera entrega.
- Delta reciente: se resolvio la confusion con la tabla de 6 casos; no corresponde a Ed.2.
- Evidencia:
  - `docs/Enunciado Taller.pdf`
  - correos de Music del 2026-04-13 y 2026-04-15
  - `evidencia/enunciado-ed1-vs-ed2/`
- Pendiente: no la comprension conceptual, sino la validacion viva ETABS 21.
- Ultima actualizacion: 2026-04-16

## Thread: Guia UI Ed.2 ETABS 21 (ACTIVO)
- Estado actual: existe un paquete autocontenido para auditar la guia manual de Ed.2 con otra IA.
- Delta reciente: se empaqueto contexto, fuentes, clases Music y scripts/derivados relevantes en un bundle de 19 archivos.
- Evidencia:
  - `C:\Seba\seba_os\study\adse_ed2\GUIA_UI_ED2_ETABS21_PAQUETE_PARA_SUBIR`
  - `C:\Seba\seba_os\study\adse_ed2\GUIA_UI_ED2_ETABS21_PAQUETE_PARA_SUBIR.zip`
- Pendiente: recibir o ejecutar auditoria y convertirla en correcciones concretas sobre la guia v21.
- Ultima actualizacion: 2026-04-16

## Thread: Pipeline tecnico Ed.2 ETABS 21 (VIGENTE)
- Estado actual: el pipeline esta rebaselinado al flujo estatico oficial y endurecido para corrida directa por consola en ETABS 21, pero no cerrado sin corrida real.
- Evidencia:
  - `autonomo/scripts/ed2/`
  - `docs/estudio/ED2_PARTE1_CANON.md`
  - `autonomo/research/ED2_PARTE1_AUDITORIA.md`
  - `https://github.com/kcortes765/taha.git`
- Delta reciente:
  - `connect()` ahora soporta create/open model via env para pipeline multi-proceso.
  - `run_pipeline_ed2.py` y `diag.py` ya exponen `--create-if-missing` y `--model`.
  - `06_assignments_ed2.py` ya no acepta insertion point incompleto ni edge constraints manuales.
- Abierto: corrida real, `results/`, `verify_ed2.py` en PASS, contraste UI/API en la misma workstation.
- Regla operativa vigente:
  - este PC publica codigo por git
  - la WS baja codigo por git
  - la WS devuelve evidencia por `transfer/`
- Ultima actualizacion: 2026-04-19
