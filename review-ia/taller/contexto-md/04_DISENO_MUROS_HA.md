# Diseño de Muros de Hormigón Armado — ADSE 2026

## Normativa aplicable
- **DS60 (2011)** → basado en ACI318-08 (diseño/cálculo HA)
- **DS61 (2011)** → diseño sísmico
- Material de referencia: `Diseño de Muros/3 métodos diseño muros.pdf` (Prof. Music, 13p)
- Ejemplos: `Diseño de Muros/Ejemplos Diseño de MHA J.M.pdf` (32p)

---

## Procedimiento de diseño — Muro especial HA (DS60/ACI318-08)

### Pasos en orden
```
a) Verificación esbeltez
b) Verificación compresión axial máxima
c) Diseño al CORTE
d) Diseño a FLEXIÓN COMPUESTA (Pu-Mu)
e) Verificación de CURVATURA y CONFINAMIENTO
```

---

## a) Verificación de esbeltez
```
t ≥ lu/16    (sin pandeo lateral)

donde lu = longitud libre entre apoyos laterales
```
Si no cumple → verificar pandeo fuera del plano.

---

## b) Compresión axial máxima (DS60 Art. 21.9.2)
```
Pu ≤ 0.35 × f'c × Ag
```
Si se supera → muro no es adecuado (problema de predimensionamiento).

---

## c) Diseño al Corte (DS60 Art. 21.9.2 + ACI 21.9.4)

### Limitación absoluta de Vn
```
Vn ≤ 0.83 × √f'c × Acv    [kgf, cm]
```
donde `Acv = t × lw` = área de la sección transversal del muro

Si se supera → aumentar espesor del muro.

### Resistencia al corte
```
Vn = Vc + Vs ≥ Vu/φ     (φ = 0.75)

Vc = αc × λ × √f'c × Acv
```

**Coeficiente αc según relación hw/lw:**
| hw/lw | αc |
|-------|-----|
| ≤ 1.5 | 0.80 |
| ≥ 2.0 | 0.53 |
| intermedio | interpolar |

Para hw/lw > 2 (edificios altos): αc = 0.53

**Forma simplificada** (más común):
```
Vc = 0.53 × λ × √f'c × bw × d

donde: d = 0.8 × lw, λ=1.0 (HA normal)
```

**Aporte del acero (Vs):**
```
Vs = Ah × fyt × d / s

Armadura transversal mínima:
ρt ≥ 0.0025    (refuerzo horizontal distribuido)
s ≤ min(3t, 45cm)

Ah/s = ρt × t × 100   [cm²/m]
```

**Armadura vertical (refuerzo distribuido)**
```
ρl ≥ 0.0025    (si hw/lw ≥ 2.5)
ρl ≥ ρt        (siempre)
sl ≤ min(3t, 45cm)
```

### Diagrama de flujo diseño al corte
```
1. Calcular Vu (de combinaciones)
2. Verificar: Vu/φ ≤ 0.83√f'c×Acv → Si no → aumentar espesor
3. Calcular Vc = αc×√f'c×Acv (o forma simplificada)
4. Vs necesario = Vu/φ - Vc
5. Calcular ρt = Vs/(fyt×Acv)
6. Tomar ρt_diseño = max(ρt_necesario, 0.0025)
7. Calcular s = Ah/(ρt×t) [barras a usar]
8. Verificar s ≤ min(3t, 45cm)
```

---

## d) Diseño a Flexión Compuesta (Pu-Mu)

### Estados de carga para el diseño
Cada combo NCh3171 da un par (Pu, Mu). Con signo sísmico hay 4 subcombinaciones:
```
+P(E) + M3(E)    →  (Pu1, Mu1)
+P(E) - M3(E)    →  (Pu2, Mu2)
-P(E) + M3(E)    →  (Pu3, Mu3)
-P(E) - M3(E)    →  (Pu4, Mu4)
```

### Diagrama de interacción
Verificar que todos los pares (Pu, Mu) estén DENTRO del diagrama Φ(Mn, Nn).

```
Φ × Mn ≥ Mu
Φ × Nn ≥ Nu
```

Factores de reducción (ACI318-08 / DS60):
- Φ = 0.90 (flexión pura)
- Φ = 0.65 → 0.90 (combinada, según nivel de compresión)
- Φ = 0.75 (corte)

### β₁ (factor bloque equivalente)
```
β₁ = 0.85 - 0.05×(f'c - 4000)/1000   [psi]
   = 0.85 - 0.05×(f'c - 280)/70       [kgf/cm²]

Para G30: β₁ = 0.85 - 0.05×(300-280)/70 = 0.836
```

### Muros con sección no rectangular (en T o L)
Según ACI 21.9.5.2:
- Tomar la sección completa (incluyendo alas)
- Ancho efectivo del ala ≤ min(0.5×dist_libre, 0.25×Ht)
- Ht = altura total del edificio

### Tablas Pu-Mu disponibles (Gerdau AZA)
En `tablas/Tabla Diseño de Muros.pdf`:
- 32 diagramas para diferentes f'c (20-55 MPa) y γ (0.8-0.9)
- ρw = 0.25% y 0.50%

