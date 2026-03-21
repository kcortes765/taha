# Edificio 1 — Geometría Completa (datos exactos del enunciado)

## Grilla de ejes

### Ejes numerados — posición X [metros desde origen]
| Eje | X (m) | | Eje | X (m) |
|-----|-------|-|-----|-------|
| 1 | 0.000 | | 10 | 21.665 |
| 2 | 3.125 | | 11 | 24.990 |
| 3 | 3.825 | | 12 | 26.315 |
| 4 | 9.295 | | 13 | 27.834 |
| 5 | 9.895 | | 14 | 32.435 |
| 6 | 15.465 | | 15 | 34.005 |
| 7 | 16.015 | | 16 | 37.130 |
| 8 | 18.565 | | 17 | 38.505 |
| 9 | 18.990 | | | |

**Lx = 38.505 m** (dimensión en X)

### Ejes letrados — posición Y [metros desde origen]
| Eje | Y (m) | Descripción |
|-----|-------|-------------|
| A | 0.000 | Borde inferior |
| B | 0.701 | Franja estrecha inferior |
| C | 6.446 | Eje central (muros importantes) |
| D | 7.996 | |
| E | 10.716 | |
| F | 13.821 | Borde superior |

**Ly = 13.821 m** (dimensión en Y)
**Área planta = 38.505 × 13.821 ≈ 532 m²**

---

## Pisos

| Piso | Altura (m) | Elevación acumulada (m) |
|------|------------|------------------------|
| 1 | 3.400 | 3.400 |
| 2 | 2.600 | 6.000 |
| 3 | 2.600 | 8.600 |
| 4 | 2.600 | 11.200 |
| 5 | 2.600 | 13.800 |
| 6 | 2.600 | 16.400 |
| 7 | 2.600 | 19.000 |
| 8 | 2.600 | 21.600 |
| 9 | 2.600 | 24.200 |
| 10 | 2.600 | 26.800 |
| 11 | 2.600 | 29.400 |
| 12 | 2.600 | 32.000 |
| 13 | 2.600 | 34.600 |
| 14 | 2.600 | 37.200 |
| 15 | 2.600 | 39.800 |
| 16 | 2.600 | 42.400 |
| 17 | 2.600 | 45.000 |
| 18 | 2.600 | 47.600 |
| 19 | 2.600 | 50.200 |
| 20 | 2.600 | **52.800** |

---

## Muros Dirección Y (planos paralelos al plano XZ)
Eje fijo = X, longitud en Y

| Eje | X (m) | Y_ini (m) | Y_fin (m) | Espesor | Sección |
|-----|--------|-----------|-----------|---------|---------|
| 1 | 0.000 | A=0.000 | C=6.446 | 30 cm | MHA30G30 |
| 2 | 3.125 | A=0.000 | B=0.701 | 20 cm | MHA20G30 |
| 2 | 3.125 | C=6.446 | F=13.821 | 20 cm | MHA20G30 |
| 3 | 3.825 | A=0.000 | B=0.701 | 30 cm | MHA30G30 |
| 3 | 3.825 | C=6.446 | F=13.821 | 30 cm | MHA30G30 |
| 4 | 9.295 | A=0.000 | B=0.701 | 30 cm | MHA30G30 |
| 4 | 9.295 | C=6.446 | F=13.821 | 30 cm | MHA30G30 |
| 5 | 9.895 | A=0.000 | B=0.701 | 30 cm | MHA30G30 |
| 5 | 9.895 | C=6.446 | F=13.821 | 30 cm | MHA30G30 |
| 6 | 15.465 | C=6.446 | F=13.821 | 20 cm | MHA20G30 |
| 7 | 16.015 | C=6.446 | F=13.821 | 30 cm | MHA30G30 |
| 8 | 18.565 | A=0.000 | B=0.701 | 20 cm | MHA20G30 |
| 9 | 18.990 | A=0.000 | B=0.701 | 20 cm | MHA20G30 |
| 10 | 21.665 | A=0.000 | B=0.701 | 20 cm | MHA20G30 |
| 11 | 24.990 | C=6.446 | F=13.821 | 20 cm | MHA20G30 |
| 12 | 26.315 | A=0.000 | B=0.701 | 30 cm | MHA30G30 |
| 12 | 26.315 | C=6.446 | F=13.821 | 30 cm | MHA30G30 |
| 13 | 27.834 | A=0.000 | B=0.701 | 30 cm | MHA30G30 |
| 13 | 27.834 | C=6.446 | F=13.821 | 30 cm | MHA30G30 |
| 14 | 32.435 | A=0.000 | B=0.701 | 30 cm | MHA30G30 |
| 14 | 32.435 | C=6.446 | F=13.821 | 30 cm | MHA30G30 |
| 15 | 34.005 | C=6.446 | F=13.821 | 20 cm | MHA20G30 |
| 16 | 37.130 | A=0.000 | B=0.701 | 30 cm | MHA30G30 |
| 16 | 37.130 | C=6.446 | F=13.821 | 30 cm | MHA30G30 |
| 17 | 38.505 | A=0.000 | C=6.446 | 30 cm | MHA30G30 |

