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

Si devuelve una instancia, no abrir otra.

## Listar archivos Edificio 1 en HECRAS2

```powershell
Get-ChildItem -LiteralPath "C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2" -Recurse -File -Include *.EDB,*.ebk,*.LOG,*.OUT,*.txt,*.xlsx | Select-Object FullName,Length,LastWriteTime | Format-Table -AutoSize
```

## Buscar modelos ED1

```powershell
Get-ChildItem -LiteralPath "C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2" -Recurse -File | Where-Object { $_.Name -match 'ED1|Edif1|Edificio1|PARTE1' } | Select-Object FullName,Length,LastWriteTime | Format-Table -AutoSize
```

## Crear reporte local

Nombre sugerido:

```text
C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\codex_ws2_context\transfer\ws2-ed1-etabs21-context\reports\WS2_REPORTE_MODELO_ED1.md
```
