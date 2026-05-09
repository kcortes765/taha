# APOS-X sync protocol - Edificio 1 WS2

## Idea base

Habra dos APOS-X relacionados:

- APOS local principal: este repo/chat, usado como coordinador y memoria canonica de decisiones.
- APOS WS2: copia operativa en la workstation nueva, usada para registrar lo que realmente pasa con ETABS 21 y el modelo `.EDB`.

No son dos verdades independientes. WS2 ejecuta y reporta; el APOS local consolida decisiones.

## Snapshot inicial

Este paquete trae un snapshot del APOS local en:

`transfer/ws2-ed1-etabs21-context/APOS_X_BASE/.apos`

En WS2, si el proyecto no tiene `.apos`, se puede usar esa carpeta como punto de partida.

## Regla critica

La regla de licencia ETABS 21 se mantiene por encima de cualquier automatizacion:

No usar mas de una instancia de ETABS 21.

## Flujo correcto

1. WS2 baja esta rama.
2. WS2 lee:
   - `README.md`
   - `LICENCIA_ETABS21_REGLA_CRITICA.md`
   - `HANDOFF_WS2_ED1.md`
   - `APOS_X_SYNC_PROTOCOL.md`
3. WS2 prepara su APOS local usando `APOS_X_BASE/.apos` si hace falta.
4. WS2 audita el modelo Edificio 1 sin modificarlo al inicio.
5. WS2 genera un reporte de estado.
6. Ese reporte vuelve al APOS local principal.
7. El APOS local principal actualiza decisiones, riesgos y siguiente paso.

## Que debe devolver WS2

Crear archivos nuevos, no reescribir historia:

```text
transfer/ws2-ed1-etabs21-context/reports/WS2_REPORTE_MODELO_ED1_YYYYMMDD_HHMM.md
transfer/ws2-ed1-etabs21-context/reports/WS2_APOS_DELTA_YYYYMMDD_HHMM.md
```

El reporte debe contener:

- estado confirmado
- cambios hechos en WS2
- evidencias/capturas/tablas
- dudas
- riesgos
- proximo paso recomendado

## Regla de conflicto

Si APOS local y APOS WS2 se contradicen:

1. Evidencia directa del modelo ETABS abierto manda.
2. Luego archivos `.EDB`/tablas/exportaciones.
3. Luego reportes WS2.
4. Luego APOS local historico.
5. Luego memoria de chat.

No borrar ni sobrescribir historia para resolver conflictos. Agregar una decision nueva que explique la correccion.

## Que no debe hacer WS2

- No editar el APOS local principal directamente con supuestos.
- No declarar cerrado un frente sin evidencia.
- No subir `.EDB` a git salvo decision explicita.
- No correr scripts destructivos o masivos sin checkpoint.
- No abrir segunda instancia de ETABS 21.

## Como sincronizar manualmente

Cuando WS2 tenga reporte, traerlo a este repo/chat y ejecutar aqui:

1. Leer reporte WS2.
2. Actualizar `.apos/STATUS.md`.
3. Append-only en `.apos/JOURNAL.md`.
4. Si hay decision, append-only en `.apos/DECISIONS.md`.
5. Si hay riesgo, actualizar `.apos/RISKS.md`.
6. Si hay dudas, actualizar `.apos/OPEN_QUESTIONS.md`.