---

## e) Verificación de Curvatura y Confinamiento (DS60 Art. 21.9.5.4)

### Condición de aplicación
Solo aplica si: `hw/lw ≥ 3`

Si cumple, verificar que la **demanda de curvatura ≤ capacidad de curvatura**.

### Demanda de curvatura (δu DS61)
```
δu = desplazamiento de diseño en el nivel superior del muro
   = extraer de análisis ETABS (Story Drifts × h_piso × factor)
```

El DS61 proporciona espectro de desplazamiento:
```
Sd(T*) = Sa(T*) × (T*/2π)² × g
```

### Capacidad de curvatura (ACI318-08 Eq. 21-7a y 21-7b)
```
Ecuación 21-7b (curvatura demandada):
φu_demanda = (δu' × lp) / (lp² × (hw - lp/2))

Ecuación 21-7a (comparar con capacidad):
φu_capacidad ≥ φu_demanda  →  φu_cap = 0.008/c
```

donde:
- c = profundidad eje neutro (de la flexión compuesta con Pu máximo)
- lp = longitud de la zona plástica

### Determinar si se requiere confinamiento
```
Limite: clim = (600 × t × δu') / (hwi × 3)

donde: hwi = distancia desde la base al último nivel significativo
       δu' = desplazamiento relativo de diseño en la sección crítica
       t = espesor del muro

Si c ≥ clim → requiere confinamiento (elementos de borde)
```

### Diseño del elemento de borde

**Longitud a confinar:**
```
cc = c - clim    [longitud a confinar desde el borde]
```

Requerimientos del elemento de borde:
- Espesor ≥ 30 cm (si c ≥ clim)
- Largo ≥ espesor del muro
- Largo ≥ cc

**Altura a confinar (desde la base):**
```
lc = max(lw, Mu/(4×Vu))
```

### Armadura de confinamiento
```
Ash = 0.09 × s × bc × f'c / fyt

donde:
  s = espaciamiento de estribos (≤ min(b/4, 6db, 100mm))
  bc = dimensión del núcleo confinado entre estribos
  fyt = fy del acero de los estribos (420 MPa)
```

Para G30 con A630-420H:
```
Ash/s = 0.09 × bc × 300/4200 = 0.00643 × bc    [cm²/cm]
```

### Espesor mínimo elemento de borde
- ≥ 30 cm cuando se requiere confinamiento
- El ala del muro en T puede servir como elemento de borde

---

## Proceso de diseño muro eje 5 (rectangular, piso 1)

**Datos geométricos:**
- lw = 0.701 m (longitud plano muro, eje 5 entre A y B)
- t = 0.30 m (espesor)
- hw = 52.8 m (altura total)
- hw/lw = 52.8/0.701 = **75.3** → Muro esbelto, requiere verificación curvatura

**Pasos:**
1. Extraer de ETABS: Pu (máx y mín), Mu (de combos con sismo), Vu
2. Verificar Pu ≤ 0.35×300×0.30×70.1 = **221 tonf** (Acv en cm²)
3. Diseño al corte → armar con ρ ≥ 0.25%
4. Diagrama de interacción → verificar todos los (Pu, Mu)
5. Curvatura → calcular clim, comparar con c del análisis
6. Si c ≥ clim → diseñar elementos de borde con Ash

---

## Proceso de diseño muro eje 4 (sección T, piso 1)

**Datos geométricos:**
- Alma: lw_alma = 0.701 m, t_alma = 0.30 m (eje 4 entre A-B)
- Ala: lf = 5.47 m (eje C entre ejes 3-4), t_ala = 0.30 m

**Ancho efectivo ala:**
```
b_ef = min(0.5×dist_libre, 0.25×Ht)
     = min(0.5×5.47, 0.25×52.8)
     = min(2.735, 13.2) = 2.735 m (usar ala de 2.735 m)
```

**Pasos adicionales:**
- Sección compuesta → tomar sección en T completa
- Diseño biaxial: M3 (eje débil alma) y M2 (eje fuerte ala)
- El ala sirve como elemento de borde → verificar si necesita confinamiento adicional

---

## Resumen de armadura mínima muros HA (DS60)

| Armadura | Requisito | Aplicación |
|----------|-----------|------------|
| Horizontal (ρt) | ≥ 0.0025 | Toda la longitud |
| Vertical distribuida (ρl) | ≥ 0.0025 | Toda la longitud |
| s max horizontal | ≤ min(3t, 450mm) | - |
| s max vertical | ≤ min(3t, 450mm) | - |
| Barras mínimas | 2 capas si t ≥ 250mm | Siempre en muros especiales |
| Confinamiento Ash | 0.09×s×bc×f'c/fyt | Solo si c ≥ clim |

Para G30 + A630-420H, espesor t=30cm:
```
Armadura mínima: As = 0.0025 × 30 × 100 = 7.5 cm²/m
Barras ∅12 c/20: As = 5.65 cm²/m × 2 capas = 11.3 cm²/m → OK
Barras ∅10 c/15: As = 5.24 cm²/m × 2 capas = 10.5 cm²/m → OK
```
