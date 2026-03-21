
  Puedo hacerte el Edificio 1 completo por API?

  Si. Un script Python que crea:

- Grilla (17 ejes Y + 6 ejes X + 20 pisos)
- Materiales (G30, A630-420H)
- Secciones (muros 30cm, 20cm, vigas 20x60, losa 15cm)
- Dibujar todos los muros en sus ejes correctos
- Dibujar vigas y losas
- Asignar cargas (SCP, SCT, TERP, TERT)
- Diafragma rigido
- Empotrado en base

  Lo corro y en ETABS aparece el edificio listo para analizar.

  ETABS vs SAP2000

  Segun el enunciado:

  ┌──────────────────────────────────┬─────────────────────────────┐
  │              Tarea               │          Programa           │
  ├──────────────────────────────────┼─────────────────────────────┤
  │ Modelo completo + analisis       │ ETABS                       │
  ├──────────────────────────────────┼─────────────────────────────┤
  │ Diagramas interaccion Pu-Mu      │ ETABS (Section Designer)    │
  ├──────────────────────────────────┼─────────────────────────────┤
  │ Curvas momento-curvatura (M-phi) │ SAP2000                     │
  ├──────────────────────────────────┼─────────────────────────────┤
  │ Diseno muros y marcos            │ ETABS + verificacion manual │
  └──────────────────────────────────┴─────────────────────────────┘

  SAP se usa solo para las curvas M-phi (epsilon_c = 0.003 y 0.008). Todo lo demas es
  ETABS.

  A que tienes que llegar MANUALMENTE (sin programa)

  El enunciado lo dice explicito:

  Parte 2 - Edificio 1:
  "Disenar el muro sin uso de programa de computacion verificando todas las
  disposiciones"

- Muro eje 5 (rectangular), piso 1
- Diseno completo a mano: esbeltez, corte, flexion, confinamiento

  Parte 2 - Edificio 2:
  "Disenar sin uso de programa de computacion"

- Viga piso 1 entre ejes 1-2 del marco eje A
- Columna piso 1 en interseccion eje A con 1

  Resumen de que hace cada cosa

  API (yo te lo hago)          GUI (tu aprendes)           A MANO (obligatorio)
  ─────────────────────        ──────────────────          ────────────────────
  Crear modelo Ed.1            Verificar modelo            Muro eje 5 piso 1
  Crear modelo Ed.2            Ajustar detalles            Viga marco A piso 1
  Extraer resultados           Correr analisis             Columna marco A piso 1
  Generar graficos             Section Designer
  Verificar drift 6 casos     Expo: mostrar dominio

  Mi propuesta

  Te escribo el script completo del Edificio 1 ahora. Tu lo corres en el lab, verificas
  que el modelo se ve bien en la GUI, y asi:

1. Tienes el modelo listo para analizar
2. Ves en la GUI que produjo cada linea de codigo
3. Aprendes la relacion API ↔ interfaz

  Lo hago?

✻ Cooked for 35s

❯ si porfa el edificio 1 completisisisiimo. aclarame, es un solo script, varios?
  cargo varios en paralelo o en serie? coo funciona?

    02:32 PM claude-opus-4-6
● Es un solo script Python. Lo corres una vez con ETABS abierto (modelo nuevo vacio) y
  te crea todo.

  Asi funciona:

  Tu abres ETABS → Nuevo modelo vacio → Corres el script → Edificio completo

  Voy a leerme el enunciado completo una vez mas y el material del taller para no dejar
  nada fuera.

● Read(docs\Material taller\Material Apoyo Taller 2026.pdf · pages 1-10)

