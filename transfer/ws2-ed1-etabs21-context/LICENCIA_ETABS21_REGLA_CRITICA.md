# LICENCIA ETABS 21 - Regla critica

No se puede usar mas de una instancia de ETABS 21.

## Regla

Siempre una sola instancia de ETABS 21.

## Por que

El usuario reporto que abrir/usar mas de una instancia puede producir revoque o bloqueo de licencia en las workstation UCN.

## Antes de hacer cualquier cosa

Ejecutar:

```powershell
Get-Process ETABS -ErrorAction SilentlyContinue
```

Si aparece una instancia:

- no abrir otra;
- no correr un script que cree otra instancia;
- usar esa instancia unica o cerrarla manualmente;
- esperar a que termine cualquier otro agente/proceso.

## Prohibido

- Dos ventanas de ETABS 21 abiertas.
- Dos scripts COM/API simultaneos.
- Un agente usando UI y otro agente usando API al mismo tiempo.
- `CreateObject` automatico sin verificar si ya hay ETABS abierto.
- Dejar ETABS abierto despues de terminar y que otro agente abra otro.

## Permitido

- Una instancia unica de ETABS 21 controlada manualmente.
- Un script a la vez, conectado a esa instancia unica.
- Auditoria primero, modificacion despues.

