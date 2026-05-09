# Protocolo critico: un edificio, una instancia ETABS 21

Fecha: 2026-05-08

## Regla dura

No trabajar dos edificios en simultaneo.

No abrir mas de una instancia de ETABS 21.

Antes de cualquier accion OAPI/COM o antes de abrir ETABS por UI:

```powershell
Get-Process ETABS -ErrorAction SilentlyContinue
```

Si aparece una instancia:

- no abrir otra;
- no correr otro script;
- identificar que modelo esta abierto;
- decidir si se sigue con esa unica instancia o se cierra manualmente antes de continuar.

## Secuencia obligatoria

1. Edificio 1 primero.
2. Edificio 1 debe quedar con Parte 1 completa, analizada, exportada y reportada.
3. Recien despues se pasa a Edificio 2.
4. Edificio 2 se trabaja desde copia limpia propia, nunca mezclado con Edificio 1.

## Copias limpias

Antes de modificar cualquier `.EDB`, crear copia limpia fechada.

Formato sugerido:

```text
HECRAS2\prog\Edif1\trabajo\ED1_PARTE1_WORK_YYYYMMDD_HHMM.EDB
HECRAS2\Edif2\trabajo\ED2_PARTE1_WORK_YYYYMMDD_HHMM.EDB
```

Ademas guardar backup del original sin tocar:

```text
HECRAS2\prog\Edif1\backups\...
HECRAS2\Edif2\backups\...
```

## Registro obligatorio

Cada corrida debe dejar reporte con:

- fecha y hora;
- ruta exacta del `.EDB`;
- edificio activo;
- confirmacion de una sola instancia ETABS;
- accion ejecutada;
- cambios aplicados;
- validaciones OAPI/tablas;
- resultados exportados;
- errores o bloqueos.

## Prohibido

- Abrir Edificio 1 y Edificio 2 a la vez.
- Lanzar dos scripts COM/OAPI simultaneos.
- Corregir releases torsionales de Edificio 1 por reflejo.
- Usar el modelo alternativo de Edificio 1 solo porque no tiene releases torsionales.
- Guardar cambios sobre el original sin backup y copia de trabajo.

