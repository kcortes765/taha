# DOCUMENTO MAESTRO — ADSE 1S-2026

> Fuente central de verdad para el ramo Análisis y Diseño Sísmico de Edificios.
> Actualizado: 3 marzo 2026

---

## 1. IDENTIFICACION DEL CURSO

| Campo | Valor |
|-------|-------|
| Codigo | DAIC 00904 |
| Carrera | Ingenieria Civil, IX semestre |
| Creditos | 5 SCT-Chile |
| Profesor | Juan Music Tomicic (jmusic@ucn.cl) |
| Atencion | Mi 9-18, Ju 9-13 |
| Ayudante taller | Roberto Cortes / Ignacio Huerta |
| Pre-requisitos | Hormigon Armado, Diseno en Acero, Dinamica de Estructuras |

### Horario semanal

| Dia | Bloque | Actividad |
|-----|--------|-----------|
| Lunes | C (11:40-13:10) | Catedra ADSE — Y3-101 |
| Martes | C (11:40-13:10) | Catedra ADSE — Y3-101 |
| Martes | E+F (16:15-19:30) | Taller ADSE — Y3-101 |

**Total**: 3h catedra + 3h taller + 2h autonomo = 8h/semana

---

## 2. SISTEMA DE EVALUACION

### Formula
```
NF = 0.70 x NC + 0.30 x NTaller

NC = 0.20 x C1 + 0.40 x C2 + 0.40 x C3
```

**Aprobacion independiente**: NC >= 4.0 Y NTaller >= 4.0

### Fechas de evaluacion

| Evaluacion | Fecha | Peso en NC | Contenido |
|------------|-------|------------|-----------|
| **C1** | Mar 5 mayo | 20% | Sismologia (RA1) |
| **C2** | Mar 26 mayo | 40% | Bases diseno + Analisis sismico (RA2+RA3) |
| **C3** | Mar 30 junio | 40% | Diseno muros + marcos (RA5+RA6) |
| Expo 1 | Mar 26 mayo | Taller | Avance taller |
| Expo 2 | Mar 16 junio | Taller | Avance taller |
| Expo 3 | Mar 7 julio | Taller | Entrega final |

### Taller
- Asistencia **100% obligatoria**
- Proyecto: analisis y diseno de 2 edificios reales en ETABS
- Evaluacion progresiva (informes + exposiciones)

---

## 3. RESULTADOS DE APRENDIZAJE (RA)

| RA | Descripcion | Semanas | Horas | Evaluacion |
|----|-------------|---------|-------|------------|
| RA1 | Conceptos de sismologia para ingenieria | 3 | 24 | C1 (20%) |
| RA2 | Estructuracion, modelacion, espectros de diseno | 1 | 8 | C2 (5%) |
| RA3 | Analisis sismico de edificios segun normativa | 4 | 32 | C2 (35%) |
| RA4 | Uso de ETABS y SAP para analisis | 3 | 24 | Taller (100%) |
| RA5 | Diseno de muros HA segun normativa | 3 | 24 | C3 (20%) |
| RA6 | Diseno de marcos especiales HA segun normativa | 3 | 24 | C3 (20%) |

---

## 4. MAPA DE CONTENIDOS POR CONTROL

### C1 — SISMOLOGIA (20% NC)

**Apuntes**: `01-Aspectos-Conceptuales.pdf` (47p), `02a-Conceptos-Fundamentales.pdf` (11p), `02b-Normativa-NCh433-DS61.pdf` (25p)

| Tema | Archivo | Pags PDF |
|------|---------|----------|
| Diafragmas (rigido, flexible, IF) | 01 | 1-8 |
| Centro de masa (CM) y rigidez (CR) | 01 | 6-8 |
| Torision natural y accidental | 01 | 6-8 |
| Matriz de rigidez (1 piso, N pisos) | 01 | 9-17 |
| Metodo equilibrio directo y rigidez directa | 01 | 11-12 |
| Matrices de transformacion | 01 | 15-17 |
| Clasificacion sismorresistente (Tipo I-V) | 01 | 25-26 |
| Modelo pseudo-3D con subestructuras | 01 | 27-37 |
| Procedimiento analisis dinamico (9 pasos) | 01 | 38-47 |
| Riesgo sismico = peligro x vulnerabilidad | 02a | 1 |
| Rigidez, ductilidad, energia | 02a | 2-4 |
| Aisladores y disipadores (ecuacion movimiento) | 02a | 5-7 |
| Etapas de un proyecto de edificio | 02a | 8-11 |
| Normativa sismica vigente Chile | 02b | 1-3 |
| Zonificacion sismica (Zona 1-3, Ao) | 02b | 5-6 |
| Tipos de suelo DS61 (A-F) | 02b | 7-8 |
| Metodos geofisicos: MASW, ReMi, Vs30 | 02b | 10-24 |

