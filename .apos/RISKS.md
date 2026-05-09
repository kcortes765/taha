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
