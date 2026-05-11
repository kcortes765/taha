# WS2 ED1 vigas - verificacion de visibilidad

- Fecha: 2026-05-09 06:25 America/Santiago
- Modelo: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif1\models\ED1_PARTE1_WS2_PROG2_20260508_2213.EDB`
- Script: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif1\workbench\ed1_beam_visibility_probe.py`
- ETABS: una sola instancia, iniciada por el script y cerrada al finalizar.

## Resultado

Las vigas si existen en el modelo. La no visualizacion en la captura parece ser un problema de display/representacion, no ausencia de frame objects.

Evidencia OAPI:

- Frame objects totales: `320`
- Vigas con seccion `VI20/60G30`: `320`
- Geometria: `320` frames horizontales
- Distribucion por piso: `16` vigas en cada una de las 20 elevaciones:
  - 3.4, 6.0, 8.6, 11.2, 13.8, 16.4, 19.0, 21.6, 24.2, 26.8, 29.4, 32.0, 34.6, 37.2, 39.8, 42.4, 45.0, 47.6, 50.2, 52.8 m
- Cardinal Point: `2` en las 320 vigas
- Stiff transform API: `False` en las 320 vigas, consistente con `Do not transform frame stiffness for offsets from centroid`
- Auto offset: `True` en las 320 vigas
- Rigid factor: `0.75` en muestras leidas

Archivos de evidencia:

- Reporte local: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif1\reports\ED1_VIGAS_VISIBILIDAD_20260509_0625.md`
- JSON: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif1\logs\ed1_beam_visibility_20260509_0625.json`
- CSV frames: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif1\exports\ed1_beam_visibility_frames_20260509_0625.csv`
- Tabla ETABS `Frame Assignments - Section Properties`: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif1\exports\ed1_beam_visibility_Frame_Assignments_Section_Properties_20260509_0625.csv`

## Interpretacion visual

La captura muestra muros/losas/grillas, pero las vigas pueden quedar poco visibles porque:

- los frames estan dibujados como lineas blancas/grises y se confunden con grilla/malla;
- la extrusion de frames podria estar apagada;
- las losas/muros translucidos pueden tapar o mezclar visualmente vigas invertidas en el mismo nivel;
- la seccion `VI20/60G30` esta presente, pero si ETABS no esta mostrando `extrude frame objects`, no se ve como volumen.

## Accion recomendada en UI

Para inspeccion visual:

- activar visualizacion/extrusion de frame objects;
- ocultar temporalmente shells/areas o bajar su transparencia;
- seleccionar `Frame Objects` o mostrar `Frame Section Assignments`;
- revisar un piso tipo en planta/elevacion, no solo vista 3D con areas translucidas.

No se debe reconstruir geometria por esta captura; primero cambiar opciones de display y confirmar seleccion de frames.
