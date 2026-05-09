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
2. `transfer/ws2-ed1-etabs21-context/APOS_X_SYNC_PROTOCOL.md`
3. `transfer/ws2-ed1-etabs21-context/HANDOFF_WS2_ED1.md`
4. `transfer/ws2-ed1-etabs21-context/FUENTES_PRIORITARIAS_WS2.md`
5. `transfer/ws2-ed1-etabs21-context/ENUNCIADO_CAMBIOS_2026-05-04.md`
6. `transfer/ws2-ed1-etabs21-context/CHECKLIST_AUDITORIA_MODELO_ED1.md`
7. `transfer/ws2-ed1-etabs21-context/PROMPT_PARA_CODEX_WS2.md`

## 5. Primera tarea

No modelar primero.

Auditar el `.EDB` activo de Edificio 1 dentro de `HECRAS2` y devolver reporte en:

```text
transfer/ws2-ed1-etabs21-context/reports/
```

