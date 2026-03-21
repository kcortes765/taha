# GUÍA COMPLETA — Edificio 1 (Muros, 20 pisos) en ETABS v19

## Taller ADSE — UCN 1S-2026 — Prof. Juan Music Tomicic

> **Objetivo**: Modelar, analizar y extraer todos los resultados de la Parte 1 del Taller,
> usando exclusivamente la interfaz gráfica de ETABS v19.
> Cubre los 6 casos de análisis (3 torsiones × 2 diafragmas).

> **Convención**: Los menús de ETABS v19 están en **inglés**.
> Formato: `Menú > Submenú > Opción` = ruta exacta en la barra de menú.

---

# ÍNDICE

- [FASE 0: Datos del edificio](#fase-0-datos-del-edificio)
- [FASE 1: Crear modelo y grilla](#fase-1-crear-modelo-y-grilla)
- [FASE 2: Materiales](#fase-2-materiales)
- [FASE 3: Secciones](#fase-3-secciones)
- [FASE 4: Geometría (muros, vigas, losas)](#fase-4-geometría)
- [FASE 5: Asignaciones (diafragma, mesh, apoyos)](#fase-5-asignaciones)
- [FASE 6: Cargas](#fase-6-cargas)
- [FASE 7: Análisis sísmico (masa, espectro, modos)](#fase-7-análisis-sísmico)
- [FASE 8: Torsión accidental (3 métodos)](#fase-8-torsión-accidental)
- [FASE 9: Combinaciones de carga](#fase-9-combinaciones-de-carga)
- [FASE 10: Ejecutar y validar](#fase-10-ejecutar-y-validar)
- [FASE 11: Extraer resultados](#fase-11-extraer-resultados)
- [FASE 12: Los 6 casos de análisis](#fase-12-los-6-casos)
- [FASE 13: Entregables específicos](#fase-13-entregables)
- [ERRORES COMUNES](#errores-comunes)
- [CHECKLIST FINAL](#checklist-final)

---

# FASE 0: DATOS DEL EDIFICIO

## Geometría general

- **20 pisos**, empotrado en base
- Piso 1: h = 3.40 m | Pisos 2-20: h = 2.60 m | Htotal = 52.80 m
- Grilla irregular: 17 ejes en X (1-17) + 6 ejes en Y (A-F)
- Antofagasta, Zona 3, Suelo C, Oficina (Categoría II)

## Coordenadas de ejes (tabla pág 5 del enunciado)

### Ejes X (dirección horizontal)

| Eje | x (m)  | Δx (m) |
| --- | ------ | ------- |
| 1   | 0.000  | —      |
| 2   | 3.125  | 3.125   |
| 3   | 3.825  | 0.700   |
| 4   | 9.295  | 5.470   |
| 5   | 9.895  | 0.600   |
| 6   | 15.465 | 5.570   |
| 7   | 16.015 | 0.550   |
| 8   | 18.565 | 2.550   |
| 9   | 18.990 | 0.425   |
| 10  | 21.665 | 2.675   |
| 11  | 24.990 | 3.325   |
| 12  | 26.315 | 1.325   |
| 13  | 27.834 | 1.519   |
| 14  | 32.435 | 4.601   |
| 15  | 34.005 | 1.570   |
| 16  | 37.130 | 3.125   |
| 17  | 38.505 | 1.375   |

### Ejes Y (dirección vertical en planta)

| Eje | y (m)  | Δy (m) |
| --- | ------ | ------- |
| A   | 0.000  | —      |
| B   | 0.701  | 0.701   |
| C   | 6.446  | 5.745   |
| D   | 7.996  | 1.550   |
| E   | 10.716 | 2.720   |
| F   | 13.821 | 3.105   |

### Alturas de pisos

| Piso | Altura (m) | Elevación (m) |
| ---- | ---------- | -------------- |
| 1    | 3.40       | 3.40           |
| 2    | 2.60       | 6.00           |
| 3    | 2.60       | 8.60           |
| ...  | 2.60       | ...            |
| 20   | 2.60       | 52.80          |

## Materiales

| Propiedad    | Valor                                                 | Unidad |
| ------------ | ----------------------------------------------------- | ------ |
| Hormigón    | G30 (f'c = 30 MPa = 300 kgf/cm²)                     |        |
| Ec           | 4700×√30 = 25,743 MPa = **2,624,300 tonf/m²** | (×101.937) |
| γ_HA        | 2.5 tonf/m³                                          |        |
| ν (Poisson) | 0.2                                                   |        |
| Acero        | A630-420H (fy = 420 MPa = 4200 kgf/cm²)              |        |
| Es           | 200,000 MPa = 2,039,000 tonf/m²                      |        |
| fu           | 630 MPa = 6300 kgf/cm²                               |        |

## Elementos estructurales

| Elemento       | Sección        | Notación ETABS |
| -------------- | --------------- | --------------- |
| Muro e=30cm    | Shell, t=0.30 m | MHA30G30        |
| Muro e=20cm    | Shell, t=0.20 m | MHA20G30        |
| Viga invertida | Frame 20×60 cm | VI20/60G30      |
| Losa           | Shell, t=0.15 m | Losa15G30       |

## Regla de espesores de muros

### Muros dirección Y (e=30cm en estos ejes, resto e=20cm):

Ejes **1, 3, 4, 5, 7, 12, 13, 14, 16, 17** → MHA30G30

Ejes **2, 6, 8, 9, 10, 11, 15** → MHA20G30

### Muros dirección X (e=30cm solo estos, resto e=20cm):

Eje **C entre ejes 3-6 y 10-14** → MHA30G30

Todos los demás muros en X → MHA20G30

## Cargas

| Carga               | Nombre | Valor                        | Aplicar en               |
| ------------------- | ------ | ---------------------------- | ------------------------ |
| Peso propio         | PP     | Automático (SWM=1)          | Todo                     |
| Terminaciones piso  | TERP   | 140 kgf/m² = 0.140 tonf/m² | Pisos 1-19               |
| Terminaciones techo | TERT   | 100 kgf/m² = 0.100 tonf/m² | Piso 20                  |
| Sobrecarga oficinas | SCP    | 250 kgf/m² = 0.250 tonf/m² | Pisos 1-19               |
| Sobrecarga pasillos | SCP_P  | 500 kgf/m² = 0.500 tonf/m² | Zonas pasillo pisos 1-19 |
| Sobrecarga techo    | SCT    | 100 kgf/m² = 0.100 tonf/m² | Piso 20                  |

## Parámetros sísmicos (NCh433 + DS61)

| Parámetro      | Valor        | Fuente           |
| --------------- | ------------ | ---------------- |
| Zona            | 3            | NCh433           |
| Ao              | 0.4g         | NCh433 Tabla 6.2 |
| Suelo           | C            | DS61             |
| S               | 1.05         | DS61 Tabla 6.3   |
| To              | 0.40 s       | DS61 Tabla 6.4   |
| T'              | 0.45 s       | DS61 Tabla 6.4   |
| n               | 1.40         | DS61 Tabla 12.3  |
| p               | 1.60         | DS61 Tabla 12.3  |
| Categoría      | II (oficina) | NCh433           |
| I               | 1.0          | NCh433 Tabla 6.1 |
| Tipo estructura | Muros HA     | NCh433           |
| R               | 7            | NCh433 Tabla 5.1 |
| Ro              | 11           | NCh433 Tabla 5.1 |

---

# FASE 1: CREAR MODELO Y GRILLA

## Paso 1.1: Abrir ETABS v19 y crear modelo nuevo

1. Abrir ETABS v19
2. `File > New Model`
3. En la ventana **"Initialize Model"**: seleccionar **"Use Built-in Settings with"** → unidades: **Tonf, m, C**
4. Click **OK**
5. Aparece ventana **"New Model Quick Templates"** → seleccionar **"Grid Only"**

## Paso 1.2: Configurar grilla

En el formulario Grid Only:

- **Number of Stories**: 20
- **Typical Story Height**: 2.6
- **Bottom Story Height**: 3.4
- **Number of Grid Lines in X Direction**: 17
- **Number of Grid Lines in Y Direction**: 6
- Click **"Custom Grid Spacing"** (o "Edit Grid Data")

### Ingresar espaciamientos en X:

Marcar **"Display Grid Data as Spacing"**. Ingresar en orden de izquierda a derecha:

| Grid   | Spacing (m) |
| ------ | ----------- |
| 1→2   | 3.125       |
| 2→3   | 0.700       |
| 3→4   | 5.470       |
| 4→5   | 0.600       |
| 5→6   | 5.570       |
| 6→7   | 0.550       |
| 7→8   | 2.550       |
| 8→9   | 0.425       |
| 9→10  | 2.675       |
| 10→11 | 3.325       |
| 11→12 | 1.325       |
| 12→13 | 1.519       |
| 13→14 | 4.601       |
| 14→15 | 1.570       |
| 15→16 | 3.125       |
| 16→17 | 1.375       |

### Ingresar espaciamientos en Y:

| Grid | Spacing (m) |
| ---- | ----------- |
| A→B | 0.701       |
| B→C | 5.745       |
| C→D | 1.550       |
| D→E | 2.720       |
| E→F | 3.105       |

### Renombrar grids:

- X Grids: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17
- Y Grids: A, B, C, D, E, F

Click **OK** para crear el modelo.

## Paso 1.3: Verificar/editar pisos

`Edit > Edit Stories and Grid Systems...` → Click en **"Modify/Show Story Data..."**

Verificar que:

- Story1: Height = **3.40 m**, Elevation = 3.40 m
- Story2 a Story20: Height = **2.60 m** cada uno
- Story20 Elevation = **52.80 m**

> **Tip**: Si hay un piso BASE, verificar que esté a elevación 0.

## Paso 1.4: Cambiar unidades de trabajo

En la esquina **inferior derecha** de ETABS, cambiar unidades según necesidad:

- Para geometría: **Tonf, m, C**
- Para materiales: **kgf, cm, C**
- Para cargas: **Tonf, m, C**

> **ADVERTENCIA**: ETABS convierte automáticamente. Verificar siempre que los valores
> ingresados son coherentes con las unidades activas en ese momento.

---

# FASE 2: MATERIALES

## Paso 2.1: Definir hormigón G30

`Define > Material Properties...` → Click **"Add New Material..."**

| Campo         | Valor              |
| ------------- | ------------------ |
| Region        | User               |
| Material Type | **Concrete** |
| Standard      | User               |
| Material Name | **G30**      |

En **Material Property Data**:

| Propiedad                 | Valor (en tonf, m, C)                | Nota                 |
| ------------------------- | ------------------------------------ | -------------------- |
| Weight per Unit Volume    | **2.5 tonf/m³**               | γ_HA del enunciado  |
| Mass per Unit Volume      | (se calcula solo: 2.5/9.81 = 0.2548) | NO tocar             |
| Modulus of Elasticity (E) | **2,624,300 tonf/m²**         | =4700√30 MPa × 101.937 |
| Poisson's Ratio (U)       | **0.2**                        |                      |
| Coeff. Thermal Expansion  | 0.0000099 /°C                       | Valor por defecto    |
| Shear Modulus (G)         | (automático = E/(2(1+U)))           | NO tocar             |

> **CÁLCULO Ec**: 4700 × √30 = 25,742.96 MPa.
> Conversión exacta: 1 MPa = 10^6 N/m² ÷ 9810 N/tonf = **101.937 tonf/m²**
> Ec = 25,743 × 101.937 = **2,624,300 tonf/m²**
>
> **Nota**: El enunciado dice "1 MPa = 10 kgf/cm²" (aprox. para cálculo a mano).
> Esa aproximación da 2,574,300 tonf/m² (~2% menos). Para ETABS usar el valor exacto.
>
> **Alternativa rápida**: cambiar unidades a kgf, cm, C → ingresar Ec = 262,430 kgf/cm²

Click **Modify/Show Material Property Design Data...**:

- Specified Concrete Compressive Strength (f'c): **300 kgf/cm²** (o 30 MPa)
- Lightweight Concrete: **No**

Click **OK** en todo.

## Paso 2.2: Definir acero A630-420H

`Define > Material Properties...` → **"Add New Material..."**

| Campo         | Valor               |
| ------------- | ------------------- |
| Material Type | **Rebar**     |
| Material Name | **A630-420H** |

| Propiedad                 | Valor                              |
| ------------------------- | ---------------------------------- |
| Weight per Unit Volume    | 7.849 tonf/m³                     |
| Modulus of Elasticity (E) | 2,039,000 tonf/m² (≈200,000 MPa) |

Click **Modify/Show Material Property Design Data...**:

| Propiedad                     | Valor                                     |
| ----------------------------- | ----------------------------------------- |
| Minimum Yield Stress (fy)     | **42,000 tonf/m² = 4200 kgf/cm²** |
| Minimum Tensile Stress (fu)   | **63,000 tonf/m² = 6300 kgf/cm²** |
| Expected Yield Stress (fye)   | 46,200 tonf/m² (= fy × 1.1)             |
| Expected Tensile Stress (fue) | 69,300 tonf/m² (= fu × 1.1)             |

---

# FASE 3: SECCIONES

## Paso 3.1: Muros — MHA30G30 y MHA20G30

`Define > Section Properties > Wall Sections...` (o Wall/Slab/Deck Sections)

Click **"Add New Section..."** → Type: **Wall**

### MHA30G30 (muro espesor 30 cm):

| Campo                | Valor                |
| -------------------- | -------------------- |
| Section Name         | **MHA30G30**   |
| Wall Material        | **G30**        |
| Modeling Type        | **Shell-Thin** |
| Thickness (Membrane) | **0.30 m**     |
| Thickness (Bending)  | **0.30 m**     |

### MHA20G30 (muro espesor 20 cm):

| Campo                | Valor                |
| -------------------- | -------------------- |
| Section Name         | **MHA20G30**   |
| Wall Material        | **G30**        |
| Modeling Type        | **Shell-Thin** |
| Thickness (Membrane) | **0.20 m**     |
| Thickness (Bending)  | **0.20 m**     |

> **¿Por qué Shell-Thin?** Para muros delgados (e/L < 0.1), Shell-Thin ignora deformación
> por corte transversal y es suficiente. Shell-Thick sería para muros muy gruesos.

## Paso 3.2: Vigas — VI20/60G30

`Define > Section Properties > Frame Sections...`

Click **"Add New Property..."** → sección: **Concrete Rectangular**

| Campo         | Valor                |
| ------------- | -------------------- |
| Property Name | **VI20/60G30** |
| Material      | **G30**        |
| Depth (t3)    | **0.60 m**     |
| Width (t2)    | **0.20 m**     |

Click **"Modify/Show Modifiers..."** (Property Modifiers):

| Modifier                         | Valor       | Razón                                    |
| -------------------------------- | ----------- | ----------------------------------------- |
| Cross-section Area               | 1           |                                           |
| Shear Area 2                     | 1           |                                           |
| Shear Area 3                     | 1           |                                           |
| **Torsional Constant (J)** | **0** | **PRÁCTICA CHILENA: J=0 en vigas** |
| Moment of Inertia 22             | 1           |                                           |
| Moment of Inertia 33             | 1           |                                           |
| Mass                             | 1           |                                           |
| Weight                           | 1           |                                           |

> **¿Por qué J=0?** Las vigas en edificios de muros HA no son elementos principales
> de resistencia a torsión. Asignar J=0 evita que tomen torsión espuria del análisis.
> (Lafontaine, pág. 28)

## Paso 3.3: Losas — Losa15G30

`Define > Section Properties > Slab Sections...` (o Wall/Slab/Deck Sections > Add > Slab)

| Campo         | Valor                |
| ------------- | -------------------- |
| Section Name  | **Losa15G30**  |
| Slab Material | **G30**        |
| Modeling Type | **Shell-Thin** |
| Slab Type     | **Slab**       |
| Thickness     | **0.15 m**     |

Click **"Modify/Show..."** (Stiffness Modifiers):

| Modifier              | Valor          | Razón                                           |
| --------------------- | -------------- | ------------------------------------------------ |
| f11 Membrane          | 1              |                                                  |
| f22 Membrane          | 1              |                                                  |
| f12 Membrane          | 1              |                                                  |
| **m11 Bending** | **0.25** | **PRÁCTICA CHILENA: Inercia losa al 25%** |
| **m22 Bending** | **0.25** | **Ídem**                                  |
| **m12 Bending** | **0.25** | **Ídem**                                  |
| v13 Shear             | 1              |                                                  |
| v23 Shear             | 1              |                                                  |
| Mass                  | 1              |                                                  |
| Weight                | 1              |                                                  |

> **¿Por qué 25%?** Si se deja 100%, la losa se acopla excesivamente con los muros,
> sobrestimando rigidez lateral, sobrestimando N en muros y subestimando M.
> Con 1% se subestima el acoplamiento. 25% es el estándar chileno. (Lafontaine)

---

# FASE 4: GEOMETRÍA

## Estrategia de dibujo

**Orden recomendado** (Lafontaine):

1. Muros (primero dirección Y, luego dirección X)
2. Vigas
3. Losas

**Trabajar en un piso tipo** (ej. Story2) y luego **replicar** a todos los pisos.

> **IMPORTANTE**: Antes de dibujar, ir al piso correcto.
> En la barra de herramientas superior hay un dropdown de pisos.
> Seleccionar **"Story2"** (o el piso tipo que quieras modelar).

## Paso 4.1: Dibujar muros dirección Y

Ir a vista en planta del piso tipo: `View > Set Plan View` → seleccionar Story2.

Herramienta: `Draw > Draw Walls` (o click en el ícono de muro en la barra lateral izquierda)

En **Properties of Object** (panel inferior izquierdo):

- Type of Area: **Pier**
- Property: **MHA30G30** (para ejes 1,3,4,5,7,12,13,14,16,17)

### Muros dirección Y — Identificación desde planos (págs 2, 3 y 6-7):

**Eje A (y=0.000) y Eje B (y=0.701)** — Muros en borde sur:
Hay machones/muros cortos en dir Y entre ejes A y B en varias posiciones.
Observar planta pág 2: los muros rojos en el borde sur van de A a B.
Largo = 0.701 m (distancia A-B), todos de e=20cm excepto los indicados.

Posiciones visibles en el plano (muros cortos A→B):

- Eje 1 (x=0): A→B, dir Y → **MHA30G30** (eje 1 es e=30cm)
- Eje 3 (x=3.825): A→B → **MHA30G30**
- Eje 5 (x=9.895): A→B → **MHA30G30**
- Eje 7 (x=16.015): A→B → (depende del plano, verificar)
- Eje 10 (x=21.665): A→B → MHA20G30
- Eje 12 (x=26.315): A→B → **MHA30G30**
- Eje 14 (x=32.435): A→B → **MHA30G30**
- Eje 16 (x=37.130): A→B → **MHA30G30**
- Eje 17 (x=38.505): A→B → **MHA30G30**

**Para dibujar cada muro:**

1. Verificar que la propiedad correcta esté seleccionada (MHA30G30 o MHA20G30)
2. Click en la intersección del eje X con eje A
3. Click en la intersección del mismo eje X con eje B
4. Presionar **Escape** para terminar el trazo

**Ejes C (y=6.446)** — Muros horizontales largos (dir X):
Ver sección de muros dir X más abajo.

**Ejes D (y=7.996)** — Muros horizontales (dir X):
Ver sección de muros dir X.

**Eje F (y=13.821)** — Borde norte:
Según pág 3 (longitud de muros), hay un muro central de 7.7 m centrado en eje 10.
También hay machones dir Y similares a los del borde sur.

> **MÉTODO PRÁCTICO**: Ir mirando la planta pág 2 zona por zona.
> Los muros ROJOS son muros. Dibujar cada línea roja como un muro.
> Verificar espesor según la regla de la pág 1 del enunciado.

### Procedimiento muro por muro desde la planta (pág 2 y 3):

**CONSEJO CRÍTICO**: Para muros que NO caen exactamente en intersecciones de grilla:

- Cambiar **Drawing Control Type** a **"Fixed Length"** e ingresar el largo
- O usar **"Coordinates"** para especificar punto inicio/fin con coordenadas exactas
- Ruta: en Properties of Object (abajo izquierda) cambiar Drawing Control Type

## Paso 4.2: Dibujar muros dirección X

Cambiar propiedad según corresponda.

**Eje C (y=6.446)** — Muros dir X:
Según enunciado: muros e=30cm entre ejes 3-6 y 10-14.

Tramos con MHA30G30:

- Eje C, de eje 3 (x=3.825) a eje 6 (x=15.465) → Largo ≈ 11.64 m → MHA30G30

  - PERO observar pág 6 (elevación eje C): hay aberturas/puertas. El muro NO es continuo.
  - Desde pág 3: muros del eje C tienen largos de 4.52m, 4.57m, 3.3m, 3.3m, 4.57m, 4.57m, 3.97m, 3.878m etc.
  - Dibujar cada tramo por separado según las longitudes de pág 3.
- Eje C, de eje 10 (x=21.665) a eje 14 (x=32.435) → MHA30G30 (tramos según pág 3)

Tramos con MHA20G30:

- Todos los demás muros en dir X sobre eje C
- Muros en eje D, E, F en dir X → MHA20G30

**Eje D (y=7.996)** — Los muros dir X son todos e=20cm (no está entre 3-6 ni 10-14 en la excepción):

- Observar pág 6 (elevación eje D): hay muros distribuidos

**Eje F (y=13.821)** — Muros dir X todos e=20cm:

- Pág 3: muro central de 7.7 m (4.25 + 3.45 centrado en eje 10)

## Paso 4.3: Dibujar vigas

Herramienta: `Draw > Draw Beam/Column/Brace` (modo Beam)

En Properties:

- Type of Line: **Beam**
- Property: **VI20/60G30**

Dibujar las vigas azules que aparecen en la planta pág 2. Las vigas están etiquetadas "VI20/60" en el plano.

Posiciones visibles de vigas (pág 2):

- Eje F, entre ejes 2-3 y 4-5: VI20/60
- Eje F, entre ejes 6-7: VI20/60
- Eje F, entre ejes 11-12: VI20/60
- Eje F, entre ejes 14-15 y 16-17: VI20/60
- Eje A, entre ejes 2-3: VI20/60
- Eje A, entre ejes 4-5: VI20/60
- Eje A, entre ejes 6-7: VI20/60 (y similares)
- Eje A, entre ejes 8-9 y 9-10: VI20/60
- Eje A, entre ejes 11-12: VI20/60
- Eje A, entre ejes 12-13: VI20/60
- Eje A, entre ejes 16-17: VI20/60

> **VIGAS INVERTIDAS**: Después de dibujar TODAS las vigas, seleccionarlas todas
> y asignar punto de inserción para que sean invertidas (ver Paso 5.2).

## Paso 4.4: Dibujar losas

Herramienta: `Draw > Quick Draw Floor/Wall`

En Properties:

- Property: **Losa15G30**

Click dentro de cada panel cerrado por muros/vigas/grillas. ETABS dibuja automáticamente la losa dentro del perímetro cerrado.

**IMPORTANTE**:

- NO dibujar una sola losa para todo el piso
- Dibujar panel por panel
- Dejar el hueco del shaft (ascensor) sin losa
- Verificar que cada panel tenga 4 nodos (o más si hay muros intermedios)

## Paso 4.5: Opening del shaft (ascensor)

El shaft mide 7.7 m × 2.345 m (verificado en enunciado pág. 3).

- NO dibujar losa en la zona del shaft
- Los muros del shaft se dibujan como muros normales formando el rectángulo

Si ya dibujaste losa encima: seleccionarla y borrar (Delete).
O usar `Draw > Draw Wall Openings` si el shaft está dentro de un muro.

## Paso 4.6: Replicar piso tipo a todos los pisos

1. Ir al piso tipo (Story2)
2. **Seleccionar TODO**: `Edit > Select All` o Ctrl+A
3. `Edit > Replicate...` (o Ctrl+R)
4. Tab **"Story"**
5. Seleccionar todos los pisos destino: Story1, Story3, Story4, ..., Story20
6. **NO marcar** "Delete Original Objects"
7. Click OK

> **ADVERTENCIA**: Antes de replicar, asegurarse de que TODOS los elementos
> estén visibles. Si un tipo de elemento está oculto (ej. losas), no se seleccionará
> y no se replicará.

## Paso 4.7: Ajustar piso 1 si es diferente (h=3.4m)

El piso 1 ya tiene la altura correcta (3.4m desde la definición de stories).
Los muros se ajustan automáticamente a la altura del piso.

## Paso 4.8: Ajustar techo (piso 20) si es diferente

Según pág 4 (planta techo): la planta del techo puede ser diferente — hay menos muros en el techo.
Observar pág 4: los muros rojos del techo son MENOS que en el piso tipo.

1. Ir a Story20
2. Borrar muros que no correspondan al techo
3. Verificar que las losas del techo cubran correctamente

## Paso 4.9: Dividir muros en intersecciones

Cuando dos muros se cruzan (ej. muro dir X con muro dir Y), DEBEN compartir nodos.

1. Seleccionar todos los muros: `Select > Properties > Wall Sections` → seleccionar MHA30G30 y MHA20G30
2. `Edit > Edit Shells > Divide Shells...`
3. Marcar: **"Divide Quadrilaterals/Triangles at Selected Joint Objects on Edges"**
4. OK

Esto divide los muros donde hay intersecciones, asegurando conectividad.

---

# FASE 5: ASIGNACIONES

## Paso 5.1: Asignar diafragma rígido

### Definir el diafragma:

`Define > Diaphragms...`

- Click **"Add New Diaphragm"**
- Name: **D1**
- Rigidity: **Rigid**
- Click OK

### Asignar a todas las losas:

1. `Select > Properties > Slab Sections...` → marcar Losa15G30 → OK (selecciona todas las losas)
2. `Assign > Shell > Diaphragm...`
3. Seleccionar **D1**
4. Click OK

> Para los **Casos 4, 5, 6** (semi-rígido), se creará después un segundo diafragma
> con Rigidity = **Semi Rigid** y se re-asignará. Ver FASE 12.

## Paso 5.2: Vigas invertidas — Punto de inserción

1. Seleccionar todas las vigas: `Select > Properties > Frame Sections...` → marcar VI20/60G30
2. `Assign > Frame > Insertion Point...`
3. Cardinal Point: **2 — Bottom Center**

> Esto posiciona el eje de la viga en la cara inferior de la sección.
> La viga invertida sobresale hacia arriba desde el nivel de piso;
> su base queda a nivel de losa → Cardinal Point 2 (Bottom Center).

## Paso 5.3: Restricciones de base (empotramiento)

1. En el dropdown de pisos, ir a **"Base"** (o Story0/nivel 0)
2. Seleccionar todos los nodos de la base (Ctrl+A, o dibujar ventana de selección)
3. `Assign > Joint > Restraints...`
4. Marcar las **6 casillas** (Translation 1, 2, 3 + Rotation about 1, 2, 3) = **Empotramiento**
5. O usar el botón rápido de empotramiento (ícono de cuadrado fijo)
6. Click OK

## Paso 5.4: Mesh de losas

1. Seleccionar todas las losas: `Select > Properties > Slab Sections...` → Losa15G30
2. `Assign > Shell > Floor Auto Mesh Options...`
3. Configurar:
   - ✅ **Auto Mesh Object into Structural Elements**
   - ✅ Mesh at Beams and Other Meshing Lines
   - ✅ Mesh at Wall and Ramp Edges
   - ✅ Further Subdivide Auto Mesh with Maximum Element Size of: **1.0 m**
   - ✅ Add Restraints on Edge if Corners have Restraints
4. Click OK

## Paso 5.5: Mesh de muros

1. Seleccionar todos los muros
2. `Assign > Shell > Wall Auto Mesh Options...`
3. Configurar:
   - ✅ **Auto Mesh Object into Structural Elements**
   - Maximum Element Size: **1.0 m** (o dejar que ETABS divida por piso)
4. Click OK

> **Regla Prof. Music**: La relación de aspecto de cada elemento de malla
> debe cumplir **1 ≤ L/h ≤ 2** (óptimo L/h = 1). Para piso h=2.6m y muro de 6m,
> L/h = 6/2.6 = 2.3 > 2 → subdividir horizontalmente.

## Paso 5.6: Auto Edge Constraint

1. Seleccionar todo: Ctrl+A
2. `Assign > Shell > Auto Edge Constraints...`
3. Marcar: **Create Edge Constraints around**
   - ✅ Walls
   - ✅ Floors
4. Marcar: **Apply to Full Structure (not just Selection)**
5. Click OK

> Esto asegura compatibilidad de deformaciones entre losa y muros
> donde el mesh no coincide nodo a nodo.

## Paso 5.7: Asignar Pier Labels a muros de interés

Para extraer fuerzas en muros específicos (eje 1 y eje F):

1. Seleccionar todos los muros del **eje 1** (en todos los pisos)
2. `Assign > Shell > Pier Label...`
3. Nombre: **P1** (o "Muro_Eje1")
4. OK
5. Seleccionar todos los muros del **eje F** (en todos los pisos)
6. `Assign > Shell > Pier Label...`
7. Nombre: **PF** (o "Muro_EjeF")
8. OK

> Los Piers permiten que ETABS integre las fuerzas del muro
> (P, V, M) como un solo elemento, facilitando el diseño.

---

# FASE 6: CARGAS

## Paso 6.1: Definir Load Patterns

`Define > Load Patterns...`

Crear los siguientes patrones:

| Load Pattern Name | Type       | Self Weight Multiplier |
| ----------------- | ---------- | ---------------------- |
| **PP**      | Dead       | **1**            |
| **TERP**    | Super Dead | 0                      |
| **TERT**    | Super Dead | 0                      |
| **SCP**     | Live       | 0                      |
| **SCT**     | Roof Live  | 0                      |

> **REGLA**: Solo PP tiene Self Weight Multiplier = 1. Todos los demás = 0.
> PP incluirá automáticamente el peso propio de muros, vigas, losas.

> **Nomenclatura del proyecto** (mapeo a NCh3171-2017):
>
> | Patrón proyecto | Equivalente NCh3171 | Descripción |
> |-----------------|---------------------|-------------|
> | PP | D (Dead) | Peso propio elementos estructurales |
> | TERP | Sd (Super Dead) | Terminaciones piso tipo (cielo, piso, tabiques, instalaciones) |
> | TERT | Sd (Super Dead) | Terminaciones de techo (más livianas) |
> | SCP | L (Live) | Sobrecarga de uso pisos tipo (oficinas / pasillos) |
> | SCT | Lr (Roof Live) | Sobrecarga de techo |
>
> **Tipo ETABS** de cada patrón: PP=Dead, TERP/TERT=Super Dead, SCP=Live, SCT=Roof Live.
> Usar **Super Dead** (no Dead) para terminaciones permite que ETABS las distinga del peso propio
> en la formación de masa sísmica y en la verificación automática de carga.

## Paso 6.2: Asignar cargas a losas — Pisos tipo (1-19)

### Terminaciones piso tipo:

1. Ir a un piso tipo en vista en planta
2. Seleccionar todas las losas del piso (tip: apagar muros primero con `View > Set Display Options`)
3. `Assign > Shell Loads > Uniform...`
4. Load Pattern: **TERP**
5. Load Value: **0.140 tonf/m²**
6. Direction: **Gravity**
7. Options: **Replace Existing Loads**
8. OK

### Sobrecarga oficinas:

1. (Mismas losas seleccionadas)
2. `Assign > Shell Loads > Uniform...`
3. Load Pattern: **SCP**
4. Load Value: **0.250 tonf/m²**
5. Direction: Gravity
6. OK

> **Origen de TERP = 0.140 tonf/m²**: Valor típico de terminaciones para piso de oficina en Chile,
> incluye cielo falso (~20 kgf/m²), piso flotante (~30 kgf/m²), tabiques livianos (~40 kgf/m²),
> e instalaciones (~50 kgf/m²). Verificar con el enunciado del taller.

### Nota sobre pasillos (500 kgf/m²) — Cómo distinguir zonas en ETABS:

La NCh1537-2009 establece sobrecargas diferenciadas:
- **Oficinas**: 250 kgf/m² (0.250 tonf/m²)
- **Pasillos y escaleras**: 500 kgf/m² (0.500 tonf/m²)

**Si el enunciado no especifica cuáles son zonas de pasillo**, usar **0.250 tonf/m² para todo**
el piso tipo. Esta es la simplificación más común en el taller.

**Si se quiere ser riguroso** (identificando zonas de pasillo):

1. **Identificar zonas de pasillo en planta**: Revisar los planos arquitectónicos del enunciado
   (pág. 2-4). Los pasillos son típicamente las franjas de circulación entre oficinas.
2. **Seleccionar losas de pasillo en ETABS**:
   - Ir a vista en planta del piso tipo
   - `View > Set Display Options...` → desactivar muros y vigas para ver solo losas
   - Seleccionar **manualmente** las losas que caen en zonas de pasillo
   - `Assign > Shell Loads > Uniform...` → SCP = **0.500 tonf/m²** (Replace Existing)
3. **Seleccionar losas de oficina**:
   - Seleccionar las losas restantes (zonas de oficina)
   - `Assign > Shell Loads > Uniform...` → SCP = **0.250 tonf/m²** (Replace Existing)
4. **Verificar**: `Display > Show Load Assigns > Shell...` → Load Pattern: SCP
   → verificar visualmente que las zonas de pasillo muestren 0.500 y las demás 0.250

> **Recomendación para el taller**: Usar 0.250 tonf/m² uniforme salvo indicación
> explícita del profesor. La diferencia es conservadora (250 vs 500) y simplifica el modelo.

### Repetir para todos los pisos tipo:

- La forma más eficiente es seleccionar losas de TODOS los pisos tipo a la vez
- `Select > Properties > Slab Sections` → seleccionar Losa15G30
- Luego deseleccionar las losas del piso 20 (techo)
- Asignar TERP = 0.140 y SCP = 0.250

## Paso 6.3: Asignar cargas a losas — Techo (piso 20)

1. Ir a Story20
2. Seleccionar las losas del techo
3. `Assign > Shell Loads > Uniform...`
   - Load Pattern: **TERT**, Value: **0.100 tonf/m²**, Gravity
4. `Assign > Shell Loads > Uniform...`
   - Load Pattern: **SCT**, Value: **0.100 tonf/m²**, Gravity

## Paso 6.4: Verificación visual de cargas asignadas

Antes de continuar, verificar que las cargas se asignaron correctamente:

1. `Display > Show Load Assigns > Shell...`
2. Seleccionar Load Pattern: **TERP** → verificar que los valores se muestran en losas tipo
3. Repetir para **SCP**, **TERT**, **SCT**
4. Verificar que no haya losas sin carga (valores en 0 donde no debería)

**Resumen de cargas asignadas:**

| Load Pattern | Pisos tipo (1-19) | Techo (20) |
|-------------|-------------------|------------|
| TERP | 0.140 tonf/m² | — |
| SCP | 0.250 tonf/m² | — |
| TERT | — | 0.100 tonf/m² |
| SCT | — | 0.100 tonf/m² |

> **Tip (Lafontaine)**: Antes de seleccionar losas para asignar cargas, usar
> `View > Set Display Options...` para **apagar muros y vigas**. Así solo quedan
> visibles las losas y se evita seleccionar elementos no deseados.

---

# FASE 7: ANÁLISIS SÍSMICO

## Paso 7.1: Definir Mass Source

`Define > Mass Source...`

| Campo            | Valor                               |
| ---------------- | ----------------------------------- |
| Mass Source Name | MsSrc1                              |
| Mass Definition  | ✅**Specified Load Patterns** |

**Mass Multipliers for Load Patterns:**

| Load Pattern   | Multiplier     | Razón                                       |
| -------------- | -------------- | -------------------------------------------- |
| **PP**   | **1**    | 100% peso propio                             |
| **TERP** | **1**    | 100% terminaciones                           |
| **TERT** | **1**    | 100% terminaciones techo                     |
| **SCP**  | **0.25** | 25% sobrecarga (NCh433, habitación privada) |
| **SCT**  | **0**    | Techo no se incluye en masa sísmica         |

**Mass Options:**

- ✅ Include Lateral Mass Only
- ✅ Lump Lateral Mass at Story Levels

> **Nota**: SCT = 0 porque NCh433 permite no considerar sobrecarga de techo en masa sísmica.
> SCP = 0.25 porque para edificios de oficina privada, se usa 25% de la sobrecarga.

## Paso 7.2: Construir espectro de diseño NCh433+DS61

### Preparar archivo de espectro (.txt)

Crear un archivo de texto con 2 columnas: Periodo (s) y Sa (m/s²).

**Fórmula del espectro elástico (DS61 Art. 12.2):**

```
α(T) = [1 + 4.5·(T/To)^p] / [1 + (T/To)^3]

Sa_elástico = S·Ao·α    [en unidades de g]
Sa(m/s²)    = Sa/g × 9.81
```

Para Zona 3, Suelo C (DS61 Tabla 12.3): Ao=0.4g, S=1.05, To=0.40s, T'=0.45s, n=1.40, p=1.60

**Tabla completa**: ver `autonomo/research/espectro_tabla_completa.md` (101 puntos, T=0.00-5.00s, ΔT=0.05s)

**Puntos clave del espectro:**

| T (s) | α      | Sa/g   | Sa (m/s²) |
|------:|-------:|-------:|----------:|
| 0.00  | 1.0000 | 0.4200 | 4.1202    |
| 0.20  | 2.2084 | 0.9275 | 9.0990    |
| 0.35  | 2.7752 | 1.1656 | 11.4343   |
| 0.40  | 2.7500 | 1.1550 | 11.3306   |
| 0.50  | 2.5163 | 1.0568 | 10.3675   |
| 1.00  | 1.2328 | 0.5178 | 5.0792    |
| 2.00  | 0.4770 | 0.2003 | 1.9652    |
| 5.00  | 0.1315 | 0.0552 | 0.5419    |

> **Pico**: α_max = 2.7752 en T = 0.35 s → Sa_max/g = 1.1656

**Archivo ETABS listo**: `autonomo/scripts/espectro_elastico_Z3SC.txt` (2 columnas: T, Sa/g — 101 líneas)

```
0.00    0.420000
0.05    0.486894
0.10    0.616042
...     (101 puntos hasta T=5.00s)
5.00    0.055241
```

> **Formato recomendado**: guardar Sa/g (adimensional) y usar **SF=9.81** en ETABS.
> Así el pico del espectro es ~1.17 (verificable visualmente).

> **ADVERTENCIA configuración regional**: Si tu Windows usa **coma** como separador
> decimal, el archivo debe usar comas. Si ETABS no lee bien, cambiar la configuración
> regional del PC a inglés (Punto decimal) o crear el archivo con el formato correcto.

### Cargar espectro en ETABS:

`Define > Functions > Response Spectrum...`

1. Choose Function Type to Add: **From File**
2. Click **"Add New Function..."**
3. En el formulario:
   - Function Name: **Esp_Elastico_Z3SC**
   - Function Damping Ratio: **0.05** (5%)
   - Values are: **Period vs Value**
   - **Browse** al archivo .txt
   - Header Lines to Skip: 0
4. **Verificar el gráfico** — debe verse la forma típica del espectro (sube, pico, baja)
5. Click OK

> **NO usar** la opción "Chile NCH433+DS61" integrada en ETABS.
> Lafontaine advierte: **"está desactualizado, tiene clasificación de suelos antigua"**.
> Siempre usar **From File** con espectro verificado manualmente.

## Paso 7.3: Definir caso Modal

`Define > Load Cases...`

Verificar que exista el caso **"Modal"**. Si no, crear uno:

1. Click **"Add New Load Case..."**
2. Load Case Name: **Modal**
3. Load Case Type: **Modal**
4. Analysis Type: **Eigen** (valores y vectores propios)
5. Mass Source: MsSrc1
6. Maximum Number of Modes: **30** (para edificio de 20 pisos, 30 modos es suficiente para captar >90% masa en cada dirección)
7. Minimum Number of Modes: 1
8. Convergence Tolerance: 1E-09
9. Click OK

## Paso 7.4: Definir casos de espectro de respuesta (sin torsión aún)

Estos son los sismos "base" sin torsión accidental, necesarios para el Caso b) Forma 1.

`Define > Load Cases...` → **"Add New Load Case..."**

### Sismo X (SDX):

| Campo                    | Valor                          |
| ------------------------ | ------------------------------ |
| Load Case Name           | **SDX**                  |
| Load Case Type           | **Response Spectrum**    |
| Modal Load Case          | Modal                          |
| **Loads Applied:** |                                |
| — Load Type             | Acceleration                   |
| — Load Name             | **U1**                   |
| — Function              | Esp_Elastico_Z3SC              |
| — Scale Factor          | **9.81**                 |
| Modal Combination        | **CQC**                  |
| Directional Combination  | **SRSS**                 |
| Modal Damping            | **Constant = 0.05**      |
| Diaphragm Eccentricity   | **0 for All Diaphragms** |

### Sismo Y (SDY):

| Campo                 | Valor                       |
| --------------------- | --------------------------- |
| Load Case Name        | **SDY**               |
| Load Case Type        | **Response Spectrum** |
| Modal Load Case       | Modal                       |
| — Load Name          | **U2**                |
| — Function           | Esp_Elastico_Z3SC           |
| — Scale Factor       | **9.81**              |
| (resto igual que SDX) |                             |

> **¿Por qué Scale Factor = 9.81?**
> El archivo .txt contiene Sa/g (adimensional, pico ~1.17).
> ETABS necesita Sa en m/s² → **SF = 9.81** convierte Sa/g a m/s².
>
> **Regla**: espectro en Sa/g → SF=9.81 | espectro en m/s² → SF=1.
> **Práctica del curso**: usar Sa/g en el .txt + SF=9.81.

---

# FASE 8: TORSIÓN ACCIDENTAL

La NCh433 art. 6.3.4 contempla dos métodos (a y b) para considerar la torsión accidental.
El método b tiene 2 formas de implementación en ETABS. Total: **3 formas** que se deben
implementar para los 6 casos del taller.

---

## Referencia normativa — Excentricidad accidental (NCh433 art. 6.3.4)

La norma establece una excentricidad accidental que varía linealmente con la altura:
- **10% de b⊥ en el techo** (piso 20)
- **0% en la base** (nivel 0)

Fórmula general:

```
ek = 0.10 × (zk / Htotal) × b_perp
```

Donde:
- `zk` = elevación del piso k
- `Htotal` = 52.80 m
- `b_perp` = dimensión en planta **perpendicular** a la dirección del sismo:
  - **Sismo X → b_perp = dimensión Y = 13.821 m**
  - **Sismo Y → b_perp = dimensión X = 38.505 m**

### Tabla de excentricidades accidentales — Los 20 pisos

| Piso | zk (m) | zk/Htotal | ek,Y (m) [sismo X] | ek,X (m) [sismo Y] |
| ---- | ------ | --------- | ------------------- | ------------------- |
| 20   | 52.80  | 1.000     | **1.382**           | **3.851**           |
| 19   | 50.20  | 0.951     | 1.314               | 3.661               |
| 18   | 47.60  | 0.902     | 1.246               | 3.472               |
| 17   | 45.00  | 0.852     | 1.178               | 3.282               |
| 16   | 42.40  | 0.803     | 1.110               | 3.092               |
| 15   | 39.80  | 0.754     | 1.042               | 2.902               |
| 14   | 37.20  | 0.705     | 0.974               | 2.713               |
| 13   | 34.60  | 0.655     | 0.906               | 2.523               |
| 12   | 32.00  | 0.606     | 0.838               | 2.333               |
| 11   | 29.40  | 0.557     | 0.770               | 2.144               |
| 10   | 26.80  | 0.508     | 0.701               | 1.954               |
| 9    | 24.20  | 0.458     | 0.633               | 1.764               |
| 8    | 21.60  | 0.409     | 0.565               | 1.575               |
| 7    | 19.00  | 0.360     | 0.497               | 1.385               |
| 6    | 16.40  | 0.311     | 0.429               | 1.195               |
| 5    | 13.80  | 0.261     | 0.361               | 1.006               |
| 4    | 11.20  | 0.212     | 0.293               | 0.816               |
| 3    | 8.60   | 0.163     | 0.225               | 0.626               |
| 2    | 6.00   | 0.114     | 0.157               | 0.437               |
| 1    | 3.40   | 0.064     | 0.089               | 0.247               |

> **Nota**: Los valores de ek se usan directamente en la Forma 1 (momentos torsores)
> y en la Forma 2 (excentricidad por piso). En el Método a) no se necesitan porque
> la excentricidad se maneja desplazando el CM un ±5% fijo.

---

## Resumen comparativo de los 3 métodos

| Aspecto | Método a) | Método b) Forma 1 | Método b) Forma 2 |
|---------|-----------|-------------------|-------------------|
| **Concepto** | Desplazar CM ±5% | Momentos torsores estáticos | Excentricidad neta por piso |
| **Mass Sources** | 5 (original + 4 desplazadas) | 1 (original, sin excentricidad) | 1 (original, sin excentricidad) |
| **Casos modales** | 5 (1 original + 4 desplazados) | 1 (original) | 1 (original) |
| **Casos espectro** | 6 (SDX, SDX±Y, SDY, SDY±X) | 2 (SDX, SDY) | 2 (SDTX, SDTY) |
| **Patrones User Defined** | No | Sí (TEX, TEY) | No |
| **Cálculo manual en Excel** | No | Sí (cortes → momentos torsores) | Sí (excentricidades por piso) |
| **Complejidad ETABS** | Alta | Media | Baja |

---

## Método a) — Desplazar Centro de Masa (Casos 1 y 4)

**Concepto:** Se traslada el CM una distancia igual a ±5% de la dimensión del diafragma
en la dirección correspondiente. ETABS recalcula la matriz de masa con las nuevas posiciones
del CM. Se requieren **4 Mass Sources adicionales** + **4 casos auxiliares** + **4 modales**
+ **4 espectrales nuevos**.

### Paso 8a.1: Crear 4 Mass Sources adicionales

`Define > Mass Source...`

Además de MsSrc1 (original), crear 4 fuentes duplicando la original:

| Nombre | Descripción | Ratio X | Ratio Y |
|--------|-------------|---------|---------|
| MsSrc1 (original) | PP(1.0) + SCP(0.25) sin excentricidad | 0 | 0 |
| **Masa+X** | Duplicar original + desplazar CM en +X | **+0.05** | **0** |
| **Masa-X** | Duplicar original + desplazar CM en −X | **-0.05** | **0** |
| **Masa+Y** | Duplicar original + desplazar CM en +Y | **0** | **+0.05** |
| **Masa-Y** | Duplicar original + desplazar CM en −Y | **0** | **-0.05** |

**Configuración de cada fuente desplazada:**
1. Duplicar MsSrc1
2. Habilitar ✅ **"Adjust Diaphragm Lateral Mass to Move Mass Centroid by:"**
3. Ingresar **0.05** (5%) en la casilla correspondiente:
   - "This Ratio of Diaphragm Width in **X** Direction" para Masa±X
   - "This Ratio of Diaphragm Width in **Y** Direction" para Masa±Y
4. **⚠️ IMPORTANTE:** Dejar la **OTRA** casilla en **0** → no desplazar CM en ambas direcciones simultáneamente

### Paso 8a.2: Crear 4 casos estáticos no-lineales auxiliares

`Define > Load Cases...` → Add New

Para CADA una de las 4 fuentes de masa desplazadas:

| Nombre              | Type             | Mass Source | Loads Applied       |
| ------------------- | ---------------- | ----------- | ------------------- |
| **AuxMasa+X** | Nonlinear Static | Masa+X      | VACÍO (sin cargas) |
| **AuxMasa-X** | Nonlinear Static | Masa-X      | VACÍO              |
| **AuxMasa+Y** | Nonlinear Static | Masa+Y      | VACÍO              |
| **AuxMasa-Y** | Nonlinear Static | Masa-Y      | VACÍO              |

> Aparecerá el mensaje: **"No Load Assignments are specified!"** → Seleccionar **"Sí"**.
> Esto es correcto — son casos auxiliares puramente numéricos para la formación de matrices
> de masa. No aplican ninguna carga al modelo.

### Paso 8a.3: Crear 4 casos modales con masa desplazada

`Define > Load Cases...` → Add New

| Nombre            | Type  | Subtype | P-Delta/Nonlinear Stiffness           | Nonlinear Case |
| ----------------- | ----- | ------- | ------------------------------------- | -------------- |
| **Modal+X** | Modal | Eigen   | **Use Nonlinear Case** (Loads NOT included) | AuxMasa+X      |
| **Modal-X** | Modal | Eigen   | **Use Nonlinear Case** (Loads NOT included) | AuxMasa-X      |
| **Modal+Y** | Modal | Eigen   | **Use Nonlinear Case** (Loads NOT included) | AuxMasa+Y      |
| **Modal-Y** | Modal | Eigen   | **Use Nonlinear Case** (Loads NOT included) | AuxMasa-Y      |

> **¿Por qué se necesitan 4 modales separados?** Al cambiar la posición del CM, las
> propiedades dinámicas (períodos, formas modales) también cambian. Cada excentricidad
> produce un análisis modal diferente. Al seleccionar el caso no lineal auxiliar,
> **ETABS importa automáticamente la matriz de masa asociada** a esa fuente desplazada.

### Paso 8a.4: Crear 4 casos espectrales con masa desplazada

`Define > Load Cases...` → Add New

**Para sismo X** → CM desplazado en **Y** (dirección perpendicular):

| Nombre          | Type              | Modal Case | Direction | Function             | SF   | Diaph Ecc   |
| --------------- | ----------------- | ---------- | --------- | -------------------- | ---- | ----------- |
| **SDX+Y** | Response Spectrum | Modal+Y    | U1        | Esp_Elastico_Z3SC    | 9.81 | **0** |
| **SDX-Y** | Response Spectrum | Modal-Y    | U1        | Esp_Elastico_Z3SC    | 9.81 | **0** |

**Para sismo Y** → CM desplazado en **X** (dirección perpendicular):

| Nombre          | Type              | Modal Case | Direction | Function             | SF   | Diaph Ecc   |
| --------------- | ----------------- | ---------- | --------- | -------------------- | ---- | ----------- |
| **SDY+X** | Response Spectrum | Modal+X    | U2        | Esp_Elastico_Z3SC    | 9.81 | **0** |
| **SDY-X** | Response Spectrum | Modal-X    | U2        | Esp_Elastico_Z3SC    | 9.81 | **0** |

> **Diaphragm Eccentricity = 0** porque la excentricidad ya está incluida físicamente
> en la matriz de masa del análisis modal. Ponerla ≠ 0 sería contarla dos veces.

**Resultado total de casos espectrales** para el Método a):

| Caso | Descripción | Torsión |
|------|-------------|---------|
| SDX | Sismo X, masa original | Sin torsión accidental |
| SDX+Y | Sismo X, CM desplazado +Y | Con torsión accidental (+) |
| SDX-Y | Sismo X, CM desplazado −Y | Con torsión accidental (−) |
| SDY | Sismo Y, masa original | Sin torsión accidental |
| SDY+X | Sismo Y, CM desplazado +X | Con torsión accidental (+) |
| SDY-X | Sismo Y, CM desplazado −X | Con torsión accidental (−) |

---

## Método b) Forma 1 — Torsión estática por piso (Casos 2 y 5)

**Concepto:** Se corre el modelo sin torsión accidental, se obtienen los cortes de piso
combinados por CQC, se calcula el momento torsor manualmente en Excel y se ingresa como
carga estática (Load Pattern tipo User Defined).

### Paso 8b1.1: Correr análisis SIN torsión

Primero correr SDX y SDY sin torsión (ya definidos en Paso 7.4).
- `Analyze > Run Analysis` (o **F5**)
- Verificar que los casos SDX y SDY hayan corrido exitosamente

### Paso 8b1.2: Obtener cortes de piso (Story Shears)

Hay **dos formas** de obtener los cortes acumulados por piso:

**Forma A — Gráfico:**
- `Display > Story Response Plots`
- Display Type: **Story Shears**
- Case/Combo: Seleccionar SDX (o SDY)
- Tomar valores tabulados o exportar a Excel

**Forma B — Tabla:**
- `Display > Show Tables...` → ANALYSIS RESULTS > Structure Output > Other Output Items > **Table: Story Forces**
- Filtrar por Output Case = SDX → Leer columna **VX** por piso (Location = **Bottom**)
- Filtrar por Output Case = SDY → Leer columna **VY** por piso
- Exportar a Excel

Se requieren valores de corte para **ambas direcciones** (X e Y).

### Paso 8b1.3: Calcular momentos torsores en Excel

**⚠️ IMPORTANTE:** Los cortes de Story Shears son **ACUMULADOS** por piso.
Se debe hacer la diferencia entre pisos consecutivos para obtener la fuerza sísmica de cada piso.

Para cada piso k:

```
Fk = Qk − Qk+1           (fuerza sísmica en piso k, Q es el corte ACUMULADO)
ek = 0.10 × (zk/Htotal) × b_perp    (excentricidad accidental, ver tabla arriba)
Mtk = Fk × ek             (momento torsor en piso k)
```

Donde:
- `Qk` = corte acumulado en piso k (de Story Shears, Location = Bottom)
- `Qk+1` = corte acumulado en piso k+1 (piso superior). Para piso 20 (techo): Qk+1 = 0
- Para sismo X: b_perp = 13.821 m (dimensión Y)
- Para sismo Y: b_perp = 38.505 m (dimensión X)
- Htotal = 52.80 m

> **Ejemplo piso 20 (techo):** F20 = Q20 − 0 = Q20, e20 = 0.10 × 1.0 × 13.821 = 1.382 m,
> Mt20 = Q20 × 1.382 m
>
> **Ejemplo piso 1 (base):** F1 = Q1 − Q2, e1 = 0.10 × (3.40/52.80) × 13.821 = 0.089 m,
> Mt1 = F1 × 0.089 m

### Paso 8b1.4: Crear Load Patterns de torsión

`Define > Load Patterns...`

| Nombre        | Type    | SWM | Auto Lateral Load      |
| ------------- | ------- | --- | ---------------------- |
| **TEX** | Seismic | 0   | **User Defined** |
| **TEY** | Seismic | 0   | **User Defined** |

Para cada uno, click **"Modify Lateral Load..."**:

1. ✅ **"Apply Load at Diaphragm Center of Mass"** (marcar esta casilla)
2. En la tabla, ingresar por piso:
   - **Fx = 0**
   - **Fy = 0**
   - **Mz = valor calculado en Excel** (el momento torsor Mt_k)
3. Additional Eccentricity Ratio = **0**

> Se copian los 20 valores de Mz desde Excel y se pegan en la tabla.
> TEX usa momentos calculados con cortes de sismo X; TEY con cortes de sismo Y.

### Paso 8b1.5: Crear Load Cases para torsión estática

`Define > Load Cases...` → Verificar que ETABS haya creado automáticamente los Load Cases TEX y TEY (tipo **Linear Static**).

Si no, crearlos manualmente:
- Load Case Name: TEX, Type: **Linear Static**, Load Applied: TEX con factor 1.0
- Load Case Name: TEY, Type: **Linear Static**, Load Applied: TEY con factor 1.0

---

## Método b) Forma 2 — Excentricidad por piso (Casos 3 y 6)

**Concepto:** Se calculan las excentricidades netas por piso y se ingresan directamente
en la configuración del caso espectral. ETABS aplica internamente **±e** para obtener
la envolvente máxima. Es el método más simple de implementar.

### Paso 8b2.1: Crear casos espectrales con excentricidad

`Define > Load Cases...`

Crear (o duplicar SDX/SDY):

| Nombre         | Como SDX/SDY pero...             |
| -------------- | -------------------------------- |
| **SDTX** | = SDX con excentricidad por piso |
| **SDTY** | = SDY con excentricidad por piso |

En cada uno:

1. Click en **"Diaphragm Eccentricity"** → **"Modify/Show..."**
2. **Eccentricity Ratio = 0** (no usar ratio global — se ingresa por piso)
3. Se listan todos los diafragmas del modelo
4. Para cada piso → columna **"Eccentricity"** → ingresar el valor **en metros** (positivo)

**Para SDTX** (sismo X → excentricidad en dirección Y):

Usar columna **ek,Y** de la tabla de excentricidades:

| Piso | Eccentricity (m) |
|------|-------------------|
| 20   | 1.382             |
| 19   | 1.314             |
| 18   | 1.246             |
| ...  | (ver tabla)       |
| 2    | 0.157             |
| 1    | 0.089             |

**Para SDTY** (sismo Y → excentricidad en dirección X):

Usar columna **ek,X** de la tabla de excentricidades:

| Piso | Eccentricity (m) |
|------|-------------------|
| 20   | 3.851             |
| 19   | 3.661             |
| 18   | 3.472             |
| ...  | (ver tabla)       |
| 2    | 0.437             |
| 1    | 0.247             |

> **⚠️ IMPORTANTE:** El valor se ingresa como **longitud positiva**. ETABS aplica
> internamente **+e y −e** para capturar la envolvente máxima. No es necesario crear
> casos separados para +e y −e.
>
> **Resultado:** Cada caso (SDTX, SDTY) genera internamente 2 sub-casos (+e y −e)
> que se combinan automáticamente en la envolvente.

---

# FASE 9: COMBINACIONES DE CARGA

`Define > Load Combinations...`

## Referencia normativa — NCh3171-2017 (7 combinaciones base)

La norma NCh3171-2017 "Diseño estructural — Disposiciones generales y combinaciones de carga"
establece las siguientes **7 combinaciones de carga** para diseño por resistencia:

| Combo NCh3171 | Fórmula estándar | Nuestro proyecto |
|---------------|-----------------|------------------|
| **U1** | 1.4·D | 1.4×PP + 1.4×TERP |
| **U2** | 1.2·D + 1.6·L + 0.5·(Lr o S) | 1.2×PP + 1.2×TERP + 1.6×SCP + 0.5×SCT |
| **U3** | 1.2·D + 1.0·L + 1.6·(Lr o S) | 1.2×PP + 1.2×TERP + 1.0×SCP + 1.6×SCT |
| **U4** | 1.2·D + 1.0·L + 1.4·E | 1.2×PP + 1.2×TERP + 1.0×SCP + 1.4×Sismo |
| **U5** | 1.2·D + 1.0·L − 1.4·E | 1.2×PP + 1.2×TERP + 1.0×SCP − 1.4×Sismo |
| **U6** | 0.9·D + 1.4·E | 0.9×PP + 0.9×TERP + 1.4×Sismo |
| **U7** | 0.9·D − 1.4·E | 0.9×PP + 0.9×TERP − 1.4×Sismo |

Donde:
- **D** = Carga muerta = PP + TERP (+ TERT en techo, si aplica)
- **L** = Sobrecarga de uso = SCP
- **Lr** = Sobrecarga de techo = SCT
- **E** = Sismo (depende del método de torsión: SDX, SDY, SDTX, SDTY, SDX±Y, etc.)

> **Mapeo nomenclatura**: En el Material Apoyo del profesor, las cargas se llaman
> CP (permanentes), L (sobrecarga), Lr (sobrecarga techo). En nuestro modelo ETABS:
> CP = PP + TERP, L = SCP, Lr = SCT.

> **Nota**: U4 y U5 (sismo ±) se expanden a múltiples combinaciones porque hay
> sismo en X e Y, cada uno con su método de torsión. U6 y U7 igualmente.
> Los combos se aplican **por separado** para sismo en X y sismo en Y.
> Esto genera 3 gravitacionales + N sísmicas, donde N depende del método de torsión.

> **Nota sobre ± en casos Response Spectrum (RS):**
> En análisis modal espectral, ETABS genera automáticamente **8 sub-combinaciones
> de signo** para cada caso RS (±P, ±V2, ±V3, ±T, ±M2, ±M3). Por lo tanto,
> definir "+1.4×SDX" ya cubre todas las permutaciones de signo.
> No es necesario crear combos separados con "−1.4×SDX".
>
> El Material Apoyo del profesor lista 19 a 27 combinaciones teóricas (incluyendo ±SDX
> separadamente). En ETABS, estas se reducen a **11, 7 o 15 combos** respectivamente,
> porque la expansión de signos es automática para casos RS.

## Combinaciones gravitacionales (comunes a los 3 métodos)

| Combo | Definición | Tipo |
|-------|------------|------|
| **C1** | 1.4×PP + 1.4×TERP | Linear Add |
| **C2** | 1.2×PP + 1.2×TERP + 1.6×SCP + 0.5×SCT | Linear Add |
| **C3** | 1.2×PP + 1.2×TERP + 1.0×SCP + 1.6×SCT | Linear Add |

---

## Para Caso 1 (Rígido + Torsión Método a) — 15 combos en ETABS

| Combo | Definición | Tipo |
| ----- | ---------- | ---- |
| C1-C3 | (gravitacionales, ver arriba) | Linear Add |
| **C4** | 1.2×PP + 1.2×TERP + 1.0×SCP + 1.4×SDX | Linear Add |
| **C5** | 1.2×PP + 1.2×TERP + 1.0×SCP + 1.4×SDX+Y | Linear Add |
| **C6** | 1.2×PP + 1.2×TERP + 1.0×SCP + 1.4×SDX-Y | Linear Add |
| **C7** | 0.9×PP + 0.9×TERP + 1.4×SDX | Linear Add |
| **C8** | 0.9×PP + 0.9×TERP + 1.4×SDX+Y | Linear Add |
| **C9** | 0.9×PP + 0.9×TERP + 1.4×SDX-Y | Linear Add |
| **C10** | 1.2×PP + 1.2×TERP + 1.0×SCP + 1.4×SDY | Linear Add |
| **C11** | 1.2×PP + 1.2×TERP + 1.0×SCP + 1.4×SDY+X | Linear Add |
| **C12** | 1.2×PP + 1.2×TERP + 1.0×SCP + 1.4×SDY-X | Linear Add |
| **C13** | 0.9×PP + 0.9×TERP + 1.4×SDY | Linear Add |
| **C14** | 0.9×PP + 0.9×TERP + 1.4×SDY+X | Linear Add |
| **C15** | 0.9×PP + 0.9×TERP + 1.4×SDY-X | Linear Add |

> **Lógica:** 3 gravitacionales + (3 RS × 2 niveles de carga) × 2 direcciones = 15.
> Cada dirección de sismo tiene 3 variantes: sin torsión (SDX/SDY), con torsión + y −.
> El profesor lista 27 combinaciones teóricas; las 12 adicionales corresponden a −1.4×RS
> que ETABS cubre automáticamente.

---

## Para Caso 2 (Rígido + Torsión b Forma 1) — 11 combos en ETABS

| Combo | Definición | Tipo |
| ----- | ---------- | ---- |
| C1-C3 | (gravitacionales, ver arriba) | Linear Add |
| **C4** | 1.2×PP + 1.2×TERP + 1.0×SCP + 1.4×SDX + 1.4×TEX | Linear Add |
| **C5** | 1.2×PP + 1.2×TERP + 1.0×SCP + 1.4×SDX − 1.4×TEX | Linear Add |
| **C6** | 0.9×PP + 0.9×TERP + 1.4×SDX + 1.4×TEX | Linear Add |
| **C7** | 0.9×PP + 0.9×TERP + 1.4×SDX − 1.4×TEX | Linear Add |
| **C8** | 1.2×PP + 1.2×TERP + 1.0×SCP + 1.4×SDY + 1.4×TEY | Linear Add |
| **C9** | 1.2×PP + 1.2×TERP + 1.0×SCP + 1.4×SDY − 1.4×TEY | Linear Add |
| **C10** | 0.9×PP + 0.9×TERP + 1.4×SDY + 1.4×TEY | Linear Add |
| **C11** | 0.9×PP + 0.9×TERP + 1.4×SDY − 1.4×TEY | Linear Add |

> **Lógica:** SDX/SDY son RS (ETABS maneja ±), pero TEX/TEY son **estáticos**
> → sí se necesitan ±TEX y ±TEY explícitamente.
> 3 gravitacionales + (±TEX × 2 niveles) + (±TEY × 2 niveles) = 11.
> El profesor lista 19 teóricas; las 8 extra son ±SDX como caso separado (redundante en ETABS).

---

## Para Caso 3 (Rígido + Torsión b Forma 2) — 7 combos en ETABS

| Combo | Definición | Tipo |
| ----- | ---------- | ---- |
| C1-C3 | (gravitacionales, ver arriba) | Linear Add |
| **C4** | 1.2×PP + 1.2×TERP + 1.0×SCP + 1.4×SDTX | Linear Add |
| **C5** | 1.2×PP + 1.2×TERP + 1.0×SCP + 1.4×SDTY | Linear Add |
| **C6** | 0.9×PP + 0.9×TERP + 1.4×SDTX | Linear Add |
| **C7** | 0.9×PP + 0.9×TERP + 1.4×SDTY | Linear Add |

> **Lógica:** SDTX/SDTY son RS con ±e incluido internamente → cada uno ya genera
> la envolvente con torsión +/−. ETABS maneja ± de signos automáticamente.
> 3 gravitacionales + (SDTX × 2 niveles) + (SDTY × 2 niveles) = 7.

---

## Casos 4, 5, 6 (Semi-rígido)

Los Casos 4, 5 y 6 usan las **mismas combinaciones** que los Casos 1, 2 y 3 respectivamente.
La diferencia es que el modelo usa **diafragma semi-rígido** en lugar de rígido,
lo cual afecta los resultados de los casos de carga pero no la definición de las combinaciones.

---

## Envolvente

Para cada caso (1 a 6), crear una combinación tipo **Envelope**:

- **ENV_Caso1**: Type = **Envelope**, incluir C1 a C15
- **ENV_Caso2**: Type = **Envelope**, incluir C1 a C11
- **ENV_Caso3**: Type = **Envelope**, incluir C1 a C7

Esto da los máximos y mínimos absolutos de cada esfuerzo para diseño.

## Nota sobre reducción por R* en combinaciones (Método B)

Si se usa el **Método B** (mantener espectro elástico en ETABS, reducir en combinaciones),
los factores sísmicos en las combinaciones se modifican así:

```
Factor sismo original:  1.4
Factor sismo reducido:  1.4 × I / R* = 1.4 / R*   (para I = 1.0)
```

**Ejemplo**: Si R* = 8.64 → factor sismo = 1.4/8.64 = **0.1620**

En este caso, las combinaciones sísmicas quedan:
- C4 = 1.2×PP + 1.2×TERP + 1.0×SCP + **0.1620**×SDX (en vez de 1.4×SDX)
- C6 = 0.9×PP + 0.9×TERP + **0.1620**×SDX

> **Ventaja del Método B**: Si T* cambia (porque se modificó el modelo), solo se actualizan
> los factores en las combinaciones — no es necesario re-correr el análisis modal espectral.
> Para este edificio (20 pisos, muros), T* ≈ 1.0-1.3s → R* ≈ 8.6-9.2 → factor ≈ 0.15-0.16.

> **IMPORTANTE**: Si el corte basal resultante es menor que Qmín (probable para este edificio),
> se debe aplicar un factor de escala adicional (ver Paso 11.5). En la práctica, esto puede
> significar que el factor final en las combinaciones es Qmín/(Qbasal_elástico) en vez de I/R*.

---

# FASE 10: EJECUTAR Y VALIDAR

## Paso 10.1: Grados de libertad

`Analyze > Set Active Degrees of Freedom...`

Verificar que esté en **Full 3D** (6 DOF):

- ✅ UX, UY, UZ, RX, RY, RZ

## Paso 10.2: Seleccionar casos a correr

`Analyze > Set Load Cases to Run...`

Verificar que TODOS los casos necesarios estén marcados con **"Run"**:

- Modal
- PP, TERP, TERT, SCP, SCT (estáticos)
- SDX, SDY (espectrales base)
- TEX, TEY (torsión estática — si usas método b forma 1)
- SDTX, SDTY (espectrales con torsión — si usas método b forma 2)
- SDX+Y, SDX-Y, SDY+X, SDY-X (espectrales con masa desplazada — si usas método a)
- Modal+X, Modal-X, Modal+Y, Modal-Y (modales con masa desplazada — si usas método a)
- AuxMasa+X, etc. (auxiliares — método a)

## Paso 10.3: Análisis P-Delta (efecto de segundo orden)

La NCh433 Art. 5.8 requiere considerar los efectos P-Delta en el análisis.
Para un edificio de 20 pisos, estos efectos son **significativos** y deben incluirse.

### Método recomendado — P-Delta iterativo:

`Analyze > Set Analysis Options...`

En la pestaña **"P-Delta"**:

1. Seleccionar **"Include P-Delta"**
2. Método: **"Iterative Based on Load Cases"** (recomendado por CSI)
3. En la tabla de Load Cases, agregar:

| Load Case | Scale Factor |
|-----------|-------------|
| PP | 1.0 |
| TERP | 1.0 |
| SCP | 0.25 |

> Estos factores corresponden a la carga gravitacional que genera el efecto P-Delta.
> Se usan los mismos factores que la masa sísmica (Mass Source) porque la masa
> es la que "empuja" lateralmente al edificio bajo aceleración sísmica.

4. Convergence Tolerance: **0.01** (1%, suficiente)
5. Maximum Iterations: **10** (normalmente converge en 2-3)

> **¿Por qué iterativo?** ETABS calcula la rigidez geométrica modificada por las cargas axiales
> de gravedad. Esto reduce ligeramente la rigidez lateral → aumenta períodos y desplazamientos.
> El efecto es mayor en pisos bajos (mayor carga axial).

> **¿Qué cambia?** Los períodos fundamentales aumentan ~2-5%, los drifts aumentan ~3-8%.
> Si el drift ya estaba cerca del límite, P-Delta puede hacer que no cumpla.

### Método alternativo — P-Delta como Load Case (avanzado):

Si el método iterativo da problemas de convergencia:

1. `Define > Load Cases...` → Add New
2. **Nombre**: PDelta
3. **Type**: Nonlinear Static
4. **Geometric Nonlinearity**: **P-Delta**
5. **Loads Applied**: PP(1.0) + TERP(1.0) + SCP(0.25)
6. OK

Luego, en los casos Modal y Response Spectrum:
- **Stiffness At End Of Nonlinear Case**: seleccionar **PDelta**

> Este método es más preciso pero requiere configurar cada caso para usar la rigidez del
> caso P-Delta. El método iterativo es más simple y generalmente suficiente.

## Paso 10.4: Opciones del solver

`Analyze > Set Analysis Options...`

En la pestaña **"Solver"** (Lafontaine, pág. 123):

- **Solver Type**: **Advanced Solver** (recomendado) o **Multi-threaded**
- Ambos son rápidos para modelos de esta escala (~2000 elementos)
- El Advanced Solver es más robusto para modelos con P-Delta

## Paso 10.5: Check Model

`Analyze > Check Model...`

Verificar con tolerancia 0.001 m:

- ✅ Joint Checks — nodos duplicados, nodos sin conectar
- ✅ Frame Checks — overlaps (vigas superpuestas), intersections sin dividir
- ✅ Shell Checks — overlaps (losas/muros superpuestos)
- ✅ Other Checks — meshing, loading, duplicate self mass

> **NO usar el botón "Fix"** — hacer correcciones manualmente (Lafontaine, pág. 120).
> "Un modelo bien hecho no debiese reportar errores que necesiten algún arreglo."

**Errores comunes del Check Model y cómo resolverlos:**

| Error | Causa probable | Solución |
|-------|---------------|----------|
| Duplicate joints | Dos nodos en el mismo punto | Borrar uno; verificar conectividad |
| Frame overlaps | Vigas dibujadas dos veces | Borrar duplicado |
| Shell overlaps | Losas dibujadas dos veces | Borrar duplicado |
| Shell not meshed | Losa sin mesh asignado | `Edit > Mesh Shells` |
| Intersection warnings | Muros que se cruzan sin dividir | `Edit > Divide Shells` en la intersección |

## Paso 10.6: Run Analysis

`Analyze > Run Analysis` (o presionar **F5**)

Esperar a que termine. Puede tomar 1-5 minutos para 20 pisos con P-Delta.

> **Antes de correr**: Verificar que la barra de estado muestra el número correcto de
> Load Cases a correr. Si hay muchos más de lo esperado, revisar que no haya casos duplicados.

## Paso 10.7: Revisar log

`Analyze > Last Analysis Run Log...`

- Verificar que **no haya errores** (ERRORS)
- Los WARNINGS hay que evaluarlos caso a caso
- Si dice "Analysis Complete" sin errores → OK

**Warnings comunes que son aceptables:**
- "Diaphragm assigned to zero mass elements" → si son losas de techo sin carga, es normal
- "Redundant constraints" → nodos con más restricciones de las necesarias (no afecta resultados)

**Warnings que requieren atención:**
- "Negative stiffness" → indica un problema de geometría o material
- "Unstable structure" → verificar apoyos de base, continuidad de muros
- "P-Delta did not converge" → reducir cargas o revisar modelo

## Paso 10.8: Validación — Peso/Área ≈ 1 tonf/m²

**PRÁCTICA CHILENA CRÍTICA** (Lafontaine):

1. `Display > Show Tables...` → Structure Data > Material List By Story

   - Filtrar Element Type = "Floor" → leer **Floor Area** de un piso tipo
   - Área total ≈ Área_piso × 20
2. `Display > Show Tables...` → ANALYSIS RESULTS > Structure Output > **Base Reactions**

   - Filtrar por Load Case = masa (PP + TERP)
   - Leer **FZ** (fuerza vertical) = Peso total
3. **P/A ≈ 1.0 tonf/m²** → modelo correcto

   - Para este edificio: Área planta ≈ 468 m² × 20 = 9,360 m²
   - Peso esperado ≈ 9,360 tonf
   - P/A = 9,360/9,360 = 1.0 tonf/m² ✓

> Si P/A < 0.8 o > 1.2: revisar cargas asignadas, duplicaciones, elementos faltantes.

## Paso 10.9: Validación — Deformadas modales

`Display > Deformed Shape` (o F6)

- Seleccionar caso **Modal** → Mode 1, 2, 3...
- Verificar:
  - Modo 1: traslación en X (o Y)
  - Modo 2: traslación en Y (o X)
  - Modo 3: rotación
  - **NO debe haber elementos sueltos** moviéndose independientemente
  - La estructura debe comportarse monolíticamente

## Paso 10.10: Qué hacer si el análisis falla

| Síntoma | Causa probable | Solución |
|---------|---------------|----------|
| "Unstable structure" | Apoyos faltantes en base | Verificar que TODOS los nodos de base tengan 6 DOF restringidos |
| "Unstable structure" | Muro o viga sin conexión | Verificar continuidad con `Check Model` |
| "Negative stiffness" | E o G incorrectos en material | Verificar Ec (debe ser ~25,743 MPa = 2,624,300 tonf/m²) |
| "Convergence failed" (P-Delta) | Cargas axiales muy altas | Reducir iteraciones, verificar no haber cargas duplicadas |
| Periodos absurdos (T>5s) | Elementos sueltos | Revisar deformada modal — buscar vibraciones locales |
| Periodos muy bajos (T<0.3s) | Rigidez excesiva | Verificar que no haya muros de espesor excesivo o material incorrecto |
| Peso/Área >> 1.2 tonf/m² | Cargas duplicadas o PP en 2+ patterns | Verificar que solo PP tenga SWM=1 |
| Peso/Área << 0.8 tonf/m² | Cargas faltantes o losas sin carga | Verificar asignación de cargas (Paso 6.4) |

> **Regla general**: Si algo falla, volver al **Check Model** y revisar las deformadas modales.
> Los problemas casi siempre son de geometría o conectividad, no de parámetros de análisis.

---

# FASE 11: EXTRAER RESULTADOS

## 11.1: Periodos y masas participativas (Entregable 3.4)

`Display > Show Tables...` → ANALYSIS RESULTS > Modal Information > **Modal Participating Mass Ratios**

Columnas clave:

| Mode | Period (s) | UX | UY | SumUX | SumUY | RZ | SumRZ |
| ---- | ---------- | -- | -- | ----- | ----- | -- | ----- |

- **Tx*** = Periodo del modo con mayor **UX** (típicamente modo 1 o 2)
- **Ty*** = Periodo del modo con mayor **UY**
- **Tz*** = Periodo del modo con mayor **RZ** (rotacional)
- **Nº modos necesarios**: el menor n tal que SumUX ≥ 0.90 **Y** SumUY ≥ 0.90

Exportar tabla completa a Excel: click derecho → Export to Excel.

> **Valores esperados para este edificio**: Tx* ≈ 1.0-1.3 s, Ty* ≈ 0.8-1.2 s

### Verificación de participación modal ≥ 90% (NCh433 Art. 6.3.4)

La NCh433 exige que la superposición modal considere **todos los modos necesarios para
alcanzar al menos el 90% de la masa total** en cada dirección de análisis.

**Procedimiento paso a paso:**

1. En la tabla **Modal Participating Mass Ratios**, buscar las columnas **SumUX** y **SumUY**
2. Recorrer los modos de arriba a abajo hasta encontrar el **primer modo** donde:
   - **SumUX ≥ 0.90** (90% masa acumulada en X)
   - **SumUY ≥ 0.90** (90% masa acumulada en Y)
3. El número de modos necesarios es el **mayor** de ambos
4. Verificar que el análisis modal incluyó **al menos** esa cantidad de modos

**¿Qué hacer si no se alcanza el 90%?**

Si con los modos definidos (ej: 30) no se logra SumUX ≥ 0.90 o SumUY ≥ 0.90:

1. Ir a `Define > Load Cases...` → seleccionar **MODAL** → Modify
2. Aumentar **Maximum Number of Modes** (ej: de 30 a 50 o 60)
3. Re-correr el análisis (F5)
4. Verificar nuevamente la tabla

> **Regla práctica**: Para edificios de 20 pisos, generalmente 30 modos son suficientes
> para superar el 90%. Si no basta, puede indicar que hay modos locales (vibración de
> elementos individuales) que consumen modos sin aportar masa global.

### Tabla resumen — Formato entregable (Entregable 3.4)

| Parámetro | Valor | Observación |
|-----------|-------|-------------|
| Tx* (s) | ___.__ | Modo ___ (mayor UX = __%) |
| Ty* (s) | ___.__ | Modo ___ (mayor UY = __%) |
| Tz* (s) | ___.__ | Modo ___ (mayor RZ = __%) |
| Nº modos para 90% X | ___ | SumUX = __% |
| Nº modos para 90% Y | ___ | SumUY = __% |
| Nº modos total del análisis | ___ | (≥ al máx de los dos anteriores) |

> **Deformadas modales**: Visualizar con `Display > Show Deformed Shape...` → seleccionar
> caso MODAL → cambiar Step Number (1, 2, 3...) para ver cada modo. Verificar que las
> deformadas son coherentes (modo 1 traslacional, modo 2 traslacional ortogonal, modo 3
> rotacional, etc.) y que no hay elementos sueltos vibrando independientemente.

## 11.2: Peso sísmico (Entregable 3.1)

`Display > Show Tables...` → Structure Data > **Mass Summary by Story**

- Leer masa por piso y total
- **Peso sísmico = Masa total × g = ΣM × 9.81**
- **Peso/m² = Peso total / (Área planta × Nº pisos)**

## 11.3: Densidad de muros (Entregable 3.2)

Calcular manualmente:

- **Ax** = Σ(espesor × largo) de todos los muros dir X en un piso tipo
- **Ay** = Σ(espesor × largo) de todos los muros dir Y en un piso tipo
- **Densidad X** = Ax / Área_planta
- **Densidad Y** = Ay / Área_planta

> Valores típicos para edificios chilenos de muros: 1.5% - 4% en cada dirección.

## 11.4: Centro de masas y rigidez (Entregable 3.3)

`Display > Show Tables...` → ANALYSIS RESULTS > Structure Output > **Centers of Mass and Rigidity**

Tabla con XCM, YCM, XCR, YCR por piso.

## 11.5: Corte basal de diseño (Entregable 3.5)

### Parámetros sísmicos (DS61 Tabla 12.3 — Suelo C, Zona 3)

| Parámetro | Valor | Fuente |
|-----------|-------|--------|
| Ao | 0.40g | NCh433 Tabla 6.2 |
| S | 1.05 | DS61 Tabla 12.3 |
| To | 0.40 s | DS61 Tabla 12.3 |
| T' | 0.45 s | DS61 Tabla 12.3 |
| n | 1.40 | DS61 Tabla 12.3 |
| p | 1.60 | DS61 Tabla 12.3 |
| R | 7 | NCh433 Tabla 5.1 (muros HA) |
| Ro | 11 | NCh433 Tabla 5.1 |
| I | 1.0 | NCh433 Tabla 6.1 (Cat. II) |

### Coeficiente sísmico C (NCh433 Art. 6.2.3.1, Ec. 2)

```
C = 2.75·S·Ao / (g·R) × (T'/T*)^n
```

El parámetro **n** (exponente) viene de DS61 Tabla 12.3 según tipo de suelo.
Para Suelo C: n = 1.40. Solo aparece en esta fórmula (método estático).

> **⚠️ No confundir n con p**: Ambos vienen de DS61 Tabla 12.3, pero son distintos:
> - **n = 1.40** → exponente de C (método estático, esta fórmula)
> - **p = 1.60** → exponente del numerador de α(T) (espectro dinámico, paso 7.2)
>
> Error frecuente: usar n donde va p (o viceversa). Verificar siempre qué fórmula se está aplicando.

Constante = 2.75 × 1.05 × 0.4 / 7 = **0.16500**

### Cmín — Coeficiente sísmico mínimo (NCh433 Art. 6.2.3.1.1)

```
Cmín = S·Ao / (6·g) = 1.05 × 0.4 / 6 = 0.0700
```

Corte basal mínimo: **Qmín = Cmín × I × P**

### Cmáx — Coeficiente sísmico máximo (NCh433 Tabla 6.4)

```
Cmáx = 0.35 · S · Ao / g = 0.35 × 1.05 × 0.4 = 0.1470
```

> **Nota**: Para R=6 y R=7, Cmáx tiene el mismo factor 0.35 (NCh433 Tabla 6.4).

**Reducción para edificios de muros HA** (NCh433 Art. 6.2.3.1.3):
f = 1.25 − 0.5·q, donde q = corte_muros / corte_total (menor valor en mitad inferior).
Para nuestro edificio (100% muros): q ≈ 1.0 → f = 0.75 → **Cmáx_reducido = 0.75 × 0.1470 = 0.1103**

### R* — Factor de reducción espectral (NCh433 Art. 6.3.5.3, Ec. 10)

```
R* = 1 + T* / (0.10·To + T*/Ro)
```

Donde:
- **T*** = período del modo con mayor masa traslacional en la dirección de análisis
- **To** = período característico del suelo (DS61 Tabla 12.3)
- **Ro** = factor de reducción base (NCh433 Tabla 5.1)

Forma algebraica equivalente: `R* = 1 + T*·Ro / (0.10·To·Ro + T*)`

> **⚠️ CUIDADO**: No confundir con versiones incorrectas que circulan en algunos textos.
> La fórmula normativa tiene **0.10·To** (no 0.10·Ro) y **T*/Ro** (no (Ro−1)·T*).
> Verificar siempre contra NCh433 Art. 6.3.5.3, Ecuación (10).

**Comportamiento límite de R*:**

| Condición | R* | Interpretación |
|-----------|-----|----------------|
| T* → 0 (muy rígido) | → 1 | Sin reducción — estructura no disipa energía |
| T* = To = 0.40 s | 6.24 | Reducción parcial |
| T* = 1.0 s (esperado) | 8.64 | Reducción alta — R* > R=7 |
| T* → ∞ (muy flexible) | → 1+Ro = 12 | Máxima reducción teórica |

> R* puede exceder R=7 para períodos largos. Esto es normal: la norma controla las
> fuerzas de diseño a través del chequeo de **Qmín** (corte basal mínimo), no limitando R*.

#### Alternativa para muros (NCh433 Art. 6.3.5.4, Ec. 11)

```
R*_muros = 1 + 4·N·T* / (N·Ro·To + T*)
```

Donde N = número de pisos. Es **más conservadora** (R* menor → fuerzas mayores).
Verificar con el Prof. Music cuál usar en el taller.

### Cálculo numérico — Edificio 1

**Datos**: Suelo C, Zona 3, Ro=11, To=0.40s, T'=0.45s, n=1.40, R=7, I=1.0, P ≈ 9,368 tonf

#### Asumiendo T* = 1.0 s (verificar con resultado modal):

| Magnitud | Cálculo | Valor |
|----------|---------|-------|
| C | 0.16500 × (0.45/1.0)^1.40 | **0.0536** |
| Cmín | 1.05 × 0.4 / 6 | **0.0700** |
| Cmáx | 0.35 × 1.05 × 0.4 | **0.1470** |
| Cdiseño | C=0.0536 < Cmín=0.0700 → **Cmín gobierna** | **0.0700** |
| Qo = Cdiseño×I×P | 0.070 × 1.0 × 9,368 | **≈ 656 tonf** |
| R* Ec.(10) | 1 + 1.0/(0.04 + 1.0/11) = 1 + 1.0/0.1309 | **8.639** |
| R*_muros Ec.(11) | 1 + 4×20×1.0/(20×11×0.4 + 1.0) = 1 + 80/89 | **1.899** |

#### Asumiendo T* = 1.3 s:

| Magnitud | Cálculo | Valor |
|----------|---------|-------|
| C | 0.16500 × (0.45/1.3)^1.40 | **0.0375** |
| Cdiseño | C < Cmín → Cmín sigue gobernando | **0.0700** |
| Qo | 0.070 × 9,368 | **≈ 656 tonf** |
| R* Ec.(10) | 1 + 1.3/(0.04 + 1.3/11) = 1 + 1.3/0.1582 | **9.218** |
| R*_muros Ec.(11) | 1 + 4×20×1.3/(88 + 1.3) | **2.165** |

> **CONCLUSIÓN**: Para T* en el rango 1.0–1.3s (esperado para 20 pisos de muros),
> **Cmín SIEMPRE gobierna**. El corte basal mínimo es Qmín ≈ 656 tonf.
> R* (Ec.10) excede R=7, lo cual es normal — la norma controla las fuerzas
> de diseño a través de Qmín, no de R*.

### Procedimiento paso a paso

**Paso A — Obtener T* del análisis modal:**

1. Ir a `Display > Show Tables...` → **Modal Participating Mass Ratios**
2. Identificar el modo con mayor **UX%** → ese período es **T*x**
3. Identificar el modo con mayor **UY%** → ese período es **T*y**
4. (Ya calculado en paso 11.1)

**Paso B — Calcular C y verificar límites (para cada dirección):**

5. C = 0.16500 × (0.45/T*)^1.40
6. Verificar: Cmín ≤ C ≤ Cmáx
7. **Cdiseño** = máx(Cmín, mín(C, Cmáx))
   - Si C < Cmín → **Cmín gobierna** (caso típico para T* > ~0.8s)
   - Si Cmín ≤ C ≤ Cmáx → C se usa directamente
   - Si C > Cmáx → **Cmáx gobierna** (caso de períodos cortos)

**Paso C — Calcular corte basal estático y R*:**

8. **Qo** = Cdiseño × I × P para cada dirección
9. Calcular **R*** con Ec.(10) usando T* de cada dirección:
   R* = 1 + T* / (0.10 × 0.40 + T*/11)

**Paso D — Verificar Qmín con resultados modales de ETABS:**

10. Obtener **Qbasal_modal** de ETABS: `Display > Show Tables...` → **Base Reactions**
    (filtrar por caso SDX o SDY, leer **Global FX** o **Global FY**)
11. Dividir por R*: **Qbasal_diseño = Qbasal_modal × (I/R*)**
    (solo si el espectro en ETABS es elástico con SF=9.81)
12. Comparar con Qmín:
    - Si Qbasal_diseño ≥ Qmín → OK, no se escala
    - Si Qbasal_diseño < Qmín → **escalar** fuerzas por factor **f = Qmín / Qbasal_diseño**

### Espectro de diseño

```
Sa_diseño(T) = Sa_elástico(T) × I / R*
```

Donde R* es un valor ÚNICO calculado con T* (no varía con T del espectro).

> Dibujar en Excel ambos espectros (elástico y reducido) para ambas direcciones.
> Incluir líneas horizontales para Cmín y Cmáx como referencia visual.

### En ETABS — Dos métodos para aplicar R*

**Método A: Reducir el Scale Factor del Load Case**

- Editar SDX: `Define > Load Cases...` → seleccionar SDX → Modify
- Cambiar Scale Factor de 9.81 a **9.81/R*x** (ej: 9.81/8.639 = 1.1356)
- Editar SDY: cambiar SF a **9.81/R*y**
- Re-correr análisis

**Método B: Mantener espectro elástico, reducir en combinaciones** (RECOMENDADO)

- Mantener SF=9.81 en SDX y SDY (espectro elástico)
- En las combinaciones sísmicas, usar factor **I/R*** en vez de 1.0:
  - Ej: C1 = 1.4×PP + 1.4×(I/R*)×SDX → factor SDX = 1.4/R*
- Ventaja: si R* cambia, solo se modifican las combinaciones (no se re-corre el análisis)

> **Método recomendado (Lafontaine)**: Método B. Mantener espectro elástico en ETABS y hacer
> la reducción (I/R*) en las combinaciones. Así se puede cambiar R* sin re-correr el análisis.

### Verificación Qmín — OBLIGATORIA (NCh433 Art. 6.3.7.1)

Independientemente del método elegido, verificar que el corte basal de diseño
en cada dirección sea ≥ Qmín:

```
Qmín = Cmín × I × P = 0.0700 × 1.0 × P
```

Si **Qbasal < Qmín**, multiplicar TODAS las fuerzas sísmicas por el factor:

```
f_escala = Qmín / Qbasal
```

En ETABS, esto se aplica multiplicando el Scale Factor del Load Case por f_escala.

### Tabla resumen — Formato entregable (Entregable 3.5)

Completar esta tabla con los resultados del análisis:

| Parámetro | Dirección X | Dirección Y | Fuente |
|-----------|:-----------:|:-----------:|--------|
| T* (s) | ___.__ | ___.__ | Modal (paso 11.1) |
| R* Ec.(10) | ___.__ | ___.__ | 1 + T*/(0.04 + T*/11) |
| C | ___._____ | ___._____ | 0.16500×(0.45/T*)^1.40 |
| Cmín | 0.0700 | 0.0700 | S·Ao/(6g) |
| Cmáx | 0.1470 | 0.1470 | 0.35·S·Ao/g |
| Cmáx reducido (f=0.75) | 0.1103 | 0.1103 | Art. 6.2.3.1.3 |
| Cdiseño | ___._____ | ___._____ | máx(Cmín, mín(C, Cmáx)) |
| ¿Qué gobierna? | Cmín / C / Cmáx | Cmín / C / Cmáx | (tachar lo que no aplique) |
| P (tonf) | _____._  | _____._  | MsSrc1 (paso 11.2) |
| Qo = Cdiseño×I×P (tonf) | _____._  | _____._  | Corte basal estático |
| Qbasal modal (tonf) | _____._  | _____._  | ETABS Base Reactions |
| Qbasal diseño (tonf) | _____._  | _____._  | Qbasal_modal × I/R* |
| Qmín (tonf) | _____._  | _____._  | 0.070 × P |
| ¿Escalar? | Sí / No | Sí / No | Qbasal_diseño < Qmín? |
| f_escala | ___.__ | ___.__ | Qmín / Qbasal_diseño |

> **Tip**: Presentar esta tabla al Prof. Music para validar antes de continuar con drift.

## 11.6: Corte y momento volcante por piso (Entregable 3.6)

`Display > Story Response Plots...`

### Esfuerzo de corte:

- Display Type: **Story Shears**
- Case/Combo: SDX (o combo sísmico)
- Leer tabla y exportar a Excel
- Repetir para SDY

### Momento volcante:

- Display Type: **Story Overturning Moments**
- Exportar y graficar

Alternativa via tablas:
`Display > Show Tables...` → **Table: Story Forces**

- Columnas: Story, VX, VY, MX, MY, T

## 11.7: Indicadores biosísmicos (Entregable 3.7)

### Indicador 1: H/T*

- H = 52.80 m
- T1 = Tx* (del análisis)
- **H/Tx*** → debe estar entre 40-70 m/s para edificio de muros HA

### Indicador 13: R*

- **R*x** y **R*y** calculados en paso 11.5
- Comparar con R=7 (valor del código)
- Interpretación:
  - **R* > R** → período largo, alta reducción espectral. Típico en edificios altos de muros.
    El corte basal cae bajo Cmín → **Qmín gobierna** (escalamiento obligatorio).
  - **R* ≈ R** → reducción moderada, C en rango normal.
  - **R* < R** → período corto, edificio más rígido de lo esperado. C puede ser alto → **Cmáx podría gobernar**.

## 11.8: Drift — Verificación deformaciones (Entregable 4.1)

### Fundamento normativo (NCh433 Art. 5.9)

La NCh433 establece dos condiciones de deformación que DEBEN cumplirse simultáneamente:

```
Condición 1 (Art. 5.9):  δ_CM / h  ≤  0.002     (drift en centro de masas)
Condición 2 (Art. 5.9):  (δ_ext - δ_CM) / h  ≤  0.001  (drift adicional por torsión)
```

Donde:
- **δ_CM** = desplazamiento relativo de entrepiso en el centro de masas
- **δ_ext** = desplazamiento relativo de entrepiso en el punto más desfavorable del piso
- **h** = altura del piso correspondiente
- Los valores δ/h ya son **drift ratios** (adimensionales)

> **Condición 1** controla la rigidez global del edificio.
> **Condición 2** controla la torsión: el drift en los extremos del piso (esquinas)
> no debe exceder el drift del CM en más de 0.001.

### Tablas de drift disponibles en ETABS v19

ETABS v19 ofrece **tres tablas** diferentes para drift. Cada una reporta información distinta:

| Tabla | Ruta en Show Tables | Qué reporta |
|-------|---------------------|-------------|
| **Story Drifts** | Analysis Results > Story Output > Story Drifts | Drift máximo del piso (en esquinas), **NO en CM** |
| **Joint Drifts** | Analysis Results > Joint Output > Joint Drifts | Drift en **cada nodo individual** — usar para obtener drift en CM |
| **Diaphragm Max Over Avg Drifts** | Analysis Results > Structure Output > Diaphragm Max Over Avg Drifts | Max Drift, Avg Drift y ratio Max/Avg por diafragma |

> **⚠️ Story Drifts ≠ drift en CM**. Story Drifts reporta el drift en los nodos extremos
> (esquinas del piso), NO en el centro de masas. Para la Condición 1 de NCh433
> se necesita **Joint Drifts filtrado al nodo del CM**.

### Condición 1: Drift en CM ≤ 0.002

**Procedimiento Prof. Music (paso a paso):**

**Paso 1 — Identificar el nodo del CM:**

1. `View > Set Display Options...` → marcar ✅ **Diaphragm Extent**
   (esto muestra el símbolo del CM en cada piso)
2. Hacer click derecho sobre el nodo más cercano al CM
3. Seleccionar **Joint Object Information** → anotar el **Label** (ej: "523")

> **Alternativa**: Obtener las coordenadas exactas del CM desde la tabla
> `Centers of Mass and Rigidity` (paso 11.4) y buscar el nodo más cercano.

**Paso 2 — Extraer drift en CM:**

4. `Display > Show Tables...` (o `Ctrl+T`)
5. Expandir **ANALYSIS RESULTS > Joint Output** → marcar ✅ **Joint Drifts**
6. Click **OK** para mostrar la tabla
7. Click derecho en columna **Label** → **Filter** → escribir el Label del CM (ej: "523")
8. Click derecho en columna **Output Case** → **Filter** → seleccionar el caso sísmico
   (SDX, SDY, o el combo sísmico correspondiente)

**Paso 3 — Verificar:**

9. Revisar columnas **Drift X** y **Drift Y** para cada piso
10. **Todos los valores deben ser ≤ 0.002**

| Story | Output Case | Drift X | Drift Y | ¿Cumple? |
|-------|-------------|---------|---------|----------|
| Story1 | SDX | ___._____ | ___._____ | ≤ 0.002? |
| Story2 | SDX | ___._____ | ___._____ | ≤ 0.002? |
| ... | ... | ... | ... | ... |
| Story20 | SDX | ___._____ | ___._____ | ≤ 0.002? |

> **IMPORTANTE — Drift CQC**: Los drifts de casos espectrales (SDX, SDY) ya vienen
> calculados con superposición CQC por ETABS. **NO restar desplazamientos manualmente**
> entre pisos consecutivos — el valor de la tabla ya es δ/h.

### Condición 2: Drift en punto extremo − Drift en CM ≤ 0.001

**Procedimiento usando dos tablas:**

**Paso 1 — Obtener Max Drift (drift en el punto más desfavorable):**

1. `Display > Show Tables...` → ANALYSIS RESULTS > Structure Output
   → marcar ✅ **Diaphragm Max Over Avg Drifts**
2. Click derecho en **Output Case** → filtrar por el caso sísmico (SDX, SDY)
3. Click derecho en **Item** → filtrar por:
   - **"Diaph D1 X"** (para verificar drift en dirección X)
   - **"Diaph D1 Y"** (para verificar drift en dirección Y)
4. Leer columna **Max Drift** — es el drift del punto más desfavorable del diafragma

**Paso 2 — Calcular la diferencia:**

5. Para cada piso, calcular: **(Max Drift) − (Drift CM del Paso anterior)**
6. Verificar que la diferencia sea **≤ 0.001**

| Story | Max Drift (tabla Diaph) | Drift CM (tabla Joint) | Diferencia | ¿Cumple? |
|-------|------------------------|----------------------|------------|----------|
| Story1 | ___._____ | ___._____ | ___._____ | ≤ 0.001? |
| Story2 | ___._____ | ___._____ | ___._____ | ≤ 0.001? |
| ... | ... | ... | ... | ... |

> **Método alternativo (simplificado)**: En la tabla **Diaphragm Max Over Avg Drifts**,
> la columna **Avg Drift** ≈ drift en CM (para diafragma rígido). Entonces:
> **(Max Drift − Avg Drift) ≤ 0.001** es una verificación equivalente usando una sola tabla.
> Sin embargo, el método exacto usa el drift del nodo del CM de la tabla Joint Drifts.

> **Interpretación del ratio Max/Avg**: La columna **Ratio** (= Max Drift / Avg Drift) indica
> la **irregularidad torsional** del piso. Si Ratio > 1.5, la torsión es excesiva
> y probablemente la Condición 2 no se cumple.

### Gráficos de drift por piso (Story Response Plots)

Para generar gráficos de drift vs. altura (requeridos en el Entregable 4.1):

**Método 1 — Gráfico directo en ETABS:**

1. `Display > Story Response Plots...`
2. Configurar:
   - **Display Type**: **Max Story Drifts**
   - **Case/Combo**: seleccionar SDX (o el combo sísmico)
3. ETABS muestra un diagrama de barras horizontales con el drift por piso
4. Click derecho → **Export** para guardar imagen o datos

> **Nota**: Story Response Plots muestra el drift MÁXIMO del piso (esquinas),
> no el drift en CM. Es útil para visualización general pero NO para la verificación
> exacta de Condición 1 (que requiere drift en CM).

5. Repetir para SDY y para cada caso de torsión
6. Dibujar la línea límite de 0.002 en el gráfico

**Método 2 — Gráfico en Excel (RECOMENDADO para entregable):**

1. Exportar la tabla **Joint Drifts** (filtrada al nodo CM) a Excel
2. Crear un gráfico XY (dispersión) con:
   - **Eje X**: Drift ratio (0 a 0.003)
   - **Eje Y**: Piso (1 a 20)
   - **Serie 1**: Drift X por piso (puntos + línea)
   - **Serie 2**: Drift Y por piso (puntos + línea)
   - **Línea vertical roja**: límite 0.002
3. Repetir para cada caso de torsión (6 gráficos totales)
4. Agregar título: "Drift en CM — Caso X — Diafragma Rígido/Semi-rígido"

```
Piso 20 |        •
Piso 19 |       •
   ...  |      •
Piso 10 |         •        ← máx drift
   ...  |        •
Piso 2  |    •
Piso 1  |  •
        +--+--+--+--+--→ drift
        0  0.5 1.0 1.5 2.0  (×10⁻³)
                         ↑ límite 0.002
```

### Tabla resumen de drift — Formato entregable (Entregable 4.1)

Compilar una tabla para los **6 casos de análisis** con el drift máximo (peor piso):

| Caso | Diafragma | Torsión | Piso crítico | Drift X CM | Drift Y CM | Cond. 1 | Δ Drift X | Δ Drift Y | Cond. 2 |
|------|-----------|---------|-------------|-----------|-----------|---------|----------|----------|---------|
| 1 | Rígido | a) Despl. CM | ___ | ___._____ | ___._____ | ✅/❌ | ___._____ | ___._____ | ✅/❌ |
| 2 | Rígido | b) Forma 1 | ___ | ___._____ | ___._____ | ✅/❌ | ___._____ | ___._____ | ✅/❌ |
| 3 | Rígido | b) Forma 2 | ___ | ___._____ | ___._____ | ✅/❌ | ___._____ | ___._____ | ✅/❌ |
| 4 | Semi-ríg. | a) Despl. CM | ___ | ___._____ | ___._____ | ✅/❌ | ___._____ | ___._____ | ✅/❌ |
| 5 | Semi-ríg. | b) Forma 1 | ___ | ___._____ | ___._____ | ✅/❌ | ___._____ | ___._____ | ✅/❌ |
| 6 | Semi-ríg. | b) Forma 2 | ___ | ___._____ | ___._____ | ✅/❌ | ___._____ | ___._____ | ✅/❌ |

Donde:
- **Drift X/Y CM** = máximo drift en CM de todos los pisos (Condición 1, límite 0.002)
- **Δ Drift X/Y** = máxima diferencia (Max Drift − Drift CM) de todos los pisos (Condición 2, límite 0.001)

### ¿Qué hacer si el drift NO cumple?

Si alguna condición no se cumple, hay varias estrategias:

| Problema | Solución | Dónde en ETABS |
|----------|----------|----------------|
| Cond. 1 no cumple (drift CM > 0.002) | Aumentar rigidez: agregar muros, engrosar muros existentes | Modificar geometría → re-analizar |
| Cond. 2 no cumple (torsión excesiva) | Reducir excentricidad: agregar muros lejos del CR, simetrizar | Modificar geometría → re-analizar |
| Drift alto en pisos bajos | Verificar continuidad de muros, agregar muros en planta baja | Revisar modelo piso a piso |
| Drift alto en pisos altos | Normal en edificios de muros — verificar que no exceda límite | — |

> **Nota sobre desplazamientos elásticos vs. inelásticos**: Los drifts del análisis
> espectral en ETABS corresponden a la respuesta del espectro utilizado. Si se usó el
> espectro elástico (Sa/g con SF=9.81), los drifts son elásticos. La NCh433 define los
> límites de drift para ser comparados directamente con los resultados del análisis modal
> espectral reducido (usando R*). Si se aplica el Método B (reducción en combinaciones),
> verificar drift desde las **combinaciones** (que ya incluyen I/R*), no desde los
> casos espectrales individuales (SDX, SDY) que son elásticos.

## 11.9: Corte en muros eje 1 y eje F (Entregable 4.2)

`Display > Show Tables...` → ANALYSIS RESULTS > Pier Output > **Table: Pier Forces**

Filtrar por:

- **Station**: P1 (muro eje 1) o PF (muro eje F)
- **Output Case**: cada combo sísmico

Leer columnas **V2** (corte en dirección del muro) por piso.

> Repetir para los 6 casos de análisis. Compilar tabla comparativa.

---

# FASE 12: LOS 6 CASOS DE ANÁLISIS

## Resumen de los 6 casos

| Caso | Diafragma    | Torsión        | Qué crear/cambiar                         |
| ---- | ------------ | --------------- | ------------------------------------------ |
| 1    | Rígido      | a) Desplazar CM | 5 Mass Sources + 4 modales + 4 espectrales |
| 2    | Rígido      | b) Forma 1      | TEX/TEY como Load Patterns                 |
| 3    | Rígido      | b) Forma 2      | SDTX/SDTY con excentricidad por piso       |
| 4    | Semi-rígido | a) Desplazar CM | Cambiar diafragma a Semi-Rigid + re-correr |
| 5    | Semi-rígido | b) Forma 1      | Cambiar diafragma + re-calcular TEX/TEY + re-correr |
| 6    | Semi-rígido | b) Forma 2      | Cambiar diafragma + re-correr              |

