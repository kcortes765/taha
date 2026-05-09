# START AQUI - WS2 Edificio 1

## 1. Regla de licencia

No abrir mas de una instancia de ETABS 21.

Antes de abrir ETABS o correr scripts:

```powershell
Get-Process ETABS -ErrorAction SilentlyContinue
```

Si aparece una instancia, no abrir otra.

## 2. Ruta real

La raiz real de trabajo es:

```text
C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2
```

El repo/contexto debe quedar dentro:

```text
C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\codex_ws2_context
```

No usar `C:\Users\Civil\Documents\taha` para este flujo.

## 3. Comandos Git

```powershell
cd "C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2"
git clone https://github.com/kcortes765/taha.git codex_ws2_context
cd "C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\codex_ws2_context"
git fetch origin
git checkout codex/ws2-ed1-etabs21-context
```

Si ya existe:

```powershell
cd "C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\codex_ws2_context"
git fetch origin
git checkout codex/ws2-ed1-etabs21-context
git pull --ff-only origin codex/ws2-ed1-etabs21-context
```

## 4. Leer en orden

1. `transfer/ws2-ed1-etabs21-context/LICENCIA_ETABS21_REGLA_CRITICA.md`
2. `transfer/ws2-ed1-etabs21-context/PROTOCOLO_UN_EDIFICIO_UNA_INSTANCIA.md`
3. `transfer/ws2-ed1-etabs21-context/APOS_X_SYNC_PROTOCOL.md`
4. `transfer/ws2-ed1-etabs21-context/HANDOFF_WS2_ED1.md`
5. `transfer/ws2-ed1-etabs21-context/CODIGO_WS2_MANIFEST.md`
6. `transfer/ws2-ed1-etabs21-context/FUENTES_PRIORITARIAS_WS2.md`
7. `transfer/ws2-ed1-etabs21-context/ENUNCIADO_CAMBIOS_2026-05-04.md`
8. `transfer/ws2-ed1-etabs21-context/APUNTES_CAMBIOS_2026-05-08.md`
9. `transfer/ws2-ed1-etabs21-context/PARTE1_ED1_ED2_PROGRAMATICO_2026-05-08.md`
10. `transfer/ws2-ed1-etabs21-context/CHECKLIST_AUDITORIA_MODELO_ED1.md`
11. `transfer/ws2-ed1-etabs21-context/PROMPT_EJECUCION_WS2_ED1_PRIMERO.md`

## 5. Primera tarea

Edificio 1 primero.

Crear copia limpia fechada de `HECRAS2\prog\Edif1\ED1_PARTE1_COMPLETA_TRABAJO.EDB`, re-verificar el estado base y completar Parte 1 de Edificio 1 por pasos incrementales. No abrir Edificio 2 mientras Edificio 1 este activo.

Reportar en:

```text
transfer/ws2-ed1-etabs21-context/reports/
```
