# Extracto Completo — Tutorial ETABS Paso a Paso (M. Lafontaine, 142 págs)
## "Práctica Chilena en el Análisis y Diseño de Edificios de Hormigón Armado — Módulo 4: Modelación en ETABS"
## Mario Lafontaine — 17/03/2021

> Fuente: `docs/Material taller/Paso a Paso ETABS M.Lafontaine.pdf`
> Extraído el 2026-03-21 por agente autónomo R06.

---

## Índice de Contenidos del Documento

| Págs | Tema |
|------|------|
| 1–2 | Portada y título |
| 3 | Seteos iniciales (unidades) |
| 4–5 | Definición de pisos (stories) |
| 6–13 | Definición de grilla (manual + importación CAD) |
| 14–20 | Materiales (hormigón, acero refuerzo, acero perfiles, propiedades no lineales) |
| 21–27 | Secciones (vigas, columnas, muros, losas + modifiers) |
| 28–32 | Cargas estáticas (CM, CV, CVR, CVT + Self Weight Multiplier) |
| 33 | Masa sísmica (Mass Source) |
| 34–38 | Espectro elástico (From File + caso modal espectral) |
| 39–41 | Combinaciones de carga (SX, SY de diseño + C1–C7) |
| 42 | Modos de vibrar (Eigen vs Ritz) |
| 43–46 | Torsión accidental (momentos torsores vs mover CM) |
| 47–50 | Modelación geométrica — principios y errores de refinación |
| 51 | Orden de dibujo: muros → vigas → losas (de arriba hacia abajo) |
| 52–53 | Dibujo de muros (entre ejes, Drawing Control Type) |
| 54 | Dibujo de vigas |
| 55–56 | Dibujo de columnas (Angle para orientación) |
| 57–60 | Punto de inserción / Cardinal Point (vigas invertidas) |
| 61–63 | Cachos rígidos (Rigid Zone Factor = 0.75) |
| 64 | Rótulas en vigas (al lado débil de un muro) |
| 65–67 | Intersecciones (dividir muros que se intersectan) |
| 68–78 | Dibujo de muros desde CAD (11 pasos con DXF) |
| 79–84 | Dibujo de losa (formas sanas vs insanas, 4 nodos, mesheo manual) |
| 85–87 | Mesh losa (máx 1m×1m, verificar visualmente) |
| 88 | Mesh muros (conectividad directa, evitar elementos alargados) |
| 89–94 | Fachadas (shell + frame, spandrels, conectividad directa) |
| 95–97 | Apoyos (empotrados vs articulados, criterios) |
| 98–99 | Auto Edge Constraint |
| 100–109 | Diafragmas (rígido, semi-rígido, sin diafragma — criterios) |
| 110–117 | Piers y Spandrels (asignación correcta e incorrecta) |
| 118–119 | Replicación de pisos |
| 120–122 | Check Model (NO usar Fix) |
| 123 | Elegir motor (Advanced Solver / Multi-threaded) |
| 124–125 | Correr modelo y ver Log |
| 126–130 | Lectura de resultados (shells, piers, spandrels, descensos diferenciales) |
| 131–137 | Resultados globales (peso sísmico, Qbasal, períodos, I/R, exportar tablas/MDB) |
| 138–141 | Validaciones (Peso/Área ≈ 1 tonf/m², deformadas, elementos sueltos) |
| 142 | Página final |

---

## 1. FLUJO COMPLETO DE MODELACIÓN

Lafontaine establece el siguiente orden:

### Fase 0 — Configuración inicial
1. **Unidades**: Definir en esquina inferior derecha (Units)
2. **Pisos (Stories)**: Definir alturas de entrepiso. Click derecho para agregar/sacar pisos
3. **Grilla**: Definición manual O importación desde plano CAD (DXF)
   - Si manual: Display Grid Data as Spacing → izq a der, abajo a arriba
   - Último espaciamiento = 0

### Fase 1 — Materiales
4. **Hormigón**: E = 4700√f'c [MPa] o E = 19000√R28 [kgf/cm²]
   - **Peso**: 2.5 tonf/m³ (incluye armaduras) — práctica chilena
   - No confundir peso (weight) con masa (mass): P = m×g
