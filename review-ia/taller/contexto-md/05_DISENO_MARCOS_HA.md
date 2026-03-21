# Diseño de Marcos Especiales de HA — Edificio 2

## Referencia
- Apuntes: `04-Marcos-Especiales-HA.pdf` (32 págs, págs 250-281 orig.)
- Manual ETABS: `manuales-csi/Manual Diseño Marco H.A-ACI-318-08.pdf`
- Normativa: DS60 (ACI318-08)

---

## Edificio 2 — Datos para diseño

**Sistema**: Marcos especiales HA (5 pisos)

| Pisos | Columnas | Vigas | Losa |
|-------|----------|-------|------|
| 1-2 | 70×70 cm | 50×70 cm | 17 cm |
| 3-5 | 65×65 cm | 45×70 cm | 17 cm |

**Marco a diseñar**: Eje A (marco perimetral, 5 vanos de 6.5m)

---

## 4.1 Diseño de Vigas de Marco Especial

### Condiciones geométricas
```
Pu < Ag × f'c / 10     (≤ 10% carga axial → si no, tratar como columna)
bw ≥ 25 cm
bw ≤ min(C2 + C2/3, C2 + 0.3h)   donde C2 = ancho columna
Ln ≥ 4d
hw ≥ 2bw    (para edificio con muros, hw = peralte viga)
```

Para vigas 50×70 (pisos 1-2):
- bw = 50 cm ≥ 25 cm ✓
- d = 70 - 5 (rec) - 1 (gancho) - db/2 ≈ 63 cm
- Ln = 6.5 - 0.70 = 5.80 m ≥ 4×0.63 = 2.52 m ✓

### Armadura longitudinal
```
ρmín = max(0.25√f'c/fy, 1.4/fy)   [ACI 21.5.2.1]
Para f'c=25MPa, fy=420MPa:
ρmín = max(0.25√25/420, 1.4/420) = max(0.00298, 0.00333) = 0.00333

ρmáx = 0.025   (ACI 21.5.2.1, zonas sísmicas)
```

**Restricciones en nudos:**
```
M⁻ cara nudo ≥ Mu(análisis)
M⁺ cara nudo ≥ 0.5 × M⁻ cara nudo
M(cualquier sección) ≥ 0.25 × max(M⁻ cara)
```

**Traslapes:**
- NO dentro de nudos
- NO en zonas de fluencia esperada (extremos viga, longitud d desde cara nudo)
- NO en zonas de separación doble

### Corte de diseño — Rótulas plásticas (ACI 21.5.4)
**⚠️ NO usar el Vu del análisis. Usar el Ve basado en Mpr:**

```
Ve = (Mpr_izq + Mpr_der) / Ln  +  Wu×Ln/2

Mpr = momento probable = Mn(con 1.25×fy en lugar de fy)
    = As × 1.25fy × (d - a/2)   con a = As×1.25fy/(0.85×f'c×b)

Wu = 1.2×w_muerta + 1.6×w_viva   (cargas gravitacionales amplificadas)
```

Para pisos 1-2, viga 50×70, Ln=5.8m, G25, A630-420H:
```
Mpr_izq = Mpr con armar sup × 1.25 × 420
Mpr_der = Mpr con armar inf × 1.25 × 420
Ve ≥ 2×Mpr/Ln
```

### Zona de rótula plástica (ACI 21.5.3)
```
Longitud zona crítica s₁ = 2h = 2 × 70 = 140 cm
(desde cara de la columna hacia el centro del vano)

s en zona crítica ≤ min(d/4, 8db_long, 24db_estribo, 300mm)
Primer estribo a ≤ 50mm de cara columna

s₂ ≤ d/2  (fuera de zona crítica)
```

### Detallamiento
- Ganchos sísmicos: 135° en barras de la viga y estribos
- Estribos cerrados traslapados
- Barras corridas: mín 2 arriba y 2 abajo en toda la longitud

---

## 4.2 Diseño de Columnas de Marco Especial

### Condiciones geométricas (ACI 21.6.1)
```
Pu > Ag × f'c / 10   (o b/h ≥ 0.4)
Sección mínima: 300mm × 300mm
b/h ≥ 0.4
```

Para columnas 70×70 (pisos 1-2):
- Pu > Ag×f'c/10 = 70×70×250/10 = 122500 kgf = 122.5 tonf → verificar

### Armadura longitudinal
```
ρmín = 0.01   (1%)
ρmáx = 0.06   (6%)

Traslapes: solo en el tercio central de la altura libre
           dimensionados como traslapes en tracción (Clase B)
```

Para columna 70×70: Ag = 4900 cm²
- As_mín = 0.01 × 4900 = 49 cm² → 12∅25 = 58.9 cm² ≈ OK
- As_máx = 0.06 × 4900 = 294 cm²

### Diagrama de interacción biaxial
Columnas de edificio real se diseñan con diagramas PMM en 3D (ETABS Section Designer).
Para diseño simplificado: método de cargas recíprocas de Bresler.

