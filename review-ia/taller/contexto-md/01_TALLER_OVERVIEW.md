# TALLER ADSE 2026 — Overview Completo

## Datos del Ramo
- **Ramo**: DAIC 00904 — Análisis y Diseño Sísmico de Edificios
- **Universidad**: UCN, Ingeniería Civil, IX semestre, 1S-2026
- **Profesor**: Juan Music Tomicic (jmusic@ucn.cl)
- **Ayudantes taller**: Roberto Cortés / Ignacio Huerta
- **Horario cátedra**: Lu+Ma bloque C (11:40–13:10), sala Y3-101
- **Horario taller**: Ma bloques E+F (16:15–19:30), sala Y3-101

## Evaluación

```
NF = 0.7×NC + 0.3×NTaller
NC = 0.20×C1 + 0.40×C2 + 0.40×C3
```

**⚠️ Condición**: NC ≥ 4.0 Y NTaller ≥ 4.0 (independientes)

| Evaluación | Fecha | Contenido |
|------------|-------|-----------|
| C1 | Mar 5 mayo | Sismología, normativa, suelos |
| C2 = Expo1 | Mar 26 mayo | Análisis sísmico |
| C3 | Mar 30 junio | Diseño muros + marcos |
| Expo2 | 16 junio | Avance diseño |
| Expo3 | 7 julio | Entrega final |

Asistencia 100% obligatoria al taller.

---

## Edificio 1 — Muros HA (20 pisos)

**Emplazamiento**: Antofagasta → Zona 3 (Ao = 0.4g), Suelo C, Categoría II (Oficinas, I=1.0)

### Geometría
- **Planta**: 38.505 m × 13.821 m ≈ 532 m²
- **Pisos**: 20 (Piso1: h=3.4m, Pisos2-20: h=2.6m)
- **H total**: 3.4 + 19×2.6 = **52.8 m**
- **Grilla**: 17 ejes numerados (dir X) × 6 ejes letrados A-F (dir Y)
- **Sistema resistente**: muros de HA + vigas de acoplamiento + losas

### Materiales
| Material | Especificación | f (kgf/cm²) | f (MPa) |
|----------|---------------|-------------|---------|
| Hormigón | G30 | f'c = 300 | 30 |
| Acero | A630-420H | fy = 4200 | 420 |

- Ec = 4700√30 = 25742 MPa ≈ 257420 kgf/cm²
- γ_HA = 2.5 tonf/m³
- g = 9.81 m/s²

### Secciones
| Elemento | Sección | Nombre ETABS |
|----------|---------|--------------|
| Vigas (invertidas) | 20×60 cm | VI20x60G30 |
| Muros principales | e=30 cm | MHA30G30 |
| Muros secundarios | e=20 cm | MHA20G30 |
| Losas | e=15 cm | Losa15G30 |

### Muros e=30cm
- **Dir Y** (planos verticales): ejes **1, 3, 4, 5, 7, 12, 13, 14, 16, 17**
- **Dir X** (horizontales): eje **C** entre ejes 3-6 y 10-14

### Muros e=20cm
- Todos los demás muros no listados arriba

### Cargas
| Tipo | Patrón | Intensidad |
|------|--------|------------|
| Peso propio | PP (Dead) | Automático (selfweight) |
| SC piso (oficinas) | SCP (Live) | 250 kgf/m² |
| SC pasillos | SCP (Live) | 500 kgf/m² |
| SC techo | SCT (Roof Live) | 100 kgf/m² |
| Terminaciones piso | TERP (Super Dead) | 140 kgf/m² |
| Terminaciones techo | TERT (Super Dead) | 100 kgf/m² |

### Modificadores de rigidez (práctica chilena)
- **Vigas**: J=0 (inercia torsional nula)
- **Losas**: f11=f22=f12=0.25 (inercia reducida al 25%)
- **Muros**: sin modificadores (rigidez completa)

---

