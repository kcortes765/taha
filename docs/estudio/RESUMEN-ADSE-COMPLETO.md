# Resumen ADSE — Análisis y Diseño Sísmico de Edificios
> UCN, Prof. Music, 1S-2026 | C1: 5 mayo | C2: 26 mayo | C3: 30 junio

---

## C1 — SISMOLOGÍA (sem 1-3, 20%)

### Conceptos base
- **Riesgo sísmico** = Peligro × Vulnerabilidad
- **Rigidez**: resistencia a deformarse (pendiente curva F-δ)
- **Ductilidad**: μ = Δ_nl / Δ_1era (capacidad de deformarse sin colapsar)
- **Energía disipada**: área bajo lazo histerético

### Diafragmas
- **Rígido**: CM y CR definen torsión natural; 3 GDL/piso (ux, uy, uθ)
- **Flexible**: IF = DMD/DPEV; IF ≤ 2.0 → rígido (ASCE 7-16)
- **Torsión**: et = ex ± ea, donde ea = ±0.05·b (accidental)

### Clasificación edificios sismorresistentes
| Tipo | Sistema | Altura máx |
|------|---------|------------|
| I | Marcos rígidos | 20-22 pisos |
| II | Muros simples | 30-35 pisos |
| III | Muros acoplados | 30-35 pisos |
| IV | Marcos + muros | 45-50 pisos |
| V | Tubo | 50-65 pisos |

### Normativa chilena
- **NCh433:1996 Mod.2009 + DS61** → diseño sísmico edificios
- **DS60** → hormigón armado (basado en ACI318-08)
- **NCh3171:2017** → estados de carga
- **Filosofía**: sin daño (moderado), limitar daño (mediano), no colapso (severo)

### Zonificación y suelos
| Zona | Ao |
|------|----|
| 1 | 0.2g |
| 2 | 0.3g |
| **3 (Antofagasta)** | **0.4g** |

- Suelos A-F según DS61, clasificados por **Vs30**
- Métodos geofísicos: **MASW** (activo), **ReMi** (pasivo, microtremores)
- Vs30 = Σdi / Σ(di/Vsi) para los primeros 30m

### Método estático
```
Qo = C × I × P          (corte basal)

C = (2.75·S·Ao)/(g·R) · (T'/T*)^n

Límites:  Ao·S/(6g) ≤ C ≤ Cmáx
```
- **P** = peso sísmico (permanentes + % sobrecarga)
- **I** = factor importancia: Cat I (0.6), Cat II (1.0), Cat III-IV (1.2)
- **R, Ro**: Muros HA → R=7, Ro=11; Marcos HA → R=7, Ro=11
- Fuerzas por piso: Fk proporcional a Ak·hk
- Se aplica cuando: edificios regulares, altura limitada

### Parámetros suelo (DS61)
| Suelo | S | To | T' | n | p |
|-------|---|----|----|----|---|
| A | 0.90 | 0.15 | 0.20 | 1.00 | 2.0 |
| B | 1.00 | 0.30 | 0.35 | 1.33 | 1.5 |
| **C** | **1.05** | **0.40** | **0.45** | **1.40** | **1.60** |
| D | 1.20 | 0.75 | 0.85 | 1.80 | 1.0 |
| E | 1.30 | 1.20 | 1.40 | 2.00 | 1.0 |

### Método dinámico modal espectral
```
Sa = (S·Ao·α) / (R*/I)        (espectro de diseño)

α(T) = [1 + 4.5·(T/To)^p] / [1 + (T/To)³]

Modos: acumular ≥ 90% masa en cada dirección
Superposición: CQC (no SRSS)
```

### Condiciones de drift (NCh433)
- **Condición 1**: drift en CM ≤ 0.002 por piso
- **Condición 2**: drift en cualquier punto ≤ 0.001 (torsión)

### Torsión accidental (método dinámico) — 3 formas
- **Caso a)**: Desplazar CM (modificar mass source)
- **Caso b) Forma 1**: Aplicar momentos estáticos Mt = F·e
- **Caso b) Forma 2**: Excentricidad por piso en load case