## Estrategia eficiente para correr los 6 casos

### Principio: minimizar re-corridas del análisis

Los 6 casos se pueden resolver con **solo 2 corridas del análisis** si se definen
todos los casos de carga de los 3 métodos de torsión **antes** de la primera corrida.

### Flujo paso a paso:

```
┌─────────────────────────────────────────────────────────┐
│  ETAPA 1 — PREPARACIÓN (antes de correr)                │
│                                                         │
│  1. Configurar modelo completo (FASES 0-8)              │
│  2. Definir TODOS los casos de carga de los 3 métodos:  │
│     - Método a): 4 MsSrc + 4 NL Static + 4 Modal + 4 RS│
│     - Método b) F1: TEX, TEY (se llenarán después)      │
│     - Método b) F2: SDTX, SDTY con excentricidades      │
│  3. Definir TODAS las combinaciones (FASE 9)            │
│  4. Check Model + verificaciones                        │
└─────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────┐
│  ETAPA 2 — CORRIDA 1: DIAFRAGMA RÍGIDO (Casos 1-3)     │
│                                                         │
│  5. Run Analysis (F5) — todos los casos de una vez      │
│  6. Extraer Story Shears de SDX y SDY para TEX/TEY      │
│  7. Calcular momentos torsores en Excel (FASE 8b1)      │
│  8. Ingresar momentos en TEX/TEY                        │
│  9. Re-correr SOLO TEX y TEY (no todo el modelo)        │
│  10. Extraer TODOS los resultados (Casos 1, 2, 3)       │
│  11. Guardar como "Edificio1_Rigido.edb"                │
└─────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────┐
│  ETAPA 3 — CORRIDA 2: DIAFRAGMA SEMI-RÍGIDO (Casos 4-6)│
│                                                         │
│  12. Cambiar diafragma D1 a Semi-Rigid                  │
│  13. Run Analysis (F5)                                  │
│  14. Extraer Story Shears → recalcular TEX/TEY          │
│  15. Re-ingresar momentos torsores actualizados         │
│  16. Re-correr TEX y TEY                                │
│  17. Extraer TODOS los resultados (Casos 4, 5, 6)       │
│  18. Guardar como "Edificio1_SemiRigido.edb"            │
└─────────────────────────────────────────────────────────┘
```

