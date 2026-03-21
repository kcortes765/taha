# Capítulo 1: Aspectos Conceptuales sobre Diseño Sismorresistente

> **Fuente**: Apuntes Prof. Juan Music Tomicic — UCN
> **Alcance**: Edificios habitacionales y de uso público (NO industriales, ni con aisladores/disipadores)

> **Claude:** Este capítulo es la base teórica de TODO el curso. Acá se definen los conceptos que van a aparecer una y otra vez: diafragmas, matrices de rigidez, torsión, clasificación de edificios y el procedimiento completo del análisis modal espectral. Si entiendes bien esto, el resto del semestre fluye. Si algo queda flojo acá, se arrastra. Tómatelo con calma.

---

## Mapa Conceptual General del Capítulo

```
                        ASPECTOS CONCEPTUALES
                    DISEÑO SISMORRESISTENTE (Cap.1)
                               │
         ┌─────────────┬───────┴───────┬──────────────┬──────────────┐
         │             │               │              │              │
    DEFINICIONES    DIAFRAGMAS    MATRICES DE    CLASIFICACIÓN   ANÁLISIS
    BÁSICAS         Y TORSIÓN     RIGIDEZ        EDIFICIOS       MODAL
         │             │               │              │           ESPECTRAL
    ·Edificio      ·Rígido        ·1 piso        ·Tipo I-V      ·10 Etapas
    ·Estructura    ·Flexible      ·N pisos       ·Altura máx    ·CQC
    ·Subestruc.    ·Semirígido    ·Eq. Directo   ·Sist.resist.  ·Torsión
    ·Exigencias    ·CM/CR         ·Rig. Directa                  accidental
                   ·Torsión
```

---

## 1. Definiciones Básicas

### 1.1 Edificio
Obra construida para la habitación o usos análogos.

```
┌──────────────────────────────────────────┐
│              E D I F I C I O             │
│                                          │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  │
│  │Ambientes│  │Circula- │  │  Vanos   │  │
│  │         │  │ ciones  │  │(puertas, │  │
│  │         │  │         │  │ventanas) │  │
│  └─────────┘  └─────────┘  └─────────┘  │
│                                          │
│  Comunicaciones: escaleras, ascensores,  │
│                  montacargas             │
│  Ductos: instalaciones verticales y      │
│          horizontales                    │
│                                          │
│  ESTRUCTURA = esqueleto resistente       │
│  (debe desarrollarse SIN interferir      │
│   con el proyecto de arquitectura)       │
└──────────────────────────────────────────┘
```

> **Claude:** El punto clave acá es que la estructura NO manda — tiene que acomodarse a la arquitectura. Esto es un desafío real: el arquitecto diseña espacios bonitos y funcionales, y el ingeniero tiene que encontrar la forma de que eso se sostenga ante un sismo. Por eso el diseño sismorresistente es un arte de compromisos, no solo de fórmulas.

### 1.2 Exigencias en Zonas de Sismicidad Alta/Moderada

| Exigencia | Razón |
|:----------|:------|
| Limitación de altura según forma estructural | Control de período y desplazamientos |
| Limitación de materiales de construcción | Garantizar ductilidad y resistencia |
| Disposición simétrica de elementos verticales | **Evitar torsión en planta** |
| Alineación vertical de columnas y muros | Componente vertical del sismo es crítica si no se respeta |
| Evitar volados de grandes luces | Misma razón anterior |
| Materiales livianos en elementos secundarios | Reducir masa sísmica |

> **Claude:** La simetría es quizás la exigencia más importante en la práctica. Si los elementos resistentes (muros, marcos) están mal distribuidos en planta, el edificio va a girar durante el sismo (torsión). Esto es exactamente lo que pasó en muchos edificios dañados en el terremoto del 27F (2010): configuraciones asimétricas que produjeron demandas de torsión no previstas. El profe Music insiste mucho en esto.
>
> La alineación vertical es otra cosa que parece obvia pero que en la realidad se viola seguido. Si un muro del piso 5 no baja hasta la fundación, la fuerza tiene que "buscar camino" para bajar, y eso genera concentraciones de esfuerzo brutales. Los volados grandes amplifican la componente vertical del sismo (que normalmente se ignora o se toma como 2/3 de la horizontal).

### 1.3 Subestructuras

```
                    EDIFICIO
                       │
          ┌────────────┴────────────┐
          │                         │
   SUBESTRUCTURAS            SUBESTRUCTURAS
   HORIZONTALES              VERTICALES
          │                         │
   Plantas de pisos         Superficies planas o
   (diafragmas)             cilíndricas de generatrices
                            verticales que abarcan
                            TODA la altura
                                    │
                        ┌───────────┼───────────┐
                        │           │           │
                      MARCOS      MUROS     MUROS-MARCOS
```

> **Claude:** Esta división en subestructuras horizontales y verticales es la base de CÓMO se modela un edificio para análisis sísmico. Piénsalo así:
> - Las **subestructuras horizontales** (diafragmas = losas de piso) son las que RECIBEN la fuerza sísmica (porque ahí está la masa) y la REPARTEN a los elementos verticales.
> - Las **subestructuras verticales** (marcos, muros) son las que BAJAN esa fuerza hasta la fundación.
>
> Es como un equipo: los diafragmas son los distribuidores y los marcos/muros son los que hacen el trabajo pesado de resistir.

---

## 2. Diafragmas

### 2.1 Definición
> **Diafragma**: Elemento estructural a nivel de un piso que distribuye las fuerzas horizontales (que actúan en su plano) a los elementos verticales resistentes.

> **Claude:** En la práctica, el diafragma es la LOSA del piso. Cuando el sismo mueve la base del edificio, la inercia de la masa de cada piso genera una fuerza horizontal. Esa fuerza nace en la losa (donde está la masa) y la losa la reparte a los muros y marcos. La pregunta clave es: ¿CÓMO la reparte? Y la respuesta depende de si el diafragma es rígido o flexible.

### 2.2 Tipos de Diafragma

```
                    DIAFRAGMAS
                        │
          ┌─────────────┼─────────────┐
          │             │             │
       RÍGIDO      SEMIRÍGIDO     FLEXIBLE
          │             │             │
   Indeformable    Rigidez real   Deformable
   en su plano     de todos los   en su plano
          │        elementos            │
   Distribuye           │          Distribuye
   por RIGIDEZ          │          por ÁREA
   de elementos         │          TRIBUTARIA
          │             │               │
   Considera       Modelo más      NO considera
   excentricidad   realista        excentricidad
```

