# Guia Edificio 1 - ETABS 21 UI

> Taller ADSE UCN 1S-2026 - Edificio 1, muros de hormigon armado, 20 pisos.
> Guia orientada a modelacion manual por interfaz de usuario en ETABS 21.

## Estado del documento

- Fecha base: 2026-05-02.
- Software objetivo: ETABS Ultimate 21.2.0 o compatible ETABS 21.
- Metodo de trabajo: interfaz grafica, no pipeline OAPI.
- Documento historico base: `docs/estudio/GUIA-COMPLETA-EDIFICIO1-ETABS-v19.md`.
- Fuente geometrica activa: enunciado + modelo manual ETABS 21 + notas vivas en `taller-etabs/MODELADO_MANUAL_ED1_NOTAS.md`.
- Base normativa de defensa: `NCh433:2026` segun `docs/estudio/00-ESTADO-NORMATIVO-CURSO-2026.md`.

## Dictamen operativo

La guia v19 sirve como flujo de referencia, pero no debe usarse como canon final porque:

- estaba escrita para ETABS v19;
- conserva referencias a `NCh433:1996 Mod.2009 + DS61`;
- parte de la interpretacion geometrica anterior del Edificio 1 fue corregida manualmente;
- el modelo correcto debe salir de la planta manual revisada en ETABS 21.

Esta guia fija el flujo UI actualizado y separa lo que ya esta cerrado de lo que requiere validacion visual.

## Fuentes que mandan

1. `docs/Enunciado Taller.pdf`: geometria, grillas, cargas y alcance.
2. `docs/enunciado_page2.png` a `docs/enunciado_page7.png`: lectura visual de plantas y elevaciones.
3. `taller-etabs/MODELADO_MANUAL_ED1_NOTAS.md`: correcciones manuales vigentes.
4. `docs/Material taller/Material Apoyo Taller 2026.pdf`: drift, torsion, combinaciones, Section Cuts y lectura ETABS.
5. `docs/Material taller/Paso a Paso ETABS M.Lafontaine.pdf`: flujo manual ETABS.
6. `docs/apuntes/INDICE.md`: indice maestro del curso.
7. `docs/apuntes/02c-Analisis-Estatico.pdf`: metodo estatico y torsion.
8. `docs/apuntes/02d-Analisis-Dinamico-Modal-Espectral.pdf`: modal espectral, CQC, masas modales y drift.
9. `docs/apuntes/02e-Diseno-Edificios-R-Pushover.pdf`: R*, CM/CR y criterios de analisis.
10. `docs/Normas Utilizadas ADSE/NCh 3171- 2017.pdf`: combinaciones.
11. `docs/Normas Utilizadas ADSE/NCh1537- 2009 ... Cargas perman.pdf`: cargas.
12. `docs/Normas Utilizadas ADSE/DECRETO 60 2011 ... HORMIGON ARMADO.pdf` y ACI: diseno HA.

## Regla de oro

No usar `All Stories` mientras se dibuja la planta tipo.

Flujo correcto:

1. Dibujar y revisar `Story2`.
2. Completar muros X/Y, vigas, losas y vacios en `Story2`.
3. Guardar checkpoint.
4. Recien despues replicar a `Story1` y `Story3` a `Story19`.
5. Tratar `Story20` como techo distinto.

## 0. Convenciones del modelo

### Unidades

Usar:

- `tonf`
- `m`
- `C`

Ruta:

`Options > Display Units...`

### Nombre de archivo recomendado

Guardar por hitos:

- `ED1_01_Grilla_v01.edb`
- `ED1_02_Story2_MurosXY_v01.edb`
- `ED1_03_Story2_Vigas_v01.edb`
- `ED1_04_Story2_Losas_v01.edb`
- `ED1_05_Story2_Verificado_v01.edb`
- `ED1_06_PisosTipo_Replicados_v01.edb`
- `ED1_07_Techo_v01.edb`
- `ED1_08_Cargas_Masa_v01.edb`
- `ED1_09_Analisis_v01.edb`

## 1. Crear modelo y grillas

### 1.1 Nuevo modelo

Ruta:

`File > New Model`

Configuracion inicial:

- Units: `Tonf, m, C`.
- Template: `Grid Only` o `Blank` + grilla manual.
- Number of Stories: `20`.
- Typical Story Height: `2.6 m`.
- Bottom Story Height: `3.4 m`.

Alturas esperadas:

| Piso | Altura |
| --- | ---: |
| Story1 | 3.40 m |
| Story2 a Story20 | 2.60 m |

### 1.2 Grilla X actual

Ingresar como coordenadas absolutas, no como espaciamientos.

| Grid ID | X (m) | Visible | Bubble Loc |
| --- | ---: | --- | --- |
| 1 | 0.000 | Yes | End |
| 2 | 3.125 | Yes | End |
| Aux1 | 3.675 | Yes | End |
| 3 | 3.825 | Yes | End |
| Aux2 | 5.325 | Yes | End |
| Aux3 | 8.345 | Yes | End |
| 4 | 9.295 | Yes | End |
| 5 | 9.895 | Yes | End |
| Aux4 | 11.445 | Yes | End |
| Aux5 | 13.865 | Yes | End |
| Aux6 | 15.265 | Yes | End |
| 6 | 15.465 | Yes | End |
| 7 | 16.015 | Yes | End |
| Aux7 | 17.415 | Yes | End |
| Aux8 | 17.620 | Yes | End |
| 8 | 18.565 | Yes | End |
| 9 | 18.990 | Yes | End |
| Aux9 | 19.510 | Yes | End |
| 10 | 21.665 | Yes | End |
| Aux10 | 21.865 | Yes | End |
| Aux11 | 23.264 | Yes | End |
| 11 | 24.990 | Yes | End |
| Aux12 | 25.115 | Yes | End |
| 12 | 26.315 | Yes | End |
| 13 | 27.834 | Yes | End |
| Aux13 | 30.885 | Yes | End |
| Aux14 | 31.804 | Yes | End |
| 14 | 32.435 | Yes | End |
| Aux15 | 33.252 | Yes | End |
| Aux16 | 33.955 | Yes | End |
| 15 | 34.005 | Yes | End |
| 16 | 37.130 | Yes | End |
| 17 | 38.505 | Yes | End |

