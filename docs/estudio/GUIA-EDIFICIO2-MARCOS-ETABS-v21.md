# Guia Operativa - Edificio 2 en ETABS 21

## Estado del documento
- Fecha: 2026-04-18
- Alcance: Taller ADSE UCN 1S-2026, Edificio 2
- Objetivo: dejar un flujo manual en ETABS 21 alineado con lo que realmente pide el taller
- Criterio: mandan enunciado, correos de Music, apunte actualizado y material de apoyo

## 1. Que se espera realmente para Edificio 2

### 1.1 Lo que pide el enunciado del taller
Fuente: `docs/Enunciado Taller.pdf`, pp. 8-13

#### Parte 1 - Edificio 2
1. Descripcion del edificio y su estructuracion.
2. Modelacion del edificio, con figuras 3D y en planta.
3. Cargas y estados de carga a considerar.
4. Analisis sismico:
   - peso sismico total y peso sismico por m2
   - periodos `Tx*`, `Ty*`, `Tz*`
   - coeficientes sismicos y chequeo `Cmin` y `Cmax`
   - corte basal de diseño en cada direccion
   - tabla de fuerzas sismicas y momentos de torsion accidental por piso
   - grafico y tabla de esfuerzo de corte en altura en ambas direcciones
   - grafico y tabla de momento volcante en altura en ambas direcciones
   - verificacion de deformaciones sismicas y comentario

#### Parte 2 - Edificio 2
1. Mostrar el diagrama de momento en las vigas del marco del eje A para:
   - `1,2D + 1,6L + 0,5Lr`
   - `0,9D + 1,4E`
   - `0,9D - 1,4E`
2. Diseñar sin programa:
   - la viga del primer piso entre ejes 1 y 2 del eje A
   - la columna del primer piso en interseccion eje A con 1
3. Diseñar en ETABS:
   - columnas del primer y segundo piso del eje A
   - vigas del primer piso del eje A
4. Verificar condiciones normativas de diseño y detallar armaduras.

### 1.2 Lo que agregan los correos de Music
Fuente: avisos del profesor citados en esta sesion

#### Aviso del 2026-04-13
- El lunes 20 se explicaria como usar ETABS.
- El martes 21 se veria torsion accidental en analisis dinamico modal espectral.

#### Aviso del 2026-04-15
- La primera entrega consiste en modelar Edificio 1 y Edificio 2.
- Para ambos edificios se debe realizar analisis modal.
- Se deben encontrar:
  - masas equivalentes
  - periodos asociados
  - tantos modos como sea necesario para lograr 90% de `Mnx`, `Mny` y `Mnteta`
  - `Tx`, `Ty` y `Tz`
- Fecha indicada en ese aviso: martes 12 de mayo de 2026.

### 1.3 Lectura operativa correcta
- Edificio 2 no hereda la tabla de 6 casos de Edificio 1.
- Edificio 2 no se resuelve por modal espectral como camino principal de la Parte 1.
- Edificio 2 si requiere un caso modal:
  - porque el enunciado pide `Tx*`, `Ty*`, `Tz*`
  - y porque el correo del 2026-04-15 lo hace explicito para la primera entrega
- El nucleo de la Parte 1 de Edificio 2 sigue siendo:
  - metodo estatico
  - diafragma rigido
  - 19 estados de carga del metodo estatico

## 2. Fuentes que mandan
1. `docs/Enunciado Taller.pdf`
2. `C:/Users/kevin/Downloads/Apunte Final del Curso.pdf`
3. `docs/apuntes/INDICE.md`
4. `docs/apuntes/02c-Analisis-Estatico.pdf`
5. `docs/apuntes/02d-Analisis-Dinamico-Modal-Espectral.pdf`
6. `docs/Material taller/Material Apoyo Taller 2026.pdf`
7. `docs/Normas Utilizadas ADSE/NCh0433-1996-Mod.2009.pdf`
8. `docs/Normas Utilizadas ADSE/DECRETO 61 2011 DISEÑO SISMICO DE EDIFICIOS.pdf`
9. `docs/Normas Utilizadas ADSE/NCh 3171- 2017.pdf`