> **⚠️ IMPORTANTE para el Caso 2/5 (Forma 1)**: Los momentos torsores TEX/TEY dependen de los
> cortes de piso (Story Shears) del modelo **sin torsión**. Estos cortes cambian cuando se pasa
> de diafragma rígido a semi-rígido. Por lo tanto, los momentos torsores del Caso 5 son
> **diferentes** a los del Caso 2. Hay que recalcularlos con los nuevos cortes.

### Paso 12.1: Cambiar de rígido a semi-rígido

1. `Define > Diaphragms...`
2. Seleccionar **D1**
3. Click **"Modify/Show..."**
4. Cambiar Rigidity de **Rigid** a **Semi Rigid**
5. OK → Re-correr análisis (F5)

> **Alternativa**: Guardar el modelo rígido como backup, luego cambiar in-situ.
> O usar `File > Save As...` para crear una copia antes de cambiar.

### Paso 12.2: Resultados a extraer para CADA caso

Para cada uno de los 6 casos, extraer y guardar los siguientes resultados:

| Resultado | Tabla ETABS | Exportar a |
|-----------|-------------|------------|
| Periodos y masas modales | Modal Participating Mass Ratios | Excel |
| Peso sísmico por piso | Mass Summary by Story | Excel |
| CM y CR por piso | Centers of Mass and Rigidity | Excel |
| Corte y momento por piso | Story Forces | Excel |
| Drift en nodo CM | Joint Drifts (filtrar nodo CM) | Excel |
| Drift máximo del diafragma | Diaphragm Max Over Avg Drifts | Excel |
| Base Reactions | Base Reactions | Excel |
| Pier Forces (eje 1 y F) | Pier Forces | Excel |

