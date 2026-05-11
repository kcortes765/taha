# Prompt de ejecucion para IA WS2 - Edificio 1 primero

Estas en WS2, proyecto ADSE UCN 1S-2026, ETABS 21. Tu objetivo es dejar completa la Parte 1 programatica/controlada de Edificio 1 y despues asegurar Edificio 2. No trabajes ambos edificios en paralelo.

El usuario quiere dejarte trabajando por horas sin loop humano constante. Opera en MODO GOD: diagnostica solo como paso cero, investiga documentacion/norma/apuntes antes de cada decision relevante, adapta codigo, ejecuta por bloques, verifica, corrige tus propios errores y continua hasta cerrar Edificio 1 Parte 1 y luego Edificio 2 Parte 1. Solo detente ante bloqueo duro de licencia, modelo corrupto, edificio equivocado o decision tecnica/normativa imposible de resolver con las fuentes.

## Regla critica de licencia

No abras mas de una instancia de ETABS 21. No corras dos scripts COM/OAPI en paralelo. No abras Edificio 1 y Edificio 2 al mismo tiempo.

Antes de abrir ETABS o ejecutar OAPI:

```powershell
Get-Process ETABS -ErrorAction SilentlyContinue
```

Si aparece una instancia, usa solo esa instancia o detente y reporta. No abras otra.

Si el script se adjunta a una instancia existente, no debe llamar `ApplicationExit`. Solo puede cerrar ETABS por API si el script creo esa instancia y el cierre fue solicitado explicitamente. Si hay mas de una instancia, no usar `GetObject()` a ciegas: usar PID con `GetObjectProcess` o detenerse.

## Ruta real

Raiz:

```text
C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2
```

Repo/contexto:

```text
C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\codex_ws2_context
```

No uses `C:\Users\Civil\Documents\taha` para este flujo.

## Lee primero

1. `transfer/ws2-ed1-etabs21-context/PROTOCOLO_UN_EDIFICIO_UNA_INSTANCIA.md`
2. `transfer/ws2-ed1-etabs21-context/LICENCIA_ETABS21_REGLA_CRITICA.md`
3. `transfer/ws2-ed1-etabs21-context/MODO_GOD_WS2.md`
4. `transfer/ws2-ed1-etabs21-context/MODO_GOD_DOCUMENTACION_WS2.md`
5. `transfer/ws2-ed1-etabs21-context/MODO_AUTONOMO_WS2_HORAS.md`
6. `transfer/ws2-ed1-etabs21-context/HANDOFF_WS2_ED1.md`
7. `transfer/ws2-ed1-etabs21-context/CODIGO_WS2_MANIFEST.md`
8. `transfer/ws2-ed1-etabs21-context/WORKBENCH_CODIGO_WS2.md`
9. `transfer/ws2-ed1-etabs21-context/PARTE1_ED1_ED2_PROGRAMATICO_2026-05-08.md`
10. `transfer/ws2-ed1-etabs21-context/CHECKLIST_AUDITORIA_MODELO_ED1.md`
11. `transfer/ws2-ed1-etabs21-context/files/01_Enunciado_Taller_actualizado_2026-05-04.pdf`
12. `transfer/ws2-ed1-etabs21-context/files/00_Apuntes_del_Curso_2026-05-08_actualizado.pdf`
13. `transfer/ws2-ed1-etabs21-context/files/02_Material_Apoyo_Taller_2026.pdf`
14. `transfer/ws2-ed1-etabs21-context/files/05_NCh433_2026_para_Curso.pdf`
15. `transfer/ws2-ed1-etabs21-context/code/ed1_taller_etabs_legacy/`
16. `transfer/ws2-ed1-etabs21-context/code/ed2_pipeline_active/`

## Como debes usar el codigo

El codigo incluido es base de trabajo, no pipeline final congelado.

Debes revisarlo, aprovechar funciones/patrones OAPI y adaptarlo al estado real de WS2. Si el codigo historico no calza con el `.EDB` actual, crea scripts nuevos incrementales en una carpeta de workbench local y deja registro.

Siempre que uses una llamada OAPI sensible o aparezca un error ETABS/COM/API, investiga primero documentacion oficial CSI/ETABS o ayuda local instalada de ETABS 21. No resuelvas errores solo por intuicion ni solo copiando codigo historico. Registra en el log la fuente oficial consultada, la firma/metodo confirmado y la decision aplicada.

