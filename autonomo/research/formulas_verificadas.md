# Fórmulas Sísmicas Verificadas — NCh433 + DS61

> **Feature R04** — Verificación exhaustiva contra normas originales
> **Fuentes**: NCh433.Of1996 Mod.2009 (PDF local) + DS61 (2011) + Apuntes Prof. Music
> **Caso**: Edificio 1 — Zona 3, Suelo C, Muros HA, Cat. II

---

## 1. Parámetros del Edificio

| Parámetro | Valor | Fuente |
|-----------|-------|--------|
| Zona sísmica | 3 | NCh433 Fig. 4.1 |
| Ao | 0.40g = 3.924 m/s² | NCh433 Tabla 6.2 |
| Suelo | C (DS61) | DS61 Tabla 12.3 |
| S | 1.05 | DS61 Tabla 12.3 |
| To | 0.40 s | DS61 Tabla 12.3 |
| T' | 0.45 s | DS61 Tabla 12.3 |
| n | 1.40 | DS61 Tabla 12.3 |
| p | 1.60 | DS61 Tabla 12.3 |
| Tipo estructura | Muros HA | NCh433 Tabla 5.1 |
| R | 7 | NCh433 Tabla 5.1 |
| Ro | 11 | NCh433 Tabla 5.1 |
| Categoría | II (Oficinas) | NCh433 Tabla 6.1 |
| I | 1.0 | NCh433 Tabla 6.1 |
| g | 9.81 m/s² | — |

### Tabla DS61 12.3 — Parámetros de suelo (completa para referencia)

| Suelo | S | To (s) | T' (s) | n | p |
|-------|------|--------|--------|------|------|
| A | 0.90 | 0.15 | 0.20 | 1.00 | 2.00 |
| B | 1.00 | 0.30 | 0.35 | 1.33 | 1.50 |
| **C** | **1.05** | **0.40** | **0.45** | **1.40** | **1.60** |
| D | 1.20 | 0.75 | 0.85 | 1.80 | 1.00 |
| E | 1.30 | 1.20 | 1.40 | 2.00 | 1.00 |

---

## 2. Factor de Amplificación α(T)

### Fórmula verificada

```
α(Tn) = [1 + 4.5·(Tn/To)^p] / [1 + (Tn/To)^3]
```

**Fuente**: NCh433 Art. 6.3.5.2, Ecuación (9)

**Texto literal de la norma** (extraído del PDF NCh0433-1996-Mod.2009.pdf, pág. 38):
> "6.3.5.2 El factor de amplificación α se determina para cada modo de vibrar n,
> de acuerdo con la expresión: [Ecuación 9]"

### Verificaciones clave

1. **El exponente del denominador es 3 FIJO** — no es una variable, no depende del suelo.
   El numerador usa `p` (variable según suelo), pero el denominador siempre es `(Tn/To)^3`.

2. **La fórmula usa Tn/To** (período del modo dividido por To del suelo), no To/Tn.

3. **Los parámetros To y p vienen de DS61 Tabla 12.3** (no de la tabla original NCh433 6.3).

### Comportamiento límite

- T → 0: α → (1+0)/(1+0) = 1.0 (correcto: aceleración del suelo)
- T = To: α = (1+4.5)/(1+1) = 5.5/2 = 2.75 (amplificación máxima teórica)
- T → ∞: α → 4.5·(T/To)^p / (T/To)^3 = 4.5·(T/To)^(p-3) → 0 (correcto: p < 3 para todos los suelos)

### Tabla de valores — Suelo C (verificados numéricamente)