> **Claude:** En edificios de hormigón armado (que es lo que se ve en Chile para vivienda), las losas son casi siempre **rígidas** en su plano. ¿Por qué? Porque una losa de hormigón de 15-20 cm de espesor es enormemente rígida comparada con los marcos/muros en dirección horizontal.
>
> El diafragma **flexible** es más típico de estructuras con techumbre liviana: galpones industriales con techo de acero, construcciones de madera, etc. En esos casos la losa/techo se deforma tanto que cada muro recibe carga según su área tributaria, como si fuera una viga apoyada en los muros.
>
> El **semirígido** es el modelo más realista (considera la rigidez real de la losa), pero en la práctica se usa poco porque complica el análisis y la diferencia suele ser menor.
>
> **ETABS por defecto asume diafragma rígido** — es lo que van a usar en el taller.

### 2.3 Diafragma Rígido vs Flexible — Comportamiento

```
     DIAFRAGMA RÍGIDO                    DIAFRAGMA FLEXIBLE
     ════════════════                    ══════════════════

     F →→→→→→→→→→→→                     F →→→→→→→→→→→→
     ┌══════════════┐                    ┌──────────────┐
     │   Se mueve   │                    │  Se deforma  │
     │   como un    │                    │  como viga   │
     │   cuerpo     │                    │  en su plano │
     │   rígido     │                    │      ╱╲      │
     └══╤═══╤═══╤══┘                    └──╤──╱──╲─╤──┘
        │   │   │                           │ ╱    ╲│
       M1  M2  M3                          M1      M3
        │   │   │                           │       │
     Según  │ rigidez                    Según área tributaria
     relativa│de cada muro
             │
```

> **Claude:** La analogía más simple:
> - **Rígido** = una regla de acero apoyada en 3 resortes (muros). Si empujas la regla, los resortes más duros (más rígidos) toman más fuerza. La regla no se dobla.
> - **Flexible** = una cuerda elástica apoyada en 3 postes. Si empujas la cuerda, cada poste recibe fuerza según cuánta cuerda tiene a cada lado (área tributaria). La cuerda se deforma.
>
> **Consecuencia práctica**: Con diafragma rígido, un muro muy rígido puede atraer mucha fuerza aunque esté lejos de donde se aplica la carga. Con diafragma flexible, solo importa la cercanía (área tributaria).

### 2.4 Ejemplo Numérico: Distribución de Fuerzas

```
    Carga total: w = 90 kN/m
    ├────3.4m────┼──────6.6m──────┤

    ┃            ┃                ┃
    M1           M2               M3
   (izq)       (centro)         (der)
```

**Caso Flexible** (por área tributaria):

| Muro | Cálculo | Fuerza |
|:-----|:--------|-------:|
| M1 (izq) | 90 × 3.4/2 | **153 kN** |
| M2 (centro) | 90 × (3.4/2 + 6.6/2) | **450 kN** |
| M3 (der) | 90 × 6.6/2 | **297 kN** |
| **Total** | | **900 kN** |

**Caso Rígido**: Se distribuye según la rigidez de cada muro y considerando excentricidad (CM ≠ CR).

> **Claude:** Fíjate cómo en el caso flexible, M2 se lleva la mitad de la carga total (450 de 900 kN) simplemente porque tiene área tributaria a ambos lados. Eso es intuitivo: el muro del medio "sostiene" más largo de losa.
>
> En el caso rígido, la distribución puede ser MUY diferente. Si por ejemplo M3 es mucho más rígido que los otros (un muro de 8 metros de largo vs muros de 2 metros), M3 podría llevarse el 70-80% de la fuerza total aunque su área tributaria sea solo el 33%. **La rigidez manda, no la geometría de la planta.** Además, si CM ≠ CR, aparece torsión que redistribuye aún más las fuerzas.

### 2.5 Índice de Flexibilidad (ASCE 7-16)

```
                    DMD
         IF = ───────────
                   DPEV

    Donde:
    DMD  = Desplazamiento máximo del diafragma
    DPEV = Desplazamiento promedio de los elementos verticales


         IF ≤ 2.0  ──→  Diafragma RÍGIDO
         IF > 2.0  ──→  Diafragma FLEXIBLE
```

> **Claude:** Este criterio es cuantitativo y viene de la norma americana ASCE 7-16 (no de la NCh433 chilena, que no define un criterio numérico explícito). La idea es: si el diafragma se deforma más del doble que el promedio de lo que se desplazan los muros, entonces ya no se puede considerar rígido.
>
> **¿Cómo se mide en la práctica?** Se modela el edificio en ETABS con diafragma semirígido, se aplica la carga lateral, y se mide cuánto se deforma la losa vs. cuánto se mueven los muros. Si IF ≤ 2, puedes usar diafragma rígido tranquilo.

---

## 3. Centro de Masa, Centro de Rigidez y Torsión

> **Claude:** Esta sección es FUNDAMENTAL. La torsión es una de las principales causas de daño sísmico en edificios. Toda la teoría de matrices de rigidez que viene después se apoya en entender bien qué son CM, CR y por qué su separación genera problemas.

### 3.1 Definiciones Clave

```
┌─────────────────────────────────────────────────────────┐
│                    PLANTA DE PISO                        │
│                                                         │
│              CM ●────── ex ──────● CR                   │
│          (Centro de           (Centro de                │
│           Masa)                Rigidez)                  │
│                                                         │
│   CM = Centro de gravedad de las MASAS del piso         │
│   CR = Centro de gravedad de las RIGIDECES de los       │
│        elementos resistentes a fuerza sísmica del piso  │
│                                                         │
│   ex = Excentricidad Natural (o inherente)              │
│      = Distancia entre CM y CR                          │
└─────────────────────────────────────────────────────────┘
```

> **Claude:** Piénsalo con una analogía simple. Imagina una bandeja (la losa) sostenida por resortes (los muros):
>
> - **CM** es donde está concentrado el peso en la bandeja. Ahí "nace" la fuerza sísmica (F = m × a, y la masa está en el CM).
> - **CR** es donde están concentradas las "resistencias" de los resortes. Es el punto alrededor del cual el piso tiende a rotar si se aplica un momento.
>
> Si CM = CR, la fuerza pasa directo por donde está la resistencia → **traslación pura**, sin giro.
> Si CM ≠ CR, la fuerza actúa en un punto y la resistencia está en otro → se genera un **momento de torsión** = F × distancia. El piso rota.
>
> **Ejemplo real**: Un edificio con todos los muros concentrados en un extremo (ej: caja de escaleras y ascensor en una esquina) y masa distribuida uniformemente → CM al centro, CR cerca de la esquina → excentricidad grande → torsión grande → PELIGRO.

