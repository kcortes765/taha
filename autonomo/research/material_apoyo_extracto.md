# Extracto Completo — Material Apoyo Taller 2026 (47 págs)
## Prof. Juan Music Tomicic — 1S-2026 — Ayudante: Roberto Cortés

> Fuente: `docs/Material taller/Material Apoyo Taller 2026.pdf`
> Extraído el 2026-03-21 por agente autónomo.

---

## Índice de Secciones del Documento

| Sección | Tema | Páginas aprox. |
|---------|------|----------------|
| A | Consideraciones al Modelar (visualización 3D) | 1–2 |
| B | Verificación condiciones de deformación NCh433 (drift) | 2–6 |
| C | Asignación de Diafragma Rígido | 6 |
| D | Definir un Section Cut | 6–7 |
| E | Ejes en Section Design — ETABS vs SAP | 7–8 |
| F | Diagramas de Interacción P-M | 8–10 |
| G | Cómo diseña ETABS en análisis modal espectral (8 sub-combos) | 10–14 |
| H | Torsión Accidental — 3 métodos (H1: método a, H2: método b forma 1 y 2) | 14–25 |
| I | Combinaciones de Carga según NCh433 (4 variantes) | 25–35+ |

---

## A) Consideraciones al Modelar — Visualización 3D

### A.1) Visualizar y caminar por el edificio
1. Seleccionar Vista 3D del edificio
2. Seleccionar → **Extrude Frames** y **Extrude Shells**
3. **Options** > **Graphics Mode** > **DirectX**
4. Comando **Rotar Edificio** según lo que se quiera ver
5. Seleccionar **View Walk** o su respectivo icono
   - **Botón izquierdo mouse**: avanzar por edificio
   - **Botón derecho mouse**: subir/bajar (como ascensor)

### A.2) Ocultar parte del edificio para mejor visualización
1. **Options** > **Graphics Mode** > **DirectX**
2. **View** > **Set Elevation View**
3. Seleccionar un eje del edificio → **3D Section** → **Left** o **Right**
   - Ejemplo: si selecciono "Left", se oculta todo desde el eje seleccionado hacia la izquierda

---

## B) Verificación Condiciones de Deformación NCh433 (DRIFT)

### Procedimiento general
El profesor indica ubicar un **nodo cercano al Centro de Masas (CM)**.

**Para encontrar el CM:**
1. Apagar losas y vigas, dejar visible solo muros
2. Con solo muros visibles, es más fácil hallar un nodo cercano al CM
3. Click derecho sobre ese nodo → anotar su número (ej: nodo 44)

### Condición 1: Drift del CM
**Ruta ETABS:** Display > Show Tables → filtrar resultados

1. Obtener tabla de drift (Joint Drifts)
2. **Filtrar por el nodo del CM** (click derecho en columna Label → seleccionar nodo)
3. **Filtrar por Output Case** (seleccionar el estado de carga a verificar)
4. Columnas relevantes:
   - **Drift X**: (disp_CM_i+1 − disp_CM_i) / h_piso, combinado mediante CQC
   - **Drift Y**: ídem en dirección Y

**⚠️ ADVERTENCIA CRÍTICA del profesor:**
> "No es correcto restar los desplazamientos que muestra la tabla anterior y calcular el drift con ellos, ya que esos valores vienen de una combinación CQC."

Los valores de Drift X y Drift Y de la tabla **ya son la diferencia dividida por h_piso combinada por CQC**. NO se deben restar manualmente los desplazamientos de la tabla.

5. Comparar drift del CM con el **límite de la norma** NCh433

**Exportar a Excel:** Desde la tabla → Export to Excel

### Condición 2: Drift máximo y verificación torsional

**i) Determinar el drift máximo de los puntos más desfavorables del edificio** (puntos extremos).

Dos formas de encontrar el nodo más desfavorable:

**Forma 1 — Manual:**
- Identificar nodos en puntos extremos del edificio
- Ver valores de drift para esos nodos (mismo procedimiento que para CM)

**Forma 2 — Tabla automática:**
- Filtrar por caso de carga (ej: SEx)
- Seleccionar diafragma en X (para sismo X) o diafragma en Y (para sismo Y)
- Usar tabla **"Diaphragm Max Over Avg Drifts"**

