# WS2 APOS delta 20260515_0016 - ED1 torsión confirmada

## Motivo

Se corrige el goal de Edificio 1 porque la torsión accidental no debía quedar como duda abierta. El usuario pidió confirmar desde fuentes oficiales del curso y dejar el plan extendido sin ambigüedad.

## Corrección central

Edificio 1 **debe incluir torsión accidental** y debe analizar 6 casos:

1. Diafragma rígido + torsión caso a).
2. Diafragma rígido + torsión caso b) forma 1.
3. Diafragma rígido + torsión caso b) forma 2.
4. Diafragma semirrígido + torsión caso a).
5. Diafragma semirrígido + torsión caso b) forma 1.
6. Diafragma semirrígido + torsión caso b) forma 2.

## Evidencia base

- Enunciado actualizado p.10-p.11: ED1 pide análisis de los 6 casos.
- Apuntes p.117-p.123: torsión accidental forma a), forma b) alternativa/forma 1 y alternativa/forma 2, con combinaciones.
- Material Apoyo p.29-p.45: pasos ETABS para método a), método b forma 1 y método b forma 2.
- NCh433:2026 p.34: torsión accidental en análisis modal espectral por forma a) o b).
- NCh433:2026 p.27 y p.29: deformaciones sísmicas con torsión accidental y límite `0.002h` para hormigón armado.
- Transcripciones `sismo 10`, `sismo 11` y `taller sismo 8`: el profesor recalca que ED1 debe aplicar las dos formas y comparar.

## Archivos creados/actualizados

Local:

- `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog4\Edificio_1\00_goal_y_plan\MATRIZ_FUENTES_ED1_PROG4_TORSION_Y_METODOLOGIA_20260515_0015.md`
- `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog4\Edificio_1\00_goal_y_plan\evidencia_fuentes_20260515_0015`
- `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog4\Edificio_1\00_goal_y_plan\GOAL_ED1_PROG4_PARTE1_DINAMICO_ESPECTRAL_OFICIAL_20260514_2332.md`

Versionado:

- `transfer/ws2-ed1-etabs21-context/reports/MATRIZ_FUENTES_ED1_PROG4_TORSION_Y_METODOLOGIA_20260515_0015.md`
- `transfer/ws2-ed1-etabs21-context/reports/GOAL_ED1_PROG4_PARTE1_DINAMICO_ESPECTRAL_OFICIAL_20260514_2332.md`

## Implicancia

Desde ahora el goal ED1 parte con metodología confirmada:

- implementar 6 casos;
- separar combinaciones por método;
- verificar deformaciones con `CP + SC ± Sismo`;
- auditar CM/CR, masa, modos, espectro, corte basal, drift, cortes de muros e indicadores.

