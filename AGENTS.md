# Análisis y Diseño Sísmico de Edificios (ADSE) — UCN 1S-2026

## Contexto
- **Ramo**: DAIC 00904 — Análisis y Diseño Sísmico de Edificios
- **UCN**, Ingeniería Civil, IX semestre, 1S-2026
- **Profesor**: Juan Music Tomicic (jmusic@ucn.cl)
- **Ayudante Taller**: Roberto Cortés / Ignacio Huerta

## Cómo responder preguntas del curso

### Paso 1: Lee el INDICE DETALLADO
**SIEMPRE empieza leyendo `docs/apuntes/INDICE.md`** — tiene el mapa completo de cada tema, fórmula y concepto con su archivo PDF y página exacta.

### Paso 2: Lee el PDF específico
Los apuntes (321 págs) están cortados en 14 PDFs temáticos en `docs/apuntes/`.
Conservan todas las imágenes, ecuaciones, diagramas y gráficos originales.
Usa `Read` con parámetro `pages` para navegar dentro de cada PDF.

### Paso 3: Si la pregunta involucra normativa, consulta las normas
Las normas están en `docs/Normas Utilizadas ADSE/`.

### Paso 4: Responde con la terminología del profesor y referencia normativa

## Estructura de archivos

```
docs/
├── Programa Curso.pdf                    ← Programa oficial (áreas temáticas, bibliografía)
├── Planificación Didáctica 1S-2026.pdf   ← Calendario, horas por RA, ponderaciones
├── Enunciado Taller.pdf                  ← Taller semestral (Ed.1 muros + Ed.2 marcos)
├── Apuntes del Curso.pdf                 ← Original 321 págs (>20MB, NO leer directo)
│
├── apuntes/                              ← APUNTES CORTADOS POR CAPÍTULO
│   ├── INDICE.md                         ← ★★★ ÍNDICE MAESTRO — LEE ESTO PRIMERO ★★★
│   ├── 00-Prologo.pdf                    (2 págs)
│   ├── 01-Aspectos-Conceptuales.pdf      (47 págs) Cap 1: diafragmas, matrices, clasificación
│   ├── 02a-Conceptos-Fundamentales.pdf   (11 págs) Riesgo, ductilidad, etapas proyecto
│   ├── 02b-Normativa-NCh433-DS61.pdf     (25 págs) Normativa, zonificación, suelos, Vs30
│   ├── 02c-Analisis-Estatico.pdf         (16 págs) Método estático, C, fuerzas, torsión
│   ├── 02d-Analisis-Dinamico-Modal-Espectral.pdf (15 págs) Espectro, modos, CQC, drift
│   ├── 02e-Diseno-Edificios-R-Pushover.pdf (25 págs) R*, pushover, CM/CR, ejemplo
│   ├── 02f-Perfil-Biosismico.pdf         (27 págs) 13 indicadores + artículo Antofagasta
│   ├── 03a-Muros-Normativa-y-Fallas.pdf  (13 págs) Evolución normativa, fallas, 27F
│   ├── 03b-Muros-Diseno-Corte-Flexion-Confinamiento.pdf (56 págs) Diseño completo muros
│   ├── 03c-Muros-Predimensionamiento-y-Ejemplos.pdf (12 págs) Predimensionamiento
│   ├── 04-Marcos-Especiales-HA.pdf       (32 págs) Cap 4: vigas, columnas, nudo, col.fuerte
│   ├── 05a-Analisis-Estructural-ACI318.pdf (16 págs) ACI318-2019, esbeltez, P-Delta
│   └── 05b-Problemas-Propuestos.pdf      (24 págs) Problemas tipo control
│
├── Material taller/                      ← MATERIAL ETABS/TALLER
│   ├── Material Apoyo Taller 2026.pdf    ← ★★★ GUÍA ESPECÍFICA DEL TALLER ★★★ (47 págs)
│   │     Drift NCh433, torsión accidental (3 métodos), combinaciones de carga,
│   │     diagramas P-M, Section Cuts, ejes ETABS vs SAP — Prof. Music
│   ├── Paso a Paso ETABS M.Lafontaine.pdf ← Tutorial modelación completa HA (143 págs)
│   │     Flujo completo: materiales → secciones → mesh → diafragmas → resultados
│   │     Prácticas chilenas, J=0 vigas, inercia losa 25%, validación Peso/Área~1 tonf/m²
│   ├── Manual de ETABS v19.pdf           ← Referencia interfaz ETABS (239 págs)
│   └── Section_Designer.pdf              ← Manual oficial CSI Section Designer (192 págs)
│         Secciones arbitrarias, superficies PMM, curvas M-φ
│
├── Diseño de Muros/Diseño de Muros/      ← DISEÑO MUROS — PROF. MUSIC
│   ├── 3 métodos diseño muros.pdf        ← Teoría + ejemplo numérico (13 págs, manuscrito)
│   │     4 métodos diseño Pu-Mu, confinamiento (Ash), corte (αc), ejemplo 5m×0.30m
│   ├── Ejemplos Diseño de MHA J.M.pdf    ← ★★★ 2 EJEMPLOS COMPLETOS ★★★ (32 págs)
│   │     Ej.1: muro rectangular, 6 combos NCh3171, confinamiento DS60/DS61, M-φ SAP
│   │     Ej.2: muro en T (edificio real 10p), diseño bidireccional
│   ├── Metodología Diseño MHA en ETABS J.M.pdf ← Guía ETABS para muros (16 págs)
│   │     3 métodos ETABS: T-C, Uniforme, General. Capturas paso a paso
│   └── Tabla Diseño de Muros.pdf         (duplicado de Tablas/)
│
├── Manuales/Manuales Oficiales CSI ETABS/ ← MANUALES OFICIALES CSI
│   ├── Introductory Tutorial.pdf         ← Tutorial ETABS: acero (4p) + HA (6p) (118 págs)
│   ├── Manual Diseño Marco H.A-ACI-318-08.pdf ← Algoritmos diseño marcos ACI318-08 (78 págs)
│   │     Superficies interacción 3D, capacity shear (Mpr 1.25fy), col.fuerte/viga.débil
│   ├── Manual Diseño Muros ACI-318-08.pdf ← Algoritmos diseño muros ACI318-08 (72 págs)
│   │     Piers, spandrels, elementos de borde (art.21.9.6), D/C ratio
│   └── Section_Designer.pdf              (duplicado de Material taller/)
│
├── Manuales (1)/Manuales Gerdau - Aza/   ← MANUALES GERDAU AZA
│   ├── gerdau-aza-manual-de-calculo-de-hormigon-armado.pdf ← Manual cálculo HA (283 págs)
│   │     ACI318-05, flexión, corte, torsión, diseño sísmico, 164 págs diagramas Pu-Mu
│   │     ⚠️ PDF escaneado (imágenes), sin texto extraíble
│   └── Manual-de-Armaduras-2022.pdf      ← Manual armaduras de refuerzo (292 págs)
│         Fabricación, doblado, ganchos sísmicos, traslapos, recubrimientos, NCh204:2020
│
├── Tablas/                               ← TABLAS DE DISEÑO (Gerdau AZA / CAP)
│   ├── Tabla Diseño de Muros.pdf         ← 32 diagramas Pu-Mu muros c/ elem. borde
│   │     f'c=20-55 MPa, fy=420, γ=0.8/0.9, ρw=0.25%/0.50%
│   ├── Tablas Diseño de Columnas.pdf     ← 13 diagramas Pu-Mu columnas rectangulares
│   │     f'c=20-50 MPa, fy=420, γ=0.8/0.9, arm. bordes/perimetral
│   └── Tablas Armaduras/Tabla de Fierros/ ← 2 imágenes JPG tablas barras CAP
│         Peso (kg/m), sección (cm²), perímetro, sección/m (cm²/m)
│
├── estudio/                              ← MATERIAL DE ESTUDIO GENERADO
│   ├── 01-Aspectos-Conceptuales.md
│   └── 02a-Conceptos-Fundamentales.md
│
└── Normas Utilizadas ADSE/              ← NORMATIVA OFICIAL
    ├── NCh0433-1996-Mod.2009.pdf         ← Diseño sísmico de edificios
    ├── DECRETO 61 2011 DISEÑO SISMICO DE EDIFICIOS.pdf
    ├── DECRETO 60 2011 DISEÑO Y CALCULO HORMIGON ARMADO.pdf
    ├── ACI-318-08_-Spanish-.pdf          ← Código concreto estructural
    ├── NCh 3171- 2017.pdf               ← Estados de carga
    └── NCh1537- 2009 Diseño estructural de edificios - Cargas perman.pdf

Horario y controles.pdf                   ← Horario semanal + fechas controles/exposiciones
```