Nota: si en ETABS ya se ingreso `Aux 12` con espacio, no rehacer la grilla solo por eso. Para la guia se normaliza como `Aux12`.

### 1.3 Grilla Y actual

| Grid ID | Y (m) | Visible | Bubble Loc |
| --- | ---: | --- | --- |
| A | 0.000 | Yes | Start |
| B | 0.701 | Yes | Start |
| aux1 | 3.271 | Yes | Start |
| C | 6.446 | Yes | Start |
| D | 7.996 | Yes | Start |
| aux2 | 8.371 | Yes | Start |
| E | 10.716 | Yes | Start |
| F | 13.821 | Yes | Start |

Nota: en Y se mantiene `aux1` y `aux2` en minuscula si ya quedaron asi en ETABS. Lo importante es la coordenada, no el estilo del nombre.

### 1.4 Ajuste visual de grillas

Para bajar saturacion visual:

Ruta:

`Edit > Edit Stories and Grid Systems... > Modify/Show Grid System...`

Recomendado:

- `Bubble Size = 0.50`.
- Si sigue saturado: `0.35`.
- No bajar de `0.25` salvo para captura muy alejada.

Para mantener cotas pero reducir texto:

`Options > Graphics Preferences...`

- `Maximum Graphic Font Size = 5` o `6`.
- `Minimum Graphic Font Size = 2`.

Para limpiar temporalmente:

`View > Set Display Options...`

Apagar:

- `Dimension Lines` si molestan.
- `Story Labels`.
- `Architectural Plan Layers` si tapa.
- `Slab Rebar`.
- `Design Strips`.
- `Tendons`.

Mantener:

- `Joint Objects`.
- `Beams`.
- `Floors`.
- `Walls`.
- `Openings`.
- `Object Edge`.

## 2. Materiales

### 2.1 Hormigon G30

Ruta:

`Define > Material Properties... > Add New Material...`

Crear material:

| Campo | Valor |
| --- | --- |
| Material Name | `G30` |
| Material Type | `Concrete` |
| Weight per Unit Volume | `2.5 tonf/m3` |
| Poisson | `0.20` |
| f'c | `3000 tonf/m2` segun convencion del curso |

Modulo elastico:

```text
Ec = 4700 sqrt(f'c[MPa])
f'c = 30 MPa
Ec = 25743 MPa
```

En `tonf/m2`, usar el valor ya configurado de forma consistente en el modelo. Si se usa conversion exacta desde MPa, queda del orden de `2.62e6 tonf/m2`. Si se usa la simplificacion del enunciado, queda del orden de `2.57e6 tonf/m2`. No mezclar convenciones dentro del mismo modelo.

### 2.2 Acero A630-420H

Ruta:

`Define > Material Properties... > Add New Material...`

Crear material:

| Campo | Valor |
| --- | --- |
| Material Name | `A630-420H` |
| Material Type | `Rebar` |
| Weight per Unit Volume | `7.85 tonf/m3` |
| E | `20387400 tonf/m2` |
| Poisson | `0.000117 1/C` si se usa coeficiente termico del set previo |
| fy | `42814 tonf/m2` |
| fu | `64220 tonf/m2` |
| fye | `46402.6 tonf/m2` |
| fue | `69603.89 tonf/m2` |

Grado ETABS:

- Si ETABS pide `Grade`: usar `Grade 60` como plantilla y reemplazar datos por A630-420H.

## 3. Secciones

Fuente principal para esta fase:

- `docs/Material taller/Paso a Paso ETABS M.Lafontaine.pdf`, pp. 21-27.
- Criterio: vigas y columnas como `frame`; muros y losas como `shell`; precaucion con la interaccion frame-shell.

### 3.1 Muros MHA30G30 y MHA20G30

Ruta:

`Define > Section Properties > Wall Sections...`

Crear:

| Property Name | Material | Modeling Type | Thickness |
| --- | --- | --- | ---: |
| `MHA30G30` | `G30` | `Shell-Thin` | 0.30 m |
| `MHA20G30` | `G30` | `Shell-Thin` | 0.20 m |

Modifiers:

- Mantener todos en `1.0` salvo instruccion expresa del profesor.
- Mass = `1.0`.
- Weight = `1.0`.

### 3.2 Vigas invertidas VI20x60G30

Fuente directa:

- `Paso a Paso ETABS M.Lafontaine.pdf`, p. 23.
- El material recomienda usar `J = 0` en vigas (`Torsional Constant`).

Ruta:

`Define > Section Properties > Frame Sections...`

Crear:

| Campo | Valor |
| --- | --- |
| Property Name | `VI20x60G30` |
| Shape | Concrete Rectangular |
| Material | `G30` |
| Depth t3 | `0.60 m` |
| Width t2 | `0.20 m` |

Modifiers:

| Modifier | Valor |
| --- | ---: |
| Cross-section Area | 1 |
| Shear Area 2 | 1 |
| Shear Area 3 | 1 |
| Torsional Constant J | 0 |
| Moment of Inertia about 2 axis | 1 |
| Moment of Inertia about 3 axis | 1 |
| Mass | 1 |
| Weight | 1 |

