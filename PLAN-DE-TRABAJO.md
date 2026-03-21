# PLAN DE TRABAJO — Ser el mejor en ADSE 1S-2026

> Objetivo: maximizar rendimiento en cada evaluacion.
> Inicio: 3 marzo 2026 | C1: 5 mayo | C2: 26 mayo | C3: 30 junio

---

## VISION GENERAL DEL SEMESTRE

```
MAR         ABR         MAY              JUN              JUL
|---3 sem---|---4 sem---|---4 sem--------|---4 sem--------|--1 sem--|
[Sismologia ][Bases+Anal][isis sismico   ][Muros+Marcos   ][cierre ]
             [ETABS taller progresivo                              ]
                         C1(5/5)  C2(26/5)        C3(30/6)
                                  Expo1    Expo2    Expo3
                                  (26/5)   (16/6)   (7/7)
```

### Peso real de cada control en la nota final

| Control | % de NC | % de NF (x0.70) | Contenido |
|---------|---------|------------------|-----------|
| C1 | 20% | **14%** | Sismologia |
| C2 | 40% | **28%** | Bases + Analisis sismico |
| C3 | 40% | **28%** | Diseno muros + marcos |
| Taller | 100% NTaller | **30%** | ETABS: 2 edificios |

**Estrategia**: C2 y C3 valen el doble que C1. Hay que dominar C1 pero invertir el mayor esfuerzo en C2 y C3.

---

## SIMULADOR DE NOTAS

Para NF = 7.0:
```
Si C1=7.0, C2=7.0, C3=7.0 → NC=7.0 → con NTaller=7.0 → NF=7.0
Si C1=6.0, C2=7.0, C3=7.0 → NC=6.8 → con NTaller=7.0 → NF=6.86
Si C1=7.0, C2=6.5, C3=7.0 → NC=6.6 → con NTaller=7.0 → NF=6.72
```

**Conclusion**: Sacrificar 1 punto en C1 baja NF solo 0.14. Sacrificar 1 punto en C2 o C3 baja NF 0.28. **Priorizar C2 y C3.**

---

## FASE 1: SISMOLOGIA (Semanas 1-3: 3 mar - 21 mar)

### Que estudiar
**Archivos**: `01-Aspectos-Conceptuales.pdf`, `02a-Conceptos-Fundamentales.pdf`, `02b-Normativa-NCh433-DS61.pdf`

### Temas criticos (alta probabilidad de pregunta)

#### Prioridad ALTA — dominar completamente
- [ ] **Diafragmas**: rigido vs flexible, indice de flexibilidad IF <= 2.0
- [ ] **CM y CR**: como se calculan, excentricidad natural, torsion
- [ ] **Matriz de rigidez**: metodo equilibrio directo vs rigidez directa
- [ ] **Matrices de transformacion**: de local a global
- [ ] **Clasificacion sismorresistente**: 5 tipos (marcos, muros, acoplados, mixto, tubo)
- [ ] **Riesgo sismico**: peligro x vulnerabilidad, fuentes
- [ ] **Ductilidad**: definicion, grafico, relacion con energia
- [ ] **Zonificacion sismica Chile**: 3 zonas, valores Ao
- [ ] **Tipos de suelo DS61**: A-F, criterios, Vs30
- [ ] **Procedimiento 9 pasos** analisis dinamico modal espectral

#### Prioridad MEDIA — entender bien
- [ ] Metodos geofisicos (MASW, ReMi) — saber que son, no memorizar procedimiento
- [ ] Modelo pseudo-3D con subestructuras
- [ ] Ecuaciones de movimiento sistema asimetrico
- [ ] Aisladores vs disipadores (concepto)
- [ ] Etapas proyecto de edificio

### Problemas tipo control (C1)
- Edificio 1 piso asimetrico: calcular rigidez rotacional, armar matriz, corte basal
- Calcular Vs30 a partir de datos de capas, clasificar suelo
- Distribuir fuerzas sismicas a elementos resistentes con diafragma rigido

### Material de apoyo generado
- `docs/estudio/01-Aspectos-Conceptuales.md` (resumen completo)
- `docs/estudio/02a-Conceptos-Fundamentales.md` (resumen completo)
- App C1: `localhost:8080` (250 preguntas interactivas)

### Meta semana a semana

| Semana | Foco | Entregable personal |
|--------|------|---------------------|
| 1 (3-7 mar) | Cap 1a-1c: Diafragmas, matrices, CM/CR | Resumen 1 pagina con formulas |
| 2 (10-14 mar) | Cap 1d-1f: Clasificacion, subestructuras, 9 pasos | Resolver 2 problemas tipo |
| 3 (17-21 mar) | Cap 2a-2b: Riesgo, ductilidad, normativa, suelos | Resolver Vs30 + clasificacion |

