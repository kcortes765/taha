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
1. Empujar el paquete `transfer/ws-u-ed1-ui-context/` a rama Git `codex/ws-u-ed1-ui-context`
2. Descargar esa rama en la WS UCN
3. Continuar Edificio 1 por UI en ETABS 21 usando el `.EDB` local de la WS
4. Usar `transfer/ws-u-ed1-ui-context/files/13_GUIA_ED1_ETABS_v21.md` como guia activa
5. Verificar vigas invertidas por asignacion/tablas, no solo por apariencia 3D
6. No versionar `.EDB` salvo decision posterior con Git LFS
7. Correr primero la nueva sesion `01_GEOMETRIA_CANONICA_UI_API_ETABS21` si se necesita auditoria externa de geometria
8. Consolidar hallazgos de Ed.1 antes de avanzar a masa, torsion, drift o resultados