Nota: `J=0` no significa viga articulada. Solo reduce torsion espuria. La continuidad flexural se controla con `Moment Releases`.

### 3.3 Losa15G30

Fuente directa:

- `Paso a Paso ETABS M.Lafontaine.pdf`, pp. 26-27.
- Si la losa se modela como membrana, la carga se reparte por criterio geometrico y no por rigidez; usarlo solo en panos rectangulares y verificando descarga.
- Para losa shell, el material recomienda reducir la inercia a flexion a 25%. Mantener 100% sobrestima acoplamiento/rigidez lateral; reducir demasiado subestima acoplamiento.

Ruta:

`Define > Section Properties > Slab Sections...`

Crear:

| Campo | Valor |
| --- | --- |
| Section Name | `Losa15G30` |
| Material | `G30` |
| Modeling Type | `Shell-Thin` |
| Slab Type | `Slab` |
| Thickness | `0.15 m` |

Modifiers recomendados:

| Modifier | Valor |
| --- | ---: |
| f11 | 1 |
| f22 | 1 |
| f12 | 1 |
| m11 | 0.25 |
| m22 | 0.25 |
| m12 | 0.25 |
| v13 | 1 |
| v23 | 1 |
| Mass | 1 |
| Weight | 1 |

## 4. Dibujo de planta tipo Story2

Fuente principal:

- `Paso a Paso ETABS M.Lafontaine.pdf`, pp. 51-54.
- Orden recomendado: elementos verticales primero, luego vigas y finalmente losas.

### 4.1 Preparacion

Antes de dibujar:

- Vista activa: `Plan View - Story2`.
- Dropdown inferior derecho: `One Story`.
- Modelo desbloqueado.
- Snaps activos.
- `Joint Objects` visibles.
- No usar `All Stories`.

### 4.2 Muros

Ruta ideal:

`Draw > Draw Floor/Wall Objects > Draw Walls (Plan)`

No usar para muros:

- `Quick Draw Walls (Plan)` mientras la geometria no este cerrada.
- `Draw Floor/Wall (Plan, Elev, 3D)` si solo muestra `Losa15G30`.

Propiedades:

- Muros 30 cm: `MHA30G30`.
- Muros 20 cm: `MHA20G30`.

Regla de conectividad:

- Lo que manda es la centrolinea del objeto.
- Si dos muros se cruzan o llegan a un punto, sus centrolineas deben llegar al mismo nodo/eje.
- Que los bordes rojos se toquen graficamente no basta.
- Si queda "casi" tocando, borrar y redibujar con snap.

### 4.3 Muros direccion Y cerrados por ahora

Lista operativa corregida para `Story2`:

| Eje X | Tramo Y | Seccion |
| --- | --- | --- |
| 1 | B -> C | MHA30G30 |
| 2 | B -> aux1 | MHA20G30 |
| 3 | D -> F | MHA30G30 |
| 4 | A -> C | MHA30G30 |
| 5 | D -> F | MHA30G30 |
| 6 | B -> aux1 | MHA20G30 |
| 7 | D -> F | MHA30G30 |
| 8 | B -> C | MHA20G30 |
| 9 | aux2 -> E | MHA20G30 |
| 10 | B -> aux1 | MHA20G30 |
| 11 | aux2 -> E | MHA20G30 |
| 12 | D -> F | MHA30G30 |
| 13 | A -> C | MHA30G30 |
| 14 | D -> F | MHA30G30 |
| 15 | B -> aux1 | MHA20G30 |
| 16 | B -> C | MHA30G30 |
| 17 | D -> F | MHA30G30 |

### 4.4 Muros direccion X

Estado: deben seguirse desde la planta del enunciado y el modelo manual.

Criterio:

- Dibujar tramo por tramo.
- No cruzar shaft o vacios.
- Cortar en intersecciones importantes si ayuda a lectura.
- Verificar propiedad `MHA20G30` o `MHA30G30` con click derecho.

Antes de pasar a vigas:

- todos los muros X/Y deben estar en `Story2`;
- no deben existir duplicados;
- los muros deben quedar como `Wall/Area Object`;
- propiedades correctas;
- centrolineas conectadas.

Checkpoint:

`File > Save As... > ED1_02_Story2_MurosXY_v01.edb`

## 5. Vigas invertidas

### 5.1 Herramienta correcta

Ruta:

`Draw > Draw Beam/Column/Brace Objects > Draw Beam/Column/Brace`

No usar:

- `Quick Draw Beams/Columns`.
- `Quick Draw Secondary Beams`.

Propiedades al dibujar:

| Campo | Valor |
| --- | --- |
| Type of Line | `Frame` |
| Property | `VI20x60G30` |
| Plan Offset Normal | `0` |
| Line Drawing Type | Straight line |

### 5.2 Continuous vs Pinned

Fuente directa:

- `Paso a Paso ETABS M.Lafontaine.pdf`, p. 64.
- Criterio del material: usualmente las vigas que comienzan o terminan al lado debil de un muro se rotulan; esto no es necesario si en el diseno se verifica que el muro puede tomar el momento negativo.

En ETABS:

- `Continuous` = sin release de momento.
- `Pinned` = libera momento en extremos.

Regla base:

- Si el plano/marca dice `C`: `Continuous`.
- Si el plano/marca dice `P`: articulado en ese extremo.
- Si el extremo llega al lado debil de un muro y el profesor/plano lo marco como rotula: `Pinned` en ese extremo.
- Si no hay marca ni simbolo de articulacion, no asumir `Pinned`.
- Si se decide no rotular un extremo en lado debil, debe quedar defendido despues en diseno: el muro debe poder tomar el momento negativo.