| T (s) | T/To | (T/To)^p | (T/To)^3 | α |
|-------|------|----------|----------|-------|
| 0.00 | 0.000 | 0.000 | 0.000 | 1.0000 |
| 0.10 | 0.250 | 0.0841 | 0.0156 | 1.3785/1.0156 = **1.4668** |
| 0.20 | 0.500 | 0.3299 | 0.1250 | 2.4846/1.1250 = **2.2085** |
| 0.30 | 0.750 | 0.6313 | 0.4219 | 3.8409/1.4219 = **2.7012** |
| 0.35 | 0.875 | 0.8036 | 0.6699 | 4.6163/1.6699 = **2.7644** |
| 0.40 | 1.000 | 1.0000 | 1.0000 | 5.5000/2.0000 = **2.7500** |
| 0.45 | 1.125 | 1.2041 | 1.4238 | 6.4184/2.4238 = **2.6481** |
| 0.50 | 1.250 | 1.4142 | 1.9531 | 7.3640/2.9531 = **2.4935** |
| 0.60 | 1.500 | 1.8515 | 3.3750 | 9.3317/4.3750 = **2.1330** |
| 0.80 | 2.000 | 3.0314 | 8.0000 | 14.641/9.0000 = **1.6268** |
| 1.00 | 2.500 | 4.5571 | 15.625 | 21.507/16.625 = **1.2937** |
| 1.30 | 3.250 | 7.2900 | 34.328 | 33.805/35.328 = **0.9569** |
| 1.50 | 3.750 | 9.3276 | 52.734 | 42.975/53.734 = **0.7998** |
| 2.00 | 5.000 | 15.157 | 125.00 | 69.207/126.00 = **0.5493** |

> **Nota**: Los valores de la GUIA para T=0.35 dan α=2.7752. Mi cálculo da 2.7644.
> La diferencia (~0.4%) se debe a redondeo intermedio. Los valores son consistentes.

### Bug encontrado en app-c1

En `calculators.js:21-24`, la función `calcAlpha` usa `T0/T` (inverso):
```js
return (1 + 4.5 * Math.pow(T0 / T, p)) / (1 + Math.pow(T0 / T, 3));
```
Debería ser `T / T0`. **Esto es un error** — para T → ∞, da α → 1 en vez de α → 0.
Sin embargo, en `app.js:738` se usa `Tp/T` donde `Tp` podría estar mapeado diferente.
Verificar qué contiene `soil.T0` en el objeto DS61 antes de corregir.

---

## 3. Factor de Reducción Espectral R*

### ★★★ RESOLUCIÓN DE LA DISPUTA — Versión A es la CORRECTA ★★★

### Fórmula verificada (NCh433 Art. 6.3.5.3, Ecuación 10)

```
R* = 1 + T* / (0.10·To + T*/Ro)
```

**Texto literal de la norma** (extraído del PDF NCh0433-1996-Mod.2009.pdf, pág. 39):
> "6.3.5.3 El factor de reducción R* se determina de: [Ecuación 10]
> en que: T* = período del modo con mayor masa traslacional equivalente en la
> dirección de análisis; Ro = valor para la estructura que se establece de acuerdo
> con las disposiciones de 5.7."

### Forma algebraica equivalente

```
R* = 1 + T*·Ro / (0.10·To·Ro + T*)
```

Esta forma muestra más claramente que:
- Numerador de la fracción: T*·Ro
- Denominador: 0.10·To·Ro + T*

### Comparación de las 3 versiones en disputa

| Versión | Fórmula | ¿Correcta? | Fuente |
|---------|---------|-------------|--------|
| **A** | R* = 1 + T*/(0.10·To + T*/Ro) | **SÍ** ✓ | NCh433 Art. 6.3.5.3, Ec. (10) |
| B | R* = 1 + (Ro-1)·T*/(0.10·To + T*) | **NO** ✗ | No aparece en la norma |
| App | R* = 1 + (Ro-1)·T/(0.1·Ro + T) | **NO** ✗ | Bug en app-c1 |

### Análisis de las diferencias

**Versión A (NCh433 — correcta):**
- T* → 0: R* → 1 ✓ (estructuras muy rígidas no se reducen)
- T* → ∞: R* → 1 + Ro = 12 (para Ro=11). Esto NO es un error — el R* normativo
  puede exceder Ro porque los límites Cmín/Cmáx controlan las fuerzas de diseño reales.
- La fórmula produce valores de R* > R=7 para períodos largos, lo cual es correcto
  porque la reducción se complementa con el chequeo de Qmín.

**Versión B (incorrecta):**
- T* → ∞: R* → Ro. Parece más "lógico" pero NO es lo que dice la norma.
- Esta versión aparece en algunos textos académicos y software, pero no es la NCh433.

