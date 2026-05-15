# GOAL_ED1_PROG4_PARTE1_DINAMICO_ESPECTRAL_OFICIAL_20260514_2332

Fecha: 2026-05-14 23:32 America/Santiago

## Objetivo largo

Cerrar Edificio 1 en `prog4` para Parte 1 del taller ADSE 1S-2026 con un flujo verificable, reproducible y trazable, usando solamente fuentes de verdad del curso para criterios ingenieriles y documentación oficial CSI/ETABS solo para operación OAPI/API.

El resultado final debe quedar listo para revisión académica y defensa técnica: modelo ETABS, scripts incrementales, resultados exportados, Excel/tablas, auditoría, guía UI y paquete de transferencia.

## Regla de fuente de verdad

Las decisiones de ingeniería se aceptan solo si quedan asociadas a una de estas fuentes:

- Enunciado actualizado del taller.
- Apuntes del curso 2026-05-08.
- Material Apoyo Taller 2026.
- NCh433:2026 usada por el curso.
- NCh3171 y NCh1537 cuando el curso las use para combinaciones/cargas.
- Transcripciones de clase, incluyendo la transcripción adicional `taller sismo 8_transcripcion.txt`.

No se aceptan como autoridad final:

- MD destilados antiguos.
- Guías genéricas de internet.
- Suposiciones por memoria.
- Decisiones tomadas porque "normalmente" se hace así.

La documentación oficial ETABS/CSI se puede consultar para llamadas OAPI, errores, tablas, comportamiento de sesión, guardado, análisis y extracción de resultados, pero no para reemplazar criterios del curso.

## Punto de partida vigente

Checkpoint base para Edificio 1:

`C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog4\Edificio_1\01_modelos\ED1_PROG4_CIERRE_MODAL_20260512_2306.EDB`

Estado conocido:

- 20 pisos.
- Alturas: Story1 = 3.40 m; Story2 a Story20 = 2.60 m; altura total = 52.80 m.
- Geometría recuperada desde el modelo real de `prog2`, no deducida desde cero.
- 880 áreas, 320 marcos, 1370 puntos.
- Losas `Losa15G30`, muros `MHA20G30`/`MHA30G30`, vigas `VI20/60G30`.
- Modificadores de losas y muros auditados en 1.0.
- Viga `VI20/60G30` con torsión en modificador 0.
- Mass source con TERP=1.0, TERT=1.0, SCP=0.25, SCT=0.0.
- Modal corrido y exportado.

Pendiente real:

- No tratar ED1 como cerrado Parte 1.
- Cerrar metodología dinámica/modal espectral según fuentes del curso.
- Resolver y documentar los casos exigidos, torsión, diafragma, espectro, escalamiento, combinaciones/verificaciones, resultados y auditoría final.

## Reglas de sesión ETABS

Antes de abrir ETABS o usar OAPI:

```powershell
Get-Process ETABS -ErrorAction SilentlyContinue
```

Si ETABS está abierto:

- no abrir otra instancia;
- usar esa instancia solo si está en estado sano;
- si aparece diálogo `miOpen`, `Warning`, `Error`, `array`, recuperación de resultados o inicialización inesperada, detener el flujo y registrar el bloqueo;
- cerrar solo con confirmación explícita si la instancia parece del usuario.

No correr dos scripts contra ETABS al mismo tiempo.

## Plan de ejecución

### Fase 0 - Memoria, Git y APOS

1. Registrar este objetivo en APOS como goal activo de Edificio 1.
2. Verificar que `codex_ws2_context` esté en rama `codex/ws2-ed1-etabs21-context`.
3. Registrar cambios materiales en APOS append-only: `JOURNAL.md`, `DECISIONS.md`, `SOURCES.md` y `RESEARCH_LOG.md` cuando corresponda.
4. Crear reportes delta en `transfer/ws2-ed1-etabs21-context/reports`.
5. No subir a Git hasta tener paquete coherente o checkpoint explícito.

### Fase 1 - Matriz de fuentes

1. Inventariar las fuentes oficiales disponibles en `prog4/00_fuentes_de_verdad`.
2. Para cada decisión ED1, crear una matriz `decisión -> fuente -> página/minuto -> evidencia`.
3. Si el PDF tiene texto como imagen, generar evidencia visual/OCR puntual.
4. Separar explícitamente:
   - lo que el enunciado exige;
   - lo que los apuntes enseñan;
   - lo que el material de apoyo operacionaliza;
   - lo que las transcripciones aclaran.

### Fase 2 - Congelamiento del modelo base

1. Crear copia fechada del checkpoint base antes de modificar.
2. Registrar hash/tamaño/fecha del `.EDB`, `.LOG`, `.OUT`, `.$et` si existen.
3. Crear carpeta de trabajo para ED1 final:
   - `models`
   - `scripts`
   - `exports`
   - `audits`
   - `excel`
   - `figures`
   - `package`
