# ACTIVE SPEC — Fix Geometría Edificio 1

## Objetivo
Corregir config.py para que la geometría del Edificio 1 en ETABS coincida exactamente con los planos del enunciado (págs 2-7).

## Criterios de aceptación
1. Vista en planta de ETABS (piso tipo) coincide visualmente con enunciado_page2.png
2. Elevación eje C coincide con enunciado_page6.png (izquierda)
3. Elevación eje D coincide con enunciado_page6.png (derecha)
4. Elevación eje F coincide con enunciado_page7.png (izquierda)
5. Conteo de muros/vigas/losas es coherente con el plano

## Inputs
- `enunciado_page2.png` a `enunciado_page7.png` — planos de referencia
- `config.py` actual (commit 90773af)
- Tabla de coordenadas exactas en page5

## Constraints
- Solo modificar config.py
- Respetar nombres de sección: MHA30G30, MHA20G30, VI20x60G30, Losa15G30
- Regla espesores: ejes 1,3,4,5,7,12,13,14,16,17 = 30cm, resto = 20cm
- El shaft (ascensor) es 7.7m ancho × 2.945m alto, centrado en eje 10

## Problema conocido
- El shaft (2.945m en Y) excede la zona C-D (1.55m) — sus bordes caen fuera de la grilla
- Paredes verticales del shaft deberían estar en x=17.415 y x=25.115 (off-grid)
- Actualmente modeladas en ejes 10 y 11 (dentro del shaft, no en bordes)

## Qué no tocar
- Scripts 03_walls.py, 04_beams.py, 05_slabs.py — lógica correcta
- Parámetros sísmicos y de carga — ya validados