## 3. Puntos de criterio ya fijados

### 3.1 Cosas que NO hay que mezclar con Edificio 1
- No usar la matriz de 6 casos de Edificio 1.
- No abrir una rama semirigida como parte oficial de Edificio 2.
- No convertir Parte 1 en un flujo modal espectral principal.

### 3.2 Cosas que SI hay que hacer en Edificio 2
- Modelar con diafragma rigido.
- Correr analisis modal para masas equivalentes y `Tx`, `Ty`, `Tz`.
- Resolver la Parte 1 con metodo estatico.
- Ingresar explicitamente los 19 estados de carga del metodo estatico.

### 3.3 Nota importante sobre nomenclatura
En apuntes y material de apoyo, Music usa:
- `CP` = cargas permanentes
- `L` = sobrecarga de piso
- `Lr` = sobrecarga de techo
- `SDX`, `SDY` = sismo estatico aplicado en centro de masa
- `TEX`, `TEY` = torsion accidental estatica aplicada en centro de masa

Para no pelear ni con el taller ni con el paquete tecnico, usa esta regla:
- en informe, planilla y explicacion oral puedes mantener la notacion del curso (`SDX`, `SDY`)
- en el modelo ETABS conviene usar la nomenclatura del paquete activo:
  - `EX`, `EY`, `TEX`, `TEY`

Mapeo recomendado:
- `CP = PP + TERP + TERT`
- `L = SCP`
- `Lr = SCT`
- `SDX` del curso = `EX` en ETABS/modelo tecnico
- `SDY` del curso = `EY` en ETABS/modelo tecnico

Regla operativa:
- si quieres interoperar luego con el paquete `ed2`, usa `EX`, `EY`, `TEX`, `TEY`
- si en el informe nombras `SDX` o `SDY`, explicita esa equivalencia una sola vez

## 4. Datos base del edificio
Fuente: `docs/Enunciado Taller.pdf`, pp. 8-10

### 4.1 Geometria y sistema
- 5 pisos
- uso: oficinas
- ubicacion: Antofagasta
- suelo de fundacion: tipo C
- sistema resistente: marcos de hormigon armado
- planta: 32.5 m x 32.5 m
- grilla: 6 x 6
- vanos: 6.5 m en ambas direcciones
- altura piso 1: 3.5 m
- altura pisos 2-5: 3.0 m
- altura total: 15.5 m
- base: empotrada

### 4.2 Secciones
- losa: 17 cm en todos los pisos
- columnas pisos 1-2: 70 x 70 cm
- columnas pisos 3-5: 65 x 65 cm
- vigas pisos 1-2: 50 x 70 cm
- vigas pisos 3-5: 45 x 70 cm

### 4.3 Materiales
- hormigon: G25
- acero: A630-420H
- peso especifico del hormigon armado: 2.5 tonf/m3
- peso especifico barras: 7.85 tonf/m3
- `Ec = 4700 * sqrt(fc')`
- `Es = 2.100.000 kgf/cm2`
- usar `g = 9.81 m/s2`

### 4.4 Cargas de area
- pisos:
  - terminaciones: 140 kgf/m2
  - sobrecarga: 300 kgf/m2
- techo:
  - terminaciones: 100 kgf/m2
  - sobrecarga techo: 100 kgf/m2

### 4.5 Cachos rigidos
- usar opcion automatica
- factor 0.75

## 5. Entregables que esta guia debe ayudarte a producir

### 5.1 Primera entrega
- modelo ETABS de Edificio 2
- analisis modal
- tabla de modos, masas equivalentes y periodos
- conclusion de `Tx`, `Ty`, `Tz`
- modos necesarios para llegar al 90% de `Mnx`, `Mny`, `Mnteta`

### 5.2 Parte 1 del enunciado
- modelo 3D y planta
- tabla de cargas y estados de carga
- `W` y `W/area`
- `Tx*`, `Ty*`, `Tz*`
- `C`, `Cmin`, `Cmax`
- `Vdx`, `Vdy`
- tabla de `Fk` y `Mtk` por piso
- graficos/tablas de `V(z)` y `Mvolcante(z)`
- drift y comentario

