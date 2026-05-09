# ÍNDICE DETALLADO — Apuntes Análisis y Diseño Sísmico de Edificios

> Autor: Prof. Juan Music Tomicic — UCN — Versión 2026
> PDF original: 321 páginas (slides PowerPoint convertidos)
> Cortado en 14 PDFs temáticos. Páginas refieren al PDF ORIGINAL.

---

## INSTRUCCIONES PARA LA IA

Cuando el usuario pregunte algo:
1. Busca el tema en este índice (usa Ctrl+F mental)
2. Identifica el **archivo PDF** y las **páginas específicas** donde está
3. Lee ese PDF con `Read` usando el parámetro `pages` si es necesario
4. Responde con la terminología del profesor y referenciando normativa chilena

**Las páginas listadas son del PDF ORIGINAL (321 págs).** Para leer un archivo cortado, las páginas internas van desde 1 hasta N (donde N = cantidad de páginas del sub-PDF). Para convertir: `página_interna = página_original - página_inicio_del_PDF + 1`.

---

## MAPA GENERAL DE ARCHIVOS

| # | Archivo | Páginas orig. | Capítulo / Tema |
|---|---------|---------------|-----------------|
| 0 | `00-Prologo.pdf` | 1-2 | Prólogo y organización del curso |
| 1 | `01-Aspectos-Conceptuales.pdf` | 3-49 | Cap 1: Aspectos conceptuales del diseño sismorresistente |
| 2a | `02a-Conceptos-Fundamentales.pdf` | 50-60 | Riesgo sísmico, rigidez, ductilidad, aisladores/disipadores, etapas proyecto |
| 2b | `02b-Normativa-NCh433-DS61.pdf` | 61-85 | Normativa sísmica Chile, zonificación, tipos de suelo, Vs30, MASW/ReMi |
| 2c | `02c-Analisis-Estatico.pdf` | 86-101 | Método estático: C, I, R, fuerzas por piso, torsión accidental, diafragmas |
| 2d | `02d-Analisis-Dinamico-Modal-Espectral.pdf` | 102-116 | Método dinámico: espectro diseño, modos, superposición CQC, deformaciones |
| 2e | `02e-Diseno-Edificios-R-Pushover.pdf` | 117-141 | Diseño integral: matrices rigidez, R*, pushover, centros masa/rigidez, ejemplo |
| 2f | `02f-Perfil-Biosismico.pdf` | 142-168 | 13 indicadores del perfil bio-sísmico + artículo científico Antofagasta |
| 3a | `03a-Muros-Normativa-y-Fallas.pdf` | 169-181 | Cap 3: Evolución normativa muros, modos de falla, confinamiento, daños 27F |
| 3b | `03b-Muros-Diseno-Corte-Flexion-Confinamiento.pdf` | 182-237 | Diseño completo de muros HA: corte, flexión compuesta, curvatura, confinamiento |
| 3c | `03c-Muros-Predimensionamiento-y-Ejemplos.pdf` | 238-249 | Predimensionamiento espesores, ejemplo edificio 16 pisos |
| 4 | `04-Marcos-Especiales-HA.pdf` | 250-281 | Cap 4: Diseño marcos especiales HA (vigas, columnas, nudo, col. fuerte-viga débil) |
| 5a | `05a-Analisis-Estructural-ACI318.pdf` | 282-297 | ACI318-2019 Cap 6: Análisis estructural, esbeltez columnas, P-Delta |
| 5b | `05b-Problemas-Propuestos.pdf` | 298-321 | Problemas propuestos (tipo control) |

---

## CAPÍTULO 1: ASPECTOS CONCEPTUALES SOBRE DISEÑO SISMORRESISTENTE
**Archivo: `01-Aspectos-Conceptuales.pdf` (47 págs)**

### a) Diafragmas (págs 3-10)
| Tema | Pág orig. | Pág PDF |
|------|-----------|---------|
| Definición de edificio y estructura | 3 | 1 |
| **Qué es un diafragma** | 4 | 2 |
| Diafragma semirígido: definición | 4 | 2 |
| **Diafragma rígido**: definición, CM, CR, excentricidad natural | 5 | 3 |
| **Diafragma flexible**: definición, índice de flexibilidad IF | 6 | 4 |
| IF ≤ 2.0 → rígido (ASCE 7-16) | 6 | 4 |
| Fórmula DMD/DPEV | 6 | 4 |
| Diagrama diafragma rígido (figura) | 7 | 5 |
| **Centro de masa (CM)** y **Centro de rigidez (CR)** | 8 | 6 |
| **Torsión natural** y **torsión accidental** | 8 | 6 |
| Excentricidad de diseño: et = ex ± ea | 8 | 6 |
| Figuras excentricidad natural y accidental | 9-10 | 7-8 |
| Determinación de esfuerzo de corte con diafragma rígido | 10 | 8 |

### b) Matriz de rigidez de edificios con diafragma rígido (págs 11-19)
| Tema | Pág orig. | Pág PDF |
|------|-----------|---------|
| Introducción: basado en Chopra Cap 9 | 11 | 9 |
| **Edificio 1 piso asimétrico**: 3 GDL (ux, uy, uθ) | 12 | 10 |
| Relación fuerza-desplazamiento, matriz [k] | 12-13 | 10-11 |
| **Método equilibrio directo** (desplazamientos unitarios) | 13-14 | 11-12 |
| **Método rigidez directa** (subestructuras) | 14 | 12 |
| Matriz de rigidez resultante 3×3 | 14 | 12 |
| Fuerzas de inercia, momento de inercia IO | 15 | 13 |
| Ecuaciones de movimiento sistema asimétrico 1 dir | 16 | 14 |
| **Edificios varios niveles** asimétricos: 3N GDL | 17-18 | 15-16 |
| Vector desplazamiento u = {ux, uy, uθ} | 18 | 16 |
| Matrices de transformación axi, ayi | 19 | 17 |
| Ensamble matriz rigidez: k = Σ ki | 19 | 17 |