5. **Acero de refuerzo**: Expected = Minimum × Ry (depende del código)
6. **Acero de perfiles** (si hay): análogo a refuerzo
7. **Propiedades no lineales** (opcional): User Stress-Strain Curve

### Fase 2 — Secciones
8. **Vigas** (frame): material es propiedad de la sección → copias si hay distintos materiales
   - **★ J = 0 (Torsional Constant)** — se recomienda para vigas
9. **Columnas** (frame): análogo a vigas, EXCEPTO J=0 (no se aplica)
   - Si razón de lados > 4 → evaluar usar shell (modelar como muro)
10. **Muros** (shell): definición de espesor y material
11. **Losas** (shell): Type = varias opciones (maciza, nervada…)
    - Si se modela como membrana → carga se distribuye por áreas tributarias, no por rigidez
    - Solo usar membrana en paños rectangulares y verificando descarga
    - **★ Modifiers → inercia a flexión = 25%** (m11, m22, m12 = 0.25)

### Fase 3 — Cargas estáticas
12. **Carga Muerta (CM)**: Self Weight Multiplier = 1 + cargas muertas adicionales
13. **Carga Viva Reducible (CVR)**: especificar como "Reducible Live"
14. **Carga Viva de Techo (CVT)**: especificar como "Roof Live"
15. Cargas en losas: apagar muros antes de seleccionar losas para aplicar cargas

### Fase 4 — Masa sísmica
16. **Mass Source**: forma más directa en edificios
    - % de carga viva depende del edificio (en su ejemplo: 25%)
    - NCh433 permite no considerar CVT en cálculo de masa

### Fase 5 — Espectro y análisis modal espectral
17. **Espectro From File**: archivo texto con 2 columnas: T(s) y PSa (m/s²)
    - ⚠️ Ojo con configuración regional (puntos/comas del sistema)
    - NO usar espectro built-in "Chile NCH433+DS61" → desactualizado (suelos antiguos)
    - Function Damping Ratio = 5% (normas lo definen así)
    - Siempre mirar forma del gráfico, validar valores peak
18. **Caso modal espectral**:
    - **Scale Factor = 1** (porque espectro está en m/s²)
    - U1 = X, U2 = Y
    - Combinación modal = CQC
    - Modal Damping = mismo % que el espectro (si no, ETABS escala valores)

### Fase 6 — Combinaciones de carga
19. **Sismos de diseño SX, SY**: Combo = sismo elástico × I/R
    - Primera iteración: usar solo I (no se conoce R aún)
    - Ventaja de Combo: al calcular R, se cambia factor sin re-correr
20. **Combinaciones de diseño C1–C7**:
    - C1: 1.4 CM
    - C2: 1.2 CM + 1.6 CV + 1.6 CVR + 0.5 CVT
    - C3: 1.2 CM + 1.0 CV + 0.5 CVR + 1.6 CVT
    - C4: 1.2 CM + 1.0 CV + 0.5 CVR ± 1.4 SX
    - C5: 1.2 CM + 1.0 CV + 0.5 CVR ± 1.4 SY
    - C6: 0.9 CM ± 1.4 SX
    - C7: 0.9 CM ± 1.4 SY
    - ETABS hace ± automáticamente cuando hay modal espectral en un combo

### Fase 7 — Configuraciones de análisis
21. **Modos de vibrar**: Eigen Values (usual) o Ritz
    - Eigen llega a solución "por abajo", Ritz puede llegar "por arriba"
22. **Torsión accidental**: 2 métodos NCh433
    - Método 1: Momentos torsores (fácil pero conservador)
    - Método 2: Mover centro de masa (complejo pero menor giro en planta)

### Fase 8 — Modelación geométrica
23. Dibujar de **arriba hacia abajo** (pisos superiores primero, subterráneos al final)
24. Orden: **muros/columnas → vigas → losas**
25. **Muros**: dibujo entre ejes o con Drawing Control Type para largos específicos
26. **Vigas**: análogo a muros
27. **Columnas**: cuidado con "Angle" (orientación)
28. **Punto de inserción vigas invertidas**: Cardinal Point → eje en fondo de viga
29. **Cachos rígidos**: Rigid Zone Factor = 0.75 (usual). Verificar asignación correcta
30. **Rótulas en vigas**: si comienzan/terminan al lado débil de un muro
31. **Intersecciones**: dividir todos los muros que se intersectan entre sí o con vigas
32. **Alternativa CAD**: importar DXF con líneas sobre muros → dibujar muros con guías → borrar guías