## Cuándo ir a la norma vs. apuntes vs. material taller

| Situación | Fuente |
|-----------|--------|
| Entender un concepto, ver diagramas, ejemplos | Apuntes (docs/apuntes/) |
| Verificar un artículo específico (ej: "art. 21.9.5.4") | ACI-318-08 o DS60 |
| Verificar zonificación, parámetros suelo, espectro | NCh433 o DS61 |
| Verificar estados de carga | NCh 3171-2017 |
| Verificar cargas permanentes | NCh1537-2009 |
| Fórmula del corte basal, C, Cmáx, Cmín | NCh433 + DS61 + Apuntes 02c |
| Cómo verificar drift en ETABS | Material Apoyo Taller 2026 (sección B) |
| Cómo aplicar torsión accidental en ETABS | Material Apoyo Taller 2026 (sección H) |
| Combinaciones de carga ETABS (método estático/dinámico) | Material Apoyo Taller 2026 (sección I) |
| Cómo modelar un edificio paso a paso en ETABS | Paso a Paso ETABS Lafontaine |
| Opciones/menús de ETABS | Manual de ETABS v19 |
| Section Designer (superficies PMM, curvas M-φ) | Section_Designer.pdf |
| Diseño de muros: teoría y métodos (Pu-Mu, corte, confinamiento) | Diseño de Muros/3 métodos diseño muros.pdf |
| Diseño de muros: ejemplos completos con normativa vigente | Diseño de Muros/Ejemplos Diseño de MHA J.M.pdf |
| Diseño de muros: implementación en ETABS (3 métodos) | Diseño de Muros/Metodología Diseño MHA en ETABS J.M.pdf |
| Cómo ETABS diseña marcos HA (algoritmos ACI318-08) | Manuales/Manual Diseño Marco H.A-ACI-318-08.pdf |
| Cómo ETABS diseña muros HA (algoritmos ACI318-08) | Manuales/Manual Diseño Muros ACI-318-08.pdf |
| Tutorial ETABS oficial (edificio HA con marcos+muros) | Manuales/Introductory Tutorial.pdf (Parte II) |
| Diagramas de interacción Pu-Mu (164 págs de ábacos) | Manuales (1)/gerdau-aza-manual-de-calculo-de-HA.pdf |
| Detalles constructivos (ganchos sísmicos, traslapos) | Manuales (1)/Manual-de-Armaduras-2022.pdf |
| Diagramas de interacción Pu-Mu para muros | Tablas/Tabla Diseño de Muros.pdf |
| Diagramas de interacción Pu-Mu para columnas | Tablas/Tablas Diseño de Columnas.pdf |
| Área/peso de barras de refuerzo, cm²/m | Tablas/Tablas Armaduras/ |

## Notación del curso
- Cargas: PP, SCP, SCT, TERP, TERT
- Elementos: VI20/60G30, MHA30G30, MHA20G30, Losa15G30
- Ec = 4700√f'c [MPa], 1 MPa ≈ 10 kgf/cm², g = 9.81 m/s²

## Evaluación
- **NF = 0.7×NC + 0.3×NTaller**
- NC = 0.20×C1 + 0.40×C2 + 0.40×C3
- Taller: asistencia 100%, ETABS/SAP, informes + exposiciones