```
1/P_mn = 1/Mnx + 1/Mny - 1/P_o

donde P_o = resistencia axial pura = 0.85×f'c×(Ag-Ast) + fy×Ast
```

### Zona crítica de confinamiento (ACI 21.6.3)
```
l₀ = mayor de: h_columna, lu/6, 450 mm

donde lu = longitud libre de la columna

Para columna 70×70, lu típico = 3.0-3.5m:
l₀ ≥ max(70, 3000/6, 450) = max(70, 500, 450) = 500 mm = 50 cm
```

### Armadura de confinamiento en zona crítica
```
Ash = max(0.09×s×bc×f'c/fyt, 0.3×s×bc×(Ag/Ach-1)×f'c/fyt)

s ≤ min(b/4, 6db_long, (350+100-hx)/3, 150mm)
  ≤ (350+100-hx)/3   donde hx = separación lateral máx de barras

Para columna 70×70, G25, A630-420H:
Ash/s = 0.09×bc×250/4200 = 0.00536×bc   [cm²/cm]
```

### Corte de diseño — Columna fuerte (ACI 21.6.5)
**⚠️ NO usar Vu del análisis. Usar Mpr de las vigas conectadas:**

```
Ve = (Mpr_top + Mpr_bot) / lu

Mpr_top = mayor Mpr de las vigas conectadas en el nudo superior
Mpr_bot = mayor Mpr de las vigas conectadas en el nudo inferior
```

Verificar: Φ×Vn ≥ Ve

---

## 4.3 Columna Fuerte — Viga Débil

**⚠️ Requisito crítico ACI 21.6.2:**
```
ΣMnc ≥ (6/5) × ΣMnb

ΣMnc = suma de momentos nominales de las columnas en el nudo
ΣMnb = suma de momentos nominales de las vigas en el nudo
```

Verificar en AMBAS direcciones de la viga (sismo X y sismo Y).
Si no cumple → aumentar refuerzo de columnas.

---

## 4.4 Diseño del Nudo (ACI 21.7)

### Fuerza de corte en el nudo
```
Vj = T_vigas - V_columna

T_vigas = Ts_arriba + Cs_abajo   (fuerzas de tracción/compresión de barras)
V_columna = Vu de la columna adyacente
```

### Resistencia del nudo (ACI 21.7.4)
```
ΦVn_nudo ≥ Vj    (Φ = 0.85)

Vn = γ × √f'c × Aj   [kgf]

donde Aj = área efectiva del nudo
```

**Valores de γ:**
| Condición del nudo | γ |
|-------------------|---|
| Confinado por vigas en 4 caras | 1.70 |
| Confinado por vigas en 3 caras | 1.25 |
| Otros casos | 1.00 |

---

## Proceso de diseño marco eje A (resumen)

### Extraer de ETABS
Para cada piso del marco A:
- Mu_vigas (cara nudo izq/der, sup/inf)
- Pu_columnas (máx compresión y mínima)
- Mu_columnas (en X e Y)
- Vu de análisis (solo referencial; NO usar para diseño)

### Diseño vigas
1. Calcular As_long con Mu de ETABS (Mn de armaduras tentativas)
2. Verificar restricciones M⁺ ≥ 0.5M⁻, etc.
3. Calcular Mpr (1.25fy) de los As definitivos
4. Calcular Ve de rótulas plásticas
5. Armar estribos en zona crítica (2h) y fuera

### Diseño columnas
1. Diagrama PMM con Pu, Mux, Muy de combos
2. Verificar ρ_long ∈ [1%, 6%]
3. Verificar columna fuerte-viga débil
4. Calcular Ve de columna (Mpr vigas/lu)
5. Armar confinamiento en zona crítica (l₀)

### Diseño nudo
1. Calcular Vj
2. Verificar ΦVn ≥ Vj
3. Si no cumple → cambiar geometría o aumentar hormigón

---

## Tabla resumen requisitos marcos especiales HA (ACI318-08)

| Elemento | Parámetro | Valor |
|----------|-----------|-------|
| Viga | Pu | < Ag×f'c/10 |
| Viga | ρ_long | [1.4/fy, 0.025] |
| Viga | M⁺/M⁻ nudo | ≥ 0.5 |
| Viga | s zona crítica | ≤ d/4 o 8db o 24db_e o 300mm |
| Viga | Ve | Mpr/Ln (no análisis) |
| Columna | b mínimo | 300 mm |
| Columna | ρ_long | [1%, 6%] |
| Columna | l₀ crítica | max(h, lu/6, 450mm) |
| Columna | Ash | 0.09×s×bc×f'c/fyt |
| Columna | Ve | (Mpr_arr+Mpr_aba)/lu |
| Nudo | ΣMnc/ΣMnb | ≥ 6/5 |
| Nudo | ΦVn | γ×√f'c×Aj (Φ=0.85) |