## Edificio 2 — Marcos especiales HA (5 pisos)

**Emplazamiento**: Antofagasta → Zona 3, Suelo C, Categoría II

### Geometría
- **Planta**: 32.5m × 32.5m (5 vanos de 6.5m en ambas direcciones)
- **Pisos**: 5 (Piso1: h=3.5m, Pisos2-5: h=3.0m)
- **H total**: 3.5 + 4×3.0 = **15.5 m**
- **Sistema resistente**: marcos especiales HA

### Materiales
| Material | Especificación | f'c (MPa) |
|----------|---------------|-----------|
| Hormigón | G25 | 25 |
| Acero | A630-420H | fy=420 MPa |

- Ec = 4700√25 = 23500 MPa

### Secciones por pisos
| Pisos | Columnas | Vigas | Losa |
|-------|----------|-------|------|
| 1-2 | 70×70 cm | 50×70 cm | 17 cm |
| 3-5 | 65×65 cm | 45×70 cm | 17 cm |

- **Cachos rígidos**: factor 0.75 (automático en ETABS)

### Cargas Ed.2
| Tipo | Intensidad |
|------|------------|
| SC piso | 300 kgf/m² |
| SC techo | 100 kgf/m² |
| Terminaciones piso | 140 kgf/m² |
| Terminaciones techo | 100 kgf/m² |

---

## Entregables del Taller

### Parte 1 — Análisis sísmico (ambos edificios)
1. Peso sísmico W (objetivo: ~1 tonf/m²/piso)
2. Densidad de muros (Aw/Pf y Aw/A_acumulada)
3. Centros de masa (CM) y rigidez (CR) por piso
4. Periodos y modos (≥90% masa participativa en X e Y)
5. Corte basal verificado (Qmín ≤ Q ≤ Qmáx)
6. Espectro de diseño con R*
7. Deformaciones (drift): 6 casos de análisis

### Los 6 casos de análisis del taller
| Caso | Diafragma | Torsión | Método |
|------|-----------|---------|--------|
| 1 | Rígido | a) Ecc 5% (NCh433 art.6.3.4) | ETABS: eccentricity override |
| 2 | Rígido | b) Forma 1 (shift CM ±5%) | Manual en ETABS |
| 3 | Rígido | b) Forma 2 (momentos Mz) | Scripts Python + ETABS |
| 4 | Semi-rígido | a) Ecc 5% | Modelo sin diafragma |
| 5 | Semi-rígido | b) Forma 1 | Manual |
| 6 | Semi-rígido | b) Forma 2 | Scripts |

### Parte 2 — Diseño estructural Ed.1 (muros)
- **Muro eje 5** (rectangular, 30cm): diseño completo piso 1
  - Corte, flexión compuesta, verificación curvatura, confinamiento
- **Muro eje 4** (sección T, 30cm): diseño completo piso 1
  - Diseño bidireccional, sección compuesta

### Parte 2 — Diseño estructural Ed.2 (marcos)
- **Vigas marco eje A**: diseño longitudinal y transversal (Mpr)
- **Columnas marco eje A**: diseño biaxial, zona crítica, confinamiento
- Verificar columna fuerte–viga débil: ΣMnc ≥ 1.2×ΣMnb

---

## Flujo de trabajo recomendado

```
1. Modelar Ed.1 en ETABS (pipeline Python automático)
   ↓
2. Verificar geometría 3D visualmente
   ↓
3. Definir espectro + mass source (manual si API falla)
   ↓
4. Correr análisis
   ↓
5. Extraer: periodos, CM/CR, peso, corte basal, drift
   ↓
6. Calcular R* = R*(Ro=11, T*) → re-escalar → re-analizar
   ↓
7. Diseño muros eje 4 y 5 (Section Designer o manual)
   ↓
8. Modelar Ed.2 manualmente en ETABS
   ↓
9. Diseño marcos (vigas + columnas + nudo)
```