### 3.2 Tipos de Excentricidad

```
    ┌─────────────────────────────────────────────┐
    │                                             │
    │   EXCENTRICIDAD NATURAL (ex)                │
    │   = Distancia CM → CR                       │
    │   Causa: geometría y distribución           │
    │          de rigideces                        │
    │                                             │
    │   EXCENTRICIDAD ACCIDENTAL (ea)             │
    │   Causa: cambios de posición de             │
    │          sobrecargas + tolerancias           │
    │          constructivas                      │
    │                                             │
    │   EXCENTRICIDAD DE DISEÑO (et)              │
    │   et = ex ± ea                              │
    │                                             │
    │   Se generan 2 casos:                       │
    │     Caso I:  et = ex - ea                   │
    │     Caso II: et = ex + ea                   │
    │                                             │
    └─────────────────────────────────────────────┘
```

> **Claude:** La excentricidad **natural** es la que puedes calcular con planos: sabes dónde están los muros (→ CR) y sabes cómo se distribuye la masa (→ CM). Es "determinista".
>
> La excentricidad **accidental** existe porque la realidad no es perfecta:
> - La sobrecarga de uso (gente, muebles) no está uniformemente distribuida como se supone en el cálculo. Puede haber un evento con mucha gente en un lado del edificio.
> - Las tolerancias constructivas hacen que un muro no quede exactamente donde dice el plano.
> - La rigidez real de los materiales puede variar.
>
> La norma NCh433 en su artículo 6.3.4 define cómo calcular ea. No es un capricho — es una protección contra la incertidumbre.
>
> **El ± es crítico**: Se toman AMBOS signos porque no sabes hacia qué lado se va a mover la excentricidad accidental. Puede empeorar o mejorar la situación. Diseñas con el **peor caso para cada elemento**.

### 3.3 Momento Torsional

```
                    V (Fuerza sísmica)
                    │
                    ▼
    ┌───────────────────────────────────┐
    │               │                   │
    │     CM ●──────┼──── et ────● CR   │
    │               │                   │
    │               │                   │
    └───────────────────────────────────┘

    Momento Torsional = V × et

    Se analizan DOS casos de diseño:
    ┌────────────────────────────────────────┐
    │  MT₁ = V × (ex - ea)  ← Caso I        │
    │  MT₂ = V × (ex + ea)  ← Caso II       │
    │                                        │
    │  Se diseña con el MÁS DESFAVORABLE     │
    │  para cada elemento                    │
    └────────────────────────────────────────┘
```

> **Claude:** "El más desfavorable para cada elemento" es clave. No es que tomes un solo caso para todo el edificio. Un muro que está cerca del CR puede ser más desfavorable con Caso I, mientras que un muro lejano puede ser peor con Caso II. En ETABS esto se hace automáticamente: corre ambos casos y toma las envolventes.
>
> **¿Cuántos análisis son en total?** Para sismo en X: 3 (sin torsión accidental, con +ea, con -ea). Para sismo en Y: otros 3. Total = 6 análisis. Esto es lo que se verá en la Etapa 10 más adelante.

---

## 4. Matrices de Rigidez de Edificios con Diafragma Rígido

> Referencia: "Dinámica de Estructuras" — Anil Chopra, 4ª edición

> **Claude:** Esta sección viene directamente del libro de Chopra y del libro de Riddell & Hidalgo. Es la parte más "matemática" del capítulo, pero la idea física es simple: **¿cómo traduzco las propiedades de cada marco/muro individual en una matriz de rigidez que represente al edificio completo?**
>
> Hay dos caminos para llegar a lo mismo:
> 1. **Equilibrio directo**: Aplico desplazamientos unitarios uno a uno y veo qué fuerzas aparecen → los coeficientes de la matriz.
> 2. **Rigidez directa**: Tomo la rigidez de cada marco, la "transformo" al sistema de coordenadas global del edificio, y sumo todo.
>
> Ambos dan la misma matriz. El método de rigidez directa es el que usan los programas (ETABS, SAP2000) porque es más sistemático y programable.

### 4.1 Edificio de UN Piso — Grados de Libertad

```
       y
       ▲
       │         Marco A (dir. Y)
       │            │
       │     ┌──────┼──────┐
       │     │      │      │
   d/2─┤     │   CM ●      │
       │     │   (O)│      │
   d/2─┤     │      │← e →│← Marco A a distancia e del CM
       │     └──────┼──────┘
       │     Marco B│     Marco C
       └─────────────────────────→ x
             (dir. X)   (dir. X)

    3 GDL por piso:
    ┌────────────────────────────┐
    │  ux  →  traslación en X   │
    │  uy  →  traslación en Y   │
    │  uθ  →  rotación torsional│
    └────────────────────────────┘
```

> **Claude:** ¿Por qué 3 GDL por piso y no más? Porque asumimos **diafragma rígido**. Si la losa es rígida en su plano, todo el piso se mueve como un cuerpo rígido en 2D: puede trasladarse en X, trasladarse en Y, y rotar θ. Esos 3 movimientos definen completamente la posición de CUALQUIER punto del piso. No necesitas saber qué hace cada punto individual — basta con saber qué hace el centro de masa.
>
> Esto es una simplificación enorme: un piso que podría tener cientos de GDL (cada nodo) se reduce a solo 3. Para un edificio de 20 pisos: 60 GDL en lugar de miles. **Esa es la magia del diafragma rígido.**
>
> Fíjate que los GDL se definen en el **centro de masa** (punto O). Esto es intencional: así la matriz de masa queda diagonal (sin términos acoplados de masa), lo cual simplifica enormemente el problema dinámico.

### 4.2 Método de Equilibrio Directo (Coeficientes de Influencia de Rigidez)

Se impone desplazamiento unitario en cada GDL y se determinan las fuerzas resultantes:

```
    (a) ux = 1, uy = uθ = 0           (b) uy = 1, ux = uθ = 0
    ┌──────────────────┐               ┌──────────────────┐
    │  kxx = kxB + kxC │               │  kxy = 0         │
    │  kyx = 0         │               │  kyy = ky        │
    │  kθx = d/2·      │               │  kθy = e·ky      │
    │       (kxC - kxB)│               │                  │
    └──────────────────┘               └──────────────────┘

    (c) uθ = 1, ux = uy = 0
    ┌──────────────────────────────┐
    │  kxθ = d/2·(kxC - kxB)      │
    │  kyθ = e·ky                  │
    │  kθθ = e²·ky + d²/4·(kxB+kxC)│
    └──────────────────────────────┘
```