**Procedimiento de exportación**: En cada tabla → click derecho → **Export to Excel**
(o `File > Export > Current Table to Excel`).

> **Tip**: Crear una carpeta por caso en tu computador:
> ```
> Resultados/
> ├── Caso1_Rigido_MetodoA/
> ├── Caso2_Rigido_FormaB1/
> ├── Caso3_Rigido_FormaB2/
> ├── Caso4_SemiRigido_MetodoA/
> ├── Caso5_SemiRigido_FormaB1/
> └── Caso6_SemiRigido_FormaB2/
> ```

### Paso 12.3: Qué cambia entre diafragma rígido y semi-rígido

| Aspecto | Rígido | Semi-rígido |
|---------|--------|-------------|
| Distribución de fuerzas | Proporcional a rigidez de muros | Depende de rigidez de muros + losa |
| Grados de libertad por piso | 3 (UX, UY, RZ) | N × 6 (cada nodo libre) |
| Drift en CM | Único valor por piso | Varía según nodo |
| Torsión | Controlada por distribución de rigidez | Más influenciada por geometría local |
| Tiempo de cálculo | Rápido | Más lento (~2-5x) |
| Periodos | Generalmente iguales o ligeramente menores | Generalmente iguales o ligeramente mayores |
| Drift esperado | Similar o menor | Similar o mayor |

