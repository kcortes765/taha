# Capítulo 2a: Conceptos Fundamentales de Ingeniería Sísmica

> **Fuente**: Apuntes Prof. Juan Music Tomicic — UCN
> **Contenido**: Riesgo sísmico, conceptos de diseño (rigidez, energía, ductilidad), estrategias de protección sísmica, etapas de un proyecto de edificio.

> **Claude:** Este capítulo es más "filosófico" que el anterior — menos fórmulas y más conceptos. Pero no lo subestimes: acá se define POR QUÉ diseñamos como diseñamos. Si en el control te preguntan "explique conceptualmente qué es la ductilidad y por qué importa en diseño sísmico", la respuesta sale de acá. El profe Music usa mucho estas preguntas conceptuales.

---

## Mapa Conceptual General

```
                    CONCEPTOS FUNDAMENTALES
                    INGENIERÍA SÍSMICA (Cap.2a)
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
    RIESGO SÍSMICO     CONCEPTOS DE          ETAPAS DE UN
    Y VULNERABILIDAD   DISEÑO                PROYECTO
          │                   │                   │
    ·Peligro           ·Rigidez              ·Roles
    ·Vulnerabilidad    ·Energía              ·Documentos
    ·Fuentes           ·Ductilidad           ·Flujo completo
                       ·Convencional
                       ·Aisladores
                       ·Disipadores
```

---

## 1. Riesgo Sísmico

### 1.1 Ecuación Fundamental

```
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                         ║
    ║   RIESGO SÍSMICO = PELIGRO SÍSMICO × VULNERABILIDAD    ║
    ║                                                         ║
    ╚═══════════════════════════════════════════════════════════╝
```

```
    PELIGRO SÍSMICO                    VULNERABILIDAD SÍSMICA
    ═══════════════                    ══════════════════════
    ┌──────────────────┐               ┌──────────────────────┐
    │  Condición       │               │  Condición de la     │
    │  NATURAL         │               │  CONSTRUCCIÓN        │
    │                  │               │                      │
    │  NO se puede     │               │  SÍ se puede         │
    │  intervenir      │               │  CONTROLAR           │
    │                  │               │                      │
    │  Propia de       │               │  ← ÚNICA forma de    │
    │  cada región     │               │    reducir el riesgo │
    └──────────────────┘               └──────────────────────┘
```

> **Claude:** Esta ecuación es la idea más importante del capítulo. Es simple pero profunda:
>
> - **Peligro sísmico**: Chile está en el Cinturón de Fuego del Pacífico. Antofagasta es Zona 3 (la más alta según NCh433). Esto NO lo puedes cambiar. Va a haber terremotos grandes, es solo cuestión de tiempo.
>
> - **Vulnerabilidad**: ES lo que controlas como ingeniero. Puedes hacer que un edificio en Zona 3 sea seguro (baja vulnerabilidad) o puedes hacer que un edificio en Zona 1 sea peligroso (alta vulnerabilidad).
>
> **Ejemplo real**: El terremoto del 27F (2010) en Chile fue Mw 8.8 (peligro altísimo). Los edificios bien diseñados según normativa sufrieron daño menor o ninguno. Los edificios con problemas de diseño o construcción colapsaron o quedaron irrecuperables. Mismo peligro, distinta vulnerabilidad → distinto riesgo.
>
> **Ejemplo opuesto**: Haití 2010, Mw 7.0 (peligro moderado). Más de 200.000 muertos. ¿Por qué? Vulnerabilidad extrema: construcciones de mampostería sin refuerzo, sin ingeniería, sin normativa. El peligro era menor que en Chile, pero la vulnerabilidad era enormemente mayor.

### 1.2 Fuentes de Vulnerabilidad

```
    ┌──────────────────────────────────────────────────────────┐
    │              FUENTES DE VULNERABILIDAD                    │
    │                                                          │
    │   ┌──────────────┐                                       │
    │   │ LOCALIZACIÓN │  Zona sísmica, tipo de suelo,        │
    │   │              │  cercanía a fallas                    │
    │   └──────┬───────┘                                       │
    │          ▼                                               │
    │   ┌──────────────────────────────┐                       │
    │   │ PROYECTO ARQUITECTÓNICO-     │  Configuración,       │
    │   │ ESTRUCTURAL Y NORMAS         │  irregularidades,     │
    │   │ DE DISEÑO                    │  cumplimiento norma   │
    │   └──────┬───────────────────────┘                       │
    │          ▼                                               │
    │   ┌──────────────┐                                       │
    │   │  MATERIALES  │  Calidad del hormigón, acero,        │
    │   │              │  propiedades mecánicas reales         │
    │   └──────┬───────┘                                       │
    │          ▼                                               │
    │   ┌──────────────┐                                       │
    │   │ CONSTRUCCIÓN │  Calidad de ejecución,               │
    │   │              │  supervisión, control calidad         │
    │   └──────┬───────┘                                       │
    │          ▼                                               │
    │   ┌──────────────────┐                                   │
    │   │ MANTENIMIENTO    │  Mantención durante TODA          │
    │   │                  │  la vida útil del edificio        │
    │   └──────────────────┘                                   │
    │                                                          │
    └──────────────────────────────────────────────────────────┘
```