No te quedes solo en diagnostico: diagnostica primero por seguridad, luego modifica por bloques verificables hasta completar Edificio 1 Parte 1.

## Estado confirmado que debes respetar

Edificio 1 activo probable:

```text
C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog\Edif1\ED1_PARTE1_COMPLETA_TRABAJO.EDB
```

Auditoria previa reporto:

- ETABS 21.2.0 build 21.2.0.3353.
- 20 stories.
- Alturas: piso 1 = 3.4 m; 19 pisos de 2.6 m; total 52.8 m.
- 41 grillas: 33 X + 8 Y.
- 1350 puntos, 320 frames, 880 areas.
- Muros: `MHA30G30` = 260 areas; `MHA20G30` = 320 areas.
- Losas: `Losa15G30` = 300 areas.
- Vigas: 320 `VI20/60G30`.
- Vigas invertidas: 320/320 con `Cardinal Point = 2 - Bottom Center`.
- `Do not transform frame stiffness for offsets from centroid`: confirmado.
- Offsets vigas: Auto, `RigidFact = 0.75`.
- Apoyos base: 50 empotrados completos.
- Modificadores losa `Losa15G30`: `m11/m22/m12 = 0.25`.
- Mesh/auto mesh presente.

Importante: los releases torsionales de Edificio 1 fueron pedidos por el profesor. No los elimines. El patron reportado fue:

- `TI, M2I, M3I`: 180 frames.
- `TJ, M2J, M3J`: 100 frames.
- `TI, M2I, M3I, M2J, M3J`: 40 frames.
- Sin release: 0 frames.

Esto debe validarse y documentarse, no corregirse como error.

## Lo que falta en Edificio 1

Completar primero Edificio 1:

1. Crear backup y copia limpia fechada desde el `.EDB` activo.
2. Crear/adaptar scripts incrementales para el `.EDB` real de WS2.
3. Re-verificar estado base por OAPI sin guardar.
4. Asignar diafragma `D1` a areas segun criterio de caso rigido.
5. Crear/normalizar patrones `PP`, `SCP`, `SCT`, `TERP`, `TERT`.
6. Aplicar cargas por losa/techo segun enunciado actualizado y apuntes.
7. Definir mass source: `PP + TERP + TERT + fraccion SCP/SCT` segun curso/enunciado, evitando duplicar peso propio.
8. Crear modal y espectral con base NCh433:2026 del curso.
9. Implementar torsion accidental / matriz de casos de Edificio 1 segun enunciado y Material Apoyo Taller.
10. Crear combinaciones requeridas.
11. Correr analisis solo despues de validaciones.
12. Exportar tablas ETABS exactas: peso sismico, CM/CR si aplica, periodos, participacion modal, corte basal, story forces, drifts, max/avg, base reactions, demandas relevantes de muros.
13. Guardar reporte con rutas, tablas, errores, resultados y scripts modificados.

## Despues de Edificio 1

Solo cuando Edificio 1 Parte 1 este cerrado, pasar a Edificio 2.

Edificio 2 activo probable:

```text
C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\Edif2\Edificio2_Estatico con carga sismica.EDB
```

Antes de tocarlo:

- crear backup y copia limpia fechada;
- verificar 5 stories, grillas, 480 frames, 130 areas;
- revisar por que hay 130 losas si canon nominal sugiere 125 panos;
- revisar contenido numerico de `TEX/TEY/SDX/SDY`;
- revisar combos `Combo 1` a `Combo 19`;
- no heredar automaticamente matriz de 6 casos de Edificio 1.

## Output obligatorio

Genera reportes en:

```text
transfer/ws2-ed1-etabs21-context/reports/
```

Nombres sugeridos:

```text
WS2_ED1_PARTE1_EJECUCION_YYYYMMDD_HHMM.md
WS2_ED2_AUDITORIA_PREVIA_YYYYMMDD_HHMM.md
WS2_APOS_DELTA_YYYYMMDD_HHMM.md
```

Cada reporte debe distinguir:

- hechos verificados;
- cambios aplicados;
- tablas exportadas;
- dudas o bloqueos;
- siguiente accion segura.
