# LEARNINGS — ADSE 1S-2026

## L-001 — COM de ETABS 19 es frágil: separar sesiones
- La sesión COM muere después de geometría pesada (>1700 areas + mesh)
- Fix: separar pipeline en fase 1 (geometría) y fase 2 (análisis) con reinicio de ETABS
- Siempre matar ETABS → abrir manual → esperar 25s → conectar

## L-002 — Helper.CreateObject produce instancias invisibles
- Si ETABS se crea via CreateObject, es invisible y File.Save produce .edb corrupto
- Fix: SIEMPRE abrir ETABS manualmente → conectar via GetActiveObject
- El .edb corrupto parece válido pero no abre

## L-003 — comtypes/gen stale causa binding inconsistente
- Los TLBs cached de sesiones anteriores pueden ser de otra versión
- Fix: limpiar comtypes/gen ANTES de cada sesión (excepto __init__.py)

## L-004 — get_story_data() siempre falla en v19
- No abortar por eso. NewGridOnly(ret=0) garantiza stories correctas.
- El análisis funciona igual.

## L-005 — GitHub raw CDN cachea archivos
- NUNCA descargar archivos individuales via raw.githubusercontent.com
- SIEMPRE descargar ZIP completo del repo

## L-006 — Geometría interpretada por IA no es confiable sin verificación visual
- 3 iteraciones de config.py por diferentes IAs, ninguna produjo geometría correcta
- Los LLMs no pueden "ver" planos con precisión suficiente para extraer coordenadas
- Verificación visual en ETABS/AutoCAD es imprescindible

## L-007 — CSS debe coincidir con HTML
- El CSS original de app-c1 usaba selectores de clase pero HTML tenía IDs
- Siempre verificar que selectores CSS coincidan con atributos HTML reales
