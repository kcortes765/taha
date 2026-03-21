# ETABS v19.1 - Referencia Completa de Interfaz

Fuente: Manual de ETABS v19.pdf (238 paginas)

---

## INDICE DE MENUS PRINCIPALES

| Menu | Pagina | Descripcion |
|------|--------|-------------|
| File | 32 | Archivos: nuevo, abrir, guardar, importar, exportar |
| Edit | 36 | Edicion: copiar, replicar, extruir, mesh, editar frames/shells |
| View | 74 | Vistas: 3D, planta, elevacion, opciones de display |
| Define | 79 | Definir propiedades: materiales, secciones, cargas, funciones |
| Draw | 127 | Dibujar: frames, shells, muros, tendones, section cuts |
| Select | 144 | Seleccionar objetos por diversos criterios |
| Assign | 145 | Asignar: restraints, cargas, diafragmas, mesh, releases |
| Analyze | 172 | Analizar: check model, DOF, run, mesh options |
| Display | 176 | Mostrar resultados: deformada, fuerzas, tablas, story plots |
| Design | 195 | Disenar: acero, concreto, compuesto, muros, losas |

---

## 1. MENU FILE: ARCHIVOS (p.32)

| Comando | Ruta | Descripcion |
|---------|------|-------------|
| New Model | File > New Model | Crear modelo nuevo. Opciones: usar defaults, copiar de existente, o iniciar con plantilla |
| Open | File > Open | Abrir modelo .edb existente |
| Save / Save As | File > Save | Guardar modelo actual |
| Show Input/Output Text Files | File > Show Input/Output | Mostrar archivos de texto de entrada/salida |
| Import | File > Import | Importar desde: AutoCAD .dxf, ProSteel .mdb, Excel, Revit .exr, ETABS .e2k |
| Export | File > Export | Exportar a: AutoCAD .dxf, ProSteel, Revit .exr, ETABS .e2k, Perform3D, Access |
| Print Setup | File > Print Setup | Configurar impresora, orientacion de hoja |
| Print Graphics | File > Print Graphics | Vista preliminar e impresion del grafico actual |
| Create Report | File > Create Report | Generar reporte del proyecto (resumen o detallado) |
| Capture Picture | File > Capture Picture | Captura de pantalla. Guardar como DXF, DWG o PDF. Ventana completa o solo viewport |
| Create Video | File > Create Video | Generar video del modelo |
| Project Information | File > Project Information | Datos del proyecto |
| Comments and Log | File > Comments and Log | Comentarios y registro |
| Upload to CSI Cloud | File > Upload to CSI Cloud | Subir modelo a la nube de CSI |
| Exit | File > Exit | Salir de ETABS |

### Plantillas al crear New Model (p.15-30)

| Plantilla | Descripcion |
|-----------|-------------|
| Blank | Entorno en blanco |
| Grid Only | Solo grilla 3D |
| Steel Deck | Porticos de acero con correas. Opciones: volados X/Y, tipo rigidez uniones, base, diafragma, cargas |
| Staggered Truss | Acero con cerchas espaciales. Incluye Vierendeel, cordones sup/inf, diagonales |
| Flat Slab | HA con losa maciza + capiteles + columnas |
| Flat Slab with Perimeter Beams | HA con losa maciza + capiteles + vigas perimetrales |
| Waffle Slab | HA con losa reticular + capiteles + nervios |
| Two Way or Ribbed Slab | HA con vigas en 2 direcciones + losa nervada |

Parametros comunes de plantillas:
- Grid spacing X/Y, numero de lineas, etiquetas
- Custom grids (nombre individual, tipo primario/secundario, visibilidad, color)
- Alturas de piso: uniforme o personalizada por piso
- Master Story / Similar To (pisos maestros y similares)
- Restricciones base (pinned/fixed/none), diafragma (rigido/semi/none)
- Secciones de vigas, columnas, losa. Patrones de carga (Dead/Live)

---

## 2. MENU EDIT: EDICION (p.36)

| Comando | Ruta | Descripcion | Parametros clave |
|---------|------|-------------|------------------|
| Undo/Redo | Edit > Undo/Redo | Deshacer/rehacer acciones | - |
| Cut/Copy/Paste | Edit > Cut/Copy/Paste | Cortar, copiar, pegar objetos | - |
| Delete | Edit > Delete | Borrar objetos seleccionados | - |
| Paste Coordinates | Edit > Paste Coordinates | Pegar coordenadas desde portapapeles | - |
| Add to Model from Template | Edit > Add to Model from Template | Agregar estructura predefinida 2D o 3D al modelo existente | Frame 2D, Armazon 2D, Pared 2D, o plantillas 3D (Steel Deck, etc.) + offset X/Y/Z/rotacion |
| **Edit Stories and Grid Systems** | Edit > Edit Stories and Grid Systems | Editar pisos y grillas | Modificar/agregar pisos, importar/exportar .dxf de grids |
| Add Grid Lines at Selected Joints | Edit > Add Grid Lines | Agregar ejes de referencia en puntos seleccionados | Orientacion: paralelo a X/Y, o angulo definido |
| Interactive Database | Edit > Interactive Database | Base de datos interactiva para edicion masiva | - |

### 2.4 Replicate (Replicas) (p.40-47)

| Tipo | Ruta | Descripcion | Parametros |
|------|------|-------------|------------|
| Linear | Edit > Replicate > Linear | Replica lineal de objetos seleccionados | dx, dy, dz; numero de copias; borrar originales |
| Radial | Edit > Replicate > Radial | Replica rotacional | Centro (x,y); angulo; numero de copias |
| Mirror | Edit > Replicate > Mirror | Replica por simetria | Linea de simetria definida por 2 puntos |
| Story | Edit > Replicate > Story | Replica a otros pisos | Seleccionar pisos destino |
| Replicate Options | Edit > Replicate > Options | Propiedades a incluir en la replica | Seleccionar que asignaciones copiar |

### 2.5 Extrude (Extruir) (p.48-59)

| Tipo | Ruta | Descripcion | Parametros |
|------|------|-------------|------------|
| Joints to Frames (Linear) | Edit > Extrude > Joints to Frames > Linear | Crear frames a partir de puntos | dx/dy/dz, numero de extrusiones |
| Joints to Frames (Radial) | Edit > Extrude > Joints to Frames > Radial | Crear frames radialmente | Centro, angulo, cantidad, total drop |
| Frames to Shells (Linear) | Edit > Extrude > Frames to Shells > Linear | Crear shells a partir de frames | Longitud, cantidad de shells |
| Frames to Shells (Radial) | Edit > Extrude > Frames to Shells > Radial | Crear shells radialmente | Eje rotacion, angulo, cantidad, descenso |

### 2.6-2.8 Edicion geometrica (p.60-63)

| Comando | Ruta | Descripcion |
|---------|------|-------------|
| Merge Joints | Edit > Merge Joints | Unir puntos cercanos segun tolerancia |
| Align Points to X/Y/Z | Edit > Align > Align Points to Ordinate | Alinear puntos a una coordenada especifica |
| Align to Nearest Line | Edit > Align > Align to Nearest Line | Alinear a la linea mas cercana |
| Trim Objects | Edit > Align > Trim Objects | Cortar sobrante de linea hasta interseccion |
| Extend Lines | Edit > Align > Extend Lines | Extender lineas |
| Move Points/Lines/Areas | Edit > Move | Mover objetos seleccionados en dx/dy/dz |

### 2.9 Edit Frames (p.63-64)

