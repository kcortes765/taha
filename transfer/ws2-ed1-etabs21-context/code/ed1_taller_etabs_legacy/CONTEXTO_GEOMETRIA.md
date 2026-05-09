# Contexto: Fix Geometría Edificio 1 — Pipeline ETABS OAPI

## Tu tarea
Revisar y corregir la geometría del Edificio 1 (20 pisos, muros de HA) definida
en `config.py`. La geometría se genera automáticamente via Python + ETABS COM API.
El modelo se está creando pero la disposición de elementos parece incorrecta vs el enunciado.

**Solo debes modificar `config.py`** — los scripts de creación (03, 04, 05) son correctos.

---

## Contexto del proyecto

- **Ramo**: Análisis y Diseño Sísmico de Edificios, UCN, Chile, 2026
- **Edificio 1**: 20 pisos, sistema de muros de hormigón armado
- **Software**: ETABS 19 (CSi), controlado via Python usando COM API (comtypes)
- **Objetivo**: Generar modelo estructural completo automáticamente para análisis sísmico

---

## Descripción del Edificio 1 (del enunciado del taller)

### Planta tipo
- Dimensiones envolvente: ~38.5m (dir X) × ~13.8m (dir Y)
- 17 ejes numéricos en dirección X (ejes 1 a 17)
- 6 ejes con letras en dirección Y (ejes A a F)
- La planta NO es un rectángulo lleno — hay una zona tipo "L" o con retranqueos
- Existe un shaft de ascensor (vacío) en la zona central, aproximadamente entre ejes 9-11 en X y C-D en Y

### Pisos
- 20 pisos totales
- Piso 1: H = 3.4 m
- Pisos 2–20: H = 2.6 m
- H total = 3.4 + 19×2.6 = 52.8 m