**Total por piso: ~24 muros dir Y × 20 pisos ≈ 480 muros**

---

## Muros Dirección X (planos paralelos al plano YZ)
Eje fijo = Y, longitud en X

| Eje | Y (m) | X_ini (m) | X_fin (m) | Espesor | Sección |
|-----|--------|-----------|-----------|---------|---------|
| A | 0.000 | eje2=3.125 | eje3=3.825 | 20 cm | MHA20G30 |
| A | 0.000 | eje4=9.295 | eje5=9.895 | 20 cm | MHA20G30 |
| A | 0.000 | eje8=18.565 | eje9=18.990 | 20 cm | MHA20G30 |
| A | 0.000 | eje12=26.315 | eje13=27.834 | 20 cm | MHA20G30 |
| A | 0.000 | eje16=37.130 | eje17=38.505 | 20 cm | MHA20G30 |
| C | 6.446 | eje3=3.825 | eje4=9.295 | 30 cm | MHA30G30 |
| C | 6.446 | eje5=9.895 | eje6=15.465 | 30 cm | MHA30G30 |
| C | 6.446 | eje10=21.665 | eje11=24.990 | 30 cm | MHA30G30 |
| C | 6.446 | eje11=24.990 | eje12=26.315 | 30 cm | MHA30G30 |
| C | 6.446 | eje13=27.834 | eje14=32.435 | 30 cm | MHA30G30 |
| C | 6.446 | eje1=0.000 | eje2=3.125 | 20 cm | MHA20G30 |
| C | 6.446 | eje7=16.015 | eje8=18.565 | 20 cm | MHA20G30 |
| C | 6.446 | eje14=32.435 | eje15=34.005 | 20 cm | MHA20G30 |
| C | 6.446 | eje15=34.005 | eje16=37.130 | 20 cm | MHA20G30 |
| C | 6.446 | eje16=37.130 | eje17=38.505 | 20 cm | MHA20G30 |
| D | 7.996 | eje2=3.125 | eje3=3.825 | 20 cm | MHA20G30 |
| D | 7.996 | eje4=9.295 | eje5=9.895 | 20 cm | MHA20G30 |
| D | 7.996 | eje12=26.315 | eje13=27.834 | 20 cm | MHA20G30 |
| E | 10.716 | eje2=3.125 | eje3=3.825 | 20 cm | MHA20G30 |
| E | 10.716 | eje4=9.295 | eje5=9.895 | 20 cm | MHA20G30 |
| E | 10.716 | eje10=21.665 | eje11=24.990 | 20 cm | MHA20G30 |
| E | 10.716 | eje14=32.435 | eje15=34.005 | 20 cm | MHA20G30 |
| F | 13.821 | eje2=3.125 | eje3=3.825 | 20 cm | MHA20G30 |
| F | 13.821 | eje4=9.295 | eje5=9.895 | 20 cm | MHA20G30 |
| F | 13.821 | eje14=32.435 | eje15=34.005 | 20 cm | MHA20G30 |
| F | 13.821 | eje16=37.130 | eje17=38.505 | 20 cm | MHA20G30 |

**Total por piso: ~24 muros dir X × 20 pisos ≈ 480 muros**
**Total muros edificio: ~960**

---

## Vigas (VI20×60G30)
Todas en dirección X (horizontal en planta), en los niveles de losa.