> **Claude:** Esto es el mismo principio que usaste en Análisis Estructural cuando calculabas la matriz de rigidez de una viga: aplicas un desplazamiento unitario en un GDL, fijas los demás en cero, y mides qué fuerzas necesitas aplicar para mantener esa configuración. Esas fuerzas son los coeficientes de la columna correspondiente de la matriz.
>
> **¿Por qué kxy = 0?** Porque los marcos B y C están orientados en X, y el marco A en Y. Si desplazas en Y (caso b), los marcos B y C no generan fuerza en X (son "libres" perpendicular a su plano). Solo A trabaja. Esto pasa por la geometría particular de este ejemplo. En un caso general con marcos inclinados, kxy ≠ 0.
>
> **¿Por qué kθx = d/2·(kxC - kxB)?** Si kxB = kxC (marcos simétricos), este término es CERO → no hay acoplamiento torsión-traslación en X. Eso es lo que pasa cuando el edificio es simétrico respecto al eje x.

### 4.3 Matriz de Rigidez Resultante (1 piso)

```
         ┌                                              ┐
         │  kxB + kxC         0        d/2·(kxC - kxB)  │
    k =  │     0              ky           e·ky          │
         │  d/2·(kxC - kxB)  e·ky    e²ky + d²/4·(kxB+kxC) │
         └                                              ┘
```

> **Claude:** Observa la estructura de esta matriz — dice TODO sobre el comportamiento del edificio:
>
> - **Diagonal**: Rigidez "pura" de cada GDL (traslación X, traslación Y, rotación).
> - **Fuera de diagonal**: Acoplamiento entre GDL. Si hay ceros, esos movimientos son independientes. Si hay valores, están acoplados.
>
> El término **e·ky** (posición [2,3] y [3,2]) acopla uy con uθ. Esto significa: si el edificio se mueve en Y, TAMBIÉN rota. ¿Cuándo desaparece? Cuando e = 0 → CM = CR → **sin excentricidad, no hay acoplamiento lateral-torsional**.
>
> El término **d/2·(kxC - kxB)** (posición [1,3] y [3,1]) acopla ux con uθ. Desaparece cuando kxB = kxC → marcos simétricos en X.
>
> **Conclusión práctica**: Un edificio simétrico en ambas direcciones tiene matriz diagonal → todo se desacopla → análisis MUCHO más simple.

### 4.4 Método de Rigidez Directa

**Paso 1**: Definir matrices de transformación para cada marco:

```
    Marco A (dir. Y):  ayA = ⟨ 0   1   e   ⟩    →  uA = uy + e·uθ
    Marco B (dir. X):  axB = ⟨ 1   0  -d/2 ⟩    →  uB = ux - (d/2)·uθ
    Marco C (dir. X):  axC = ⟨ 1   0   d/2 ⟩    →  uC = ux + (d/2)·uθ
```

> **Claude:** Estas matrices de transformación son pura **cinemática** (geometría del movimiento). La pregunta es: "si el centro de masa se mueve ux, uy, uθ, ¿cuánto se desplaza lateralmente cada marco?"
>
> Tomemos el marco A como ejemplo: `uA = uy + e·uθ`. El marco A está en dirección Y, a distancia e del CM. Si el piso traslada uy, el marco A se desplaza uy. Pero si el piso ROTA uθ, el marco A (que está a distancia e del centro de rotación) también se desplaza e·uθ adicional. Es el efecto de brazo de palanca: rotación × distancia = desplazamiento.
>
> Lo mismo para B y C: el signo -d/2 vs +d/2 refleja que están a lados opuestos del CM. Si el piso rota, uno se acerca y el otro se aleja.

**Paso 2**: Obtener matriz de cada marco en coordenadas globales:

```
    ki = aᵀ · k_lateral · a

                   ┌       ┐       ┌         ┐       ┌        ┐
                   │0  0  0│       │1  0 -d/2 │       │1  0 d/2│
    kA = ky·       │0  1  e│  kB=kxB│0  0  0  │ kC=kxC│0  0  0 │
                   │0  e e²│       │-d/2 0 d²/4│      │d/2 0 d²/4│
                   └       ┘       └          ┘       └        ┘
```

**Paso 3**: Sumar → `k = kA + kB + kC` → Resulta la misma matriz que con equilibrio directo.

> **Claude:** La fórmula `ki = aᵀ · k · a` es la misma transformación de coordenadas que viste en Análisis Estructural. Es como "proyectar" la rigidez local de cada marco al sistema global del edificio. Es elegante porque es completamente mecánica: defines las matrices a, multiplicas, sumas, y listo. No necesitas pensar caso por caso como en equilibrio directo.
>
> **Este es el método que usan los programas.** ETABS internamente hace exactamente esto para cada elemento del modelo.

### 4.5 Casos Especiales

```
    ┌─────────────────────────────────────────────────────────────┐
    │  SISTEMA ASIMÉTRICO EN 2 DIRECCIONES (caso general)        │
    │  kxB ≠ kxC, e ≠ 0                                         │
    │  → 3 ecuaciones ACOPLADAS (ux, uy, uθ)                    │
    │  → Sismo en X produce: desplaz. X + Y + torsión           │
    ├─────────────────────────────────────────────────────────────┤
    │  SISTEMA ASIMÉTRICO EN 1 DIRECCIÓN                         │
    │  kxB = kxC = kx, e ≠ 0                                    │
    │  → ux se DESACOPLA → ecuación de 1GDL independiente        │
    │  → uy y uθ quedan ACOPLADOS (2 ecuaciones)                 │
    ├─────────────────────────────────────────────────────────────┤
    │  SISTEMA SIMÉTRICO                                         │
    │  kxB = kxC = kx, e = 0                                    │
    │  → 3 ecuaciones DESACOPLADAS                               │
    │  → Sismo X → solo ux  |  Sismo Y → solo uy  |  θ indep.  │
    └─────────────────────────────────────────────────────────────┘
```

> **Claude:** Estos 3 casos son pregunta clásica de control. Asegúrate de entender la lógica:
>
> **Caso general (asimétrico en 2 dir.):** Todo acoplado. Un sismo que viene en X hace que el edificio se mueva en X, pero TAMBIÉN en Y y TAMBIÉN rote. Es el caso más desfavorable y el más común en la realidad (la simetría perfecta casi no existe).
>
> **Asimétrico en 1 dir.:** Si los marcos en X son iguales (B=C), la estructura es simétrica respecto al eje x. Sismo en X → solo traslación en X (se resuelve como 1GDL simple). Pero sismo en Y → traslación Y + torsión acoplados (porque e ≠ 0 → el marco A no está centrado).
>
> **Simétrico:** El caso ideal. Todo independiente. Es lo que se busca al diseñar — aunque rara vez se logra perfectamente.
>
> **Truco para el control**: Si te dan un edificio y te preguntan qué pasa si aplicas sismo en una dirección, mira la simetría. Si es simétrico en esa dirección → solo traslación. Si no → acoplamiento lateral-torsional.

