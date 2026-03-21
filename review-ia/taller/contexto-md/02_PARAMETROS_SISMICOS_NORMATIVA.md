# Parámetros Sísmicos y Normativa — Taller ADSE 2026

## Normativa aplicable
- **NCh433 Of.1996 Mod.2009** → diseño sísmico edificios
- **DS61 (2011)** → complementa NCh433 (espectro, suelos, R*)
- **DS60 (2011)** → diseño/cálculo HA (basado en ACI318-08)
- **NCh3171:2017** → estados de carga (combinaciones)
- **NCh1537:2009** → cargas permanentes y sobrecargas
- **ACI318-08 (español)** → código concreto estructural

---

## Parámetros Sísmicos Edificio 1 (Antofagasta)

### Zonificación y suelo
| Parámetro | Valor | Fuente |
|-----------|-------|--------|
| Ciudad | Antofagasta | - |
| Zona sísmica | **Zona 3** | NCh433 art.2.5, DS61 |
| Ao/g | **0.40** | DS61 Tabla 6.1 |
| Tipo de suelo | **C** | DS61 Tabla 6.2 |
| Categoría edificio | **II** (Oficinas) | NCh433 art.4.1 |
| Factor importancia I | **1.0** | NCh433 art.4.1 |

### Parámetros del suelo tipo C (DS61 Tabla 6.3)
| Parámetro | Símbolo | Valor |
|-----------|---------|-------|
| Factor amplificación suelo | S | **1.05** |
| Periodo corte zona plana | To | **0.40 s** |
| Periodo esquina | T' | **0.45 s** |
| Exponente rama larga | n | **1.40** |
| Exponente decaimiento | p | **1.60** |

### Factor de reducción
| Sistema | Ro |
|---------|-----|
| Muros HA especiales | **11** |
| Marcos HA especiales | 11 |
| Pórticos simples | 3 |

---

## Espectro Elástico de Diseño (NCh433 + DS61)

### Función α(T)
```
α(T) = [1 + 4.5·(To/T)^p] / [1 + (To/T)^3]
```

### Aceleración espectral elástica
```
Sa_elastico(T) = S · Ao · α(T)    [fracción de g]
```

Para suelo C, Zona 3 (Antofagasta):
```
Sa_e(T) = 1.05 × 0.40 × α(T) = 0.42 × α(T)
```

### Tabla espectro (puntos clave)
| T (s) | α(T) | Sa/g |
|-------|------|------|
| 0.00 | 1.000 | 0.420 |
| 0.05 | 4.486 | 1.884 |
| 0.10 | 4.489 | 1.885 |
| 0.20 | 4.219 | 1.772 |
| 0.40 | 3.455 | 1.451 |
| 0.45 | 3.176 | 1.334 |
| 0.50 | 2.897 | 1.217 |
| 1.00 | 1.678 | 0.705 |
| 1.50 | 1.116 | 0.469 |
| 2.00 | 0.788 | 0.331 |
| 3.00 | 0.456 | 0.191 |
| 5.00 | 0.203 | 0.085 |

### Factor R* (DS61 Art. 5.1.2)
Reduce el espectro elástico al espectro de diseño:

**Sa_diseño = Sa_elastico / R***

Donde R* se calcula:
```
T0r = 0.1 × Ro² / (Ro - 1)   [para Ro=11 → T0r ≈ 1.21 s]

Si T* ≥ T0r:
    R* = 1 + (Ro-1) × T* / (0.1×Ro² + T*)

Si T* < T0r:
    R* = 1 + (Ro-1) × √(T* / T0r)
```

**Ejemplos con Ro=11:**
| T* (s) | R* |
|--------|-----|
| 0.50 | 4.21 |
| 1.00 | 5.82 |
| 1.50 | 6.76 |
| 2.00 | 7.43 |
| 3.00 | 8.29 |

### Coeficiente sísmico C (método estático)
```
C = (2.75·S·Ao) / (g·R) × (T'/T*)^n

Límites: (Ao·S)/(6g) ≤ C ≤ Cmáx
```

Para Antofagasta, suelo C, Ro=11, I=1.0, R=Ro/I=11:
```
C = (2.75 × 1.05 × 0.40g) / (g × 11) × (0.45/T*)^1.40
  = 0.1050 × (0.45/T*)^1.40

Cmín = Ao·S/(6g) = 0.40×1.05/6 = 0.0700
Cmáx = 2.75×S×Ao/(g×3) = 2.75×1.05×0.40/3 = 0.385  (no más que esto)
```

### Corte basal estático
```
Qo = C × I × P

Donde P = peso sísmico = PP + 1.0×TERP + 0.25×SCP
```

---

## Combinaciones de Carga (NCh3171:2017)

