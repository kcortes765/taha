# Canon Oficial - Edificio 2 Parte 1

## Estado del documento
- Fecha: 2026-04-20
- Alcance: Edificio 2, Parte 1 del taller ADSE
- Regla: este documento fija el camino oficial para la guia UI ETABS 21 y el pipeline API

## Jerarquia de fuentes
1. `docs/Enunciado Taller.pdf`
2. `docs/estudio/00-ESTADO-NORMATIVO-CURSO-2026.md`
3. Correos y transcripciones del curso posteriores al `2026-03-27`
4. `materiales_fuente/sismo/Normas Curso/Normas a Utilizar en Curso/NCh433-2026 para Curso.pdf`
5. `docs/Material taller/Material Apoyo Taller 2026.pdf`
6. `docs/Normas Utilizadas ADSE/NCh 3171- 2017.pdf`
7. `docs/Normas Utilizadas ADSE/NCh1537-_2009_Diseno_estructural_de_edificios_-_Cargas_perman.pdf`
8. `docs/Normas Utilizadas ADSE/DECRETO 60 2011 DISEÃ‘O Y CALCULO HORMIGON ARMADO.pdf`
9. Todo lo demas del repo se considera derivado o historico

## Estado normativo de Edificio 2
- Desde el punto de vista del curso, Edificio 2 debe defenderse con `NCh433:2026`.
- El enunciado sigue diciendo "normativa vigente", por lo que despues del cambio del curso esa frase ya no debe leerse como `NCh433:1996 Mod.2009 + DS61`.
- Para `Antofagasta + Zona 3 + Sitio C + Categoria II`, los parametros principales del caso historico coinciden numericamente con `NCh433:2026`.
- Por eso Edificio 2 no cambia radicalmente en numeros, pero si cambia la base formal de cita y defensa.

## Geometria y estructuracion exigida
- Sistema: marcos especiales de hormigon armado, 5 pisos.
- Planta: 32.5 m x 32.5 m, grilla regular 6 x 6, vanos de 6.5 m.
- Alturas: 3.5 m en piso 1; 3.0 m en pisos 2 a 5; altura total 15.5 m.
- Base: empotrada.
- Diafragma: rigido `D1` en Parte 1, segun enunciado.
- Cachos rigidos: automaticos, factor 0.75, en todos los encuentros viga-columna.

## Materiales y secciones
- Hormigon: G25.
- Acero: A630-420H.
- Losa: 17 cm en todos los pisos.
- Columnas:
  - Pisos 1-2: 70 x 70 cm
  - Pisos 3-5: 65 x 65 cm
- Vigas:
  - Pisos 1-2: 50 x 70 cm
  - Pisos 3-5: 45 x 70 cm

## Cargas y pesos
- Cargas permanentes:
  - `PP`: peso propio automatico
  - `TERP`: 140 kgf/m2 en pisos tipo
  - `TERT`: 100 kgf/m2 en techo
- Sobrecargas:
  - `SCP`: 300 kgf/m2 en pisos tipo
  - `SCT`: 100 kgf/m2 en techo
- Masa sismica:
  - usar `NCh433:2026 5.5.1` como base
  - en uso general, no considerar menos de `25%` de sobrecarga
  - si existiera una zona de aglomeracion usual, no bajar de `50%`
- Peso sismico operativo:
  - `W = PP + TERP + TERT + 0.25*SCP + 0.25*SCT`
  - el cierre exige contraste con tablas reales de ETABS

## Metodo de analisis oficial
- Metodo principal: estatico.
- Justificacion: Ed.2 tiene 5 pisos y altura total 15.5 m, por lo que el metodo estatico es aplicable bajo `NCh433:2026 6.2.1`.
- El caso modal se conserva solo para extraer `Tx*`, `Ty*` y `Tz*`.
- El analisis dinamico modal espectral no pertenece al camino oficial de Parte 1.

## Parametros sismicos oficiales
- Ubicacion: Antofagasta.
- Zona: 3.
- `Ao = 0.4g`
- Suelo: C
- `S = 1.05`
- `T0 = 0.40 s`
- `T' = 0.45 s`
- `n = 1.40`
- `p = 1.60`
- Categoria: II
- `I = 1.0`
- Sistema: marcos especiales HA
- `R = 7`
- `R0 = 11`
- Fuente: `NCh433:2026`, Tablas 5, 7 y 8

## Formulas oficiales

### Coeficiente sismico
`C = (2.75*S*Ao)/(g*R) * (T'/T*)^n`