### c) Respuesta sísmica de estructuras tridimensionales (págs 20-26)
| Tema | Pág orig. | Pág PDF |
|------|-----------|---------|
| Basado en Ridell & Hidalgo | 20 | 18 |
| Caso 1 piso: distribución fuerzas a elementos resistentes | 20 | 18 |
| Disposiciones NCh433 sobre deformaciones y torsión accidental | 20 | 18 |

### d) Clasificación sismo-resistente de edificios (págs 27-28)
| Tema | Pág orig. | Pág PDF |
|------|-----------|---------|
| **Tipo I**: Marcos rígidos (máx 20-22 pisos) | 27 | 25 |
| **Tipo II**: Muros de rigidez simples (máx 30-35 pisos) | 27 | 25 |
| **Tipo III**: Muros de rigidez acoplados (máx 30-35 pisos) | 28 | 26 |
| **Tipo IV**: Marcos + muros (máx 45-50 pisos) | 28 | 26 |
| **Tipo V**: Tubo simple/doble/múltiple (máx 50-65 pisos) | 28 | 26 |

### e) Matriz de rigidez: modelo pseudo-tridimensional con subestructuras (págs 29-39)
| Tema | Pág orig. | Pág PDF |
|------|-----------|---------|
| Modelación en base a subestructuras verticales | 29 | 27 |
| Grados de libertad: sistema tri-ortogonal | 30 | 28 |
| Coordenadas subestructura p (en planta) | 31 | 29 |
| Regla para recordar (matrices transformación) | 39 | 37 |

### f) Análisis dinámico superposición modal espectral — Procedimiento paso a paso (págs 40-49)
| Tema | Pág orig. | Pág PDF |
|------|-----------|---------|
| **Etapa 1**: Estructurar el edificio | 40 | 38 |
| **Etapa 2**: Identificar subestructuras verticales | 40 | 38 |
| **Etapa 3**: Matriz rigidez cada subestructura (locales) | 40 | 38 |
| **Etapa 4**: Matriz rigidez horizontal (condensación estática) | 40 | 38 |
| **Etapa 5**: Matriz rigidez del edificio (sistema global) | 40 | 38 |
| Caso 1: CM coinciden → método equilibrio directo | 40 | 38 |
| Caso 2: CM no coinciden → método rigidez directa | 41 | 39 |
| [Kp]global = [Ap]T [Kp] [Ap] | 42 | 40 |
| **Etapa 6**: Determinar matriz de masas | 43 | 41 |
| **Etapa 7**: Frecuencias y modos de vibrar | 43 | 41 |
| **Etapa 8**: Normalizar modos de vibrar | 43 | 41 |
| **Etapa 9**: Masas equivalentes (tabla Ux%, Uy%, Rz%) | 44 | 42 |
| Verificación Qmín ≤ Qbasal ≥ Qmáx | 45 | 43 |
| **Paso 2**: Factores participación modal | 45 | 43 |
| **Paso 3**: Desplazamientos por modo | 45 | 43 |
| **Paso 4**: Verificar condición desplazamiento norma | 45 | 43 |
| **Paso 5**: Solicitaciones sísmicas en CM | 45 | 43 |
| **Paso 6-7**: Desplazamientos y fuerzas por subestructura | 46 | 44 |
| **Paso 8**: Esfuerzos internos por subestructura | 46 | 44 |
| **Superposición CQC** → esfuerzos finales | 47 | 45 |
| Estados de carga NCh3171 para diseño | 48 | 46 |
| **Paso 9**: Torsión accidental (art. 6.3.4 NCh433) | 48 | 46 |
| Sismo X con torsión accidental +/- | 48-49 | 46-47 |

---

## CAPÍTULO 2: ANÁLISIS DE EDIFICIOS — FILOSOFÍA, CRITERIOS, MÉTODOS Y NORMATIVA

### 2a) Conceptos Fundamentales
**Archivo: `02a-Conceptos-Fundamentales.pdf` (11 págs)**

| Tema | Pág orig. | Pág PDF |
|------|-----------|---------|
| **Riesgo sísmico = Peligro × Vulnerabilidad** | 50 | 1 |
| Fuentes de vulnerabilidad: localización, proyecto, materiales, construcción | 50 | 1 |
| **Rigidez** (concepto y gráfico) | 51 | 2 |
| **Energía absorbida y disipada** (gráfico histerético) | 52 | 3 |
| **Ductilidad** (definición y gráfico) | 53 | 4 |
| Diseño convencional vs. aisladores vs. disipadores (ecuación movimiento) | 54 | 5 |
| Referencia: Crisafulli 2018 | 56 | 7 |
| **Etapas de un proyecto de edificio** | 57 | 8 |
| Roles: mandante, arquitecto, ingeniero estructural, revisor | 58 | 9 |
| Flujo: proyecto final → permiso construcción → ejecución → recepción | 59-60 | 10-11 |
| Ley 19748: revisión obligatoria cálculo estructural | 57 | 8 |