● Bash(PYTHONIOENCODING=utf-8 python -c "
      import fitz
      doc = fitz.open('C:/Seba/1° Sem. 2026 - UCN/docs/Material taller/Material Apoyo
    Taller 2026.pdf')
      for i in range(min(15, len(doc))):
          text = doc[i].get_text()
          text = text.encode('ascii', 'replace').decode('ascii')
          print(f'=== PAG {i+1} ===')
          print(text[:2000])
      " 2>&1 | head -300)
  ⎿  === PAG 1 ===
     XXXXXXXXXXXX
     Verde
     A) Consideraciones al Modelar

    === PAG 2 ===

    === PAG 3 ===

    Visualizar Edificio en 3D y moverse a trav?s de ?l

    A) Visualizar y caminar por edificio
     1) Seleccionar Vista 3D del edificio
     2) Seleccionar                     y seleccionar Extrude Frames y Extrude
     Shells
     3) Options luego Graphics Mode y DirectX
     4) Commando Rotar Edificio seg?n lo que se quiera ver
     5) Seleccionar View Walk o su respectivo icono
          Con bot?n Izquierdo mouse se avanza por edificio
          Con bot?n derecho mouse subir y bajar por el edificio (como
     ascensor)

    B) Dejar de ver parte del edificio para mejor visualizar lo que nos
     interesa
     1) Options luego Graphics Mode y DirectX
     2) View y luego Set Elevation View
     3) Seleccionar un eje del edificio que indica lo que a partir de ?l se quiere
    ver. Se selecciona 3D Section y ya sea Left o Right
     Ejemplo: Si selecciono Left se deja de ver desde eje seleccionado hacia
     la izquierda.

    === PAG 4 ===
     B)
     Verificaci?n condiciones de deformaci?n de Norma NCh433
     Ubicar un nodo cercano al CM.
     Para ver centro de masas:

    === PAG 5 ===
     Para buscar un nodo cercano al CM recomiendo apagar losas y vigas, dejar
     visible solo muros.
     Con solo los muros visibles es mas f?cil hallar un nodo cercano al CM.
     Apagamos vigas y losas:
     Buscamos un nodo cercano  al CM y hacemos click derecho sobre ese nodo:
     El nodo 44 representara la ubicaci?n del CM. Ahora ir a mostrar el drift de
    ese nodo para verificar la
     condici?n N?1:

    === PAG 6 ===

    === PAG 7 ===
     Le doy Ok.
     Me mostrar? una tabla con muchos valores.
     Se debe filtrar por el nodo que yo he seleccionado, el 44.
     Click derecho donde dice Label y selecciono el 44:
     Click derecho sobre Output Case, selecciono el estado de carga para el cual
    quiero
     verificar la condici?n.

    === PAG 8 ===
     Drift X y Drift Y muestra el (dispcm i+1- dispcm i)/hpiso del nodo en cuesti?n
    combinado seg?n CQC.
     No es correcto restar los desplazamientos que muestra la tabla anterior y
     calcular el
     drift con ellos, ya que esos valores vienen de una combinaci?n CQC.
     De esta manera se obtiene el drift del centro de masa y luego se compara con
    el
     limite que indica la norma.
     Para exportar los datos a Excel ir a:

    === PAG 9 ===
     Para esta condici?n se debe:
      i)   Derminar el drift m?ximo de puntos mas desfavorable del edifico. Son los
    puntos extremos de ?l.
     Para ello:
     - Ver n?mero de nodos de esos puntos
     - Ver valores de drift para esos nodos de forma similar como se explic? para
    el centro de masa.
     ii) Verificaci?n condici?n 2
     Teniendo tanto los drift de cada punto extremo se le restan los drift del
     centro de masa antes
     determinados, para una misma condici?n de carga de servicio que establece la
    normativa y se
     verifica si se cumple condici?n de la norma.
     - Se repite esto para los distintos estados de carga para los que se debe
     verifica (ver apuntes del
     curso)
     Para ver donde, por ejemplo, esta el nodo 29 en la planta del edificio
     seleccionar:

    === PAG 10 ===
     Comentario:
     El procedimiento antes descrito para saber cual es el punto mas desfavorable
    requiere bastante
     observaciones de resultados.
     La pregunta es:
     ? Como saber cual es el nodo que tiene mayor drift en el edificio?:
     Una forma se muestra a continuaci?n:

    === PAG 11 ===
     Filtrar por el caso de carga. Ejemplo SEx

    === PAG 12 ===
     Seleccionar el diafragma en X (si va a verificar el sismo en X) y diafragma Y
    (si va a
     verificar sismo Y). Yo puse en X solo para ejemplo.
     Esta columna indica el drift m?ximo en planta.

    === PAG 13 ===
     TABLE:  Joint Drifts
     Story
     Label
     Unique Name Output Case Case Type Step Type Step Number
     Disp X
     Disp Y
     Drift  X
     Drift Y
     mm
     mm
     Story5
     31
     176
     Sismo X
     LinStatic
     19,423
     3
     0,000922
     0,000158
     Story4
     31
     175
     Sismo X
     LinStatic
     16,657
     2,527
     0,00139
     0,000228
     Story3
     31
     174
     Sismo X
     LinStatic
     12,486
     1,843
     0,001664
     0,000258
     Story2
     31
     161
     Sismo X
     LinStatic
     7,494
     1,068
     0,001487
     0,000216
     Story1
     31
     193
     Sismo X
     LinStatic
     3,033
     0,419
     0,001011
     0,00014
     TABLE:  Diaphragm Max Over Avg Drifts
     Story
     Output Case Case Type
     Step Type Step Number
     Item
     Max Drift
     Avg Drift
     Ratio
     Label
     Max Loc X
     Max Loc Y
     m
     m
     Story5
     Sismo X
     LinStatic
     Diaph Diafragma Rigido X
     0,000922
     0,000764
     1,206 31
     32,5
     0
     Story4
     Sismo X
     LinStatic
     Diaph Diafragma Rigido X
     0,00139
     0,001162
     1,196 31
     32,5
     0
     Story3
     Sismo X
     LinStatic
     Diaph Diafragma Rigido X
     0,001664
     0,001406
     1,184 31
     32,5
     0
     Story2
     Sismo X
     LinStatic
     Diaph Diafragma Rigido X
     0,001487
     0,001271
     1,17 31
     32,5
     0
     Story1
     Sismo X
     LinStatic
     Diaph Diafragma Rigido X
     0,001011
     0,000871
     1,16 31
     32,5
     0
     Las tablas muestra los resultados del drift del nodo 31 del edificio antes
     mostrado y que resulto ser el
     mas desfavorable por las dos forma antes descritas.
     Se puede ver que los valores de los drifts de ese nodo son los mismos en ambas
    tablas.

    === PAG 14 ===
     C) Asignaci?n de Diafragma R?gido
     Para asignar diafragma r?gido:
     i) Primero se debe definir el diafragma. En Define y diaphragms se define un
    nombre para el diafragma.
     ii) Para asignar el diafragma:  Para ello voy a Selec y Propertie y slab
     sections lo
     cual selecciona todas las losas.
     iii) Asign? el diafragma. Assign, Shell y diaphragms y seleccion? nombre del
    diafragma a asignar.
     D) Definir un Section Cut
     i) Se crea un nombre de grupo. Para ello Define, Group Definitions y ADD y se
    crea un grupo. Se vamos, por ejemplo, encontrar valor con section cut en
     todos los pisos se deben definir un grupo por piso.
     ii) Luego seleccion? el piso y asign? ese grupo al piso. Assign, Assign Objets
    to
     Group y seleccion? el nombre de grupo que corresponda.
     iii) Luego defino el Section Cut. Define, Section Cuts, ADD Section Cuts.
     Ingreso
     un nombre para el section cut y seleccion?: grupo que corresponda, tipo de
     resultado que quiero encontrar (Ejemplo Analysis para momentos torsores) y
     en User Defined coordenadas x,y,z del punto para los cuales deseo los
     resultados y OK.

    === PAG 15 ===
     E)
     Explicaci?n de posici?n de ejes en Section Design de
     programas ETABS y SAP
     E1)En Section Design ETABS
     E2) En Section Design programa SAP
     Sismo X, 0 grado, Sismo - X, 180 grados, Sismo Y, 90 grado y Sismo -Y 180
     grados
     Cero?grados?es?para?sismo?direcci?n?+Y?y?180%?para?Sismo??Y
     90 grados es para Sismo -X y 270 grados es para Sismo +X

