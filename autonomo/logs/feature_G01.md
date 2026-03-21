# Feature G01 — Espectro Elástico Completo + Archivo ETABS

## Estado: COMPLETADA

## Resumen
Generada la tabla completa del espectro elástico NCh433/DS61 para Zona 3, Suelo C
y el archivo .txt listo para importar en ETABS.

## Parámetros usados (DS61 Tabla 12.3)
- Ao = 0.4g, S = 1.05, To = 0.40s, p = 1.60
- Fórmula: α(T) = [1 + 4.5·(T/To)^p] / [1 + (T/To)^3]
- Sa/g = S × Ao × α = 0.42 × α

## Archivos generados
1. **autonomo/research/espectro_tabla_completa.md** — Tabla formateada con 101 puntos
   (T=0.00 a 5.00s, paso 0.05s), parámetros, fórmula, pico, instrucciones ETABS
2. **autonomo/scripts/espectro_elastico_Z3SC.txt** — Archivo listo para ETABS
   (2 columnas: T[s] y Sa/g, separadas por tab, 101 líneas)
3. **autonomo/scripts/calc_espectro.py** — Script Python que genera ambos archivos

## Verificaciones realizadas
- Pico: α_max = 2.7752 en T = 0.35s (≈2.78 como esperado) ✓
- Sa_max/g = 1.1656, Sa_max = 11.434 m/s² ✓
- T=0: α=1.0 (caso límite correcto) ✓
- T=To=0.40: α=5.5/2=2.750 (valor exacto analítico) ✓
- T→∞: α→0 (p=1.6 < 3, denominador domina) ✓
- Cross-check con formulas_verificadas.md (R04): consistente (diff < 0.4% por redondeo)
- Fórmula confirmada contra NCh433 Art. 6.3.5.2 Ec. (9)

## Modificaciones a la guía
- Actualizado Paso 7.2 en GUIA-COMPLETA-EDIFICIO1-ETABS-v19.md:
  - Reemplazada tabla parcial (16 filas + "...") por tabla resumida de 8 puntos clave
  - Agregada referencia al archivo completo (espectro_tabla_completa.md)
  - Agregada referencia al archivo ETABS (espectro_elastico_Z3SC.txt)
  - Corregida fórmula: eliminado "/ (I)" incorrecto del Sa elástico
  - Agregada referencia a Art. 12.2 del DS61

## Instrucciones de uso en ETABS
1. Define > Functions > Response Spectrum > From File
2. Browse al archivo espectro_elastico_Z3SC.txt
3. Scale Factor = 9.81 (convierte Sa/g a m/s²)
4. Damping = 5%
5. Asignar a Load Cases SEx y SEy
