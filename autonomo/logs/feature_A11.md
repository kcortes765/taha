# Feature A11 — 10_combinations.py (NCh3171)

## Estado: COMPLETADO

## Archivo generado
- `autonomo/scripts/10_combinations.py` (~480 líneas)

## Qué implementa

Script Python + comtypes para definir combinaciones de carga LRFD según NCh3171:2017 en ETABS v19.

### 11 Combinaciones base (SDX/SDY)

| ID | Expresión | Tipo |
|----|-----------|------|
| C1 | 1.4·PP + 1.4·TERP + 1.4·TERT | Gravitacional |
| C2 | 1.2·D + 1.6·SCP + 0.5·SCT | Gravitacional |
| C3 | 1.2·D + 1.6·SCT + 1.0·SCP | Gravitacional |
| C4 | 1.2·D + 1.0·SCP + 1.4·SDX | Sismo X |
| C5 | 1.2·D + 1.0·SCP - 1.4·SDX | Sismo X |
| C6 | 1.2·D + 1.0·SCP + 1.4·SDY | Sismo Y |
| C7 | 1.2·D + 1.0·SCP - 1.4·SDY | Sismo Y |
| C8 | 0.9·D + 1.4·SDX | Volteo X |
| C9 | 0.9·D - 1.4·SDX | Volteo X |
| C10 | 0.9·D + 1.4·SDY | Volteo Y |
| C11 | 0.9·D - 1.4·SDY | Volteo Y |

Donde D = PP + TERP + TERT (todas las cargas permanentes con mismo factor).

### Envolvente
- **ENV**: Envelope (tipo 1) de C1 a C11 — captura máximo/mínimo para diseño.

### Torsión Forma 2 (opcional, --torsion-f2)
- Crea 8 combos adicionales CT4-CT11 usando SDTX/SDTY en vez de SDX/SDY.
- Omite C1-C3 gravitacionales (ya existen como base).
- Crea envolvente **ENVT** con C1-C3 + CT4-CT11.

### Funcionalidades del script
- **verify_prerequisites()** — verifica que existan load patterns (PP, TERP, TERT, SCP, SCT) y casos sísmicos (SDX, SDY)
- **delete_existing_combos()** — limpieza para re-ejecución segura
- **create_combo()** — crea combo LinearAdd + agrega casos con SetCaseList
- **create_envelope()** — crea combo Envelope con sub-combos (CNameType=1)
- **verify_combos()** — verificación con GetNameList + spot checks (GetCaseList)
- **_build_combos()** — función parametrizada para generar combos con diferentes nombres de casos sísmicos

## Corrección vs config.py

El diccionario `COMBINATIONS` en config.py:
1. Usa 'SX'/'SY' en vez de 'SDX'/'SDY' (nombres reales de los casos ETABS)
2. Omite TERT en todas las combinaciones

El script corrige ambos problemas definiendo los combos directamente con nombres ETABS correctos y TERT incluido.

## COM Signatures usadas
- `RespCombo.Add(Name, ComboType)` — §16.1, ComboType: 0=LinearAdd, 1=Envelope
- `RespCombo.SetCaseList(Name, CNameType, CName, SF)` — §16.2, CNameType: 0=Case, 1=Combo
- `RespCombo.GetNameList()` — §16.4, retorna (count, names, ret)
- `RespCombo.GetCaseList(Name)` — §16.3, retorna (n, types, names, SFs, ret)
- `RespCombo.Delete(Name)` — §16.5
- `LoadPatterns.GetNameList()` — verificación prereqs
- `LoadCases.GetNameList()` — verificación prereqs

## Fuentes consultadas
- NCh3171:2017 (combinaciones LRFD)
- Material Apoyo Taller 2026 Sección I (4 variantes de combinaciones)
- Material Apoyo Sección G (8 sub-combinaciones internas de ETABS)
- autonomo/research/etabs_api_reference.md §16
- autonomo/research/com_signatures.md
- config.py COMBINATIONS (referencia, corregida en el script)

## Notas sobre NCh3171
- Factor 1.4 en E es el load factor sísmico per NCh3171:2017
- ETABS genera internamente 8 sub-combinaciones de signos para cada combo con sismo
- Para Forma 2 (SDTX/SDTY), ETABS aplica ±e internamente → menos combos manuales
- La envolvente ENV es crítica para diseño — captura extremos de todos los estados
