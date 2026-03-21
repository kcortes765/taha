# Instrucciones de Coding — ADSE 1S-2026

## Para material de estudio (.md)
- Lee el PDF original COMPLETO antes de escribir (usa `Read` con `pages`)
- Lee `docs/apuntes/INDICE.md` para ubicar el tema
- Estructura: mapa conceptual → contenido → preguntas tipo control
- Calidad > cantidad: eliminar relleno, cada oración debe aportar
- Diagramas ASCII precisos donde el PDF tiene figuras
- Notas "Claude:" solo cuando agregan valor real (contexto, ejemplo, conexión)
- Preguntas tipo control: 5-8 por sección principal, nivel IX semestre ingeniería civil
- Referencia exacta: "Pág X del PDF" o "Art. X de NCh433"

## Para scripts Python (ETABS API)
- Python 3.8+, comtypes para COM
- Firmas COM verificadas contra autonomo/research/com_signatures.md
- Docstrings en español, código en inglés
- Manejo de errores COM con mensajes claros
- NO inventar funciones de API

## Para correcciones
- Leer autonomo/research/validacion_cruzada.md para las discrepancias
- Leer autonomo/research/informe_final.md para las observaciones
- Priorizar la guía UI como fuente de verdad para valores del edificio
- Los scripts deben coincidir con la guía

## Verificación
- Al terminar, verificar coherencia interna del archivo
- Verificar que fórmulas coincidan con normas/apuntes
- Verificar que no se rompió nada existente
