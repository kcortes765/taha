# Investigación profunda ED1 PROG4 - fuentes del curso

Fecha: 2026-05-15 01:01 America/Santiago

## Regla de verdad aplicada

Para Edificio 1 PROG4, las decisiones de ingeniería se basan sólo en:

- `prog4/00_fuentes_de_verdad/01_enunciado/01_Enunciado_Taller_actualizado_2026-05-04.pdf`
- `prog4/00_fuentes_de_verdad/02_apuntes/00_Apuntes_del_Curso_2026-05-08_actualizado.pdf`
- `prog4/00_fuentes_de_verdad/03_material_apoyo/02_Material_Apoyo_Taller_2026.pdf`
- `prog4/00_fuentes_de_verdad/04_normativa/05_NCh433_2026_para_Curso.pdf`
- `prog4/00_fuentes_de_verdad/04_normativa/08_NCh3171_2017.pdf`, sólo cuando el curso la usa para combinaciones
- `prog4/00_fuentes_de_verdad/04_normativa/09_NCh1537_2009.pdf`, sólo cuando el curso la usa para cargas
- `prog4/00_fuentes_de_verdad/05_transcripciones_clase/*.txt`

La documentación CSI/ETABS se permite únicamente para operación OAPI, tablas, errores, sesión, guardado y extracción de resultados. No justifica criterios sísmicos.

## Evidencia visual ya revisada

Las páginas clave están renderizadas como PNG en:

`C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog4\Edificio_1\00_goal_y_plan\evidencia_fuentes_20260515_0015`

Páginas visuales críticas:

- Enunciado p.11: tabla de 6 casos y entregables de deformación/corte de muros/conclusiones.
- Apuntes p.117: torsión accidental forma a), con texto visible "5 modelos y 6 análisis".
- Apuntes p.118-p.119: combinaciones Método A.
- Apuntes p.122: Método B forma 1, 11 combinaciones.
- Apuntes p.123: Método B forma 2, 7 combinaciones y total 19 casos.
- Apuntes p.124: deformaciones sísmicas `CP + SC ± Sismo`, con y sin torsión accidental.
- Material Apoyo p.29-p.33: implementación Método A en ETABS mediante fuentes de masa desplazadas, casos auxiliares y modales específicos.
- Material Apoyo p.35-p.36: Método B forma 1 mediante cortes de piso CQC y momentos estáticos.
- Material Apoyo p.40-p.41: Método B forma 2 ingresando excentricidad por diafragma/piso.
- NCh433:2026 p.34: torsión accidental en análisis modal espectral por forma a) o b).

## Conclusiones de fuente

### 1. Edificio 1 no es un caso estático

El curso separa explícitamente Edificio 2 como método estático y Edificio 1 como análisis dinámico de superposición modal espectral. La transcripción `sismo 11_transcripcion.txt`, líneas 23 en adelante, dice que el método estático es para Edificio 2 y el dinámico modal para Edificio 1.

### 2. Los 6 casos del enunciado son obligatorios

El enunciado p.11 exige:

- diafragma rígido + torsión accidental caso a);
- diafragma rígido + torsión accidental caso b), forma 1;
- diafragma rígido + torsión accidental caso b), forma 2;
- diafragma semirrígido + torsión accidental caso a);
- diafragma semirrígido + torsión accidental caso b), forma 1;
- diafragma semirrígido + torsión accidental caso b), forma 2.

Estos son los 6 casos oficiales para tablas y conclusiones del informe.

### 3. Método A implica 5 estados por tipo de diafragma

Apuntes p.117 y NCh433:2026 p.34 indican que la forma a) desplaza el centro de masa:

- modelo natural;
- sismo X con CM desplazado +Y;
- sismo X con CM desplazado -Y;
- sismo Y con CM desplazado +X;
- sismo Y con CM desplazado -X.

Apuntes p.117 dice explícitamente que este caso implica `5 modelos y 6 análisis`.

La transcripción `taller sismo 8_transcripcion.txt` confirma el mismo criterio:

- línea 1665: un modelo para forma 1, un modelo para forma 2 y un modelo para forma A con centro de masa original;
- líneas 1667-1669: se corre hacia un lado, hacia el otro, hacia el otro y hacia el otro;
- línea 1785: método A significa considerar torsión accidental moviendo el centro de masa;
- líneas 2023-2025: análisis modal para estos 5 casos;
- líneas 2233-2235: se construyen cinco espectros, uno por caso;
- líneas 2695-2699: separar método B forma 1/forma 2 y luego método A con 5 casos.

Conclusión operativa corregida: para entrega defendible se materializan 5 checkpoints/EDB de Método A por diafragma. Como hay diafragma rígido y semirrígido, son 10 checkpoints/EDB para Método A.

### 4. Método B forma 1 y forma 2 deben contrastarse

`taller sismo 8_transcripcion.txt`:

- líneas 105-119: el profesor llama forma 1 y forma 2 a dos implementaciones y pide hacer ambas para demostrar que dan lo mismo;
- líneas 1139-1141: forma 1 calcula momentos de torsión y los ingresa como cargas;
- líneas 1243-1245: en forma 1 la torsión accidental la introduce el alumno;
- líneas 1271-1291: forma 2 la calcula internamente el programa;
- líneas 1317-1321: forma 1 y forma 2 deben dar iguales desplazamientos y cortes.

Conclusión operativa: B1 y B2 se dejan como familias separadas por diafragma. Para evitar ambigüedad de estado ETABS, se guardan 4 checkpoints/EDB: rígido B1, rígido B2, semirrígido B1, semirrígido B2.

### 5. Total defendible de checkpoints ED1 Parte 1

El informe mantiene 6 casos conceptuales del enunciado, pero la ejecución literal deja:

- 10 EDB de Método A: 5 rígidos + 5 semirrígidos;
- 4 EDB de Método B: B1/B2 rígidos + B1/B2 semirrígidos;
- 1 EDB base congelado y 1 EDB base auditado/modal.

Total operativo principal: 14 EDB/checkpoints de resultados, más base congelada.

### 6. Deformaciones no usan combinaciones mayoradas de resistencia

Apuntes p.124 exige verificar deformaciones con:

`CP + SC ± Sismo`

El mismo apunte aclara que el sismo se considera con y sin torsión accidental. Por eso las combinaciones mayoradas de p.118-p.123 sirven para resistencia/demandas de diseño, mientras que deformaciones se verifican con estados sin mayorar.

### 7. Corte basal y espectros deben quedar trazados

`sismo 13_transcripcion.txt` líneas 11-19 dice que tanto estático como modal espectral deben verificar que el corte basal sea mayor que el mínimo y que debe presentarse una tabla clara en el informe.

La misma transcripción explica que se debe reportar:

- masa/peso sísmico desde ETABS;
- peso sísmico por área;
- períodos asociados a mayores masas translacionales/rotacionales;
- R* por dirección;
- espectro elástico y espectro de diseño;
- corte elástico, corte de diseño, mínimo y factor de amplificación si corresponde.

## Corrección de rumbo

La estrategia compacta anterior de dos EDB para Método A era programáticamente posible, pero no era suficientemente literal frente a la evidencia de apuntes/transcripción. Se conserva como prototipo técnico, no como forma principal de entrega.

La estrategia vigente desde este documento es:

- ningún cierre ED1 Parte 1 se declara final con sólo 4 EDB compactos;
- Método A se expande a 5 estados por diafragma;
- B1/B2 se guardan separados por diafragma;
- cada EDB debe tener reporte, log, exportaciones y relación con el caso oficial del enunciado.