● Bash(PYTHONIOENCODING=utf-8 python -c "
      import fitz
      doc = fitz.open('C:/Seba/1° Sem. 2026 - UCN/docs/Material taller/Material Apoyo
    Taller 2026.pdf')
      for i in range(15, min(30, len(doc))):
          text = doc[i].get_text()
          text = text.encode('ascii', 'replace').decode('ascii')
          print(f'=== PAG {i+1} ===')
          print(text[:2000])
      " 2>&1 | head -300)
  ⎿  === PAG 16 ===
     3

    === PAG 17 ===
     Conclusiones:
     i)
     Tanto orientaci?n de ejes locales del elemento en
     el Section Design como ?ngulos para sismo X, -
     X, Y y -Y son diferente en ambos programas.
     ii) En el curso para realizar el an?lisis y dise?ar los
     elementos de los edificios (vigas, muros,
     columnas) usaremos programa ETABS. Ver ejes
     locales
     de
     elementos
     estructurales
     para
     interpretar bien el tipo de esfuerzo.
     iii) Para ver diagramas de interacci?n de muros
     usaremos ETABS y para diagrama momento
     curvatura  usaremos section design del SAP.

    === PAG 18 ===
     1) Exportar tablas de ETABS a EXCEL: Se copia de a una tabla o todas ellas del
    diagrama de
     interacci?n y se lleva a Excel.
     2) Ir a Insertar grafico de dispersi?n con l?neas suavizadas:
     F) Diagramas de Interacci?n

    === PAG 19 ===
     3) Click derecho sobre el grafico en blanco e ir a seleccionar datos:
     Luego seleccionamos ?agregar datos?.

    === PAG 20 ===
     4) Seleccionamos los datos que correspondan para dibujar el diagrama P-M:
     Para seleccionar los datos en X o en Y se debe arrastrar el mouse por sobre
    los valores
     que se graficaran. Donde dice ?nombre de la serie? se le asigna un nombre a la
    curva
     que se est? graficando.

    Se repite el proceso para la otra curva. Deber?a verse as?:

    Se repite el proceso para graficar las curvas sin PHI.

    === PAG 21 ===
     5) Editar diagrama:
     Para dejar ambas curvas del mismo color se debe hacer click derecho sobre la
    curva
     que se desea cambiar el color y luego cambiar ?relleno? y ?contorno? al color
    deseado.

    Con la opci?n de ?+?:
     Seleccionamos:
     -t?tulo del eje
     -t?tulo de grafico
     -leyenda

    === PAG 22 ===

    Con todo ello realizado el diagrama de interacci?n deber?a empezar a verse