4. No modificar el checkpoint base original.

### Fase 3 - Auditoría profunda antes de modelar

Verificar por OAPI/UI/exportación:

- historias y alturas;
- grillas principales y auxiliares;
- materiales y secciones;
- muros por dirección, espesor y nivel;
- losas y diafragma;
- vigas invertidas;
- offsets/cachos rígidos;
- releases de vigas, incluyendo la excepción de torsión pedida por el profesor;
- apoyos de base;
- modificadores;
- automesh;
- cargas gravitacionales;
- mass source;
- modal y masa participante;
- CM/CR si corresponde y si ETABS lo calcula de forma válida.

Cada ítem debe quedar como `OK`, `pendiente`, `no aplica` o `bloqueado`, con evidencia.

### Fase 4 - Definición oficial de metodología ED1

Antes de crear casos:

1. Confirmar desde fuentes oficiales si ED1 exige análisis modal espectral.
2. Confirmar si se requieren 6 casos: diafragma rígido/semirrígido por métodos de torsión A, B1 y B2.
3. Confirmar cómo se define espectro, amortiguamiento, combinatoria modal, dirección, excentricidad accidental y escalamiento.
4. Confirmar combinaciones y verificaciones de desplazamiento/drift desde apuntes/material.
5. Registrar toda ambigüedad como pregunta abierta antes de decidir.

### Fase 5 - Implementación incremental

Crear scripts pequeños y reversibles:

1. Script de inspección base sin modificar.
2. Script de copia y saneamiento controlado.
3. Script de cargas/mass source si falta corregir.
4. Script de espectro y casos modal/espectrales.
5. Script de torsión accidental y variantes.
6. Script de combinaciones/verificaciones.
7. Script de análisis por caso.
8. Script de exportación y auditoría.

Cada script debe:

- chequear instancia ETABS antes de iniciar;
- rechazar segunda instancia;
- registrar retornos OAPI;
- detectar diálogos/bloqueos conocidos;
- guardar logs;
- no guardar sobre el modelo base sin backup.

### Fase 6 - Batería de pruebas

La meta no es repetir análisis sin valor, sino acumular pruebas verificables. Se esperan cientos de checks por objetos, pisos, casos y tablas; miles si el tamaño del modelo lo justifica.

Familias de pruebas:

- Preflight: proceso ETABS, versión, ruta, disco, permisos, backup.
- Invariantes del modelo: conteos, historias, grillas, secciones, materiales, apoyos.
- Asignaciones: diafragmas, cargas, mass source, releases, offsets, modificadores, mesh.
- Fuentes: cada criterio con referencia verificable.
- Modal: períodos, masa participante, modos dominantes, acumulados, torsión/acoplamiento.
- Espectro: función, unidades, parámetros, archivo si aplica, casos, direcciones.
- Resultados: base reactions, story forces, story drifts, max/avg drift, CM/CR, escalamiento.
- Consistencia matemática: sumas, signos, unidades, orden de magnitud, comparaciones independientes.
- Comparación entre casos: rígido vs semirrígido, torsión A/B1/B2.
- Robustez ETABS: reabrir copia, reanalizar, exportar y comparar checksums/tablas cuando sea seguro.

### Fase 7 - Validación conceptual e ingenieril

Contrastar:

- comportamiento esperado de edificio irregular de muros;
- acoplamiento modal;
- relevancia de torsión;
- diferencia rígido/semirrígido;
- consistencia de drift;
- corte basal modal/espectral y escalamiento si el curso lo exige;
- resultados esperados por transcripciones/apuntes.

No declarar "cumple" sin tabla y criterio.

### Fase 8 - Entregables

Crear:

- modelo final ED1 `.EDB`;
- backups y checkpoints;
- CSV/JSON de resultados;
- Excel de control si aporta;
- reporte de auditoría final;
- guía UI final basada solo en fuentes de verdad;
- paquete de transferencia;
- delta APOS;
- commit Git con todo lo versionable.

### Fase 9 - Cierre y transferencia

1. Verificar `git status`.
2. Empaquetar archivos pesados fuera de Git si corresponde.
3. Subir a Git solo lo versionable y reportes/manifest.
4. Dejar instrucciones claras para laptop personal.
5. Cerrar ETABS si fue abierto por scripts y no dejar instancia huérfana.

## Criterio de éxito

El trabajo queda aceptable solo si existe:

- modelo final reproducible;
- matriz fuente/decisión;
- auditoría completa;
- resultados exportados;
- comparación técnica entre casos;
- registro APOS;
- paquete transferible;
- indicación clara de lo que es oficial, auxiliar, histórico o pendiente.

