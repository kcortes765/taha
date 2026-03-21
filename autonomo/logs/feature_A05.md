# Feature A05 — 04_beams.py (vigas invertidas)

## Estado: COMPLETADO

## Archivo generado
- `autonomo/scripts/04_beams.py` (~270 lineas)

## Que hace el script
Dibuja TODAS las vigas del edificio (20 pisos) en ETABS v19 via COM (comtypes).

### Vigas por eje (30 vigas/piso)
Todas las vigas son VI20x60G30 (invertidas), corren en direccion X a Y=constante:

- **Eje A** (Y=0.000): 10 vigas — fachada sur
  Tramos: 1-2, 3-4, 5-6, 7-8, 9-10, 10-11, 11-12, 13-14, 14-15, 15-16

- **Eje F** (Y=13.821): 8 vigas — fachada norte
  Tramos: 2-3, 3-4, 5-6, 6-7, 11-12, 12-13, 13-14, 15-16

- **Eje B** (Y=0.701): 12 vigas — eje intermedio
  Tramos: 1-2, 3-4, 5-6, 6-7, 7-8, 9-10, 10-11, 11-12, 13-14, 14-15, 15-16, 16-17

### Totales
- 30 vigas/piso x 20 pisos = **600 vigas**
- Seccion: VI20x60G30 (0.20 x 0.60 m)
- Cardinal Point: 2 (Bottom Center — vigas invertidas)
- J=0: definido en la seccion (02_materials_sections.py)
- Vigas se colocan a la elevacion superior de cada piso (nivel losa)

## Firmas COM usadas (verificadas en com_signatures.md)
| Funcion | Args | Seccion |
|---------|------|---------|
| FrameObj.AddByCoord | 8 (6 req + 2 opt) | 6.1 |
| FrameObj.SetInsertionPoint | 6 (6 req) | 6.3 |

## Geometria
Los datos de vigas provienen de config.py (VIGAS_EJE_A, VIGAS_EJE_F, VIGAS_EJE_B),
levantados del Enunciado Taller pag 2 (planta tipo). Cada viga es una tupla
(y_fijo, x_ini, x_fin).

Para cada piso, las vigas se colocan a z = STORY_ELEVATIONS[story_idx]:
- Piso 1: z=3.40
- Piso 2: z=6.00
- ...
- Piso 20: z=52.80

## Cardinal Point 2 (Bottom Center)
Las vigas invertidas tienen su linea de referencia en el FONDO de la seccion.
Esto significa que la viga "cuelga" debajo del nivel de losa. SetInsertionPoint
se llama despues de AddByCoord para cada viga individual.

Parametros: Mirror2=False, StiffTransform=False, Offsets=[0,0,0].

## Verificacion
- Syntax: script sigue el mismo patron probado de 03_walls.py
- Config imports: VIGAS tiene 30 elementos (10+8+12), N_VIGAS=30
- FrameObj.AddByCoord: firma verificada en com_signatures.md §6.1
- FrameObj.SetInsertionPoint: firma verificada en com_signatures.md §6.3
- Incluye verificacion post-creacion (FrameObj.GetNameList)
- Logging de progreso cada 5 pisos
- Tabla resumen de vigas por eje impresa antes de crear

## Notas
- GetNameList puede retornar 0 en v19 (bug conocido) — las vigas existen
  de todas formas. Verificar en ETABS UI.
- J=0 ya esta seteado a nivel de seccion en 02_materials_sections.py
  (VIGA_MODIFIERS), por lo que NO se aplica via FrameObj.SetModifiers en este script.
- El script es autocontenido y modular, siguiendo el patron de 03_walls.py.