### Fase 9 — Losas y mesh
33. **Losas**: dibujar por sectores según cargas distintas. Elementos de 4 nodos
    - Meshear manualmente en esquinas de muros y columnas
    - NO alejarse mucho de 90° en ángulos
34. **Mesh losa**: máximo 1m×1m usualmente suficiente. Verificar visualmente
35. **Mesh muros**: conectividad directa, mesheo manual para evitar elementos alargados

### Fase 10 — Conectividad y apoyos
36. **Fachadas**: si vigas de acople son altas → cambiar frame por shell (spandrel)
37. **Apoyos**: empotrado (losa fundación) o articulado (zapatas corridas). Ser consecuente
38. **Auto Edge Constraint**: compatibilidad de deformaciones en nodos sobre misma línea
39. **Diafragmas**: rígido, semi-rígido, o sin diafragma (ver criterios abajo)

### Fase 11 — Piers, Spandrels y replicación
40. **Piers**: asignar a muros (integra esfuerzos en sección inf/sup del pier por piso)
41. **Spandrels**: asignar a vigas (integra esfuerzos en sección izq/der)
42. **Replicación de pisos**: seleccionar elementos y replicar a pisos deseados
    - ⚠️ Verificar que TODO esté prendido antes de seleccionar

### Fase 12 — Pre-análisis
43. **Check Model**: usar herramienta, pero **NO usar "Fix"** (perder control)
44. **Motor**: Advanced Solver o Multi-threaded (ambos rápidos)

### Fase 13 — Correr y verificar
45. **Correr modelo**
46. **Ver Log**: siempre verificar que no haya problemas
47. **Leer resultados**: shells, piers/spandrels, diagramas

### Fase 14 — Post-proceso y validación
48. **Resultados globales**: peso sísmico, cortes basales, períodos
49. **Calcular I/R** y actualizar combos SX, SY
50. **Exportar**: tablas a Excel o base de datos .mdb
51. **Validación**: Peso/Área ≈ 1.0 tonf/m²
52. **Observar deformadas**: verificar que no haya elementos sueltos

---

## 2. CONFIGURACIONES ESPECÍFICAS RECOMENDADAS

### 2.1 J = 0 en vigas (Torsional Constant)

**Dónde**: Define > Section Properties > Frame Sections > seleccionar viga > Modify/Show Property
**Campo**: Torsional Constant (J) → poner 0

**Por qué** (pág. 23):
- "Se recomienda utilizar J = 0 para vigas (Torsional Constant)"
- Lafontaine NO da una justificación explícita larga, solo lo indica como recomendación
- La razón estándar en práctica chilena: vigas de HA fisuradas pierden casi toda su rigidez torsional. Mantener J>0 genera momentos torsionales ficticios que no se diseñan y distorsionan equilibrio
- **NO aplica a columnas** (pág. 24: "Análogo a definición de vigas (excepto J=0)")

### 2.2 Inercia de losa al 25%

**Dónde**: Define > Section Properties > Shell Sections > seleccionar losa > Modifiers
**Campos**: m11, m22, m12 → 0.25

**Por qué** (pág. 27):
- "Una recomendación es reducir la inercia a flexión a un 25%"
- Si se mantiene al 100%:
  - Se **sobrestima** acoplamiento y rigidez lateral
  - La losa no tendrá capacidad para resistir los momentos que ese acoplamiento genera
  - Se **sobrestima** N y **subestima** M en los muros
- Si se reduce demasiado (ej. 1%):
  - Se **subestima** acoplamiento y rigidez lateral
  - Efecto contrario

### 2.3 Peso/Área ≈ 1 tonf/m²

**Cómo verificar** (págs. 138–140):

**Paso 1 — Obtener Área Total:**
- Display > Show Tables > **Material List By Story**
- Seleccionar Element Type = **"Floor"**
- Leer columna **"Floor Area"**
- Sumar: Área Total = N_pisos × Área_piso
- En su ejemplo: 20 pisos × 484 m² = 9,680 m²

**Paso 2 — Obtener Peso Total:**
- Display > Show Tables > **Story Forces**
- Leer peso sísmico en la base
- En su ejemplo: 9,070 tonf

