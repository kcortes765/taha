# PROMPT DE INVESTIGACIÓN — Modelación Edificio 1 en ETABS v19

> **INSTRUCCIÓN PARA LA IA**: Este documento es un prompt de investigación autocontenido.
> Tu tarea es investigar, verificar, complementar y mejorar la guía adjunta
> "GUIA-COMPLETA-EDIFICIO1-ETABS-v19.md" para que un estudiante pueda seguirla
> sin ningún error en ETABS v19. Lee TODO este documento antes de actuar.

---

## CONTEXTO DEL PROYECTO

### Qué es esto
Taller semestral de **Análisis y Diseño Sísmico de Edificios** (ADSE), UCN Chile, 1S-2026.
Profesor: Juan Music Tomicic. Software: ETABS v19 (CSI).

### Qué se necesita
Una guía paso a paso **perfecta** para modelar el Edificio 1 (20 pisos, muros HA) en ETABS v19 usando la **interfaz gráfica** (NO API/COM). El estudiante debe poder abrir ETABS, seguir la guía, y obtener todos los resultados sin errores ni ambigüedades.

### Qué ya existe
Se generó una guía de ~1500 líneas (GUIA-COMPLETA-EDIFICIO1-ETABS-v19.md) basada en:
- Enunciado del taller (14 págs)
- Material Apoyo Taller 2026 del profesor (47 págs)
- Paso a Paso ETABS de Lafontaine (143 págs)
- Manual ETABS v19 (239 págs)

### Qué falta
La guía fue generada por IA sin acceso directo a ETABS. **Necesita verificación y complemento** en los puntos que se detallan abajo.

---

## DATOS COMPLETOS DEL EDIFICIO 1

### Geometría
- 20 pisos hormigón armado, empotrado en base
- Piso 1: h=3.40m, pisos 2-20: h=2.60m → Htotal=52.80m
- Grilla irregular: 17 ejes X + 6 ejes Y
- Antofagasta, Zona 3, Suelo tipo C, Oficina (Categoría II)

### Coordenadas exactas de ejes

**Ejes X:**
```
Eje 1:  x = 0.000 m
Eje 2:  x = 3.125 m  (Δ = 3.125)
Eje 3:  x = 3.825 m  (Δ = 0.700)
Eje 4:  x = 9.295 m  (Δ = 5.470)
Eje 5:  x = 9.895 m  (Δ = 0.600)
Eje 6:  x = 15.465 m (Δ = 5.570)
Eje 7:  x = 16.015 m (Δ = 0.550)
Eje 8:  x = 18.565 m (Δ = 2.550)
Eje 9:  x = 18.990 m (Δ = 0.425)
Eje 10: x = 21.665 m (Δ = 2.675)
Eje 11: x = 24.990 m (Δ = 3.325)
Eje 12: x = 26.315 m (Δ = 1.325)
Eje 13: x = 27.834 m (Δ = 1.519)
Eje 14: x = 32.435 m (Δ = 4.601)
Eje 15: x = 34.005 m (Δ = 1.570)
Eje 16: x = 37.130 m (Δ = 3.125)
Eje 17: x = 38.505 m (Δ = 1.375)
```

**Ejes Y:**
```
Eje A: y = 0.000 m
Eje B: y = 0.701 m  (Δ = 0.701)
Eje C: y = 6.446 m  (Δ = 5.745)
Eje D: y = 7.996 m  (Δ = 1.550)
Eje E: y = 10.716 m (Δ = 2.720)
Eje F: y = 13.821 m (Δ = 3.105)
```

### Materiales
```
Hormigón G30:
  f'c = 30 MPa = 300 kgf/cm²
  Ec = 4700×√30 = 25,743 MPa
  γ = 2.5 tonf/m³
  ν = 0.2

Acero A630-420H:
  fy = 420 MPa = 4200 kgf/cm²
  fu = 630 MPa = 6300 kgf/cm²
  Es = 200,000 MPa
```

### Elementos estructurales
```
Muros dir Y e=30cm: ejes 1, 3, 4, 5, 7, 12, 13, 14, 16, 17
Muros dir Y e=20cm: ejes 2, 6, 8, 9, 10, 11, 15
Muros dir X e=30cm: eje C entre ejes 3-6 y 10-14
Muros dir X e=20cm: todos los demás en dir X
Vigas invertidas: 20×60 cm (todas iguales)
Losas: 15 cm espesor
Notación: MHA30G30, MHA20G30, VI20/60G30, Losa15G30
```

