# Flujo de Modelación ETABS — Taller ADSE 2026

## Referencia
- `material-apoyo-taller/Material Apoyo Taller 2026.pdf` — Guía Prof. Music (47p) ★★★
- `material-apoyo-taller/Paso a Paso ETABS M.Lafontaine.pdf` — Tutorial (143p)

---

## Edificio 1 — Automático con Pipeline Python

El pipeline en `taller-etabs/` automatiza toda la Fase 1 (geometría) y Fase 2 (análisis).

### Workflow en el laboratorio

```powershell
# 1. Matar todo ETABS
Get-Process ETABS -EA SilentlyContinue | Stop-Process -Force
Start-Sleep 3

# 2. Abrir ETABS 19 y esperar
Start-Process "C:\Program Files\Computers and Structures\ETABS 19\ETABS.exe"
Start-Sleep 20

# 3. Descargar scripts
cd C:\Users\Civil\Desktop
Invoke-WebRequest -Uri "https://github.com/kcortes765/taller-etabs/archive/refs/heads/master.zip" -OutFile ta.zip
Expand-Archive ta.zip -DestinationPath ta -Force
Copy-Item ta\taller-etabs-master\* ta\ -Force -Recurse
Remove-Item ta\taller-etabs-master, ta.zip -Recurse -Force
cd ta

# 4. Verificar conexión (PRIMERA VEZ)
python diag.py

# 5. Ejecutar todo
python run_all.py
```

### Pasos del pipeline
| # | Script | Resultado |
|---|--------|-----------|
| 1 | 01_init_model | 20 pisos + guarda Edificio1.edb |
| 2 | 02_materials_sections | G30, A630-420H, secciones |
| 3 | 03_walls | ~960 muros (con verificación) |
| 4 | 04_beams | ~400 vigas |
| 5 | 05_slabs | ~700 losas |
| 6 | 06_loads | 7 patrones de carga |
| 7 | 07_diaphragm_supports | Diafragma rígido + empotramientos |
| 7b | 07b_save_checkpoint | **VERIFICACIÓN** → aborta si vacío |
| **7c** | **07c_automesh** | **Auto-Mesh 1.0m (CRÍTICO — ver nota)** |
| 8 | 08_spectrum_cases | Espectro + modal + combos |
| 9 | 09_torsion_cases | Torsión caso a + b forma 2 |
| 10 | 10_save_run | Guardar + Run Analysis |
| 11 | 11_adjust_Rstar | T* → R* → re-escalar → re-analizar + Qmin |
| 12 | 12_results | Periodos, drift, peso, corte basal + **Qmin** |
| 13 | 13_semirigid | Modelo sin diafragma rígido |

---

## ★ CHECKLIST PRE-ENTREGA (4 puntos críticos — review IA)

### 1. AUTO-MESH (OBLIGATORIO — sin esto el modelo es inválido)
**Problema**: Sin mallado, ETABS usa 1 EF por panel de piso → T* ~ 0.2s (irreal), drift ~ 0.00001 (irreal).
**Con malla**: T* ~ 1.0–1.5s (realista), drift verificable con NCh433 límite 0.002.

**Automático (paso 7c)**: El script intenta `SetAutoMesh` via API con tamaño 1.0m.

**Si falla (manual)**:
```
Ctrl+A (seleccionar todo)

Assign > Shell > Wall Auto Mesh Options
  ☑ Auto Rectangular Mesh
  Max Element Size: 1.0 m
  ☑ Add Points from Lines
  → OK

Assign > Shell > Floor Auto Mesh Options
  ☑ Auto Rectangular Mesh
  Max Element Size: 1.0 m
  → OK

File > Save → luego re-analizar
```

### 2. QMIN NCh433 art.6.3.3 (verificado automáticamente en pasos 11 y 12)
**Regla**: Q_din (corte basal espectral) ≥ Qmin = 0.07 × I × W

Para este edificio: Qmin ≈ 0.07 × 1.0 × 10640 ≈ **745 tonf**

**Si Q_din < Qmin** (el script imprime la instrucción):
```
ETABS: Define > Load Cases > SEx > Modify/Show
Scale Factor = (g/R*) × (Qmin / Q_din_actual)
Luego: Analyze > Run Analysis
```

