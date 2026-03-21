# Feature G03 — Corregir guía: Torsión accidental (3 métodos)

**Fecha**: 2026-03-21
**Archivo editado**: `docs/estudio/GUIA-COMPLETA-EDIFICIO1-ETABS-v19.md`
**Fuente**: `autonomo/research/material_apoyo_extracto.md` (sección H) + Lafontaine extracto + NCh433 art. 6.3.4

## Cambios realizados

### FASE 8 — Reescritura completa (líneas 920-1232)

1. **Fórmula de excentricidad CORREGIDA** — Error crítico:
   - ANTES: `ek = L_perp × (0.10 × (N-k)/(N-1))` → daba 10% en base, 0% en techo (AL REVÉS)
   - AHORA: `ek = 0.10 × (zk / Htotal) × b_perp` → correctamente 10% en techo, 0% en base
   - Fórmula basada en elevación (no piso), funciona con alturas de entrepiso variables

2. **Tabla completa de 20 excentricidades** — valores numéricos para ambas direcciones:
   - ek,Y (sismo X): 0.089 m (piso 1) a 1.382 m (piso 20)
   - ek,X (sismo Y): 0.247 m (piso 1) a 3.851 m (piso 20)

3. **Resumen comparativo** de los 3 métodos (tabla del extracto)

4. **Método a) — Detalles agregados:**
   - Nota sobre NO desplazar CM en ambas direcciones simultáneamente
   - Explicación de por qué se necesitan 4 modales separados (propiedades dinámicas cambian)
   - Nota sobre importación automática de matriz de masa via caso no lineal
   - Tabla resumen de 6 casos RS resultantes (SDX, SDX±Y, SDY, SDY±X)
   - Nota sobre Diaph Eccentricity = 0 para evitar doble conteo

5. **Método b) Forma 1 — Detalles agregados:**
   - Dos formas de obtener story shears (Story Response Plots vs Show Tables)
   - Nota sobre cortes ACUMULADOS (hay que restar Qk - Qk+1)
   - Checkbox "Apply Load at Diaphragm Center of Mass"
   - Campos Fx=0, Fy=0, solo Mz
   - Ejemplos numéricos para piso 20 y piso 1

6. **Método b) Forma 2 — Detalles agregados:**
   - Tablas parciales con valores de excentricidad para SDTX y SDTY
   - Nota: valor se ingresa como longitud positiva, ETABS aplica ±e internamente
   - Resultado: 2 sub-casos automáticos por caso espectral

### FASE 9 — Reestructuración (líneas 1234-1338)

1. **Nota explicativa** sobre ± automático en Response Spectrum
2. **Relación teórico-práctico**: profesor lista 19-27 combos, ETABS necesita 11/7/15
3. **Combinaciones gravitacionales** extraídas como sección común
4. **Caso 1 expandido**: de notación abreviada (CP, L) a notación explícita (PP, TERP, SCP)
5. **Notas de lógica** por caso explicando el conteo
6. **Sección Casos 4-6**: nota sobre mismas combos con diafragma semi-rígido
7. **Envolventes** por caso separado (ENV_Caso1/2/3)

## Verificaciones realizadas

- Fórmula de excentricidad: confirmada contra NCh433 art. 6.3.4 + Lafontaine + extracto Material Apoyo
- Valores numéricos tabla: verificados manualmente (pisos 1, 5, 10, 19, 20)
- Coherencia con FASE 12 (los 6 casos): verificada
- Nomenclatura de casos (SDX, SDX±Y, SDY, SDY±X, TEX, TEY, SDTX, SDTY): consistente entre FASE 8, 9 y 12
