# GOVERNANCE — ADSE 1S-2026

## Roles
- **Humano**: Alumno, decisor final. Opera ETABS en lab.
- **IA (Claude Code)**: Genera/corrige código, analiza planos, prepara material de estudio.
- **IAs externas**: Consulta puntual para validación cruzada (geometría, etc.)

## Autonomía del agente
**Puede decidir solo:**
- Estructura de código, refactors, fixes menores
- Generación de material de estudio
- Optimizaciones del pipeline

**Debe consultar antes de:**
- Cambiar geometría del edificio (config.py)
- Decisiones de modelado sísmico (R*, espectro, combinaciones)
- Push a GitHub
- Crear commits

## Convenciones
- Español por defecto
- Unidades: tonf, m, kgf/cm², MPa (Ton_m_C en ETABS)
- Respuestas directas y concisas
- Código Python 3.12+, comtypes para COM

## Reglas de actualización
- STATUS y BOOTSTRAP se actualizan al cierre de cada sesión
- DECISIONS se actualiza cuando se toma cualquier decisión no trivial
- WORKING_MODEL se reconcilia (reescribe), no se apila

## Calidad
- Config.py debe verificarse contra planos antes de correr en ETABS
- Pipeline debe probarse en ETABS real (no solo sintácticamente)
- Siempre tener fallback manual documentado para el lab