> **Claude:** Desglose con ejemplos concretos:
>
> **1. Localización**: No es solo la zona sísmica. El tipo de suelo es crucial. Un suelo blando (tipo IV según NCh433) amplifica las ondas sísmicas → más daño. Antofagasta tiene sectores con rellenos artificiales que amplifican mucho. También importa la cercanía a la costa (tsunami) y a fallas activas.
>
> **2. Proyecto**: Acá entra TODO lo que hace el ingeniero civil y el arquitecto. Irregularidades en planta (L, T, U), irregularidades en altura (pisos blandos, retranqueos), configuraciones torsionalmente vulnerables. Las normas chilenas (NCh433, DS61, DS60) regulan esto, pero hay que CUMPLIRLAS correctamente.
>
> **3. Materiales**: Un hormigón que especifica f'c = 30 MPa pero que en obra sale de 22 MPa es un problema. Las probetas de ensayo son clave. El acero también: si usas barras sin certificación, no sabes su ductilidad real.
>
> **4. Construcción**: Un plano puede ser perfecto, pero si el fierrero no respeta el recubrimiento, o si el hormigón se vibra mal, o si las juntas de construcción quedan mal hechas, la estructura es vulnerable. La inspección técnica de obra (ITO) existe para controlar esto.
>
> **5. Mantenimiento**: Un edificio de 30 años con corrosión en sus armaduras (por carbonatación o cloruros en zona costera como Antofagasta) ha perdido capacidad resistente. El mantenimiento NO es opcional.

### 1.3 Cadena de Reducción de Riesgo

```
    PELIGRO SÍSMICO (fijo)
         │
         │  ×  ¿Cómo reducir?
         │         │
         ▼         ▼
    ┌─── Vulnerabilidad ───┐
    │  Localización        │ ← Elegir sitio adecuado
    │  Proyecto            │ ← Buen diseño + normas vigentes
    │  Materiales          │ ← Especificación correcta
    │  Construcción        │ ← Control de calidad riguroso
    │  Mantenimiento       │ ← Preservar durante vida útil
    └──────────────────────┘
              │
              ▼
    ═══ MENOR RIESGO SÍSMICO ═══
```

> **Claude:** Nota que las 5 fuentes de vulnerabilidad representan las 5 etapas de la vida de un edificio: ubicación → diseño → materiales → construcción → uso. Un fallo en CUALQUIERA de ellas aumenta el riesgo. La cadena es tan fuerte como su eslabón más débil.

---

## 2. Conceptos Importantes de Diseño Sismorresistente

> **Claude:** El profe Music presenta tres conceptos que forman la "tríada" del diseño sismorresistente: rigidez, energía y ductilidad. Los tres están conectados y todo diseño sísmico busca un balance entre ellos. Estos tres conceptos responden a tres preguntas:
> - **Rigidez**: ¿Cuánto se mueve la estructura?
> - **Energía**: ¿Cuánta demanda sísmica puede absorber?
> - **Ductilidad**: ¿Cuánto puede deformarse sin colapsar?

### 2.1 Rigidez

```
    F (Fuerza)
    ▲
    │         ╱
    │        ╱
    │       ╱  ← Pendiente = RIGIDEZ (k)
    │      ╱
    │     ╱     k = F / δ
    │    ╱
    │   ╱
    │  ╱
    │ ╱
    ├──────────────────→ δ (Desplazamiento)
    0

    ┌─────────────────────────────────────────────┐
    │  RIGIDEZ (k):                               │
    │  Capacidad de un elemento de resistir       │
    │  deformación ante una fuerza aplicada.      │
    │                                             │
    │  Mayor k → Menor deformación → Período      │
    │           más corto → Mayor aceleración      │
    │                                             │
    │  Menor k → Mayor deformación → Período      │
    │           más largo → Menor aceleración      │
    │           (pero mayor desplazamiento)        │
    └─────────────────────────────────────────────┘
```

> **Claude:** La rigidez es la pendiente de la curva fuerza-desplazamiento en el rango elástico. Es un concepto que ya conoces de Resistencia de Materiales (k = EA/L para barra axial, k = 3EI/L³ para viga en voladizo, etc.).
>
> Lo nuevo acá es la CONEXIÓN con el período y la aceleración espectral. Recuerda de Dinámica de Estructuras:
>
> ```
>     T = 2π√(m/k)
> ```
>
> Si k es grande → T es corto → en el espectro de diseño, períodos cortos tienen aceleraciones ALTAS. Entonces la estructura rígida "atrae" más fuerza pero se desplaza menos.
>
> Si k es pequeño → T es largo → aceleraciones BAJAS en el espectro. Menos fuerza, pero más desplazamiento.
>
> **No hay solución mágica**: todo es un trade-off. Más rígido = más fuerza pero menos desplazamiento. Más flexible = menos fuerza pero más desplazamiento. El ingeniero elige el punto de equilibrio.

