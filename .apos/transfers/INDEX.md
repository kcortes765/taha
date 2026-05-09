# Transfers Index

## 2026-05-08 - WS2 Edificio 1 ETABS 21

- Ruta: `transfer/ws2-ed1-etabs21-context/`
- Rama: `codex/ws2-ed1-etabs21-context`
- Objetivo: pasar contexto minimo y reglas operativas a otra IA/Codex en WS2 para auditar el modelo Edificio 1.
- Regla critica: una sola instancia de ETABS 21; no abrir ni automatizar segunda instancia.
- Ruta WS2 esperada: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2`
- Ruta corregida para clonar contexto: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\codex_ws2_context`
- Primer entregable esperado desde WS2: reporte de estado del `.EDB` activo antes de modificar.
- Enunciado prioritario: `transfer/ws2-ed1-etabs21-context/files/01_Enunciado_Taller_actualizado_2026-05-04.pdf`
- Apuntes prioritarios: `transfer/ws2-ed1-etabs21-context/files/00_Apuntes_del_Curso_2026-05-08_actualizado.pdf`
- Alcance actualizado: Parte 1 de Edificio 1 y Edificio 2.
- Delta 2026-05-08 noche:
  - WS2 ya audito Ed.1 y Ed.2 por OAPI con una sola instancia ETABS.
  - Se agrego codigo a `transfer/ws2-ed1-etabs21-context/code/`.
  - Ed.1 va primero hasta cierre Parte 1; Ed.2 queda despues.
  - Los releases torsionales de Ed.1 fueron pedidos por el profesor y no se deben eliminar por defecto.
  - Nuevo prompt operativo: `transfer/ws2-ed1-etabs21-context/PROMPT_EJECUCION_WS2_ED1_PRIMERO.md`.