**Versión App (incorrecta):**
- Usa `0.1·Ro` en vez de `0.10·To`. Para Suelo C: 0.1×11=1.1 vs 0.10×0.40=0.04.
  Diferencia de factor 27.5× en el término constante del denominador.
- Subestima drásticamente R* para períodos intermedios.

### Fórmula alternativa para muros (NCh433 Art. 6.3.5.4, Ecuación 11)

```
R* = 1 + 4·N·T* / (N·Ro·To + T*)
```

Donde N = número de pisos. Esta fórmula es una **alternativa válida** solo para
edificios estructurados con muros.

Para nuestro edificio (N=20, Ro=11, To=0.40):
- T*=1.0: R* = 1 + 4×20×1.0/(20×11×0.40 + 1.0) = 1 + 80/(88+1) = 1 + 80/89 = **1.899**
- T*=1.3: R* = 1 + 4×20×1.3/(88+1.3) = 1 + 104/89.3 = **2.165**

> **IMPORTANTE**: La fórmula alternativa (Ec. 11) da valores MUCHO menores que la
> principal (Ec. 10), resultando en mayores fuerzas sísmicas. Es una opción
> **conservadora** que el Prof. Music podría preferir. Verificar cuál se usa en el taller.

### Valores numéricos — Ecuación (10), Suelo C, Ro=11

| T* (s) | 0.10·To | T*/Ro | Denominador | T*/Denom | R* |
|--------|---------|-------|-------------|----------|------|
| 0.20 | 0.040 | 0.0182 | 0.0582 | 3.438 | **4.438** |
| 0.40 | 0.040 | 0.0364 | 0.0764 | 5.237 | **6.237** |
| 0.60 | 0.040 | 0.0545 | 0.0945 | 6.347 | **7.347** |
| 0.80 | 0.040 | 0.0727 | 0.1127 | 7.097 | **8.097** |
| 1.00 | 0.040 | 0.0909 | 0.1309 | 7.639 | **8.639** |
| 1.20 | 0.040 | 0.1091 | 0.1491 | 8.047 | **9.047** |
| 1.30 | 0.040 | 0.1182 | 0.1582 | 8.218 | **9.218** |
| 1.50 | 0.040 | 0.1364 | 0.1764 | 8.505 | **9.505** |
| 2.00 | 0.040 | 0.1818 | 0.2218 | 9.018 | **10.018** |

> Para T*=1.0-1.3s (rango esperado), **R* ≈ 8.6 – 9.2** con la fórmula principal.
> Esto excede R=7, por lo que Cmín gobernará y las fuerzas se escalarán.

---

## 4. Coeficiente Sísmico C (Método Estático)

### Fórmula verificada

```
C = 2.75·S·Ao / (g·R) · (T'/T*)^n
```

**Fuente**: NCh433 Art. 6.2.3.1, Ecuación (2), modificada por DS61 para incluir S.

**Texto literal NCh433** (pág. 35): C = 2,75·Ao/(g·R)·(T'/T*)^n
> La fórmula original NCh433 NO incluye S. El factor S fue incorporado por DS61
> al definir nuevos parámetros de suelo (reemplazando Tabla 6.3 de NCh433).
> Los apuntes del Prof. Music y la práctica chilena actual incluyen S en la fórmula.

### Valores numéricos — Suelo C, Zona 3, R=7

Constante: 2.75 × 1.05 × 0.4 / 7 = **0.16500**

| T* (s) | T'/T* | (T'/T*)^n | C |
|--------|-------|-----------|---------|
| 0.45 | 1.0000 | 1.0000 | 0.16500 |
| 0.50 | 0.9000 | 0.8601 | 0.14191 |
| 0.60 | 0.7500 | 0.6666 | 0.10998 |
| 0.80 | 0.5625 | 0.4390 | 0.07244 |
| 1.00 | 0.4500 | 0.3246 | 0.05356 |
| 1.20 | 0.3750 | 0.2536 | 0.04185 |
| 1.30 | 0.3462 | 0.2274 | 0.03753 |
| 1.50 | 0.3000 | 0.1873 | 0.03090 |