| Comando | Ruta | Descripcion |
|---------|------|-------------|
| Divide Frames | Edit > Edit Frames > Divide | Dividir en grids visibles, puntos seleccionados, o N segmentos |
| Join Frames | Edit > Edit Frames > Join | Unir frames colineales |
| Reverse Connectivity | Edit > Edit Frames > Reverse | Invertir conectividad i-j |
| Modify/Show Frame Type | Edit > Edit Frames > Modify/Show Type | Ver/cambiar tipo de frame (viga/columna/brace) |

### 2.10 Edit Shells (p.65-73)

| Comando | Ruta | Descripcion | Parametros |
|---------|------|-------------|------------|
| Mesh Areas (Cookie Cut Horizontal) | Edit > Edit Shells > Mesh Areas | Dividir area con lineas horizontales seleccionadas | Seleccionar linea de corte |
| Mesh Areas (Cookie Cut at Angle) | Edit > Edit Shells > Mesh Areas | Dividir a un angulo entre puntos seleccionados | Angulo (ej: 45) |
| Mesh Quads/Triangles NxM | Edit > Edit Shells > Mesh Areas | Dividir area en NxM cuadrados | N por M areas |
| Mesh at Grids/Points/Lines | Edit > Edit Shells > Mesh Areas | Dividir en intersecciones de grids, puntos o lineas | Seleccionar criterio |
| Merge Areas | Edit > Edit Shells > Merge Areas | Unir shells en uno solo | Elegir propiedades/asignaciones de cual shell |
| Expand/Shrink Shells | Edit > Edit Shells > Expand/Shrink | Expandir o reducir el tamano | Valor de expansion/reduccion |
| Slab Rebar Object Data | Edit > Edit Shells > Slab Rebar | Definir refuerzo de losa | Capa, tamano barra, material, locacion vertical, espaciamiento |
| Add Design Strips | Edit > Edit Shells > Add Design Strips | Agregar flejes de diseno | Grid system, direccion, capa (A/B), grosor auto/manual |
| Explode Mesh | Edit > Edit Shells > Explode Mesh | Separar malla en shells individuales | - |
| Convert to User Mesh | Edit > Edit Shells > Convert to User Mesh | Convertir auto-mesh en definido por usuario | - |
| Reverse Wall Local 3 | Edit > Edit Shells > Reverse Wall | Invertir eje local 3 del muro | - |
| Divide Walls for Openings | Edit > Edit Shells > Divide Walls | Dividir muros para crear aberturas | - |

---

## 3. MENU VIEW: VER (p.74-78)

| Comando | Ruta | Descripcion | Parametros |
|---------|------|-------------|------------|
| Set 3D View | View > Set 3D View | Vista 3D | Angulo horizontal, vertical, apertura. Vistas rapidas predefinidas |
| Set Plan View | View > Set Plan View | Vista en planta | Seleccionar nivel/piso |
| Set Elevation View | View > Set Elevation View | Vista en elevacion | Seleccionar elevacion. Agregar/borrar/renombrar elevaciones. Filtros: incluir grids o definidas por usuario |
| Set Building View Limits | View > Set Building View Limits | Limites de visualizacion | Rango X/Y, rango de pisos. Ignorar limites |
| Set Display Options | View > Set Display Options | Opciones visuales del modelo | Asignaciones a objetos, otras opciones visuales |
| Change Axes Location | View > Change Axes Location | Mover origen de ejes | Coordenadas X/Y/Z |
| Zoom (Window/In/Out) | View > Zoom | Controles de zoom | Ventana, acercar, alejar, restaurar |
| Pan | View > Pan | Mover pantalla | - |
| Show/Hide Grid | View > Show/Hide Grid | Mostrar/ocultar grilla | - |
| Show Axes | View > Show Axes | Mostrar ejes | - |
| Show Only Selected | View > Show Only Selected | Ver solo objetos seleccionados | - |
| Invert Visibility | View > Invert Visibility | Invertir visibilidad | - |
| Make Invisible | View > Make Invisible | Ocultar seleccion | - |
| Show All | View > Show All | Mostrar todos los objetos | - |
| Refresh View | View > Refresh View | Actualizar pantalla | - |
| Rendered View | View > Rendered View | Vista renderizada | - |
| DirectX Options | View > DirectX Options | Opciones DirectX | - |

---

## 4. MENU DEFINE: DEFINIR (p.79-126)

### 4.1 Materials Properties (Propiedades de Materiales) (p.80-82)

**Ruta**: Define > Material Properties

Opciones: Add New, Add Copy, Modify/Show, Delete

#### Tipo CONCRETO (CONC)
| Parametro | Descripcion |
|-----------|-------------|
| Name | Nombre del material |
| Type | Isotrópico u ortotropico |
| Grade | Grado del material |
| f'c | Compresion especifica (MPa) |
| Ec (Modulo elasticidad) | Modulo de Young |
| Weight per Volume | Peso especifico (kN/m3 o tonf/m3) |
| Mass per Volume | Masa/volumen |
| Poisson Ratio | Relacion de Poisson |
| Thermal Expansion Coeff | Coeficiente expansion termica |
| Shear Modulus | Modulo de corte |
| Shear Reduction Factor | Factor reduccion cortante |
| Propiedades de diseno | Parametros para diseno segun codigo |

#### Tipo ACERO (STEEL)
| Parametro | Descripcion |
|-----------|-------------|
| Fy (min yield) | Limite elastico minimo |
| Fu (min tensile) | Resistencia minima a la tension |
| Fye (expected yield) | Limite elastico esperado |
| Fue (effective tensile) | Resistencia efectiva a la tension |
| E | Modulo de elasticidad |
| Poisson | Relacion de Poisson |
| Weight/Mass per Volume | Peso y masa especificos |

### 4.2 Section Properties (Propiedades de Seccion) (p.83-102)

**Ruta**: Define > Section Properties > [tipo]

Submenu completo:
- Frame Sections
- Tendon Sections
- Wall/Slab/Deck Sections
- Reinforcing Bar Sizes
- Link Properties
- Nonlinear Hinges
- Panel Zone

#### 4.2.1 Frame Sections (p.84-92)

**Ruta**: Define > Section Properties > Frame Sections

| Tipo seccion | Parametros geometricos | Notas |
|--------------|----------------------|-------|
| I/Wide Flange | t3 (altura), t2 (ancho ala sup), tf (espesor ala sup), tw (espesor alma), t2b (ancho ala inf), tfb (espesor ala inf) | Doble T |
| Channel (U) | t3, t2, tf, tw | Canal |
| Tee (T) | Total Depth, Total Width, Flange Thickness, Web Thickness, Z (radio doblado) | T |
| Angle (L) | t3 (ala vertical), t2 (ala horizontal), tf, tw | Angulo |
| Double Angle (2L) | t3, t2, tf, tw, dis (distancia back-to-back) | Doble angulo |
| Box Tube | t3 (altura), t2 (ancho), tf (espesor alas), tw (espesor almas) | Tubo rectangular |
| Pipe | t3 (diametro exterior), tw (espesor pared) | Tubo circular |
| Rectangular | t3 (Depth), t2 (Width) | Seccion HA mas comun |
| Circle | t3 (Diameter) | Seccion circular HA |
| General | Propiedades ingresadas manualmente (A, I, J, etc.) | Seccion generica |
| Auto Select | Lista de secciones para diseno iterativo acero | Solo acero |
| SD (Section Designer) | Geometria arbitraria dibujada | Cualquier forma, incluye refuerzo arbitrario |
| Nonprismatic | Secciones variables: IOFF, L, JOFF; variacion EI lineal/parabolica/cubica | Vigas de seccion variable |