> **Resultado esperado**: Para un edificio regular como este, los resultados con diafragma
> rígido y semi-rígido deberían ser **similares** (diferencia < 10-15%).
> Si la diferencia es grande, puede indicar un problema de modelo o una planta muy irregular.

### Paso 12.4: Verificaciones cruzadas entre los 6 casos

Después de obtener todos los resultados, verificar coherencia:

1. **Periodos**: T1(rígido) ≈ T1(semi-rígido) (diferencia < 5% típica)
2. **Peso sísmico**: IDÉNTICO en los 6 casos (no depende de diafragma ni torsión)
3. **Corte basal**: Similar en los 6 casos (pequeñas diferencias por redistribución)
4. **Drift**: Casos con torsión método a) tienden a dar drifts algo mayores que b)
5. **Coherencia entre métodos**: Los 3 métodos de torsión deben dar resultados
   del mismo orden — si uno difiere mucho, revisar la implementación

---

# FASE 13: ENTREGABLES ESPECÍFICOS

## Resumen de entregables

| #   | Entregable                                | Fuente en ETABS                 |
| --- | ----------------------------------------- | ------------------------------- |
| 1   | Descripción edificio                     | Texto + figuras del enunciado   |
| 2   | Modelación ETABS                         | Capturas 3D y planta            |
| 3.1 | Peso sísmico (tonf) y peso/m²           | Mass Summary + Base Reactions   |
| 3.2 | Densidad muros X e Y                      | Cálculo manual                 |
| 3.3 | CM y CR por piso                          | Centers of Mass and Rigidity    |
| 3.4 | Tx*, Ty*, Tz* + tabla modal + verif. ≥90% | Modal Participating Mass Ratios |
| 3.5 | Corte basal + tabla Prof + espectros      | Cálculo + Excel                |
| 3.6 | Corte y Mv por piso (tablas + gráficos)  | Story Response Plots            |
| 3.7 | Indicadores 1 y 13                        | Cálculo manual                 |
| 4.1 | Drift (6 casos, 2 cond., gráficos, tabla) | Joint Drifts + Diaph Max/Avg   |
| 4.2 | Corte muro eje 1 y F (6 casos, tabla)     | Pier Forces                     |
| 4.3 | Cuadro resumen + conclusiones             | Compilar todo                   |

