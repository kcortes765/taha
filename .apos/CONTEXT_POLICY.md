# CONTEXT_POLICY

## Lectura minima

1. `CONTEXT_POLICY.md`
2. `INDEX.md`
3. `STATUS.md`
4. `HANDOFF.md`
5. `PLAN.md`
6. `RISKS.md` y `OPEN_QUESTIONS.md` si la tarea afecta seguridad, ejecucion o decisiones.

## Lectura bajo demanda

- `ACTIVE_SPEC.md` para alcance activo.
- `WORKING_MODEL.md` para arquitectura y flujos.
- `DECISIONS.md` para decisiones activas.
- `JOURNAL.md` para historia reciente.
- `NARRATIVE.md` solo para onboarding o confusion historica.
- `SOURCES.md` y `RESEARCH_LOG.md` para evidencia externa o research.

## Prioridad de evidencia

1. Archivos reales actuales
2. Resultados de comandos recientes
3. `DECISIONS.md`
4. `STATUS.md`
5. `JOURNAL.md`
6. `NARRATIVE.md`
7. Chat actual
8. Memoria conversacional
9. Fuentes externas

## Clasificacion obligatoria

- Hecho verificado
- Decision
- Inferencia
- Pendiente
- Riesgo
- Desconocido

## Cuando pedir confirmacion

- Antes de modificar global/user/system skills, hooks o config.
- Antes de borrar, mover o sobrescribir memoria.
- Antes de ejecuciones productivas, grandes, destructivas, batch, GPU, ambiguas o costosas.

## Cuando usar safe-harness

- Produccion, batch, GPU, comandos destructivos, cambios masivos, `run_production.py`, o cualquier comando con riesgo de costo o perdida.

## Que no cargar por defecto

- Conversaciones completas.
- `transfers/raw/`.
- `snapshots/large/`.
- Logs extensos sin una pregunta concreta.