### 4.6 Ecuación de Movimiento (1 piso, caso general)

```
    ┌       ┐   ┌    ┐     ┌              ┐   ┌  ┐       ┌       ┐
    │ m     │   │ üx │     │kxx  0   kxθ  │   │ux│       │m·ügx  │
    │   m   │ · │ üy │  +  │ 0  kyy  kyθ  │ · │uy│  = −  │m·ügy  │
    │     IO│   │ üθ │     │kθx kθy  kθθ  │   │uθ│       │IO·ügθ │
    └       ┘   └    ┘     └              ┘   └  ┘       └       ┘

    Donde:
    m  = masa del diafragma
    IO = m·(b² + d²)/12  = momento de inercia del diafragma
    ügx, ügy = aceleración del terreno en X e Y
```

> **Claude:** Esta es la ecuación maestra de un edificio de 1 piso. Es la misma `M·ü + K·u = -M·üg` que viste en Dinámica de Estructuras, pero ahora en 3 GDL.
>
> **IO = m·(b² + d²)/12**: Es el momento de inercia de masa de la losa rectangular de dimensiones b × d, asumiendo masa uniformemente distribuida. Es análogo al momento de inercia de sección que usas en resistencia de materiales, pero con masa en vez de área.
>
> El lado derecho `-m·üg(t)` son las **fuerzas sísmicas efectivas**: la fuerza que "siente" la estructura por la aceleración del suelo. Nota que para traslación es proporcional a m (masa) y para rotación a IO (inercia rotacional). **Si la masa es mayor, la fuerza sísmica es mayor** → por eso se buscan estructuras livianas.

---

## 5. Edificio de VARIOS Pisos con Diafragma Rígido

### 5.1 Grados de Libertad

```
    Para N pisos → 3N grados de libertad totales:

    Piso j:  ujx (traslación X),  ujy (traslación Y),  ujθ (rotación)

              Piso N ──→  uNx, uNy, uNθ
              Piso j ──→  ujx, ujy, ujθ
                ...
              Piso 2 ──→  u2x, u2y, u2θ
              Piso 1 ──→  u1x, u1y, u1θ
```

> **Claude:** La extensión de 1 piso a N pisos es directa: cada piso tiene sus 3 GDL, definidos en su propio centro de masa. Un edificio de 20 pisos tiene 60 GDL.
>
> **Nota importante del profe Music**: Los pisos se enumeran de ABAJO hacia ARRIBA. El piso 1 es el primero sobre el suelo, el piso N es el último (techo). Esto es la convención que usa en los apuntes y es la misma que usa ETABS.

### 5.2 Método de Rigidez Directa (N pisos) — 4 Pasos

```
┌─────────────────────────────────────────────────────────────────────┐
│ PASO 1: Matriz de rigidez lateral de cada marco (N×N)              │
│                                                                     │
│   Para cada marco i:                                                │
│   a) Definir GDL del marco: desplazamientos laterales a nivel piso │
│   b) Obtener matriz de rigidez completa                            │
│   c) Condensar estáticamente GDL rotacionales y verticales         │
│   → Resultado: kxi (N×N) si marco en dir.X                        │
│                 kyi (N×N) si marco en dir.Y                        │
├─────────────────────────────────────────────────────────────────────┤
│ PASO 2: Matrices de transformación (N × 3N)                        │
│                                                                     │
│   Marco en dir. Y:  ayi = [ O  |  I  |  xi·I ]                    │
│   Marco en dir. X:  axi = [ I  |  O  | -yi·I ]                    │
│                                                                     │
│   xi, yi = coordenadas del marco i en planta                       │
│   I = identidad N×N,  O = ceros N×N                               │
├─────────────────────────────────────────────────────────────────────┤
│ PASO 3: Transformar a coordenadas globales                         │
│                                                                     │
│   ki = aᵀxi · kxi · axi    (marco dir. X)                         │
│   ki = aᵀyi · kyi · ayi    (marco dir. Y)                         │
├─────────────────────────────────────────────────────────────────────┤
│ PASO 4: Sumar todas las contribuciones                             │
│                                                                     │
│   K_edificio = Σ ki    (para todos los marcos)                     │
└─────────────────────────────────────────────────────────────────────┘
```

> **Claude:** Es exactamente lo mismo que para 1 piso, pero las matrices son más grandes:
> - Las `k` de cada marco ahora son N×N (una fila/columna por piso)
> - Las matrices de transformación `a` ahora son N×3N
> - La matriz del edificio `K` es 3N×3N
>
> **La condensación estática (Paso 1c)** es un concepto que viene de Análisis Estructural. Un marco tiene muchos GDL (desplazamientos horizontales, verticales y rotaciones en cada nodo). Pero para el edificio con diafragma rígido, solo nos interesan los desplazamientos LATERALES a nivel de piso. Los demás GDL se eliminan por condensación estática (no aportan GDL independientes porque están "esclavizados" por el diafragma rígido). El resultado es una matriz más pequeña que solo relaciona fuerzas laterales con desplazamientos laterales.

### 5.3 Estructura de la Matriz de Rigidez del Edificio (3N × 3N)

```
              ┌                    ┐
              │  Kxx    0    Kxθ   │
    K_edif =  │   0    Kyy   Kyθ   │       Cada submatriz es N×N
              │  Kθx   Kθy   Kθθ   │
              └                    ┘

    Donde:
    ┌──────────────────────────────────────────┐
    │  Kxx = Σ kxi                             │
    │  Kyy = Σ kyi                             │
    │  Kθθ = Σ (xi²·kyi + yi²·kxi)            │
    │  Kxy = 0                                 │
    │  Kxθ = Σ (-yi·kxi)                       │
    │  Kyθ = Σ (xi·kyi)                         │
    └──────────────────────────────────────────┘
```

> **Claude:** Fíjate en la analogía con el caso de 1 piso:
> - **Kxx** sigue siendo la suma de rigideces de marcos en X.
> - **Kyy** sigue siendo la suma de rigideces de marcos en Y.
> - **Kθθ** incluye los "xi²·kyi + yi²·kxi" que son el equivalente del e²·ky + d²/4·(kxB+kxC) pero generalizado para cualquier configuración.
>
> **El término Kxy = 0** siempre, porque los marcos están orientados en X o Y (ortogonales). Si hubiera marcos inclinados, Kxy ≠ 0.
>
> **Kθθ** es especialmente interesante: depende del **cuadrado de las distancias** de los marcos al CM. Marcos lejanos al centro aportan MUCHO más rigidez torsional que marcos cercanos. **Por eso se busca poner los muros en el perímetro del edificio** → máxima rigidez torsional → mínima torsión.