---

## Entregable 1 — Descripción del edificio

**Contenido:**
- Descripción general: ubicación (Antofagasta), uso (oficinas), sistema estructural (muros HA)
- Datos geométricos: 20 pisos, alturas (3.40 + 19×2.60 = 52.80 m), dimensiones en planta
- Materiales: G30 (f'c=30 MPa, Ec=25,743 MPa), A630-420H (fy=420 MPa)
- Secciones: muros 20 y 30 cm, vigas invertidas 20/60, losa 15 cm
- Clasificación sísmica: Zona 3, Suelo C, Categoría II (I=1.0), R=7, Ro=11

**Figuras a incluir:**
1. Planta tipo del edificio (escanear o capturar del enunciado pág. 2)
2. Elevación/corte esquemático mostrando los 20 pisos
3. Tabla de ejes con coordenadas (ya en la guía, Fase 0)

**Formato**: 1-2 páginas máximo.

---

## Entregable 2 — Modelación ETABS

**Capturas de pantalla requeridas:**

1. **Vista 3D del modelo completo** (con Extrude View activado):
   - `View > Set 3D View` → perspectiva general
   - `Options > Graphics Mode > DirectX` para mejor calidad visual
   - Activar **Extrude Frames** y **Extrude Shells** para ver el edificio sólido

2. **Vista en planta del piso tipo** mostrando:
   - Muros, vigas, losas con nombres de sección visibles
   - `View > Set Display Options...` → ✅ Section Tags
   - Diafragma D1 visible

3. **Vista en planta de la base** mostrando:
   - Apoyos empotrados (símbolo de restricción)

4. **Vista en elevación** (al menos un eje lateral):
   - `View > Set Elevation View` → seleccionar un eje

5. **Vista del mesh** de losas y muros:
   - `View > Set Display Options...` → ✅ Object Fill
   - Verificar que el mesh sea uniforme y sin elementos degenerados

**Texto complementario**: Describir brevemente las decisiones de modelación:
- J=0 en vigas (razón: torsión fisurada)
- Inercia losa 25% (razón: reducir acoplamiento losa-muro)
- Cardinal Point Bottom Center en vigas invertidas
- AutoMesh ≤ 1.0 m
- Auto Edge Constraint activado

**Formato**: 2-3 páginas con capturas y texto.

---

## Entregable 3.1 — Peso sísmico

**Tabla a presentar:**

| Piso | Masa (tonf·s²/m) | Peso (tonf) |
|------|-------------------|-------------|
| 20 (techo) | ___.__ | ___.__ |
| 19 | ___.__ | ___.__ |
| ... | ... | ... |
| 1 | ___.__ | ___.__ |
| **TOTAL** | **___.___** | **___.___** |

**Fuente ETABS**: `Display > Show Tables...` → Structure Data > **Mass Summary by Story**

**Cálculo adicional**:
- Peso/m² = Peso total / (Área planta × Nº pisos) = P / (468.4 × 20)
- **Valor esperado**: P/A ≈ 1.0 tonf/m² (entre 0.85 y 1.15 es aceptable)

---

## Entregable 3.2 — Densidad de muros

**Tabla a presentar:**

| Dirección | Σ(espesor × largo) (m²) | Área planta (m²) | Densidad (%) |
|-----------|--------------------------|-------------------|--------------|
| X (muros en dir. X) | ___.__ | 468.4 | ___.__ % |
| Y (muros en dir. Y) | ___.__ | 468.4 | ___.__ % |

**Cálculo manual**: Ir al plano del piso tipo y sumar (espesor × largo) de cada muro
en su dirección correspondiente.

> **Valores típicos**: 1.5% - 4% para edificios chilenos de muros HA.
> Si es < 1.5%, el edificio puede tener problemas de rigidez lateral.
> Si es > 4%, el edificio es muy rígido (períodos cortos, fuerzas altas).

---

## Entregable 3.3 — Centro de masas y rigidez

**Tabla a presentar:**

| Piso | XCM (m) | YCM (m) | XCR (m) | YCR (m) | ex = XCM−XCR (m) | ey = YCM−YCR (m) |
|------|---------|---------|---------|---------|-------------------|-------------------|
| 20 | ___.__ | ___.__ | ___.__ | ___.__ | ___.__ | ___.__ |
| 19 | ___.__ | ___.__ | ___.__ | ___.__ | ___.__ | ___.__ |
| ... | ... | ... | ... | ... | ... | ... |
| 1 | ___.__ | ___.__ | ___.__ | ___.__ | ___.__ | ___.__ |

**Fuente ETABS**: `Display > Show Tables...` → ANALYSIS RESULTS > Structure Output > **Centers of Mass and Rigidity**

**Gráfico recomendado**: Planta con CM y CR marcados (para un piso tipo).
- Mostrar las distancias ex y ey como vectores

> **Interpretación**: Si CM ≈ CR, el edificio tiene poca excentricidad inherente → bueno
> para torsión. Si ex o ey son grandes, la torsión será significativa.

---

## Entregable 3.4 — Periodos y masas participativas

**Tabla modal a presentar** (primeros N modos hasta alcanzar 90%):

| Modo | T (s) | UX (%) | UY (%) | RZ (%) | SumUX (%) | SumUY (%) |
|------|--------|--------|--------|--------|-----------|-----------|
| 1 | ___.__ | ___.__ | ___.__ | ___.__ | ___.__ | ___.__ |
| 2 | ___.__ | ___.__ | ___.__ | ___.__ | ___.__ | ___.__ |
| 3 | ___.__ | ___.__ | ___.__ | ___.__ | ___.__ | ___.__ |
| ... | ... | ... | ... | ... | ... | ... |
| n | ___.__ | ___.__ | ___.__ | ___.__ | **≥90%** | **≥90%** |

**Tabla resumen:**

| Parámetro | Valor | Modo |
|-----------|-------|------|
| **Tx*** (período fundamental X) | ___.__ s | Modo ___ |
| **Ty*** (período fundamental Y) | ___.__ s | Modo ___ |
| **Tz*** (período rotacional) | ___.__ s | Modo ___ |
| Nº modos para SumUX ≥ 90% | ___ | — |
| Nº modos para SumUY ≥ 90% | ___ | — |

**Fuente ETABS**: `Display > Show Tables...` → ANALYSIS RESULTS > Modal Information > **Modal Participating Mass Ratios**

**Capturas adicionales**: Deformadas de los 3 primeros modos (`Display > Show Deformed Shape...` → caso MODAL → Step 1, 2, 3).

---

## Entregable 3.5 — Corte basal de diseño

**Tabla del profesor** (ver Paso 11.5 para cálculos detallados):

| Parámetro | Dirección X | Dirección Y | Fuente |
|-----------|:-----------:|:-----------:|--------|
| T* (s) | ___.__ | ___.__ | Modal |
| R* (Ec.10) | ___.__ | ___.__ | NCh433 |
| C | ___._____ | ___._____ | NCh433 |
| Cmín | 0.0700 | 0.0700 | NCh433 |
| Cmáx | 0.1470 | 0.1470 | NCh433 |
| Cdiseño | ___._____ | ___._____ | — |
| P (tonf) | _____._  | _____._  | MsSrc1 |
| Qo (tonf) | _____._  | _____._  | Cdiseño×I×P |
| Qbasal modal (tonf) | _____._  | _____._  | ETABS |
| Qbasal diseño (tonf) | _____._  | _____._  | Qmodal×I/R* |
| Qmín (tonf) | _____._  | _____._  | 0.070×P |
| ¿Escalar? | Sí/No | Sí/No | — |
| f_escala | ___.__ | ___.__ | Qmín/Qdiseño |

**Gráficos requeridos** (hacer en Excel):

1. **Espectro elástico Sa/g vs T**: mostrar los 101 puntos con pico marcado
2. **Espectro reducido Sa_diseño vs T**: superponer sobre el elástico (Sa_diseño = Sa_elástico/R*)
3. En ambos gráficos, incluir líneas horizontales para Cmín y Cmáx como referencia

---

## Entregable 3.6 — Corte y momento volcante por piso

**Tablas a presentar** (para sismo X y sismo Y):

| Piso | Qx (tonf) | Qy (tonf) | Mvx (tonf·m) | Mvy (tonf·m) |
|------|-----------|-----------|-------------|-------------|
| 20 | ___.__ | ___.__ | ___.__ | ___.__ |
| ... | ... | ... | ... | ... |
| 1 (base) | ___.__ | ___.__ | ___.__ | ___.__ |

**Fuente ETABS**: `Display > Story Response Plots...` → Story Shears / Overturning Moments
O alternativamente: `Display > Show Tables...` → **Table: Story Forces**

**Gráficos requeridos** (hacer en ETABS o Excel):

1. **Corte por piso** (Qx vs altura, Qy vs altura) — diagramas de barras horizontales
2. **Momento volcante por piso** (Mvx vs altura, Mvy vs altura)
3. Incluir los ejes X e Y en un mismo gráfico para comparar

---

## Entregable 3.7 — Indicadores biosísmicos

**Indicador 1: H/T***

| Dirección | H (m) | T* (s) | H/T* (m/s) | Rango típico |
|-----------|-------|--------|-----------|--------------|
| X | 52.80 | ___.__ | ___.__ | 40-70 m/s |
| Y | 52.80 | ___.__ | ___.__ | 40-70 m/s |

**Indicador 13: R***

| Dirección | R* (Ec.10) | R (código) | R*/R | Interpretación |
|-----------|-----------|----------|------|----------------|
| X | ___.__ | 7 | ___.__ | R*>R → Cmín gobierna |
| Y | ___.__ | 7 | ___.__ | R*>R → Cmín gobierna |

> **Interpretación**: Para un edificio de 20 pisos de muros con T*≈1.0-1.3s,
> H/T* ≈ 40-53 m/s (rango normal) y R* ≈ 8.6-9.2 (mayor que R=7 → Cmín gobierna).

---

## Entregable 4.1 — Drift (6 casos, 2 condiciones)

**Para CADA uno de los 6 casos**, presentar:

### a) Tabla de verificación Condición 1 (drift CM ≤ 0.002)

| Piso | Drift X (CM) | ≤0.002? | Drift Y (CM) | ≤0.002? |
|------|-------------|---------|-------------|---------|
| 20 | ___._____ | ✅/❌ | ___._____ | ✅/❌ |
| ... | ... | ... | ... | ... |
| 1 | ___._____ | ✅/❌ | ___._____ | ✅/❌ |

### b) Tabla de verificación Condición 2 (drift extremo − drift CM ≤ 0.001)

| Piso | Max Drift X | Drift X CM | ΔDrift X | ≤0.001? |
|------|-----------|-----------|---------|---------|
| 20 | ___._____ | ___._____ | ___._____ | ✅/❌ |
| ... | ... | ... | ... | ... |

### c) Gráficos de drift por piso (6 gráficos)

Para cada caso, hacer un gráfico en Excel:
- **Eje X**: Drift ratio (0 a 0.003)
- **Eje Y**: Piso (1 a 20)
- **Series**: Drift X, Drift Y, límite 0.002 (línea vertical roja)
- **Título**: "Drift en CM — Caso N — Diafragma [Rígido/Semi-rígido] — Torsión [Método]"

### d) Tabla resumen comparativa (los 6 casos juntos)

| Caso | Diafragma | Torsión | Piso crítico | Max Drift X | Max Drift Y | Cond. 1 | Max Δ Drift X | Max Δ Drift Y | Cond. 2 |
|------|-----------|---------|-------------|-----------|-----------|---------|-------------|-------------|---------|
| 1 | Rígido | a) | ___ | ___._____ | ___._____ | ✅/❌ | ___._____ | ___._____ | ✅/❌ |
| 2 | Rígido | b) F1 | ___ | ___._____ | ___._____ | ✅/❌ | ___._____ | ___._____ | ✅/❌ |
| 3 | Rígido | b) F2 | ___ | ___._____ | ___._____ | ✅/❌ | ___._____ | ___._____ | ✅/❌ |
| 4 | Semi-ríg. | a) | ___ | ___._____ | ___._____ | ✅/❌ | ___._____ | ___._____ | ✅/❌ |
| 5 | Semi-ríg. | b) F1 | ___ | ___._____ | ___._____ | ✅/❌ | ___._____ | ___._____ | ✅/❌ |
| 6 | Semi-ríg. | b) F2 | ___ | ___._____ | ___._____ | ✅/❌ | ___._____ | ___._____ | ✅/❌ |

