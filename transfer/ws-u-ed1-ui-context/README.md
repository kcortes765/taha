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
- La planta tipo ya fue trabajada manualmente en ETABS: grilla, muros, vigas y losas.
- Las vigas invertidas deben verificarse por asignacion, no solo por apariencia 3D:
  `Assign > Frame > Insertion Point... > Cardinal Point = 2 - Bottom Center`.
- La casilla `Do not transform frame stiffness for offsets from centroid` debe quedar marcada, segun el material de Lafontaine/profesor.

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