**Relación Rigidez-Período-Aceleración:**

```
    Estructura         Estructura
    RÍGIDA             FLEXIBLE
    (k alto)           (k bajo)
       │                  │
       ▼                  ▼
    T corto            T largo
       │                  │
       ▼                  ▼
    Sa alto            Sa bajo
    (más aceler.)      (menos aceler.)
       │                  │
       ▼                  ▼
    δ pequeño          δ grande
    (poco desplaz.)    (mucho desplaz.)
```

> **Claude:** Un ejemplo concreto:
> - **Edificio de 5 pisos de muros (T ≈ 0.3s)**: Rígido, T corto, Sa alto → recibe mucha fuerza, pero se mueve poco. Los muros son gruesos y no se agrietan.
> - **Edificio de 25 pisos de marcos (T ≈ 2.0s)**: Flexible, T largo, Sa bajo → recibe menos fuerza relativa, pero los desplazamientos son grandes. Hay que controlar el drift.
>
> La NCh433 limita el drift precisamente por esto: un edificio flexible puede cumplir en fuerza pero fallar en desplazamientos.

### 2.2 Energía Absorbida y Disipada

```
    F ▲
      │     ┌────── Curva de carga
      │    ╱│╲
      │   ╱ │ ╲
      │  ╱  │  ╲──── Curva de descarga
      │ ╱   │   ╲
      │╱    │    ╲
      ├─────┼─────╲───→ δ
      0     │
            │
            ▼

    ┌──────────────────────────────────────────────┐
    │  ENERGÍA ABSORBIDA (Es):                     │
    │  Área bajo la curva de carga                 │
    │  = Energía que entra al sistema              │
    │                                              │
    │  ENERGÍA DISIPADA (Ed):                      │
    │  Área encerrada dentro del ciclo             │
    │  histerético (lazo de histéresis)            │
    │  = Energía que se transforma en calor/daño   │
    │                                              │
    │  ENERGÍA RECUPERABLE (Er):                   │
    │  Er = Es - Ed                                │
    │  = Energía elástica almacenada               │
    └──────────────────────────────────────────────┘
```

> **Claude:** La energía es el concepto más intuitivo si lo piensas en términos cotidianos:
>
> Cuando un sismo sacude un edificio, le "inyecta" energía (energía de entrada). El edificio tiene que hacer algo con esa energía. Hay 3 opciones:
> 1. **Almacenarla elásticamente** (como un resorte comprimido → se recupera)
> 2. **Disiparla por amortiguamiento** (fricción, viscosidad → se convierte en calor)
> 3. **Disiparla por daño** (agrietamiento, fluencia del acero → deformación permanente)
>
> Un **material elástico perfecto** absorbe y devuelve toda la energía → la curva de carga y descarga son la misma → no hay lazo → no disipa energía → rebota indefinidamente.
>
> Un **material con histéresis** (como el hormigón armado en rango inelástico) disipa energía en cada ciclo → el área del lazo es la energía disipada. Cuanto más "gordo" es el lazo, más energía disipa.

**Ciclo Histerético (lazo de histéresis):**

```
    F ▲
      │        ╱──────╮
      │       ╱       │
      │      ╱    Ed  │  ← Área sombreada = energía DISIPADA
      │     ╱  (área) │
      │────╱──────────┤
      │   ╱           │
      │──╱────────────┤
      │ ╱       ╱     │
      │╱───────╱──────┘
    ──┼─────────────────→ δ
      │╲───────╲
      │ ╲       ╲
      │  ╲───────╲
      │
      │   Mayor área del lazo
      │   = Mayor energía disipada
      │   = Mayor capacidad de
      │     absorber sismos
```

> **Claude:** El ciclo histerético es la "huella digital" del comportamiento sísmico de un elemento. En un ensayo de laboratorio, se somete una columna o muro a ciclos de carga-descarga lateral y se grafican los lazos de histéresis.
>
> **Lazos estables y gordos** = buen comportamiento sísmico (ejemplo: viga de HA bien confinada).
> **Lazos que se degradan y se "pellizcan"** = mal comportamiento (ejemplo: muro sin confinamiento adecuado, columna con falla frágil de corte).
>
> El 27F (2010) mostró que los muros de hormigón armado con bajo confinamiento tenían lazos que se degradaban rápidamente → los nuevos requisitos del DS60 exigen mayor confinamiento en elementos de borde de muros.

### 2.3 Ductilidad