Viga que pasa por varios muros:

- No dibujar una sola viga larga atravesando muros.
- Dibujar por tramos:

```text
muro - viga - muro - viga - muro
```

Si debe ser continua en el muro intermedio, los dos tramos quedan sin release en ese nodo.

### 5.3 Como dibujar tramos

Para una viga entre tres muros:

1. Click en centrolinea del primer muro.
2. Click en centrolinea del muro intermedio.
3. Se crea tramo 1.
4. Click en el mismo punto intermedio.
5. Click en centrolinea del siguiente muro.
6. Se crea tramo 2.

Tambien se puede:

1. Dibujar tramo 1.
2. Click derecho o `Esc`.
3. Dibujar tramo 2 desde el mismo nodo.

Ambos son equivalentes si el snap toma exactamente el mismo punto.

### 5.4 Tramos con releases mixtos

Si un tramo es `C-C`:

- Dibujar con `Moment Releases = Continuous`.

Si un tramo es `P-P`:

- Se puede dibujar con `Moment Releases = Pinned`.

Si un tramo es `P-C` o `C-P`:

1. Dibujar como `Continuous`.
2. Seleccionar la viga.
3. Ir a `Assign > Frame > Releases/Partial Fixity...`.
4. Liberar solo el extremo marcado `P`.
5. Liberar `M2` y `M3`.
6. No liberar `P`, `V2`, `V3`.

Para identificar extremo `I` y `J`:

- el extremo inicial dibujado suele ser `I`;
- el extremo final suele ser `J`;
- confirmar con click derecho o mostrando ejes locales.

### 5.5 Viga invertida

Fuente directa:

- `docs/Material taller/Paso a Paso ETABS M.Lafontaine.pdf`, pp. 57-60.
- En esas paginas se indica que el punto de insercion sirve para modelar vigas invertidas de modo que el eje quede en el fondo de la viga.

Despues de dibujar todas las vigas `VI20x60G30`:

1. Seleccionar todas las vigas:
   `Select > Properties > Frame Sections... > VI20x60G30`.
2. Ir a:
   `Assign > Frame > Insertion Point...`.
3. Configurar:
   - `Cardinal Point = 2 - Bottom Center`.
   - Mantener marcada la casilla `Do not transform frame stiffness for offsets from centroid`.
   - Offsets `End-I` y `End-J` en `0`.
4. OK.

Esto modela la viga como invertida segun el material de apoyo. No desmarcar la casilla salvo instruccion expresa del profesor.

### 5.6 Si las vigas parecen desaparecer al aplicar Insertion Point

Este comando no deberia borrar vigas. Segun la ayuda oficial de CSI, `Assign > Frame > Insertion Point...` reemplaza la asignacion de punto cardinal/offset de los frames seleccionados. Si despues de aplicar `Cardinal Point = 2 - Bottom Center` las vigas no se ven, primero asumir problema de visualizacion o seleccion antes de redibujar.

Protocolo de verificacion:

1. No guardar encima del checkpoint anterior.
2. Si se necesita conservar el estado actual, usar `File > Save As...` con nombre de incidente, por ejemplo:
   `ED1_incidente_vigas_no_visibles_v01.edb`.
3. Verificar si las vigas siguen existiendo:
   `Select > Properties > Frame Sections... > VI20x60G30`.
4. Si ETABS selecciona objetos, las vigas no estan borradas. Entonces revisar visualizacion:
   `View > Set Display Options...`
   - marcar `Beams`;
   - marcar `Object Edge`;
   - desmarcar temporalmente `Object Fill` si la losa gris tapa las vigas;
   - probar con `Extrude Frames` activado/desactivado;
   - usar una vista `3D` o una elevacion para confirmar la posicion fisica.
5. Si no se selecciona ninguna viga, verificar por tablas:
   `Display > Show Tables... > Model Definition > Connectivity Data > Frame Object Connectivity`
   y/o tablas de asignaciones de seccion de frames.
6. Si tampoco aparecen en tablas, recuperar desde el ultimo checkpoint y no confiar en `Ctrl+Z`.

Interpretacion:

- Si aparecen seleccionadas o en tablas, no redibujar: estan presentes y el problema es de display/offset.
- Si no aparecen seleccionadas ni en tablas, hubo perdida real de objetos o se aplico/elimino otra operacion; abrir checkpoint.
- El hecho de que el modelo de otro companero se vea igual despues de usar `Bottom Center` es una senal de que puede ser comportamiento visual normal, no eliminacion.

Checkpoint:

`File > Save As... > ED1_03_Story2_Vigas_v01.edb`

## 6. Losas y vacios

Fuente directa:

- `Paso a Paso ETABS M.Lafontaine.pdf`, pp. 79-84.
- Recomendaciones: dibujar losas en sectores con cargas distintas, usar elementos de cuatro nodos, meshear/cortar manualmente en esquinas de muros y columnas, y evitar formas poco sanas que deleguen todo al mallado automatico.

### 6.1 Dibujo de losas

Ruta:

`Draw > Draw Floor/Wall Objects > Draw Floor/Wall (Plan, Elev, 3D)`

Propiedad:

- `Losa15G30`.

Criterio:

- Dibujar paneles reales, no una envolvente rectangular completa.
- Preferir panos de cuatro nodos cuando sea posible.
- Dibujar por sectores de carga si hay zonas con sobrecarga distinta.
- Cortar o panelizar la losa en esquinas de muros y puntos donde la conectividad sea critica.
- Respetar vacios/shaft.
- Si la planta es irregular, dividir en poligonos simples.
- No tapar el shaft con losa.
- Evitar panos muy deformados o con angulos muy alejados de 90 grados.