**Para secciones rectangulares HA (vigas)**:
- Refuerzo Ductil: Permite colocar refuerzo real a flexion en extremos de viga
- Top Left, Top Right, Bottom Left, Bottom Right: refuerzo en cada esquina
- Recubrimiento superior e inferior
- Tipo de diseno: viga o columna
- Check (revisar) vs Design (disenar)

**Para secciones rectangulares HA (columnas)**:
- Configuracion: rectangular o circular
- Confinamiento: ties (ligaduras) o spiral (zunchos)
- Parametros de refuerzo: numero de barras, recubrimiento, diametro
- Check vs Design

**Section Designer (SD)** (p.88-90):
- Herramientas de dibujo para secciones arbitrarias
- Puede incluir concreto + acero de refuerzo
- Genera diagramas momento-curvatura
- Genera diagramas de interaccion P-M
- Tipo: columna o viga
- Refuerzo: rectangular/circular, ties/spiral

#### 4.2.2 Wall/Slab/Deck Sections (p.93-100)

**Ruta**: Define > Section Properties > Wall/Slab/Deck Sections

Opciones: Add New, Add Copy, Modify/Show, Delete

##### Tipo SLAB (Losa) (p.93)
| Parametro | Descripcion |
|-----------|-------------|
| Name | Nombre de la seccion |
| Material | Material asignado |
| Modeling Type | Shell-Thin, Shell-Thick, Membrane, Plate-Thin, Plate-Thick |
| Type | Slab |
| Thickness | Espesor de la losa |

##### Tipo DECK (p.94-95)
| Subtipo | Descripcion |
|---------|-------------|
| Filled Deck | Concreto vaciado con encofrado colaborante (composite) |
| Unfilled Deck | Lamina metalica sin concreto |
| Solid Slab | Concreto vaciado sin encofrado colaborante |

Parametros: geometria de deck (alturas, anchos), materiales (concreto + acero)

##### Tipo WALL (Muro) (p.96-100)
| Parametro | Descripcion |
|-----------|-------------|
| Name | Nombre |
| Material | Material |
| Type | Shell, Membrane, o Plate |
| Modeling Type | Shell-Thin, Shell-Thick |
| Thickness (bending) | Espesor para deformacion a flexion |
| Thickness (shear) | Espesor para deformacion a corte |
| Load distribution | Distribucion en 1 direccion |

**Tipos de elemento de area** (CRITICO para modelacion):

| Tipo | GDL por nodo | Comportamiento | Usar para |
|------|-------------|----------------|-----------|
| **Membrane** | 2 (U1, U2 en plano) | Solo fuerza axial en plano. Sin flexion. Mecanismo si carga perpendicular (ETABS convierte a Shell automaticamente) | Losas simplemente apoyadas (area tributaria), muros bajo cargas en su plano |
| **Plate** | 3 (U3, R1, R2 fuera plano) | Solo flexion. Mecanismo si carga en plano | Losas macizas bajo cargas perpendiculares (MEF) |
| **Shell** | 5 (U1, U2, U3, R1, R2) | Membrana + Plate. Estable ante cualquier carga | **EL MAS USADO**. Muros y losas generales |

**Formulacion Shell**:
- **Thin (Kirchhoff)**: Si L/T > 20. Despreciar deformacion a corte. Mas rapido
- **Thick (Mindlin)**: Si L/T < 20. Incluir deformacion a corte. Para elementos gruesos

#### 4.2.6 Reinforcing Bar Sizes (Barras de refuerzo) (p.101)
**Ruta**: Define > Section Properties > Reinforcing Bar Sizes
- Limpiar/organizar seleccion, agregar grupo de barras comerciales

#### 4.2.7 Link Properties (p.101-102)
**Ruta**: Define > Section Properties > Link Properties
- Tipos de links: Linear, Multi-Linear Elastic, Multi-Linear Plastic, Gap, Hook, Damper, Friction Isolator, Rubber Isolator, etc.
- Propiedades: masa, peso, inercia rotacional, rigidez por direccion, factores para lineas/resortes

#### 4.2.8 Frame/Wall Nonlinear Hinges (Rotulas) (p.102)
**Ruta**: Define > Section Properties > Nonlinear Hinges
- Definir propiedades de rotulas plasticas para analisis pushover

### 4.3 Spring Properties (Resortes) (p.103-106)

**Ruta**: Define > Spring Properties

| Subtipo | Ruta | Parametros |
|---------|------|------------|
| Point Springs | Define > Springs > Point Springs | Rigidez traslacional/rotacional en ejes globales. Link a juntas. Basado en zapatas |
| Line Springs | Define > Springs > Line Springs | Rigidez. Direccion fuerza. No lineal: solo compresion/tension |
| Area Springs | Define > Springs > Area Springs | Rigidez. Direccion fuerza |
| Soil Profile Data | Define > Springs > Soil Profile | Capas de suelo, parametros por capa, factor reduccion corte, amortiguamiento |
| Isolated Column Footing | Define > Springs > Isolated Footing | Dimensiones zapata (largo, ancho, grosor), profundidad empotramiento |

### 4.4 Diaphragms (p.107)

**Ruta**: Define > Diaphragms

| Parametro | Opciones |
|-----------|----------|
| Name | Nombre del diafragma |
| Type | **Rigid** o **Semi-Rigid** |

- **Rigido**: Limita deformaciones axiales en plano. Solo 3 GDL (Ux, Uy, Rz) por planta. Usar cuando losa+vigas tienen rigidez muy alta en plano
- **Semi-Rigido (Flexible)**: Trabaja con rigidez real del conjunto. Cuando hay deformaciones relativas significativas en plano

Opciones: Add New, Modify/Show, Delete

### 4.5 Define Groups (p.108)
**Ruta**: Define > Groups
- Crear grupos de objetos para: seleccion rapida, section cuts, diseno compartido, salida selectiva

### 4.6 Section Cut (p.108)
**Ruta**: Define > Section Cut
- Nombre, grupo asociado, angulo orientacion respecto eje 1, criterio de suma global

### 4.7 Strain Gauges (p.109-110)
**Ruta**: Define > Strain Gauge Properties

| Tipo | Parametros |
|------|------------|
| Line Gauges | Nombre, direccion, criterios aceptacion (IO, LS, CP) |
| Quad Gauges | Nombre, direccion (Pier/Spandrel), tipo (corte/rotacion), criterios aceptacion |

### 4.8 Functions (p.111-113)

**Ruta**: Define > Functions

#### 4.8.1 Response Spectrum Functions (p.111-112)
**Ruta**: Define > Functions > Response Spectrum

| Opcion | Descripcion |
|--------|-------------|
| From File | Cargar espectro desde archivo .txt. Formato: frecuencia vs aceleracion, o periodo vs aceleracion |
| Convert to User Defined | Los datos del .txt se integran permanentemente al modelo |
| Codigos predefinidos | IBC, UBC, ASCE, Eurocode, NCh2745, etc. |

Opciones: Add, Modify, Delete. Ver grafica y archivo fuente

#### 4.8.2 Time History Functions (p.113)
**Ruta**: Define > Functions > Time History
- Lista de funciones predefinidas o desde archivo
- Grafica de la funcion, tabla de valores, parametros