### 5.4 Ecuación de Movimiento (N pisos)

```
    ┌       ┐       ┌              ┐          ┌       ┐   ┌ ┐         ┌ ┐         ┌ ┐
    │ m     │ {ü} + │ Kxx  0   Kxθ │ {u}  = − │ m     │·(│1│ügx(t) + │0│ügy(t) + │0│ügθ(t))
    │   m   │       │  0  Kyy  Kyθ │          │   m   │  │0│         │1│         │0│
    │     IO│       │ Kθx Kθy  Kθθ │          │     IO│  │0│         │0│         │1│
    └       ┘       └              ┘          └       ┘   └ ┘         └ ┘         └ ┘

    m = diagonal N×N (masas de cada piso)
    IO = diagonal N×N (momentos de inercia de cada diafragma)
```

> **Claude:** Los vectores `{1, 0, 0}`, `{0, 1, 0}`, `{0, 0, 1}` son los **vectores de influencia sísmica** (ι). Cada uno "enciende" una dirección de excitación.
>
> En la práctica, ügθ (aceleración rotacional del terreno) normalmente se ignora porque no se mide con acelerómetros estándar. Así que quedan solo 2 componentes: sismo en X y sismo en Y, que se analizan por separado.

---

## 6. Clasificación Sismo-Resistente de Edificios

> **Claude:** Esta clasificación es la forma en que el profe Music organiza los sistemas estructurales. No viene de una norma específica sino que es una clasificación didáctica basada en la experiencia constructiva mundial. Es importante para predimensionamiento: según el tipo de sistema, tienes un rango de alturas máximas "razonables".

```
┌──────────┬──────────────────────────────────┬──────────────┐
│   TIPO   │  SISTEMA RESISTENTE              │  ALTURA MÁX  │
├══════════╪══════════════════════════════════╪══════════════┤
│          │                                  │              │
│  TIPO I  │  Marcos Rígidos                  │  20-22 pisos │
│          │                                  │              │
│          │   ┌──┬──┬──┐                     │              │
│          │   ├──┼──┼──┤  (pórticos)         │              │
│          │   ├──┼──┼──┤                     │              │
│          │   └──┴──┴──┘                     │              │
├──────────┼──────────────────────────────────┼──────────────┤
│          │                                  │              │
│  TIPO II │  Muros de Rigidez Simples        │  30-35 pisos │
│          │                                  │              │
│          │   ┌┐    ┌┐    ┌┐                 │              │
│          │   ││    ││    ││  (muros aislados)│              │
│          │   ││    ││    ││                 │              │
│          │   └┘    └┘    └┘                 │              │
├──────────┼──────────────────────────────────┼──────────────┤
│          │                                  │              │
│ TIPO III │  Muros de Rigidez Acoplados      │  30-35 pisos │
│          │                                  │              │
│          │   ┌┐════┌┐                       │              │
│          │   ││    ││  (muros + vigas de    │              │
│          │   ││════││   acoplamiento)       │              │
│          │   └┘    └┘                       │              │
├──────────┼──────────────────────────────────┼──────────────┤
│          │                                  │              │
│  TIPO IV │  Marcos + Muros (simple/acoplado)│  45-50 pisos │
│          │                                  │              │
│          │   ┌┐─┬──┬─┌┐                     │              │
│          │   ││─┼──┼─││ (sistema dual)      │              │
│          │   ││─┼──┼─││                     │              │
│          │   └┘─┴──┴─└┘                     │              │
├──────────┼──────────────────────────────────┼──────────────┤
│          │                                  │              │
│  TIPO V  │  Tubo Simple / Tubo en Tubo /    │  50-65 pisos │
│          │  Tubo Múltiple                   │              │
│          │                                  │              │
│          │   ┌──────────┐                   │  Simple: 50-60│
│          │   │┌────────┐│                   │  En tubo:60-65│
│          │   ││  tubo  ││                   │              │
│          │   ││interior││                   │              │
│          │   │└────────┘│                   │              │
│          │   └──────────┘                   │              │
└──────────┴──────────────────────────────────┴──────────────┘
```

> **Claude:** Contexto chileno:
> - **Tipo II (muros simples)** es EL sistema dominante en Chile para edificios habitacionales de 10-25 pisos. La tradición constructiva chilena es de muros de hormigón armado.
> - **Tipo I (marcos)** es más común en edificios bajos y en países como EEUU, Japón, México.
> - **Tipo IV (dual)** se usa en edificios altos chilenos (30+ pisos) y es el sistema del edificio del taller.
> - **Tipo V (tubo)** es para rascacielos (Costanera Center, por ejemplo).
>
> Los **muros acoplados** (Tipo III) son dos muros conectados por vigas cortas (vigas de acoplamiento). Estas vigas disipan energía y permiten que el sistema sea más eficiente que muros simples. Son comunes en Chile alrededor de puertas y ventanas.

### Comparación visual de alturas máximas

```
    Pisos
    65 ┤                                              ████
    60 ┤                                              ████
    55 ┤                                              ████
    50 ┤                                    ████      ████
    45 ┤                                    ████      ████
    40 ┤                                    ████
    35 ┤                  ████    ████       ████
    30 ┤                  ████    ████       ████
    25 ┤                  ████    ████       ████
    22 ┤      ████        ████    ████       ████
    20 ┤      ████        ████    ████       ████
    15 ┤      ████        ████    ████       ████
    10 ┤      ████        ████    ████       ████
     5 ┤      ████        ████    ████       ████
     0 ┼──────────────────────────────────────────────────
          Tipo I      Tipo II  Tipo III   Tipo IV    Tipo V
          Marcos      Muros    Muros      Marcos+    Tubo
          Rígidos    Simples  Acoplados   Muros
```

---

## 7. Análisis Dinámico de Superposición Modal Espectral

> **Claude:** Este es el PROCEDIMIENTO COMPLETO que se usa en Chile (y en casi todo el mundo) para analizar edificios ante sismos. Es lo que hacen ETABS y SAP2000 internamente. El profe Music lo presenta en 10 etapas + 9 pasos detallados. Si entiendes este flujo, entiendes qué hace el software y puedes interpretar (y cuestionar) los resultados.
>
> El nombre "superposición modal espectral" significa:
> - **Modal**: descompones el movimiento del edificio en sus modos de vibrar (como descomponer una onda en sus frecuencias).
> - **Espectral**: para cada modo, usas un espectro de diseño para obtener la respuesta máxima.
> - **Superposición**: combinas las respuestas de todos los modos para obtener la respuesta total (usando CQC u otro método de combinación).

