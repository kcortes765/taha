# APOS_X_BASE

Snapshot del APOS-X local al momento de preparar el handoff WS2.

Uso previsto:

1. En WS2, si el repo no trae `.apos`, copiar `APOS_X_BASE/.apos` a la raiz del repo.
2. Leer `.apos/CONTEXT_POLICY.md`, `.apos/STATUS.md` y `.apos/HANDOFF.md`.
3. Registrar cualquier hallazgo nuevo como delta append-only.
4. Devolver reportes en `transfer/ws2-ed1-etabs21-context/reports/`.

Este snapshot no reemplaza la memoria principal. Sirve para que WS2 parta con el mismo contexto y devuelva evidencia trazable.

