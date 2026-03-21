# OPEN QUESTIONS — ADSE 1S-2026

## OQ-001 — Shaft: ¿2.945m es dimensión en Y o en Z? [BLOQUEANTE]
- Contexto: Page 3 muestra shaft 7.7m × 2.945m. Si 2.945m es en Y, el shaft cruza más allá de C-D (1.55m), hasta y=9.391 (entre D y E). Esto cambiaría paneles de losa y muros.
- Impacto: Cambia SLAB_PANELS (gap en D-F) y posición de muros del shaft
- Acción: Verificar visualmente en plano y preguntar a ayudante si es necesario

## OQ-002 — Shaft: ¿Paredes verticales en ejes 10/11 o en bordes reales?
- Contexto: Bordes reales del shaft = x=17.415 y x=25.115 (off-grid). Ejes 10 (21.665) y 11 (24.990) están dentro del shaft.
- Impacto: Si los muros deben estar en bordes reales, necesitan coordenadas absolutas (no de grilla)
- Acción: Verificar contra elevaciones y plantas

## OQ-003 — Eje F: ¿hay más muros además del central de 7.7m?
- Contexto: Page 2 muestra el muro central pero es ambiguo si hay stubs adicionales en 4-5 o 14-15
- Impacto: Afecta rigidez en dirección Y del borde norte
- Acción: Verificar con page 7 (Elevación Eje F)

## OQ-004 — Ejes 6-7 zona A-C: ¿tienen muros?
- Contexto: Config actual no tiene muros dir Y en ejes 6-7 para zona A-C (sur). En el plano no se ven claramente.
- Impacto: Menor — son ejes secundarios

## OQ-005 — SetFromFile firma correcta para ETABS v19
- Contexto: 4 variantes implementadas pero ninguna probada en sesión COM estable
- Acción: Probar en lab cuando geometría esté resuelta
