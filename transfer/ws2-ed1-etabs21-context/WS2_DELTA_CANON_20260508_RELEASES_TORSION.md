# Delta canonico 2026-05-08 - releases torsionales Edificio 1

## Cambio

La auditoria WS2 detecto releases torsionales en Edificio 1. Inicialmente eso se podia interpretar como problema critico, pero el usuario corrigio el canon:

> Los releases torsionales fueron pedidos por el profesor.

## Implicancia

No corregir ni eliminar releases torsionales por defecto.

Lo correcto es:

- verificar que el patron coincida con lo pedido por el profesor;
- confirmar que no haya liberaciones axiales/corte indebidas;
- documentar el patron;
- mantenerlo en la copia de trabajo salvo instruccion explicita contraria.

## Patron reportado

- `TI, M2I, M3I`: 180 frames.
- `TJ, M2J, M3J`: 100 frames.
- `TI, M2I, M3I, M2J, M3J`: 40 frames.
- Sin release: 0 frames.

