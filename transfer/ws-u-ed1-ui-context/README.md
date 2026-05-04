# WS UCN - Edificio 1 UI/API Context

Paquete de transferencia para trabajar el Edificio 1 en la workstation de la UCN.

Objetivo inmediato:

- usar la WS como maquina de ETABS 21/UI;
- mantener este repo como fuente de instrucciones, guias, normas y codigo;
- no versionar el modelo `.EDB` vivo salvo decision explicita posterior;
- usar la carpeta `files/` como contexto cerrado para lectura, revision y asistencia.

## Estado operativo

- El modelo UI vive en la WS.
- En este repo se consolida el contexto tecnico, la guia UI y la trazabilidad APOS.
- Carpeta WS correcta:
  - `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS\prog\Edif1`
- Modelo activo al retomar:
  - `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS\prog\Edif1\ED1_PARTE1_COMPLETA_TRABAJO.EDB`
- La planta tipo ya fue trabajada manualmente en ETABS: grilla, muros, vigas y losas.
- Segun reporte externo, el modelo original ya fue corregido por API COM antes del bloqueo de licencia.
- Las vigas invertidas deben verificarse por asignacion, no solo por apariencia 3D:
  `Assign > Frame > Insertion Point... > Cardinal Point = 2 - Bottom Center`.
- La casilla `Do not transform frame stiffness for offsets from centroid` debe quedar marcada, segun el material de Lafontaine/profesor.
- Pendiente vivo:
  - cargas `PP/SCP/SCT/TERP/TERT`;
  - fuente de masa;
  - diafragmas;
  - modal/espectral;
  - torsion accidental;
  - analisis y extraccion de tablas.

## Siguiente paso ETABS

Cuando vuelva la licencia ETABS 21:

1. Abrir solo `ED1_PARTE1_COMPLETA_TRABAJO.EDB`.
2. Re-verificar vigas invertidas, offsets, releases, apoyos y modificadores de losa.
3. Asignar diafragma rigido.
4. Crear patrones y cargas.
5. Definir fuente de masa.
6. Crear modal/espectral.
7. Resolver torsion accidental / 6 casos.
8. Exportar tablas de Parte 1.

## Orden de lectura recomendado

1. `files/13_GUIA_ED1_ETABS_v21.md`
2. `files/01_Enunciado_Taller.pdf`
3. `files/02_Material_Apoyo_Taller_2026.pdf`
4. `files/03_Paso_a_Paso_ETABS_Lafontaine.pdf`
5. `files/05_NCh433_2026_para_Curso.pdf`
6. `files/14_ESTADO_NORMATIVO_CURSO_2026.md`
7. `files/18_validacion_cruzada.md`

## Uso correcto

Usar este paquete para:

- seguir la guia UI en ETABS 21;
- resolver dudas de menu/criterio;
- contrastar con enunciado y material del profesor;
- preparar futuras corridas API o extraccion de resultados;
- dejar evidencia de decisiones.

No usar este paquete para:

- reemplazar la verificacion visual del modelo abierto en ETABS;
- inferir dimensiones desde capturas si contradicen el enunciado;
- mezclar la base normativa historica `NCh433 + DS61` con la base vigente `NCh433:2026` sin indicarlo.
