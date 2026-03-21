# Índice de Archivos de Contexto — Taller ADSE 2026

## Cómo usar estos archivos

Estos MDs capturan TODO el contexto del Taller de Análisis y Diseño Sísmico de Edificios
para poder continuar el trabajo en cualquier sesión sin perder información.

**Leer siempre en este orden:**
1. Este archivo (00_INDICE_CONTEXTO.md)
2. El MD relevante al tema en que se trabaja

---

## Archivos disponibles

| Archivo | Contenido | Cuándo usarlo |
|---------|-----------|---------------|
| `01_TALLER_OVERVIEW.md` | Overview completo: ambos edificios, entregables, fechas, evaluación | Inicio de sesión |
| `02_PARAMETROS_SISMICOS_NORMATIVA.md` | Espectro NCh433+DS61, R*, combinaciones NCh3171, drift, torsión | Análisis sísmico |
| `03_EDIFICIO1_GEOMETRIA_COMPLETA.md` | Grilla exacta, todos los muros y vigas por eje, losas | Modelación |
| `04_DISENO_MUROS_HA.md` | Procedimiento completo: corte, flexión, curvatura, confinamiento | Diseño Ed.1 |
| `05_DISENO_MARCOS_HA.md` | Vigas, columnas, nudos, col.fuerte-viga débil, Mpr | Diseño Ed.2 |
| `06_ETABS_WORKFLOW.md` | Flujo ETABS para Ed.1 (pipeline) y Ed.2 (manual), Section Cuts | Modelación |
| `07_TABLAS_REFERENCIA_RAPIDA.md` | Todas las tablas: parámetros suelo, barras, fórmulas clave | Consulta rápida |

---

## Material complementario (PDFs en la misma carpeta)

Ver `../INDICE_TALLER.md` para el índice completo de PDFs disponibles.

**Los más importantes:**
- `enunciado/Enunciado Taller.pdf` — Datos oficiales de los edificios
- `material-apoyo-taller/Material Apoyo Taller 2026.pdf` — Guía Prof. Music (★★★)
- `diseno-muros/Ejemplos Diseño de MHA J.M.pdf` — 2 ejemplos completos normativa vigente
- `normas/DECRETO 61...pdf` — DS61 (parámetros sísmicos)
- `normas/DECRETO 60...pdf` — DS60 (diseño HA)

---

## Estado actual del taller (5 marzo 2026)

### ✅ Completado
- Pipeline Python para Ed.1 (14 pasos con 07c, commit 89d810c base)
- Bug "geometría fantasma" resuelto (config_helper.py v3)
- Verificación post-creación en cada paso de geometría
- Generación automática de espectro, combos NCh3171, torsión b2
- **Paso 07c**: Auto-Mesh via API (con fallback a instrucciones manuales)
- **Paso 11**: Verificación Qmin NCh433 integrada post re-análisis
- **Paso 12**: Verificación Qmin con corrección de escala automática

### 🔄 En progreso
- Probar pipeline actualizado en lab con ETABS 19

### ⏳ Pendiente
- **P-Delta** (manual en ETABS, API muy inestable)
- Análisis completo Ed.1 en ETABS
- Verificaciones: peso ~1 tonf/m², drift < 0.002, periodos T*
- Diseño muros eje 4 (T) y eje 5 (rectangular) — piso 1
- Modelar Ed.2 manualmente en ETABS
- Diseño vigas y columnas marco eje A

### ★ Checklist pre-entrega (ver 06_ETABS_WORKFLOW.md §CHECKLIST)
1. **Auto-Mesh** ← automático (07c) o manual si falla
2. **Qmin** ← automático (pasos 11 y 12)
3. **P-Delta** ← siempre manual
4. **Modificadores inercia** ← ya correctos en código

---

## Fechas críticas

| Fecha | Evento |
|-------|--------|
| **5 mayo** | **Control 1 (C1)** — Sismología |
| **26 mayo** | **Control 2 = Expo 1** — Análisis sísmico |
| 16 junio | Expo 2 — Diseño avanzado |
| 30 junio | Control 3 — Diseño muros + marcos |
| 7 julio | Expo 3 — Entrega final |

---

## Repositorio del pipeline

- **URL**: https://github.com/kcortes765/taller-etabs
- **Commit actual**: 89d810c (Fix v3)
- **Descargar ZIP en lab**: ver `06_ETABS_WORKFLOW.md`

---

## Notas técnicas importantes

### ETABS API (para la IA de revisión)
- Se usa comtypes (Python) para comunicarse con ETABS via COM
- Bug crítico resuelto: `Helper.CreateObject` crea instancias invisibles
- Fix: priorizar `GetActiveObject`, forzar `Visible=True` si se crea nueva instancia
- Ver `../CONTEXTO_REVIEW.md` para contexto completo del código

### Práctica chilena en ETABS (de Lafontaine)
- **J=0** para vigas (sin rigidez torsional)
- **Inercia losa = 25%** (modificadores f11=f22=0.25)
- **Peso sísmico/área/piso ≈ 1 tonf/m²** (validación del modelo)
- **Vs30** determina tipo de suelo para NCh433
