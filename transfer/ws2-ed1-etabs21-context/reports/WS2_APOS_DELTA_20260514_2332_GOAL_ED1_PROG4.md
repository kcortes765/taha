# WS2 APOS delta 20260514_2332 - Goal ED1 PROG4

## Motivo

El usuario pidió ordenar memoria, elocuencia, foco técnico y trazabilidad antes de continuar con Edificio 1. Se define un objetivo largo específico para cerrar Edificio 1 Parte 1 con fuentes oficiales del curso, pruebas en serie y control estricto de sesión ETABS.

## Goal creado

`GOAL_ED1_PROG4_PARTE1_DINAMICO_ESPECTRAL_OFICIAL_20260514_2332`

Archivo:

`C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog4\Edificio_1\00_goal_y_plan\GOAL_ED1_PROG4_PARTE1_DINAMICO_ESPECTRAL_OFICIAL_20260514_2332.md`

Copia versionable para Git:

`transfer\ws2-ed1-etabs21-context\reports\GOAL_ED1_PROG4_PARTE1_DINAMICO_ESPECTRAL_OFICIAL_20260514_2332.md`

## Criterio central

- Fuentes de verdad de ingeniería: enunciado, apuntes 2026-05-08, Material Apoyo Taller 2026, NCh433:2026 usada por el curso, NCh3171/NCh1537 cuando el curso las use, y transcripciones.
- Documentación oficial CSI/ETABS: permitida para API/OAPI, errores, tablas, sesión y extracción, no para reemplazar criterios del curso.
- No usar MD destilados ni guías genéricas como autoridad final.

## Estado de partida ED1

Checkpoint base:

`C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog4\Edificio_1\01_modelos\ED1_PROG4_CIERRE_MODAL_20260512_2306.EDB`

ED1 no queda declarado cerrado Parte 1. Queda como base física/modal para cerrar el flujo dinámico/modal espectral.

## Seguridad ETABS

Antes de abrir ETABS o OAPI se debe ejecutar:

`Get-Process ETABS -ErrorAction SilentlyContinue`

Una sola instancia. Si aparece diálogo `miOpen`, `Warning`, `Error`, `array`, recuperación de resultados o inicialización inesperada, detener y registrar.

## Archivos APOS actualizados

Se anexaron entradas a:

- `.apos/DECISIONS.md`
- `.apos/JOURNAL.md`
- `.apos/SOURCES.md`
- `.apos/RESEARCH_LOG.md`

No se reescriben archivos append-only.