---

## Entregable 4.2 — Corte en muros eje 1 y eje F

**Para CADA uno de los 6 casos**, presentar tabla de corte por piso en los piers del eje 1 y eje F:

### Muro eje 1:

| Piso | V2 Caso 1 | V2 Caso 2 | V2 Caso 3 | V2 Caso 4 | V2 Caso 5 | V2 Caso 6 |
|------|-----------|-----------|-----------|-----------|-----------|-----------|
| 20 | ___.__ | ___.__ | ___.__ | ___.__ | ___.__ | ___.__ |
| ... | ... | ... | ... | ... | ... | ... |
| 1 | ___.__ | ___.__ | ___.__ | ___.__ | ___.__ | ___.__ |

### Muro eje F:

(misma estructura que eje 1)

**Fuente ETABS**: `Display > Show Tables...` → ANALYSIS RESULTS > Pier Output > **Table: Pier Forces**
- Filtrar por **Station**: nombre del Pier asignado al eje 1 o eje F
- Filtrar por **Output Case**: cada combo sísmico
- Leer columna **V2** (corte en la dirección del muro)

**Gráfico recomendado**: Corte V2 vs piso para los 6 casos superpuestos (2 gráficos: eje 1 y eje F).

---

## Entregable 4.3 — Cuadro resumen y conclusiones