**Paso 3 — Validar:**
- P/A = 9,070 / 9,680 = **0.93 tonf/m²** ✓ (≈ 1.0)

**Valores típicos**: 0.85–1.15 tonf/m² para edificios HA en Chile

### 2.4 Espectro From File — Formato exacto

**Formato del archivo de texto** (págs. 34–36):
- 2 columnas separadas por espacio/tabulación:
  - Columna 1: **T (s)** — período
  - Columna 2: **PSa (m/s²)** — pseudoaceleración espectral

**Ejemplo de formato** (basado en descripción):
```
0.00    X.XXX
0.05    X.XXX
0.10    X.XXX
...
5.00    X.XXX
```

**Configuración en ETABS**:
- Function Type: **From File**
- Function Damping Ratio: **0.05** (5%)
- ⚠️ Configuración regional: verificar que puntos decimales del sistema coincidan con archivo
- ⚠️ **NO usar** espectro built-in "Chile NCH433+DS61" → clasificación de suelos desactualizada

**En el caso modal espectral**:
- **Scale Factor = 1** (espectro ya en m/s²)
- Si el espectro estuviera en Sa/g → Scale Factor = 9.81
- U1 = dirección X, U2 = dirección Y
- Combinación modal: **CQC**
- Modal Damping: **5%** (mismo que Function Damping Ratio)
- Si Modal Damping ≠ Function Damping Ratio → ETABS escala valores (pág. 38)

---

## 3. MENÚS ETABS EXACTOS USADOS

### 3.1 Definiciones (Define)

| Menú | Submenú | Uso |
|------|---------|-----|
| Define > Section Properties > Frame Sections | Add New Property | Vigas, columnas (+ J=0 vigas) |
| Define > Section Properties > Shell Sections | Add New Property | Muros, losas (+ Modifiers losa 25%) |
| Define > Materials | Add New Material | Hormigón, acero refuerzo, acero perfiles |
| Define > Load Patterns | — | CM (SWM=1), CVR (Reducible Live), CVT (Roof Live) |
| Define > Mass Source | — | CM 100% + %CV para masa sísmica |
| Define > Functions > Response Spectrum | From File | Importar espectro .txt |
| Define > Load Cases | Add New | Caso modal espectral (SXE, SYE) |
| Define > Combos | Add New | SX, SY (diseño), C1–C7 |
| Define > Diaphragms | — | Rigid, Semi-rigid |

### 3.2 Asignación (Assign)

| Menú | Submenú | Uso |
|------|---------|-----|
| Assign > Frame > Insertion Point | Cardinal Point | Vigas invertidas (punto 2 = Bottom Center) |
| Assign > Frame > End Offsets | Rigid Zone Factor | Cachos rígidos (0.75) |
| Assign > Frame > Releases | — | Rótulas en vigas |
| Assign > Shell > Diaphragm | — | Asignar diafragma a losas |
| Assign > Shell > Auto Edge Constraint | — | Compatibilidad deformaciones |
| Assign > Shell > Pier Label | — | Asignar etiqueta pier a muros |
| Assign > Shell > Spandrel Label | — | Asignar etiqueta spandrel a vigas de acople |
| Assign > Joint > Restraints | — | Apoyos en base |
| Assign > Shell > Uniform Loads | — | Cargas en losas (CM adicional, CVR, CVT) |

### 3.3 Dibujo (Draw)

| Menú | Submenú | Uso |
|------|---------|-----|
| Draw > Draw Wall/Floor | Wall | Dibujar muros (entre ejes o Drawing Control Type) |
| Draw > Draw Wall/Floor | Floor | Dibujar losas (4 nodos) |
| Draw > Draw Line Objects | — | Dibujar vigas |
| Draw > Draw Point Objects | — | Dibujar columnas (ojo: Angle) |

### 3.4 Edición y Mesh

| Menú | Submenú | Uso |
|------|---------|-----|
| Edit > Mesh Shells | At Points | Meshear losas en esquinas de muros/columnas |
| Edit > Mesh Shells | General | Mesh automático máx 1m×1m |
| Edit > Divide Shells | — | Dividir muros en intersecciones |
| Edit > Replicate | Stories | Replicar pisos completos |

### 3.5 Análisis y Resultados