| as?:                                                                          |
| ----------------------------------------------------------------------------- |
| Se le asigno titulo a ambos ejes y al gr?fico.                                |
| -                                                                             |
| Se grafico la curva con PHI y sin PHI.                                        |
| -                                                                             |
| Se le cambio el color a cada curva.                                           |
| -                                                                             |
| Se editaron las leyendas (deber?an aparecer 4, ya que son 4 curvas, pero deje |
| solo una de la curva con PHI y una de la curva sin PHI para que se vea        |
| ordenado).                                                                    |

    === PAG 23 ===
     6) Para graficar los distintos puntos de combinaciones de carga:
     Al igual como se exportaron las curvas de ETABS a EXCEL ahora se deben
     exportar las
     combinaciones P-M para luego graficarlas y verificar que est?n dentro de las
    curvas
     de interacci?n.
     Para graficarlas se debe ir a seleccionar datos y graficar los puntos que
     correspondan. IMPORTANTE: Se debe ver como est?n orientados los ejes locales
    del
     PIER para interpretar bien los esfuerzos. Ejemplo si P es tracci?n o
     compresi?n.
     Al graficarlos se ver? as?:

    === PAG 24 ===
     Para visualizarlo como puntos hacemos click derecho sobre la leyenda de la
     curva
     que corresponde a las combinaciones de carga:

    Seleccionamos cambiar tipo de grafico de series:

    === PAG 25 ===
     Deber?a verse as?:

    As? se grafican los diagramas de interacci?n.

    === PAG 26 ===
     G) Como dise?a los elementos estructurales el programa ETABS cuando se
     realiza un An?lisis S?smico de Superposici?n Modal Espectral
     Considerando que al hacer un an?lisis modal espectral se combinan mediante CQC
    los
     aportes de cada modo de vibrar el resultado es siempre positivo. Esto
     significa, por ejemplo,
     en el caso de un muro que el esfuerzo axial Pu de la figura ser? positivo. La
    pregunta es
     ?produce compresi?n o tracci?n en el muro? Lo mismo ocurre con momento M2 y
    M3.
     Por lo tanto, para estar por el lado de la seguridad el programa genera 8
     combinaciones de
     esfuerzos s?smicos para el estado de carga que est? considerando el sismo.
     Estos se
     muestran en las figuras siguientes.
     Supongamos que vamos a dise?ar para estado de carga: 0,9*D+1,4*SY(s/t)+1,4*TY
    En tablas siguientes se muestran los estados de carga que se generan para el
    dise?o de ?l.
     G)  Forma que ETABS en el dise?o cuando se realiza An?lisis Modal Espectral

    === PAG 27 ===
     TABLE:  Design Forces - Piers
     Story
     Pier
     Combo
     Location
     P
     V2
     V3
     T
     M2
     M3
     Direcci?n
     tonf
     tonf
     tonf
     tonf-cm tonf-cm
     tonf-cm
     del Sismo
     Story1
     MR
     Comb10-1 Bottom
     -160,03
     59,448
     0,2909
     71,927
     75,277
     83116,72
     Story1
     MR
     Comb10-2 Bottom
     -160,03
     -87,41
     0,2909
     71,927
     -12,51
     83116,72
     Story1
     MR
     Comb10-3 Bottom
     -160,03
     59,448
     -0,046
     71,927
     75,277
     -129964
     Story1
     MR
     Comb10-4 Bottom
     -160,03
     -87,41
     -0,046
     71,927
     -12,51
     -129964
     Story1
     MR
     Comb10-5 Bottom
     -670,22
     59,448
     0,2909
     19,336
     75,277
     83116,72
     Story1
     MR
     Comb10-6 Bottom
     -670,22
     -87,41
     0,2909
     19,336
     -12,51
     83116,72
     Story1
     MR
     Comb10-7 Bottom
     -670,22
     59,448
     -0,046
     19,336
     75,277
     -129964
     Story1
     MR
     Comb10-8 Bottom
     -670,22
     -87,41
     -0,046
     19,336
     -12,51
     -129964
     Story1
     MR
     0,9D-1
     Bottom
     -469,51
     -2,006
     0,0202
     2,401
     3,149
     -2528,78
     SY-
     Story1
     MR
     1,4SY-1
     Bottom 255,093
     73,432
     0,1684
     26,296
     43,896
     106540,2
     SX+
     Story1
     MR
     1,4SY-2
     Bottom 255,093
     -73,43
     0,1684
     26,296
     -43,9
     106540,2
     SY-
     Story1
     MR
     1,4SY-3
     Bottom 255,093
     73,432
     -0,168
     26,296
     43,896
     -106540
     SY+
     Story1
     MR
     1,4SY-4
     Bottom 255,093
     -73,43
     -0,168
     26,296
     -43,9
     -106540
     SY-
     Story1
     MR
     1,4SY-5
     Bottom
     -255,09
     73,432
     0,1684
     -26,3
     43,896
     106540,2
     SY+
     Story1
     MR
     1,4SY-6
     Bottom
     -255,09
     -73,43
     0,1684
     -26,3
     -43,9
     106540,2
     SY-
     Story1
     MR
     1,4SY-7
     Bottom
     -255,09
     73,432
     -0,168
     -26,3
     43,896
     -106540
     SY+
     Story1
     MR
     1,4SY-8
     Bottom
     -255,09
     -73,43
     -0,168
     -26,3