---

## FASE 2: BASES + ANALISIS SISMICO (Semanas 4-8: 24 mar - 25 abr)

### Que estudiar
**Archivos**: `02c-Analisis-Estatico.pdf`, `02d-Analisis-Dinamico-Modal-Espectral.pdf`, `02e-Diseno-Edificios-R-Pushover.pdf`, `02f-Perfil-Biosismico.pdf`

### Temas criticos — ESTE ES EL BLOQUE MAS IMPORTANTE (40% NC)

#### Prioridad MAXIMA — calcular sin dudar
- [ ] **Corte basal Qo = C x I x P**: aplicar completo
- [ ] **Coeficiente C**: formula, parametros suelo (S, n, T'), limites Cmin/Cmax
- [ ] **Fuerzas por piso**: formulas 6.4 y 6.5, saber distribuir
- [ ] **Estados de carga NCh3171**: C1 a C7, cuando usar cada uno
- [ ] **Espectro de diseno Sa**: formula, R*, alpha
- [ ] **Superposicion CQC**: formula, coeficientes correlacion
- [ ] **Drift**: Condicion 1 (CM <= 0.002) y Condicion 2 (extremo <= 0.001)
- [ ] **R* = FSRE x FIRNL x FDED**: saber que es cada factor

#### Prioridad ALTA — entender y aplicar
- [ ] Torsion accidental: metodo estatico vs dinamico (2 formas)
- [ ] Analisis pushover: curva V-delta, interpretacion
- [ ] Cuando usar metodo estatico vs dinamico
- [ ] Diafragma rigido vs flexible: distribucion de fuerzas
- [ ] Verificacion deformaciones (metodo estatico)
- [ ] Factor R y Ro: valores para marcos y muros HA

#### Prioridad MEDIA — conocer
- [ ] 13 indicadores perfil bio-sismico (saber que evaluan)
- [ ] Ejemplo edificio 15+1 pisos Antofagasta
- [ ] 5 preguntas fundamentales del diseno sismico
- [ ] Espectro de desplazamiento elastico

### Problemas tipo control (C2)
- Dado un edificio: clasificar, calcular C, calcular Qo, distribuir fuerzas por piso
- Verificar drift (condicion 1 y 2) con datos de ETABS
- Calcular espectro de diseno para parametros dados
- Aplicar torsion accidental
- Calcular R* a partir de curva pushover

### Meta semana a semana

| Semana | Foco | Entregable personal |
|--------|------|---------------------|
| 4 (24-28 mar) | Metodo estatico: C, Qo, fuerzas/piso | Calcular Qo para Ed.1 y Ed.2 del taller |
| 5 (31 mar - 4 abr) | NCh3171, torsion accidental | Listar 7 combos con signos |
| 6 (7-11 abr) | Metodo dinamico: espectro, modos, CQC | Entender procedimiento completo |
| 7 (14-18 abr) | Drift, R*, pushover | Verificar drift para ejemplo |
| 8 (21-25 abr) | Perfil bio-sismico + repaso C2 | Resolver 3+ problemas tipo C2 |

---

## FASE 2.5: PREPARACION C1 (Semanas 8-9: 25 abr - 5 may)

### Plan de estudio intensivo pre-C1
- [ ] **2 semanas antes (21 abr)**: Repasar resumen de sismologia
- [ ] **1 semana antes (28 abr)**: Resolver todos los problemas tipo C1
- [ ] **3 dias antes (2 may)**: Usar app C1 (test completo MOD9)
- [ ] **1 dia antes (4 may)**: Repasar formulas clave + problemas errados
- [ ] **Dia del control (5 may)**: Llegar con formulas frescas

### Checklist de dominio C1
Antes del control, debo poder responder sin dudar:
- [ ] Que es un diafragma rigido? Cuando se considera rigido?
- [ ] Como se calcula CM y CR?
- [ ] Que es la excentricidad de diseno? (et = ex +- ea)
- [ ] Como se arma la matriz de rigidez de un edificio 1 piso?
- [ ] Diferencia entre equilibrio directo y rigidez directa?
- [ ] Los 5 tipos de estructuracion sismorresistente?
- [ ] Que es Vs30 y como se determina?
- [ ] Tipos de suelo DS61 y sus criterios?
- [ ] Que es riesgo sismico?
- [ ] Los 9 pasos del analisis dinamico modal espectral?

---

## FASE 3: PREPARACION C2 (Semanas 9-12: 5 may - 26 may)

### Solo 3 semanas entre C1 y C2 — tiempo critico

| Semana | Foco |
|--------|------|
| 9 (5-9 may) | Post-C1: repasar metodo estatico a fondo |
| 10 (12-16 may) | Metodo dinamico + drift + torsion |
| 11 (19-23 may) | Repaso integral C2: resolver problemas |
| **26 may** | **C2 + Expo1** (mismo dia!) |

### Checklist de dominio C2
- [ ] Calcular C completo con parametros dados
- [ ] Aplicar limites Cmin y Cmax
- [ ] Distribuir fuerzas por piso
- [ ] Escribir los 7 estados de carga NCh3171
- [ ] Calcular Sa para un modo dado
- [ ] Verificar drift condicion 1 y condicion 2
- [ ] Explicar los 3 componentes de R*
- [ ] Cuando se usa metodo estatico vs dinamico
- [ ] Aplicar torsion accidental (al menos 1 forma)

---

## FASE 4: DISENO MUROS + MARCOS (Semanas 12-17: 26 may - 30 jun)

### Que estudiar
**Archivos**: `03a`, `03b` (56p — el mas largo), `03c`, `04` (32p), `05a`
**Material extra critico**: `Diseno de Muros/Ejemplos Diseno de MHA J.M.pdf` (2 ejemplos completos)

### Temas criticos (40% NC — peso igual a C2)

#### Prioridad MAXIMA — MUROS
- [ ] **Verificacion esbeltez**: t > lu/16
- [ ] **Carga maxima**: Pu <= 0.35 f'c Ag
- [ ] **Diseno al corte**: Vc, Vs, Vn <= 0.83 sqrt(f'c) Acv
- [ ] **Diagrama de flujo completo del corte**
- [ ] **Diagrama de interaccion** Pu-Mu: como verificar
- [ ] **Elementos de borde**: cuando confinar (c >= clim)
- [ ] **Armadura confinamiento**: Ash = 0.09 s bc f'c/fyt
- [ ] **Signos cargas sismicas**: 4 subcombinaciones

#### Prioridad MAXIMA — MARCOS
- [ ] **Condiciones geometricas** vigas y columnas
- [ ] **Armadura longitudinal vigas**: momentos cara nudo, M+ >= 0.5 M-
- [ ] **Corte diseno vigas**: Ve basado en Mpr (1.25fy), NO del analisis
- [ ] **Zona rotula plastica**: s1 = 2h, espaciamientos
- [ ] **Confinamiento columnas**: zona critica l0, Ash
- [ ] **Columna fuerte - viga debil**: Sum(Mnc) >= 1.2 Sum(Mnb)
- [ ] **Corte en nudo**: Vn segun confinamiento (1.7/1.25/1.0 sqrt f'c Aj)

#### Prioridad ALTA
- [ ] Predimensionamiento muros (tau_lim)
- [ ] Verificacion curvatura (phi = 0.008/c)
- [ ] Esbeltez columnas ACI318
- [ ] Detallamiento: traslapos, ganchos sismicos

### Meta semana a semana

| Semana | Foco |
|--------|------|
| 12 (26-30 may) | Post-C2: fallas muros, normativa, esbeltez |
| 13 (2-6 jun) | Diseno al corte muros (completo) |
| 14 (9-13 jun) | Flexion compuesta + confinamiento muros |
| 15 (16-20 jun) | Marcos: vigas (longitudinal + transversal) - **Expo2 (16 jun)** |
| 16 (23-27 jun) | Marcos: columnas + col.fuerte-viga.debil + nudo |
| 17 (30 jun) | **C3** |

### Checklist de dominio C3
- [ ] Diseno completo de un muro: esbeltez → corte → flexion → confinamiento
- [ ] Usar diagrama de interaccion para verificar Pu-Mu
- [ ] Determinar si requiere elementos de borde
- [ ] Calcular Ash para confinamiento
- [ ] Disenar armadura longitudinal y transversal de una viga
- [ ] Calcular Ve de viga basado en Mpr
- [ ] Verificar col.fuerte-viga.debil
- [ ] Verificar corte en nudo

---

## TALLER — PLAN PARALELO

El taller corre en paralelo. Asistencia 100%.

| Periodo | Actividad taller |
|---------|-----------------|
| Mar-Abr | Modelacion Ed.1 (muros) en ETABS: materiales, secciones, mesh |
| Abr-May | Analisis sismico Ed.1: periodos, corte basal, drift, torsion |
| May (Expo1) | Presentar resultados analisis Ed.1 |
| May-Jun | Modelacion + analisis Ed.2 (marcos) |
| Jun (Expo2) | Presentar analisis Ed.2 + inicio diseno |
| Jun-Jul | Diseno muros Ed.1 + marcos Ed.2 |
| Jul (Expo3) | Entrega final con diseno completo |

### Material clave para el taller
1. **Material Apoyo Taller 2026.pdf** — instrucciones del profesor, leer PRIMERO
2. **Paso a Paso ETABS Lafontaine.pdf** — cuando te trabes con ETABS
3. **Ejemplos Diseno MHA J.M.pdf** — modelo para la Parte 2

---

## ESTRATEGIAS PARA SER EL MEJOR

### 1. Anticiparse a la clase
- Leer los apuntes ANTES de la catedra de cada semana
- Llegar con preguntas preparadas

### 2. Resolver problemas propuestos
- `05b-Problemas-Propuestos.pdf` tiene 24 paginas de problemas tipo control
- Resolver al menos 1 problema por semana desde semana 4

### 3. Conectar teoria con taller
- Cada concepto de catedra aplicarlo inmediatamente al modelo ETABS
- El taller refuerza lo que entra en los controles

### 4. Usar la app C1
- 250 preguntas con retroalimentacion
- Interactivos: calculadora estatica, verificador drift, CQC, modos
- Correr tests completos 1 semana antes de cada control

### 5. Dominar las normas
- Tener NCh433 y DS61 marcados con los articulos mas usados
- Saber navegar ACI318 por numero de articulo (ej: 21.9.5.4)

### 6. Grupo de estudio
- Resolver problemas con companeros la semana antes de cada control
- Explicar conceptos a otros es la mejor forma de dominarlos

### 7. Horario de atencion del profesor
- **Miercoles 9-18, Jueves 9-13** — aprovecharlo, especialmente antes de controles

---

## CALENDARIO VISUAL

```
MARZO 2026
Lu  Ma  Mi  Ju  Vi
 3   4   5   6   7   ← Semana 1: Diafragmas, matrices
10  11  12  13  14   ← Semana 2: Clasificacion, subestructuras
17  18  19  20  21   ← Semana 3: Riesgo, normativa, suelos
24  25  26  27  28   ← Semana 4: Metodo estatico

ABRIL 2026
Lu  Ma  Mi  Ju  Vi
31   1   2   3   4   ← Semana 5: NCh3171, torsion
 7   8   9  10  11   ← Semana 6: Metodo dinamico, CQC
14  15  16  17  18   ← Semana 7: Drift, R*, pushover
21  22  23  24  25   ← Semana 8: Perfil biosismico + repaso

MAYO 2026
Lu  Ma  Mi  Ju  Vi
28  29  30   1   2   ← Repaso intensivo C1
 5   6   7   8   9   ← ★ C1 (Mar 5) | Semana 9
12  13  14  15  16   ← Semana 10: Repaso C2
19  20  21  22  23   ← Semana 11: Repaso intensivo C2
26  27  28  29  30   ← ★ C2 + Expo1 (Mar 26) | Semana 12

JUNIO 2026
Lu  Ma  Mi  Ju  Vi
 2   3   4   5   6   ← Semana 13: Diseno corte muros
 9  10  11  12  13   ← Semana 14: Flexion + confinamiento
16  17  18  19  20   ← ★ Expo2 (Mar 16) | Semana 15: Marcos vigas
23  24  25  26  27   ← Semana 16: Marcos columnas + nudo
30                   ← ★ C3 (Mar 30)

JULIO 2026
Lu  Ma  Mi  Ju  Vi
     1   2   3   4   ← Semana 17
 7   8               ← ★ Expo3 (Mar 7)
```

---

## TRACKING DE PROGRESO

### Notas reales (completar despues de cada evaluacion)
| Evaluacion | Nota | Meta | Diferencia |
|------------|------|------|------------|
| C1 | ___ | 7.0 | ___ |
| C2 | ___ | 7.0 | ___ |
| C3 | ___ | 7.0 | ___ |
| Taller | ___ | 7.0 | ___ |
| **NF** | ___ | **7.0** | ___ |

### Materiales de estudio generados
- [x] Resumen Cap 1 (01-Aspectos-Conceptuales.md)
- [x] Resumen Cap 2a (02a-Conceptos-Fundamentales.md)
- [ ] Resumen Cap 2b (normativa, suelos)
- [ ] Resumen Cap 2c (metodo estatico)
- [ ] Resumen Cap 2d (metodo dinamico)
- [ ] Resumen Cap 3 (muros)
- [ ] Resumen Cap 4 (marcos)

---

*Actualizar este documento cada domingo con el progreso de la semana.*