Columnas clave de esta tabla:
| Columna | Significado |
|---------|-------------|
| Max Drift | Drift máximo en planta |
| Avg Drift | Drift promedio del diafragma |
| Ratio | Max Drift / Avg Drift |
| Label | Nodo con drift máximo |
| Max Loc X, Max Loc Y | Coordenadas del nodo con drift máximo |

**ii) Verificación Condición 2:**
- Restar el drift del CM a los drift de cada punto extremo
- Verificar para cada condición de carga de servicio según normativa
- Repetir para todos los estados de carga requeridos

**Para localizar un nodo específico en planta:** Usar función de selección por nodo en ETABS.

El profesor confirma que los valores de drift del nodo más desfavorable obtenidos por ambas formas (manual y tabla Diaphragm Max Over Avg Drifts) **coinciden**.

### Ejemplo numérico del documento (edificio de 5 pisos)

**Tabla Joint Drifts — Nodo 31 (más desfavorable), Sismo X:**

| Story | Disp X (mm) | Disp Y (mm) | Drift X | Drift Y |
|-------|-------------|-------------|---------|---------|
| Story5 | 19.423 | — | 0.000922 | 0.000158 |
| Story4 | 16.657 | — | 0.001390 | 0.000228 |
| Story3 | 12.486 | 2.527 | 0.001664 | 0.000258 |
| Story2 | 7.494 | 1.843 | 0.001487 | 0.000216 |
| Story1 | 3.033 | 1.068 | 0.001011 | 0.000140 |

**Tabla Diaphragm Max Over Avg Drifts — Sismo X:**

| Story | Max Drift | Avg Drift | Ratio | Label |
|-------|-----------|-----------|-------|-------|
| Story5 | 0.000922 | 0.000764 | 1.206 | 31 |
| Story4 | 0.001390 | 0.001162 | 1.196 | 31 |
| Story3 | 0.001664 | 0.001406 | 1.184 | 31 |
| Story2 | 0.001487 | 0.001271 | 1.170 | 31 |
| Story1 | 0.001011 | 0.000871 | 1.160 | 31 |

---

## C) Asignación de Diafragma Rígido

**Procedimiento en 3 pasos:**

1. **Definir** el diafragma:
   - **Define** > **Diaphragms** → crear un nombre para el diafragma

2. **Seleccionar** las losas:
   - **Select** > **Properties** > **Slab Sections** → selecciona todas las losas

3. **Asignar** el diafragma:
   - **Assign** > **Shell** > **Diaphragms** → seleccionar el nombre del diafragma creado

---

## D) Definir un Section Cut

**Procedimiento en 3 pasos:**

1. **Crear grupo:**
   - **Define** > **Group Definitions** > **ADD** → crear nombre de grupo
   - Si se quieren resultados en todos los pisos → **definir un grupo por piso**

2. **Asignar elementos al grupo:**
   - Seleccionar el piso
   - **Assign** > **Assign Objects to Group** → seleccionar grupo correspondiente

3. **Definir Section Cut:**
   - **Define** > **Section Cuts** > **ADD Section Cuts**
   - Ingresar:
     - **Nombre** del section cut
     - **Grupo** correspondiente
     - **Tipo de resultado**: ej. "Analysis" para momentos torsores
     - **User Defined**: coordenadas x, y, z del punto para resultados
   - OK

**Uso:** Section Cuts son necesarios para obtener momentos torsores por piso, cortes basales, etc.

---

## E) Ejes en Section Design — ETABS vs SAP

### E1) En Section Design de ETABS

| Dirección sismo | Ángulo |
|-----------------|--------|
| Sismo +X | 0° |
| Sismo −X | 180° |
| Sismo +Y | 90° |
| Sismo −Y | 270° (implícito) |

### E2) En Section Design de SAP

| Dirección sismo | Ángulo |
|-----------------|--------|
| Sismo +Y | 0° |
| Sismo −Y | 180° |
| Sismo −X | 90° |
| Sismo +X | 270° |

### Conclusiones del profesor

