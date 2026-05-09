# Comandos WS2

## Carpeta correcta en WS2

No usar `C:\Users\Civil\Documents\taha` como ruta de trabajo para este caso.

La raiz real entregada por el usuario es:

```text
C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2
```

El repo/contexto debe quedar dentro de esa raiz, en:

```text
C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\codex_ws2_context
```

## Clonar o actualizar repo dentro de HECRAS2

```powershell
cd "C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2"
git clone https://github.com/kcortes765/taha.git codex_ws2_context
cd "C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\codex_ws2_context"
git fetch origin
git checkout codex/ws2-ed1-etabs21-context
```

Si el repo ya existe:

```powershell
cd "C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\codex_ws2_context"
git fetch origin
git checkout codex/ws2-ed1-etabs21-context
git pull --ff-only origin codex/ws2-ed1-etabs21-context
```

## Verificar una sola instancia ETABS

```powershell
Get-Process ETABS -ErrorAction SilentlyContinue
```

Si devuelve una instancia, no abrir otra. Identificar que modelo esta abierto antes de seguir.

No trabajar dos edificios en simultaneo. Edificio 1 primero, Edificio 2 despues.

## Si Git no esta disponible

Si `git` no existe en PATH, descargar el ZIP de la rama `codex/ws2-ed1-etabs21-context` desde GitHub y extraerlo dentro de:

```text
C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\codex_ws2_context
```

## Listar archivos Edificio 1 en HECRAS2

```powershell
Get-ChildItem -LiteralPath "C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2" -Recurse -File -Include *.EDB,*.ebk,*.LOG,*.OUT,*.txt,*.xlsx | Select-Object FullName,Length,LastWriteTime | Format-Table -AutoSize
```

## Buscar modelos ED1

```powershell
Get-ChildItem -LiteralPath "C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2" -Recurse -File | Where-Object { $_.Name -match 'ED1|Edif1|Edificio1|PARTE1' } | Select-Object FullName,Length,LastWriteTime | Format-Table -AutoSize
```

## Crear copia limpia Edificio 1

Ejemplo, ajustar timestamp:

```powershell
$root = "C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2"
$src = Join-Path $root "prog\Edif1\ED1_PARTE1_COMPLETA_TRABAJO.EDB"
$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupDir = Join-Path $root "prog\Edif1\backups"
$workDir = Join-Path $root "prog\Edif1\trabajo"
New-Item -ItemType Directory -Force -Path $backupDir,$workDir | Out-Null
Copy-Item -LiteralPath $src -Destination (Join-Path $backupDir "ED1_PARTE1_COMPLETA_TRABAJO_backup_$stamp.EDB") -Force
Copy-Item -LiteralPath $src -Destination (Join-Path $workDir "ED1_PARTE1_WORK_$stamp.EDB") -Force
```

## Crear reporte local

Nombre sugerido:

```text
C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\codex_ws2_context\transfer\ws2-ed1-etabs21-context\reports\WS2_ED1_PARTE1_EJECUCION_YYYYMMDD_HHMM.md
```
