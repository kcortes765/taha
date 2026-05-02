# Resultados Esperados — Edificio 1 (20 pisos, muros HA)

> **Proyecto**: Taller ADSE UCN 1S-2026
> **Edificio**: 20 pisos de muros HA, Antofagasta
> **Script**: `autonomo/scripts/12_extract_results.py`
> **Nota**: Este documento contiene los valores esperados PRE-analisis.
>   Al ejecutar el script, se sobreescribe con los valores obtenidos.

---

## Datos del Edificio

| Parametro | Valor | Fuente |
|-----------|-------|--------|
| Pisos | 20 | Enunciado |
| H piso 1 | 3.40 m | Enunciado |
| H pisos 2-20 | 2.60 m | Enunciado |
| H total | 52.80 m | 3.40 + 19×2.60 |
| Area planta | 468.4 m2 | Huella real (no envolvente) |
| Area envolvente | 532.2 m2 | 38.505 × 13.821 |
| f'c | 30 MPa (G30) | Enunciado |
| fy | 420 MPa (A630-420H) | Enunciado |
| Muros | 20 cm y 30 cm | Enunciado |
| Vigas | 20/60 cm invertidas | Enunciado |
| Losas | 15 cm macizas | Enunciado |

## Parametros Sismicos (DS61 Tabla 12.3)

| Parametro | Valor | Fuente |
|-----------|-------|--------|
| Zona | 3 (Antofagasta) | NCh433 Tabla 6.2 |
| Ao/g | 0.40 | NCh433 Tabla 6.2 |
| Suelo | C | DS61 |
| S | 1.05 | DS61 Tabla 12.3 |
| To | 0.40 s | DS61 Tabla 12.3 |
| T' | 0.45 s | DS61 Tabla 12.3 |
| n | 1.40 | DS61 Tabla 12.3 |
| p | 1.60 | DS61 Tabla 12.3 |
| R | 7 | NCh433 Tabla 5.1, muros HA |
| Ro | 11 | NCh433 Tabla 5.1, muros HA |
| I | 1.0 | NCh433 Tabla 6.1, Cat II |

## 1. Resultados Modales — Valores Esperados

| Parametro | Esperado | Rango aceptable | Justificacion |
|-----------|----------|-----------------|---------------|
| T1 | 1.0–1.3 s | 0.5–2.5 s | Regla H/40 a H/50: 52.8/50=1.06, 52.8/40=1.32 |
| T2 | 0.3–0.5 s | — | Segundo modo translacional |
| T3 | 0.2–0.4 s | — | Primer modo torsional o tercer translacional |
| SumUX (30 modos) | > 90% | 90–100% | NCh433 Art. 6.3.6.2 |
| SumUY (30 modos) | > 90% | 90–100% | NCh433 Art. 6.3.6.2 |

### Coeficientes sismicos esperados

- **R\*(T1=1.0s)** = 1 + 1.0 / (0.10×0.40 + 1.0/11) = **8.0** (aprox)
- **R\*(T1=1.3s)** = 1 + 1.3 / (0.04 + 0.118) = **9.2** (aprox)
- **Cmin** = Ao×S/(6g) = 0.40×1.05/6 = **0.070**
- **Cmax** = 0.35×S×Ao/g = 0.35×1.05×0.40 = **0.147**

## 2. Drifts — Valores Esperados

| Parametro | Limite | Fuente |
|-----------|--------|--------|
| Drift CM (Condicion 1) | <= 0.002 | NCh433 Art. 5.9.2 |
| Drift max punto (Condicion 2) | <= 0.002 | NCh433 Art. 5.9 |

### Notas sobre el drift

- El pipeline usa espectro **elastico** (Sa/g, no reducido por R*)
- ETABS calcula desplazamientos elasticos bajo este espectro
- Para T1 >> To (este edificio), principio de igualdad de desplazamientos:
  δ_inelastico ≈ δ_elastico
- Por lo tanto, drift de ETABS puede compararse directamente contra 0.002
- Los pisos superiores (Story 15-20) suelen tener drift mas alto en edificios de muros
- Drift esperado: 0.0005-0.0015 (tipico para edificios chilenos de muros)

## 3. Corte Basal — Valores Esperados

| Parametro | Formula | Valor esperado |
|-----------|---------|----------------|
| Peso sismico W | PP + TERP + 0.25×SCP | ~9,368 tonf |
| Peso/area | W / (A × N) | ~1.0 tonf/m2 |
| Qmin | Cmin × W | ~656 tonf |
| Qmax | Cmax × W | ~1,377 tonf |

