# WS2 APOS delta - modelos clase pre-espectro

Fecha: 2026-05-11 14:20.

## Cambio aplicado

Se creó una carpeta específica para modelos de clase previos al bloque sísmico/espectral:

`C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\CLASE_PRE_ESPECTRO_20260511_1356`

## Modelos generados

- Edificio 1:
  - `Edificio_1\models\ED1_CLASE_PRE_ESPECTRO_20260511.EDB`
  - Estado: geometría, diafragma, apoyos, cargas gravitacionales, fuente de masa y modal listos.
  - No contiene espectro, casos `SEx/SEy/SEx_b2/SEy_b2`, torsión accidental ni combinaciones dinámicas.

- Edificio 2:
  - `Edificio_2\models\ED2_CLASE_PRE_ESPECTRO_20260511.EDB`
  - Estado: pipeline ED2 pasos 1 a 8 completado: geometría, materiales, secciones, elementos, diafragma, cargas, fuente de masa y modal auxiliar.
  - No contiene aplicación de `EX/EY/TEX/TEY`, combinaciones ni análisis final sísmico estático.

## Nota sobre error visto

El log ED2 registra `UnicodeEncodeError` por caracteres de consola Windows durante mensajes de logging, pero el pipeline reportó `Succeeded: 8 | Failed: 0`. No fue falla estructural del modelo.

## ETABS

Se mantuvo una sola instancia ETABS 21.2.0. Al cierre de este delta, la instancia seguía respondiendo con el modelo ED2 de clase activo.