### 2b) Normativa Sísmica en Chile + Clasificación de Suelos
**Archivo: `02b-Normativa-NCh433-DS61.pdf` (25 págs)**

| Tema | Pág orig. | Pág PDF |
|------|-----------|---------|
| **Normas sísmicas vigentes** en Chile | 61 | 1 |
| NCh433:1996 Mod.2009 + DS61 → edificios | 61 | 1 |
| NCh2369:2025 → instalaciones industriales | 61 | 1 |
| NCh2745:2013 → aislación sísmica | 61 | 1 |
| **Principios NCh433**: sin daño (moderado), limitar daño (mediano), evitar colapso (severo) | 62 | 2 |
| **Filosofía implícita**: sismo moderado/fuerte/severo | 63 | 3 |
| Modelo estructural (figura) | 64 | 4 |
| **Factores que influyen en solicitaciones sísmicas** | 65 | 5 |
| **Zonificación sísmica**: Zona 1 (Ao=0.2g), Zona 2 (0.3g), **Zona 3 (0.4g)** | 65-66 | 5-6 |
| Mapa zonificación Chile | 66 | 6 |
| **Tipos de suelo** según DS61 (tabla, A-F) | 67 | 7 |
| **Clasificación suelos proyecto NCh433:2026** (nueva norma) | 68 | 8 |
| Importancia estudio mecánica de suelos | 69 | 9 |
| **Métodos geofísicos** para Vs30 | 70 | 10 |
| Cross Hole, Down Hole | 70 | 10 |
| **SASW**, **MASW** (Park et al. 1999) | 70-71 | 10-11 |
| Procedimiento MASW ensayo activo (figuras detalladas) | 72-76 | 12-16 |
| Arreglo geófonos, sismogramas, equipo adquisición | 72-76 | 12-16 |
| **ReMi** (ensayo pasivo, microtremores) | 77-80 | 17-20 |
| **Análisis registros ondas superficiales** → perfil Vs | 81 | 21 |
| Tabla ejemplo: tramos, profundidad, Vs | 81 | 21 |
| **Ejemplo determinación Vs30** y clasificación suelo DS61 | 84 | 24 |

### 2c) Método de Análisis Estático
**Archivo: `02c-Analisis-Estatico.pdf` (16 págs)**

| Tema | Pág orig. | Pág PDF |
|------|-----------|---------|
| **Clasificación de edificio** según importancia (I) | 86 | 1 |
| Tipo I (I=0.6), Tipo II (I=1.0), Tipo III (I=1.2), Tipo IV (I=1.2) | 86 | 1 |
| **Factor R y Ro**: Pórticos HA (R=7, Ro=11), Muros HA (R=7, Ro=11) | 86 | 1 |
| **Factor de reducción de la respuesta** (gráfico) | 87 | 2 |
| **Estados de carga NCh3171:2017** | 88 | 3 |
| C1: 1.4D, C2: 1.2D+1.6L+0.5Lr, C3: 1.2D+L+1.6Lr | 88 | 3 |
| C4: 1.2D+L±1.4Ex, C5: 0.9D±1.4Ex | 88 | 3 |
| C6: 1.2D+L±1.4Ey, C7: 0.9D±1.4Ey | 88 | 3 |
| **Métodos de análisis sísmico**: estático y dinámico | 89 | 4 |
| **Corte basal: Qo = C × I × P** | 89 | 4 |
| **Coeficiente sísmico C** = (2.75×S×Ao)/(g×R) × (T'/T*)^n | 89 | 4 |
| **(Ao×S)/(6×g) ≤ C ≤ Cmáx** | 89 | 4 |
| **Peso sísmico P** = permanentes + % sobrecarga | 89 | 4 |
| **Parámetros dependientes del suelo** (S, n, T') — tabla | 90 | 5 |
| **¿Cuándo se puede aplicar análisis estático?** | 91 | 6 |
| **Determinación fuerzas a nivel de piso** (fórmulas 6.4, 6.5) | 92 | 7 |
| **Torsión accidental** en método estático | 93 | 8 |
| Fuerzas para edificios 5-16 pisos | 94 | 9 |
| **Edificio sin diafragma rígido** (distribución fuerzas) | 94 | 9 |
| **Diafragma rígido vs flexible**: comparación distribución | 97 | 12 |
| Ejemplo: tren de casas 1 piso | 98 | 13 |
| Fuerzas sísmicas piso flexible | 100 | 15 |
| **Verificación deformaciones** (método estático) | 101 | 16 |

### 2d) Método Dinámico de Superposición Modal Espectral
**Archivo: `02d-Analisis-Dinamico-Modal-Espectral.pdf` (15 págs)**

| Tema | Pág orig. | Pág PDF |
|------|-----------|---------|
| **Espectro de diseño: Sa = (S×Ao×α)/(R*/I)** | 102 | 1 |
| Sae = espectro elástico (ξ=0.05) × I | 102 | 1 |
| **R* = factor reducción espectral** | 102 | 1 |
| Significado de Ao: sismo severo, 5-10% excedencia vida útil | 102 | 1 |
| Gráfico espectro elástico vs diseño | 103 | 2 |
| **Modos a considerar**: acumular ≥ 90% masa en cada dirección | 104 | 3 |
| Conceptos importantes (figuras) | 105 | 4 |
| **Superposición modal CQC** | 106 | 5 |
| **Torsión accidental en método dinámico**: 2 formas | 107 | 6 |
| Caso a) y Caso b) forma 1 y 2 | 107-109 | 6-8 |
| **Condición 1: drift CM ≤ 0.002** | 110 | 9 |
| **Condición 2: drift cualquier punto ≤ 0.001** | 110 | 9 |
| Explicación Condición 2 (figuras) | 112 | 11 |
| **Espectro de desplazamiento elástico** | 114 | 13 |
| **Comentario sobre Ro**: sobreresistencia edificios chilenos muros HA | 116 | 15 |