### R* y Pushover
```
R* = FSRE × FIRNL × FDED

FSRE = Q_1era / Q_diseño     (sobrerresistencia elástica)
FIRNL = Q_nl / Q_1era        (incursión no lineal)
FDED = Q_e / Q_nl            (dif. elástico-inelástico)

Típicamente: Q_nl ≈ (1.9 a 3.0) × Q_diseño
```

### Perfil bio-sísmico (13 indicadores)
1. H/T₁ (rigidez global)
2. Efecto P-Δ (Mv_PΔ / Mv_sísmica)
3. δ_techo/H ≤ 1/1000
4. Drift CM ≤ 0.002
5. Drift extremo ≤ 0.001
6. T_rot / T_trasl (acoplamiento)
7-11. Masas/cortes acoplados vs directos
12. ≥ 3 ejes resistentes por dirección
13. R efectivo

---

## C2 — ANÁLISIS SÍSMICO (sem 4-8, 40%)

### Matriz de rigidez
- 1 piso asimétrico: **3 GDL** (ux, uy, uθ) → matriz [K] 3×3
- N pisos: **3N GDL** → vector u = {ux, uy, uθ} por piso
- Métodos: **equilibrio directo** (desplaz. unitarios) o **rigidez directa** (subestructuras)
- Ensamble: [K]global = Σ [Ap]ᵀ [Kp] [Ap]
- Matrices de transformación: axi, ayi (posición subestructura respecto CM)

### Procedimiento análisis dinámico (9 etapas)
1. Estructurar edificio (identificar elementos resistentes)
2. Identificar subestructuras verticales
3. Matriz rigidez local de cada subestructura
4. Condensación estática → rigidez horizontal
5. Matriz rigidez del edificio (sistema global)
6. Matriz de masas (diagonal: m, m, Io por piso)
7. Frecuencias naturales ω y modos de vibrar φ
8. Normalizar modos (φᵀMφ = I)
9. Masas equivalentes (participación modal Ux%, Uy%, Rz%)

### Post-análisis
- Verificar Q_mín ≤ Q_basal (si no, escalar)
- CQC para superponer modos
- Torsión accidental (3 métodos)
- Drift condiciones 1 y 2
- Verificar participación modal ≥ 90%

### Estados de carga NCh3171:2017
```
C1: 1.4D
C2: 1.2D + 1.6L + 0.5Lr
C3: 1.2D + L + 1.6Lr
C4: 1.2D + L ± 1.4E
C5: 0.9D ± 1.4E
```
(aplicar C4-C5 en ambas direcciones → C4x, C5x, C4y, C5y)

---

## C3 — DISEÑO MUROS + MARCOS (sem 12-17, 40%)

### Diseño muros HA (Cap 3)

**Verificaciones previas:**
- Esbeltez: t > lu/16 (evitar pandeo)
- Compresión: Pu ≤ 0.35·f'c·Ag

**a) Diseño al corte:**
```
φVn ≥ Vu

Vn = Vc + Vs ≤ 0.83·√f'c · Acv    (muros especiales)
Vc = 0.53·λ·√f'c · bw·d            (simplificado)
d = 0.8·lw

αc: 0.25 si hw/lw ≥ 2.0 (esbelto)
     0.17 si hw/lw ≤ 1.5 (achaparrado)
     interpolar entre medio

Armadura mín: ρt = ρl ≥ 0.0025
Espaciamiento: s ≤ 3t ni 45cm
```

**b) Diseño a flexión compuesta:**
- **Diagrama de interacción** Pu-Mu (o Pu-Mn)
- φMn ≥ Mu y φPn ≥ Pu simultáneamente
- Secciones compuestas (L, T, C): considerar sección completa
- Ancho efectivo ala: menor de 0.5·dist_muro_vecino ó 0.25·Ht
- 4 subcombinaciones por estado: ±P(E) ± M(E)