### Limites
- `Cmin = Ao*S/(6*g)`
- `Cmax = 0.35*S*Ao/g`

### Corte basal de diseÃ±o
`Vd = C*I*W`

### Distribucion por piso
- Para Ed.2 (5 pisos), usar NCh433 6.2.5 para edificios de no mas de 5 pisos:
- `Fk = (Ak*Pk / sum(Aj*Pj)) * Qo`
- `Ak = sqrt(1 - Zk-1/H) - sqrt(1 - Zk/H)`

### Torsion accidental estatica
- Formula oficial Ed.2: `ea = +/-0.10*bk*(Zk/H)`
- Para Ed.2 cuadrado: `bk = 32.5 m` en ambas direcciones
- Se exige como momento de torsion accidental por piso: `Mtk = Fk * ea`

## Drift y masa bajo NCh433:2026
- Drift en `CM`: usar `5.9.2`.
- Drift en cualquier punto de planta: usar `5.9.3`.
- Para marcos especiales de hormigon armado, el limite sigue siendo `0.0020h`.

## Casos oficiales
- `Modal`: auxiliar para periodos y participacion modal
- `EX`: sismo estatico en X
- `EY`: sismo estatico en Y
- `TEX`: torsion accidental asociada a `EX`
- `TEY`: torsion accidental asociada a `EY`

## Combinaciones oficiales
- Gravitacionales:
  - `C1 = 1.4D`
  - `C2 = 1.2D + 1.6L + 0.5Lr`
  - `C3 = 1.2D + L + 1.6Lr`
- Sismicas:
  - `C4 = 1.2D + L + 1.4Ex`
  - `C5 = 0.9D + 1.4Ex`
  - `C6 = 1.2D + L + 1.4Ey`
  - `C7 = 0.9D + 1.4Ey`
- En implementacion ETABS/API, `C4-C7` se expanden en la familia completa:
  - signo positivo y negativo del sismo principal
  - signo positivo y negativo de la torsion accidental
  - total: 19 combinaciones (3 gravitacionales + 8 en X + 8 en Y)

## Combinaciones de servicio para drift
- Para verificar drift con torsion accidental, usar combinaciones de servicio:
  - `EX + TEX`, `EX - TEX`, `-EX + TEX`, `-EX - TEX`
  - `EY + TEY`, `EY - TEY`, `-EY + TEY`, `-EY - TEY`
- La verificacion debe revisar:
  - condicion 1: drift en CM `<= 0.002`
  - condicion 2: exceso torsional `drift_max - drift_CM <= 0.001`
- Flujo ETABS oficial:
  - `Joint Drifts` filtrado al nodo mas cercano al CM para la condicion 1
  - `Diaphragm Max Over Avg Drifts` para el drift maximo y la condicion 2

## Verificaciones oficiales Parte 1
- Peso sismico total y por area.
- Periodos `Tx*`, `Ty*`, `Tz*`.
- Calculo de `C`, chequeo `Cmin/Cmax`.
- Corte basal de diseÃ±o por direccion.
- Fuerzas por piso.
- Momentos de torsion accidental por piso.
- Graficos `V(z)` y `Mvolcante(z)` en ambas direcciones.
- Drift sismico y verificacion de cumplimiento.

## Entregables minimos
- Figuras de planta y 3D.
- Tabla de cargas y estados de carga.
- Tabla de `W`, `Tx*`, `Ty*`, `Tz*`, `C`, `Cmin`, `Cmax`, `Vd`.
- Tabla de fuerzas por piso y torsion accidental.
- Graficos `V(z)` y `Mvolcante(z)`.
- Drift con conclusion de cumplimiento.

## Conclusion operativa Ed.2
- Edificio 2 sigue siendo defendible por el camino estatico de Parte 1.
- Los valores principales de `Ao`, `S`, `T0`, `T'`, `n`, `p`, `I`, `R` y `R0` para este caso coinciden con la capa historica que el repo venia usando.
- Por lo tanto, el impacto practico en numeros es bajo.
- El impacto fuerte esta en la base de cita y en no seguir justificando el modelo con `DS61` como si siguiera siendo la norma activa del curso.

## Lo que queda fuera del camino oficial
- Response spectrum como metodo principal de Ed.2 Parte 1.
- Flujo semi-rigido heredado de Ed.1.
- Tres metodos de torsion accidental heredados del material dinamico.
- Generacion de informes o plots con resultados sinteticos cuando faltan `.edb` o CSV reales.