### 5.3 Dejar preparado el terreno para Parte 2
- marco del eje A correctamente modelado
- combinaciones gravitacionales y sismicas listas
- resultados de momentos accesibles en vigas del eje A

## 6. Flujo recomendado en ETABS 21

## Fase 0 - Preflight
Antes de modelar:
- trabajar en `Tonf, m, C`
- dejar claro el nombre del archivo `.edb`
- crear una carpeta local donde guardar:
  - capturas
  - tablas exportadas
  - planilla de calculo manual

## Fase 1 - Crear el modelo

### 1.1 Nuevo modelo
Ruta:
- `File > New Model`

Configuracion:
- Units: `Tonf, m, C`
- Template: `Grid Only`

### 1.2 Grilla y pisos
- X Grids: 6
- Y Grids: 6
- Spacing X: 6.5 m
- Spacing Y: 6.5 m
- Stories: 5
- Bottom Story Height: 3.5 m
- Typical Story Height: 3.0 m

## Fase 2 - Materiales y secciones

### 2.1 Materiales
Ruta:
- `Define > Material Properties`

Crear o revisar:
- hormigon `G25`
- acero `A630-420H`

### 2.2 Secciones de columnas
Ruta:
- `Define > Section Properties > Frame Sections`

Crear:
- `C70x70G25`
- `C65x65G25`

### 2.3 Secciones de vigas
Crear:
- `V50x70G25`
- `V45x70G25`

### 2.4 Losa
Ruta:
- `Define > Section Properties > Slab Sections`

Crear:
- `L17G25`

## Fase 3 - Dibujar la estructura

### 3.1 Columnas
- dibujar columnas en todas las intersecciones de la grilla
- asignar:
  - pisos 1-2: `C70x70G25`
  - pisos 3-5: `C65x65G25`

### 3.2 Vigas
- dibujar vigas en todas las lineas de grilla y todos los vanos
- asignar:
  - pisos 1-2: `V50x70G25`
  - pisos 3-5: `V45x70G25`

### 3.3 Losas
- dibujar 25 paneles por piso
- asignar `L17G25`

### 3.4 Apoyos
- empotrar la base

## Fase 4 - Asignaciones obligatorias del modelo

### 4.1 Diafragma
Ruta:
- `Define > Diaphragms`
- crear `D1`

Asignar:
- seleccionar todas las losas
- ejecutar `Assign > Shell > Diaphragms`
- en el formulario `Shell Assignment - Diaphragms`, elegir `D1`

Decision de taller:
- Edificio 2 se trabaja con diafragma rigido
- no abrir una rama semirigida para la Parte 1 oficial

### 4.2 Cardinal Point de vigas
Para reproducir el paquete tecnico vigente:
- usar `Cardinal Point = 8 Top Center`

Razon:
- son vigas normales, no invertidas
- la cara superior de la viga queda al nivel de la losa

### 4.3 Rigid End Zones
Ruta:
- `Assign > Frame > End Length Offsets`

Usar:
- `Automatic from Connectivity`
- `Rigid Zone Factor = 0.75`

### 4.4 Property Modifiers
Estos valores no vienen detallados en el enunciado ni en el material de apoyo como
exigencia textual del taller. Quedan aqui publicados porque hoy son parte del modelo
tecnico vigente del paquete `ed2` y, si se omiten, la guia UI y el paquete tecnico dejan
de reproducir lo mismo.

Lectura correcta:
- son supuestos de modelacion del paquete activo
- no son una frase literal del enunciado
- si Music fija otro criterio de rigidez efectiva en sala, esa aclaracion manda

Nota CSI oficial:
- ETABS permite definir los modifiers en la propiedad de la seccion o como asignacion
  al objeto, pero no conviene hacer ambas cosas a la vez.
- En esta guia se recomienda dejarlos definidos en la propiedad de la seccion para que
  queden consistentes desde el origen.

#### Columnas
- `I22 = 0.70`
- `I33 = 0.70`
- `J = 1.0`

#### Vigas
- `I22 = 0.35`
- `I33 = 0.35`
- `J = 0.0`

#### Losas
- `m11 = 0.25`
- `m22 = 0.25`
- `m12 = 0.25`