### Desglose peso esperado

- PP (hormigon armado): ~7,000-8,000 tonf (estructura)
- TERP (sobrecarga permanente): ~600-1,000 tonf (tabiques, terminaciones)
- 0.25×SCP (25% sobrecarga uso): ~400-600 tonf
- **Total esperado**: ~9,000-10,000 tonf

## 4. Centros de Masa y Rigidez

| Parametro | Esperado | Justificacion |
|-----------|----------|---------------|
| XCM | ~19-21 m | Aprox mitad de 38.505 m (planta irregular) |
| YCM | ~6.5-7.5 m | Aprox mitad de 13.821 m |
| XCR | ~19-21 m | Muros distribuidos simetricamente en X |
| YCR | ~6.5-7.5 m | Muros distribuidos simetricamente en Y |
| eX = |XCM-XCR| | < 1.0 m | Excentricidad natural |
| eY = |YCM-YCR| | < 0.5 m | Excentricidad natural |
| eaX (accidental) | 1.925 m | 5% × 38.505 m |
| eaY (accidental) | 0.691 m | 5% × 13.821 m |

## 5. Fuerzas por Piso

- **Distribucion**: En edificios de muros, la fuerza cortante es maxima en la base
  y disminuye hacia arriba (forma triangular invertida para el primer modo)
- **Cortante basal SDX**: ~500-1,400 tonf (entre Qmin y Qmax)
- **Momento volcante en base**: ~15,000-35,000 tonf-m (estimacion)

## 6. Muros de Borde — Identificacion

### Eje 1 (x = 0.0 m, borde izquierdo)
- Muro: Eje 1, A-C, espesor 30 cm
- Longitud: 6.446 m (de y=0.0 a y=6.446)
- **Critico** para sismo en Y (mayor brazo de palanca)

### Eje F (y = 13.821 m, borde superior)
- Multiples muros en ejes 3, 4, 5, 6, 7, 10, 11, 12, 13, 14, 15, 16 (D-F)
- Espesores: 20 cm y 30 cm segun eje
- **Criticos** para sismo en X

### Eje 17 (x = 38.505 m, borde derecho)
- Muro: Eje 17, A-C, espesor 30 cm
- Longitud: 6.446 m

## 7. Diagramas P-M — Referencia

Para la verificacion de muros por diagrama de interaccion:

1. **Demanda (Pu, Mu)**: Se obtiene del script para cada combo C1-C11
2. **Capacidad**: Se calcula con:
   - Tablas de Diseno Gerdau AZA (`docs/Tablas/Tabla Diseno de Muros.pdf`)
   - Section Designer de ETABS
   - Calculo manual (metodos del apunte `03b-Muros-Diseno-Corte-Flexion-Confinamiento.pdf`)

### Combos criticos para muros

| Combo | Tipo | Descripcion |
|-------|------|-------------|
| C4/C5 | Sismo X+ / X- | 1.2D + 1.0L + 1.4SX |
| C6/C7 | Sismo Y+ / Y- | 1.2D + 1.0L + 1.4SY |
| C8/C9 | Sismo X (min grav) | 0.9D + 1.4SX |
| C10/C11 | Sismo Y (min grav) | 0.9D + 1.4SY |

Los combos C8-C11 son criticos para **traccion** (Pu minimo con Mu maximo).
Los combos C4-C7 son criticos para **compresion + flexion** (Pu y Mu maximos).

---

## Archivos de Salida

Al ejecutar `python 12_extract_results.py`:

| Archivo | Contenido |
|---------|-----------|
| `results/modal_results.csv` | Periodos, participacion, tipo de modo |
| `results/story_drifts.csv` | Drift por piso, caso, direccion |
| `results/drift_envelope.csv` | Envolvente de drift max por piso |
| `results/base_reactions.csv` | Reacciones en base por caso |
| `results/cm_cr_per_story.csv` | CM y CR por piso |
| `results/story_forces.csv` | Corte y volcante por piso |
| `results/wall_forces_axis_1.csv` | Fuerzas muro eje 1 (si hay piers) |
| `results/wall_forces_axis_F.csv` | Fuerzas muro eje F (si hay piers) |
| `results/pm_pier_*.csv` | Demandas P-M por pier |
| `results/pm_global_reactions.csv` | Reacciones globales por combo |
