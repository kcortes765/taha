# Índice del Material del Taller ADSE 2026

## Contexto
- **Ramo**: Análisis y Diseño Sísmico de Edificios (DAIC 00904)
- **UCN**, Ing. Civil, IX semestre, 1S-2026
- **Profesor**: Juan Music Tomicic
- **Taller**: 2 edificios — Ed.1 (muros 20p) + Ed.2 (marcos 5p)
- **Evaluación**: NTaller ≥ 4.0 independiente, 100% asistencia

## Estructura de esta carpeta

```
taller/
├── INDICE_TALLER.md              ← ESTE ARCHIVO
├── Programa Curso.pdf            ← Programa oficial del ramo
├── Planificación Didáctica 1S-2026.pdf ← Calendario, ponderaciones
│
├── enunciado/                    ← ENUNCIADO DEL TALLER
│   ├── Enunciado Taller.pdf      ← PDF completo (7 págs)
│   └── enunciado_page2-7.png     ← Imágenes de planos (planta, elevaciones, cortes)
│
├── material-apoyo-taller/        ← MATERIAL ESPECÍFICO DEL TALLER
│   ├── Material Apoyo Taller 2026.pdf  ← ★★★ GUÍA PROF. MUSIC (47p) ★★★
│   │     Drift NCh433, torsión accidental (3 métodos),
│   │     combinaciones de carga, diagramas P-M, Section Cuts
│   ├── Paso a Paso ETABS M.Lafontaine.pdf ← Tutorial modelación HA (143p)
│   │     Flujo completo: materiales → secciones → mesh → resultados
│   ├── Manual de ETABS v19.pdf   ← Referencia interfaz ETABS (239p)
│   └── Section_Designer.pdf      ← Secciones arbitrarias, PMM, M-φ (192p)
│
├── normas/                       ← NORMATIVA OFICIAL APLICABLE
│   ├── NCh0433-1996-Mod.2009.pdf ← Diseño sísmico de edificios
│   ├── DECRETO 61...pdf          ← DS61: complemento sísmico
│   ├── DECRETO 60...pdf          ← DS60: diseño/cálculo HA
│   ├── NCh 3171-2017.pdf         ← Estados de carga (combinaciones)
│   ├── NCh1537-2009...pdf        ← Cargas permanentes
│   └── ACI-318-08_-Spanish-.pdf  ← Código concreto estructural
│
├── diseno-muros/                 ← DISEÑO DE MUROS — PROF. MUSIC
│   ├── 3 métodos diseño muros.pdf      ← Teoría: Pu-Mu, corte, confinamiento (13p)
│   ├── Ejemplos Diseño de MHA J.M.pdf  ← ★ 2 ejemplos completos (32p)
│   └── Metodología Diseño MHA en ETABS J.M.pdf ← 3 métodos ETABS (16p)
│
├── manuales-csi/                 ← MANUALES OFICIALES CSI
│   ├── Introductory Tutorial.pdf       ← Tutorial: edificio HA marcos+muros (118p)
│   ├── Manual Diseño Marco H.A-ACI-318-08.pdf ← Algoritmos marcos (78p)
│   └── Manual Diseño Muros ACI-318-08.pdf     ← Algoritmos muros (72p)
│
├── manuales-gerdau/              ← MANUALES GERDAU AZA
│   ├── gerdau-aza-manual-de-calculo-de-HA.pdf ← Manual cálculo HA (283p)
│   └── Manual-de-Armaduras-2022.pdf           ← Armaduras, detalles (292p)
│
├── tablas/                       ← TABLAS DE DISEÑO
│   ├── Tabla Diseño de Muros.pdf       ← 32 diagramas Pu-Mu muros
│   ├── Tablas Diseño de Columnas.pdf   ← 13 diagramas Pu-Mu columnas
│   ├── Fierros_01.jpg                  ← Tabla de barras (peso, sección)
│   └── Fierros_02.jpg                  ← Tabla de barras (cm²/m)
│
└── apuntes-relevantes/           ← APUNTES DEL CURSO (solo los del taller)
    ├── INDICE.md                 ← Índice maestro de todos los apuntes
    ├── 02c-Analisis-Estatico.pdf        ← Método estático, C, fuerzas
    ├── 02d-Analisis-Dinamico-Modal-Espectral.pdf ← Espectro, modos, CQC, drift
    ├── 02e-Diseno-Edificios-R-Pushover.pdf      ← R*, pushover, CM/CR
    └── 03b-Muros-Diseno-Corte-Flexion-Confinamiento.pdf ← Diseño completo muros
```

## Edificio 1 (el que automatiza el pipeline)
- **20 pisos**: h1=3.4m, h2-20=2.6m, H=52.8m
- **Planta**: 38.5m × 13.8m (~532 m²)
- **Sistema**: Muros de HA (Ro=11)
- **Zona 3** (Antofagasta): Ao=0.4g, Suelo C
- **Materiales**: G30 (f'c=30 MPa), A630-420H (fy=420 MPa)

## Edificio 2 (marcos, NO automatizado)
- **5 pisos**: marcos especiales de HA
- **Se modela manualmente en ETABS**

## Entregables del taller
1. Modelo ETABS de ambos edificios
2. Informes con verificaciones (drift, peso, corte basal)
3. Diseño de muros (Ed.1) y marcos (Ed.2)
4. 3 exposiciones (26 mayo, 16 junio, 7 julio)

## Fechas clave
- C1: 5 mayo | C2: 26 mayo | C3: 30 junio
- Expo1: 26 mayo | Expo2: 16 junio | Expo3: 7 julio
