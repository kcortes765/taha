# Apuntes actualizados 2026-05-08 - Revision ejecutiva

## Archivos comparados

Anterior:

`docs/Apuntes del Curso.pdf`

Nuevo entregado por usuario:

`C:\Users\kevin\Downloads\Apuntes del Curso 080526.pdf`

Copia guardada en repo:

`docs/Apuntes del Curso 2026-05-08 actualizado.pdf`

Copia para WS2:

`transfer/ws2-ed1-etabs21-context/files/00_Apuntes_del_Curso_2026-05-08_actualizado.pdf`

## Hashes y tamano

Anterior:

`C07FD85E517A6E7711B430DE9938962B20A404828AB27135FD94465B8E9B98A7`

Nuevo:

`ED7AC937AB1F04D2F34DC8FB9DBFB0D272F554068BCBDCDE148BCBA4B42504FB`

## Cambio estructural

- Apuntes anteriores: 321 paginas.
- Apuntes actualizados: 344 paginas.
- Aumentan 23 paginas.
- Fecha de modificacion PDF nuevo: 2026-05-04 10:58:05.

## Paginas clave nuevas/relevantes para Parte 1

- Pagina 61: declara que desde el 26 de marzo de 2026 esta vigente `NCh433:2026`.
- Paginas 70 a 77: incorporan `NCh3793:2025`, `Vs30`, `Tg` y razon espectral `H/V` para caracterizacion del sitio.
- Pagina 96: bloque `Factor de reduccion de la respuesta NCh433:2026`.
- Pagina 98: metodo estatico con `Qo = C * I * P`, formula de `C`, periodo `T*` y limites `Cmin/Cmax`.
- Pagina 103: combinaciones para metodo estatico, 19 combinaciones con `CP`, `L`, `Lr`, `SDX`, `SDY`, `TEX`, `TEY`.
- Pagina 112: metodo dinamico modal espectral, espectro `Sa`, `R*`, `I`, `Ao`, y limites de corte basal.
- Pagina 118: metodo dinamico con torsion accidental forma `a)`, 15 combinaciones.
- Pagina 122: metodo dinamico con torsion accidental forma `b)`, alternativa 1, 11 combinaciones.
- Pagina 123: metodo dinamico con torsion accidental forma `b)`, alternativa 2, 7 combinaciones.
- Paginas 321 a 344: problemas propuestos ampliados/actualizados, incluyendo problemas con metodo estatico, dinamico modal espectral, torsion accidental, desplazamientos y casos de muros/marcos.

## Contraste con NCh433:2026

La lectura vigente para el curso queda:

1. `NCh433:2026` es la base normativa canonica.
2. Los apuntes actualizados ya reconocen explicitamente esa vigencia en pagina 61.
3. Las paginas 70 a 77 agregan capa moderna de sitio (`NCh3793:2025`, `Vs30`, `Tg`, `H/V`).
4. Las formulas y combinaciones de paginas 98, 103, 112, 118, 122 y 123 deben usarse como guia del profesor para ETABS, siempre contrastadas contra la norma oficial incluida en `files/05_NCh433_2026_para_Curso.pdf`.

## Advertencia sobre material historico dentro del mismo PDF

El PDF actualizado todavia conserva paginas/problemas que mencionan:

- `NCh433 Of.96 Mod 2009`
- `DS61`

Eso no debe interpretarse como vuelta a la base normativa antigua. Es material historico o de problemas previos. Para el taller 2026, si hay conflicto, priorizar:

1. Enunciado actualizado.
2. `NCh433:2026`.
3. Material de apoyo taller 2026.
4. Apuntes actualizados 2026-05-08.
5. Guias UI/API actualizadas.
6. Capa historica `NCh433:1996 + DS61` solo como referencia si no contradice.

## Impacto practico

- No cambia por si solo la geometria de Ed.1 ni Ed.2.
- Si cambia la fuente academica principal: ya no conviene usar el PDF de 321 paginas como base.
- Para WS2, usar siempre `files/00_Apuntes_del_Curso_2026-05-08_actualizado.pdf`.
- El indice cortado antiguo `docs/apuntes/INDICE.md` sigue sirviendo para orientacion, pero sus paginas corresponden al PDF viejo de 321 paginas. No usarlo como paginacion final del PDF nuevo.