### Cuadro resumen final:

Compilar los resultados principales de los 6 casos en una sola tabla:

| Parámetro | Caso 1 | Caso 2 | Caso 3 | Caso 4 | Caso 5 | Caso 6 |
|-----------|--------|--------|--------|--------|--------|--------|
| T1 (s) | — | — | — | — | — | — |
| Peso (tonf) | — | — | — | — | — | — |
| Qbasal X (tonf) | — | — | — | — | — | — |
| Qbasal Y (tonf) | — | — | — | — | — | — |
| Max Drift X | — | — | — | — | — | — |
| Max Drift Y | — | — | — | — | — | — |
| Cond.1 cumple | — | — | — | — | — | — |
| Cond.2 cumple | — | — | — | — | — | — |
| V2 muro eje 1 (base) | — | — | — | — | — | — |
| V2 muro eje F (base) | — | — | — | — | — | — |

### Conclusiones — Puntos a abordar:

1. **Comparación de métodos de torsión**: ¿Cuál de los 3 métodos da los mayores drifts?
   ¿Los resultados son consistentes entre métodos? Justificar diferencias.

2. **Efecto del diafragma**: ¿Cómo cambian los resultados al pasar de rígido a semi-rígido?
   ¿Es significativa la diferencia? ¿Para qué tipo de edificios importaría más?

3. **Cumplimiento normativo**: ¿Se cumplen las dos condiciones de drift (NCh433 Art. 5.9)?
   Si no se cumple, ¿qué modificaciones se propondrían?

4. **Corte basal y R***: ¿Cmín gobierna? ¿El escalamiento es necesario?
   ¿Qué implica esto para el diseño?

5. **Distribución de esfuerzos en muros**: ¿Los muros del eje 1 y eje F toman el corte
   esperado según su rigidez? ¿Hay redistribución significativa por torsión?

6. **Validez del modelo**: Comentar sobre peso/área, períodos, deformadas modales.
   ¿El modelo es razonable y confiable?

> **Formato conclusiones**: 1-2 páginas, redacción clara y técnica.
> Incluir recomendaciones si alguna verificación no cumple.

---

## Estructura sugerida del informe

```
INFORME TALLER — PARTE 1: EDIFICIO DE MUROS

1. Introducción (Entregable 1)
   1.1. Descripción del edificio
   1.2. Materiales y secciones
   1.3. Normativa aplicada

2. Modelación (Entregable 2)
   2.1. Capturas del modelo ETABS
   2.2. Decisiones de modelación
   2.3. Verificación del modelo (Check Model, peso/área)

3. Análisis Sísmico (Entregables 3.1-3.7)
   3.1. Peso sísmico
   3.2. Densidad de muros
   3.3. Centro de masas y rigidez
   3.4. Análisis modal
   3.5. Corte basal de diseño
   3.6. Corte y momento volcante por piso
   3.7. Indicadores biosísmicos

4. Resultados por Caso (Entregables 4.1-4.2)
   4.1. Drift — Condiciones 1 y 2 (6 casos)
   4.2. Corte en muros eje 1 y eje F (6 casos)

5. Resumen y Conclusiones (Entregable 4.3)
   5.1. Cuadro resumen comparativo
   5.2. Conclusiones

Anexos:
- Tablas modales completas
- Hojas de cálculo Excel (combos, drift, etc.)
- Archivos ETABS (.edb)
```

---

# ERRORES COMUNES Y CÓMO EVITARLOS

| Error                                 | Consecuencia                                  | Solución                                           |
| ------------------------------------- | --------------------------------------------- | --------------------------------------------------- |
| Confundir peso con masa               | Masa duplicada o inexistente                  | Ingresar Weight per Unit Volume, ETABS calcula masa |
| Espectro NCh433 integrado en ETABS    | Clasificación de suelos antigua              | Usar**From File** siempre                     |
| Modal Damping ≠ damping del espectro | ETABS escala valores erróneamente            | Ambos deben ser 0.05                                |
| Losa con inercia 100%                 | Sobrestima acoplamiento, subestima M en muros | Usar 0.25 en m11, m22, m12                          |
| Vigas sin J=0                         | Vigas toman torsión espuria                  | Modifier J=0 en vigas                               |
| Vigas invertidas sin Insertion Point  | Longitud flexible columna incorrecta          | Cardinal Point = Bottom Center                      |
| Diafragma rígido en planta irregular | Resultados erróneos                          | Evaluar semi-rígido                                |
| Muros sin dividir en intersecciones   | No hay conectividad                           | Edit > Divide Shells                                |
| Un Pier para dos muros separados      | Fuerzas combinadas erróneamente              | Un Pier por muro continuo                           |
| Check Model → "Fix"                  | Pérdida de control                           | Corregir manualmente                                |
| Replicar sin todo visible             | Elementos faltantes en pisos                  | Verificar visibilidad antes de Ctrl+A               |
| Config regional (coma/punto)          | Espectro no se lee bien                       | Verificar separador decimal                         |
| Torsión contada dos veces            | Sobredimensionamiento                         | Si mueves CM, Diaph Ecc = 0                         |
| Scale Factor espectro incorrecto      | Fuerzas x10 o /10                             | SF=9.81 si espectro en g, SF=1 si en m/s²          |
| No asignar Auto Edge Constraint       | Incompatibilidad losa-muro                    | Assign > Shell > Auto Edge Constraints              |
| Olvidar restricciones de base         | Mecanismo, análisis falla                    | Assign > Joint > Restraints en BASE                 |
| Usar Story Drifts para Cond. 1       | Story Drifts = drift en esquinas, NO en CM   | Usar Joint Drifts filtrado al nodo del CM           |
| Restar desplaz. manualmente para drift| Error en CQC (no se restan promedios)        | Leer drift directo de tabla — ETABS ya calcula δ/h  |
| No verificar participación modal ≥90%| Resultados espectrales incompletos           | SumUX y SumUY ≥ 0.90, si no aumentar modos         |
| Verificar drift con caso elástico     | Drift sin reducir por R* (sobreestimado)     | Verificar desde combinaciones (Método B) o reducir SF|

---

# CHECKLIST FINAL

## Antes de correr el análisis:

**Geometría y secciones:**
- [ ] Grilla con 17 ejes X + 6 ejes Y (coordenadas verificadas)
- [ ] 20 pisos con alturas correctas (3.4 + 19×2.6)
- [ ] Material G30: Ec=2,624,300 tonf/m², γ=2.5 tonf/m³
- [ ] Material A630-420H: fy=42,000 tonf/m², fu=63,000 tonf/m²
- [ ] Secciones: MHA30G30, MHA20G30, VI20/60G30, Losa15G30
- [ ] J=0 en vigas
- [ ] Inercia losa 25% (m11=m22=m12=0.25)

**Modelo geométrico:**
- [ ] Muros dibujados según planta (verificar visualmente)
- [ ] Muros divididos en intersecciones
- [ ] Vigas dibujadas + punto inserción Bottom Center
- [ ] Losas panel por panel (hueco del shaft)
- [ ] Diafragma D1 asignado a todas las losas
- [ ] Base empotrada (6 DOF restringidos)
- [ ] Auto mesh losas ≤ 1.0 m
- [ ] Auto Edge Constraint activado
- [ ] Pier Labels en muros eje 1 y eje F

**Cargas y masa:**
- [ ] Load Patterns: PP(SWM=1), TERP, TERT, SCP, SCT
- [ ] Tipos correctos: PP=Dead, TERP/TERT=Super Dead, SCP=Live, SCT=Roof Live
- [ ] Cargas asignadas: TERP=0.14, SCP=0.25, TERT=0.10, SCT=0.10
- [ ] Verificación visual de cargas (Display > Show Load Assigns)
- [ ] Mass Source: PP=1, TERP=1, SCP=0.25, TERT=1, SCT=0

**Análisis sísmico:**
- [ ] Espectro cargado desde archivo **From File** (verificado gráficamente)
- [ ] Caso Modal: 30 modos, Eigen, MsSrc1
- [ ] Casos espectrales SDX (U1) y SDY (U2): SF=9.81, CQC, 5% damping
- [ ] Modal Damping = 0.05 = Function Damping Ratio (coinciden)
- [ ] Torsión accidental configurada (3 métodos)
- [ ] Combinaciones NCh3171 definidas (según método de torsión)
- [ ] Envolventes definidas

**Pre-análisis:**
- [ ] **P-Delta activado** (Analyze > Set Analysis Options > Include P-Delta)
- [ ] Solver: Advanced Solver o Multi-threaded
- [ ] Check Model sin errores
- [ ] Full 3D DOF activado (6 DOF)

## Después del análisis:

**Validación inmediata:**
- [ ] Log sin errores (`Analyze > Last Analysis Run Log`)
- [ ] Peso/Área ≈ 1.0 tonf/m² (rango aceptable: 0.85-1.15)
- [ ] Deformadas modales coherentes (sin elementos sueltos vibrando independientemente)
- [ ] Tx* y Ty* razonables (0.8-1.5 s para 20 pisos de muros)
- [ ] **Participación modal ≥ 90%** en X (SumUX) **Y** en Y (SumUY) — si no, aumentar nº modos

**Verificación de drift (para los 6 casos):**
- [ ] **Drift Condición 1**: Drift CM ≤ 0.002 en todos los pisos (tabla Joint Drifts, nodo CM)
- [ ] **Drift Condición 2**: (Max Drift − Drift CM) ≤ 0.001 en todos los pisos (tabla Diaph Max/Avg)
- [ ] Drift verificado en **ambas direcciones** (X e Y) para cada caso
- [ ] Drifts verificados desde **combinaciones** (no desde casos RS individuales si se usa Método B)
- [ ] Gráficos de drift por piso generados en Excel (6 gráficos)
- [ ] Tabla resumen comparativa de drift para los 6 casos completada

**Exportación de resultados:**
- [ ] Resultados exportados a Excel para los 6 casos
- [ ] Pier Forces exportados para muros eje 1 y eje F
- [ ] Modelo guardado como Edificio1_Rigido.edb y Edificio1_SemiRigido.edb
- [ ] Capturas de pantalla del modelo tomadas (3D, planta, elevación, mesh, deformadas)

---

# APÉNDICE: ATAJOS DE TECLADO ÚTILES

| Atajo  | Acción                    |
| ------ | -------------------------- |
| F5     | Run Analysis               |
| F6     | Deformed Shape             |
| Ctrl+T | Show Tables                |
| Ctrl+A | Select All                 |
| Ctrl+R | Replicate                  |
| Ctrl+D | Set Grid System Visibility |
| Ctrl+Z | Undo                       |
| Escape | Terminar comando de dibujo |
| Delete | Borrar selección          |

---

> **Documento generado el 20-03-2026, actualizado el 21-03-2026 (G05)**
> Fuentes: Material Apoyo Taller 2026 (Prof. Music), Paso a Paso ETABS (Lafontaine),
> Manual ETABS v19, Tutorial CSI, NCh3171-2017, NCh433 Mod 2009, DS61.