### 2e) Diseño de Edificios: Rigidez, R*, Pushover
**Archivo: `02e-Diseno-Edificios-R-Pushover.pdf` (25 págs)**

| Tema | Pág orig. | Pág PDF |
|------|-----------|---------|
| **5 preguntas fundamentales** del diseño sísmico | 117 | 1 |
| **Condiciones del diseño**: resistencia, rigidez, durabilidad, ductilidad | 118 | 2 |
| **Matriz de rigidez de un edificio** (resumen) | 119 | 3 |
| Casos especiales | 120-121 | 4-5 |
| **Edificios con 1 eje de simetría** | 122 | 6 |
| **Edificios con 2 ejes de simetría** | 123 | 7 |
| **Comportamiento edificio durante sismo** (conceptualización) | 124 | 8 |
| **Análisis Pushover**: definición, curva V-Δtecho | 125 | 9 |
| **Curva Corte basal vs Desplazamiento techo**: Qe, Qnl, Q1era rótula, Qdiseño | 126 | 10 |
| **Composición R* = FSRE × FIRNL × FDED** | 127 | 11 |
| FSRE = sobrerresistencia elástica = Q1era/Qdiseño | 127 | 11 |
| FIRNL = incursión rango no lineal = Qnl/Q1era | 127 | 11 |
| FDED = diferencia desempeño elástico-inelástico = Qe/Qnl | 127 | 11 |
| **μ = ductilidad global** = Δnl/Δ1era | 127 | 11 |
| Comentarios: Qnl ≈ (1.9 a 3.0) × Qdiseño | 128 | 12 |
| **Interpretación filosofía norma chilena** con curva pushover | 129 | 13 |
| Sismo moderado → OB, mediano → OB/BC, severo → daños pero no colapso | 129 | 13 |
| **ASCE/SEI 7-16**: R = Rμ × Ω0 | 131 | 15 |
| **Ejemplo edificio 15+1 pisos Antofagasta** | 132-137 | 16-21 |
| Tabla análisis sísmico completa | 136 | 20 |
| **Espectro diseño Rx*=4.32, Ry*=4.85** | 137 | 21 |
| **Dónde se producen daños**: vigas (marcos), dinteles (muros) | 138 | 22 |
| **Columna fuerte – viga débil** | 138 | 22 |
| Consideraciones especiales HA: confinamiento, detallamiento | 138-139 | 22-23 |
| Diseño muros: DS60 + ACI318, desplazamiento diseño DS61 | 139 | 23 |
| **Visión integral diseño edificio** | 140 | 24 |
| Análisis complementarios recomendados | 140-141 | 24-25 |

### 2f) Perfil Bio-Sísmico e Indicadores Estructurales
**Archivo: `02f-Perfil-Biosismico.pdf` (27 págs)**

| Tema | Pág orig. | Pág PDF |
|------|-----------|---------|
| Origen: Guendelman, Guendelman & Lindenberg, 585 edificios | 141 | 1 (último de 2e, en realidad comienza aquí) |
| **INDICADOR 1: H total / Periodo 1er modo traslacional** | 142 | 1 |
| **INDICADOR 2: Efecto P-Δ** (Mv_PΔ / Mv_sísmica) | 143 | 2 |
| **INDICADOR 3: Desplazamiento nivel superior** (δ/H ≤ 1/1000) | 144 | 3 |
| **INDICADOR 4: Máx drift entrepisos en CM** (≤ 0.002) | 145 | 4 |
| **INDICADOR 5: Máx drift entrepisos en puntos extremos** (≤ 0.001) | 146 | 5 |
| **INDICADOR 6: Periodo rotacional / periodo traslacional** | 147 | 6 |
| Acoplamiento modal, sintonía, error hasta 30% | 147 | 6 |
| Frecuencias modos rotac/traslac alejarse 20% | 147 | 6 |
| **INDICADOR 7: Masa rotacional acoplada / masa traslacional directa** | 148 | 7 |
| Transformación masa rotacional → traslacional equivalente | 149 | 8 |
| **INDICADOR 8: Excentricidad dinámica / radio giro basal** | 150 | 9 |
| **INDICADOR 9: Masa traslacional acoplada / masa traslacional directa** | 151 | 10 |
| **INDICADOR 10: Corte basal acoplado / corte basal directo** | 152 | 11 |
| **INDICADOR 11: Momento volcante basal acoplado / Mv directo** | 153 | 12 |
| **INDICADOR 12: Nº elementos relevantes en la resistencia** (≥ 3 ejes) | 154 | 13 |
| **INDICADOR 13: R** (factor reducción espectral efectivo)** | 155 | 14 |
| **Artículo científico**: Índices estructurales edificios altos Antofagasta (Soto & Music) | 156-161 | 15-20 |
| Niveles demanda sísmica (tabla periodo retorno) | 158 | 17 |
| Densidad muros: Aw/Pf y Aw/Aacumulada | 159 | 18 |
| Resultados 8 edificios Antofagasta (Tx*, Ty*, δ) | 160 | 19 |
| Conclusiones del estudio | 161 | 20 |
| **Puntos débiles del edificio**: analizar modos, CM/CR, acoplamiento | 162 | 21 |
| Análisis complementarios: cambios bruscos, empotramiento, P-Δ | 163 | 22 |
| Proceso constructivo en análisis | 163 | 22 |
| Elementos no estructurales | 164 | 23 |
| **Análisis no lineal**: pushover, MEC, N2 | 164 | 23 |
| **Tendencia futura: diseño basado en desempeño** | 165 | 24 |
| VISION 2000 (SEAOC), ATC-40, FEMA | 165 | 24 |
| Niveles de desempeño, demanda sísmica, objetivos | 165 | 24 |
| **Cómo disminuir vulnerabilidad**: constructores, arquitectos, autoridades, usuarios | 166-168 | 25-27 |