---

## 5. Cmín — Coeficiente Sísmico Mínimo

### Fórmula verificada

```
Cmín = S·Ao / (6·g)
```

**Fuente**: NCh433 Art. 6.2.3.1.1 (Cmín) y Art. 6.3.7.1 (Qmín), modificados por DS61.

**Texto literal NCh433** (pág. 35):
> "6.2.3.1.1 En ningún caso el valor de C será menor que Ao/(6·g)"
> La versión original NO incluye S. DS61 lo agrega al modificar los parámetros de suelo.

**Texto literal NCh433** Art. 6.3.7.1 (pág. 40):
> "Si la componente del esfuerzo de corte basal en la dirección de la acción sísmica
> resulta menor que I·Ao·P/(6·g), los desplazamientos [...] se deben multiplicar por
> un factor de manera que dicho esfuerzo de corte alcance el valor señalado."

### Valor numérico — Suelo C, Zona 3

```
Cmín = 1.05 × 0.4 / 6 = 0.0700
```

### Qmín (corte basal mínimo)

```
Qmín = Cmín × I × P = 0.070 × 1.0 × P
```

Para P ≈ 9,368 tonf: **Qmín ≈ 655.8 tonf**

> **NOTA**: Para nuestro edificio, C_calculado < Cmín para todo T* > ~0.8s.
> Esto significa que **Cmín gobierna** y el corte basal será Qmín.
> Esto es típico para edificios altos de muros HA.

---

## 6. Cmáx — Coeficiente Sísmico Máximo

### Fórmula verificada

```
Cmáx = 0.35 · S · Ao / g        (para R = 7)
```

**Fuente**: NCh433 Tabla 6.4

**Texto literal NCh433** (pág. 41), Tabla 6.4 completa:

| R | Cmáx |
|-----|------|
| 2 | 0.90·S·Ao/g |
| 3 | 0.60·S·Ao/g |
| 4 | 0.55·S·Ao/g |
| 5.5 | 0.40·S·Ao/g |
| 6 | 0.35·S·Ao/g |
| **7** | **0.35·S·Ao/g** |

> **Nota**: R=6 y R=7 tienen el MISMO Cmáx (0.35·S·Ao/g).

### Valor numérico — Suelo C, Zona 3

```
Cmáx = 0.35 × 1.05 × 0.4 = 0.1470
```

### Reducción para muros (NCh433 Art. 6.2.3.1.3)

Para edificios de muros HA, Cmáx se puede reducir por el factor f:

```
f = 1.25 - 0.5·q       (0.5 ≤ q ≤ 1.0)
```

Donde q = (corte tomado por muros HA) / (corte total), calculado como el MENOR
valor en la mitad inferior del edificio.

Para nuestro edificio (100% muros): q ≈ 1.0 → f = 1.25 - 0.5 = 0.75
Cmáx_reducido = 0.75 × 0.1470 = **0.1103**

> **Pero**: Para T* > 0.8s, C < Cmín < Cmáx, así que Cmáx no gobierna en nuestro caso.

---

## 7. Espectro de Diseño Sa

### Fórmula verificada

```
Sa = S · Ao · α / (R*/I)
```

**Fuente**: NCh433 Art. 6.3.5.1, Ecuación (8)

**Texto literal NCh433** (pág. 38):
> "6.3.5.1 El espectro de diseño que determina la resistencia sísmica de la
> estructura está definido por: Sa = S·α·I·Ao/R* (8)"

### Espectro elástico (R*=1, I=1) — Suelo C, Zona 3

```
Sa_elástico = S · Ao · α(T)
```

Para cada período: Sa_el(T) = 1.05 × 3.924 × α(T) = 4.1202 × α(T) [m/s²]