### Cargas
```
PP = peso propio (automático, SWM=1)
TERP = 140 kgf/m² = 0.140 tonf/m² (terminaciones piso tipo, pisos 1-19)
TERT = 100 kgf/m² = 0.100 tonf/m² (terminaciones techo, piso 20)
SCP = 250 kgf/m² = 0.250 tonf/m² (sobrecarga oficinas, pisos 1-19)
SCP_pasillos = 500 kgf/m² = 0.500 tonf/m² (si se diferencian zonas de pasillo)
SCT = 100 kgf/m² = 0.100 tonf/m² (sobrecarga techo, piso 20)
```

### Parámetros sísmicos NCh433 + DS61
```
Zona: 3, Ao = 0.4g = 3.924 m/s²
Suelo: C → S=1.05, To=0.40s, T'=0.45s, n=1.33, p=1.50
Categoría: II (oficina), I=1.0
Tipo estructura: Muros HA → R=7, Ro=11
```

### Shaft (ascensor)
```
Dimensiones: 7.7 m (dir X) × 2.945 m (dir Y)
Centrado en eje 10 (x=21.665)
Subdivisión: 4.25 m + 3.45 m en X
Hueco: entre ejes C y D (o más allá, ver preguntas abiertas)
```

---

## LO QUE PIDE EL TALLER — Parte 1, Edificio 1

### Entregables de la Parte 1

**1)** Descripción del edificio y su estructuración

**2)** Modelación del edificio en ETABS con diafragma rígido

**3) Determinar:**
- 3.1 Peso sísmico (tonf) y peso sísmico/m²
- 3.2 Densidad de muros en cada dirección (Ax/Aplanta, Ay/Aplanta)
- 3.3 Centro de masas y centro de rigidez en cada piso
- 3.4 Periodos Tx*, Ty*, Tz* + tabla modal completa + nº modos para ≥90% masa
- 3.5 Corte basal de diseño en cada dirección:
  - Tabla tipo pág 71 apuntes del profesor
  - Concluir corte basal y R* en cada dirección
  - Dibujar espectro elástico y de diseño para ambas direcciones
- 3.6 Corte y momento volcante por piso (tablas + gráficos, ambas direcciones)
- 3.7 Indicadores 1 y 13 del perfil biosísmico + comentarios

**4) Para 6 casos de análisis sísmico:**

| | Torsión caso a) | Torsión caso b) F1 | Torsión caso b) F2 |
|---|---|---|---|
| Diafragma rígido | Caso 1 | Caso 2 | Caso 3 |
| Diafragma semi-rígido | Caso 4 | Caso 5 | Caso 6 |

- 4.1 Verificación deformaciones (drift condición 1 ≤ 0.002 y condición 2 ≤ 0.001) con gráficos
- 4.2 Corte en muro eje 1 y muro eje F — tabla por pisos para los 6 casos
- 4.3 Cuadro resumen comparativo + conclusiones

---

## PRÁCTICAS CHILENAS OBLIGATORIAS EN ETABS

Estas son reglas que el profesor y la práctica profesional chilena exigen. **No son opcionales.**

| Práctica | Dónde aplicar | Valor |
|----------|---------------|-------|
| J=0 en vigas | Frame Section > Modifiers > Torsional Constant | 0 |
| Inercia losa 25% | Slab Section > Modifiers > m11=m22=m12 | 0.25 |
| Peso HA 2.5 tonf/m³ | Material > Weight per Unit Volume | 2.5 |
| Espectro desde archivo | Define > Functions > Response Spectrum > From File | .txt |
| NO usar espectro integrado NCh433 | El de ETABS está desactualizado | — |
| CQC para combinación modal | Load Case espectral | CQC |
| SRSS para combinación direccional | Load Case espectral | SRSS |
| Amortiguamiento 5% | Espectro y Modal Damping | 0.05 |
| Mass Source especificado | PP=1, TERP=1, SCP=0.25 | — |
| Peso/Área ≈ 1 tonf/m² | Validación post-análisis | ~1.0 |
| Mesh máximo 1×1 m (losas) | Floor Auto Mesh Options | 1.0 m |
| Relación aspecto muros 1≤L/h≤2 | Wall mesh | — |
| Auto Edge Constraint | Assign > Shell > Auto Edge Constraints | ON |
| Vigas invertidas: Insertion Point | Cardinal Point = Bottom Center | 8 |