### 4.9 Generalized Displacements (p.114)
**Ruta**: Define > Generalized Displacements
- Nombre, tipo (traslacional/rotacional), factores de escala

### 4.10 Mass Source Data (FUENTE DE MASA) (p.114-116)

**Ruta**: Define > Mass Source

**CRITICO PARA ANALISIS SISMICO**

| Opcion | Descripcion | Cuando usar |
|--------|-------------|-------------|
| From Self and Specified Mass | Masa del peso propio + masas adicionales | Solo peso propio |
| **From Loads** | Masa desde patrones de carga con factores (0 a 1). Incluir DEAD como carga | **Metodo NCh433: DEAD x1.0 + SCP x0.25** |
| From Self and Specified Mass and Loads | Peso propio + masas + cargas con factores. NO agregar DEAD (ya incluido en Self) | Cuando hay masas adicionales |

Parametros:
- Nombre
- Patrones de carga y multiplicador por cada uno
- Incluir masa lateral / masa vertical
- Masa lateral al nivel de pisos
- Ajuste masa lateral del diafragma (ratio espesor X/Y)

### 4.11 P-Delta Options (p.116)
**Ruta**: Define > P-Delta Options

| Metodo | Descripcion |
|--------|-------------|
| None | Sin P-Delta |
| Non-Iterative (Mass Based) | Basado en masa, no iterativo |
| **Iterative (Load Based)** | Basado en cargas, iterativo. Patron de carga + factor escala. Tolerancia convergencia |

### 4.12 Load Patterns (Patrones de Carga) (p.117-121)

**Ruta**: Define > Load Patterns

| Parametro | Descripcion |
|-----------|-------------|
| Name | Nombre del patron (ej: PP, SCP, SCT, SXE) |
| Type | DEAD, LIVE, SUPER DEAD, QUAKE, WIND, etc. |
| Self Weight Multiplier | Factor de peso propio. **Solo 1.0 en PP (DEAD). Los demas en 0** |
| Auto Lateral Load | Para tipo QUAKE: codigo sismico o User Coefficient/User Loads |

**Para carga sismica estatica (tipo QUAKE)**:

| Opcion | Descripcion |
|--------|-------------|
| Normas predefinidas | UBC97, IBC2000, IBC2003, NEHRP97, BOCA96, etc. |
| **User Coefficient** | Coeficiente sismico manual. Direccion, excentricidad, rango de pisos |
| User Loads | Cargas directas por piso/diafragma |

Parametros UBC-97 como ejemplo: Direccion/excentricidad, factor excentricidad diafragmas, factor importancia, tipo suelo, zona sismica, Ca, Cv, factor fuente cercana, R, rango pisos, periodo estimado

### 4.13 Shell Uniform Loads (p.121)
**Ruta**: Define > Shell Uniform Loads
- Crear sets de cargas uniformes (nombre + patron de carga + valor)

### 4.14 Load Cases (Casos de Carga) (p.122)

**Ruta**: Define > Load Cases

| Parametro | Opciones |
|-----------|----------|
| Name | Nombre del caso |
| Type | Static, Modal, Response Spectrum, Time History, Buckling, etc. |
| Applied Loads | Patrones de carga aplicados |
| Mass Source | Fuente de masa para el caso |

**Para casos espectrales (Response Spectrum)**:
- Caso modal asociado
- Metodo combinacion modal: **CQC**, SRSS, etc.
- Respuesta rigida: frecuencias, tipo periodica+rigida
- **Combinacion direccional**: SRSS, ABS, CQC3
- Factor de escala por funcion espectral

### 4.15 Load Combinations (Combinaciones de Carga) (p.123)

**Ruta**: Define > Load Combinations

| Tipo combinacion | Descripcion |
|------------------|-------------|
| **ADD (Additive)** | Suma algebraica con factores |
| **ENV (Envelope)** | Envolvente max/min |
| ABS (Absolute) | Suma de valores absolutos |
| SRSS | Raiz cuadrada de suma de cuadrados |

Parametros: nombre, casos de carga con factor de escala. Agregar combinaciones aleatorias

### 4.16 Auto Construction Sequence (p.124)
**Ruta**: Define > Auto Construction Sequence Case
- Secuencia de construccion paso a paso
- Combinar N pisos por fase, excluir grupos hasta ultima fase
- Opciones geometricas no lineales

### 4.17 Walking Vibrations (p.125)
**Ruta**: Define > Walking Vibrations
- Parametros: peso persona, factor carga, frecuencia, velocidad, duracion impacto
- Umbrales: oficina, centro comercial, puente, usuario
- Trayectoria de pasos, caso modal

### 4.18 Table Named Sets (p.126)
**Ruta**: Define > Table Named Sets
- Definir conjuntos de tablas para exportacion/visualizacion de resultados

---

## 5. MENU DRAW: DIBUJAR (p.127-143)

### 5.1 Draw Beam/Column/Brace Objects (Frames) (p.128-130)

| Herramienta | Ruta | Descripcion | Parametros |
|------------|------|-------------|------------|
| Draw Beam/Column/Brace | Draw > Draw Beam/Column/Brace | Dibujo libre de frame punto a punto | Tipo, propiedad, momento release, offset, tipo linea/control |
| Quick Draw Beam/Columns | Draw > Quick Draw Beam/Columns | Dibujo instantaneo en grids/puntos | Tipo, propiedad, momento release, offset, dibujar en (grids/punto) |
| Quick Draw Columns | Draw > Quick Draw Columns | Columnas instantaneas en planta | Propiedad, momento release, angulo, offset X/Y, punto cardinal |
| Quick Draw Secondary Beams | Draw > Quick Draw Secondary Beams | Vigas secundarias uniformemente espaciadas | Propiedad, espaciamiento, cantidad, orientacion (X/Y) |
| Quick Draw Braces | Draw > Quick Draw Braces | Tirantes/arriostramientos | Propiedad, momento release |

### 5.2 Draw Floor/Wall Objects (Shells) (p.131-137)

| Herramienta | Ruta | Descripcion | Parametros |
|------------|------|-------------|------------|
| Draw Floor/Wall | Draw > Draw Floor/Wall | Dibujar losa/muro punto a punto | Propiedad (muro/losa), eje local, tipo borde (linea/multilinea), control |
| Draw Rectangular Floor/Wall | Draw > Draw Rectangular Floor/Wall | Shell rectangular con 2 puntos | Propiedad, eje local, dimensiones |
| Quick Draw Floor/Wall | Draw > Quick Draw Floor/Wall | Shell instantaneo | Propiedad, eje local, dibujar usando (grids, perimetro, puntos) |
| Quick Draw Area Around Point | Draw > Quick Draw Area Around Point | Area alrededor de un punto | Forma (rectangular/circular), propiedad, dimensiones |
| **Draw Walls** | Draw > Draw Walls | Dibujar muros con etiquetas automaticas | Tipo area (Pier/Spandrel), propiedad (muro/abertura), offset, auto-asignar tipo |
| **Quick Draw Walls** | Draw > Quick Draw Walls | Muros instantaneos | Tipo area, propiedad, offset, auto-asignar, dibujar en (grids/puntos) |
| **Draw Wall Openings** | Draw > Draw Wall Openings | Aberturas en muros existentes | Grosor, altura, distancia inferior, distancia izquierda |