### Diagrama de Flujo: Las 10 Etapas

```
    ┌─────────────────────────────────────────────┐
    │  ETAPA 1: Estructurar el edificio           │
    └──────────────────┬──────────────────────────┘
                       ▼
    ┌─────────────────────────────────────────────┐
    │  ETAPA 2: Identificar subestructuras        │
    │           verticales resistentes            │
    └──────────────────┬──────────────────────────┘
                       ▼
    ┌─────────────────────────────────────────────┐
    │  ETAPA 3: Matriz de rigidez de cada         │
    │           subestructura (coord. locales)     │
    └──────────────────┬──────────────────────────┘
                       ▼
    ┌─────────────────────────────────────────────┐
    │  ETAPA 4: Condensación estática →           │
    │           Matriz de rigidez LATERAL          │
    │           de cada subestructura [Kp]         │
    └──────────────────┬──────────────────────────┘
                       ▼
    ┌─────────────────────────────────────────────┐
    │  ETAPA 5: Matriz de rigidez del EDIFICIO    │
    │           (respecto al centro de masa)       │
    │                                             │
    │  Caso 1: CM en misma vertical → método      │
    │          directo                            │
    │  Caso 2: CM no coinciden → método de        │
    │          rigidez directa con [Ap]           │
    │                                             │
    │  K = Σ [Ap]ᵀ·[Kp]·[Ap]                     │
    └──────────────────┬──────────────────────────┘
                       ▼
    ┌─────────────────────────────────────────────┐
    │  ETAPA 6: Matriz de MASAS (diagonal)        │
    └──────────────────┬──────────────────────────┘
                       ▼
    ┌─────────────────────────────────────────────┐
    │  ETAPA 7: Frecuencias y modos de vibrar     │
    │           [K - ω²·M]{φ} = 0                 │
    │           → Periodos Ti y Matriz Modal [Φ]  │
    └──────────────────┬──────────────────────────┘
                       ▼
    ┌─────────────────────────────────────────────┐
    │  ETAPA 8: Normalizar modos de vibrar        │
    │           (dibujar modos normalizados)       │
    └──────────────────┬──────────────────────────┘
                       ▼
    ┌─────────────────────────────────────────────┐
    │  ETAPA 9: Masas Equivalentes (participación)│
    │                                             │
    │  ┌──────┬──────┬──────┬──────┬──────┬─────┐ │
    │  │ Modo │  T   │Ux(%) │Uy(%) │Rz(%) │ΣUx  │ │
    │  │      │(seg) │Mnx/M │Mny/M │MnƟ/J │     │ │
    │  ├──────┼──────┼──────┼──────┼──────┼─────┤ │
    │  │  1   │      │      │      │      │     │ │
    │  │  2   │      │      │      │      │     │ │
    │  │ ...  │      │      │      │      │     │ │
    │  │  3n  │      │      │      │      │     │ │
    │  └──────┴──────┴──────┴──────┴──────┴─────┘ │
    │                                             │
    │  Determinar Tx*, Ty*, Tz*                   │
    └──────────────────┬──────────────────────────┘
                       ▼
    ┌─────────────────────────────────────────────┐
    │  ETAPA 10: Análisis Sísmico (NCh433 + DS61) │
    │            Para SISMO X y SISMO Y           │
    └──────────────────┬──────────────────────────┘
                       ▼
              (Ver detalle abajo)
```

> **Claude:** Comentarios por etapa:
>
> **Etapa 1-2**: Son etapas de INGENIERÍA, no de cálculo. Decidir cómo estructurar el edificio (dónde poner muros, marcos) y cuáles son los elementos que resisten sismo. Esto lo hace el ingeniero con criterio, no el software.
>
> **Etapa 3-4**: La condensación estática elimina los GDL internos de cada marco/muro y deja solo los desplazamientos laterales a nivel de piso. Es lo que ETABS hace cuando defines un diafragma rígido.
>
> **Etapa 5**: El Caso 1 (CM en misma vertical) es la situación ideal y más común en edificios regulares. El Caso 2 (CM no coinciden) ocurre en edificios con plantas que cambian forma en altura. En ambos casos se usa `K = Σ [Ap]ᵀ·[Kp]·[Ap]`.
>
> **Etapa 7**: El problema de valores propios `[K - ω²M]{φ} = 0` es el corazón matemático. De acá salen los períodos de vibración (T = 2π/ω) y las formas modales (φ). ETABS resuelve esto automáticamente.
>
> **Etapa 8**: Normalizar los modos es conveniente para simplificar cálculos posteriores. Hay varias formas de normalizar (por masa, por componente máxima, etc.).
>
> **Etapa 9**: La tabla de masas equivalentes es MUY importante. Te dice qué modos son relevantes y en qué dirección. Si el Modo 1 tiene Ux=65%, Uy=0%, Rz=35% → es principalmente traslacional en X con algo de torsión. Si la suma acumulada ΣUx llega a 90% con 5 modos, puedes usar solo 5 modos para sismo en X (NCh433 exige ≥ 90%).
>
> **Tx*, Ty*, Tz***: Son los períodos fundamentales "predominantes" en cada dirección. Se usan para verificar límites de la norma.

### Etapa 10 — Detalle: 9 Pasos del Análisis Sísmico

