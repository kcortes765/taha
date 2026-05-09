# Comandos WS2

## Clonar o actualizar repo

```powershell
cd C:\Users\Civil\Documents
git clone https://github.com/kcortes765/taha.git taha
cd taha
git fetch origin
git checkout codex/ws2-ed1-etabs21-context
```

Si el repo ya existe:

```powershell
cd C:\Users\Civil\Documents\taha
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
C:\Users\Civil\Documents\taha\transfer\ws2-ed1-etabs21-context\REPORTE_WS2_MODELO_ED1.md
```