Herramientas:

- `Draw Rectangular Floor/Wall (Plan, Elev)`: para panos rectangulares.
- `Draw Floor/Wall (Plan, Elev, 3D)`: para poligonos irregulares.
- `Quick Draw Floor/Wall`: usar solo en celdas obvias y revisar despues.

Nota practica: no es necesario una losa por recinto, pero tampoco una sola losa gigante. Buscar equilibrio entre tiempo y calidad, siguiendo la forma rigurosa del material.

### 6.2 Openings

Para aberturas:

`Draw > Draw Floor/Wall Objects > Draw Wall Openings (Plan, Elev, 3D)`

o dibujar la losa evitando el vacio desde el inicio.

Regla:

- Si se puede dibujar la losa ya con el hueco, mejor.
- Si se usa opening, verificar visualmente que no haya shell de losa cruzando el vacio.

Checkpoint:

`File > Save As... > ED1_04_Story2_Losas_v01.edb`

## 7. Revision de conectividad antes de copiar pisos

Fuente directa:

- `Paso a Paso ETABS M.Lafontaine.pdf`, p. 65.
- El material recomienda dividir todos los muros que se intersectan entre ellos o con alguna viga.

No replicar si falla algo de esta lista:

- Muros X/Y completos.
- Vigas completas.
- Losa tipo completa.
- Shaft/vacios correctos.
- No hay muros duplicados.
- No hay vigas duplicadas.
- Muros y vigas llegan a centrolineas/nodos correctos.
- Click derecho confirma propiedades correctas.

Verificaciones:

1. `Set Display Options`: activar `Joint Objects`.
2. Revisar intersecciones con zoom.
3. Click derecho en varios muros y vigas.
4. Mostrar propiedades/asignaciones por color si es necesario.
5. Dividir/intersectar muros donde se cruzan entre ellos o con vigas.
6. Guardar checkpoint.

Regla: si una viga o muro solo "pasa por encima" visualmente pero no genera nodo/interseccion, corregir antes de copiar pisos.

## 8. Replicar planta tipo

Solo despues de validar `Story2`.

Regla:

- Copiar `Story2` a `Story1` y `Story3` a `Story19`.
- No copiar como definitivo a `Story20`.
- `Story20`/techo se modela aparte.

Ruta usual:

`Edit > Replicate...`

Usar opcion por stories si esta disponible.

Despues de replicar:

- revisar `Story1`;
- revisar `Story3`;
- revisar `Story19`;
- verificar que `Story20` no haya quedado contaminado con planta tipo completa si no corresponde.

Checkpoint:

`File > Save As... > ED1_06_PisosTipo_Replicados_v01.edb`

## 9. Techo Story20

Estado: pendiente de cierre geometrico.

Regla:

- No asumir que el techo es igual a planta tipo.
- Revisar planta de techo del enunciado.
- Dibujar o editar manualmente `Story20`.
- Verificar muros, vigas, losas, vacios y cargas de techo.

Checkpoint:

`File > Save As... > ED1_07_Techo_v01.edb`

## 10. Asignaciones estructurales

### 10.1 Diafragma

Fuente directa:

- `Paso a Paso ETABS M.Lafontaine.pdf`, pp. 100-109.
- El material distingue tres opciones: diafragma rigido, diafragma semirigido y no asignar diafragma.
- Se recomienda asignar diafragmas a losas, no a puntos.

Definir diafragma rigido:

`Define > Diaphragms...`

- Name: `D1`.
- Type: `Rigid` para los casos rigidos.

Asignar a losas:

1. Seleccionar losas de pisos.
2. `Assign > Shell > Diaphragms...`.
3. Asignar `D1`.

Para casos semirigidos:

- duplicar modelo o guardar copia;
- cambiar diafragma a `Semi-Rigid` segun metodo de comparacion;
- no mezclar resultados rigidos y semirigidos en el mismo archivo sin control.

Advertencias del material:

- No asignar un mismo diafragma rigido a partes que no tienen conexion suficiente.
- No asignar diafragma rigido a losas con grandes estrangulaciones sin justificar.
- No asignar diafragma rigido a losas con razones de aspecto extremas sin revisar.
- En diafragma rigido se pierden esfuerzos/deformaciones en el plano del diafragma.
- En diafragma semirigido no hay condensacion; las masas quedan en nodos y no se pierden esfuerzos/deformaciones en el plano.

### 10.2 Apoyos en base

Ir a nivel base.

Seleccionar nodos base.

Ruta:

`Assign > Joint > Restraints...`

Marcar:

- U1
- U2
- U3
- R1
- R2
- R3

### 10.3 Mesh de losas

Fuente directa:

- `Paso a Paso ETABS M.Lafontaine.pdf`, pp. 85-87.
- Mesh maximo usual: `1 m x 1 m`.

Seleccionar losas.

Ruta:

`Assign > Shell > Floor Auto Mesh Options...`

Recomendado:

- Auto mesh into structural elements.
- Mesh at beams and wall edges.
- Max element size inicial: `1.0 m`.
- Revisar visualmente como queda la losa mesheada.

### 10.4 Mesh de muros

Fuente directa:

- `Paso a Paso ETABS M.Lafontaine.pdf`, p. 88.
- El material recomienda conectividad directa entre elementos y mesheado manual/controlado para evitar elementos muy alargados.

Seleccionar muros.

Ruta:

`Assign > Shell > Wall Auto Mesh Options...`

Recomendado:

- Auto mesh into structural elements.
- Max element size inicial: `1.0 m`.

Regla de revision:

