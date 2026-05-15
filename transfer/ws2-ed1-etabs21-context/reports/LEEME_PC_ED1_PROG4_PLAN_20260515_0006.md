# LEEME PC - ED1 PROG4 plan 20260515_0006

## Objetivo

Continuar Edificio 1 en `prog4` sin mezclar estados antiguos. El objetivo vigente es cerrar Parte 1 del Edificio 1 con análisis dinámico/modal espectral, trazabilidad por fuentes oficiales del curso y auditoría fuerte antes de declarar resultados.

## Archivo principal que debes leer

`transfer/ws2-ed1-etabs21-context/reports/GOAL_ED1_PROG4_PARTE1_DINAMICO_ESPECTRAL_OFICIAL_20260514_2332.md`

Ese es el plan maestro.

## Checkpoint base local en WS2

Modelo base físico/modal, no final Parte 1:

`C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog4\Edificio_1\01_modelos\ED1_PROG4_CIERRE_MODAL_20260512_2306.EDB`

Estado: base vigente para seguir. No declararlo como cierre final.

## Regla central

Para decisiones de ingeniería usar solo:

- enunciado actualizado;
- apuntes del curso 2026-05-08;
- Material Apoyo Taller 2026;
- NCh433:2026 usada por el curso;
- NCh3171/NCh1537 cuando el curso las use;
- transcripciones de clase.

La documentación oficial CSI/ETABS se usa solo para API/OAPI, errores, tablas, guardado, sesión y extracción.

No usar como verdad final:

- guías MD destiladas;
- respuestas previas de IA;
- internet genérico;
- criterios tipo "normalmente".

## Seguridad ETABS

Antes de abrir ETABS o usar OAPI:

```powershell
Get-Process ETABS -ErrorAction SilentlyContinue
```

Una sola instancia. Si aparece `miOpen`, `Warning`, `Error`, `array`, recuperación de resultados o inicialización inesperada: detener y registrar.

## Qué NO hacer todavía

- No tratar ED1 como terminado.
- No aplicar criterios desde Edificio 2.
- No volver a los modificadores de losa `0.25`.
- No modificar el checkpoint base sin copia fechada.
- No correr análisis masivos sin matriz de fuentes y auditoría previa.

## Estado Git

Rama:

`codex/ws2-ed1-etabs21-context`

Commit donde quedó el plan:

`8a58fd5 Add ED1 PROG4 official goal plan`

Este archivo agrega sólo un resumen para sincronizar la laptop personal.