**Elementos Pier vs Spandrel** (p.135-137):
- **Pier**: Muro con comportamiento tipo columna. Variacion V y M vertical (eje Z). Diseno reporta acero flexo-compresion + corte en extremos superior e inferior
- **Spandrel**: Muro con comportamiento tipo viga-dintel. Variacion V y M horizontal (eje X/Y). Diseno reporta acero flexion + corte + diagonal en extremos izquierdo y derecho

### 5.3-5.8 Otras herramientas de dibujo

| Herramienta | Ruta | Descripcion |
|------------|------|-------------|
| Draw Tendon | Draw > Draw Tendon | Dibujar tendones postensados. Perfil, luz, sistema, cargas, efecto elevacion |
| Draw Section Cut | Draw > Draw Section Cut | Linea de corte para analizar fuerzas/momentos. Funciona en frames y shells |
| Developed Elevation | Draw > Developed Elevation | Vista en elevacion desarrollada. Linea en planta para seleccionar secciones |
| Draw Wall Stacks | Draw > Draw Wall Stacks | Nucleos de muros (pilas de muros verticales) |
| Auto Draw Cladding | Draw > Auto Draw Cladding | Revestimiento automatico. Usar pisos/vigas/columnas/solo seleccionados |
| Draw Strain Gauge (Line) | Draw > Draw Line Strain Gauge | Galga extensometrica lineal |
| Draw Strain Gauge (Quad) | Draw > Draw Quad Strain Gauge | Galga extensometrica cuadruple |
| Snap Options | Draw > Snap Options | Opciones de puntero/snap para precision |
| Work Planes | Draw > Work Planes | Planos de trabajo para dibujo |

---

## 6. MENU SELECT: SELECCIONAR (p.144-145)

| Comando | Ruta | Descripcion |
|---------|------|-------------|
| Select | Select > Select | Seleccion individual por clic |
| Select via Polygon | Select > Select via Polygon | Seleccionar con poligono |
| Select via Intersecting Polygon | Select > via Intersecting Polygon | Poligono intersecante |
| Select via Intersecting Line | Select > via Intersecting Line | Linea intersecante |
| Select via Coordinates | Select > via Coordinates | Por coordenadas |
| Select by Object Type | Select > by Object Type | Por tipo (Joint, Frame, Shell, Link, Tendon) |
| Select by Properties | Select > by Properties | Por propiedad de seccion/material |
| Select by Labels | Select > by Labels | Por etiquetas (Pier, Spandrel) |
| Select by Groups | Select > by Groups | Por grupo definido |
| Select All on Story | Select > All on Story | Todo un piso |
| Select All | Select > All | Todo el modelo |
| Deselect | Select > Deselect | Deseleccionar |
| Invert Selection | Select > Invert | Invertir seleccion |
| Previous Selection | Select > Previous Selection | Seleccion anterior |
| Deselect All | Select > Deselect All | Deseleccionar todo |

---

## 7. MENU ASSIGN: ASIGNAR (p.145-171)

### 7.1 Joint (Juntas) (p.146)

| Comando | Ruta | Descripcion | Parametros |
|---------|------|-------------|------------|
| **Restraints** | Assign > Joint > Restraints | Apoyos/restricciones | Empotrado, fijo, movil, ninguno. Restricciones por direccion global |
| Springs | Assign > Joint > Springs | Resortes en junta | Seleccionar propiedad de resorte definida |
| **Diaphragm** | Assign > Joint > Diaphragm | Asignar diafragma a junta | Seleccionar diafragma definido |
| Panel Zone | Assign > Joint > Panel Zone | Zona de panel | - |
| Additional Mass | Assign > Joint > Additional Mass | Masa adicional en junta | Masa en direcciones globales, momentos de inercia |
| Floor Meshing Options | Assign > Joint > Floor Meshing | Opciones mallado piso por juntas | - |

### 7.2 Frame (p.147-155)

| Comando | Ruta | Descripcion | Parametros clave |
|---------|------|-------------|------------------|
| Section Property | Assign > Frame > Section Property | Asignar seccion frame | Seleccionar seccion definida |
| Property Modifiers | Assign > Frame > Property Modifiers | Modificadores de rigidez | Factores para A, I22, I33, J, As2, As3, masa, peso |
| **Frame Release/Partial Fixity** | Assign > Frame > Releases | Liberacion de extremos / rigidez parcial | Liberar M2, M3, V2, V3, T, P en extremo i/j. Rigidez parcial via resorte |
| **End Length Offsets** | Assign > Frame > End Offsets | Longitud rigida en extremos (luz libre) | Automatico desde conectividad, longitud definida, factor zona rigidez. Peso propio: auto/longitud completa/luz libre |
| **Insertion Points** | Assign > Frame > Insertion Point | Punto de insercion/excentricidad | Punto referencia (top, bottom, centroid, left, right, etc.), excentricidad, sistema coord. Opcion: no modificar rigidez |
| Local Axes | Assign > Frame > Local Axes | Orientacion ejes locales | Rotar angulo desde posicion original/actual, orientar eje mayor en X/radial |
| Output Station | Assign > Frame > Output Station | Puntos de analisis a lo largo del frame | Max/min espaciamiento de estacion |
| Tension/Compression Limits | Assign > Frame > T/C Limits | Limites tension/compresion | Valores limite |
| **Hinges** | Assign > Frame > Hinges | Rotulas plasticas | Propiedad rotula, tipo locacion, distancia relativa/absoluta |
| Line Springs | Assign > Frame > Line Springs | Resortes lineales | - |
| Additional Mass | Assign > Frame > Additional Mass | Masa adicional | - |
| Pier Label | Assign > Frame > Pier Label | Etiqueta Pier | Asignar etiqueta pier al frame |
| Spandrel Label | Assign > Frame > Spandrel Label | Etiqueta Spandrel | Asignar etiqueta spandrel al frame |
| **Auto Mesh** | Assign > Frame > Auto Mesh | Mallado automatico de frame | Mesh en puntos intermedios, intersecciones con otros frames/bordes, min/max segmentos |
| Floor Meshing Options | Assign > Frame > Floor Meshing | Incluir frame en malla de piso | Determinado por programa, incluir, no incluir |
| Moment Connection Type | Assign > Frame > Moment Connection | Tipo conexion momento viga | Tipo conexion, ubicacion, reduccion seccion (RBS) |
| Column Splice Overwrite | Assign > Frame > Column Splice | Empalme columna | Sin empalme, o a altura sobre piso |
| Nonprismatic Parameters | Assign > Frame > Nonprismatic | Parametros seccion variable | Seccion no prismatica, distancia relativa |
| Material Overwrite | Assign > Frame > Material Overwrite | Sobrescribir material | - |

### 7.3 Shell (p.156-165)