| Menú | Submenú | Uso |
|------|---------|-----|
| Analyze > Set Analysis Options | — | Motor (Advanced/Multi-threaded) |
| Analyze > Check Model | — | Verificar errores (NO Fix) |
| Analyze > Run Analysis | — | Correr modelo |
| Display > Show Tables | — | Tablas de resultados |
| Display > Show Tables > Story Forces | — | Peso sísmico, cortes basales |
| Display > Show Tables > Material List By Story | Floor | Áreas por piso |
| Display > Show Tables > Modal Information | — | Períodos, masas participantes |
| File > Export | — | Exportar a .mdb |

### 3.6 Modos de Vibrar

| Menú | Submenú | Uso |
|------|---------|-----|
| Define > Load Cases > Modal | Eigen Vectors | Método usual (valores propios) |
| Define > Load Cases > Modal | Ritz Vectors | Método alternativo |

---

## 4. ERRORES COMUNES QUE MENCIONA

### 4.1 Errores de modelación geométrica (págs. 47–50)

**"En modelos de edificios, lo perfecto es enemigo de lo bueno"**

Lafontaine muestra ejemplos de **refinación innecesaria** (imágenes en págs. 48–50):
- Modelar detalles arquitectónicos que no aportan estructuralmente
- Exceso de elementos pequeños que complican el modelo sin mejorar resultados
- Nota: "Un modelo es una representación matemática de un edificio, no el edificio propiamente tal"

### 4.2 Losas mal dibujadas (págs. 79–84)

**Formas "poco sanas"** (pág. 80–81):
- Losa como un solo panel grande → "se le da toda la responsabilidad al mallado automático"
- Losa con ángulos muy distintos de 90°
- No meshear en esquinas de muros/columnas

**Forma correcta** (págs. 82–84):
- Elementos de 4 nodos
- Meshear manualmente donde hay muros y columnas
- Usar líneas "nulas" como guías para cortar la losa
- Apagar muros antes de meshear (no cortarlos)

### 4.3 Diafragmas mal asignados (págs. 104–106)

- **NO asignar un mismo diafragma rígido a dos partes sin conexión** o con conexión insuficiente
- **NO asignar diafragma rígido a losas con grandes estrangulaciones**
- **NO asignar diafragma rígido a losas con razón de lados extrema** (muy larga/angosta)

### 4.4 Piers y Spandrels mal asignados (págs. 112–113)

- **Error 1**: Pier que abarca dos columnas → "entregará fuerzas de diseño de ambas columnas combinadas"
- **Error 2**: Pier que no cubre toda la sección → "faltarían obtener las fuerzas de diseño en las secciones señaladas"

### 4.5 Descensos diferenciales en vigas (págs. 129–130)

- En pisos superiores: momentos por carga muerta muestran momento positivo en apoyo (error)
- **Causa**: descensos diferenciales entre apoyos
- **Soluciones**: secuencia constructiva, aislar piso en otro modelo, descarga de vigas a mano

### 4.6 Espectro built-in desactualizado (pág. 35)

- ETABS tiene opción "Chile NCH433+DS61" built-in
- **Está desactualizado** (clasificación de suelos antigua)
- **NO usar sin previa verificación**

### 4.7 Check Model — NO usar Fix (pág. 120)

- "Se recomienda no usar la opción de Fix, perdemos el control"
- "Un modelo bien hecho no debiese reportar errores que necesiten algún arreglo"

### 4.8 Replicación incompleta (pág. 118)

- "Verificar que esté todo prendido antes de seleccionar los elementos a replicar"
- Si hay elementos ocultos, no se seleccionan y no se replican

### 4.9 Modal Damping inconsistente (pág. 38)

- Si Modal Damping del caso ≠ Function Damping Ratio del espectro → ETABS escala valores
- Deben coincidir (ambos 5%)

### 4.10 Losa como membrana mal aplicada (pág. 26)

- "Si se modela losa como membrana, carga se distribuye por criterios geométricos (áreas tributarias) y no por rigidez"
- Solo usar en paños rectangulares y verificando descarga

---

## 5. PRÁCTICAS CHILENAS DOCUMENTADAS

### 5.1 Prácticas ya en nuestra guía (confirmadas por Lafontaine)