## Fase 5 - Patrones de carga gravitacionales

### 5.1 Definir patrones
Ruta:
- `Define > Load Patterns`

Crear:
- `PP`
- `TERP`
- `TERT`
- `SCP`
- `SCT`

Configuracion sugerida:
- `PP`: tipo Dead, Self Weight Multiplier = 1
- `TERP`: tipo Super Dead, SWM = 0
- `TERT`: tipo Super Dead, SWM = 0
- `SCP`: tipo Live, SWM = 0
- `SCT`: tipo Roof Live, SWM = 0

### 5.2 Asignar cargas de area

#### Pisos 1 a 4
- `TERP = 0.140 tonf/m2`
- `SCP = 0.300 tonf/m2`

#### Techo
- `TERT = 0.100 tonf/m2`
- `SCT = 0.100 tonf/m2`

## Fase 6 - Fuente de masa y analisis modal

### 6.1 Fuente de masa
Ruta:
- `Define > Mass Source`

Criterio operativo del paquete actual:
- `PP = 1.0`
- `TERP = 1.0`
- `TERT = 1.0`
- `SCP = 0.25`
- `SCT = 0.25`

Nota:
- esto debe quedar explicitado en el informe
- si Music fija otra convencion de `SCT` en sala o ayudantia, esa aclaracion manda

### 6.2 Caso modal
Ruta:
- `Define > Modal Cases`

Crear o revisar:
- `Modal`

Parametros:
- tipo: Modal
- metodo: Eigen
- suficientes modos para llegar al 90% de `Mnx`, `Mny`, `Mnteta`

Nota CSI oficial:
- ETABS crea automaticamente un caso modal eigen al iniciar un modelo nuevo.
- Aun asi, conviene revisarlo o redefinirlo explicitamente para dejar documentado el
  numero de modos y el nombre del caso.

### 6.3 Que sacar del modal
Exportar tabla donde aparezcan:
- modos
- periodos
- `Mnx/M`
- `Mny/M`
- `Mnteta/J`

Concluir:
- `Tx*`
- `Ty*`
- `Tz*`
- numero de modos necesarios para cumplir el 90%

Fuente fuerte:
- `Apunte Final del Curso.pdf`, p. 44

## Fase 7 - Calculo estatico fuera de ETABS

### 7.1 Regla central
No usar el auto lateral load chileno de ETABS como solucion oficial.

Music deja claro que:
- el metodo estatico se calcula a mano
- luego se ingresa al modelo

### 7.2 Peso sismico
Armar planilla para:
- `W`
- `W/area`

### 7.3 Coeficiente sismico
Calcular:
- `C`
- `Cmin`
- `Cmax`

Usar:
- `Ao = 0.4g`
- suelo `C`
- `S = 1.05`
- `T' = 0.45 s`
- `n = 1.40`
- `I = 1.0`
- `R = 7`

Y verificar:
- si `C < Cmin`, usar `Cmin`
- si `C > Cmax`, usar `Cmax`

### 7.4 Corte basal
Calcular por direccion:
- `Qo = C * I * P`

### 7.5 Distribucion por piso
Para Edificio 2, usar la formulacion de edificios de no mas de 5 pisos:
- `Fk = (Ak * Pk / sum(Aj * Pj)) * Qo`
- `Ak = sqrt(1 - Z(k-1)/H) - sqrt(1 - Zk/H)`

### 7.6 Torsion accidental estatica
Para cada piso:
- `ea_k = 0.10 * bk * (Zk/H)`
- `Mt_k = Fk * ea_k`

Regla fisica:
- si el sismo es en X, la excentricidad accidental se toma en Y
- si el sismo es en Y, la excentricidad accidental se toma en X

Fuente fuerte:
- clase Music curada
- `Apunte Final del Curso.pdf`, p. 103
- `docs/Material taller/Material Apoyo Taller 2026.pdf`, pp. 38-39

## Fase 8 - Cargar el metodo estatico en ETABS 21

### 8.1 Patrones sismicos recomendados
Crear:
- `EX`
- `EY`
- `TEX`
- `TEY`

