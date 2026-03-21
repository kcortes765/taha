# Tablas de Referencia Rápida — ADSE 2026

## Parámetros sísmicos por zona (NCh433 + DS61)

| Zona | Ciudades principales | Ao/g |
|------|---------------------|------|
| 1 | Sur (Valdivia, Osorno) | 0.20 |
| 2 | Centro (Stgo, Concepción) | 0.30 |
| **3** | **Norte (Antofagasta, Calama)** | **0.40** |

## Parámetros de suelo (DS61 Tabla 6.3)

| Suelo | Descripción | S | To (s) | T' (s) | n | p |
|-------|-------------|---|--------|--------|---|---|
| A | Roca | 0.90 | 0.15 | 0.20 | 1.00 | 1.50 |
| B | Roca blanda | 1.00 | 0.30 | 0.35 | 1.33 | 1.50 |
| **C** | **Suelo denso** | **1.05** | **0.40** | **0.45** | **1.40** | **1.60** |
| D | Suelo rígido | 1.20 | 0.75 | 0.85 | 1.80 | 1.00 |
| E | Suelo blando | 1.30 | 1.20 | 1.35 | 1.80 | 1.00 |
| F | Licuación/rellenos | - | - | - | - | - |

## Factor R y Ro (NCh433 + DS61)

| Sistema estructural | R | Ro |
|--------------------|----|-----|
| Marcos rígidos HA especiales | 7 | 11 |
| Muros HA especiales | 7 | 11 |
| Marcos HA intermedios | 5 | 7 |
| Marcos de acero especiales | 7 | 11 |
| Pórticos simples | - | 3 |

## Factor de importancia I (NCh433 art.4.1)

| Tipo | Descripción | I |
|------|-------------|---|
| I | No esencial | 0.6 |
| **II** | **Uso normal (Oficinas)** | **1.0** |
| III | Emergencias | 1.2 |
| IV | Infraestructura crítica | 1.2 |

---

## Combinaciones de carga NCh3171:2017

| # | Expresión | D incluye |
|---|-----------|-----------|
| C1 | 1.4(D+L_supermuerta) | PP + TERP + TERT |
| C2 | 1.2D + 1.6L + 0.5Lr | + SCP + SCT |
| C3 | 1.2D + L + 0.5Lr + **1.4Ex** | + SEx |
| C4 | 1.2D + L + 0.5Lr + **1.4Ey** | + SEy |
| C5 | 0.9D + **1.4Ex** | - |
| C6 | 0.9D + **1.4Ey** | - |
| C7 | 0.9D - **1.4Ex** | - |
| C8 | 0.9D - **1.4Ey** | - |

---

## Límites de deformación

| Condición | Limit | Descripción |
|-----------|-------|-------------|
| Drift CM | ≤ 0.002 | Condición 1 NCh433 |
| Drift extremo | ≤ 0.001 | Condición 2 NCh433 |
| δ/H total | ≤ 0.001 | Desplazamiento techo/altura total |
| P-Δ | Θ = P×δ/(V×h) ≤ 0.10 | Efecto P-Delta |

---

## Fórmulas espectro NCh433+DS61 (Antofagasta Zona 3, Suelo C)

```
α(T) = (1 + 4.5·(0.40/T)^1.60) / (1 + (0.40/T)^3)

Sa_e(T) = 1.05 × 0.40g × α(T) = 0.42g × α(T)   [espectro elástico]

Sa_d(T) = Sa_e(T) / R*   [espectro de diseño]

R*(Ro=11, T*):
  T0r = 0.1 × 11² / (11-1) = 1.21 s
  Si T* ≥ 1.21: R* = 1 + 10 × T*/(12.1+T*)
  Si T* < 1.21: R* = 1 + 10 × √(T*/1.21)
```

**Tabla R* para Ro=11:**
| T* (s) | R* | Sa_d/g |
|--------|-----|--------|
| 0.50 | 4.21 | Sa_e/4.21 |
| 1.00 | 5.82 | Sa_e/5.82 |
| 1.21 | 6.55 | Sa_e/6.55 |
| 1.50 | 6.76 | Sa_e/6.76 |
| 2.00 | 7.43 | Sa_e/7.43 |

---

## Diseño de muros HA — fórmulas clave

### Corte
| Fórmula | Descripción |
|---------|-------------|
| Vn ≤ 0.83√f'c·Acv | Límite máximo |
| Vc = αc·√f'c·Acv | Aporte hormigón |
| αc = 0.53 (hw/lw≥2) | Edificios altos |
| d = 0.8·lw | Peralte efectivo |
| ρt ≥ 0.0025 | Armadura mínima horizontal |
| sl ≤ min(3t, 450mm) | Espaciamiento máximo |

### Flexión compuesta
| Fórmula | Descripción |
|---------|-------------|
| Φ·Mn ≥ Mu | Condición flexión |
| Φ·Pn ≥ Pu | Condición axial |
| Pu ≤ 0.35·f'c·Ag | Límite compresión |
| β₁ (G30) = 0.836 | Factor bloque compresión |

