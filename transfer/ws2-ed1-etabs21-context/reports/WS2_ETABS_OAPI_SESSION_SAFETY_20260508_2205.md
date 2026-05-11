# WS2 - Seguridad de sesion ETABS OAPI

Fecha: 2026-05-08 22:05 America/Santiago  
Objetivo: reducir el riesgo de que una corrida API cierre ETABS, cierre la sesion/licencia o se adjunte a una instancia equivocada.

## Conclusion ejecutiva

No encontre una fuente oficial que diga literalmente que "abrir doble instancia por API cierra la sesion de ETABS". Lo que si queda confirmado por documentacion oficial CSI/ETABS es:

1. `ApplicationExit(FileSave)` cierra ETABS. Si un script se adjunta a una instancia abierta por el usuario y luego llama `ApplicationExit(False)`, el script puede cerrar esa sesion de ETABS.
2. `ApplicationStart()` inicia la aplicacion. Si ya hay ETABS abierto y el script crea otro objeto + `ApplicationStart`, puede abrir/consumir otra instancia/licencia.
3. En ETABS API historica, `GetObject()` se adjunta a la instancia activa o a la instancia registrada en ROT; si hay varias instancias, puede no ser la que se espera.
4. Desde ETABS v20.2.0 existe `cHelper.GetObjectProcess(typeName, pid)`, que permite adjuntarse a una instancia por PID. En ETABS 21 conviene usar este camino cuando haya cualquier ambiguedad.
5. ETABS 21.2.0 puede usar licencia Cloud/Network/Standalone. La documentacion de ETABS 21.2.0 indica que la licencia Cloud necesita comunicacion por puerto 443 para adquirir y mantener licencia, y que cada Activation Key tiene numero limitado de usuarios/seats. Una segunda instancia puede fallar o consumir otro seat.

Inferencia tecnica: el incidente previo pudo deberse a doble instancia/licencia, pero el riesgo mas directo de cierre por API es llamar `ApplicationExit` sobre una instancia que no fue creada exclusivamente por el script. El segundo riesgo importante es adjuntarse a la instancia equivocada y cerrarla, por usar `GetObject()` cuando existen varias.

## Fuentes oficiales usadas

Fuentes web oficiales CSI:

- CSI API ETABS 2015, "Attaching to a Manually Started Instance of ETABS": `https://docs.csiamerica.com/help-files/etabs-api-2015/html/3ceb8889-9028-4de3-9c87-69a12055ade7.htm`
- CSI API ETABS 2016, `cOAPI.ApplicationStart`: `https://docs.csiamerica.com/help-files/etabs-api-2016/html/da3c2062-cb41-dc93-8df2-64725899285e.htm`
- CSI API ETABS 2015, `cOAPI.ApplicationExit`: `https://docs.csiamerica.com/help-files/etabs-api-2015/html/460653c6-7b02-f086-c201-2c7e64c7dc5f.htm`
- CSI API ETABS 2016, `cHelper.GetObject`: `https://docs.csiamerica.com/help-files/etabs-api-2016/html/744b0c41-dca8-c45c-2a86-d7a5fef0c2fc.htm`
- CSI ETABS v20.2.0 Release Notes, API enhancement `cHelper.GetObjectProcess`: `https://www.csiamerica.com/software/ETABS/20/ReleaseNotesETABSv2020.pdf`
- CSI ETABS v21.2.0 ReadMe, licensing and seats: `https://www.csiamerica.com/software/ETABS/21/ReadMeETABSv2120.pdf`

Fuente local oficial instalada:

- `C:\Program Files\Computers and Structures\ETABS 21\CSI API ETABS v1.chm`
- `C:\Program Files\Computers and Structures\ETABS 21\ETABS.exe`
- DLL/API local: `C:\Program Files\Computers and Structures\ETABS 21\ETABSv1.dll`

## Hallazgos oficiales relevantes