- evitar elementos extremadamente alargados;
- revisar que muros y losas queden conectados;
- no confiar solo en que el modelo corre.
- si aparecen elementos muy alargados, subdividir manualmente o ajustar mesh antes de analizar.

### 10.5 Auto Edge Constraint

Fuente directa:

- `Paso a Paso ETABS M.Lafontaine.pdf`, pp. 98-99.
- `Auto Edge Constraint` genera compatibilidad de deformaciones en nodos que estan en una misma linea.

Ruta:

`Assign > Shell > Auto Edge Constraints...`

Procedimiento recomendado:

1. Seleccionar todo el modelo o al menos los shells relevantes.
2. Aplicar `Auto Edge Constraints`.
3. Revisar que no este ocultando errores gruesos de geometria.

Verificar visualmente despues, especialmente en uniones muro-losa y muro-muro.

### 10.6 End offsets / rigid zone en vigas

Fuente directa:

- `docs/Material taller/Paso a Paso ETABS M.Lafontaine.pdf`, pp. 61-63.
- El material indica que ETABS asigna cachos rigidos automaticamente entre frames, pero que en frames que penetran shells no viene incorporado automaticamente.
- El valor usual mostrado es `Rigid-zone factor = 0.75`.
- Se recomienda verificar siempre que ETABS haya asignado correctamente los cachos rigidos.

Seleccionar vigas `VI20x60G30`.

Ruta:

`Assign > Frame > End Length Offsets...`

Configurar:

- `Automatic from Connectivity`.
- `Rigid-zone factor = 0.75`.
- Frame Self Weight Option: `Auto`.

Despues verificar visualmente en una elevacion o vista deformada/asignaciones que los cachos rigidos quedaron donde corresponden. Si una viga llega a un muro shell y ETABS no reconoce el cacho, documentar y revisar manualmente con el profesor/ayudante antes de analizar.

### 10.7 Piers y spandrels

Fuente directa:

- `Paso a Paso ETABS M.Lafontaine.pdf`, pp. 110-117.
- `Pier` se usa para muros/elementos verticales.
- `Spandrel` se usa para vigas o elementos horizontales tipo shell/spandrel.
- En un pier, ETABS integra esfuerzos internos en la seccion inferior y superior del pier por piso.
- Una mala asignacion mezcla fuerzas de elementos distintos o deja sin leer secciones criticas.

Procedimiento:

1. Identificar muros que se van a reportar/disenar.
2. Seleccionar cada muro o conjunto realmente continuo que corresponda a un solo pier.
3. `Assign > Shell > Pier Label...`.
4. Usar nombres claros, por ejemplo `P_EJE5`, `P_EJE4_T`, etc.
5. Si hay spandrels relevantes, asignar `Assign > Shell > Spandrel Label...`.

Regla: no agrupar en un mismo pier dos muros que estructuralmente se quieren leer por separado.

## 11. Cargas

### 11.1 Load Patterns

Ruta:

`Define > Load Patterns...`

Crear:

| Pattern | Type | Self Weight Multiplier |
| --- | --- | ---: |
| `PP` | Dead | 1 |
| `TERP` | Super Dead | 0 |
| `TERT` | Super Dead | 0 |
| `SCP` | Live | 0 |
| `SCT` | Roof Live | 0 |

Regla:

- Solo `PP` lleva Self Weight Multiplier = 1.
- No duplicar peso propio en otro patron.

### 11.2 Cargas uniformes en losas

Pisos tipo:

| Pattern | Valor |
| --- | ---: |
| `TERP` | 0.140 tonf/m2 |
| `SCP` | 0.250 tonf/m2 |

Techo:

| Pattern | Valor |
| --- | ---: |
| `TERT` | 0.100 tonf/m2 |
| `SCT` | 0.100 tonf/m2 |

Ruta:

`Assign > Shell Loads > Uniform...`

Usar:

- Direction: `Gravity`.
- Replace Existing Loads cuando se este corrigiendo.

Pasillos:

- Si el enunciado/profesor exige pasillos, usar `0.500 tonf/m2` en esas zonas.
- Si no esta definido con claridad, dejar `0.250 tonf/m2` uniforme y documentar criterio.

### 11.3 Verificacion visual de cargas

Ruta:

`Display > Show Load Assigns > Shell...`

Revisar:

- `TERP` solo en pisos tipo.
- `SCP` en pisos tipo.
- `TERT` solo en techo.
- `SCT` solo en techo.
- No hay losas sin carga por error.

## 12. Mass Source

Ruta:

`Define > Mass Source...`

Crear o editar `MsSrc1`.

Configuracion recomendada:

- Mass Definition: `Specified Load Patterns`.
- Include Lateral Mass Only.
- Lump Lateral Mass at Story Levels.

Multiplicadores:

| Load Pattern | Multiplier |
| --- | ---: |
| `PP` | 1.0 |
| `TERP` | 1.0 |
| `TERT` | 1.0 |
| `SCP` | 0.25 |
| `SCT` | 0.0 |

Nota critica:

- `TERT` debe estar en la masa.
- `SCT` no entra en masa sismica salvo criterio distinto exigido.
- Verificar que no se duplique peso propio con opcion de self mass y patron `PP`.

## 13. Analisis modal

Ruta:

`Define > Load Cases...`

Caso:

- Name: `MODAL`.
- Type: `Modal`.
- Method: Eigen o Ritz segun criterio del curso.
- Number of modes: usar suficientes para alcanzar al menos 90% de masa participativa en X/Y y torsion cuando aplique.

Verificacion:

`Display > Show Tables... > Analysis > Modal > Participating Mass Ratios`

Entregables:

- periodos principales `Tx`, `Ty`, `Tz`;
- masas participantes;
- numero de modos usado;
- deformadas modales razonables.