1. **Tanto la orientación de ejes locales como los ángulos para sismos son DIFERENTES entre ETABS y SAP**
2. En el curso se usará **ETABS** para análisis y diseño de vigas, muros y columnas → verificar ejes locales para interpretar correctamente los esfuerzos
3. **Diagramas de interacción**: usar **ETABS**
4. **Diagrama momento-curvatura (M-φ)**: usar **Section Designer de SAP**

---

## F) Diagramas de Interacción P-M

### Procedimiento completo para graficar en Excel

**Paso 1 — Exportar datos de ETABS a Excel:**
- Se copia de a una tabla o todas ellas del diagrama de interacción → llevar a Excel

**Paso 2 — Crear gráfico:**
- Insertar → Gráfico de dispersión con líneas suavizadas

**Paso 3 — Agregar datos:**
- Click derecho sobre gráfico en blanco → Seleccionar datos → Agregar datos
- Seleccionar valores X e Y arrastrando el mouse
- Asignar nombre a la serie de la curva

**Paso 4 — Graficar curvas con y sin φ:**
- Repetir el proceso para la curva **sin φ** (factor de reducción)
- Se deben ver ambas curvas (con φ y sin φ)

**Paso 5 — Editar diagrama:**
- Cambiar color: click derecho sobre curva → cambiar "relleno" y "contorno"
- Con la opción "+": seleccionar título del eje, título de gráfico, leyenda
- Dejar solo 2 leyendas (una curva con φ, una sin φ)

**Paso 6 — Graficar puntos de combinaciones de carga:**
- Exportar las **combinaciones P-M** de ETABS a Excel
- Graficar como puntos sobre el diagrama de interacción
- **⚠️ IMPORTANTE:** Verificar orientación de ejes locales del PIER para interpretar correctamente si P es tracción o compresión
- Click derecho → Cambiar tipo de gráfico de series → puntos

**Resultado final:** Diagrama P-M con curvas (con/sin φ) y puntos de combinaciones de carga superpuestos.

---

## G) Cómo Diseña ETABS en Análisis Modal Espectral — Las 8 Sub-combinaciones

### Concepto fundamental

Al hacer un análisis modal espectral, los aportes de cada modo se combinan mediante **CQC** → el resultado es **siempre positivo**. Esto genera ambigüedad en signos (¿P es compresión o tracción?, ¿M2 positivo o negativo?).

### Solución de ETABS: 8 sub-combinaciones por estado de carga

Para estar por el lado de la seguridad, ETABS genera **8 combinaciones de esfuerzos sísmicos** para cada estado de carga que incluye sismo.

**Ejemplo para el estado: 0.9×D + 1.4×SY(s/t) + 1.4×TY**

Se descompone en contribuciones:

| Componente | Sub-combo | P (tonf) | V2 (tonf) | V3 (tonf) | T (tonf-cm) | M2 (tonf-cm) | M3 (tonf-cm) |
|-----------|-----------|----------|-----------|-----------|-------------|--------------|--------------|
| 0.9D-1 | — | −469.51 | — | — | — | — | — |
| 1.4SY-1 | +P,+V2 | +255.09 | +73.43 | +0.169 | +26.30 | +43.90 | — |
| 1.4SY-2 | +P,−V2 | +255.09 | −73.43 | +0.169 | +26.30 | −43.90 | — |
| 1.4SY-3 | +P,+V2 | +255.09 | +73.43 | −0.169 | +26.30 | +43.90 | — |
| 1.4SY-4 | +P,−V2 | +255.09 | −73.43 | −0.169 | +26.30 | −43.90 | — |
| 1.4SY-5 | −P,+V2 | −255.09 | +73.43 | +0.169 | −26.30 | +43.90 | — |
| 1.4SY-6 | −P,−V2 | −255.09 | −73.43 | +0.169 | −26.30 | −43.90 | — |
| 1.4SY-7 | −P,+V2 | −255.09 | +73.43 | −0.169 | −26.30 | +43.90 | — |
| 1.4SY-8 | −P,−V2 | −255.09 | −73.43 | −0.169 | −26.30 | −43.90 | — |