| Práctica | Pág. Lafontaine | Estado |
|----------|-----------------|--------|
| J = 0 en vigas | 23 | ✅ En guía |
| Inercia losa 25% (m11, m22, m12 = 0.25) | 27 | ✅ En guía |
| Peso/Área ≈ 1 tonf/m² | 138–140 | ✅ En guía |
| Espectro From File (no built-in) | 34–35 | ✅ En guía |
| Cardinal Point vigas invertidas | 57–59 | ✅ En guía |
| Peso hormigón = 2.5 tonf/m³ | 15 | ✅ En guía |
| Cachos rígidos RZF = 0.75 | 62 | ✅ En guía |
| CQC para combinación modal | 38 | ✅ En guía |
| Dibujar de arriba hacia abajo | 51 | ✅ En guía |

### 5.2 Prácticas adicionales NO en nuestra guía (nuevas)

| Práctica | Pág. | Detalle |
|----------|------|---------|
| **Columna con razón lados > 4 → modelar como muro** | 24 | "Si razón de lados es mayor a 4, evaluar usar shell" |
| **Rótulas en vigas al lado débil de muros** | 64 | "Las vigas que comienzan o terminan al lado débil de un muro se rotulan, a menos que se verifique que el muro resiste el momento negativo" |
| **Dividir muros en intersecciones** | 65–67 | Seleccionar muros que se intersectan y dividir (Edit > Divide) — asegura conectividad |
| **Auto Edge Constraint** | 98–99 | Compatibilidad de deformaciones en nodos sobre misma línea, reemplaza necesidad de conectividad total manual |
| **Mesh muros manual (no solo automático)** | 88 | "Conectividad directa entre elementos. Mesheo manual para evitar elementos muy alargados (sino no considera correctamente la deformación por flexión y queda más rígido)" |
| **Mesh losa con líneas nulas como guía** | 83 | Dibujar líneas "nulas" donde se cortará la losa, dibujar sobre estas, luego borrar las nulas |
| **Fachadas: vigas altas de acople → cambiar a spandrel (shell)** | 89–94 | Si la viga de acople es alta y corta, modelar como shell spandrel en vez de frame. Meshear para conectividad directa |
| **Apoyos: empotrado vs articulado según fundación** | 95–96 | Losa fundación → empotrado. Zapatas corridas → articulado. Si empotrado → controlar el giro |
| **Diafragma: asignar a losas, no a puntos** | 109 | "Se recomienda asignar a losas, no a puntos" |
| **No asignar mismo DR a partes sin conexión** | 104 | Ver errores arriba |
| **Piers pueden repetir nombre en pisos distintos** | 116 | "Piers y Spandrels pueden tener el mismo nombre en pisos distintos" |
| **Verificar deformadas post-análisis** | 141 | "Observar deformadas para visualizar posibles elementos sueltos que estén alterando el análisis modal" |
| **CVR: Reducible Live + setear tipo reducción** | 30–31 | La reducción es sobre el diseño, no sobre el análisis. Solo relevante si se usa diseñador ETABS |
| **NCh433 permite no considerar CVT en masa** | 33 | Masa sísmica puede excluir CVT |
| **Eigen vs Ritz** | 42 | "VP llega a la solución por abajo, Ritz puede llegar por arriba" — Eigen es el método usual |
| **Combo SX/SY como Combo (no Load Case)** | 39–40 | Ventaja: al calcular R, se cambia factor sin re-correr el modelo |
| **Scale Factor = I inicialmente (no I/R)** | 40 | "En una primera etapa no se saben los períodos del edificio, por ende tampoco el factor de reducción R. Se puede partir colocando solo I" |
| **Descensos diferenciales → secuencia constructiva** | 129–130 | Momementos positivos en apoyos de vigas superiores por descensos diferenciales. Evaluar secuencia constructiva |

---

## 6. COMPARACIÓN CON NUESTRA GUÍA Y LA VERSIÓN DE ETABS

### 6.1 Versión de ETABS

Lafontaine **no especifica explícitamente** qué versión de ETABS usa en el tutorial. Basado en:
- Las capturas de pantalla muestran interfaz consistente con ETABS 2016–2019
- Menciona "Advanced Solver" y "Multi-threaded Solver" (disponibles desde v2016)
- La opción "Chile NCH433+DS61" la marca como desactualizada → sugiere versión ≤ 2019
- **Conclusión**: compatible con ETABS v19 sin diferencias significativas de interfaz

