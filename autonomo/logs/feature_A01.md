# Feature A01 — config.py (conexion ETABS + datos edificio)

## Estado: COMPLETADO
**Fecha**: 2026-03-21

## Output
- `autonomo/scripts/config.py` (~550 lineas)

## Contenido del script

### 14 secciones:
1. **Constantes ETABS** — eUnits, eMatType, eLoadPatternType, eShellType, Cardinal Points, ProgIDs COM
2. **Grilla** — 17 ejes X + 6 ejes Y con coordenadas exactas del enunciado
3. **Pisos** — 20 pisos, h1=3.40m, h_tip=2.60m, elevaciones acumuladas, H_total=52.80m
4. **Materiales** — G30 y A630-420H en unidades Tonf_m_C (factor 101.937), propiedades no lineales
5. **Secciones** — VI20x60G30, MHA30G30, MHA20G30, Losa15G30 + modifiers (J=0, losa 25%)
6. **Muros dir Y** — 26 segmentos, espesores verificados por eje
7. **Muros dir X** — 23 segmentos, machones eje C (30cm) + stubs A/D/E/F (20cm)
8. **Vigas** — 30 por piso (10 eje A + 8 eje F + 12 eje B)
9. **Losas** — 7 paneles piso tipo + 5 paneles techo, area=468.4 m2, CM=(21.120, 6.927)
10. **Cargas** — TERP, TERT, SCP, SCT en tonf/m2 + Mass Source (PP+TERP+0.25*SCP)
11. **Parametros sismicos** — Zona 3, Suelo C, R=7, Ro=11, combinaciones NCh3171 (C1-C11)
12. **Formulas sismicas** — alpha (Ec.9), R* (Ec.10), R*_alt (Ec.11), C, Cmin, Cmax
13. **Conexion COM** — Patron robusto 3 niveles: GetActiveObject > Helper.GetObject > CreateObject
14. **Helper functions** — check_ret, verify_model, unlock_model, set_units, get_section_name

### Datos verificados contra:
- Enunciado Taller paginas 2-7
- Config.py anterior (taller-etabs/config.py)
- Investigaciones R01 (API ref), R02 (patrones), R03 (firmas COM), R04 (formulas)

### Self-test exitoso:
```
Grilla: 17 ejes X, 6 ejes Y | Lx=38.505, Ly=13.821
Pisos: 20 | H=52.8m
Materiales: Ec=2,624,160 tonf/m2 | fy=42,813.5 tonf/m2
Geometria: 26+23 muros, 30 vigas/piso, 7 paneles losa
Area piso: 468.4 m2 | CM=(21.120, 6.927)
Peso esperado: ~9368 tonf
Formulas: alpha, R*, Cmin=0.07, Cmax=0.147
Espectro: archivo .txt encontrado
```

### Diferencias vs config anterior:
- **Nuevo**: conexion COM completa con clean_comtypes_gen(), connect(), disconnect()
- **Nuevo**: constantes ETABS (eUnits, eMatType, etc.)
- **Nuevo**: materiales en Tonf_m_C (antes solo MPa/kgf)
- **Nuevo**: formulas sismicas (alpha, R*, C, Cmin, Cmax)
- **Nuevo**: combinaciones NCh3171 (C1-C11)
- **Nuevo**: Mass Source config
- **Nuevo**: check_ret(), verify_model(), unlock_model()
- **Nuevo**: SPECTRUM_FILE path + SPECTRUM_SF
- **Corregido**: R* usa NCh433 Ec. 10 verificada (antes usaba formula DS61 diferente)
- **Mantenido**: toda la geometria identica al config probado en lab