### Combinaciones básicas de diseño
| Combo | Expresión | Uso |
|-------|-----------|-----|
| C1 | 1.4D | Solo cargas muertas |
| C2 | 1.2D + 1.6L + 0.5Lr | Gravedad dominante |
| C3 | 1.2D + L + 0.5Lr + **1.4Ex** | Sismo X más desfavorable |
| C4 | 1.2D + L + 0.5Lr + **1.4Ey** | Sismo Y |
| C5 | 0.9D + **1.4Ex** | Sismo X (compresión reducida) |
| C6 | 0.9D + **1.4Ey** | Sismo Y |
| C7 | 0.9D - **1.4Ex** | Sismo X invertido |
| C8 | 0.9D - **1.4Ey** | Sismo Y invertido |

Donde:
- D = cargas muertas (PP + TERP + TERT)
- L = sobrecargas de uso (SCP, SCT)
- Ex, Ey = efectos sísmicos en X e Y

**Factor 1.4** en el sismo: incorpora R* en el denominador del espectro.
El espectro en ETABS usa Sa_elastico × g. El factor de escala = g/R*.
Después el combo multiplica por 1.4 → efecto total = 1.4×g/R*.

### Implementación en ETABS (8 combos base)
```
C1_1.4D:       PP×1.4 + TERP×1.4 + TERT×1.4
C2_1.2D+1.6L:  PP×1.2 + TERP×1.2 + TERT×1.2 + SCP×1.6 + SCT×0.5
C3_1.2D+L+SEx: PP×1.2 + TERP×1.2 + SCP×1.0 + SEx×1.4
C4_1.2D+L+SEy: PP×1.2 + TERP×1.2 + SCP×1.0 + SEy×1.4
C5_0.9D+SEx:   PP×0.9 + TERP×0.9 + SEx×1.4
C6_0.9D+SEy:   PP×0.9 + TERP×0.9 + SEy×1.4
C7_0.9D-SEx:   PP×0.9 + TERP×0.9 + SEx×(-1.4)
C8_0.9D-SEy:   PP×0.9 + TERP×0.9 + SEy×(-1.4)
```

---

## Verificaciones de Deformación (NCh433 art.6.3.5)

### Condición 1 (drift en CM)
```
δ_CM/h ≤ 0.002    (para cada entrepiso)
```
Aplica al punto de aplicación de las fuerzas sísmicas (CM).

### Condición 2 (drift en puntos extremos)
```
δ_cualquier_punto/h ≤ 0.001
```
El punto extremo del diafragma puede tener mayor desplazamiento por torsión.

### Conversión en ETABS
- ETABS reporta drift como δ/h (adimensional) en las tablas Story Drifts
- Verificar para SEx y SEy por separado
- Condición 1: CM drift < 0.002
- Condición 2: extremos < 0.001

---

## Torsión Accidental (NCh433 art.6.3.4)

### Método dinámico — 3 casos del taller

**Caso a)** — Eccentricidad accidental 5%
- Desplazar el CM en ±5% de la dimensión perpendicular
- En ETABS: Eccentricity Override = 0.05 por diafragma
- ea_x = 0.05 × Lx = 0.05 × 38.505 = 1.925 m (para sismo Y)
- ea_y = 0.05 × Ly = 0.05 × 13.821 = 0.691 m (para sismo X)

**Caso b) Forma 1** — Shift físico del CM
- Crear RS cases con CM desplazado ±ea en cada dirección
- 4 RS cases adicionales (MANUAL en ETABS)

**Caso b) Forma 2** — Momentos torsionales estáticos
- Aplicar momentos Mz = Qi × ea en cada piso
- Qi es el corte sísmico del piso i
- Implementado via load patterns TorX+, TorX-, TorY+, TorY-

---

## Masa Sísmica (mass source)

Según NCh433 art.5.2:
```
P = PP + 1.0×TERP + 0.25×SCP
```

En ETABS (Define > Mass Source):
- Element Self Mass: SI
- Load Pattern TERP: factor 1.0
- Load Pattern SCP: factor 0.25

### Verificación peso sísmico
Para un edificio de oficinas bien modelado:
```
W/área/piso ≈ 1 tonf/m²/piso    (objetivo de diseño)
```
Si sale muy diferente (< 0.7 o > 1.3), hay un error de modelación.

---

## Modos de Vibración Requeridos

NCh433 exige acumular **≥ 90% de masa participativa** en cada dirección (X e Y).

Para un edificio de 20 pisos con diafragma rígido:
- 3 GDL/piso × 20 pisos = 60 GDL totales
- Usar **60 modos** en el análisis modal
- Los primeros 2-3 modos suelen dominar en X e Y

### Superposición CQC (Complete Quadratic Combination)
```
E = √[Σᵢ Σⱼ ρᵢⱼ × Eᵢ × Eⱼ]

ρᵢⱼ = 8ξ² × (1+β)×β^(3/2) / [(1-β²)² + 4ξ²×β×(1+β)²]

donde β = ωⱼ/ωᵢ, ξ = 0.05
```

Para modos muy separados (β < 0.1): CQC ≈ SRSS.
