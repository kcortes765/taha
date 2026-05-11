# ED2 clase - modelo previo a cargas sísmicas estáticas

- Modelo generado: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\CLASE_PRE_ESPECTRO_20260511_1356\Edificio_2\models\ED2_CLASE_PRE_ESPECTRO_20260511.EDB`
- Modelo activo al guardar: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\CLASE_PRE_ESPECTRO_20260511_1356\Edificio_2\models\Edificio2_parte1_oficial.EDB`
- Estado: geometría, materiales, secciones, columnas, vigas, losas, diafragma, apoyos, cargas gravitacionales, fuente de masa y modal auxiliar listos.
- Corte exacto: no se aplicaron casos sísmicos estáticos `EX/EY` ni torsión `TEX/TEY`.

## Resumen verificado

- Patrones de carga: `Dead, Live, PP, TERP, TERT, SCP, SCT, ~LLRF`
- Casos de carga: `Dead, Live, Modal, PP, TERP, TERT, SCP, SCT, ~LLRF`
- Combinaciones: `sin combinaciones agregadas por este script`

## Modal auxiliar

```json
{
  "modal_case": "Modal",
  "directional_periods": {
    "X": {
      "period": 0.562,
      "mode": 1,
      "participation": 0.7853
    },
    "Y": {
      "period": 0.562,
      "mode": 2,
      "participation": 0.7853
    },
    "RZ": {
      "period": 0.517,
      "mode": 3,
      "participation": 0.8418
    }
  }
}
```

## Uso en clase

Desde este modelo corresponde seguir con el método estático: cálculo/aplicación de `EX/EY`, torsión accidental `TEX/TEY`, combinaciones, análisis y extracción de resultados.