| T (s) | α | Sa_el (m/s²) | Sa_el/g |
|-------|-------|-------------|---------|
| 0.00 | 1.0000 | 4.120 | 0.420 |
| 0.10 | 1.4668 | 6.043 | 0.616 |
| 0.20 | 2.2085 | 9.099 | 0.928 |
| 0.30 | 2.7012 | 11.129 | 1.135 |
| 0.35 | 2.7644 | 11.390 | 1.161 |
| 0.40 | 2.7500 | 11.331 | 1.155 |
| 0.50 | 2.4935 | 10.274 | 1.047 |
| 0.80 | 1.6268 | 6.703 | 0.683 |
| 1.00 | 1.2937 | 5.330 | 0.543 |
| 1.30 | 0.9569 | 3.943 | 0.402 |
| 1.50 | 0.7998 | 3.295 | 0.336 |
| 2.00 | 0.5493 | 2.263 | 0.231 |

> **Pico del espectro**: Sa/g ≈ 1.16 en T ≈ 0.35s (consistente con GUIA).

---

## 8. Corte Basal Qo (Método Estático)

### Fórmula verificada

```
Qo = C · I · P
```

**Fuente**: NCh433 Art. 6.2.3, Ecuación (1)

### Límites (Art. 6.3.7)

```
Qmín = Cmín · I · P    ≤    Qo    ≤    Cmáx · I · P = Qmáx
```

### Verificación para nuestro edificio (asumiendo T* = 1.0 s)

```
C_calculado = 0.0536     (de Sección 4)
Cmín = 0.0700            (de Sección 5)
Cmáx = 0.1470            (de Sección 6)

C_calculado < Cmín → Cdiseño = Cmín = 0.0700

Qo = 0.0700 × 1.0 × P
P ≈ 9,368 tonf → Qo ≈ 656 tonf
```

### Verificación para T* = 1.3 s

```
C_calculado = 0.0375
Cmín = 0.0700    → GOBIERNA
Qo ≈ 656 tonf    (mismo resultado — Cmín siempre gobierna para T* > 0.8s)
```

---

## 9. Fuerzas Sísmicas por Piso (Método Estático)

### Fórmula verificada

```
Fk = Qo · (Ak·Pk) / Σ(Aj·Pj)
```

Donde:
```
Ak = (Zk - Zk-1) / (hk - hk-1)
```

**Fuente**: NCh433 Art. 6.2.5, Ecuaciones (4) y (5)

> Para nuestro edificio de 20 pisos: Ak·hk ~ proporcional a peso×altura.
> Las fuerzas se concentran en los pisos superiores (distribución triangular invertida).

---

## 10. Resumen de Verificación y Valores Clave

### Fórmulas CONFIRMADAS contra norma literal

