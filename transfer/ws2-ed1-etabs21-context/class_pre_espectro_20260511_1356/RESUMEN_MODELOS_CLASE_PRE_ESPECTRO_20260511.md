# Resumen modelos clase pre-espectro

Fecha: 2026-05-11.

Carpeta base:

`C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\CLASE_PRE_ESPECTRO_20260511_1356`

## Modelos generados

### Edificio 1

Modelo:

`C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\CLASE_PRE_ESPECTRO_20260511_1356\Edificio_1\models\ED1_CLASE_PRE_ESPECTRO_20260511.EDB`

Fuente:

`C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog\Edif1\ED1_PARTE1_COMPLETA_TRABAJO.EDB`

Quedó listo con:

- geometría existente del modelo base;
- apoyos de base empotrados;
- diafragma rígido `D1` asignado a las 300 losas;
- patrones `PP`, `TERP`, `TERT`, `SCP`, `SCT`;
- cargas de losa:
  - pisos tipo: `TERP` y `SCP`;
  - cubierta: `TERT` y `SCT`;
- fuente de masa con masa propia de elementos + `TERP + TERT + 0.25*SCP + 0.0*SCT`;
- caso modal `MODAL` con 80 modos.

No quedó aplicado:

- función de espectro `Espectro_NCh433_2026_Z3_C`;
- casos espectrales `SEx`, `SEy`, `SEx_b2`, `SEy_b2`;
- torsión accidental por espectro;
- combinaciones dinámicas `ED1_DYN_*`;
- ajuste por corte mínimo `Qmin`;
- análisis final espectral.

Implicancia para clase:

Desde este archivo corresponde seguir exactamente con la definición del espectro, creación de casos espectrales, escalamiento, torsión, combinaciones y análisis.

### Edificio 2

Modelo:

`C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\CLASE_PRE_ESPECTRO_20260511_1356\Edificio_2\models\ED2_CLASE_PRE_ESPECTRO_20260511.EDB`

Quedó listo con:

- modelo creado desde cero con grilla 6x6 y 5 pisos;
- materiales y secciones;
- columnas, vigas y losas;
- diafragma `D1`, auto mesh, apoyos y asignaciones;
- patrones y cargas gravitacionales;
- fuente de masa oficial del taller;
- modal auxiliar ejecutado para obtener períodos;
- resultados modales auxiliares en `Edificio_2\results`.

No quedó aplicado:

- fuerzas sísmicas estáticas `EX` y `EY`;
- torsión accidental `TEX` y `TEY`;
- combinaciones oficiales posteriores;
- análisis final con sismo estático;
- extracción final de resultados de Parte 1.

Implicancia para clase:

Edificio 2 no depende de un espectro como núcleo principal de Parte 1. El equivalente correcto de "antes del espectro" es "antes de aplicar el método estático", es decir antes de `EX/EY/TEX/TEY`. Desde este archivo corresponde seguir con el cálculo y aplicación de `C*I*P`, distribución por piso, torsión accidental, combinaciones, análisis y resultados.

## Sobre el error visto durante la corrida

El log registra un `UnicodeEncodeError` al imprimir símbolos como flechas o checks en consola Windows. No fue una falla del modelo ni de ETABS:

- el pipeline ED2 terminó con `Succeeded: 8 | Failed: 0`;
- se detuvo en el punto pedido: después de masa/modal y antes de `EX/EY/TEX/TEY`;
- ETABS quedó con una sola instancia y respondiendo.

## Regla para abrirlos

Antes de abrir ETABS:

```powershell
Get-Process ETABS -ErrorAction SilentlyContinue
```

Abrir un solo edificio a la vez. Si se desbloquea solo para mirar, cerrar sin guardar.