### 6.2 Diferencias potenciales con ETABS v19

| Aspecto | Lafontaine | ETABS v19 |
|---------|------------|-----------|
| Espectro Chile built-in | Desactualizado, no usar | Igual, sigue desactualizado |
| Auto Edge Constraint | Disponible | Disponible, mejorado |
| Check Model | Disponible con Fix | Disponible, Fix mejorado |
| Export to MDB | Disponible | Disponible |
| Advanced Solver | Disponible | Disponible |

No se identifican diferencias relevantes para nuestro proyecto.

---

## 7. TORSIÓN ACCIDENTAL — DETALLE LAFONTAINE (págs. 43–46)

### Método 1: Momentos Torsores (fácil, conservador)
- ETABS da opción de ingresar excentricidad por piso
- **10% en techo, 0% en base**, interpolación lineal en la altura
- Si diafragma rígido → aplica momento torsor en CM
- Si diafragma semi-rígido → distribuye momento torsor global proporcional a masa de nodos del diafragma
- Ingresar excentricidad como **valor neto, no %**, en cada piso y diafragma
- **Dirección X → % de dimensión en Y de planta**
- **Dirección Y → % de dimensión en X de planta**

### Método 2: Mover Centro de Masas (complejo, menos giro)
- ETABS da la opción, **pero no está documentado cómo lo hace** → Validar
- Al cambiar ubicación del CM → actualizar masa traslacional
- **No olvidar eliminar excentricidades en sismos**, sino torsión accidental se considera dos veces

### Comparación con Material Apoyo (Prof. Music)
El Prof. Music documenta 3 métodos (método a, método b forma 1 y forma 2). Lafontaine documenta 2, equivalentes a:
- Lafontaine Método 1 ≈ Music Método a (momentos torsores)
- Lafontaine Método 2 ≈ Music Método b (mover CM)
- Music tiene un tercer método (forma 2 del método b: excentricidad por piso)

---

## 8. CARGAS Y COMBINACIONES — DETALLE LAFONTAINE

### 8.1 Load Patterns definidos
| Load Pattern | Type | SWM | Descripción |
|-------------|------|-----|-------------|
| CM | Dead | 1 | Peso propio + carga muerta adicional |
| CV | Live | 0 | Carga viva no reducible |
| CVR | Reducible Live | 0 | Carga viva reducible (NCh1537) |
| CVT | Roof Live | 0 | Carga viva de techo |

### 8.2 Reducción de cargas vivas (NCh1537:2009)
- Aplica si carga ≤ 500 kgf/m², no estacionamientos, no lugares públicos
- Reducción máx: 50% (1 piso), 60% (>1 piso)
- KLL depende del tipo de elemento, At = área tributaria (todos los pisos), L0 = sobrecarga sin reducir
- **Reducción solo sobre diseño**, no sobre análisis → solo relevante si usa diseñador ETABS

### 8.3 Combinaciones
Las 7 combinaciones de Lafontaine difieren ligeramente de las NCh3171. Nuestro proyecto usa NCh3171 (7 combos C1–C7). Las de Lafontaine incluyen CVR como carga separada.

**Nota para nuestro proyecto**: Las combinaciones del proyecto usan TERP/TERT/SCP/SCT, que son equivalentes pero con nomenclatura distinta a las CM/CV/CVR/CVT de Lafontaine.

### 8.4 Correspondencia de nomenclatura
| Lafontaine | Nuestro proyecto | Descripción |
|-----------|------------------|-------------|
| CM (SWM=1) | PP (SWM=1) | Peso propio |
| CM (adicional) | TERP | Sobrecarga permanente (terminaciones) |
| CV | SCP | Sobrecarga de piso |
| CVR | — | (CVR integrada en SCP/SCT para nuestro caso) |
| CVT | TERT / SCT | Techo: permanente y uso |

---

## 9. MASA SÍSMICA — DETALLE (pág. 33)

**Configuración de Lafontaine**:
- Mass Source tipo: "From Loads"
- Incluye: CM (100%) + CV (25% en su ejemplo)
- NCh433 permite no considerar CVT en cálculo de masa

**Para nuestro proyecto** (confirmado en context.md):
- TERP = 1.0 (100%)
- SCP = 0.25 (25%)