---

## CAPÍTULO 3: DISEÑO DE MUROS DE HORMIGÓN ARMADO

### 3a) Evolución Normativa y Modos de Falla
**Archivo: `03a-Muros-Normativa-y-Fallas.pdf` (13 págs)**

| Tema | Pág orig. | Pág PDF |
|------|-----------|---------|
| Portada Cap 3 | 169 | 1 |
| **Evolución normativa sísmica Chile** para muros | 170-171 | 2-3 |
| NCh433 Of.1996 → NCh433 Mod.2009 → DS60/DS61 | 171 | 3 |
| **2) Modos de falla en muros HA** | 172 | 4 |
| Falla por corte, flexión, deslizamiento (figuras) | 172-173 | 4-5 |
| **2.2 Efecto del confinamiento** | 174-175 | 6-7 |
| Respuesta frágil sin confinamiento | 176 | 8 |
| **2.3 Daños terremoto 27F-2010** en edificios chilenos | 176-177 | 8-9 |
| Fotos: falta confinamiento, ausencia elementos de borde | 177 | 9 |
| Estribos insuficientes, ganchos mal ejecutados | 177 | 9 |
| **3) Diferencias diseño muros antes/después 27F** | 179-181 | 11-13 |
| Antes: NCh430 Of.2008 (ACI318-05) | 179 | 11 |
| Después: DS60 (ACI318-08) + DS61 | 179 | 11 |
| Etiquetado muros ETABS: Pier 1, Pier 2 | 180-181 | 12-13 |

### 3b) Diseño de Muros: Corte, Flexión Compuesta, Curvatura, Confinamiento
**Archivo: `03b-Muros-Diseno-Corte-Flexion-Confinamiento.pdf` (56 págs)**

| Tema | Pág orig. | Pág PDF |
|------|-----------|---------|
| **4) Diseño de muros HA** | 182 | 1 |
| **Tipos**: especiales (R=7, Ro=11) y ordinarios (≤5 pisos, R≤4) | 182 | 1 |
| **Estados de carga NCh3171** para muros | 182 | 1 |
| **iii) Diseño muros estructurales especiales** | 183 | 2 |
| Procedimiento: a) esbeltez, b) compresión, c) corte, d) flexión, e) curvatura | 183 | 2 |
| **a) Verificación esbeltez**: t > lu/16 → no pandeo | 184 | 3 |
| **b) Carga máxima compresión: Pu ≤ 0.35 f'c × Ag** | 184 | 3 |
| **c) DISEÑO AL CORTE** | 185-189 | 4-8 |
| Armadura transversal continua (ACI 21.9.2.1) | 185 | 4 |
| Espaciamiento ≤ 3t ni 45cm | 185 | 4 |
| **Resistencia: Vn ≤ 0.83√f'c × Acv** (muros especiales) | 185 | 4 |
| **Aporte hormigón Vc**: forma simplificada (0.53λ√f'c × bw×d) | 186 | 5 |
| Nu positivo (compresión) y negativo (tracción) | 186 | 5 |
| d = 0.8 × lw | 186 | 5 |
| Forma detallada de Vc | 187 | 6 |
| **Vc ≤ αc × √f'c × Acv** | 187 | 6 |
| **Limitaciones Vs**: armadura mín/máx | 187 | 6 |
| **Diagrama de flujo diseño al corte** | 188 | 7 |
| Ah/s = ρt × h × 100 (cm²/m) | 188 | 7 |
| Armadura vertical y horizontal distribuida (figura) | 189 | 8 |
| **d) DISEÑO A FLEXIÓN COMPUESTA** | 190-204 | 9-23 |
| Distribución tensiones y deformaciones | 190 | 9 |
| **Φ×Mn ≥ Mu, Φ×Nn ≥ Nu, Φ×Vn ≥ Vu** | 190 | 9 |
| **Factor reducción Φ** y **β1** | 191 | 10 |
| **Diagrama de interacción** (ejemplo gráfico) | 192 | 11 |
| Art. 21.9.5.2: secciones compuestas (L, T, C) → sección completa | 193 | 12 |
| Ancho efectivo ala: menor entre 0.5×dist y 0.25×Ht | 193 | 12 |
| **Signos cargas sísmicas**: 4 subcombinaciones por estado de carga | 194 | 13 |
| +P(E)+M3(E), +P(E)-M3(E), -P(E)+M3(E), -P(E)-M3(E) | 194 | 13 |
| Ejemplo con ETABS: M2, M3 positivos | 195 | 14 |
| **Ejemplo chequeo sección completa** (diagrama interacción) | 196-203 | 15-22 |
| **Sección crítica**: zona donde ocurre incursión inelástica | 204 | 23 |
| Posibles secciones críticas en X e Y | 204 | 23 |
| **e) VERIFICACIÓN CURVATURA Y CONFINAMIENTO** | 205-237 | 24-56 |
| **e1) Verificación curvatura** (Art. 21.9.5.4) | 205 | 24 |
| Ht/lw ≥ 3 → demanda ≤ capacidad curvatura | 205 | 24 |
| Ht = distancia último nivel significativo a sección crítica | 205 | 24 |
| Demostración ecuación 21-7b | 207 | 26 |
| Demostración ecuación 21-7a | 211 | 30 |
| **Desplazamiento de diseño δu** (tabla ejemplo Antofagasta) | 212 | 31 |
| **Espectro de desplazamiento elástico** (gráfico) | 213 | 32 |
| **Capacidad curvatura: φ = 0.008/c** | 214 | 33 |
| **Curva momento-curvatura** de la sección | 214 | 33 |
| Verificaciones εc=0.008 y εc=0.003 | 215-216 | 34-35 |
| **e2) Verificación elementos de borde** | 217 | 36 |
| **c ≥ clim → requiere confinamiento** | 217 | 36 |
| δu' = desplazamiento relativo de diseño | 217 | 36 |
| **Largo a confinar: cc = c - clim** | 218 | 37 |
| **Espesor elemento borde ≥ 30cm**, largo ≥ espesor muro | 218 | 37 |
| **Altura a confinar: máx(lw, Mu/4Vu)** | 218 | 37 |
| ¿Cómo determinar "c" (eje neutro)? | 219-221 | 38-40 |
| **Resumen aplicación DS60** | 222 | 41 |
| Verificación compresión media (todos muros, todos niveles) | 222 | 41 |
| Verificación confinamiento (muros esbeltos, secciones críticas) | 223 | 42 |
| **Armadura confinamiento: Ash = 0.09×s×bc×f'c/fyt** | 224 | 43 |
| Detalle armadura confinamiento (figuras) | 225-226 | 44-45 |
| **5) RESUMEN DETALLAMIENTO ARMADURAS MUROS** | 227-237 | 46-56 |
| Caso muros que requieren confinamiento | 228 | 47 |
| **h ≥ 30cm y Cc ≥ h** cuando c ≥ clim | 229 | 48 |
| Art. 21.9.6.5: muros sin confinamiento con ρ > 28/fy | 230-232 | 49-51 |
| **Distribución vertical armadura confinamiento** | 233 | 52 |
| Armadura mínima de borde ACI318-2019 | 234 | 53 |
| **Traslapos** (figuras detalladas) | 236-237 | 55-56 |