```
    F ▲
      │
   Fy ├─────────────────────────╮  ← Fluencia
      │        ╱                │
      │       ╱                 │  Zona PLÁSTICA
      │      ╱                  │  (deformación permanente)
      │     ╱   Zona ELÁSTICA   │
      │    ╱    (recuperable)   │
      │   ╱                     │
      │  ╱                      │
      │ ╱                       │
      ├─────────┬───────────────┼──→ δ
      0        δy              δu

                 │←──── δu ────→│
                 │←─ δy ─→│

    ╔═══════════════════════════════════════════════╗
    ║                                               ║
    ║           μ = δu / δy                         ║
    ║                                               ║
    ║   μ = Ductilidad de desplazamiento            ║
    ║   δy = Desplazamiento de fluencia             ║
    ║   δu = Desplazamiento último (capacidad máx)  ║
    ║                                               ║
    ╚═══════════════════════════════════════════════╝
```

> **Claude:** La ductilidad es probablemente el concepto MÁS importante de todo el diseño sismorresistente. ¿Por qué?
>
> Porque el diseño sísmico convencional se basa en una premisa fundamental: **la estructura VA a incursionar en rango inelástico durante un sismo severo**. No se diseña para que permanezca elástica (eso sería carísimo e impráctico). Se diseña para que se deforme plásticamente de manera CONTROLADA sin colapsar.
>
> Eso solo es posible si la estructura es DÚCTIL (μ grande). Si es frágil (μ ≈ 1), pasa de elástico a colapso sin transición.
>
> **¿Qué hace dúctil a un elemento de hormigón armado?**
> - Buen confinamiento (estribos cerrados, espaciados adecuadamente)
> - Cuantía de acero controlada (no excesiva — la sobrecuantía genera falla frágil)
> - Falla por flexión (dúctil) en vez de falla por corte (frágil)
> - Acero de refuerzo con buena elongación a la rotura
>
> **Valores típicos de ductilidad:**
> - Muro sin confinar: μ ≈ 2-3
> - Muro bien confinado: μ ≈ 5-8
> - Marco dúctil (viga): μ ≈ 6-10
> - Mampostería no reforzada: μ ≈ 1-1.5 (FRÁGIL → prohibida en Zona 3)

**Comportamiento según ductilidad:**

```
    F ▲
      │
      │   Frágil (μ ≈ 1)         Dúctil (μ >> 1)
      │      │╲                      ┌──────────────╮
      │      │ ╲                    ╱│              │
      │      │  ╲                  ╱ │   GRAN       │
      │     ╱│   ╲ ← FALLA       ╱  │  capacidad   │
      │    ╱ │    ╲  SÚBITA      ╱   │  de deform.  │
      │   ╱  │     ╲            ╱    │              │
      │  ╱   │      ╲         ╱     │              │
      │ ╱    │                ╱      │              │
      ├──────┴────────────────┴──────┴──────────────→ δ
      0
          │←→│ corto              │←───── largo ────→│

    ┌──────────────────────────────────────────────────┐
    │  FRÁGIL: Falla sin aviso, colapso repentino      │
    │  DÚCTIL: Se deforma mucho antes de fallar,       │
    │          da AVISO, permite redistribución de      │
    │          esfuerzos → DESEABLE en diseño sísmico  │
    └──────────────────────────────────────────────────┘
```

> **Claude:** "Da AVISO" es la clave. Un elemento dúctil se agrieta visiblemente, se deforma, las puertas no cierran, las ventanas se quiebran — TODO ANTES de colapsar. Hay tiempo para evacuar. Un elemento frágil colapsa sin señales previas.
>
> Esto conecta directamente con la filosofía de diseño de la norma chilena:
> 1. **Sismo frecuente** (período de retorno ~50 años): La estructura debe permanecer ELÁSTICA. Sin daño.
> 2. **Sismo de diseño** (período de retorno ~475 años): Daño reparable. La estructura entra en rango inelástico pero mantiene su integridad.
> 3. **Sismo extremo** (período de retorno ~2500 años): No debe colapsar. Puede quedar irrecuperable, pero la gente se salva.
>
> Para cumplir 2 y 3, NECESITAS ductilidad.

### 2.4 Relación entre los 3 Conceptos

```
    ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
    │   RIGIDEZ    │     │   ENERGÍA    │     │  DUCTILIDAD  │
    │              │     │              │     │              │
    │  Controla    │     │  Disipa la   │     │  Permite     │
    │  los desplaz.│────→│  demanda     │←────│  deformación │
    │  y fuerzas   │     │  sísmica     │     │  sin colapso │
    │              │     │              │     │              │
    │  k = F/δ     │     │  Ed = ∮F·dδ  │     │  μ = δu/δy   │
    └──────┬───────┘     └──────┬───────┘     └──────┬───────┘
           │                    │                    │
           └────────────────────┼────────────────────┘
                                │
                    DISEÑO SISMORRESISTENTE
                    busca el BALANCE entre los 3
```