**c) Verificación curvatura (si Ht/lw ≥ 3):**
```
φu = 0.008/c     (capacidad curvatura)

Demanda ≤ Capacidad
δu = desplazamiento de diseño (DS61, espectro desplazamiento)
```

**d) Confinamiento elementos de borde:**
```
Si c ≥ c_lim → REQUIERE confinamiento

c_lim = lw / [600·(δu'/hw)]     (DS60)

Largo confinar: cc = c - c_lim
Espesor elem borde ≥ 30cm
Altura confinar: máx(lw, Mu/4Vu)

Ash = 0.09·s·bc·f'c/fyt     (armadura confinamiento)
```

**Predimensionamiento rápido:**
- τ_lim = (0.6/1.4)·2τc → área mínima muros
- Peso/área ≈ 1 tonf/m² (regla de pulgar)

### Diseño marcos HA (Cap 4)

**Vigas de marcos especiales:**
```
Geométricas: bw ≥ 25cm, Pu < Ag·f'c/10

Longitudinal:
  M⁻(cara nudo) ≥ mayor Mu de combos
  M⁺(cara nudo) ≥ 0.5·M⁻
  M(cualquier sección) ≥ 0.25·M_máx

Corte (por capacidad, NO del análisis):
  Ve = (Mpr₁ + Mpr₂)/ln     (Mpr con 1.25fy)

Zona rótula plástica: s1 = 2h
  Espaciamiento: mín(d/4, 8db_long, 24db_cerco, 300mm)
  Primer cerco a ≤ 50mm de cara apoyo
  Fuera zona rótula: s ≤ d/2
  Ganchos sísmicos: 135°
```

**Columnas de marcos especiales:**
```
Geométricas: b ≥ 300mm, b/h ≥ 0.4, Pu > Ag·f'c/10

Longitudinal: ρ_mín = 0.01, ρ_máx = 0.06
  Traslapes solo en mitad central

Zona crítica: l0 = máx(h, lu/6, 450mm)
  Confinamiento: Ash = 0.09·s·bc·f'c/fyt
  Espaciamiento: mín(b/4, 6db, (350+100-hx)/3)

Corte (por capacidad):
  Ve = (Mpr₁ + Mpr₂)/lu
```

**Columna fuerte — viga débil:**
```
ΣMnc ≥ (6/5) · ΣMnb = 1.2 · ΣMnb
```

**Nudo viga-columna:**
```
Confinado 4 caras: Vn = 1.7·√f'c · Aj
Confinado 3 caras: Vn = 1.25·√f'c · Aj
Otros:             Vn = 1.0·√f'c · Aj
φ = 0.85
```

---

## Datos Taller — Edificio 1 (20 pisos, muros)

| Parámetro | Valor |
|-----------|-------|
| Ubicación | Antofagasta, Zona 3, Ao=0.4g |
| Suelo | C (S=1.05, To=0.40, n=1.40, p=1.60) |
| Categoría | II (oficina), I=1.0 |
| Hormigón | G30: f'c=300 kgf/cm², Ec=25742 MPa |
| Acero | A630-420H: fy=4200 kgf/cm² |
| Altura | P1=3.4m, P2-20=2.6m → H=52.8m |
| Vigas | Invertidas 20×60cm (J=0) |
| Losas | e=15cm (inercia 25%) |
| Muros Y e=30 | Ejes 1,3,4,5,7,12,13,14,16,17 |
| Muros Y e=20 | Ejes 2,6,8,9,10,11,15 |
| SC oficina | 250 kgf/m² |
| SC pasillo | 500 kgf/m² |
| SC techo | 100 kgf/m² |
| TERP | 140 kgf/m² |
| TERT | 100 kgf/m² |

**Valores esperados:** T₁ ≈ 1.0-1.3s | Peso ≈ 9368 tonf | Drift < 0.002

---

## Fórmulas rápidas

```
Ec = 4700·√f'c  [MPa]
1 MPa ≈ 10 kgf/cm²
g = 9.81 m/s²

Qo = C·I·P
Q_mín = Ao·S·I·P / (6g)

Peso/área ≈ 1 tonf/m²  (verificación rápida)
```
