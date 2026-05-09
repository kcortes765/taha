# Regla critica de licencia ETABS 21

## Prohibicion operativa

No abrir ni mantener mas de una instancia de ETABS 21 al mismo tiempo.

No trabajar Edificio 1 y Edificio 2 en simultaneo. Siempre un edificio activo.

## Motivo

El usuario reporto que usar mas de una instancia de ETABS 21 puede producir revoque/bloqueo de licencia en la workstation de la UCN.

## Regla obligatoria

Antes de abrir ETABS 21 o ejecutar cualquier script COM/API:

1. Verificar si ya existe una instancia abierta de ETABS.
2. Si existe, usar esa instancia unica o cerrarla manualmente antes de abrir otra.
3. No lanzar ETABS desde scripts si ya esta abierto.
4. No correr dos agentes, dos scripts o dos procesos COM contra ETABS al mismo tiempo.
5. No dejar ETABS abierto en segundo plano despues de terminar una corrida.
6. Confirmar que modelo/edificio esta abierto antes de actuar.

## Comando de verificacion en PowerShell

```powershell
Get-Process ETABS -ErrorAction SilentlyContinue
```

Si el comando devuelve una instancia, no abrir otra.

## Estado del proyecto

Esta regla aplica especialmente al trabajo de Edificio 1 primero y Edificio 2 despues en ETABS 21, WS2, carpeta:

`C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2`