Configuracion:
- Type: Seismic
- Self Weight Multiplier: 0
- Auto Lateral Load: opcion de cargas sismicas de usuario sobre diafragmas
  - segun build, puede verse como `User Defined` o texto equivalente

Nota CSI oficial:
- En ETABS 21, el formulario correcto para ingresar `Fx`, `Fy` y `Mz` por diafragma es
  `User Seismic/Wind Loads on Diaphragms`.
- Se accede desde `Define > Load Patterns`, creando el patron con `Type = Seismic` y
  luego `Modify Lateral Load`.

### 8.2 Cargar `EX` y `EY`
Hay dos formas razonables:

#### Opcion recomendada
- definir `EX` y `EY` como patrones sismicos manuales
- ingresar las fuerzas por piso que ya calculaste en la planilla
- usar `Modify Lateral Load`
- marcar `Apply Load at Diaphragm Center of Mass`
- para `EX`, pegar valores en la columna `Fx` por piso y dejar `Fy = 0`, `Mz = 0`
- para `EY`, pegar valores en la columna `Fy` por piso y dejar `Fx = 0`, `Mz = 0`

#### Regla importante
- el valor oficial lo pone tu planilla, no el auto lateral load chileno de ETABS

### 8.3 Cargar `TEX` y `TEY`
Esto si queda bien definido en el material de apoyo:

Ruta:
- `Define > Load Patterns`
- Type = Seismic
- Self Weight Multiplier = 0
- Auto Lateral Load = opcion de cargas sismicas de usuario sobre diafragmas

Luego:
- `Modify Lateral Load`
- marcar `Apply Load at Diaphragm Center of Mass`
- pegar los `Mz` por piso en la columna `Mz`
- dejar `Fx = 0`
- dejar `Fy = 0`

Nota UI:
- en ETABS 21, manten el mismo criterio que en `EX` y `EY`:
  - `Type = Seismic`
- evita pelearte con la etiqueta exacta del build; lo importante es que abra el formulario
  oficial `User Seismic/Wind Loads on Diaphragms`

Fuente:
- `docs/Material taller/Material Apoyo Taller 2026.pdf`, pp. 38-39

### 8.4 Nota sobre nombres
En el modelo UI conviene usar:
- `EX`, `EY`, `TEX`, `TEY`

En el informe puedes aclarar una sola vez:
- `EX = SDX`
- `EY = SDY`

## Fase 9 - Combinaciones de carga

### 9.1 Regla del curso
Cuando se aplica metodo estatico, Music muestra 19 combinaciones a ingresar a ETABS.

Fuente fuerte:
- `C:/Users/kevin/Downloads/Apunte Final del Curso.pdf`, p. 103
- `docs/Material taller/Material Apoyo Taller 2026.pdf`, p. 42

Nota CSI oficial:
- estas combinaciones deben crearse como `user-defined load combinations`
- ruta: `Define > Load Combinations`
- no conviene depender de combinaciones automaticas de diseño para este taller, porque
  ETABS las regenera y pueden no coincidir con la familia exacta que Music exige

### 9.2 Combinaciones
Usa exactamente esta familia.

Si quieres compatibilidad con el paquete tecnico y con `verify_ed2.py`, crea las
combinaciones con estos nombres. Entre parentesis se deja la equivalencia visual con
`COMBO 1` a `COMBO 19` del material de apoyo.

#### Gravitacionales
1. `C1 (COMBO 1) = 1,4CP`
2. `C2 (COMBO 2) = 1,2CP + 1,6L + 0,5Lr`
3. `C3 (COMBO 3) = 1,2CP + L + 1,6Lr`

#### X
4. `C4_XP_TP (COMBO 4) = 1,2CP + L + 1,4EX + 1,4TEX`
5. `C4_XN_TP (COMBO 5) = 1,2CP + L - 1,4EX + 1,4TEX`
6. `C4_XP_TN (COMBO 6) = 1,2CP + L + 1,4EX - 1,4TEX`
7. `C4_XN_TN (COMBO 7) = 1,2CP + L - 1,4EX - 1,4TEX`
8. `C5_XP_TP (COMBO 8) = 0,9CP + 1,4EX + 1,4TEX`
9. `C5_XN_TP (COMBO 9) = 0,9CP - 1,4EX + 1,4TEX`
10. `C5_XP_TN (COMBO 10) = 0,9CP + 1,4EX - 1,4TEX`
11. `C5_XN_TN (COMBO 11) = 0,9CP - 1,4EX - 1,4TEX`

