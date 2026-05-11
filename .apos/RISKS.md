# RISKS

## R-20260508-ETABS21-MULTIINSTANCIA

- Estado: vivo.
- Severidad: critica operacional.
- Riesgo: abrir o usar mas de una instancia de ETABS 21 puede producir revoque/bloqueo de licencia en la WS UCN.
- Mitigacion obligatoria:
  - verificar `Get-Process ETABS -ErrorAction SilentlyContinue` antes de abrir ETABS o correr COM/API
  - usar una sola instancia
  - trabajar un solo edificio activo
  - no correr dos agentes/scripts simultaneos
  - no lanzar ETABS automaticamente desde scripts sin verificar instancia existente
- Evidencia/registro:
  - `ETABS21_REGLA_LICENCIA.md`
  - `transfer/ws2-ed1-etabs21-context/LICENCIA_ETABS21_REGLA_CRITICA.md`

## R-20260508-WS2-ESTADO-NO-TRAZADO

- Estado: mitigado parcialmente.
- Severidad: alta tecnica.
- Riesgo: el usuario reporto que en WS2 hubo un avance leve por UI posterior a WS1. Ya existe auditoria OAPI inicial, pero aun faltan resultados de ejecucion Parte 1.
- Mitigacion:
  - usar `reports/WS2_REPORTE_PARTE1_ED1_ED2_20260508_2116.md` como baseline
  - crear copia limpia fechada antes de modificar
  - devolver reporte de ejecucion Ed.1

## R-20260508-ED1-RELEASES-TORSION-MALINTERPRETADOS

- Estado: vivo.
- Severidad: alta tecnica.
- Riesgo: una IA/agente puede eliminar releases torsionales de Ed.1 por considerarlos error, aunque el usuario aclaro que fueron pedidos por el profesor.
- Mitigacion:
  - leer `WS2_DELTA_CANON_20260508_RELEASES_TORSION.md`
  - preservar torsion liberada salvo instruccion explicita contraria
  - verificar que no haya axial/corte liberados indebidamente

## R-20260508-ED1-ED2-PARALELO

- Estado: vivo.
- Severidad: critica operacional.
- Riesgo: trabajar Ed.1 y Ed.2 en paralelo puede mezclar modelos, scripts, reportes y abrir mas de una instancia ETABS.
- Mitigacion:
  - Ed.1 primero hasta cierre Parte 1
  - Ed.2 despues
  - registrar edificio activo en cada reporte
  - usar `PROTOCOLO_UN_EDIFICIO_UNA_INSTANCIA.md`

## R-20260508-ED1-MATRIZ-VARIANTES

- Estado: abierto.
- Severidad: media/alta tecnica.
- Riesgo: Edificio 1 quedo con la base dinamica rigida ejecutada, escalada por R* y Qmin, con resultados exportados y `Qmin` cumplido. Sin embargo, si la rubrica exige literalmente las seis variantes de Edificio 1 como entregables separados, falta materializar y exportar todas las variantes formales.
- Evidencia actual:
  - `HECRAS2\prog2\Edif1\reports\ED1_PARTE1_PROG2_run-adjust-export_20260508_2247.md`
  - `HECRAS2\prog2\Edif1\logs\ed1_run-adjust-export_20260508_2247.json`
- Mitigacion:
  - crear copias variantes desde la copia final Ed.1 y correrlas una a una en la misma instancia ETABS
  - no tocar releases torsionales pedidos por el profesor

## R-20260508-ED2-CR-NO-EXPUESTO

- Estado: aceptado con advertencia.
- Severidad: baja/media documental.
- Riesgo: la tabla CM/CR de ETABS entrega CR=(0,0), espurio para la planta. Usarlo como CR real induciria excentricidades falsas.
- Mitigacion aplicada:
  - conservar CM real desde tabla ETABS
  - marcar CR como placeholder explicito `etabs_cm_table_placeholder_cr_zero`
  - cerrar Ed.2 con `PASS` y warning documentado, no con dato inventado

## R-20260509-ETABS-MODAL-BLOQUEANTE

