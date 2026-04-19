# Canon Oficial - Edificio 2 Parte 1

## Estado del documento
- Fecha: 2026-04-03
- Alcance: Edificio 2, Parte 1 del taller ADSE
- Regla: este documento fija el camino oficial para la guia UI ETABS 21 y el pipeline API

## Jerarquia de fuentes
1. `docs/Enunciado Taller.pdf`
2. `docs/apuntes/INDICE.md` y `docs/apuntes/02c-Analisis-Estatico.pdf`
3. `docs/Material taller/Material Apoyo Taller 2026.pdf`
4. `docs/Normas Utilizadas ADSE/NCh0433-1996-Mod.2009.pdf`
5. `docs/Normas Utilizadas ADSE/DECRETO 61 2011 DISEÑO SISMICO DE EDIFICIOS.pdf`
6. Todo lo demas del repo se considera derivado

## Geometria y estructuracion exigida
- Sistema: marcos especiales de hormigon armado, 5 pisos.
- Planta: 32.5 m x 32.5 m, grilla regular 6 x 6, vanos de 6.5 m.
- Alturas: 3.5 m en piso 1; 3.0 m en pisos 2 a 5; altura total 15.5 m.
- Base: empotrada.
- Diafragma: solo rigido `D1`.
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
- Peso sismico:
  - `W = PP + TERP + TERT + 0.25*SCP + 0.25*SCT_techo`
  - para el flujo oficial API se aceptan story weights derivados del modelo; el cierre exige contraste con reacciones/base de ETABS

## Metodo de analisis oficial
- Metodo principal: estatico.
- Justificacion: Ed.2 tiene 5 pisos, por lo que el metodo estatico es aplicable.
- El caso modal se conserva solo para extraer `T*`, `Ty*` y `Tz*`.
- El analisis dinamico modal espectral no pertenece al camino oficial de Parte 1.

## Parametros sismicos oficiales
- Ubicacion: Antofagasta.
- Zona: 3.
- `Ao = 0.4g`
- Suelo: C
- `S = 1.05`
- `T' = 0.45 s`
- `n = 1.40`
- Categoria: II
- `I = 1.0`
- Sistema: marcos especiales HA
- `R = 7`
- `Ro = 11`

## Formulas oficiales

### Coeficiente sismico
`C = (2.75*S*Ao)/(g*R) * (T'/T*)^n`

### Limites
- `Cmin = Ao*S/(6*g)`
- `Cmax = 0.35*S*Ao/g`

### Corte basal de diseño
`Vd = C*I*W`

### Distribucion por piso
- Para Ed.2 (5 pisos), usar NCh433 6.2.5 para edificios de no mas de 5 pisos:
- `Fk = (Ak*Pk / sum(Aj*Pj)) * Qo`
- `Ak = sqrt(1 - Zk-1/H) - sqrt(1 - Zk/H)`

### Torsion accidental estatica
- Formula oficial Ed.2: `ea = +/-0.10*bk*(Zk/H)`
- Para Ed.2 cuadrado: `bk = 32.5 m` en ambas direcciones
- Se exige como momento de torsion accidental por piso: `Mtk = Fk * ea`

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
- Periodos `T*`, `Ty*`, `Tz*`.
- Calculo de `C`, chequeo `Cmin/Cmax`.
- Corte basal de diseño por direccion.
- Fuerzas por piso.
- Momentos de torsion accidental por piso.
- Graficos `V(z)` y `Mvolcante(z)` en ambas direcciones.
- Drift sismico y verificacion de cumplimiento.

## Entregables minimos
- Figuras de planta y 3D.
- Tabla de cargas y estados de carga.
- Tabla de `W`, `T*`, `Ty*`, `Tz*`, `C`, `Cmin`, `Cmax`, `Vd`.
- Tabla de fuerzas por piso y torsion accidental.
- Graficos `V(z)` y `Mvolcante(z)`.
- Drift con conclusion de cumplimiento.

## Lo que queda fuera del camino oficial
- Response spectrum como metodo principal de Ed.2 Parte 1.
- Flujo semi-rigido heredado de Ed.1.
- Tres metodos de torsion accidental heredados del material dinamico.
- Generacion de informes o plots con resultados sinteticos cuando faltan `.edb` o CSV reales.