### Curvatura y confinamiento
| Fórmula | Descripción |
|---------|-------------|
| clim = 600·t·δu'/(hwi·3) | Límite posición eje neutro |
| cc = c - clim | Largo a confinar |
| lc = max(lw, Mu/4Vu) | Altura a confinar |
| Ash = 0.09·s·bc·f'c/fyt | Armadura confinamiento |
| t_borde ≥ 30 cm | Espesor elemento borde |

---

## Diseño de marcos HA — fórmulas clave

### Vigas
| Fórmula | Descripción |
|---------|-------------|
| ρmín = max(0.25√f'c/fy, 1.4/fy) | G25: ρmín=0.00333 |
| ρmáx = 0.025 | Zonas sísmicas |
| M⁺ ≥ 0.5·M⁻ | Restricción nudos |
| Ve = (Mpr_L+Mpr_R)/Ln ± wuLn/2 | Corte diseño (no análisis) |
| Mpr = As·1.25fy·(d-a/2) | Momento probable |
| s₁ = 2h (zona crítica) | Longitud rótula plástica |

### Columnas
| Fórmula | Descripción |
|---------|-------------|
| ρ ∈ [1%, 6%] | Armadura longitudinal |
| l₀ ≥ max(h, lu/6, 450mm) | Zona de confinamiento |
| Ash = 0.09·s·bc·f'c/fyt | Confinamiento |
| Ve = (Mpr_sup+Mpr_inf)/lu | Corte diseño |
| ΣMnc ≥ 1.2·ΣMnb | Col. fuerte–viga débil |

### Nudos
| Tipo nudo | Vn = γ√f'c·Aj | Φ |
|-----------|--------------|---|
| 4 caras confinadas | 1.70√f'c·Aj | 0.85 |
| 3 caras confinadas | 1.25√f'c·Aj | 0.85 |
| Otros | 1.00√f'c·Aj | 0.85 |

---

## Tablas de barras de refuerzo (A630-420H)

| Barra | db (mm) | Área (cm²) | Peso (kg/m) |
|-------|---------|------------|-------------|
| ∅8 | 8 | 0.503 | 0.395 |
| ∅10 | 10 | 0.785 | 0.617 |
| ∅12 | 12 | 1.131 | 0.888 |
| ∅14 | 14 | 1.539 | 1.208 |
| ∅16 | 16 | 2.011 | 1.578 |
| ∅18 | 18 | 2.545 | 1.998 |
| ∅20 | 20 | 3.142 | 2.466 |
| ∅22 | 22 | 3.801 | 2.984 |
| ∅25 | 25 | 4.909 | 3.854 |
| ∅28 | 28 | 6.158 | 4.834 |
| ∅32 | 32 | 8.042 | 6.313 |
| ∅36 | 36 | 10.179 | 7.990 |

## Área de armadura por metro (cm²/m)

| db | s=100 | s=150 | s=200 | s=250 | s=300 |
|----|-------|-------|-------|-------|-------|
| ∅10 | 7.85 | 5.24 | 3.93 | 3.14 | 2.62 |
| ∅12 | 11.31 | 7.54 | 5.65 | 4.52 | 3.77 |
| ∅14 | 15.39 | 10.26 | 7.70 | 6.16 | 5.13 |
| ∅16 | 20.11 | 13.40 | 10.05 | 8.04 | 6.70 |
| ∅18 | 25.45 | 16.97 | 12.73 | 10.18 | 8.48 |
| ∅20 | 31.42 | 20.94 | 15.71 | 12.57 | 10.47 |
| ∅25 | 49.09 | 32.72 | 24.54 | 19.63 | 16.36 |

---

## Materiales — propiedades elásticas

| Material | f (MPa) | E (MPa) | ν | γ (tonf/m³) |
|----------|---------|---------|---|-------------|
| G25 | f'c=25 | 23500 | 0.2 | 2.5 |
| **G30** | **f'c=30** | **25742** | **0.2** | **2.5** |
| G35 | f'c=35 | 27806 | 0.2 | 2.5 |
| A630-420H | fy=420 | 200000 | 0.3 | 7.85 |

Ec = 4700√f'c [MPa]

---

## Notación del curso (Prof. Music)

| Símbolo | Descripción |
|---------|-------------|
| PP | Peso propio |
| SCP | Sobrecarga de uso (piso) |
| SCT | Sobrecarga de uso (techo) |
| TERP | Terminaciones piso |
| TERT | Terminaciones techo |
| SEx/SEy | Sismo en X o Y |
| VI20/60G30 | Viga invertida 20×60 cm, G30 |
| MHA30G30 | Muro HA 30cm, G30 |
| MHA20G30 | Muro HA 20cm, G30 |
| Losa15G30 | Losa 15cm, G30 |
| G | Hormigón (Gxx = f'c en MPa) |
| Ao | Aceleración pico del terreno |
| T* | Período fundamental de vibración |
| R* | Factor de reducción espectral |
| Ro | Factor de reducción base |
| CM | Centro de masa |
| CR | Centro de rigidez |
| ea | Excentricidad accidental |
| hw | Altura total del muro/edificio |
| lw | Largo del muro en planta |
| t | Espesor del muro |
