# Feature A09 — 08_seismic.py (masa, espectro, modos)

**Estado**: COMPLETADO
**Fecha**: 2026-03-21
**Output**: `autonomo/scripts/08_seismic.py`

## Resumen

Script de configuración sísmica completa para Edificio 1. Implementa 4 pasos:

1. **Mass Source** — `PropMaterial.SetMassSource_1` (6 args, en PropMaterial NO en MassSource)
   - IncludeElements=True (captura PP con SWM=1)
   - TERP×1.0, SCP×0.25 (NCh433 Art. 5.4.3)

2. **Función de espectro** — `Func.FuncRS.SetUser` (5 args)
   - Lee `espectro_elastico_Z3SC.txt` en Python (101 puntos, T=0-5s)
   - **SetFromFile NO EXISTE en ETABS** (confirmado en R03 §10.2) — se usa SetUser
   - Fallback a `Func.ResponseSpectrum.SetUser` si FuncRS no resuelve en binding
   - Sa/g adimensional, SF=9.81 se aplica en el load case

3. **Caso Modal** — `LoadCases.ModalEigen` (firmas confirmadas vía CSI OAPI docs)
   - SetCase("Modal"), SetNumberModes(30, 1), SetParameters(tol=1E-9)
   - SetInitialCase("", zero initial conditions)
   - 30 modos para >90% participación masiva en edificio de 20 pisos

4. **Casos de espectro** — `LoadCases.ResponseSpectrum`
   - SDX: U1, Esp_Elastico_Z3SC, SF=9.81
   - SDY: U2, Esp_Elastico_Z3SC, SF=9.81
   - SetModalCase → "Modal"
   - CQC (modal) y SRSS (direccional) son defaults de ETABS
   - Excentricidad accidental NO se configura aquí (script separado)

## Firmas COM verificadas

| Función | Args | Fuente |
|---------|------|--------|
| `PropMaterial.SetMassSource_1` | 6 | com_signatures §12.1 |
| `Func.FuncRS.SetUser` | 5 | com_signatures §10.1 |
| `Func.FuncRS.SetFromFile` | — | **NO EXISTE EN ETABS** (§10.2) |
| `LoadCases.ModalEigen.SetCase` | 1 | CSI OAPI docs |
| `LoadCases.ModalEigen.SetNumberModes` | 3 | CSI OAPI docs |
| `LoadCases.ModalEigen.SetParameters` | 5 | CSI OAPI docs |
| `LoadCases.ModalEigen.SetInitialCase` | 2 | CSI OAPI docs |
| `ResponseSpectrum.SetCase` | 1 | com_signatures §11.1 |
| `ResponseSpectrum.SetLoads` | 7 | com_signatures §11.2 |
| `ResponseSpectrum.SetModalCase` | 2 | com_signatures §11.3 |

## Decisiones de diseño

- PP no se incluye en los load patterns del Mass Source porque ya está capturado por IncludeElements=True (self-weight multiplier = 1.0)
- Se usa SetUser en vez de SetFromFile porque esta última función es de SAP2000, no de ETABS
- Tolerancia 1E-9 (más estricta que el default 1E-7) para mejor precisión
- 30 modos (no 20) para asegurar >90% de participación masiva en ambas direcciones
- Fallback automático entre Func.FuncRS y Func.ResponseSpectrum (el path COM varía según binding)

## Patrón de código

Consistente con 07_loads.py: connect → set_units → pasos numerados → verificación → resumen.