**Cada Comb10-k = 0.9D-1 + 1.4SY-k + 1.4TY-1**

Resultados finales de las 8 sub-combinaciones:

| Sub-combo | P (tonf) | V2 (tonf) | V3 (tonf) | T (tonf-cm) | M2 (tonf-cm) | M3 (tonf-cm) |
|-----------|----------|-----------|-----------|-------------|--------------|--------------|
| Comb10-1 | −160.03 | 59.45 | 0.291 | 71.93 | 75.28 | 83,117 |
| Comb10-2 | −160.03 | −87.41 | 0.291 | 71.93 | −12.52 | 83,117 |
| Comb10-3 | −160.03 | 59.45 | −0.046 | 71.93 | 75.28 | −129,964 |
| Comb10-4 | −160.03 | −87.41 | −0.046 | 71.93 | −12.52 | −129,964 |
| Comb10-5 | −670.22 | 59.45 | 0.291 | 19.34 | 75.28 | 83,117 |
| Comb10-6 | −670.22 | −87.41 | 0.291 | 19.34 | −12.52 | 83,117 |
| Comb10-7 | −670.22 | 59.45 | −0.046 | 19.34 | 75.28 | −129,964 |
| Comb10-8 | −670.22 | −87.41 | −0.046 | 19.34 | −12.52 | −129,964 |

**Nota:** ETABS genera estas 8 sub-combinaciones internamente para cada combo que contiene sismo. El diseñador solo define el combo envolvente (ej: 0.9D + 1.4SY + 1.4TY) y ETABS expande automáticamente.

---

## H) Torsión Accidental en ETABS — 3 Métodos

La normativa NCh433 (art. 6.3.4) contempla dos métodos (a y b). El método b tiene 2 formas de implementación en ETABS. Total: **3 formas**.

---

### H1) Método a) — Desplazar el Centro de Masas

**Concepto:** Se traslada el CM una distancia igual a ±5% de la dimensión mayor perpendicular a la acción sísmica. ETABS recalcula la matriz de masa con las nuevas posiciones del CM.

**Se requieren 4 matrices de masa extra** (además de la original).

#### Paso 1: Definición de Fuentes de Masa (Mass Sources)

**Ruta:** `Define > Mass Source`

| Nombre | Descripción | Excentricidad X | Excentricidad Y |
|--------|-------------|-----------------|-----------------|
| **Masa Original** | 100% permanentes + 25% sobrecarga | 0 | 0 |
| **Masa+X** | Duplicar original + desplazar CM | **+0.05** | 0 |
| **Masa−X** | Duplicar original + desplazar CM | **−0.05** | 0 |
| **Masa+Y** | Duplicar original + desplazar CM | 0 | **+0.05** |
| **Masa−Y** | Duplicar original + desplazar CM | 0 | **−0.05** |

**Detalle de configuración:**
- Duplicar la fuente original
- Habilitar **"Adjust Diaphragm Lateral Mass to Move Mass Centroid by:"**
- Ingresar 0.05 (5%) en la casilla correspondiente:
  - "This Ratio of Diaphragm Width in X Direction" para +X/−X
  - La casilla de Y Direction para +Y/−Y
- **⚠️ IMPORTANTE:** Dejar la OTRA casilla en 0 → no desplazar CM en ambas direcciones simultáneamente

#### Paso 2: Configuración de Casos Estáticos No Lineales (auxiliares)

**Ruta:** `Define > Load Cases > Add New Case`

Para CADA una de las 4 fuentes de masa desplazadas:
- **Load Case Type:** Nonlinear Static
- **Mass Source:** Seleccionar la fuente de masa desplazada correspondiente (ej: Masa+X)
- **Loads Applied:** Lista de cargas **vacía** (o con coeficientes cero)
- Aparecerá mensaje: "No Load Assignments are specified!" → seleccionar **"Sí"**
- **Función:** Son casos auxiliares puramente numéricos para la formación de matrices

Crear 4 casos: +XMasa, −XMasa, +YMasa, −YMasa

#### Paso 3: Definición de Casos Modales Específicos

**Ruta:** `Define > Load Cases > Add New Case`