> **Claude:** El balance funciona así:
>
> - Si **solo buscas rigidez** (k muy alto): El edificio no se mueve pero atrae muchísima fuerza. Necesitas secciones enormes → caro y pesado → atrae aún más fuerza (por más masa). Círculo vicioso.
>
> - Si **solo buscas ductilidad** (μ muy alto): El edificio se deforma mucho. Puede sobrevivir el sismo, pero los daños son tan grandes que es irrecuperable. Además, el contenido (personas, equipos) sufre por los desplazamientos excesivos.
>
> - Si **solo buscas disipar energía**: Sin rigidez mínima, los desplazamientos son enormes. Sin ductilidad, no hay deformación inelástica para disipar.
>
> **La receta exitosa (diseño chileno):**
> Rigidez ADECUADA (muros que controlan drift) + ductilidad SUFICIENTE (confinamiento en zonas críticas) + disipación de energía como CONSECUENCIA de los dos anteriores.

---

## 3. Estrategias de Protección Sísmica

### 3.1 Ecuación de Movimiento (base del concepto)

```
    m·ü + c·u̇ + k·u = -m·üg(t)

    Donde:
    ┌──────┬────────────────────────────────────┐
    │  m   │  Masa de la estructura             │
    │  c   │  Amortiguamiento                   │
    │  k   │  Rigidez                           │
    │  ü   │  Aceleración relativa              │
    │  u̇   │  Velocidad relativa                │
    │  u   │  Desplazamiento relativo           │
    │  üg  │  Aceleración del terreno (sismo)   │
    └──────┴────────────────────────────────────┘
```

> **Claude:** Esta ecuación conecta TODA la teoría de diseño sísmico. Cada estrategia de protección modifica uno o más términos:
>
> ```
>     m·ü  +  c·u̇  +  k·u  =  -m·üg(t)
>     ───     ───     ───      ─────────
>     inercia  amort.  rigidez   excitación
> ```
>
> - **Convencional**: Modifica k (diseño de rigidez) y acepta daño (ductilidad = energía disipada por deformación inelástica).
> - **Aislación**: Reduce k dramáticamente → alarga T → reduce la excitación efectiva que llega a la superestructura.
> - **Disipadores**: Aumenta c → más energía se disipa por amortiguamiento → menos demanda sobre la estructura.

### 3.2 Tres Estrategias de Diseño

```
┌────────────────────────────────────────────────────────────────────┐
│                  3 ESTRATEGIAS DE PROTECCIÓN SÍSMICA               │
├────────────────────┬─────────────────────┬─────────────────────────┤
│                    │                     │                         │
│   CONVENCIONAL     │    AISLACIÓN        │     DISIPACIÓN          │
│                    │    SÍSMICA          │     DE ENERGÍA          │
│                    │                     │                         │
│  Modifica:         │  Modifica:          │  Modifica:              │
│  · k (rigidez)     │  · k (la reduce)   │  · c (lo aumenta)      │
│  · ductilidad      │  · T (lo alarga)   │                         │
│                    │                     │                         │
│   ┌────┐           │   ┌────┐            │   ┌────┐               │
│   │////│           │   │    │            │   │    │               │
│   │////│           │   │    │            │   │╲  ╱│ ← Disipador  │
│   │////│           │   │    │            │   │ ╲╱ │   (diagonal)  │
│   │////│           │   │    │            │   │ ╱╲ │               │
│   │////│           │   ├────┤            │   │╱  ╲│               │
│   └────┘           │   │≈≈≈≈│ ← Aislador│   │    │               │
│   ══════           │   └────┘            │   └────┘               │
│   (suelo)          │   ══════            │   ══════               │
│                    │                     │                         │
│  Se acepta daño    │  Reduce la demanda  │  Absorbe energía       │
│  controlado.       │  sísmica sobre la   │  que llegaría a la     │
│  Estructura        │  superestructura.   │  estructura.           │
│  diseñada para     │  Estructura se      │  Reduce deformación    │
│  disipar energía   │  mueve como cuerpo  │  y daño.               │
│  mediante          │  rígido sobre los   │                         │
│  deformación       │  aisladores.        │                         │
│  inelástica.       │                     │                         │
│                    │                     │                         │
│  Costo: menor      │  Costo: mayor       │  Costo: intermedio     │
│  Daño: mayor       │  Daño: mínimo       │  Daño: reducido        │
└────────────────────┴─────────────────────┴─────────────────────────┘
```

