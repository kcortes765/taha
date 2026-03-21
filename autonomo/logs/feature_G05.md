# Feature G05 — Completar guía FASES 6-13

## Estado: COMPLETADO
## Fecha: 2026-03-21

## Archivo modificado
- `docs/estudio/GUIA-COMPLETA-EDIFICIO1-ETABS-v19.md` (2133 → 2834 líneas, +701 líneas)

## Fuentes consultadas
- `autonomo/research/lafontaine_extracto.md` — Tutorial Lafontaine completo
- `autonomo/research/material_apoyo_extracto.md` — Material Apoyo Prof. Music completo
- Guía existente (FASES 0-13 leídas íntegramente)

## Cambios realizados

### FASE 6 — Cargas
- Agregada tabla de mapeo nomenclatura proyecto ↔ NCh3171 (PP/TERP/SCP/SCT vs D/Sd/L/Lr)
- Nota sobre tipos ETABS correctos (Super Dead para terminaciones)
- Origen del valor TERP = 0.140 tonf/m² (desglose cielo/piso/tabiques/instalaciones)
- Instrucciones detalladas para distinguir zonas de pasillo vs oficina en ETABS (4 pasos)
- Recomendación práctica para el taller (usar 0.250 uniforme)
- Paso 6.4: Verificación visual de cargas asignadas con Display > Show Load Assigns
- Tabla resumen de cargas por zona (tipo vs techo)
- Tip de Lafontaine: apagar muros antes de seleccionar losas

### FASE 9 — Combinaciones de carga
- Referencia normativa NCh3171-2017 con las 7 combinaciones base (U1-U7)
- Tabla de mapeo explícita NCh3171 → nomenclatura del proyecto
- Nota sobre expansión de U4-U7 a múltiples combos (por sismo X/Y + torsión)
- Sección "Nota sobre reducción por R*" con Método B (factor en combinaciones)
- Ejemplo numérico: si R*=8.64, factor sismo = 1.4/8.64 = 0.1620
- Advertencia sobre Qmín y factor de escala adicional

### FASE 10 — Ejecutar y validar
- **Paso 10.3: P-Delta** (NUEVO, antes no existía):
  - Método iterativo (Analyze > Set Analysis Options > P-Delta)
  - Tabla de Load Cases para P-Delta (PP=1.0, TERP=1.0, SCP=0.25)
  - Método alternativo via Nonlinear Static Load Case
  - Explicación de qué cambia (períodos +2-5%, drifts +3-8%)
- **Paso 10.4: Solver** (NUEVO): Advanced Solver vs Multi-threaded
- Paso 10.5 (Check Model): tabla de errores comunes con causas y soluciones
- Paso 10.6 (Run): nota sobre verificación de Load Cases antes de correr
- Paso 10.7 (Log): lista de warnings aceptables vs warnings que requieren atención
- **Paso 10.10: Troubleshooting** (NUEVO): tabla completa síntoma→causa→solución

### FASE 12 — Los 6 casos de análisis
- Expansión masiva (de ~35 líneas a ~130 líneas)
- Diagrama de flujo ASCII de las 3 etapas (preparación → rígido → semi-rígido)
- Nota sobre recalcular TEX/TEY para Caso 5 (cortes cambian con diafragma)
- Paso 12.2: tabla de resultados a extraer por caso (8 tipos de tabla ETABS)
- Tip: organización de carpetas por caso
- Paso 12.3: tabla comparativa rígido vs semi-rígido (7 aspectos)
- Paso 12.4: verificaciones cruzadas entre los 6 casos (5 checks)

### FASE 13 — Entregables específicos
- Expansión masiva (de ~20 líneas a ~360 líneas)
- **Entregable 1**: contenido, figuras, formato (1-2 págs)
- **Entregable 2**: 5 capturas específicas, texto complementario
- **Entregable 3.1**: tabla peso por piso, cálculo peso/m²
- **Entregable 3.2**: tabla densidad muros, valores típicos
- **Entregable 3.3**: tabla CM/CR por piso con excentricidades
- **Entregable 3.4**: tabla modal, tabla resumen, capturas deformadas
- **Entregable 3.5**: tabla del profesor completa, 2 gráficos de espectros
- **Entregable 3.6**: tablas corte/momento, 2 tipos de gráficos
- **Entregable 3.7**: tablas indicadores 1 y 13 con interpretación
- **Entregable 4.1**: plantillas para tablas Cond.1 y Cond.2, tabla resumen 6 casos
- **Entregable 4.2**: plantilla tabla Pier Forces 6 casos, gráfico recomendado
- **Entregable 4.3**: cuadro resumen final, 6 puntos para conclusiones
- **Estructura sugerida del informe**: índice completo del informe final

### Checklist final
- Reorganizada en 4 secciones: geometría, modelo, cargas, análisis
- Agregados: tipos ETABS correctos, verificación visual cargas, P-Delta, solver, damping consistency
- Post-análisis: verificar drifts desde combinaciones, capturas, archivos guardados

## Verificaciones realizadas
- Numeración de pasos FASE 10: 10.1-10.10 (sin saltos)
- FASES 0-13 todas presentes con headers correctos
- Referencias cruzadas entre fases verificadas
- Valores numéricos consistentes con context.md y CLAUDE.md