### Materiales
- Hormigón G30 (f'c = 300 kgf/cm² = 30 MPa)
- Acero A630-420H (fy = 4200 kgf/cm² = 420 MPa)

### Elementos estructurales
| Elemento | Nombre en ETABS | Dimensión |
|----------|----------------|-----------|
| Muro 30cm | MHA30G30 | e=0.30m |
| Muro 20cm | MHA20G30 | e=0.20m |
| Viga invertida | VI20x60G30 | b=0.20m, h=0.60m |
| Losa | Losa15G30 | e=0.15m |

### Convención de ejes (del plano)
- **Ejes numéricos (1–17)**: posición en X (dirección horizontal del edificio, la más larga ~38.5m)
- **Ejes letrados (A–F)**: posición en Y (dirección transversal ~13.8m)
- Eje A = Y mínimo (fachada sur), Eje F = Y máximo (fachada norte)
- Los muros de mayor espesor (30cm) están en ejes: 1, 3, 4, 5, 7, 12, 13, 14, 16, 17

---

## Coordenadas de grilla actuales en config.py

```python
GRID_X = {
    '1':  0.000,   '2':  3.125,   '3':  3.825,   '4':  9.295,
    '5':  9.895,   '6':  15.465,  '7':  16.015,  '8':  18.565,
    '9':  18.990,  '10': 21.665,  '11': 24.990,  '12': 26.315,
    '13': 27.834,  '14': 32.435,  '15': 34.005,  '16': 37.130,
    '17': 38.505,
}

GRID_Y = {
    'A': 0.000,   'B': 0.701,   'C': 6.446,
    'D': 7.996,   'E': 10.716,  'F': 13.821,
}
```

### Observación importante sobre la grilla
- A–B: franja muy angosta (0.701m) — zona de vigas de acoplamiento en fachada sur
- B–C: franja amplia (~5.7m) — zona interior sur
- C–D: franja angosta (~1.55m) — zona del shaft/ascensor
- D–F: franja amplia (~5.8m) — zona interior norte
- Los ejes 1–2 y 16–17 son franjas angostas (~1.2m y ~1.4m) en los extremos

---

## Descripción de muros actuales en config.py

### Muros dirección Y (planos verticales paralelos al eje Y — van "de norte a sur")
Se definen como: `(nombre_eje, x_coord, y_inicio, y_fin, espesor)`

```
Eje 1  (x=0.000,   e=30cm): A → C  (cubre A–B–C, longitud ~6.4m)
Eje 2  (x=3.125,   e=20cm): A → B  y  C → F  (dos tramos separados)
Eje 3  (x=3.825,   e=30cm): A → B  y  C → F
Eje 4  (x=9.295,   e=30cm): A → B  y  C → F
Eje 5  (x=9.895,   e=30cm): A → B  y  C → F
Eje 6  (x=15.465,  e=20cm): C → F
Eje 7  (x=16.015,  e=30cm): C → F
Eje 8  (x=18.565,  e=20cm): A → B
Eje 9  (x=18.990,  e=20cm): A → B
Eje 10 (x=21.665,  e=20cm): A → B
Eje 11 (x=24.990,  e=20cm): C → F
Eje 12 (x=26.315,  e=30cm): A → B  y  C → F
Eje 13 (x=27.834,  e=30cm): A → B  y  C → F
Eje 14 (x=32.435,  e=30cm): A → B  y  C → F
Eje 15 (x=34.005,  e=20cm): C → F
Eje 16 (x=37.130,  e=30cm): A → B  y  C → F
Eje 17 (x=38.505,  e=30cm): A → C  (cubre A–B–C)
```

### Muros dirección X (planos horizontales paralelos al eje X — van "de este a oeste")
Se definen como: `(nombre_eje, y_coord, x_inicio, x_fin, espesor)`

```
Eje A (y=0.000,   e=20cm): varios tramos: 2–3, 4–5, 8–9, 12–13, 16–17
Eje C (y=6.446):
  e=20cm: 1→3, 7→8, 14→15, 15→16, 16→17
  e=30cm: 3→4, 5→6, 10→11, 11→12, 13→14
Eje D (y=7.996,   e=20cm): 2–3, 4–5, 12–13, 14–15  (muros cortos/stubs)
Eje E (y=10.716,  e=20cm): 2–3, 4–5, 10–11, 14–15
Eje F (y=13.821,  e=20cm): 2–3, 4–5, 14–15, 16–17
```

---

## Paneles de losa actuales en config.py

### Piso tipo (19 pisos): 7 paneles
```
Panel 1: ejes 3–6  en X,  A–B  en Y  → x:[3.825–15.465], y:[0.000–0.701]
Panel 2: ejes 7–8  en X,  A–B  en Y  → x:[16.015–18.565], y:[0.000–0.701]
Panel 3: ejes 9–16 en X,  A–B  en Y  → x:[18.990–37.130], y:[0.000–0.701]
Panel 4: ejes 3–17 en X,  B–C  en Y  → x:[3.825–38.505], y:[0.701–6.446]
Panel 5: ejes 3–9  en X,  C–D  en Y  → x:[3.825–18.990], y:[6.446–7.996]
Panel 6: ejes 11–17 en X, C–D  en Y  → x:[24.990–38.505], y:[6.446–7.996]
Panel 7: ejes 3–17 en X,  D–F  en Y  → x:[3.825–38.505], y:[7.996–13.821]
```
→ Área total piso tipo ≈ 468.4 m²
→ Centro de masa ≈ (21.12, 6.93) m

### Techo (piso 20): 5 paneles
```
Panel 1: ejes 3–16 en X,  A–B  en Y
Panel 2: ejes 3–17 en X,  B–C  en Y
Panel 3: ejes 3–9  en X,  C–D  en Y
Panel 4: ejes 11–17 en X, C–D  en Y
Panel 5: ejes 3–17 en X,  D–F  en Y
```

### Nota: zonas sin losa
- Franja 1–3 en A–B: NO tiene losa (zona de escalera/acceso sur)
- Shaft ascensor: zona C–D entre ejes 9–11: NO tiene losa

---

## Vigas actuales en config.py

Todas son VI20/60G30. Se definen como `(y_coord, x_inicio, x_fin)`.

```
Eje A (y=0): 1–2, 3–4, 5–6, 7–8, 9–10, 10–11, 11–12, 13–14, 14–15, 15–16
Eje F (y=13.821): 2–3, 3–4, 5–6, 6–7, 11–12, 12–13, 13–14, 15–16
Interiores eje B (y=0.701): 1–2, 3–4, 5–6, 6–7, 7–8, 9–10, 10–11, 11–12, 13–14, 14–15, 15–16, 16–17
```

---

## Cómo funciona el pipeline (solo para contexto)

Los scripts Python se conectan a ETABS 19 via COM API (comtypes). El flujo es:
1. `01_init_model.py` — inicializa el modelo, define pisos y grilla
2. `02_materials_sections.py` — define materiales y secciones
3. `03_walls.py` — itera los 20 pisos, dibuja todos los muros con `AreaObj.AddByCoord`
4. `04_beams.py` — itera los 20 pisos, dibuja todas las vigas con `FrameObj.AddByCoord`
5. `05_slabs.py` — itera los 20 pisos, dibuja losas con `AreaObj.AddByCoord`

### API de creación de muros (vertical, dir Y)
```python
m.AreaObj.AddByCoord(
    4,                         # 4 puntos
    [x, x, x, x],             # X (constante = posición del muro)
    [y0, y1, y1, y0],         # Y (inicio y fin del muro)
    [z_bot, z_bot, z_top, z_top],  # Z (base y tope del piso)
    '', seccion, '', 'Global'
)
```

### API de creación de muros (horizontal, dir X)
```python
m.AreaObj.AddByCoord(
    4,
    [x0, x1, x1, x0],         # X (inicio y fin del muro)
    [y, y, y, y],              # Y (constante = posición del muro)
    [z_bot, z_bot, z_top, z_top],
    '', seccion, '', 'Global'
)
```

### API de creación de losas (horizontal, en planta)
```python
m.AreaObj.AddByCoord(
    4,
    [x1, x2, x2, x1],         # X
    [y1, y1, y2, y2],         # Y
    [z, z, z, z],              # Z (elevación del piso)
    '', LOSA_NAME, '', 'Global'
)
```

---

## Resultado actual y problema

El modelo se crea exitosamente:
- 1040 muros (52/piso × 20 pisos)
- 600 vigas (30/piso × 20 pisos)
- 138 losas (7×19 + 5 techo)

Sin embargo, la vista en planta muestra que la disposición NO corresponde al plano del enunciado. La geometría parece incorrecta en la distribución de muros y/o losas.

---

## Referencia principal

El plano del edificio está en:
`docs/Enunciado Taller.pdf` — páginas 2 a 7

Contenido por página:
- Pág 2: Planta tipo (vista superior con muros en rojo, vigas en azul, losas en gris)
- Pág 3: Longitudes de muros por eje (dimensiones exactas)
- Pág 4: Planta de techo
- Pág 5-6: Elevaciones (cortes A-A, B-B)
- Pág 7: Elevaciones ejes F y demás

**ADJUNTAR ESE PDF junto con este documento y los 4 scripts .py.**

---

## Tu tarea concreta

1. **Leer el plano** (Enunciado págs 2–7) y verificar cada elemento:
   - ¿Los ejes `GRID_X` y `GRID_Y` tienen las coordenadas correctas?
   - ¿`MUROS_DIR_Y` cubre los tramos correctos? ¿faltan muros? ¿hay muros de más?
   - ¿`MUROS_DIR_X` es correcto?
   - ¿`SLAB_PANELS_FLOOR` cubre la huella correcta?
   - ¿Las vigas están donde deben?

2. **Entregar `config.py` corregido** con comentarios explicando cada cambio.

3. **No modificar** `03_walls.py`, `04_beams.py`, `05_slabs.py` — la lógica de creación es correcta.

---

## Archivos a adjuntar a esta IA

```
1. ESTE ARCHIVO (CONTEXTO_GEOMETRIA.md)
2. config.py
3. 03_walls.py
4. 04_beams.py
5. 05_slabs.py
6. docs/Enunciado Taller.pdf  ← referencia principal (adjuntar completo)
```