### 3c) Predimensionamiento y Ejemplo
**Archivo: `03c-Muros-Predimensionamiento-y-Ejemplos.pdf` (12 págs)**

| Tema | Pág orig. | Pág PDF |
|------|-----------|---------|
| **Fotos muros reales** (René Lagos Engineers) | 238-242 | 1-5 |
| **7) Predimensionamiento espesores muros** | 243 | 6 |
| Requisito corte: Vs ≤ 0.66√f'c × bw×d (ACI 11.4.7.9) | 243 | 6 |
| Vc = 0.17√f'c × bw×d | 243 | 6 |
| Criterio diseño: Vs ≤ Vc (recomendado) o Vs ≤ 2Vc (límite) | 244 | 7 |
| τlim = (0.6/1.4) × 2τc | 244 | 7 |
| **Ejemplo edificio 16 pisos + subterráneo** | 246-249 | 9-12 |
| Cubicación peso sísmico | 246-247 | 9-10 |
| Qmín, Qmáx, elección corte diseño | 248 | 11 |
| Áreas muros: Ax=15.74m², Ay=17.57m² | 248 | 11 |
| **Otras disposiciones predimensionamiento (DS60)** | 249 | 12 |
| Espesor ≥ hwi/16 | 249 | 12 |
| Ancho efectivo alas ≤ min(0.5×dist, 0.25×hw) | 249 | 12 |
| Carga axial ≤ 0.35×f'c×Ag | 249 | 12 |
| Espesor ≥ 30cm si requiere confinamiento | 249 | 12 |

---

## CAPÍTULO 4: DISEÑO SÍSMICO DE MARCOS ESPECIALES DE HORMIGÓN ARMADO
**Archivo: `04-Marcos-Especiales-HA.pdf` (32 págs)**