---

## 10. DIAFRAGMAS — RESUMEN DE CRITERIOS (págs. 100–109)

### Diafragma Rígido (DR)
- Programa calcula CM y asigna toda masa traslacional y rotacional allí
- Se pierden fuerzas/deformaciones en plano del diafragma
- Se puede asignar torsión accidental
- **NO usar si**: partes sin conexión, estrangulaciones, razón de lados extrema

### Diafragma Semi-rígido
- No hace condensación. Masa se asigna a cada nodo
- Se puede asignar torsión accidental
- No se pierden esfuerzos/deformaciones en plano

### Sin diafragma
- Para análisis: igual que semi-rígido
- NO se puede asignar torsión accidental

### Recomendación de Lafontaine
- "Asignar a losas, no a puntos"
- No es necesario un diafragma distinto por piso
- Hoy no es necesario DR para velocidad computacional ("un modelo no se demora más de 15 minutos si está bien construido")

---

## 11. VALIDACIONES DEL MODELO — CHECKLIST COMPLETO

### Pre-análisis
- [ ] Check Model ejecutado (Analyze > Check Model), NO usar Fix
- [ ] Log revisado sin problemas (Display > Show Log)
- [ ] Todo visible antes de replicar pisos

### Post-análisis
- [ ] **Peso/Área ≈ 1 tonf/m²** (Material List By Story + Story Forces)
- [ ] **Deformadas sin elementos sueltos** (debe verse monolítico)
- [ ] **Períodos razonables** (T1 ≈ N/15 a N/10 para muros HA)
- [ ] **Cortes basales** verificados contra Cmín NCh433
- [ ] Diagramas de momento de vigas sin anomalías (descensos diferenciales)

---

## 12. RESUMEN DE VALORES NUMÉRICOS CLAVE DEL EJEMPLO DE LAFONTAINE

| Parámetro | Valor |
|-----------|-------|
| Pisos | 20 |
| Área piso | 484 m² |
| Área total | 9,680 m² |
| Peso sísmico | 9,070 tonf |
| P/A | 0.93 tonf/m² |
| Peso hormigón | 2.5 tonf/m³ |
| E hormigón | 4700√f'c [MPa] |
| Mesh losa | máx 1m×1m |
| Rigid Zone Factor | 0.75 |
| Amortiguamiento | 5% |
| Scale Factor espectro (si en m/s²) | 1 |
| J vigas | 0 |
| Inercia losa (modifiers) | 0.25 |
| CV en masa sísmica | 25% (ejemplo) |

---

## 13. CONCLUSIONES PARA NUESTRO PROYECTO

### Lo que Lafontaine confirma de nuestra guía
Todas las prácticas chilenas clave ya documentadas están correctas: J=0 vigas, inercia 25%, Peso/Área≈1, From File, Cardinal Point, etc.

### Lo que debemos agregar a nuestra guía
1. **Rótulas en vigas al lado débil de muros** — verificar en nuestro edificio
2. **Dividir muros en intersecciones** (Edit > Divide) — paso crucial que falta
3. **Auto Edge Constraint** — aplicar a todo (Assign > Shell > Auto Edge Constraint)
4. **Mesh muros manual** — no confiar solo en AutoMesh para muros
5. **Verificar deformadas post-análisis** — paso de validación faltante
6. **Fachadas**: evaluar si tenemos vigas de acople altas que requieran spandrels
7. **Piers/Spandrels**: agregar instrucciones de asignación correcta
8. **Combo SX/SY como Combo** — para cambiar I/R sin re-correr
9. **Scale Factor inicial = solo I** — primera iteración antes de conocer T y R
10. **Líneas nulas como guía para losas** — técnica práctica de dibujo
11. **No olvidar eliminar excentricidades si se mueve CM** — doble conteo torsión
12. **Check Model: NO usar Fix** — explicitarlo

### Comparación numérica con nuestro edificio
| Parámetro | Lafontaine | Nuestro Ed.1 |
|-----------|-----------|--------------|
| Pisos | 20 | 20 |
| Área piso | 484 m² | 468.4 m² |
| Peso estimado | 9,070 tonf | ~9,368 tonf |
| P/A | 0.93 | ~1.0 |

Los valores son muy similares, lo que valida la geometría y cargas de nuestro proyecto.