#### Y
12. `C6_YP_TP (COMBO 12) = 1,2CP + L + 1,4EY + 1,4TEY`
13. `C6_YN_TP (COMBO 13) = 1,2CP + L - 1,4EY + 1,4TEY`
14. `C6_YP_TN (COMBO 14) = 1,2CP + L + 1,4EY - 1,4TEY`
15. `C6_YN_TN (COMBO 15) = 1,2CP + L - 1,4EY - 1,4TEY`
16. `C7_YP_TP (COMBO 16) = 0,9CP + 1,4EY + 1,4TEY`
17. `C7_YN_TP (COMBO 17) = 0,9CP - 1,4EY + 1,4TEY`
18. `C7_YP_TN (COMBO 18) = 0,9CP + 1,4EY - 1,4TEY`
19. `C7_YN_TN (COMBO 19) = 0,9CP - 1,4EY - 1,4TEY`

### 9.3 Nota sobre un typo del apunte
En algunos derivados aparece en una fila Y la combinacion con `TEX`.
Por simetria de la familia y por consistencia fisica, para la familia Y se debe leer `TEY`.

### 9.4 Combinaciones de servicio para drift
Si quieres dejar el modelo manual alineado con el paquete `ed2`, crea ademas estas 8
combinaciones de servicio:

- `DRIFT_XP_TP = 1,0EX + 1,0TEX`
- `DRIFT_XP_TN = 1,0EX - 1,0TEX`
- `DRIFT_XN_TP = -1,0EX + 1,0TEX`
- `DRIFT_XN_TN = -1,0EX - 1,0TEX`
- `DRIFT_YP_TP = 1,0EY + 1,0TEY`
- `DRIFT_YP_TN = 1,0EY - 1,0TEY`
- `DRIFT_YN_TP = -1,0EY + 1,0TEY`
- `DRIFT_YN_TN = -1,0EY - 1,0TEY`

Uso:
- estas no reemplazan las 19 combinaciones resistentes
- sirven para revisar drift con sismo principal y torsion accidental sin factores LRFD

## Fase 10 - Correr y revisar el analisis

### 10.1 Correr
- guardar `.edb`
- correr analisis

### 10.2 Chequeos minimos inmediatos
- `Analyze > Last Analysis Run Log`
  - debe terminar en `Analysis Complete`
- revisar los primeros modos
  - traslacion en X
  - traslacion en Y
  - rotacion en Z
- revisar que no haya elementos sueltos

## Fase 11 - Extraer resultados para la entrega

### 11.1 Periodos y masas equivalentes
Ruta:
- ejecutar `Display > Show Tables`
- en el formulario `Choose Tables`, elegir la tabla modal correspondiente

Entregar:
- tabla ETABS
- conclusion de `Tx*`, `Ty*`, `Tz*`
- cantidad de modos hasta 90%

### 11.2 Peso sismico
Entregar:
- `W`
- `W/area`

Si quieres contraste del modelo:
- ejecutar `Display > Show Tables`
- en `Choose Tables`, elegir `Base Reactions`
- revisar el combo gravitacional

Chequeo de sanidad:
- el `W/area` debe quedar en un orden razonable para un edificio de HA de estas
  caracteristicas
- en el material ETABS de apoyo aparece como referencia practica un valor del orden de
  `~1 tonf/m2`

### 11.3 Fuerzas por piso y torsion accidental
Esto sale de tu planilla estatica, no de improvisar sobre resultados de ETABS.

Entregar:
- tabla por piso con `Fk`
- tabla por piso con `Mt`
- indicar que estados de carga se consideran

### 11.4 Esfuerzo de corte en altura
Ruta recomendada:
- ejecutar `Display > Show Tables`
- en `Choose Tables`, seleccionar `Analysis Results > Structure Output > Other Output Items > Story Forces`