### 4.1 Vigas de marcos especiales (págs 250-261)
| Tema | Pág orig. | Pág PDF |
|------|-----------|---------|
| Introducción: elementos a flexión en marcos especiales | 250 | 1 |
| Unidades MKS (ACI) y SI en anexo | 250 | 1 |
| **4.1.1 Condiciones geométricas vigas** | 250 | 1 |
| Pu < Ag×f'c/10 | 251 | 2 |
| bw ≥ 25cm, bw ≤ C2 + menor(C2, 0.3h) | 251 | 2 |
| Ln ≥ 0.75×C1 | 251 | 2 |
| Fig. 4.1: resumen condiciones geométricas | 251 | 2 |
| Fig. 4.2 (R21.5.1 ACI): determinación C1, C2 | 252 | 3 |
| **4.1.2 Diseño armadura longitudinal vigas** | 253 | 4 |
| M⁻ cara nudo ≥ mayor Mu de estados de carga | 253 | 4 |
| M⁺ cara nudo ≥ 0.5 × M⁻ | 253 | 4 |
| M cualquier sección ≥ 0.25 × Mmáx cara nudo | 253 | 4 |
| **Armadura mínima y máxima longitudinal** | 253 | 4 |
| Detallamiento: 2 barras continuas sup/inf | 254 | 5 |
| No traslapes: dentro nudos, distancia s1, zonas fluencia | 254 | 5 |
| Fig. 4.3: resumen diseño armadura longitudinal | 254 | 5 |
| **4.1.3 Diseño armadura transversal vigas** | 255 | 6 |
| Corte diseño NO del análisis, sino de **rótulas plásticas** | 255 | 6 |
| **Ve basado en Mpr** (momento probable) con 1.25fy | 255-256 | 6-7 |
| Art. 21.5.4.1: Ve entre caras de nudo | 256 | 7 |
| Fig. R21.5.4: cortante diseño vigas y columnas | 256 | 7 |
| Fórmulas: ΦVn ≥ Ve, Vs máx/mín | 257 | 8 |
| **Zona rótula plástica s1 = 2h** | 258 | 9 |
| Espaciamiento: d/4, 8db(long), 24db(cerco), 300mm | 258 | 9 |
| Primer cerco a ≤ 50mm de cara apoyo | 258 | 9 |
| Fig. 4.4: diseño a corte en vigas | 259 | 10 |
| Fig. 4.5: detallamiento armadura vigas sismorresistentes | 260 | 11 |
| s2 ≤ d/2 (fuera zona rótula) | 260 | 11 |
| s3 ≤ mín(d/4, 100mm) en zona empalme | 260 | 11 |
| **Ganchos sísmicos**: 135°, cercos traslapados | 261 | 12 |

### 4.2 Columnas de marcos especiales (págs 262-272)
| Tema | Pág orig. | Pág PDF |
|------|-----------|---------|
| Condiciones: Pu > Ag×f'c/10 | 262 | 13 |
| b ≥ 300mm, b/h ≥ 0.4 | 263 | 14 |
| Fig. 4.7: condiciones geométricas columnas | 263 | 14 |
| **4.2.2 Armadura longitudinal columnas** | 264 | 15 |
| Verificar columna corta o esbelta | 264 | 15 |
| Diagramas de interacción o programa | 264 | 15 |
| **ρmín = 0.01, ρmáx = 0.06** | 264 | 15 |
| Traslapes: solo mitad central, dimensionados en tracción | 265 | 16 |
| **4.2.3 Armadura transversal columnas** | 265 | 16 |
| **Zona crítica l0**: mayor de h, lu/6, 450mm | 265 | 16 |
| **Confinamiento**: Ash = 0.09×s×bc×f'c/fyt (o fórmula Ag/Ach) | 266 | 17 |
| Para zunchos/espirales | 266 | 17 |
| **Corte diseño columnas: Ve = (Mpr1+Mpr2)/lu** | 267 | 18 |
| Mpr con 1.25fy, máxima capacidad flexión | 267 | 18 |
| Vs máx/mín, armadura Av por corte | 268 | 19 |
| **Espaciamiento zona crítica**: b/4, 6db, (350+100-hx)/3 | 268 | 19 |
| hx y sx en mm | 268 | 19 |
| Trabas ≤ 350mm centro a centro | 269 | 20 |
| Fig. 4.8: parámetros armadura transversal columnas | 270 | 21 |
| Fig. 4.9: esfuerzo corte diseño columnas | 271 | 22 |
| Fig. 4.10: arreglos admisibles refuerzo | 271 | 22 |
| Fig. 4.11: detallamiento completo columnas sismorresistentes | 272 | 23 |

### 4.3 Columna fuerte – Viga débil (págs 273-274)
| Tema | Pág orig. | Pág PDF |
|------|-----------|---------|
| **ΣMnc ≥ (6/5) × ΣMnb** (ecuación 21.1) | 273 | 24 |
| Ejemplo Caso 1: sismo dirección X | 274 | 25 |

### 4.4 Resistencia al corte en el nudo (págs 275-281)
| Tema | Pág orig. | Pág PDF |
|------|-----------|---------|
| Definición de nudo: parte columna dentro altura viga | 275 | 26 |
| **Vn nudo confinado 4 caras: 1.7√f'c × Aj** | 276 | 27 |
| **Vn nudo confinado 3 caras: 1.25√f'c × Aj** | 276 | 27 |
| **Vn otros: 1.0√f'c × Aj** | 276 | 27 |
| **Φ = 0.85** para corte en nudos | 276 | 27 |
| **Cálculo Vx-x en sección del nudo** | 277 | 28 |
| Fig. 4.13: diseño a corte en nudos | 277 | 28 |
| Tabla resumen ACI318-2008: marcos ordinarios/intermedios/especiales | 280 | 31 |
| Fórmulas en distintas unidades (SI, MKS, inglés) Cap 21 ACI | 281 | 32 |

---

## CAPÍTULO 5: ANÁLISIS ESTRUCTURAL (ACI318-2019) Y PROBLEMAS

### 5a) Análisis Estructural ACI318-2019 Cap 6
**Archivo: `05a-Analisis-Estructural-ACI318.pdf` (16 págs)**

| Tema | Pág orig. | Pág PDF |
|------|-----------|---------|
| Cap 6 ACI318-2019: análisis estructural | 282 | 1 |
| **Diagrama flujo esbeltez columnas** | 284 | 3 |
| **Análisis lineal elástico 1er orden** | 287 | 6 |
| Método magnificación momentos | 287 | 6 |
| Sistema MKS | 292 | 11 |
| **Análisis lineal elástico 2do orden** | 294 | 13 |
| Efecto esbeltez a lo largo columna | 294 | 13 |
| **Análisis inelástico** (1er y 2do orden) | 296 | 15 |
| **Análisis elementos finitos** | 297 | 16 |