> **Claude:** Profundicemos en cada una:
>
> **CONVENCIONAL**: Es lo que se usa en el 95%+ de los edificios en Chile. La filosofía es: "acepto que la estructura se dañe, pero la diseño para que no colapse". El daño controlado (fluencia del acero, agrietamiento del hormigón) DISIPA energía. Es barato, bien entendido, y funciona. Todo este curso se enfoca en diseño convencional.
>
> **AISLACIÓN SÍSMICA**: Se ponen dispositivos flexibles (aisladores elastoméricos o de péndulo de fricción) entre la fundación y la superestructura. La superestructura "flota" sobre los aisladores. Durante un sismo, la base se mueve pero los aisladores absorben el desplazamiento y la superestructura apenas se mueve. Ejemplo en Chile: Nuevo Hospital de Antofagasta (aislado), Hospital Militar de Santiago. Es más caro pero el edificio queda prácticamente sin daño → ideal para hospitales, centros de datos, edificios esenciales.
>
> **DISIPADORES**: Se agregan dispositivos (viscosos, de fricción, metálicos) que absorben energía sísmica. Pueden ir en diagonales (como arriostramiento) o entre pisos. La estructura mantiene su rigidez pero el amortiguamiento efectivo aumenta de ~5% a ~15-25%. Ejemplo: Torre Titanium en Santiago tiene disipadores viscosos.
>
> **¿Por qué el curso se enfoca en convencional?** Porque es lo que se usa masivamente en Chile, es lo que la norma NCh433 cubre en detalle, y es el fundamento que necesitas entender antes de pasar a sistemas avanzados (que se ven en cursos de posgrado).

### 3.3 Efecto en el Espectro de Respuesta

```
    Sa ▲
    (aceler.)
       │
       │  ╱╲
       │ ╱  ╲    CONVENCIONAL
       │╱    ╲   (T corto, Sa alto)
       │●     ╲
       │       ╲
       │        ╲──────────
       │         ╲    DISIPADORES
       │          ╲   (mismo T, menor Sa
       │           ●   por mayor ξ)
       │            ╲
       │             ╲────── AISLACIÓN
       │                   ● (T largo, Sa bajo)
       │
       ├────────────────────────────→ T (período)
       0

    Convencional: T corto, Sa alto → mucha fuerza, poca deformación
    Aislación:    T largo, Sa bajo → poca fuerza, estructura casi intacta
    Disipadores:  T similar, ξ alto → reduce respuesta sin cambiar T
```

> **Claude:** Este gráfico es clave para la pregunta de control "explique gráficamente cómo funcionan las tres estrategias de protección sísmica".
>
> Recuerda que el espectro de respuesta tiene curvas para distintos amortiguamientos (ξ = 2%, 5%, 10%, 20%...). A mayor ξ, la curva está más abajo → menor Sa para el mismo T.
>
> - **Convencional**: Estás en la zona alta del espectro (T corto, ξ ≈ 5%). Recibes mucha aceleración.
> - **Disipadores**: Mismo T, pero saltas a una curva con ξ mayor → bajas la aceleración sin cambiar la rigidez.
> - **Aislación**: Te mueves a la derecha (T largo) → la curva misma baja. Es como "escapar" de la zona peligrosa del espectro.
>
> **Analogía**: Imagina que estás en un río con corriente fuerte. Convencional = te paras firme y aguantas (fuerte pero sufres). Aislación = te subes a un bote que flota sobre la corriente (no sientes nada). Disipadores = pones una red que frena la corriente antes de que te llegue.

---

## 4. Etapas de un Proyecto de Edificio

> **Claude:** Esta sección parece "administrativa" pero es importante para entender el ROL del ingeniero estructural dentro del proyecto completo. En el control pueden preguntar "describa las etapas de un proyecto de edificio y los roles involucrados".

### 4.1 Actores Principales

```
    ┌───────────────────────────────────────────────────┐
    │                    MANDANTE                       │
    │  (Inmobiliaria, Empresa, Particular)              │
    └────────────┬──────────────────────────────────────┘
                 │ encarga
                 ▼
    ┌────────────────────────┐
    │      ARQUITECTO        │──→ Proyecto de Arquitectura
    │                        │    (según requerimientos del
    │  Respeta:              │     mandante + Plan Regulador
    │  · Plan Regulador      │     + O.G.U.C.)
    │  · O.G.U.C.           │
    └────────────┬───────────┘
                 │ coordina con
         ┌───────┼───────────────────┐
         │       │                   │
         ▼       ▼                   ▼
    ┌─────────┐ ┌──────────────┐ ┌────────────────┐
    │MECÁNICO │ │  INGENIERO   │ │INSTALACIONES   │
    │DE SUELOS│ │ ESTRUCTURAL  │ │(agua, elec,    │
    │         │ │              │ │gas, alcant,    │
    │ Estudio │ │ · Memoria    │ │teléfono, etc.) │
    │ de suelo│ │   de Cálculo │ │                │
    │         │ │ · Espec.     │ │                │
    │         │ │   Técnicas   │ │                │
    └────┬────┘ └──────┬───────┘ └───────┬────────┘
         │             │                 │
         └─────────────┼─────────────────┘
                       ▼
              ┌─────────────────┐
              │ PROYECTO FINAL  │
              └────────┬────────┘
                       │
                       ▼
    ┌──────────────────────────────────┐
    │   REVISIÓN INDEPENDIENTE         │
    │   (Ing. Revisor Cálculo Estruc.) │
    │   (Ley 19.748)                   │
    └────────────┬─────────────────────┘
                 │
                 ▼
    ┌──────────────────────────────────┐
    │  Revisor de Arquitectura         │
    └────────────┬─────────────────────┘
                 │
                 ▼
         PRESENTACIÓN A D.O.M.
```