| Comando | Ruta | Descripcion | Parametros clave |
|---------|------|-------------|------------------|
| Slab Section | Assign > Shell > Slab Section | Asignar seccion losa | Seleccionar seccion |
| Deck Section | Assign > Shell > Deck Section | Asignar seccion deck | Seleccionar seccion |
| Wall Section | Assign > Shell > Wall Section | Asignar seccion muro | Seleccionar seccion |
| Opening | Assign > Shell > Opening | Marcar como abertura | - |
| **Stiffness Modifiers** | Assign > Shell > Stiffness Modifiers | Modificadores de rigidez de shell | f11, f22, f12, m11, m22, m12, v13, v23, masa, peso |
| Thickness Overwrites | Assign > Shell > Thickness Overwrites | Sobrescribir espesor | Por punto, especificado punto a punto, quitar |
| **Insertion Point** | Assign > Shell > Insertion Point | Punto de insercion shell | Punto cardinal, offset nodos en ejes locales, sistema coordenadas |
| **Diaphragm** | Assign > Shell > Diaphragm | Asignar diafragma a shell | Seleccionar diafragma |
| Edge Releases | Assign > Shell > Edge Releases | Liberar bordes del shell | Corte en plano, fuerza normal, corte fuera plano, momento flexor, momento torsor por borde |
| Rib Location | Assign > Shell > Rib Location | Ubicacion de nervios (losa nervada) | Punto X, Y |
| Local Axes | Assign > Shell > Local Axes | Orientacion ejes locales | Rotar desde angulo default o actual |
| Area Springs | Assign > Shell > Area Springs | Resortes en area | - |
| Additional Mass | Assign > Shell > Additional Mass | Masa adicional | Cantidad de masa |
| **Pier Label** | Assign > Shell > Pier Label | Etiqueta Pier para muros | Asignar etiqueta Pier (para diseno de muros) |
| **Spandrel Label** | Assign > Shell > Spandrel Label | Etiqueta Spandrel para muros | Asignar etiqueta Spandrel (para diseno vigas dintel) |
| Wall Hinge | Assign > Shell > Wall Hinge | Rotula de muro | Lista de rotulas, agregar/reemplazar |
| Reinforce Wall Hinges | Assign > Shell > Reinforce Wall Hinges | Refuerzo para rotulas muro | Ratio refuerzo uniforme (V/H), capa refuerzo, material, geometria, detalle flexion/corte |
| **Floor Auto Mesh Options** | Assign > Shell > Floor Auto Mesh | Mallado automatico pisos | **Opciones criticas**: (1) Rigid Diaphragm and Mass Only, (2) No Auto-Mesh, (3) Mesh into NxM, (4) Auto Mesh - subdividir en vigas/muros/rampas/grids con max size |
| **Wall Auto Mesh Options** | Assign > Shell > Wall Auto Mesh | Mallado automatico muros | Mesh NxM vertical/horizontal, o auto rectangular mesh |
| Auto Edge Constraints | Assign > Shell > Auto Edge Constraints | Restriccion bordes automatica | No crear, o crear alrededor de muros/losa |
| Material Overwrite | Assign > Shell > Material Overwrite | Sobrescribir material | - |

**Opciones de Floor Auto Mesh (CRITICO)** (p.163-164):
1. **For Defining Rigid Diaphragm and Mass Only**: Discretiza solo para masa+diafragma, SIN transferencia carga vertical
2. **No Auto-Meshing**: Sin discretizacion. Usa objeto como elemento estructural
3. **Mesh object into NxM**: Dividir en NxM cuadros
4. **Auto Mesh Object**: Discretizacion automatica con opciones:
   - Mesh at beams and meshing lines
   - Mesh at Wall and Ramp Edges
   - Mesh at Visible Grids
   - Further Subdivide with Max Element Size

### 7.4 Joint Loads (Cargas en juntas) (p.165-167)

| Comando | Ruta | Descripcion | Parametros |
|---------|------|-------------|------------|
| Force | Assign > Joint Loads > Force | Fuerza/momento en junta | Patron carga, fuerzas y momentos en ejes globales, tamano puncion |
| Ground Displacement | Assign > Joint Loads > Ground Displacement | Desplazamiento suelo | Patron carga, traslacion y rotacion |
| Temperature | Assign > Joint Loads > Temperature | Temperatura en junta | Patron carga, valor temperatura |

### 7.5 Frame Loads (Cargas en frames) (p.167-169)

| Comando | Ruta | Descripcion | Parametros |
|---------|------|-------------|------------|
| **Point** | Assign > Frame Loads > Point | Carga puntual en frame | Patron, tipo/direccion carga, distancia relativa/absoluta, valor. Opciones: agregar/reemplazar/borrar |
| **Distributed** | Assign > Frame Loads > Distributed | Carga distribuida en frame | Patron, tipo/direccion, distancia relativa/absoluta, carga uniforme o trapezoidal. Opciones: agregar/reemplazar/borrar |
| Temperature | Assign > Frame Loads > Temperature | Temperatura en frame | Patron, temperatura, incluir efectos juntas |
| Wind Load (Open Structure) | Assign > Frame Loads > Wind | Parametros carga viento | - |

### 7.6 Shell Loads (Cargas en shells) (p.169-171)

| Comando | Ruta | Descripcion | Parametros |
|---------|------|-------------|------------|
| Uniform Load Sets | Assign > Shell Loads > Uniform Sets | Asignar set de cargas uniformes predefinido | Seleccionar set definido en Define |
| **Uniform** | Assign > Shell Loads > Uniform | Carga uniforme en shell | Patron, valor carga, direccion (gravedad/ejes locales/globales) |
| **Non-uniform** | Assign > Shell Loads > Non-uniform | Carga no uniforme | Patron, direccion, restricciones (todos/sin negativos/sin positivos), valores por punto |
| Temperature | Assign > Shell Loads > Temperature | Temperatura en shell | Patron, temperatura objeto, incluir efectos juntas |
| Wind Pressure Coefficient | Assign > Shell Loads > Wind Pressure | Coeficiente presion viento | Patrones de carga viento, presion barlovento/sotavento |

### 7.x Otros comandos Assign

| Comando | Ruta | Descripcion |
|---------|------|-------------|
| Assign to Group | Assign > Assign to Group | Asignar objetos seleccionados a un grupo |
| Clear Display of Assigns | Assign > Clear Display | Quitar visualizacion de asignaciones |
| Copy Assignments | Assign > Copy Assignments | Copiar asignaciones entre objetos |

---

## 8. MENU ANALYZE: ANALIZAR (p.172-175)

| Comando | Ruta | Descripcion | Parametros clave |
|---------|------|-------------|------------------|
| **Check Model** | Analyze > Check Model | Chequear errores en el modelo | Revisa: duplicados, instabilidades, elementos sueltos, etc. |
| **Set Active DOF** | Analyze > Set Active DOF | Grados de libertad activos | **Full 3D** (todos), XZ Plane, YZ Plane, No Z Rotation |
| **Set Load Cases to Run** | Analyze > Set Load Cases to Run | Elegir casos a correr | Lista de casos, activar/desactivar, **Run Now**, **Calcular centro de rigidez del diafragma** |
| Advanced SAPFire Options | Analyze > Advanced SAPFire Options | Opciones avanzadas solver | Opciones solucion, proceso analisis, hilos internos, tamano max archivos respuesta |
| Advanced Design and Response Recovery | Analyze > Advanced Design/Response | Opciones avanzadas recuperacion | - |
| **Auto Mesh Options (Floors)** | Analyze > Auto Mesh (Floors) | Mallado automatico pisos para analisis | Mallado regular/rectangular, usar malla localizada, unir juntas, tamano maximo |
| **Auto Mesh Options (Walls)** | Analyze > Auto Mesh (Walls) | Mallado automatico muros para analisis | Tamano mallado automatico |
| Nonlinear Hinge Analysis Model | Analyze > Nonlinear Hinge Model | Modelo rotulas no lineales | - |
| Collapse Analysis Options | Analyze > Collapse Analysis | Opciones analisis colapso | - |
| **Run Analysis** | Analyze > Run Analysis | Ejecutar el analisis | - |
| Live Model | Analyze > Live Model | Modelo en vivo | - |
| Merge Analysis Results | Analyze > Merge Results | Unir resultados de analisis | - |
| Modify Undeformed Geometry | Analyze > Modify Geometry | Modificar geometria no deformada | - |
| Show Analysis Messages | Analyze > Show Messages | Mostrar mensajes de analisis | - |
| Last Analysis Log | Analyze > Last Analysis Log | Cargar ultimo log de analisis | - |
| Lock/Unlock Model | Analyze > Lock Model | Bloquear/desbloquear modelo | - |