● Bash(PYTHONIOENCODING=utf-8 python -c "
      import fitz
      doc = fitz.open('C:/Seba/1° Sem. 2026 - UCN/docs/Material taller/Material Apoyo
    Taller 2026.pdf')
      for i in range(27, min(47, len(doc))):
          text = doc[i].get_text()
          text = text.encode('ascii', 'replace').decode('ascii')
          print(f'=== PAG {i+1} ===')
          print(text[:1500])
      " 2>&1 | head -300)
  ⎿  === PAG 28 ===

    P
     V2
     V3
     T
     M2
     M3
     tonf
     tonf
     tonf
     tonf-cm
     tonf-cm
     tonf-cm
     Comb10-1 -160,031
     59,4483
     0,2909
     71,928
     75,277
     83116,7
     Comb10-2 -160,031 -87,4149
     0,2909
     71,928
     -12,515
     83116,7
     Comb10-3 -160,031
     59,4483
     -0,0459
     71,928
     75,277
     -129964
     Comb10-4 -160,031 -87,4149
     -0,0459
     71,928
     -12,515
     -129964
     Comb10-5 -670,217
     59,4483
     0,2909
     19,336
     75,277
     83116,7
     Comb10-6 -670,217 -87,4149
     0,2909
     19,336
     -12,515
     83116,7
     Comb10-7 -670,217
     59,4483
     -0,0459
     19,336
     75,277
     -129964
     Comb10-8 -670,217 -87,4149
     -0,0459
     19,336
     -12,515
     -129964

    === PAG 29 ===
     172
     ? M?todo a): Torsi?n accidental desplazando el centro de masas.
     Paso 1: Definici?n de Fuentes de Masa (Mass Sources).
     En este m?todo se debe trasladar el centro de masa, en cada una de las
     direcciones estipuladas en la normativa vigente una distancia igual a ?5% de
    la
     direcci?n mayor perpendicular a la acci?n s?smica. Especificado ello el
     programa
     obtiene la matriz de masa de la estructura teniendo en cuenta las nuevas
     posiciones de ?l.
     Para esto en el programa debemos generar 4 matrices de masa extra con
     excentricidades accidentales, nos dirigimos a:
     1) ?Define? > ?Mass Source?
     a. Masa Original: Se define seg?n las cargas normativas (100% de las
     cargas permanentes + 25% de sobrecarga para construcciones de
     habitaci?n privada) con 0% de excentricidad, es decir, en posici?n
     original del centro de masa.
     b. Masa+X: Se duplica la fuente original, luego se habilita la secci?n
     ?Adjust Diaphragm Lateral Mass to Move Mass Centroid by:? para
     poder ingresar el valor de 0.05 (5%) en la casilla que indica ?This
     Ratio of Diaphragm Width in X Direction? esto le indica al programa
     que deber? mover el centro de masa en la direcci?n X una distancia
     igual al 5% del valor del ancho mayor en X. (Es importante dejar la
     otra casilla con un valor igual a 0 para evitar desplazar el Centro de
     Masa en ambas direcciones de manera simult?nea)
     H) Aplicaci?n de Torsi?n Accidental en ETABS
     H1: M?todo a) Normativa Vigente

    === PAG 30 ===
     173
     c. Masa-X: Se repite el paso anterior con excentricidad -0.05.
     d. Masa+Y: Se repite para la direcci?n Y con excentricidad 0.05.
     e. Masa-Y: Se repite para la direcci?n Y con excentricidad -0.05.
     Figura B.1 Opci?n para ingresar excentricidad seg?n forma a. Fuente: ETABS.
    Paso 2: Configuraci?n de Casos Est?ticos No Lineales.
     Se requiere crear casos de carga auxiliares para vincular cada una de las
     cuatro
     fuentes de masas, esto es para que el programa pueda considerar dentro de sus
    c?lculos las 4 fuentes de masa de manera simult?nea. Estos casos no aplican
    cargas externas, su funci?n es puramente num?rica para la formaci?n de
     matrices.
     2) ?Define? > ?Load Cases? > ?Add New Case?
     a. Load Case Type: Nonlinear Static.
     b. Mass Source: Seleccionar la fuente de masa desplazada
     correspondiente creada en el paso 1 (ej. Masa+X).
     c. Loads Applied: Asegurarse de que la lista de cargas est? vac?a (o
     con coeficientes cero).

    === PAG 31 ===
     174
     d. Aparecer? un mensaje de advertencia ?No Load Assignments are
     specified! Do you really want to closet he form??, debemos
     seleccionar ?S?? ya que es un caso auxiliar, que no considera
     cargas.
     e. Repetir este paso para cada una de las direcciones a analizar (+X,
     -X, +Y, -Y).
     Figura B.2 Men? para ingresar estado de carga para masa s?smica. Fuente:
     ETABS.

    === PAG 32 ===
     175
     Paso 3: Definici?n de Casos de An?lisis Modal Espec?ficos
     Dado que el centro de masa cambia, las propiedades din?micas (periodos y
     formas modales) tambi?n cambian. Se debe realizar un an?lisis modal
     independiente para cada excentricidad, para esto crearemos 4 casos modales:
    3) ?Define? > ?Load Cases? > ?Add New Case?
     a. Load Case Type: Modal.
     b. Subtype: Eigen.
     c. P-Delta/Nonlinear Stiffnes: Seleccionar la opci?n ?Use Nonlinear
     Case (Loads at End of Case NOT included)?.
     d. Case Selection: Escoger el caso est?tico no lineal auxiliar creado
     en el paso 2 (ej. +XMasa).
     e. Repetir este paso para cada una de las direcciones a analizar (+X,
     -X, +Y, -Y).
     Al seleccionar el caso no lineal, ETABS importa autom?ticamente la matriz de
    masa asociada a ese caso.

    === PAG 33 ===
     176
     Figura B.3 Men? para ingresar casos modales para masa s?smica. Fuente: ETABS.
    Paso 4: Generaci?n de Casos de Espectro de Respuesta (Response Spectrum)
     Finalmente, se configuran los casos s?smicos de dise?o utilizando los modos de

    vibrar que ya incorporan el efecto din?mico de la torsi?n accidental.
     4) ?Define? > ?Load Cases? > ?Add New Case?
     a. Load Case Type: Response Spectrum.
     b. Modal Case: Seleccionar el caso modal espec?fico creado en el
     paso 3 (ej. Modal+X).
     c. Loads Applied: Asignar la funci?n de espectro (Original o
     Consistente) con la aceleraci?n de la gravedad y la direcci?n
     correspondiente (U1 para sismo en X o U2 para sismo en Y).

    === PAG 34 ===
     177
     d. Diaphragm Eccentricity: En esta secci?n se debe dejar el valor en
     0, dado que la excentricidad ya est? incluida f?sicamente en la
     matriz de masa del an?lisis modal seleccionado.
     Figura B.4 Men? para ingresar estado de carga para sismo con torsi?n
     accidental debido a
     movimiento del centro de masa. Fuente: ETABS.

    === PAG 35 ===
     178
     ? M?todo b forma 1: Aplicando torsi?n accidental est?tica en cada piso.
     Para aplicar lo indicado en el inciso b de la normativa, primeramente, se har?

    correr el modelo sin considerar la torsi?n accidental. De este modelo se
     obtendr?n los esfuerzos de corte basal por piso combinados mediante CQC, con
    estos esfuerzos de corte se determina la diferencia de los cortes combinados
    en
     cada piso. Ejemplo piso k, seria (Qk-Qk+1) y se multiplica por la
     excentricidad
     accidental en piso k especificada en la norma.
     Paso 1: Configuraci?n del Modelo Base (Sin Excentricidad)
     Para aplicar el M?todo b, el an?lisis modal espectral de base debe estar libre
    de
     efectos torsionales accidentales din?micos.
     1) ?Define? > ?Mass Source?
     a. Asegurarse de que la fuente de masa utilizada para el an?lisis
     espectral tenga el valor 0 (cero) en la opci?n ?Move Mass Centroid
     over Diaphragm?.
     b. Correr el an?lisis del modelo (Run Analysis) con los casos
     espectrales est?ndar (Sx y Sy).
     Figura B.5 Men? ?Mass Source?, sin desplazamiento de centro de masa. Fuente:
    ETABS.
     H2: Forma b) Normativa Vigente
     Se puede hacer de 2 formas en ETABS. Las llamaremos forma 1 y forma 2
     Forma 1:

    === PAG 36 ===
     179
     Paso 2 Obtenci?n de Cortes de Entrepiso (Story Shears)
     El software generar? el gr?fico de distribuci?n de corte en altura.
     2) ?Display? > ?Story Response Plots?
     a. Display Type: Desplegar la lista y seleccionar Story Shears.
     b. Case/Combo:
     Seleccionar
     el
     caso
     de
     an?lisis
     espectral
     correspondiente a la direcci?n de an?lisis (Sismo_X o Sismo_Y, ver
     Figura B.6).
     c. Para el c?lculo num?rico, se deben tomar los valores tabulados que
     aparecen en la parte inferior de la ventana o exportar la tabla a
     Excel (clic derecho sobre la tabla > Export to Excel).
     Se requieren los valores de corte de cada piso para ambas direcciones de
     an?lisis
     (X e Y).
     Estos mismos esfuerzos pueden obtenerse mediante la funci?n ?Show Table?,
     para esto:
     2) ?Display? > ?Show Tables?
     a. Seleccionar la casilla ?ANALYSIS RESULTS? > ?Structure Output?
     > ?Other Output Items? > ?Table: Story Forces?.
     b. Con la tabla desplegada debemos aplicar el filtro para el ?Output
     Case? para que solo nos muestre los resultados para el Load Case
     del sismo que se quiere analizar, ver Figura B.7.
     c. En esta tabla se debe leer el valor de corte en la direcci?n del sismo
     (Vx para sismo en X y Vy para sismo en Y), estos est?n ordenados
     por piso y por locaci?n (Top o Bottom).

    === PAG 37 ===
     180
     Figura B.6 Men? para extraer los esfuerzos de corte por piso, para sismo en X.
    Fuente: ETABS.
     Figura B.7 Men? para extraer los esfuerzos de corte por piso con ?Show Table?.
    Fuente: ETABS.

    === PAG 38 ===
     181
     Paso 3: C?lculo de Momentos Torsores Est?ticos
     Mediante una planilla Excel, se obtienen los momentos torsores seg?n lo
     indicado
     en el punto 6.3.4 b) de la NCh433, indicado en el inciso 3.3.4.2 de esta
     memoria.
     Es importante aclarar que los cortes obtenidos por el Paso 2 son los
     acumulados
     para cada piso, por lo que se debe hacer la diferencia entre el piso superior
    e
     inferior para poder realizar el c?lculo del momento.
     Paso 4: Definici?n de Patrones de Carga para Torsi?n (User Defined)
     Se deben crear patrones de carga est?ticos para ingresar los momentos
     calculados manualmente.
     4) ?Define? > ?Load Patterns?
     a. Type: Seismic.
     b. Self Weight Multiplier: 0.
     c. Auto Lateral Load: Seleccionar User Defined.
     Figura B.8 Opci?n para ingresar los momentos est?ticos de torsi?n accidental,
    calculados a mano.
     Fuente: ETABS.

    === PAG 39 ===
     182
     Ingreso de Cargas:
     a. Hacer clic en Modify Lateral Load.
     b. Asegurarse de que la opci?n "Apply at Center of Mass" est?
     marcada.
     c. Copiar los valores calculados de momentos torsores desde la
     planilla Excel y pegarlos en la columna Mz correspondiente a cada
     piso.
     d. Las columnas Fx y Fy deben permanecer en 0.
     Figura B.9 Men? "Modify Lateral Load?. Fuente: ETABS.

    === PAG 40 ===
     183
     ? M?todo b forma 2: Entregando la excentricidad para cada piso.
     Una vez calculados los valores de excentricidad en cada piso seg?n lo indicado

    en el punto 6.3.4 b) de la NCh433, indicado en el inciso 3.3.4.2 de esta
     memoria.
     Se procede a ingresarlos en el programa para que realice el procedimiento
     conocido como m?todo b) forma 2:
     Paso 1: Configuraci?n del Caso Espectral
     Se procede a ingresar estos valores directamente en la configuraci?n del caso
    de
     carga espectral.
     1) ?Define? > ?Load Cases?
     a. Seleccionar el caso espectral a modificar (Sx o Sy) y hacer clic en
     Modify/Show Case.
     b. Localizar el apartado ?Diaphragm Eccentricity?.
     c. Hacer clic en el bot?n Modify/Show.
     Figura B.10 Opci?n para ingresar las excentricidades para los diafragmas por
    piso. Fuente: ETABS.
     Forma 2

    === PAG 41 ===
     184

    Es importante que la opci?n ?Eccentricity Ratio? tenga un valor de 0, luego:
    d. Se listar?n todos los diafragmas definidos en el modelo (en caso de
     haber m?s de un diafr?gma definido), es importante seleccionar
     aquel que corresponda al piso analizado.
     e. Para cada piso, en la columna Eccentricity, se debe ingresar el valor
     calculado de la excentricidad en cada piso.
     Este valor se ingresa como una longitud positiva. El programa internamente

02:42 PM `<synthetic>`
  ⎿  API Error: Claude's response exceeded the 32000 output token maximum. To configure
     this behavior, set the CLAUDE_CODE_MAX_OUTPUT_TOKENS environment variable.
  ⎿  Interrupted · What should Claude do instead?

---



 Bash(PYTHONIOENCODING=utf-8 python -c "
      import fitz…)
  ⎿  === PAG 28 ===

    P
     … +124 lines (ctrl+o to expand)
  ⎿  API Error: Claude's response exceeded the 32000 output token maximum. To configure this
     behavior, set the CLAUDE_CODE_MAX_OUTPUT_TOKENS environment variable.
