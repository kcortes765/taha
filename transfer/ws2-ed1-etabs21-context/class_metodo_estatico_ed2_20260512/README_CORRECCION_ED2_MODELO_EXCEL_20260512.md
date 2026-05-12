# Nota histórica: variante ED2 con cachos solo en vigas

Fecha de cierre local: `2026-05-12 16:36`.

**Actualización importante 2026-05-12 17:05:** este paquete no debe leerse como recomendación final del modelo del curso. Corresponde a una variante de sensibilidad que quitó cachos rígidos de columnas para explicar por qué el período sube hacia `0.46 s`. El enunciado actualizado exige cachos rígidos automáticos `0.75` en encuentros de vigas y columnas. La versión alineada a ese criterio está documentada en:

`README_DIAGNOSTICO_PERIODO_ED2_AMBOS_RZ_20260512.md`

## Estado corregido

- Modelo corregido: `Edificio_2/models/ED2_CLASE_METODO_ESTATICO_CORREGIDO_20260512_162839.EDB`.
- Excel corregido: `Edificio_2/excel/ED2_METODO_ESTATICO_MANUAL_EXCEL_CORREGIDO_20260512.xlsx`.
- Reporte técnico: `Edificio_2/reports/FINALIZAR_ED2_INSTANCIA_RECUPERADA_20260512_163634.md`.
- CSV modal: `Edificio_2/results/modal_participating_mass_ratios_instancia_recuperada_20260512_163634.csv`.
- CSV distribución estática: `Edificio_2/results/ed2_static_distribution_instancia_recuperada_20260512_163634.csv`.

## Cambios aplicados en esta variante

- Cachos rígidos `Rigid-zone factor = 0.75` solo en vigas `V50x70G25` y `V45x70G25`.
- Cachos rígidos removidos de columnas `C70x70G25` y `C65x65G25`.
- Masa sísmica corregida a `PP + TERP + TERT + 0.25*SCP + 0*SCT`.
- `SCT` sigue existiendo como carga gravitacional; no entra en la matriz de masa para el método estático según la clase `sismo 14`.
- El modelo fue guardado después de recuperar resultados para resolver el aviso de compatibilidad de ETABS.

## Resultados de esta variante

- `Tx* = 0.461202 s`, modo 2.
- `Ty* = 0.461221 s`, modo 1.
- `Tz* = 0.408064 s`, modo 3.
- Peso sísmico total: `5248.471 tonf`.
- `Q0x = 771.525 tonf`.
- `Q0y = 771.525 tonf`.
- `sum(Fx)-Q0x = 1.13687e-13`.
- `sum(Fy)-Q0y = 1.13687e-13`.

## Nota sobre la anormalidad de ETABS

ETABS mostró el aviso:

`Recent analysis results have been found for this model filename, but which are not flagged as being compatible with this model.`

La acción segura usada fue seleccionar `Sí` para recuperar resultados, guardar el modelo y cerrar ETABS. Seleccionar `No` habría eliminado los resultados.

Al finalizar, se verificó que no quedara ninguna instancia de ETABS abierta.
