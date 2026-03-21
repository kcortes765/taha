# Tarea Actual — Agente Autónomo ETABS

## Progreso: 26/27 features completadas

## Feature actual: V02 — Revisión final — calidad y completitud
**Fase**: validation

## Descripción de la tarea
Revisión final exhaustiva de TODO lo producido.

1. Leer la guía UI completa — verificar coherencia interna
2. Leer cada script API — verificar que compila, tiene docstrings, maneja errores
3. Verificar que todos los valores numéricos son consistentes entre documentos
4. Verificar que las referencias normativas son correctas
5. Lista de verificación:
   - [ ] Todos los ejes y coordenadas correctos
   - [ ] Todos los materiales con propiedades correctas
   - [ ] Todos los muros con espesor correcto por eje
   - [ ] Todas las cargas con valores correctos
   - [ ] Espectro calculado correctamente
   - [ ] 6 casos de análisis definidos
   - [ ] Drift, fuerzas, modos: método de extracción documentado
   - [ ] Scripts API compilables y documentados
6. Generar informe final en autonomo/research/informe_final.md
7. Actualizar RETOMAR.md con el estado final

## Outputs esperados
- autonomo/research/informe_final.md
- RETOMAR.md

## Features ya completadas
- R01
- R02
- R03
- R04
- R05
- R06
- G01
- G02
- G03
- G04
- G05
- A01
- A02
- A03
- A04
- A05
- A06
- A07
- A08
- A09
- A10
- A11
- A12
- A13
- A14
- V01

## Instrucciones obligatorias
1. Lee `autonomo/context.md` PRIMERO para el contexto completo del proyecto
2. Ejecuta la tarea descrita arriba con máximo rigor y exhaustividad
3. Si necesitas investigar en internet, hazlo (web search, web fetch)
4. Escribe los resultados en los archivos indicados en "Outputs esperados"
5. Al terminar, escribe un resumen breve en `autonomo/logs/feature_V02.md`
6. NO modifiques autonomo/progress.json — el orquestador lo gestiona

## Reglas
- Español para explicaciones, inglés para código/ETABS
- Para scripts API: Python + comtypes, compatible ETABS v19 (CSI OAPI)
- No inventar funciones de API — usar solo las documentadas
- Verificar contra las normas originales cuando corresponda
- Ser exhaustivo: esta es una tarea crítica
