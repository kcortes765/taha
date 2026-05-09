# Modelado manual Edificio 1 - notas vivas

Fecha: 2026-04-27
Contexto: modelado manual en ETABS 21 desde modelo vacio.

## Grilla auxiliar corregida por usuario

Coordenadas auxiliares en direccion Y, medidas desde el origen:

- `Aux1`: `Y = 3.271 m`
- `Aux2`: `Y = 8.371 m`

Estas coordenadas se usan para tramos de muros en direccion Y que no terminan exactamente en ejes letrados `A-F`.

## Muros direccion Y - planta tipo Story2

Lista operativa corregida:

| Eje | Tramo | Seccion |
| --- | --- | --- |
| 1 | B -> C | MHA30G30 |
| 2 | B -> Aux1 | MHA20G30 |
| 3 | D -> F | MHA30G30 |
| 4 | A -> C | MHA30G30 |
| 5 | D -> F | MHA30G30 |
| 6 | B -> Aux1 | MHA20G30 |
| 7 | D -> F | MHA30G30 |
| 8 | B -> C | MHA20G30 |
| 9 | Aux2 -> E | MHA20G30 |
| 10 | B -> Aux1 | MHA20G30 |
| 11 | Aux2 -> E | MHA20G30 |
| 12 | D -> F | MHA30G30 |
| 13 | A -> C | MHA30G30 |
| 14 | D -> F | MHA30G30 |
| 15 | B -> Aux1 | MHA20G30 |
| 16 | B -> C | MHA30G30 |
| 17 | D -> F | MHA30G30 |

## Regla de trabajo

- Dibujar primero en `Story2`.
- No usar `All Stories` al dibujar.
- Completar y revisar planta tipo antes de replicar.
- Replicar despues a `Story1` y `Story3-Story19`.
- Tratar `Story20` aparte por techo distinto.
