# RISKS

## R-20260508-ETABS21-MULTIINSTANCIA

- Estado: vivo.
- Severidad: critica operacional.
- Riesgo: abrir o usar mas de una instancia de ETABS 21 puede producir revoque/bloqueo de licencia en la WS UCN.
- Mitigacion obligatoria:
  - verificar `Get-Process ETABS -ErrorAction SilentlyContinue` antes de abrir ETABS o correr COM/API
  - usar una sola instancia
  - no correr dos agentes/scripts simultaneos
  - no lanzar ETABS automaticamente desde scripts sin verificar instancia existente
- Evidencia/registro:
  - `ETABS21_REGLA_LICENCIA.md`
  - `transfer/ws2-ed1-etabs21-context/LICENCIA_ETABS21_REGLA_CRITICA.md`

## R-20260508-WS2-ESTADO-NO-TRAZADO

- Estado: vivo.
- Severidad: alta tecnica.
- Riesgo: el usuario reporta que en WS2 hubo un avance leve por UI posterior a WS1, pero el repo aun no contiene evidencia del estado real del `.EDB`.
- Mitigacion:
  - no continuar modelando hasta auditar el modelo activo
  - identificar ruta exacta del `.EDB`
  - devolver reporte WS2 con conteos, asignaciones, cargas, mesh, diafragmas y diferencias contra WS1