Para CADA caso auxiliar del Paso 2:
- **Load Case Type:** Modal
- **Subtype:** Eigen
- **P-Delta/Nonlinear Stiffness:** Seleccionar **"Use Nonlinear Case (Loads at End of Case NOT included)"**
- **Case Selection:** Escoger el caso estático no lineal auxiliar del Paso 2 (ej: +XMasa)

**Razón:** Como el CM cambia, las propiedades dinámicas (períodos, formas modales) también cambian → se necesita un análisis modal independiente por cada excentricidad.

Al seleccionar el caso no lineal, **ETABS importa automáticamente la matriz de masa asociada**.

Crear 4 modales: Modal+X, Modal−X, Modal+Y, Modal−Y

#### Paso 4: Generación de Casos de Espectro de Respuesta

**Ruta:** `Define > Load Cases > Add New Case`

Para CADA caso modal del Paso 3:
- **Load Case Type:** Response Spectrum
- **Modal Case:** Seleccionar el caso modal específico (ej: Modal+X)
- **Loads Applied:** Función de espectro con aceleración de gravedad
  - **U1** para sismo en X
  - **U2** para sismo en Y
- **⚠️ Diaphragm Eccentricity = 0** (la excentricidad ya está incluida físicamente en la matriz de masa del análisis modal)

**Resultado:** Se generan múltiples casos de espectro de respuesta, cada uno con los modos que ya incorporan el efecto dinámico de la torsión accidental.

**Casos RS resultantes (para sismo X y Y):**
- SDX (masa original, sin torsión)
- SDX+Y (masa desplazada en +Y)
- SDX−Y (masa desplazada en −Y)
- SDY (masa original)
- SDY+X (masa desplazada en +X)
- SDY−X (masa desplazada en −X)

---

### H2) Método b) — Torsión Estática

Se puede implementar de **2 formas** en ETABS:

---

#### Forma 1: Aplicando momentos torsores estáticos por piso

**Concepto:** Se corre el modelo sin torsión accidental, se obtienen los cortes basales por piso combinados por CQC, se calcula el momento torsor manualmente y se ingresa como carga estática.

##### Paso 1: Configuración del Modelo Base (Sin Excentricidad)
- **Define** > **Mass Source**
- Asegurarse de que "Move Mass Centroid over Diaphragm" = **0 (cero)**
- **Run Analysis** con los casos espectrales estándar (Sx y Sy)

##### Paso 2: Obtención de Cortes de Entrepiso (Story Shears)

**Forma A — Gráfico:**
- **Display** > **Story Response Plots**
- Display Type: **Story Shears**
- Case/Combo: Seleccionar caso espectral (Sismo_X o Sismo_Y)
- Tomar valores tabulados o exportar a Excel

**Forma B — Tabla:**
- **Display** > **Show Tables**
- Seleccionar: ANALYSIS RESULTS > Structure Output > Other Output Items > **Table: Story Forces**
- Filtrar por Output Case del sismo
- Leer **Vx** (para sismo X) o **Vy** (para sismo Y)
- Resultados ordenados por piso y locación (Top o Bottom)

Se requieren valores de corte para **ambas direcciones** (X e Y).

##### Paso 3: Cálculo de Momentos Torsores (en Excel)

Según NCh433 art. 6.3.4 b):

**⚠️ Los cortes de Story Shears son ACUMULADOS por piso** → se debe hacer la diferencia entre piso superior e inferior:

```
Fk = Qk − Qk+1       (fuerza sísmica en piso k)
Mtk = Fk × ek         (momento torsor en piso k)
```

Donde `ek` es la excentricidad accidental en piso k según NCh433.

##### Paso 4: Definición de Patrones de Carga para Torsión

**Ruta:** `Define > Load Patterns`
- **Type:** Seismic
- **Self Weight Multiplier:** **0**
- **Auto Lateral Load:** **User Defined**

**Ingreso de cargas:**
- Click en **Modify Lateral Load**
- Marcar **"Apply at Center of Mass"**
- Copiar valores de momentos torsores desde Excel → pegar en columna **Mz** por piso
- Columnas **Fx** y **Fy** deben permanecer en **0**

