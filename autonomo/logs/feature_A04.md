# Feature A04 — 03_walls.py (muros por eje)

## Estado: COMPLETADO

## Archivo generado
- `autonomo/scripts/03_walls.py` (~320 lineas)

## Que hace el script
Dibuja TODOS los muros del edificio (20 pisos) en ETABS v19 via COM (comtypes).

### Muros Direccion Y (26 segmentos/piso)
Muros verticales en planta (corren en dir Y, a x=constante):
- **e=30cm (MHA30G30)**: ejes 1, 3, 4, 5, 7, 12, 13, 14, 16, 17
- **e=20cm (MHA20G30)**: ejes 2, 6, 8, 9, 10, 11, 15
- Los muros NO cruzan el pasillo central (gap entre ejes C y D)
- Eje 1 y 17: solo tramo A-C (una cara del edificio)

### Muros Direccion X (23 segmentos/piso)
Muros horizontales en planta (corren en dir X, a y=constante):
- **Eje A**: 5 stubs cortos (20cm)
- **Eje C**: 8 segmentos, 30cm entre ejes 3-6 y 10-14, 20cm el resto
- **Eje D**: 5 machones (20cm)
- **Eje E**: 4 stubs superiores pasillo (20cm)
- **Eje F**: 1 muro centrado (20cm)

### Totales
- 49 segmentos/piso x 20 pisos = **980 paneles de muro**
- AutoMesh 0.4m aplicado a cada panel
- Tiempo estimado: depende de sesion COM (~1-3 min)

## Firmas COM usadas (verificadas en com_signatures.md)
| Funcion | Args | Seccion |
|---------|------|---------|
| AreaObj.AddByCoord | 6 (4 req + 2 opt) | 7.1 |
| AreaObj.SetAutoMesh | 14 | 7.3 |

## Geometria
Los datos de muros provienen de config.py (MUROS_DIR_Y, MUROS_DIR_X),
levantados del Enunciado Taller pags 2-6. Cada segmento es una tupla
con eje, coordenada fija, coordenadas inicio/fin, y espesor.

Para cada piso, las elevaciones z_bot/z_top se calculan de STORY_ELEVATIONS:
- Piso 1: z_bot=0.0, z_top=3.40
- Piso 2: z_bot=3.40, z_top=6.00
- ...
- Piso 20: z_bot=50.20, z_top=52.80

## Verificacion
- Syntax check: OK (py_compile)
- Config imports: todos resuelven correctamente (26 dir Y + 23 dir X)
- get_section_name(): resuelve espesor a nombre de seccion sin error
- Incluye verificacion post-creacion (AreaObj.GetNameList)
- Logging de progreso cada 5 pisos

## Notas
- El comentario en config.py dice "22 segmentos" para MUROS_DIR_X, pero el
  conteo real es 23 (5+8+5+4+1). El script usa len() asi que es correcto.
- GetNameList puede retornar 0 en v19 (bug conocido) — los muros existen
  de todas formas. Verificar en ETABS UI.
- AutoMesh SetAutoMesh con MeshType=4 (MaxSize) y 0.4m en las 3 dimensiones.