### C2 — ANALISIS SISMICO (40% NC)

**Apuntes**: `02c-Analisis-Estatico.pdf` (16p), `02d-Analisis-Dinamico-Modal-Espectral.pdf` (15p), `02e-Diseno-Edificios-R-Pushover.pdf` (25p), `02f-Perfil-Biosismico.pdf` (27p)

| Tema | Archivo | Pags PDF |
|------|---------|----------|
| Clasificacion edificio (I, Tipo I-IV) | 02c | 1 |
| Factor R y Ro | 02c | 1-2 |
| Estados de carga NCh3171 (C1-C7) | 02c | 3 |
| **Corte basal: Qo = C x I x P** | 02c | 4 |
| Coeficiente sismico C y sus limites | 02c | 4-5 |
| Parametros suelo (S, n, T') | 02c | 5 |
| Cuando aplicar metodo estatico | 02c | 6 |
| Fuerzas por piso (formulas 6.4, 6.5) | 02c | 7 |
| Torsion accidental (estatico) | 02c | 8 |
| Diafragma rigido vs flexible | 02c | 12-15 |
| Verificacion deformaciones | 02c | 16 |
| **Espectro de diseno: Sa** | 02d | 1-2 |
| R* = factor reduccion espectral | 02d | 1 |
| Modos: acumular >= 90% masa | 02d | 3 |
| **Superposicion CQC** | 02d | 5 |
| Torsion accidental (dinamico, 2 formas) | 02d | 6-8 |
| **Drift CM <= 0.002, punto extremo <= 0.001** | 02d | 9-13 |
| 5 preguntas fundamentales diseno sismico | 02e | 1 |
| Condiciones: resistencia, rigidez, ductilidad | 02e | 2 |
| **Analisis Pushover** | 02e | 9-13 |
| **R* = FSRE x FIRNL x FDED** | 02e | 11 |
| Ejemplo edificio 15+1 pisos Antofagasta | 02e | 16-21 |
| Columna fuerte - viga debil (concepto) | 02e | 22 |
| 13 indicadores perfil bio-sismico | 02f | 1-14 |
| Articulo 8 edificios Antofagasta | 02f | 15-20 |

### C3 — DISENO MUROS + MARCOS (40% NC)

**Apuntes**: `03a` (13p), `03b` (56p), `03c` (12p), `04` (32p), `05a` (16p)
**Material extra**: `Diseno de Muros/` (3 PDFs), `Tablas/`

#### Muros HA

| Tema | Archivo | Pags PDF |
|------|---------|----------|
| Evolucion normativa muros Chile | 03a | 2-3 |
| Modos de falla (corte, flexion, deslizamiento) | 03a | 4-5 |
| Efecto confinamiento | 03a | 6-7 |
| Danos terremoto 27F-2010 | 03a | 8-9 |
| Verificacion esbeltez: t > lu/16 | 03b | 3 |
| Carga max: Pu <= 0.35 f'c Ag | 03b | 3 |
| **Diseno al corte** (Vc, Vs, diagrama flujo) | 03b | 4-8 |
| **Diseno a flexion compuesta** (diag. interaccion) | 03b | 9-23 |
| Signos cargas sismicas (4 subcombinaciones) | 03b | 13 |
| **Verificacion curvatura** (art 21.9.5.4) | 03b | 24-35 |
| **Elementos de borde** (c >= clim) | 03b | 36-42 |
| Armadura confinamiento Ash | 03b | 43-45 |
| Detallamiento armaduras muros | 03b | 46-56 |
| Predimensionamiento espesores | 03c | 6-12 |

#### Marcos especiales HA

| Tema | Archivo | Pags PDF |
|------|---------|----------|
| Condiciones geometricas vigas | 04 | 1-3 |
| **Armadura longitudinal vigas** | 04 | 4-5 |
| **Armadura transversal vigas (Ve, Mpr)** | 04 | 6-12 |
| Condiciones geometricas columnas | 04 | 13-14 |
| Armadura longitudinal columnas | 04 | 15-16 |
| **Armadura transversal columnas (confinamiento)** | 04 | 16-23 |
| **Columna fuerte - viga debil** (ecuacion 21.1) | 04 | 24-25 |
| **Corte en el nudo** (Vn segun confinamiento) | 04 | 26-32 |

---

## 5. FORMULAS CLAVE (REFERENCIA RAPIDA)

### Analisis sismico
```
Qo = C x I x P                              (corte basal estatico)
C  = (2.75 S Ao)/(g R) x (T'/T*)^n          (coeficiente sismico)
     con (Ao S)/(6g) <= C <= Cmax
Sa = (S Ao alpha)/(R*/I)                     (espectro diseno)
R* = FSRE x FIRNL x FDED                    (composicion R*)
```

### Diseno muros
```
Pu <= 0.35 f'c Ag                            (compresion maxima)
Vn <= 0.83 sqrt(f'c) Acv                     (resistencia corte)
Vc = 0.53 lambda sqrt(f'c) bw d              (aporte hormigon)
d  = 0.8 lw                                  (peralte efectivo)
phi_u = 0.008/c                              (capacidad curvatura)
c >= clim  =>  CONFINAR                       (elem. de borde)
cc = c - clim                                (largo a confinar)
Ash = 0.09 s bc f'c/fyt                      (armadura confinamiento)
```

### Diseno marcos
```
Ve = (Mpr1 + Mpr2)/lu                        (corte diseno columnas)
Mpr con 1.25 fy                              (momento probable)
Sum(Mnc) >= 1.2 Sum(Mnb)                     (col. fuerte-viga debil)
Vn nudo = gamma sqrt(f'c) Aj                 (gamma=1.7/1.25/1.0)
```

### Constantes del taller
```
Antofagasta = Zona 3, Ao = 0.4g, Suelo C, I = 1.0
Ec = 4700 sqrt(f'c) [MPa]
1 MPa ~ 10 kgf/cm^2,  g = 9.81 m/s^2
```

---

## 6. NORMATIVA UTILIZADA

| Norma | Archivo | Uso principal |
|-------|---------|---------------|
| NCh433:1996 Mod.2009 | `NCh0433-1996-Mod.2009.pdf` | Diseno sismico edificios |
| DS 61 (2011) | `DECRETO 61...pdf` | Complemento NCh433: suelos, espectro |
| DS 60 (2011) | `DECRETO 60...pdf` | Requisitos HA (basado en ACI318-08) |
| ACI 318-08 | `ACI-318-08_-Spanish-.pdf` | Codigo concreto estructural |
| NCh 3171:2017 | `NCh 3171- 2017.pdf` | Estados de carga |
| NCh 1537:2009 | `NCh1537- 2009...pdf` | Cargas permanentes |

**Ubicacion**: `docs/Normas Utilizadas ADSE/`

---

## 7. TALLER SEMESTRAL

### Edificio 1 — Muros (20 pisos)
- Antofagasta, Zona 3, Suelo C, Oficina (Cat II, I=1.0)
- G30 (f'c=300 kgf/cm^2), A630-420H (fy=4200 kgf/cm^2)
- Piso 1: 3.4m, pisos 2-20: 2.6m → Htotal = 52.8m
- Ec = 25742 MPa, gamma_HA = 2.5 tonf/m^3
- Vigas invertidas 20x60cm, Losas 15cm
- Muros e=30cm y e=20cm segun ejes

### Edificio 2 — Marcos (5 pisos)
- Misma ubicacion, G25 (f'c=250 kgf/cm^2)
- Planta 32.5x32.5m (5 vanos x 6.5m)
- Piso 1: 3.5m, pisos 2-5: 3.0m → Htotal = 15.5m
- Pisos 1-2: Col 70x70, Vigas 50x70, Losa 17cm
- Pisos 3-5: Col 65x65, Vigas 45x70, Losa 17cm

### Entregables del taller
1. **Parte 1**: Analisis sismico (peso, densidad muros, CM/CR, periodos, corte basal, espectros, deformaciones, 6 casos torsion)
2. **Parte 2 Ed.1**: Diseno muros eje 5 (rectangular) y eje 4 (T) en piso 1
3. **Parte 2 Ed.2**: Diseno vigas y columnas marco eje A (manual + ETABS)

---

## 8. MAPA DE MATERIALES

### Apuntes del curso (docs/apuntes/)
14 PDFs tematicos cortados del original de 321 paginas.
**Siempre consultar primero**: `INDICE.md`

### Material taller (docs/Material taller/)
| Archivo | Pags | Descripcion |
|---------|------|-------------|
| Material Apoyo Taller 2026.pdf | 47 | Instrucciones Prof. Music: drift, torsion, combos |
| Paso a Paso ETABS Lafontaine.pdf | 143 | Tutorial completo modelacion HA |
| Manual de ETABS v19.pdf | 239 | Referencia interfaz menus |
| Section_Designer.pdf | 192 | Superficies PMM, curvas M-phi |

### Diseno de muros (docs/Diseno de Muros/)
| Archivo | Pags | Descripcion |
|---------|------|-------------|
| 3 metodos diseno muros.pdf | 13 | Teoria + ejemplo numerico |
| Ejemplos Diseno de MHA J.M.pdf | 32 | 2 ejemplos completos normativa |
| Metodologia Diseno MHA en ETABS J.M.pdf | 16 | 3 metodos ETABS |

### Manuales CSI (docs/Manuales/)
| Archivo | Pags | Descripcion |
|---------|------|-------------|
| Introductory Tutorial.pdf | 118 | Tutorial oficial ETABS |
| Manual Diseno Marco HA ACI-318-08.pdf | 78 | Algoritmos marcos |
| Manual Diseno Muros ACI-318-08.pdf | 72 | Algoritmos muros |

### Tablas de diseno (docs/Tablas/)
- Diagramas Pu-Mu muros (32p) y columnas (13p)
- Tablas de barras (area, peso, cm^2/m)

### Manuales Gerdau AZA (docs/Manuales (1)/)
- Manual calculo HA (283p, escaneado) — 164p de abacos Pu-Mu
- Manual armaduras 2022 (292p) — detalles constructivos

---

## 9. APP DE ESTUDIO (app-c1/)

Aplicacion web para preparar C1. 6 archivos, ~11,000 lineas, 250 preguntas.
- **Stack**: HTML+CSS+JS vanilla, Three.js, Chart.js, MathJax
- **Modulos**: MOD1-MOD9 con interactivos y calculadoras
- **Servir**: `cd app-c1 && python -m http.server 8080` → localhost:8080

---

## 10. TABLA DE CONSULTA RAPIDA

| Necesito... | Ir a... |
|-------------|---------|
| Entender un concepto | Apuntes (docs/apuntes/) |
| Verificar articulo ACI | ACI-318-08 o DS60 |
| Zonificacion, suelo, espectro | NCh433 o DS61 |
| Estados de carga | NCh3171:2017 |
| Corte basal, C, Cmax, Cmin | NCh433 + DS61 + Apuntes 02c |
| Drift en ETABS | Material Apoyo Taller 2026 (sec B) |
| Torsion accidental en ETABS | Material Apoyo Taller 2026 (sec H) |
| Combinaciones de carga ETABS | Material Apoyo Taller 2026 (sec I) |
| Modelar edificio paso a paso | Paso a Paso ETABS Lafontaine |
| Diseno muros: teoria y metodos | 3 metodos diseno muros.pdf |
| Diseno muros: ejemplos completos | Ejemplos Diseno MHA J.M.pdf |
| Diseno muros en ETABS | Metodologia Diseno MHA en ETABS J.M.pdf |
| Algoritmos ETABS marcos HA | Manual Diseno Marco HA ACI-318-08.pdf |
| Algoritmos ETABS muros HA | Manual Diseno Muros ACI-318-08.pdf |
| Diagramas interaccion Pu-Mu | Tablas/ o Gerdau AZA |
| Detalles constructivos | Manual Armaduras 2022 |

---

## 11. NOTACION DEL CURSO

- **Cargas**: PP (peso propio), SCP (sobrecarga piso), SCT (sobrecarga techo), TERP (terminaciones piso), TERT (terminaciones techo)
- **Elementos**: VI20/60G30 (viga 20x60 G30), MHA30G30 (muro HA e=30 G30), Losa15G30
- **Unidades**: 1 MPa ~ 10 kgf/cm^2, g = 9.81 m/s^2, Ec = 4700 sqrt(f'c) [MPa]

---

*Este documento se actualiza conforme avanza el semestre.*