### Adjuntar a instancia ya abierta

La ayuda CSI indica que, si ETABS ya esta iniciado manualmente, no se debe crear e iniciar otra instancia. En su lugar se debe adjuntar al objeto ETABS existente. La misma pagina indica que, al adjuntarse a una instancia ya iniciada, no hace falta llamar `ApplicationStart()`.

Implicancia WS2:

- si `Get-Process ETABS` devuelve una instancia, el script debe adjuntarse;
- no debe llamar `ApplicationStart()` en ese caso;
- debe registrar PID y ruta/modelo antes de modificar.

### Multiples instancias

La ayuda CSI historica advierte que si se inician multiples instancias de ETABS manualmente, un cliente API puede adjuntarse solo a la primera instancia iniciada.

ETABS v20.2.0 agrega una mejora oficial: `cHelper.GetObjectProcess()` permite adjuntarse a cualquier instancia de ETABS dada por su process ID. Tambien se agrego en el menu Tools el comando "Set as active instance for API".

Implicancia WS2:

- con ETABS 21, si existe mas de un proceso ETABS, no usar `GetObject()` a ciegas;
- usar `GetObjectProcess("CSI.ETABS.API.ETABSObject", pid)` si se decide explicitamente un PID;
- si no se puede confirmar el PID/modelo correcto, detenerse.

### ApplicationStart

La documentacion oficial describe `ApplicationStart()` como la funcion que inicia la aplicacion y devuelve cero si inicia correctamente.

Implicancia WS2:

- solo usar `ApplicationStart()` si no hay ETABS abierto y el script esta autorizado a crear la unica instancia;
- marcar en codigo `started_by_script = True`;
- si ya hay ETABS abierto, `ApplicationStart()` es indicio de flujo inseguro.

### ApplicationExit

La documentacion oficial describe `ApplicationExit(FileSave)` como el metodo que sale/cierra la aplicacion. Si `FileSave` es `True`, guarda el modelo actual con su nombre antes de cerrar. Tambien indica limpiar referencias `cSapModel` despues.

Implicancia WS2:

- nunca llamar `ApplicationExit()` por defecto en scripts que se adjuntan a una instancia existente;
- nunca poner `ApplicationExit()` en `finally` sin chequear si el script creo esa instancia;
- `ApplicationExit(False)` tambien cierra ETABS, aunque no guarde;
- `ApplicationExit(True)` puede guardar cambios no deseados sobre el modelo actual, por lo que esta prohibido salvo bloque final explicitamente validado sobre copia de trabajo.

### Licencia ETABS 21.2.0

El ReadMe oficial de ETABS 21.2.0 indica:

- Cloud license necesita comunicacion con servidor por puerto 443 para adquirir y mantener licencia.
- Cada Activation Key tiene numero limitado de usuarios/seats.
- Cuando se alcanza el limite, no pueden correr usuarios adicionales hasta que alguien cierre ETABS.
- Cerrar ETABS libera licencia para otro usuario/maquina.
- Network license requiere un License Manager accesible.

Implicancia WS2:

- una segunda instancia puede no cerrar la primera, pero si puede competir por licencia o fallar al iniciar;
- una perdida de internet/puerto 443 puede afectar mantener licencia Cloud;
- correr ETABS/API bajo otro usuario/contexto puede cambiar configuracion/licencia local;
- antes de corrida larga, evitar suspension del equipo y cortes de red.

## Protocolo anti-cierre para WS2

### Regla 1: decidir modo de conexion

Antes de cualquier OAPI:

```powershell
Get-Process ETABS -ErrorAction SilentlyContinue | Select-Object Id,ProcessName,MainWindowTitle,StartTime
```

Casos:

- 0 procesos: el script puede iniciar una unica instancia si el bloque lo requiere.
- 1 proceso: el script debe adjuntarse a esa instancia; no iniciar otra.
- 2+ procesos: bloqueo duro salvo PID explicitamente confirmado y documentado.