> **Claude:** Aclaraciones sobre cada actor:
>
> **Mandante**: Quien paga. Puede ser una inmobiliaria (lo más común en edificios habitacionales), una empresa (para su sede), o un particular. Define el programa (cuántos departamentos, qué uso, presupuesto).
>
> **Arquitecto**: Lidera el proyecto. El Plan Regulador define qué se puede construir (altura máxima, uso de suelo, coeficiente de constructibilidad). La O.G.U.C. (Ordenanza General de Urbanismo y Construcciones) define las reglas generales. El arquitecto es el "director de orquesta" del proyecto.
>
> **Mecánico de Suelos**: Hace la investigación geotécnica (calicatas, SPT, ensayo de placa). Define el tipo de suelo (I, II, III, IV según NCh433), la capacidad de soporte, el nivel freático, etc. Sin esto, el ingeniero estructural no puede diseñar las fundaciones ni definir el espectro de diseño.
>
> **Ingeniero Estructural**: Diseña la estructura. Produce la Memoria de Cálculo (documento que justifica todos los cálculos) y las Especificaciones Técnicas (cómo construir: materiales, recubrimientos, empalmes, etc.). Es TU futuro rol.
>
> **Revisor de Cálculo Estructural**: Desde la Ley 19.748, es OBLIGATORIO que un ingeniero independiente revise el cálculo estructural. No es el mismo que diseñó. Es un control de calidad externo. Los revisores están registrados en www.restructural.cl.

### 4.2 Flujo Completo del Proyecto

```
    ┌─────────────────────────────────────────────┐
    │  1. PROYECTO FINAL                          │
    │     ┌──────────────┐                        │
    │     │ Arquitectura │                        │
    │     │ Ingeniería   │ → Memoria de Cálculo   │
    │     │ Estructural  │ → Espec. Técnicas      │
    │     │ Instalaciones│                        │
    │     └──────────────┘                        │
    └──────────────────┬──────────────────────────┘
                       │
                       ▼
    ┌─────────────────────────────────────────────┐
    │  2. REVISIÓN INDEPENDIENTE                  │
    │     · Revisor Cálculo Estructural           │
    │     · Revisor Arquitectura                  │
    └──────────────────┬──────────────────────────┘
                       │
                       ▼
    ┌─────────────────────────────────────────────┐
    │  3. PRESENTACIÓN A D.O.M.                   │
    │     (Dirección de Obras Municipales)         │
    └──────────────────┬──────────────────────────┘
                       │
                       ▼
    ╔═════════════════════════════════════════════╗
    ║  4. OBTENCIÓN DEL PERMISO DE CONSTRUCCIÓN  ║
    ╚══════════════════════╤══════════════════════╝
                           │
                           ▼
    ┌─────────────────────────────────────────────┐
    │  5. EJECUCIÓN DE LA CONSTRUCCIÓN            │
    │     + Inspección especializada              │
    │     (Control de calidad)                    │
    └──────────────────┬──────────────────────────┘
                       │
                       ▼
    ┌─────────────────────────────────────────────┐
    │  6. RECEPCIÓN FINAL por D.O.M.             │
    └──────────────────┬──────────────────────────┘
                       │
                       ▼
    ┌─────────────────────────────────────────────┐
    │  7. MANTENIMIENTO durante TODA              │
    │     la vida útil del edificio               │
    └─────────────────────────────────────────────┘
```

> **Claude:** Puntos que el profe enfatiza:
>
> **Etapa 2 — Revisión independiente**: Es uno de los hitos más importantes del proceso. Si el revisor encuentra errores, el proyecto vuelve al ingeniero estructural para corrección. Esto puede retrasar todo el proyecto. Por eso es crucial hacer un buen trabajo la primera vez.
>
> **Etapa 4 — Permiso de construcción**: Sin permiso de la D.O.M. (Dirección de Obras Municipales), no se puede construir legalmente. La D.O.M. verifica que se cumplan las normas urbanísticas y que estén las revisiones al día.
>
> **Etapa 5 — Inspección**: La ITO (Inspección Técnica de Obra) es obligatoria para edificios de cierta envergadura. Verifica que la construcción se ejecute según los planos y especificaciones. Si encuentra desviaciones, puede detener la obra.
>
> **Etapa 7 — Mantenimiento**: Es la etapa que más se descuida en Chile. Un edificio bien diseñado y construido puede perder capacidad resistente si no se mantiene (corrosión de armaduras, daño por uso, modificaciones no autorizadas como demoler muros para ampliar departamentos — sí, pasa).

### 4.3 Documentos Legales Importantes

