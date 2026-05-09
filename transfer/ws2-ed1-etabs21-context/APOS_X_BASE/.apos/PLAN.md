# PLAN - ADSE 1S-2026

## Fase 0: Auditoria externa Ed.1 con GPT-5.4 Pro [LISTA]
- Paquete `review-ia/ed1-gpt54pro-10-sesiones/` creado y poblado
- 10 sesiones separadas listas
- Pendiente: correrlas y convertir hallazgos en decisiones del repo

## Fase 1: Canon y alcance Ed.2 [85%]
- Canon Ed.2 Parte 1 consolidado
- Auditoria tecnica consolidada
- Confusion Ed.1 vs Ed.2 resuelta con evidencia del enunciado
- Pendiente: congelar una version final de guia UI ETABS 21 ya auditada

## Fase 2: Guia UI Ed.2 ETABS 21 [EN CURSO]
- Paquete de auditoria externa listo
- Evidencia de contexto y clases Music relevantes ya incluida
- Pendiente: recibir hallazgos de otra IA o ejecutar esa auditoria localmente y aplicar correcciones finales a la guia

## Fase 3: Pipeline Ed.2 ETABS 21 [EN CURSO]
- Codigo Ed.2 rebaselinado al flujo estatico oficial
- Arranque por consola endurecido para ETABS 21 WS UCN
- Runtime root portable + bundle WS + empaquetado de retorno listos
- Repo GitHub remoto ya poblado para que la WS baje codigo real por `git`
- Pendiente: corrida viva en ETABS 21 con evidencia real
- Pendiente: validar guia UI contra comportamiento real del modelo

## Fase 4: Entrega intermedia Ed.1 + Ed.2 [ACTIVA]
- Modal de ambos edificios exigido por correo del 2026-04-15
- Para Ed.2: mantener modal como apoyo y exigencia de entrega, no como reemplazo del analisis estatico Parte 1

## Prioridad inmediata
1. Retomar Ed.1 solo cuando vuelva licencia ETABS 21 en la WS
2. Abrir `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS\prog\Edif1\ED1_PARTE1_COMPLETA_TRABAJO.EDB`
3. Re-verificar correcciones base reportadas:
   - vigas `Cardinal Point = 2`
   - offsets automaticos y `Rigid Zone Factor = 0.75`
   - releases solo `M2/M3` donde corresponde
   - apoyos base empotrados
   - losa con `m11/m22/m12 = 0.25`
4. Asignar diafragma rigido
5. Crear patrones `PP/SCP/SCT/TERP/TERT`
6. Aplicar cargas de uso, terminaciones y techo
7. Definir fuente de masa
8. Crear modal/espectral
9. Resolver torsion accidental / 6 casos
10. Exportar tablas: peso sismico, CM/CR, periodos, corte basal, drifts, Story Forces y esfuerzos en muros eje 1/eje F