Crear patrones: **TEX** (torsión sismo X) y **TEY** (torsión sismo Y).

---

#### Forma 2: Entregando la excentricidad por piso directamente

**Concepto:** Se calculan las excentricidades netas por piso y se ingresan directamente en la configuración del caso espectral. ETABS aplica internamente ±e para obtener la envolvente máxima.

##### Paso 1: Configuración del Caso Espectral

**Ruta:** `Define > Load Cases`
1. Seleccionar el caso espectral (Sx o Sy) → **Modify/Show Case**
2. Localizar **"Diaphragm Eccentricity"**
3. Click en **Modify/Show**
4. **Eccentricity Ratio = 0** (importante)
5. Se listan todos los diafragmas del modelo
6. Para cada piso → columna **Eccentricity** → ingresar el valor calculado
7. El valor se ingresa como **longitud positiva**
8. ETABS internamente aplica **+e y −e** para capturar la envolvente máxima

**Casos resultantes:**
- SDTX = Sismo X con Torsión Accidental (2 sub-casos: +e y −e)
- SDTY = Sismo Y con Torsión Accidental (2 sub-casos: +e y −e)

---

## I) Combinaciones de Carga según NCh433 — 4 Variantes

El documento presenta **4 conjuntos de combinaciones** dependiendo del método de análisis y de torsión accidental utilizado.

### Nomenclatura de cargas

| Abreviatura | Significado |
|-------------|-------------|
| CP | Cargas Permanentes |
| L | Sobrecarga Pisos |
| Lr | Sobrecarga Techo |
| SDX | Sismo X aplicado en CM |
| SDY | Sismo Y aplicado en CM |
| TEX | Torsión Accidental Estática para sismo X (aplicada en CM) |
| TEY | Torsión Accidental Estática para sismo Y (aplicada en CM) |
| SDTX | Sismo X con Torsión Accidental entregada por piso (Forma 2) |
| SDTY | Sismo Y con Torsión Accidental entregada por piso (Forma 2) |
| SDX+Y | Sismo X con masa desplazada en +Y (Método a) |
| SDX−Y | Sismo X con masa desplazada en −Y (Método a) |
| SDY+X | Sismo Y con masa desplazada en +X (Método a) |
| SDY−X | Sismo Y con masa desplazada en −X (Método a) |

---

### Variante 1: Método Estático — 19 Combinaciones

| N° | Estado de Carga | COMBO ETABS |
|----|----------------|-------------|
| 1 | 1.4·CP | COMBO 1 |
| 2 | 1.2·CP + 1.6·L + 0.5·Lr | COMBO 2 |
| 3 | 1.2·CP + L + 1.6·Lr | COMBO 3 |
| 4 | 1.2·CP + L + 1.4·SDX + 1.4·TEX | COMBO 4 |
| 5 | 1.2·CP + L − 1.4·SDX + 1.4·TEX | COMBO 5 |
| 6 | 1.2·CP + L + 1.4·SDX − 1.4·TEX | COMBO 6 |
| 7 | 1.2·CP + L − 1.4·SDX − 1.4·TEX | COMBO 7 |
| 8 | 0.9·CP + 1.4·SDX + 1.4·TEX | COMBO 8 |
| 9 | 0.9·CP − 1.4·SDX + 1.4·TEX | COMBO 9 |
| 10 | 0.9·CP + 1.4·SDX − 1.4·TEX | COMBO 10 |
| 11 | 0.9·CP − 1.4·SDX − 1.4·TEX | COMBO 11 |
| 12 | 1.2·CP + L + 1.4·SDY + 1.4·TEY | COMBO 12 |
| 13 | 1.2·CP + L − 1.4·SDY + 1.4·TEY | COMBO 13 |
| 14 | 1.2·CP + L + 1.4·SDY − 1.4·TEY | COMBO 14 |
| 15 | 1.2·CP + L − 1.4·SDY − 1.4·TEY | COMBO 15 |
| 16 | 0.9·CP + 1.4·SDY + 1.4·TEY | COMBO 16 |
| 17 | 0.9·CP − 1.4·SDY + 1.4·TEY | COMBO 17 |
| 18 | 0.9·CP + 1.4·SDY − 1.4·TEY | COMBO 18 |
| 19 | 0.9·CP − 1.4·SDY − 1.4·TEY | COMBO 19 |