---

## 9. MENU DISPLAY: MOSTRAR (p.176-195)

| Comando | Ruta | Descripcion | Parametros clave |
|---------|------|-------------|------------------|
| Undeformed Shape | Display > Undeformed Shape | Forma sin deformar | - |

### 9.1 Load Assigns (p.177-179)
| Comando | Ruta | Parametros |
|---------|------|------------|
| Joint Loads | Display > Load Assigns > Joint | Patron carga, tipo (fuerzas/desplazamientos/temperatura), mostrar valores |
| Frame Loads | Display > Load Assigns > Frame | Patron, tipos carga, incluir puntuales, mostrar valores |
| Shell Loads | Display > Load Assigns > Shell | Patron, tipo (uniforme/temperatura/viento/no-uniforme), contorno, incluir uniformes/no-uniformes |
| Tendon Loads | Display > Load Assigns > Tendon | Patron, tipo (asignadas/calculadas), mostrar valores |

### 9.2 Deformed Shape (Deformada) (p.179)
**Ruta**: Display > Deformed Shape
- Mostrar para: casos de carga, combinaciones, casos modales
- Escalamiento: automatico o usuario
- Opciones contorno: dibujar contorno, rango
- Sombreado de alambrado, curva cubica
- **Controles de animacion** (para modos)

### 9.3 Force/Stress Diagrams (p.180-191)

| Diagrama | Ruta | Descripcion | Parametros |
|----------|------|-------------|------------|
| **Support/Spring Reactions** | Display > Force/Stress > Reactions | Reacciones en apoyos/resortes | Caso/combinacion, tipo diagrama (flechas/tabulado), componentes a mostrar |
| Soil Pressure | Display > Force/Stress > Soil Pressure | Presion del suelo | Caso, contorno, transparencia, escalamiento |
| **Frame/Pier/Spandrel/Link Forces** | Display > Force/Stress > Frame Forces | Fuerzas en frames, piers, spandrels, links | Caso, componentes (P, V2, V3, T, M2, M3), escalamiento, incluir frames/piers/spandrels/links |
| **Shell/Stress Forces** | Display > Force/Stress > Shell Forces | Fuerzas y esfuerzos en shells | Caso, fuerzas o esfuerzos, componente, contorno, escalamiento |
| Strip Forces | Display > Force/Stress > Strip Forces | Fuerzas en flejes de diseno | Caso, componentes (M, P, V, T), capas, escalamiento |
| Diaphragm Forces | Display > Force/Stress > Diaphragm Forces | Fuerzas en diafragmas | Caso, mostrar cargas/reacciones, escalamiento, fuerzas |

**Componentes Shell Forces** (p.187):
- **Fuerzas**: F11, F22, F12 (en plano), FMAX, FMIN (principales), M11, M22, M12 (momentos), MMAX, MMIN, V13, V23, VMAX (corte fuera plano)
- **Esfuerzos**: S11, S22, S12, SMAX, SMIN (en caras top/bottom), S13, S23, SMAX (corte)

**Convenciones de signo** (p.182-184):
- Frames: segun ejes locales 1-2-3
- Pier: similar a columna (fuerzas max en extremos superior/inferior)
- Spandrel: similar a viga-dintel (fuerzas max en extremos izquierdo/derecho)

### 9.4-9.6 Diagramas adicionales

| Diagrama | Ruta | Descripcion |
|----------|------|-------------|
| Energy/Virtual Work | Display > Energy/Virtual Work | Diagrama de energia o trabajo virtual |
| Cumulative Energy Components | Display > Cumulative Energy | Componentes energia acumulativa (cinetica, potencial, amortiguamiento global/viscoso/histeretico, error) |
| **Story Response Plots** | Display > Story Response Plots | Diagramas respuesta por piso. Desplazamiento, drift, fuerzas por piso. Nombre, combinacion, rango de pisos. **Combined Story** muestra todos los diagramas |

### 9.7 Otros Display

| Comando | Ruta | Descripcion |
|---------|------|-------------|
| Story Combination Response | Display > Story Combination Response | Combinaciones de respuesta sismica |
| Spectrum Curves | Display > Spectrum Curves | Curvas espectro sismico |
| Function Plots | Display > Function Plots | Graficas de funciones |
| Fast Hysteresis | Display > Fast Hysteresis | Lazos histereticos rapidos |
| Pushover Curve | Display > Pushover Curve | Curva de empuje estatico no lineal |
| Hinge Results | Display > Hinge Results | Resultados de rotulas |
| Beam Details | Display > Beam Details | Detalles de viga |
| Slab Details | Display > Slab Details | Detalles de losa |
| Save Named Display | Display > Save Named Display | Guardar vista con nombre |
| Show Named Display | Display > Show Named Display | Mostrar vista guardada |
| **Show Tables** | Display > Show Tables | Mostrar tablas de resultados (exportable) |

---

## 10. MENU DESIGN: DISENAR (p.195-226)

### 10.1 Steel Frame Design (Acero) (p.196-203)

**Ruta**: Design > Steel Frame Design

| Comando | Ruta | Descripcion |
|---------|------|-------------|
| View/Revise Preferences | Design > Steel > Preferences | Preferencias de codigo de diseno. Descripcion detallada por item |
| View/Revise Overwrites | Design > Steel > Overwrites | Sobrescribir parametros por elemento |
| Lateral Bracing | Design > Steel > Lateral Bracing | Refuerzos laterales: determinado por programa, especificado por usuario (puntual o uniforme) |
| Select Groups of Design | Design > Steel > Select Groups | Grupos para diseno conjunto (fuerzas y deflexiones) |
| Select Design Combinations | Design > Steel > Select Combinations | Combinaciones para diseno |
| Start Design/Check | Design > Steel > Start Design | **Ejecutar diseno o chequeo** |
| Interactive Design | Design > Steel > Interactive Design | Diseno interactivo elemento por elemento |
| Display Design Info | Design > Steel > Display Info | Mostrar info: diseno entrada/salida |
| Change Design Section | Design > Steel > Change Section | Cambiar seccion de diseno |
| Make Auto Select Null | Design > Steel > Auto Select Null | Anular autoseleccion |
| Reset Design Section | Design > Steel > Reset Section | Resetear seccion al ultimo analisis |
| Verify Analysis vs Design | Design > Steel > Verify | Verificar analisis vs seccion diseno |
| Check All Members Passed | Design > Steel > Check All Passed | Verificar que todos pasen |
| Reset All Overwrites | Design > Steel > Reset Overwrites | Resetear todas las sobrescrituras |
| Delete Results | Design > Steel > Delete Results | Borrar resultados |

**Resultado**: Coeficiente de Suficiencia C.S. = Demanda/Capacidad (debe ser <= 1.00)
Segun AISC-LRFD. Para SMF: verifica compacidad sismica, soporte lateral, columna fuerte-viga debil (Ry=1.50)

### 10.2 Concrete Frame Design (Concreto HA) (p.204-210)

**Ruta**: Design > Concrete Frame Design