Filtrar:
- caso o combinacion de interes

Leer:
- `Vx` para sismo X
- `Vy` para sismo Y

Armar:
- tabla por piso
- grafico `V(z)` en ambas direcciones

Ruta alternativa valida:
- `Display > Combined Story Response Plots`
- sirve para revisar rapido la forma del corte en altura, pero para entrega conviene guardar
  tambien la tabla

Fuente:
- `docs/Material taller/Material Apoyo Taller 2026.pdf`, p. 36
- CSI User's Guide: `Display > Show Tables` y `Display > Combined Story Response Plots` son rutas oficiales para obtener tablas y graficos globales por piso

### 11.5 Momento volcante en altura
Primer camino:
- usar la tabla `Story Forces` si tu build de ETABS 21 muestra directamente los momentos globales por piso

Si tu tabla no lo deja limpio:
- definir `Section Cuts` por piso
- extraer el momento acumulado por nivel

Armar:
- tabla por piso
- grafico `Mvolcante(z)` en ambas direcciones

### 11.6 Drift - condicion 1 y condicion 2

#### Condicion 1
Usar:
- ejecutar `Display > Show Tables`
- en `Choose Tables`, elegir `Joint Drifts`

Procedimiento:
- elegir un nodo cercano al centro de masa
- leer `Drift X` o `Drift Y`
- verificar `drift_CM <= 0.002`

#### Condicion 2
Usar:
- ejecutar `Display > Show Tables`
- en `Choose Tables`, elegir `Diaphragm Max Over Avg Drifts`

Procedimiento:
- para el mismo estado de carga, comparar el drift mas desfavorable de planta con el drift del punto cercano al CM
- reporta siempre ambos valores:
  - `drift_CM`
  - `drift_max`
- para dejarte alineado con el material de apoyo y con el paquete activo, revisa el exceso
  torsional como:
  - `drift_max - drift_CM <= 0.001`

Notas:
- el material de apoyo muestra el uso conjunto de `Joint Drifts` y `Diaphragm Max Over Avg Drifts`
- si en correccion Music o ayudantia te piden expresarlo como drift extremo absoluto, muestra
  ademas el `Max Drift` directo de la tabla
- la conclusion debe comentar ambas disposiciones

Fuente:
- `docs/Material taller/Material Apoyo Taller 2026.pdf`, pp. 12-13

### 11.7 Centros de masa y rigidez
Si necesitas documentar excentricidades o revisar coherencia de la torsion accidental:

Ruta:
- `Display > Show Tables`
- buscar una tabla equivalente a `Centers of Mass and Rigidity`

Regla operativa:
- si tu build de ETABS 21 muestra la tabla, exportala y usala
- si el nombre cambia, usa el buscador interno de `Show Tables`
- si la tabla no aparece, no reemplaces `CR` con centro geometrico ni con tablas de masa
- para entrega del taller, es preferible declarar que esa tabla no quedo disponible en el
  build antes que inventar un `CR` espurio

## Fase 12 - Parte 2 en ETABS

### 12.1 Frame del eje A
Verificar que quede claro:
- eje A
- vigas del primer piso
- columnas del primer y segundo piso

### 12.2 Combinaciones utiles para Parte 2
Ademas de las 19 combinaciones del metodo estatico, deja identificadas:
- gravitacional:
  - `1,2D + 1,6L + 0,5Lr`
- sismo X para diseño de marco A:
  - `0,9D + 1,4E`
  - `0,9D - 1,4E`

### 12.3 Momento en vigas del eje A
Ruta:
- seleccionar vigas del eje A
- mostrar diagramas de momentos para los estados de carga requeridos

### 12.4 Codigo y preferencias de diseño
Ruta:
- `Design > Concrete Frame Design > View/Revise Preferences`

Revisar:
- codigo de diseño activo en la workstation
- preferencias relevantes antes de correr el diseño

Nota:
- aqui manda lo que efectivamente este adoptando el curso/laboratorio
- no cambies preferencias a ciegas; primero deja captura de lo que trae la instalacion

### 12.5 Seleccionar combinaciones de diseño
Ruta:
- `Design > Concrete Frame Design > Select Design Combos`