```
┌─────────────────────────────────────────────────────────────────┐
│                    SISMO EN DIRECCIÓN X                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  PASO 1: Corte basal combinado (CQC)                           │
│  ┌──────────────────────────────────────┐                       │
│  │  Qix = Mix × Sa(Ti)                 │                       │
│  │  Sa(Ti) = espectro de diseño NCh433  │                       │
│  │                                      │                       │
│  │  Verificar: Qmin ≤ Qbasal ≤ Qmax    │                       │
│  │  Si Q < Qmin → amplificar espectro   │                       │
│  │               fmin = Qmin/Q_calc     │                       │
│  └──────────────────────────────────────┘                       │
│                                                                 │
│  PASO 2: Factores de participación modal                       │
│                                                                 │
│  PASO 3: Desplazamientos por modo {q}n_max = {un, vn, θn}max  │
│                                                                 │
│  PASO 4: Verificar condición de desplazamiento (norma)         │
│          ¿Cumple? ─── NO → Modificar estructuración            │
│             │                                                   │
│            SÍ                                                   │
│             ▼                                                   │
│  PASO 5: Solicitaciones sísmicas en CM por modo                │
│                                                                 │
│          3 ANÁLISIS REQUERIDOS:                                │
│          ┌─────────────────────────────────────┐               │
│          │ i)   Sismo X SIN torsión accidental │               │
│          │ ii)  Sismo X + torsión acc. (+)     │               │
│          │ iii) Sismo X + torsión acc. (-)     │               │
│          └─────────────────────────────────────┘               │
│                                                                 │
│  ═══ CASO: SIN TORSIÓN ACCIDENTAL ═══                          │
│                                                                 │
│  PASO 6: Desplazamientos laterales por subestructura y modo    │
│          {up} = [Ap]{q}n                                       │
│                                                                 │
│  PASO 7: Fuerzas laterales por subestructura y modo            │
│          {Fp} = [Kp]{up}                                       │
│                                                                 │
│  PASO 8: Esfuerzos internos → superponer con CQC              │
│          (Axial, Corte, Momento en cada viga y columna)        │
│                                                                 │
│  ═══ CASOS: CON TORSIÓN ACCIDENTAL ═══                         │
│                                                                 │
│  PASO 9: Torsión accidental (art. 6.3.4b NCh433)              │
│          · Determinar ea y Mt = V × ea en cada piso            │
│          · Caso (+): Mt antihorario                            │
│          · Caso (-): Mt horario                                │
│          · Repetir Pasos 6-8 para cada caso                   │
│          · Sumar/restar a esfuerzos sin torsión accidental     │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                    SISMO EN DIRECCIÓN Y                         │
│           Repetir todos los pasos (1 a 9)                      │
│           para la dirección Y                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  DISEÑO FINAL: Considerar esfuerzos más desfavorables          │
│  de TODOS los estados de carga según NCh 3171                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

> **Claude:** Desglose paso a paso:
>
> **Paso 1 — Corte basal**: `Qix = Mix × Sa(Ti)` es la fuerza total en la base para el modo i. Mix es la masa equivalente del modo i en dirección X, y Sa(Ti) es la aceleración espectral para el período Ti. Luego se combinan todos los modos con CQC (Combinación Cuadrática Completa) para obtener el corte basal total.
>
> La norma NCh433 define un **Qmin** (corte mínimo, para que no se diseñe con fuerzas ridículamente bajas) y un **Qmax** (corte máximo, para no penalizar excesivamente). Si tu corte calculado es menor que Qmin, debes amplificar TODO el espectro por fmin = Qmin/Qcalc. Esto es muy común en edificios altos con períodos largos.
>
> **Paso 4 — Desplazamientos**: La norma limita el drift (desplazamiento relativo entre pisos dividido por la altura de entrepiso). Si no cumple, hay que rigidizar la estructura (agregar muros, aumentar secciones). **No puedes seguir con el diseño si no cumples desplazamientos.**
>
> **Paso 8 — CQC**: La Combinación Cuadrática Completa es un método estadístico para combinar las respuestas modales. No se suman directamente (porque los máximos de cada modo no ocurren al mismo tiempo). CQC considera la correlación entre modos, lo cual es importante cuando los períodos son cercanos. Es el método que exige la NCh433.
>
> **Paso 9 — Torsión accidental**: Es el paso que más confunde. La idea es: el análisis "sin torsión accidental" ya incluye la torsión NATURAL (por CM ≠ CR). Pero la norma pide ADEMÁS considerar una torsión extra (accidental) que se suma o resta. Son momentos aplicados en cada piso. En ETABS se configura directamente.

---

## 8. Resumen de Fórmulas Clave

### Matrices

| Concepto | Fórmula |
|:---------|:--------|
| Rigidez lateral marco | `ki = aᵀ · k_lat · a` |
| Rigidez edificio | `K = Σ ki` (todos los marcos) |
| Rigidez edificio (general) | `K = Σ [Ap]ᵀ [Kp] [Ap]` |
| Momento inercia diafragma | `IO = m·(b² + d²)/12` |

### Torsión

| Concepto | Fórmula |
|:---------|:--------|
| Excentricidad de diseño | `et = ex ± ea` |
| Momento torsional | `MT = V × et` |

### Diafragma

| Concepto | Fórmula |
|:---------|:--------|
| Índice de flexibilidad | `IF = DMD / DPEV` |
| Criterio ASCE 7-16 | `IF ≤ 2.0 → rígido` |

### Dinámica

| Concepto | Fórmula |
|:---------|:--------|
| Problema de valores propios | `[K - ω²M]{φ} = 0` |
| Corte basal modo i | `Qi = Mi × Sa(Ti)` |
| Ecuación de movimiento | `M·ü + K·u = -M·ι·üg(t)` |

---

## 9. Mapa de Relaciones: Todo el Capítulo

```
    ESTRUCTURA DEL EDIFICIO
           │
    ┌──────┴──────┐
    │             │
  HORIZONTAL    VERTICAL
  (diafragma)   (marcos/muros)
    │             │
    │        ┌────┴────┐
    │        │         │
    │     Rigidez    Coord.
    │     lateral    en planta
    │     [Kp]       (xi,yi)
    │        │         │
    │        └────┬────┘
    │             │
    │        TRANSFORMACIÓN
    │        [Ap] = f(xi,yi)
    │             │
    │        RIGIDEZ GLOBAL
    │        K = Σ [Ap]ᵀ[Kp][Ap]
    │             │
    ├─────────────┤
    │             │
  MASAS [M]    RIGIDEZ [K]
    │             │
    └──────┬──────┘
           │
     PROBLEMA DINÁMICO
     [K - ω²M]{φ} = 0
           │
    ┌──────┴──────┐
    │             │
  Periodos Ti   Modos φi
    │             │
    └──────┬──────┘
           │
     MASAS EQUIVALENTES
     (participación modal)
           │
     ANÁLISIS SÍSMICO
     (NCh433 + DS61)
           │
    ┌──────┼──────┐
    │      │      │
  Sin TA  +TA   -TA
    │      │      │
    └──────┼──────┘
           │
     ESFUERZOS INTERNOS
     (CQC por modo)
           │
     DISEÑO (NCh 3171)
```

> **Claude:** Este mapa es tu guía para entender el flujo completo. Si te pierdes en algún paso del análisis modal espectral, ubícate acá y verás de dónde vienes y a dónde vas. Todo empieza con la estructura física (geometría + materiales) y termina con esfuerzos de diseño. En el medio, las matemáticas (matrices, eigenvalores, espectros) son el puente.