### Regla 2: ownership de instancia

Todo helper OAPI debe manejar una bandera:

```text
started_by_script = True/False
```

Solo si `started_by_script = True` y el bloque lo pide, se permite `ApplicationExit(False)` al final. Si el script se adjunto a una instancia existente, esta prohibido llamar `ApplicationExit`.

### Regla 3: adjuntar por PID cuando haya ambiguedad

Con ETABS 21, preferir:

```text
helper.GetObjectProcess("CSI.ETABS.API.ETABSObject", pid)
```

cuando haya mas de una instancia o se necesite asegurar cual instancia se controla.

Si se usa `GetObject("CSI.ETABS.API.ETABSObject")`, debe ser solo cuando:

- hay exactamente una instancia ETABS;
- el modelo abierto fue verificado;
- el log registra PID y ruta del `.EDB`.

### Regla 4: no cerrar en `finally`

Patron prohibido:

```python
finally:
    etabs.ApplicationExit(False)
```

Patron permitido:

```python
finally:
    if started_by_script and close_etabs_requested:
        etabs.ApplicationExit(False)
    sap_model = None
    etabs = None
```

### Regla 5: verificar modelo antes de tocar

Despues de adjuntar:

- obtener version/build;
- obtener ruta del modelo actual si es posible;
- comparar con la copia de trabajo esperada;
- si el modelo abierto no es el esperado, detenerse.

### Regla 6: guardar solo sobre copia de trabajo

Nunca usar `ApplicationExit(True)` como mecanismo de guardado. Guardar con metodo explicito sobre copia limpia, verificar ruta, y luego no cerrar ETABS salvo que el script la haya iniciado y la politica del bloque lo permita.

### Regla 7: separar cierre COM de cierre ETABS

Soltar referencias COM no debe equivaler a cerrar ETABS. El cierre de ETABS solo ocurre por `ApplicationExit` o cierre manual. En Python/comtypes, limpiar variables y recolectar COM esta bien; llamar `ApplicationExit` no.

## Plantilla segura recomendada para scripts Python

```python
def connect_etabs(expected_model=None, allow_start=False, target_pid=None):
    started_by_script = False
    procs = list_etabs_processes()

    if len(procs) == 0:
        if not allow_start:
            raise RuntimeError("No hay ETABS abierto y allow_start=False")
        etabs = helper.CreateObject(r"C:\Program Files\Computers and Structures\ETABS 21\ETABS.exe")
        ret = etabs.ApplicationStart()
        if ret != 0:
            raise RuntimeError(f"ApplicationStart fallo ret={ret}")
        started_by_script = True

    elif len(procs) == 1:
        pid = procs[0]["pid"]
        etabs = helper.GetObjectProcess("CSI.ETABS.API.ETABSObject", pid)

    else:
        if target_pid is None:
            raise RuntimeError("Multiples ETABS abiertos: se requiere target_pid confirmado")
        etabs = helper.GetObjectProcess("CSI.ETABS.API.ETABSObject", target_pid)

    sap = etabs.SapModel
    verify_model(sap, expected_model)
    return etabs, sap, started_by_script

def safe_disconnect(etabs, sap, started_by_script, close_requested=False):
    sap = None
    if started_by_script and close_requested:
        etabs.ApplicationExit(False)
    etabs = None
```

## Decision operativa para el modo autonomo

WS2 esta autorizada a trabajar sola solo si respeta este protocolo:

- una instancia;
- un edificio;
- un script OAPI a la vez;
- sin `ApplicationExit` salvo instancia creada por el script y cierre solicitado;
- sin `GetObject()` ambiguo si hay multiples instancias;
- documentacion oficial consultada ante errores API;
- backup y copia limpia antes de modificar.

Si aparece cualquier escenario de licencia/sesion ambiguo, se considera bloqueo duro y se reporta antes de continuar.