## 14. Sismo y espectro

Base de defensa:

- `NCh433:2026`.
- Para Edificio 1 segun estado normativo local:
  - Zona 3.
  - Sitio C.
  - Categoria II.
  - `Ao = 0.40 g`.
  - `S = 1.05`.
  - `T0 = 0.40 s`.
  - `T' = 0.45 s`.
  - `n = 1.40`.
  - `p = 1.60`.
  - `I = 1.0`.
  - `R = 7`.
  - `R0 = 11`.

No defender como base final `DS61` si el curso ya exige `NCh433:2026`.

Recomendacion ETABS:

- usar espectro desde archivo `.txt`;
- no depender del espectro automatico de ETABS si no coincide con NCh433:2026;
- guardar el archivo de espectro junto al modelo.

Casos base:

- `SDX` o `SEx`: espectro en X.
- `SDY` o `SEy`: espectro en Y.

Usar nomenclatura consistente en todo el modelo.

## 15. Torsion accidental y 6 casos

Fuente directa:

- `docs/Material taller/Material Apoyo Taller 2026.pdf`, pp. 29-41.
- El material presenta metodo a, metodo b forma 1 y metodo b forma 2 para torsion accidental en ETABS.

Edificio 1 requiere comparar:

- 3 formas/metodos de torsion accidental;
- 2 condiciones de diafragma;
- total: 6 casos.

No duplicar torsion:

- si un caso ya incluye excentricidad accidental en el load case, no agregar momento torsor externo equivalente al mismo tiempo;
- si se usa metodo por momentos torsores, no activar excentricidad accidental adicional.

Estructura de trabajo:

| Caso | Diafragma | Torsion |
| --- | --- | --- |
| 1 | Rigido | Metodo a |
| 2 | Rigido | Metodo b forma 1 |
| 3 | Rigido | Metodo b forma 2 |
| 4 | Semi-rigido | Metodo a |
| 5 | Semi-rigido | Metodo b forma 1 |
| 6 | Semi-rigido | Metodo b forma 2 |

### 15.1 Metodo a: desplazar centro de masa

Segun el material:

1. Crear una `Mass Source` original con excentricidad `0`.
2. Crear cuatro fuentes de masa adicionales:
   - `Masa+X`
   - `Masa-X`
   - `Masa+Y`
   - `Masa-Y`
3. En cada una, habilitar `Adjust Diaphragm Lateral Mass to Move Mass Centroid by`.
4. Usar `+/-0.05` de la direccion perpendicular correspondiente.
5. Dejar la otra direccion en `0` para no desplazar el CM en dos direcciones a la vez.
6. Crear casos estaticos no lineales auxiliares sin cargas externas, solo para vincular cada fuente de masa.
7. Crear casos modales especificos usando `Use Nonlinear Case (Loads at End of Case NOT included)`.
8. Crear casos espectrales asociados a cada modal desplazado.

### 15.2 Metodo b forma 1: torsion estatica por piso

Segun el material:

1. Correr primero el modelo base sin excentricidad accidental dinamica.
2. En `Mass Source`, asegurar que `Move Mass Centroid over Diaphragm = 0`.
3. Obtener cortes de piso combinados por CQC.
4. Calcular fuerza de piso como diferencia de cortes `Qk - Qk+1`.
5. Multiplicar por la excentricidad accidental del piso.
6. Ingresar momentos torsores estaticos por piso como cargas auxiliares.

### 15.3 Metodo b forma 2: excentricidad por piso

Segun el material:

1. Ir a `Define > Load Cases`.
2. Modificar el caso espectral `Sx` o `Sy`.
3. En `Diaphragm Eccentricity`, usar `Modify/Show`.
4. Dejar `Eccentricity Ratio = 0`.
5. Para cada diafragma/piso, ingresar la excentricidad calculada como longitud positiva.
6. ETABS aplica internamente el brazo para capturar la envolvente.

Pendiente operativo:

- cerrar implementacion exacta contra `Material Apoyo Taller 2026.pdf`;
- documentar ruta UI usada para cada metodo;
- guardar archivo ETABS por caso o usar nomenclatura estricta de load cases.

## 16. Combinaciones

Fuente:

- `NCh3171-2017`.
- `Material Apoyo Taller 2026.pdf`, pp. 42-45.

Regla:

- Crear combinaciones gravitacionales y sismicas.
- Mantener `PP + TERP + TERT` como parte permanente cuando corresponda.
- Incluir signos +/- de sismo.
- No mezclar combinaciones de metodo a, b1 y b2 sin nombre claro.

Nomenclatura sugerida:

- `C1_...` para caso 1.
- `C2_...` para caso 2.
- `C3_...` para caso 3.
- repetir con `C4`, `C5`, `C6`.

Conteos del material de apoyo:

| Metodo | Descripcion | Combinaciones ETABS |
| --- | --- | ---: |
| Metodo estatico | SDX/SDY + TEX/TEY | 19 |
| Dinamico metodo b forma 1 | espectral + torsion estatica | 11 |
| Dinamico metodo b forma 2 | espectral con excentricidad por piso | 7 |
| Dinamico metodo a | matrices de masa desplazadas | 15 |

Mapeo de cargas del material:

- `CP`: cargas permanentes = `PP + TERP + TERT`.
- `L`: sobrecarga de pisos = `SCP`.
- `Lr`: sobrecarga de techo = `SCT`.
- `SDX`, `SDY`: sismos aplicados en centro de masa.
- `TEX`, `TEY`: torsion accidental estatica.
- `SDTX`, `SDTY`: sismo con torsion accidental entregada por piso.