---

## TORSIÓN ACCIDENTAL — Los 3 métodos

### Método a) — Desplazar centro de masa (±5%)

**Concepto**: Crear 4 Mass Sources adicionales con CM desplazado:
- Masa+X: CM desplazado +5% en X
- Masa-X: CM desplazado -5% en X
- Masa+Y: CM desplazado +5% en Y
- Masa-Y: CM desplazado -5% en Y

**Requiere**: 4 casos estáticos no-lineales auxiliares (sin carga), 4 casos modales independientes, 4 casos espectrales (SDX+Y, SDX-Y, SDY+X, SDY-X).

**En ETABS**:
- Define > Mass Source: "Adjust Diaphragm Lateral Mass to Move Mass Centroid by" ratio ±0.05
- Define > Load Cases: Nonlinear Static (auxiliar), Modal (Eigen con P-Delta del auxiliar), Response Spectrum (con modal correspondiente, Diaph Ecc=0)

**Combos**: 15 en total (3 gravitacionales + 6 sismo X + 6 sismo Y)

### Método b) Forma 1 — Momentos torsores estáticos

**Concepto**: Calcular fuerzas de corte por piso del análisis espectral, luego calcular momento torsor = ΔQ×e y aplicarlo como carga estática.

**Requiere**: Correr primero SDX/SDY sin torsión, extraer Story Shears, calcular Mz en Excel, crear Load Patterns TEX/TEY tipo Seismic con User Defined.

**Excentricidad**: Interpolación lineal de 10% en techo a 0% en base.
- Para sismo X: e = 0.10 × dim_Y × (N-k)/(N-1) donde N=20, k=piso
- Para sismo Y: e = 0.10 × dim_X × (N-k)/(N-1)
- dim_Y = 13.821 m, dim_X = 38.505 m

**En ETABS**:
- Define > Load Patterns: TEX tipo Seismic, SWM=0, Auto Lateral Load = User Defined
- Modify Lateral Load: Apply at CM, Fx=0, Fy=0, Mz=valor por piso

**Combos**: 11 en total

### Método b) Forma 2 — Excentricidad por piso en el caso espectral

**Concepto**: Ingresar directamente la excentricidad neta (en metros) por piso en el caso espectral.

**En ETABS**:
- Define > Load Cases > (caso espectral) > Diaphragm Eccentricity > Modify/Show
- Eccentricity Ratio = 0, luego llenar columna "Eccentricity (m)" por piso
- ETABS aplica ±e internamente

**Combos**: 7 en total (más simple)

---

## COMBINACIONES DE CARGA NCh3171

### Estados de carga según NCh3171:2017
```
C1: 1.4D
C2: 1.2D + 1.6L + 0.5Lr
C3: 1.2D + L + 1.6Lr
C4: 1.2D + L ± 1.4Ex
C5: 0.9D ± 1.4Ex
C6: 1.2D + L ± 1.4Ey
C7: 0.9D ± 1.4Ey
```

Donde D = PP + TERP (o TERT en techo), L = SCP, Lr = SCT, E = sismo.

### Nota sobre ETABS y signos ±
ETABS genera automáticamente las permutaciones ± cuando hay un caso espectral CQC (8 sub-combinaciones internas: ±P, ±V2, ±V3, ±T, ±M2, ±M3). Por eso un combo "1.2D + L + 1.4×SDX" ya cubre tanto +SDX como -SDX.

---

## EXTRACCIÓN DE RESULTADOS — Rutas exactas