| Comando | Ruta | Descripcion |
|---------|------|-------------|
| View/Revise Preferences | Design > Concrete > Preferences | Preferencias segun codigo (ACI318, etc.) |
| View/Revise Overwrites | Design > Concrete > Overwrites | Sobrescribir por elemento |
| Select Groups of Design | Design > Concrete > Select Groups | Grupos de diseno |
| Select Design Combinations | Design > Concrete > Select Combinations | Combinaciones para diseno |
| Start Design/Check | Design > Concrete > Start Design | **Ejecutar diseno o chequeo** |
| Interactive Design | Design > Concrete > Interactive Design | Diseno interactivo |
| **Display Beam Design** | Design > Concrete > Display Beam | Diagramas de refuerzo de vigas: tipo muestra, tipo refuerzo, imponer minimo, envolvente, extension barras |
| Display Design Info | Design > Concrete > Display Info | Info diseno entrada/salida |
| Change Design Section | Design > Concrete > Change Section | Cambiar seccion |
| Reset/Verify/Delete | Design > Concrete > Reset/Verify/Delete | Resetear, verificar, borrar |

### 10.3 Composite Beam Design (Vigas Compuestas) (p.211-215)

**Ruta**: Design > Composite Beam Design

Comandos similares a acero. Resultado: C.S. para servicio y estado ultimo (flexion, corte, flecha, vibracion). Reportes detallados por elemento.

### 10.4 Shear Wall Design (Diseno de Muros) (p.216-221)

**Ruta**: Design > Shear Wall Design

| Comando | Ruta | Descripcion |
|---------|------|-------------|
| View/Revise Preferences | Design > Shear Wall > Preferences | Preferencias |
| **Define General Pier Sections** | Design > Shear Wall > Define Pier Sections | Definir secciones Pier: nombre, material, geometria. **Agregar nueva o desde muro existente**. Ver diagrama momento, interaccion superficie |
| **Assign Pier Sections** | Design > Shear Wall > Assign Pier Sections | Asignar seccion Pier a muros |
| Select Design Combinations | Design > Shear Wall > Select Combinations | Combinaciones para diseno |
| View/Revise Pier Overwrites | Design > Shear Wall > Pier Overwrites | Sobrescribir parametros de Piers |
| View/Revise Spandrel Overwrites | Design > Shear Wall > Spandrel Overwrites | Sobrescribir parametros de Spandrels |
| Start Design/Check | Design > Shear Wall > Start Design | **Ejecutar diseno** |
| Interactive Design | Design > Shear Wall > Interactive Design | Diseno interactivo |
| Display Design Info | Design > Shear Wall > Display Info | Cuantia acero de secciones Pier |

**Opciones de asignacion Pier** (p.218-219):
1. **Simplified C and T**: Disenos C y T simplificados
2. **Uniform Reinforcing**: Distribucion barras (tamano, espaciamiento, recubrimiento), barras esquinas, check/design
3. **General Reinforcing**: Secciones superiores/inferiores, check/design. Vista previa, detalle flexion/corte por cara

### 10.5 Concrete Slab Design (Diseno de Losas) (p.222-226)

**Ruta**: Design > Concrete Slab Design

| Comando | Ruta | Descripcion |
|---------|------|-------------|
| View Preferences | Design > Slab > Preferences | Preferencias |
| View/Revise Flexural Overwrites | Design > Slab > Flexural Overwrites | Cambios diseno flexion. **Strip Based** o **FEM Based** |
| View/Revise Punching Check | Design > Slab > Punching Check | Chequeo perforacion: ubicacion, perimetro, profundidad efectiva, aperturas, refuerzo (ortogonal/radial) |
| Select Design Combinations | Design > Slab > Select Combinations | Combinaciones |
| Select Design Floors | Design > Slab > Select Floors | Pisos para diseno |
| Start Design | Design > Slab > Start Design | Ejecutar diseno |
| Display Flexural Design | Design > Slab > Display Flexural | Tipo muestra, refuerzo minimo, ubicacion (capa superior/inferior), intensidad/area total/tamano barras, envolvente, direccion barras |
| Display Punching Check | Design > Slab > Display Punching | Mostrar chequeo perforacion |
| Display Crack Spacing | Design > Slab > Display Crack | Mostrar espaciamiento de grietas |

**Strip Based vs FEM Based** (p.223):
- Strip: capas refuerzo, tipo fleje, material, recubrimiento, espaciamiento, reduccion carga viva
- FEM: material, recubrimiento, espaciamiento barras, reduccion carga viva

### 10.x Otros Design

| Comando | Ruta |
|---------|------|
| Composite Column Design | Design > Composite Column Design |
| Steel Joist Design | Design > Steel Joist Design |
| Override Frame Design Procedure | Design > Override Frame Design Procedure |
| Live Load Reduction Factors | Design > Live Load Reduction Factors |
| Define Target Lateral Displacement | Design > Define Target Displacement |
| Define Target Seismic Motion Period | Design > Define Target Period |
| Detailing | Design > Detailing |

---

## RESUMEN DE FLUJO DE TRABAJO TIPICO EN ETABS

```
1. File > New Model          → Crear grids y pisos
2. Define > Materials        → Definir materiales (concreto, acero)
3. Define > Section Props    → Definir secciones (vigas, columnas, muros, losas)
4. Define > Diaphragms       → Crear diafragma (rigido/semi)
5. Draw > elementos          → Dibujar muros, vigas, columnas, losas
6. Assign > Restraints       → Apoyos en base (empotrado)
7. Assign > Diaphragm        → Asignar diafragma a losas/juntas
8. Assign > Shell Mesh       → Configurar auto-mesh (pisos y muros)
9. Assign > Stiffness Mods   → Modificadores rigidez (inercia losa 25%, etc.)
10. Define > Load Patterns   → Patrones: PP, SCP, SCT, SXE, SYE
11. Define > Mass Source      → Fuente masa: From Loads (PP x1.0 + SCP x0.25)
12. Define > Functions        → Espectro de respuesta (desde archivo)
13. Define > Load Cases       → Casos espectrales (SEx, SEy con CQC)
14. Define > Load Combos      → Combinaciones NCh3171
15. Define > P-Delta          → Opciones P-Delta (iterativo)
16. Assign > Shell Loads      → Cargas en losas (SCP, SCT)
17. Analyze > Check Model     → Verificar modelo
18. Analyze > Set DOF         → Full 3D
19. Analyze > Run Analysis    → CORRER
20. Display > Deformed Shape  → Verificar deformada y modos
21. Display > Story Response  → Drift, desplazamientos por piso
22. Display > Tables          → Tablas de resultados
23. Design > Shear Wall       → Diseno de muros
24. Design > Concrete Frame   → Diseno de marcos
```

---

## ATAJOS Y TIPS

- **Unidades**: Siempre verificar en esquina inferior derecha. Cambiar segun necesidad
- **Master Story**: Cambios en piso maestro se replican en pisos "Similar To"
- **Self Weight Multiplier**: Solo 1.0 en el patron DEAD. Todos los demas en 0
- **Auto Mesh muros**: Usar tamano max compatible con vanos (ej: 0.4m si vano min = 0.425m)
- **Shell Thin vs Thick**: Si L/T > 20 usar Thin (mas rapido). Si L/T < 20 usar Thick
- **Pier vs Spandrel**: Pier = muro vertical (tipo columna). Spandrel = dintel horizontal (tipo viga)
- **Section Cut**: Herramienta critica para obtener fuerzas integradas en un corte del modelo
- **Story Response Plots**: Para verificar drift por piso segun NCh433