Uso minimo:
- en `Strength`, seleccionar las combinaciones resistentes que correspondan
- si el laboratorio usa otras combinaciones de servicio para revision adicional, dejarlas
  documentadas aparte

### 12.6 Correr diseño ETABS
Ruta:
- `Design > Concrete Frame Design > Start Design/Check of Structure`

Luego:
- revisar vigas del primer piso del eje A
- revisar columnas del primer y segundo piso del eje A

### 12.7 Extraer resultados de diseño
Ruta principal:
- `Design > Concrete Frame Design > Display Design Info`

Revisar como minimo:
- refuerzo longitudinal de vigas y columnas
- refuerzo de corte
- `PMM interaction ratios` en columnas
- relaciones viga-columna / columna-viga si el build las muestra
- detalles de torsion y nudo si aparecen en el display de diseño

Complemento:
- click derecho sobre el elemento con resultados visibles para entrar a revision mas detallada
- guarda capturas y tablas del eje A que realmente vas a reportar

## 7. Checklist final de entrega

### Modelo
- [ ] Edificio 2 modelado en ETABS 21
- [ ] diafragma rigido `D1`
- [ ] cachos rigidos `0.75`
- [ ] modifiers publicados y aplicados
- [ ] base empotrada

### Primera entrega
- [ ] analisis modal corrido
- [ ] tabla de modos y masas equivalentes
- [ ] `Tx`, `Ty`, `Tz`
- [ ] modos hasta 90%

### Parte 1
- [ ] `W`
- [ ] `W/area`
- [ ] `C`, `Cmin`, `Cmax`
- [ ] `Vdx`, `Vdy`
- [ ] tabla de `Fk`
- [ ] tabla de `Mt`
- [ ] grafico `V(z)` X
- [ ] grafico `V(z)` Y
- [ ] grafico `Mvolcante(z)` X
- [ ] grafico `Mvolcante(z)` Y
- [ ] drift y comentario

### Parte 2
- [ ] marco eje A identificable
- [ ] combinaciones utiles localizadas
- [ ] diagrama de momentos accesible
- [ ] codigo de diseño revisado
- [ ] design combos seleccionadas
- [ ] diseño ETABS corrido para marco A

## 8. Que no debe volver a aparecer en esta guia
- response spectrum como camino principal de Parte 1
- tabla de 6 casos de Edificio 1
- diafragma semirigido como exigencia oficial de Edificio 2
- flujo heredado de muros de Edificio 1

## 9. Criterio de cierre
Esta guia queda alineada si, al usarla, produces exactamente estas tres capas:
- primera entrega: modelo + modal de Edificio 2
- Parte 1: metodo estatico completo de Edificio 2
- Parte 2: diagrama de momentos + diseño ETABS revisable del marco del eje A

## 10. Alineacion oficial CSI usada en esta version
Esta version ya fue endurecida contra ayuda y manuales oficiales de CSI para ETABS:
- `Mass Source`
- `Load Patterns`
- `User Seismic/Wind Loads on Diaphragms`
- `Modal Cases`
- `End Length Offsets`
- `Diaphragms - Shells`
- `Frame Property Modifiers`
- `Shell Stiffness Modifiers`
- `Load Combinations`
- `Show Tables`
- `Combined Story Response Plots`
- `Concrete Frame Design`

En particular, se fijo explicitamente:
- uso del formulario oficial de cargas sismicas de usuario sobre diafragmas para `EX`, `EY`, `TEX`, `TEY`
- `Apply Load at Diaphragm Center of Mass` como opcion UI correcta al ingresar cargas en diafragma
- `Define > Modal Cases` como ruta oficial para revisar/definir el caso modal
- `Define > Load Combinations` como ruta oficial para las 19 combinaciones del taller
- regla CSI de no duplicar modifiers en propiedad y en asignacion simultaneamente
- `Display > Combined Story Response Plots` como ruta grafica oficial para corte/volcamiento por piso
- `Design > Concrete Frame Design > View/Revise Preferences`, `Select Design Combos`,
  `Start Design/Check of Structure` y `Display Design Info` como secuencia base de Parte 2