**Pregunta de defensa típica**: "¿Cómo verificaste el corte mínimo?"
→ Respuesta: "Qmin = 0.07·I·W = {valor} tonf. El espectral dio {valor} > Qmin."

### 3. P-DELTA (MANUAL — API muy inestable para esto)
**Cuándo**: Antes de extraer fuerzas definitivas para diseño de muros.

**Por qué**: Aumenta momentos de 2° orden en pisos bajos (~5-15%). Requerido para diseño riguroso.

```
ETABS: Define > P-Delta Options
Tipo: Iterative - Based on Loads
Cargas:
  PP    → Factor 1.0
  TERP  → Factor 1.0
  TERT  → Factor 1.0
  SCP   → Factor 0.25
→ OK → Analyze > Run Analysis
```

**Θ ≤ 0.10**: Verificar que el índice de estabilidad no exceda 0.10 (NCh433 / ACI318-08).

### 4. MODIFICADORES DE INERCIA (ya correctos en el código)
- Losas: f11=f22=0.25 ✅ (práctica Lafontaine)
- Vigas: J=0 ✅ (práctica chilena)
- Muros: 100% sección bruta ✅ (correcto para verificación de derivas en Chile)
- **No cambiar nada** — explicar en defensa si preguntan.

### Torsión B2 — defensa
Si preguntan por la aproximación en `09_torsion_cases.py`:
> "Aplicamos distribución de corte estático linealmente creciente con la altura (Fi ∝ hi) para pre-calcular los momentos torsionales. Para edificio de muros regulares de 20 pisos, el primer modo domina y la aproximación es muy certera."

---

### Intervenciones manuales probables

**Si el espectro no se define:**
```
Define > Functions > Response Spectrum > From File
Archivo: espectro_nch433.txt (generado automáticamente)
Nombre: Espectro_NCh433
```

**Si mass source no se define:**
```
Define > Mass Source
- Element Self Mass: ✓
- Load Pattern TERP: 1.0
- Load Pattern SCP: 0.25
```

**Si ETABS no conecta (modelo vacío):**
```
1. taskkill /F /IM ETABS.exe
2. Abrir ETABS 19 manualmente
3. Esperar 20+ segundos
4. python run_all.py
```

---

## Edificio 1 — Verificaciones post-análisis

### Verificar peso sísmico (~1 tonf/m²/piso)
```
Display > Show Tables > Building Output > Story Forces
Filtrar caso PP
Fuerza vertical en base / (área × n_pisos) ≈ 1 tonf/m²

Área planta ≈ 532 m², 20 pisos
W_total ≈ 532 × 20 × 1.0 ≈ 10640 tonf
```

### Verificar drift (NCh433 art.6.3.5)
```
Display > Show Tables > Analysis Output > Story Drifts

Filtrar SEx y SEy
Condición 1: max drift CM < 0.002  → "≤ 1/500"
Condición 2: max drift extremos < 0.001 → "≤ 1/1000"
```

### Verificar periodos fundamentales
```
Display > Show Tables > Analysis Output > Modal Participating Mass Ratios

Periodo 1: dominante traslacional X (Ux% mayor)
Periodo 2: dominante traslacional Y (Uy% mayor)
Periodo 3: rotacional (Rz% mayor)
```

Valores típicos edificio muros 20p Antofagasta:
- T1 ≈ 1.0–1.5s (X o Y)
- T2 ≈ 0.8–1.3s (la otra dir)
- T3 ≈ 0.6–1.0s (torsional)

### Corte basal verificado
```
Display > Show Tables > Analysis Output > Base Reactions (SEx, SEy)

Verificar que: Qmín ≤ Q_sismico ≤ Qmáx
Qmín = Cmín × I × P = 0.07 × 1.0 × W
Qmáx = Cmáx × I × P = 0.385 × 1.0 × W (aprox.)
```

---

## Edificio 1 — Drift NCh433 (Material Apoyo Taller 2026)

### Sección B del Material Apoyo Taller 2026
El Prof. Music especifica cómo extraer y verificar el drift en ETABS.

**Condición 1 (CM):**
```
δ/h ≤ 0.002    (en el centro de masa de cada piso)
```

**Condición 2 (extremos):**
```
δ/h ≤ 0.001    (en cualquier punto del diafragma)
δ_extremo = δ_CM + θ × r
donde r = distancia del CM al extremo, θ = rotación del diafragma
```