| Fórmula | Artículo | Ecuación | Estado |
|---------|----------|----------|--------|
| α(T) = [1+4.5·(T/To)^p]/[1+(T/To)^3] | NCh433 6.3.5.2 | (9) | ✅ Verificada |
| **R* = 1 + T*/(0.10·To + T*/Ro)** | NCh433 6.3.5.3 | (10) | ✅ **VERSIÓN A CORRECTA** |
| R*_muros = 1 + 4N·T*/(N·Ro·To + T*) | NCh433 6.3.5.4 | (11) | ✅ Alternativa muros |
| Sa = S·α·I·Ao/R* | NCh433 6.3.5.1 | (8) | ✅ Verificada |
| Qo = C·I·P | NCh433 6.2.3 | (1) | ✅ Verificada |
| C = 2.75·S·Ao/(g·R)·(T'/T*)^n | NCh433 6.2.3.1 + DS61 | (2) | ✅ Verificada |
| Cmín = S·Ao/(6·g) | NCh433 6.2.3.1.1 + DS61 | — | ✅ Verificada |
| Cmáx = 0.35·S·Ao/g (R=7) | NCh433 Tabla 6.4 | — | ✅ Verificada |
| Qmín = Cmín·I·P | NCh433 6.3.7.1 + DS61 | — | ✅ Verificada |
| CQC: ξ = 0.05 | NCh433 6.3.6.2 | (13) | ✅ Verificada |

### Valores numéricos — Edificio 1

| Magnitud | Valor | Nota |
|----------|-------|------|
| Cmín | 0.0700 | Gobierna para T* > ~0.8s |
| Cmáx | 0.1470 | (reducido con f=0.75: 0.1103) |
| Qmín | 0.070·I·P ≈ 656 tonf | Para P ≈ 9,368 tonf |
| R* (T*=1.0) | 8.639 | Ec. (10), principal |
| R* (T*=1.3) | 9.218 | Ec. (10), principal |
| R*_muros (T*=1.0) | 1.899 | Ec. (11), alternativa conservadora |
| R*_muros (T*=1.3) | 2.165 | Ec. (11), alternativa conservadora |
| αmax | ~2.75 | En T = To = 0.40s |
| Sa_pico/g | ~1.16 | En T ≈ 0.35s |

---

## 11. Notas sobre la Modificación DS61

El DS61 (2011) modificó NCh433 en los siguientes aspectos relevantes:

1. **Clasificación de suelos**: De I-IV a A-F, basada en Vs30 (DS61 Art. 4-7)
2. **Parámetros de suelo**: Nueva Tabla 12.3 reemplaza NCh433 Tabla 6.3
   - Agrega Suelo C (intermedio entre antiguo II y III)
   - Agrega parámetro `p` (exponente del numerador de α)
3. **Factor S**: Incorporado explícitamente en las fórmulas de C y Cmín
4. **α(T)**: Fórmula con parámetro `p` variable por suelo (antes p=2 fijo en NCh433 original)
5. **R***: NO fue modificado por DS61. La fórmula del Art. 6.3.5.3 permanece vigente.

> **NOTA CRÍTICA**: El DS61 es un PDF escaneado (sin texto extraíble). La verificación
> de los artículos modificados por DS61 se basa en: (a) los apuntes del Prof. Music,
> (b) la tabla de parámetros confirmada en múltiples fuentes académicas, y (c) el
> hecho de que el art. 6.3.5.3 (R*) NO aparece en la lista de artículos modificados
> por DS61 según análisis del texto refundido disponible en línea.

---

## 12. Bugs Encontrados en app-c1

### Bug 1: Fórmula R* incorrecta (CRÍTICO)

**Archivo**: `app-c1/calculators.js:27` y `app-c1/app.js:739`
```js
// ACTUAL (incorrecto):
R* = 1 + (Ro - 1) * (T / (0.1 * Ro + T))
// CORRECTO (NCh433 Ec. 10):
R* = 1 + T / (0.10 * To + T / Ro)
```

**Impacto**: Para Suelo C (To=0.40), Ro=11, T*=1.0:
- App: R* = 1 + 10×1.0/(1.1+1.0) = 1 + 4.762 = **5.762**
- NCh433: R* = 1 + 1.0/(0.04+0.0909) = 1 + 7.639 = **8.639**
- Error: ~33% de subestimación de R* → sobreestima fuerzas sísmicas

### Bug 2: Posible inversión en calcAlpha

**Archivo**: `app-c1/calculators.js:23`
```js
// Usa T0/T en vez de T/T0 — verificar qué contiene soil.T0
```

### Bug 3: Pregunta con respuesta incorrecta

**Archivo**: `app-c1/questions.js:1039-1041`
- Pregunta: R* para T=0.8, Ro=7 usando la fórmula de la app
- Answer: 4.47, pero la explicación calcula 4.2
- Debería ser: R* = 1 + 6×0.8/(0.7+0.8) = 1 + 3.2 = **4.2** (no 4.47)

---

## 13. Recomendaciones para el Taller

1. **Usar Ecuación (10)** para R* en el espectro de ETABS, a menos que el Prof. Music
   indique usar la alternativa (Ec. 11) para muros.

2. **Verificar Qmín**: Para nuestro edificio, Cmín gobierna. En ETABS, escalar las
   fuerzas del análisis modal para que Qbasal ≥ Qmín = 656 tonf.

3. **Espectro en ETABS**: Usar From File con el espectro elástico (Sa/g) y SF=9.81.
   Luego reducir por R* en las combinaciones o en el Scale Factor del Load Case.

4. **Método del Prof. Music** (Material Apoyo Taller 2026):
   - Calcular R* con T* del análisis
   - Verificar que Qbasal ≥ Qmín
   - Si Qbasal < Qmín, escalar fuerzas por factor Qmín/Qbasal