| Resultado | Ruta en ETABS v19 |
|-----------|-------------------|
| Periodos + masas | Display > Show Tables > Modal Participating Mass Ratios |
| Peso por piso | Display > Show Tables > Mass Summary by Story |
| CM y CR | Display > Show Tables > Centers of Mass and Rigidity |
| Drift CM (cond 1) | Display > Show Tables > Joint Drifts (filtrar nodo CM) |
| Drift máximo (cond 2) | Display > Show Tables > Diaphragm Max Over Avg Drifts |
| Corte por piso | Display > Story Response Plots > Story Shears |
| Momento volcante | Display > Story Response Plots > Story Overturning Moments |
| Corte en muros | Display > Show Tables > Pier Forces (filtrar por Pier label) |
| Base Reactions | Display > Show Tables > Base Reactions |
| Deformada modal | Display > Deformed Shape (F6) > caso Modal |

---

## PREGUNTAS ABIERTAS — INVESTIGAR

Las siguientes preguntas NO están resueltas en la guía. **Necesitan investigación:**

### P1: Geometría exacta de muros desde los planos
La guía tiene la grilla y las reglas de espesor, pero NO tiene la lista muro por muro con coordenadas inicio/fin extraída de los planos (págs 2-7 del enunciado). **Se necesita:**
- Lista de CADA muro con: eje, coord inicio, coord fin, dirección (X/Y), espesor, largo
- Verificar contra las elevaciones (págs 6-7) que los muros son correctos
- Especialmente los muros del eje C (que tienen aberturas/huecos) y del shaft

### P2: Shaft — geometría exacta
- El shaft mide 7.7m × 2.945m centrado en eje 10
- ¿Los 2.945m son en dirección Y?
- ¿Las paredes del shaft van de eje C a más allá de eje D?
- ¿Dónde exactamente están las paredes verticales del shaft? ¿En ejes 10/11 o en coordenadas off-grid?
- Los bordes calculados del shaft serían: x = 21.665 - 4.25 = 17.415 y x = 21.665 + 3.45 = 25.115 (ambos off-grid)

### P3: Zonas de pasillo
- El enunciado dice 500 kgf/m² en pasillos pero no identifica cuáles son
- ¿Usar 250 kgf/m² para todo? ¿O identificar pasillos desde la planta?
- Afecta la masa sísmica (aunque solo al 25%)

### P4: Scale Factor del espectro
- Si el espectro .txt tiene valores en m/s² → SF=1 en ETABS
- Si el espectro .txt tiene valores adimensionales (Sa/g) → SF=9.81
- **¿Cuál es la práctica estándar en Chile?** Verificar con el formato del archivo

### P5: Techo diferente al piso tipo
- Pág 4 del enunciado muestra planta del techo con MENOS muros
- ¿Cuáles muros faltan en el techo? Detallar diferencias

### P6: Vigas — ubicación exacta
- Las vigas aparecen etiquetadas "VI20/60" en la planta pág 2
- Necesito la lista COMPLETA de vigas: eje, entre qué ejes, dirección

### P7: Losas — paneles exactos
- ¿Cuántos paneles de losa hay por piso tipo?
- ¿Cuáles son sus vértices?
- ¿Dónde está el hueco del shaft exactamente?

### P8: Interpolación de excentricidad accidental
- NCh433 art. 6.3.4: ¿la interpolación es lineal de 10% en techo a 0% en base?
- ¿O es 10% en todos los pisos? Verificar texto exacto de la norma
- El Material Apoyo del profesor dice "10% en el techo, 0% en la base, interpolación lineal"

### P9: Espectro de diseño vs elástico
- ¿ETABS debe tener el espectro elástico y el factor I/R* se aplica en las combinaciones?
- ¿O se carga directamente el espectro de diseño (ya reducido por R*)?
- Lafontaine recomienda cargar elástico y reducir en combos (permite cambiar R* sin re-correr)

### P10: P-Delta
- ¿Se debe considerar efecto P-Delta?
- Si sí: ¿qué opción en ETABS? (Preset P-Delta en Load Case, Iterative Based on Mass?)
- El enunciado no lo menciona explícitamente

### P11: Tabla "página 71 apuntes del profesor"
- El entregable 3.5 dice "elaborar tabla página 71 apuntes del profesor"
- Esta tabla muestra: T*, R*, Qmin, Qmax, Qdiseño, C, Cmin, Cmax para cada dirección
- ¿Cuál es el formato exacto? Investigar en los apuntes