### 5b) Problemas Propuestos
**Archivo: `05b-Problemas-Propuestos.pdf` (24 págs)**

| Problema | Pág orig. | Pág PDF | Tema |
|----------|-----------|---------|------|
| **Prob 1** | 298 | 1 | Edificio 1 piso, marcos HA, diafragma rígido: rigidez rotacional, matriz rigidez, corte basal máx |
| **Prob 2** | 299 | 2 | Edificio con ala nueva: asimetría, CM/CR, torsión, corte en muros |
| **Prob 3** | 300 | 3 | Edificio 5 pisos, marcos HA, Antofagasta: Vs30, tipo suelo, método estático, fuerzas por piso |
| **Prob 4** | ~301 | ~4 | (continúa serie problemas tipo control) |
| Prob 5-16+ | 302-321 | 5-24 | Problemas adicionales de análisis sísmico y diseño |

---

## RESUMEN DE FÓRMULAS CLAVE (referencia rápida)

| Fórmula | Descripción | Pág | Archivo |
|---------|-------------|-----|---------|
| Qo = C × I × P | Corte basal estático | 89 | 02c |
| C = (2.75·S·Ao)/(g·R)·(T'/T*)^n | Coeficiente sísmico | 89 | 02c |
| (Ao·S)/(6g) ≤ C ≤ Cmáx | Límites coef. sísmico | 89 | 02c |
| Sa = (S·Ao·α)/(R*/I) | Espectro diseño | 102 | 02d |
| R* = FSRE × FIRNL × FDED | Composición factor reducción | 127 | 02e |
| Pu ≤ 0.35·f'c·Ag | Compresión máx muros | 184 | 03b |
| Vn ≤ 0.83√f'c·Acv | Resistencia corte muros especiales | 185 | 03b |
| Vc = 0.53λ√f'c·bw·d | Aporte hormigón al corte (simple) | 186 | 03b |
| d = 0.8·lw | Peralte efectivo muro | 186 | 03b |
| Φ·Mn ≥ Mu | Diseño flexión | 190 | 03b |
| φu = 0.008/c | Capacidad curvatura | 214 | 03b |
| c ≥ clim → confinar | Requerimiento elem. borde | 217 | 03b |
| cc = c - clim | Largo a confinar | 218 | 03b |
| Ash = 0.09·s·bc·f'c/fyt | Armadura confinamiento | 224 | 03b |
| Ve = (Mpr1+Mpr2)/lu | Corte diseño columnas | 267 | 04 |
| ΣMnc ≥ 1.2·ΣMnb | Columna fuerte-viga débil | 273 | 04 |

---

## DATOS DEL TALLER (Enunciado Taller.pdf)

### Edificio 1 — Muros (20 pisos)
- Antofagasta, Zona 3 (Ao=0.4g), Suelo C, Oficina (Cat II, I=1.0)
- H°A° G30 (f'c=300 kgf/cm²), Acero A630-420H (fy=4200 kgf/cm²)
- Piso 1: 3.4m, pisos 2-20: 2.6m → Htotal = 3.4 + 19×2.6 = 52.8m
- Ec = 4700√30 = 25742 MPa ≈ 257420 kgf/cm²
- γ_HA = 2.5 tonf/m³, g = 9.81 m/s²
- Vigas invertidas 20×60cm, Losas 15cm
- Muros Y (e=30cm): ejes 1,3,4,5,7,12,13,14,16,17; resto e=20cm
- Muros X (e=30cm): eje C entre 3-6 y 10-14; resto e=20cm
- SC oficinas: 250 kgf/m², SC pasillos: 500 kgf/m², SC techo: 100 kgf/m²
- Terminaciones piso: 140 kgf/m², terminaciones techo: 100 kgf/m²

### Edificio 2 — Marcos (5 pisos)
- Antofagasta, Zona 3, Suelo C, Oficina
- H°A° G25 (f'c=250 kgf/cm²), Acero A630-420H
- Planta 32.5×32.5m (5 vanos × 6.5m en ambas dirs)
- Piso 1: 3.5m, pisos 2-5: 3.0m → Htotal = 3.5 + 4×3.0 = 15.5m
- Ec = 4700√25 = 23500 MPa
- Pisos 1-2: Col 70×70, Vigas 50×70, Losa 17cm
- Pisos 3-5: Col 65×65, Vigas 45×70, Losa 17cm
- Cachos rígidos: factor 0.75 automático
- SC piso: 300 kgf/m², SC techo: 100 kgf/m²
- Terminaciones piso: 140 kgf/m², techo: 100 kgf/m²

### Evaluación Taller
- **Parte 1**: Análisis sísmico (peso, densidad muros, CM/CR, periodos, corte basal, espectros, deformaciones, 6 casos torsión)
- **Parte 2 Ed.1**: Diseño muros eje 5 (rectangular) y eje 4 (T) en piso 1
- **Parte 2 Ed.2**: Diseño vigas y columnas marco eje A (manual + ETABS)

### Evaluación Curso
- **NF = 0.7×NC + 0.3×NTaller**
- NC = 0.20×C1 + 0.40×C2 + 0.40×C3
- C1: Sismología (sem 1-3)
- C2: Bases diseño + análisis sísmico (sem 4-8)
- C3: Diseño muros + marcos (sem 12-17)