**Nota:** En combo 15, el documento tiene un error tipográfico ("−1.4·TEX" en vez de "−1.4·TEY"). La intención es TEY.

---

### Variante 2: Método Dinámico + Torsión b) Forma 1 — 19 Combinaciones

**Idéntica estructura a la Variante 1** (mismas 19 fórmulas). La diferencia es que:
- SDX, SDY son **casos espectrales** (Response Spectrum) en vez de estáticos
- TEX, TEY son **patrones de carga User Defined** con momentos torsores calculados manualmente (Forma 1 del método b)

---

### Variante 3: Método Dinámico + Torsión b) Forma 2 — 7 estados → 19 casos

| N° | Estado de Carga | COMBO ETABS |
|----|----------------|-------------|
| 1 | 1.4·CP | COMBO 1 |
| 2 | 1.2·CP + 1.6·L + 0.5·Lr | COMBO 2 |
| 3 | 1.2·CP + L + 1.6·Lr | COMBO 3 |
| 4 | 1.2·CP + L + 1.4·SDTX *(2 sub-casos)* | COMBO 4 |
| 5 | 1.2·CP + L − 1.4·SDTX *(2 sub-casos)* | — |
| 6 | 1.2·CP + L + 1.4·SDTY *(2 sub-casos)* | COMBO 5 |
| 7 | 1.2·CP + L − 1.4·SDTY *(2 sub-casos)* | COMBO 6 |
| 8 | 0.9·CP + 1.4·SDTX *(2 sub-casos)* | COMBO 7 |
| 9 | 0.9·CP − 1.4·SDTX *(2 sub-casos)* | — |
| 10 | 0.9·CP + 1.4·SDTY *(2 sub-casos)* | — |
| 11 | 0.9·CP − 1.4·SDTY *(2 sub-casos)* | — |

**Total: 19 casos** (7 estados × ~2 sub-casos + 3 sin sismo)

**Nota:** SDTX y SDTY ya incluyen la torsión accidental (±e por piso). ETABS expande internamente cada caso en 2 sub-casos (+e y −e). No se necesitan patrones TEX/TEY separados.

---

### Variante 4: Método Dinámico + Torsión Método a) — 27 Combinaciones

| N° | Estado de Carga | COMBO ETABS |
|----|----------------|-------------|
| 1 | 1.4·CP | COMBO 1 |
| 2 | 1.2·CP + 1.6·L + 0.5·Lr | COMBO 2 |
| 3 | 1.2·CP + L + 1.6·Lr | COMBO 3 |
| 4 | 1.2·CP + L + 1.4·SDX | COMBO 4 |
| 5 | 1.2·CP + L − 1.4·SDX | COMBO 5 |
| 6 | 1.2·CP + L + 1.4·SDX+Y | — |
| 7 | 1.2·CP + L − 1.4·SDX+Y | — |
| 8 | 1.2·CP + L + 1.4·SDX−Y | COMBO 6 |
| 9 | 1.2·CP + L − 1.4·SDX−Y | — |
| 10 | 0.9·CP + 1.4·SDX | COMBO 7 |
| 11 | 0.9·CP − 1.4·SDX | — |
| 12 | 0.9·CP + 1.4·SDX+Y | COMBO 8 |
| 13 | 0.9·CP − 1.4·SDX+Y | COMBO 9 |
| 14 | 0.9·CP + 1.4·SDX−Y | COMBO 10 |
| 15 | 0.9·CP − 1.4·SDX−Y | COMBO 11 |
| 16 | 1.2·CP + L + 1.4·SDY | — |
| 17 | 1.2·CP + L − 1.4·SDY | — |
| 18 | 1.2·CP + L + 1.4·SDY+X | — |
| 19 | 1.2·CP + L − 1.4·SDY+X | — |
| 20 | 1.2·CP + L + 1.4·SDY−X | COMBO 12 |
| 21 | 1.2·CP + L − 1.4·SDY−X | COMBO 13 |
| 22 | 0.9·CP + 1.4·SDY | — |
| 23 | 0.9·CP − 1.4·SDY | — |
| 24 | 0.9·CP + 1.4·SDY+X | COMBO 14 |
| 25 | 0.9·CP − 1.4·SDY+X | COMBO 15 |
| 26 | 0.9·CP + 1.4·SDY−X | — |
| 27 | 0.9·CP − 1.4·SDY−X | — |