### P12: Nombres exactos de tablas en ETABS v19
- ¿"Joint Drifts" se llama exactamente así en v19? ¿O es "Story Drifts"?
- ¿"Diaphragm Max Over Avg Drifts" existe en v19? ¿O es otra tabla?
- ¿"Pier Forces" o "Pier Design Forces"? ¿Cuál tiene V2, M3?
- Verificar nombres exactos en ETABS v19

---

## TU TAREA COMO IA INVESTIGADORA

### Fase 1: Verificar la guía existente
1. Lee GUIA-COMPLETA-EDIFICIO1-ETABS-v19.md completa
2. Identifica errores, inconsistencias o ambigüedades
3. Verifica que las rutas de menú sean correctas para ETABS v19
4. Verifica que los valores numéricos sean correctos (conversiones de unidades, fórmulas)

### Fase 2: Resolver las preguntas abiertas (P1-P12)
Investiga cada pregunta usando:
- Documentación CSI oficial
- Foros de ingeniería (CSI Knowledge Base, eng-tips.com, civilgeeks.com)
- Videos de YouTube sobre ETABS v19
- NCh433:2009, DS61, NCh3171:2017 (textos normativos)
- Cualquier fuente confiable

### Fase 3: Complementar la guía con
1. **Lista muro por muro** (P1) — si puedes interpretar los planos
2. **Tabla de espectro completa** — valores T vs Sa para ΔT=0.05s desde T=0 hasta T=5.0s
3. **Tabla de excentricidad por piso** — valores calculados para los 20 pisos
4. **Tabla de momentos torsores por piso** — para método b) forma 1 (necesita cortes de ETABS, pero puedes estimar valores)
5. **Formato exacto de la tabla pág 71** del profesor
6. **Fórmulas del espectro** con valores numéricos reemplazados
7. **Cualquier paso que falte** en la guía

### Fase 4: Mejorar la guía
1. Agregar pasos que falten
2. Corregir errores
3. Agregar advertencias y tips basados en tu investigación
4. Mejorar la claridad donde sea ambiguo
5. Agregar screenshots o diagramas ASCII si ayudan

### Formato de entrega
Entrega un documento con:
```
## CORRECCIONES A LA GUÍA
(lista de errores encontrados y cómo corregirlos)

## PREGUNTAS RESUELTAS
(respuesta a cada pregunta P1-P12 con fuentes)

## COMPLEMENTOS
(tablas, listas, fórmulas adicionales)

## GUÍA MEJORADA
(secciones re-escritas o nuevas)
```

---

## REFERENCIAS DISPONIBLES

Si tienes acceso a buscar en la web, estas son fuentes clave:
- CSI Knowledge Base: wiki.csiamerica.com
- CSI YouTube: youtube.com/@caboratoryCSI
- Foro eng-tips.com (sección ETABS)
- civilgeeks.com (recursos en español)
- NCh433:1996 Mod.2009 — norma sísmica chilena
- DS61 — decreto suplementario diseño sísmico
- DS60 — decreto hormigón armado
- NCh3171:2017 — estados de carga
- ACI 318-08 — código de concreto

---

## VALORES DE REFERENCIA ESPERADOS

Para validar resultados:
```
Peso sísmico total: ~9,000-10,000 tonf
Peso/Área: ~1.0 tonf/m²
Tx*: ~1.0-1.3 s (dir X, más larga porque planta es más larga en X)
Ty*: ~0.8-1.2 s (dir Y, más corta)
Tz*: ~0.5-0.8 s (rotacional)
Drift CM máximo: < 0.002 (debe cumplir)
Corte basal mínimo (Qmín): ~0.07 × P ≈ 650 tonf
R*: probablemente < 7 (se usará Cmáx en alguna dirección)
Indicador 1 (H/T*): ~40-53 m/s (rango típico edificios muros)
```

---

## NOTAS FINALES

- La interfaz de ETABS v19 está en **inglés**
- Las unidades se cambian dinámicamente en la esquina inferior derecha
- Los archivos de espectro (.txt) deben tener el separador decimal correcto para la configuración regional del PC
- **NO usar la opción Fix de Check Model** — corregir manualmente
- **NO usar el espectro NCh433 integrado en ETABS** — está desactualizado
- Guardar el modelo frecuentemente (File > Save, Ctrl+S)
- Para los 6 casos: correr primero con diafragma rígido (casos 1-3), guardar, luego cambiar a semi-rígido y re-correr (casos 4-6)