- Estado: mitigado con watchdog, mantener vivo.
- Severidad: critica operacional.
- Riesgo: ETABS puede abrir un dialogo modal durante `File.OpenFile`, recuperacion de resultados/masa ensamblada o `Analyze.RunAnalysis`; el proceso queda `Responding=True`, pero el script COM puede quedar bloqueado durante horas.
- Evidencia:
  - usuario observo el modal `Error in recovering joint assembled mass`;
  - la instancia antigua PID 23284 quedo abierta desde 2026-05-08 22:21 hasta la auditoria post-modal.
- Mitigacion aplicada:
  - cerrar la instancia vieja antes de abrir otra;
  - agregar `HECRAS2\prog2\_common\ws2_etabs_watchdog.py`;
  - vigilar `File.OpenFile` y `Analyze.RunAnalysis` desde proceso externo;
  - registrar JSON `*_watchdog.json` y fallar el script si aparece modal.
- Pendiente:
  - si reaparece el error de masa ensamblada, no declarar resultados cerrados; abrir desde copia limpia, borrar resultados con API oficial `Analyze.DeleteResults(..., All=True)` si procede, rerun y verificar `.LOG/.OUT`.

## R-20260509-ETABS-Y-TEMPORAL

- Estado: abierto bajo observacion.
- Severidad: media operacional.
- Riesgo: al cerrar ETABS despues de auditoria OAPI, la consola reporto `Cannot open file ... .Y_` para ED1 y ED2. No hubo modal ni error en `.LOG/.OUT`, pero puede indicar archivo temporal/resultados no recuperable.
- Mitigacion:
  - mantener este evento en reportes;
  - no confiar solo en `ret=0`; revisar `.LOG/.OUT`, watchdog y exportaciones;
  - si el mensaje pasa a modal o impide abrir modelos, regenerar desde copia limpia y borrar/rerun resultados.

## R-20260509-ED1-RERUN-NO-IDEMPOTENTE

- Estado: mitigado.
- Severidad: alta tecnica.
- Riesgo: rerun de ED1 sobre un modelo ya escalado puede mezclar resultados/estado anterior y producir amplificaciones Qmin absurdas.
- Evidencia:
  - corrida `ed1_run-adjust-export_20260509_0619` dejo `SEx/SEy ~18815 tonf`, aunque el Qmin requerido era `737.086 tonf`.
- Mitigacion aplicada:
  - copia afectada guardada en `HECRAS2\prog2\Edif1\models\quarantine_20260509_0630_bad_qmin_scale`;
  - modelo activo restaurado desde `.EDB` original limpio;
  - `ed1_part1_prog2.py` ahora llama `Analyze.DeleteResults("", True)` antes de cada `RunAnalysis`;
  - se agregaron limites de amplificacion y ratio final Qmin.
- Verificacion:
  - corrida limpia `ED1_PARTE1_PROG2_full_20260509_0630.md` vuelve a `SEx=740.771`, `SEy=740.771`, ratio `1.005`.

## R-20260509-ED1-METODO-A-PESADO

- Estado: mitigado con copias fechadas y watchdog.
- Severidad: media/alta operacional.
- Riesgo: metodo a crea cuatro fuentes de masa desplazadas, cuatro casos no lineales auxiliares, cuatro modales y cuatro espectrales; en semi-rigido la corrida toma varios minutos y puede ser sensible a errores modales.
- Mitigacion aplicada:
  - se ejecuto en copias `*_METHOD_A_20260509_0958.EDB`;
  - `Analyze.RunAnalysis ret=0` en rigido y semi-rigido;
  - watchdog sin eventos bloqueantes;
  - tablas exportadas confirman `MoveMass=Yes`, ratios `+/-0.05`, modales propios y `EccenRatio=0`.
- Pendiente:
  - para informe docente, incluir capturas/tablas de mass source y modal cases si se exige evidencia visual.

## R-20260509-ED2-CR-NO-EXPUESTO

- Estado: abierto documentado.
- Severidad: baja/media de presentacion.
- Riesgo: ETABS no expuso centro de rigidez real en el flujo programatico ED2; el verificador usa CM real y CR placeholder explicito.
- Mitigacion:
  - no inventar CR;
  - mantener warning visible en reportes y verificador;
  - si el profesor exige CR real, obtenerlo por procedimiento alternativo o captura UI.