**Total: 27 combinaciones** (3 gravitacionales + 12 sismo X + 12 sismo Y)

**Nota:** El método a) genera más combinaciones porque cada dirección de sismo se corre con la masa original y con la masa desplazada en cada sentido perpendicular.

---

## Resumen Comparativo de Métodos de Torsión

| Aspecto | Método a) | Método b) Forma 1 | Método b) Forma 2 |
|---------|-----------|-------------------|-------------------|
| **Concepto** | Desplazar CM (±5%) | Momentos torsores estáticos | Excentricidad neta por piso |
| **Mass Sources** | 5 (original + 4 desplazadas) | 1 (original, sin excentricidad) | 1 (original, sin excentricidad) |
| **Casos modales** | 5 (1 original + 4 desplazados) | 1 (original) | 1 (original) |
| **Casos espectro** | 6 (SDX, SDX±Y, SDY, SDY±X) | 2 (SDX, SDY) | 2 (SDTX, SDTY) |
| **Patrones User Defined** | No | Sí (TEX, TEY) | No |
| **Cálculo manual en Excel** | No | Sí (cortes → momentos torsores) | Sí (excentricidades por piso) |
| **Total combinaciones** | 27 | 19 | 19 (7 estados × sub-casos) |
| **Complejidad ETABS** | Alta (muchos mass sources/modales) | Media (cálculo Excel + carga manual) | Baja (excentricidad directa en RS) |

---

## Validaciones que el Profesor Espera Ver

1. **Drift del CM** comparado con límite NCh433
2. **Drift máximo de puntos extremos** − drift del CM → verificar Condición 2
3. **Tabla Diaphragm Max Over Avg Drifts**: ratio Max/Avg como indicador de torsión
4. **Diagramas P-M** con curvas (con/sin φ) + puntos de combinaciones de carga superpuestos
5. **Verificar orientación de ejes locales del PIER** al interpretar P (tracción vs compresión)
6. **Section Cuts** para obtener momentos torsores por piso
7. **Exportación a Excel** de todos los resultados tabulados

---

## Detalles que NO Están en la Guía Actual

1. **Las 8 sub-combinaciones de ETABS** (sección G): cuando se define un combo con sismo modal espectral, ETABS genera internamente 8 variaciones de signos para P, V2, V3, T, M2, M3. El diseñador solo define la envolvente y ETABS la expande.

2. **Procedimiento exacto para visualización 3D**: View Walk con botón izquierdo (avanzar) y derecho (subir/bajar), Set Elevation View para cortar en 3D.

3. **Advertencia sobre CQC en drift**: NO restar desplazamientos de la tabla Joint Drifts manualmente — los Drift X/Y ya son la diferencia normalizada combinada por CQC.

4. **Diferencia de ejes ETABS vs SAP**: ángulos 0°/90°/180°/270° mapean a direcciones de sismo distintas en cada programa. Crítico para interpretar diagramas P-M y M-φ.

5. **Método a) requiere 4 casos estáticos no lineales auxiliares** (sin cargas) como paso intermedio para vincular mass sources con análisis modales.

6. **Error tipográfico en combo 15** de la Variante 1 y 2: dice "−1.4·TEX" pero debería ser "−1.4·TEY".

7. **La tabla "Diaphragm Max Over Avg Drifts"** como herramienta directa para encontrar el nodo más desfavorable sin búsqueda manual.

8. **Forma 2 del método b)**: ETABS aplica internamente ±e cuando se ingresa la excentricidad como longitud positiva, generando la envolvente automáticamente.

9. **Section Cuts requieren un grupo por piso** y coordenadas User Defined del punto de interés.

10. **Para diagramas M-φ** se usa SAP (Section Designer), no ETABS directamente.