```
    ┌─────────────────────────────────────────────────────────┐
    │              MARCO LEGAL                                │
    │                                                         │
    │  ┌──────────────────────────────────────────┐           │
    │  │  Ley General de Urbanismo y              │           │
    │  │  Construcciones (LGUC)                   │           │
    │  └──────────────────┬───────────────────────┘           │
    │                     │ (ley marco, define principios)    │
    │  ┌──────────────────▼───────────────────────┐           │
    │  │  Ordenanza General de Urbanismo y        │           │
    │  │  Construcciones (O.G.U.C.)               │           │
    │  └──────────────────┬───────────────────────┘           │
    │                     │ (reglamento, define detalles)     │
    │  ┌──────────────────▼───────────────────────┐           │
    │  │  Ley 19.748                              │           │
    │  │  Establece OBLIGATORIEDAD de revisar     │           │
    │  │  el proyecto de cálculo estructural      │           │
    │  │  www.restructural.cl                     │           │
    │  └──────────────────────────────────────────┘           │
    │                                                         │
    └─────────────────────────────────────────────────────────┘
```

> **Claude:** La jerarquía legal es: LGUC (ley) → O.G.U.C. (reglamento) → Normas técnicas (NCh433, DS60, DS61, etc.). La LGUC define los grandes principios. La O.G.U.C. los operacionaliza. Las normas técnicas son las que usas día a día como ingeniero.
>
> La Ley 19.748 fue un cambio importante en Chile: antes de ella, no era obligatorio tener un revisor independiente. Después del 27F se reforzó aún más la regulación.

---

## 5. Resumen Visual Integrado

### 5.1 Fórmulas Clave

| Concepto | Fórmula | Significado |
|:---------|:--------|:------------|
| Riesgo sísmico | `R = P × V` | Peligro × Vulnerabilidad |
| Rigidez | `k = F / δ` | Fuerza / Desplazamiento |
| Ductilidad | `μ = δu / δy` | Desplaz. último / Desplaz. fluencia |
| Período | `T = 2π√(m/k)` | Depende de masa y rigidez |
| Ecuación de movimiento | `mü + cu̇ + ku = -müg` | Equilibrio dinámico |

### 5.2 Mapa de Relaciones: Riesgo → Diseño → Proyecto

```
    TERREMOTO (amenaza natural, inevitable)
         │
         ▼
    ┌─── PELIGRO SÍSMICO (P) ───┐
    │  · Magnitud                │
    │  · Distancia a falla       │
    │  · Tipo de suelo           │
    └────────────┬───────────────┘
                 │
                 │ ×
                 │
    ┌─── VULNERABILIDAD (V) ────┐
    │  · Localización            │
    │  · Proyecto                │──→ AQUÍ ACTÚA EL
    │  · Materiales              │    INGENIERO ESTRUCTURAL
    │  · Construcción            │
    │  · Mantenimiento           │
    └────────────┬───────────────┘
                 │
                 ▼
    ┌─── RIESGO SÍSMICO (R=P×V)─┐
    │                            │
    │  ¿Cómo minimizarlo?        │
    └────────────┬───────────────┘
                 │
         ┌───────┼───────┐
         │       │       │
         ▼       ▼       ▼
    ┌────────┐┌────────┐┌────────┐
    │Diseño  ││Aislac. ││Disipac.│
    │Conven- ││Sísmica ││Energía │
    │cional  ││        ││        │
    │        ││Modif.  ││Modif.  │
    │Modif.  ││k (↓)   ││c (↑)   │
    │k,μ     ││T (↑)   ││        │
    └───┬────┘└───┬────┘└───┬────┘
        │         │         │
        └─────────┼─────────┘
                  │
                  ▼
         PROYECTO DE EDIFICIO
         (7 etapas hasta mantención)
```

### 5.3 Lo que DEBE Saber el Ingeniero Estructural

```
    ┌─────────────────────────────────────────────────────┐
    │  CHECKLIST del Ingeniero Estructural                │
    │                                                     │
    │  □ Evaluar el peligro sísmico de la zona           │
    │  □ Reducir la vulnerabilidad del diseño            │
    │  □ Elegir estrategia: convencional / aislación /   │
    │    disipación                                      │
    │  □ Garantizar RIGIDEZ adecuada (controlar δ)       │
    │  □ Garantizar DUCTILIDAD (μ alto, falla dúctil)    │
    │  □ Maximizar disipación de ENERGÍA (lazos amplios) │
    │  □ Cumplir normativa vigente                       │
    │  □ Coordinar con arquitecto e instalaciones        │
    │  □ Pasar revisión independiente (Ley 19.748)       │
    │  □ Supervisar construcción                         │
    └─────────────────────────────────────────────────────┘
```

> **Claude:** Si llegas al control y te preguntan algo abierto tipo "¿cuál es la responsabilidad del ingeniero estructural en un proyecto de edificio?", esta checklist es tu respuesta. Cubre desde la concepción (evaluar peligro, elegir estrategia) hasta la construcción (supervisar). El ingeniero no termina su trabajo cuando entrega los planos — su responsabilidad se extiende hasta que el edificio está construido correctamente.