En ETABS: activar Section Cuts para obtener fuerzas en muros específicos.

---

## Edificio 2 — Manual en ETABS

### Flujo básico (Lafontaine + Material Apoyo)

```
1. File > New > Blank Model
2. Units: tonf, m, C
3. Define > Grid System (grilla 5×5 vanos de 6.5m)
4. Define > Story Data (5 pisos: 3.5m + 4×3.0m)
5. Define > Materials (G25, A630-420H)
6. Define > Section Properties > Frame (columnas, vigas)
7. Draw > Frame (dibujar columnas y vigas)
8. Define > Section Properties > Slab (losa 17cm)
9. Draw > Area (dibujar losas)
10. Assign > Frame > End Length Offsets (cachos 0.75)
11. Assign > Joint > Restraints (empotrar base)
12. Define > Load Patterns (PP, SCP, SCT, TERP)
13. Assign > Shell > Uniform Load (cargas a losas)
14. Define > Mass Source (PP + TERP×1.0 + SCP×0.25)
15. Define > Functions > Response Spectrum (Espectro_NCh433)
16. Define > Load Cases > Modal (60 modos)
17. Define > Load Cases > Response Spectrum (SEx, SEy)
18. Define > Combinations (C1-C8)
19. Analyze > Run Analysis
```

### Modificadores de rigidez Ed.2
- **Vigas**: J=0 (igual que Ed.1)
- **Losas**: f11=f22=f12=0.25 (igual que Ed.1)
- **Columnas**: sin modificadores
- **Cachos rígidos**: factor 0.75 (Assign > Frame > End Length Offsets)

### Espectro Ed.2
Mismo espectro que Ed.1 (misma zona, mismo suelo).
Pero R* puede diferir porque el período T* de marcos es diferente al de muros.

Ro = 11 (marcos especiales HA = misma categoría que muros)

---

## Torsión accidental — 3 métodos del enunciado

### Caso a) Eccentricidad accidental (automático)
En ETABS:
```
Load Cases > Response Spectrum > SEx →
Edit > Modify/Show Case → Diaphragm Eccentricity → Override = 5%
```
Repeti para SEy.

### Caso b) Forma 1 — Shift del CM (MANUAL)
```
Para cada piso crear RS case con CM desplazado:
  SEx_b1a: CM + ea_y en Y
  SEx_b1b: CM - ea_y en Y
  SEy_b1a: CM + ea_x en X
  SEy_b1b: CM - ea_x en X

ea_y = 0.05 × 13.821 = 0.691 m (para sismo X)
ea_x = 0.05 × 38.505 = 1.925 m (para sismo Y)
```
Material Apoyo Taller 2026 sección H explica esto paso a paso.

### Caso b) Forma 2 — Momentos torsionales (automático vía Python)
```
Crear load patterns: TorX+, TorX-, TorY+, TorY-
Aplicar momentos Mz en el CM de cada piso:
  Mz = Qi × ea  (proporcional al corte sísmico)
```
Ya implementado en 09_torsion_cases.py.

---

## Section Cuts — Verificar fuerzas en muros (Material Apoyo Taller)

Section Cuts se usan para extraer fuerzas (P, V, M) en secciones horizontales de muros.

```
Define > Section Cuts > Add New Cut
  - Tipo: Quadrilateral
  - Seleccionar área del muro
  - Nombrar: SC_Muro_Eje5_Piso1

Display > Show Tables > Section Cut Forces
  - Filtrar por combo (ej: C3_1.2D+L+SEx)
  - Leer: P (axial), V2, V3 (cortes), M2, M3 (momentos)
```

Estos valores (Pu, Vu, Mu) van directamente al diseño del muro.

---

## Diagramas de interacción P-M (Section Designer)

Para el diseño del muro eje 4 (T), usar Section Designer:
```
Define > Section Properties > Section Designer > New

1. Dibujar sección (T o rectangular)
2. Asignar materiales (G30, A630-420H)
3. Definir armadura tentativa
4. Run > PMM Interaction Surfaces
5. Verificar que todos los pares (Pu, Mu) sean ≤ ΦPMn
```

El manual `material-apoyo-taller/Section_Designer.pdf` tiene todo el detalle.