### Eje A (Y=0.000)
| X_ini (m) | X_fin (m) |
|-----------|-----------|
| 0.000 (eje1) | 3.125 (eje2) |
| 3.825 (eje3) | 9.295 (eje4) |
| 9.895 (eje5) | 15.465 (eje6) |
| 16.015 (eje7) | 18.565 (eje8) |
| 18.990 (eje9) | 21.665 (eje10) |
| 21.665 (eje10) | 24.990 (eje11) |
| 24.990 (eje11) | 26.315 (eje12) |
| 27.834 (eje13) | 32.435 (eje14) |
| 32.435 (eje14) | 34.005 (eje15) |
| 34.005 (eje15) | 37.130 (eje16) |

### Eje F (Y=13.821)
| X_ini (m) | X_fin (m) |
|-----------|-----------|
| 3.125 (eje2) | 3.825 (eje3) |
| 3.825 (eje3) | 9.295 (eje4) |
| 9.895 (eje5) | 15.465 (eje6) |
| 15.465 (eje6) | 16.015 (eje7) |
| 24.990 (eje11) | 26.315 (eje12) |
| 26.315 (eje12) | 27.834 (eje13) |
| 27.834 (eje13) | 32.435 (eje14) |
| 34.005 (eje15) | 37.130 (eje16) |

### Ejes intermedios (vigas de acoplamiento en Y=0.701 eje B)
| X_ini (m) | X_fin (m) |
|-----------|-----------|
| 0.000 | 3.125 |
| 3.825 | 9.295 |
| 9.895 | 15.465 |
| 15.465 | 16.015 |
| 16.015 | 18.565 |
| 18.990 | 21.665 |
| 21.665 | 24.990 |
| 24.990 | 26.315 |
| 27.834 | 32.435 |
| 32.435 | 34.005 |
| 34.005 | 37.130 |
| 37.130 | 38.505 |

**Total por piso: ~30 vigas × 20 pisos ≈ 600 vigas**
*(Nota: el pipeline usa ~20 vigas/piso = 400 total; el número exacto depende de las vigas visibles en los planos)*

---

## Losas (Losa15G30)
Paneles rectangulares cubriendo toda la planta:

**Por franja (5 franjas en Y, 7 paneles en X = 35 paneles/piso)**

| Franja Y | Y_ini | Y_fin | N° paneles X |
|----------|-------|-------|--------------|
| A-B | 0.000 | 0.701 | 7 |
| B-C | 0.701 | 6.446 | 7 |
| C-D | 6.446 | 7.996 | 7 |
| D-E | 7.996 | 10.716 | 7 |
| E-F | 10.716 | 13.821 | 7 |

**Paneles X para cada franja:**
1. eje1–eje3: 0.000 → 3.825
2. eje3–eje5: 3.825 → 9.895
3. eje5–eje7: 9.895 → 16.015
4. eje7–eje10: 16.015 → 21.665
5. eje10–eje13: 21.665 → 27.834
6. eje13–eje15: 27.834 → 34.005
7. eje15–eje17: 34.005 → 38.505

**Total: 35 paneles/piso × 20 pisos = 700 losas**

---

## Parámetros de torsión accidental
```
Lx = 38.505 m   (dimensión en X)
Ly = 13.821 m   (dimensión en Y)

ea_X = 0.05 × Ly = 0.05 × 13.821 = 0.691 m  (para sismo en X)
ea_Y = 0.05 × Lx = 0.05 × 38.505 = 1.925 m  (para sismo en Y)

CM_X ≈ 19.25 m  (centro geométrico aproximado)
CM_Y ≈ 6.91 m
```

---

## Longitudes de muros claves (para diseño)

### Muros a diseñar (piso 1)

**Muro eje 5 (rectangular)**: eje 5, entre A y B
- Longitud: 0.701 m (entre Y=A y Y=B)
- Espesor: 30 cm
- Sección: rectangular simple

**Muro eje 4 (en T)**: eje 4, entre A-B + eje C entre 3-4
- Alma vertical (dir Y): x=9.295m, entre A(0.000) y B(0.701) → lw=0.701m
- Ala horizontal (dir X): y=6.446m, entre eje3(3.825) y eje4(9.295) → lf=5.47m
- Espesor alma: 30 cm, espesor ala: 30 cm
- Forma T → requiere diseño bidireccional

*(Nota: los muros reales a diseñar pueden variar; verificar con el enunciado impreso)*