Regla de trazabilidad: si en ETABS se usan nombres distintos (`SEx`, `SEy`, etc.), incluir una tabla de equivalencia en el informe.

## 17. Check Model y analisis

Antes de correr:

1. Guardar.
2. `Analyze > Check Model...`.
3. Revisar warnings.
4. No usar `Fix` automatico sin entender que cambia.
5. Corregir geometria si aparecen elementos desconectados o duplicados.

Correr:

`Analyze > Run Analysis`

Despues:

- revisar deformada gravitacional;
- revisar deformadas modales;
- revisar log;
- revisar masa y peso;
- revisar que no haya inestabilidades.

## 18. Resultados a extraer

Fuente directa:

- `Material Apoyo Taller 2026.pdf`, pp. 5-14 para drift, diafragma y Section Cuts.
- `Paso a Paso ETABS M.Lafontaine.pdf`, pp. 126-130 para lectura de fuerzas en shells y precauciones.

Tablas minimas:

| Resultado | Ruta ETABS aproximada |
| --- | --- |
| Peso sismico | `Display > Show Tables... > Mass Summary` |
| Periodos | `Modal Periods And Frequencies` |
| Masas participantes | `Modal Participating Mass Ratios` |
| Reacciones base | `Base Reactions` |
| Cortes de piso | `Story Forces` |
| Drifts | `Story Drifts` y `Joint Drifts` |
| CM/CR | tablas de centers si estan disponibles |
| Fuerzas en muros | `Pier Forces` o Section Cuts |

Exportar a Excel:

`Display > Show Tables... > Export to Excel`

Regla:

- cada valor del informe debe poder rastrearse a una tabla ETABS;
- no usar solo capturas si existe tabla exportable;
- guardar archivo con fecha.

### 18.1 Drift

Reglas del material de apoyo:

- Para el drift del CM, buscar un nodo cercano al centro de masa; el material recomienda apagar losas y vigas y dejar visibles solo muros para encontrarlo.
- No calcular drift restando desplazamientos CQC manualmente. La tabla de desplazamientos ya esta combinada por CQC y no corresponde restarla para obtener drift.
- Usar directamente `Joint Drifts` para el nodo del CM y para puntos extremos.
- Para hallar el punto desfavorable, usar `Diaphragm Max Over Avg Drifts`; la columna `Max Drift` indica el maximo en planta.
- Verificar condicion 1 con drift del CM.
- Verificar condicion 2 comparando drift extremo menos drift del CM para la misma condicion/caso.

### 18.2 Section Cuts

Ruta base del material:

1. `Define > Group Definitions...`.
2. Crear un grupo por piso o por seccion que se quiera leer.
3. Seleccionar el piso/elementos y asignar:
   `Assign > Assign Objects to Group...`.
4. Ir a:
   `Define > Section Cuts... > Add Section Cut`.
5. Seleccionar grupo, tipo de resultado y coordenadas del punto de referencia.

Usar Section Cuts cuando el resultado requerido no queda limpio con tablas de pier/spandrel o cuando el profesor lo pide explicitamente.

### 18.3 Validacion peso/area

Fuente:

- `Paso a Paso ETABS M.Lafontaine.pdf`, p. 138.

Criterio de chequeo:

```text
Peso sismico total / Area total de losas ~= 1.0 tonf/m2
```

No es resultado oficial por si solo; es una validacion gruesa de plausibilidad.

## 19. Checklist antes de seguir modelando

Estado actual esperado antes de avanzar a cargas/analisis:

- [ ] Grilla X completa con auxiliares.
- [ ] Grilla Y completa con `aux1` y `aux2`.
- [ ] `Story2` activo.
- [ ] Muros X/Y dibujados.
- [ ] Vigas `VI20x60G30` dibujadas por tramos.
- [ ] Releases `P` asignados solo donde corresponde.
- [ ] Vigas invertidas con `Cardinal Point = 2 - Bottom Center`.
- [ ] Casilla `Do not transform frame stiffness for offsets from centroid` marcada en vigas invertidas.
- [ ] End Length Offsets con `Automatic from Connectivity` y `Rigid-zone factor = 0.75`.
- [ ] Losa tipo dibujada sin tapar vacios.
- [ ] Shaft revisado.
- [ ] `Story20` pendiente o cerrado por separado.
- [ ] Modelo guardado por checkpoint.

## 20. Errores que bloquean el modelo

Bloquean analisis oficial:

- usar planta historica incorrecta;
- copiar a `All Stories` antes de cerrar `Story2`;
- dibujar muros con propiedad `Losa15G30`;
- dibujar vigas largas atravesando muros sin tramos/nodos;
- usar `Pinned` en vigas sin evidencia;
- dejar vigas invertidas con `Cardinal Point = 10 (Centroid)`;
- desmarcar `Do not transform frame stiffness...` contra la captura del material;
- olvidar `Rigid-zone factor = 0.75` en cachos rigidos;
- olvidar `TERT` en masa;
- duplicar peso propio;
- tapar shaft con losa;
- correr casos de torsion duplicando excentricidad;
- defender resultados con `DS61` como base final si el curso ya exige `NCh433:2026`.

## 21. Proximo hito

Para cerrar esta guia como 100% final faltan evidencias del modelo manual:

- captura limpia de `Story2`;
- captura limpia de `Story20`;
- tabla/export de objetos de muros;
- tabla/export de objetos de vigas;
- tabla/export de losas/vacios;
- confirmacion de releases `C/P` en vigas;
- confirmacion de shaft;
- confirmacion de diafragma y mesh.

Hasta tener eso, esta guia es el flujo UI maestro y seguro, pero la geometria fina de techo, losas y algunos tramos debe verificarse contra el modelo manual.
