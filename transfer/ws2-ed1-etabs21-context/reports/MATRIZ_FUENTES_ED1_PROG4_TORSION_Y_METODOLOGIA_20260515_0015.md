# Matriz de fuentes ED1 PROG4 - torsión y metodología oficial

Fecha: 2026-05-15 00:15 America/Santiago

## Conclusión corregida

Edificio 1 **sí debe incluir torsión accidental**. No es opcional para el taller. El enunciado exige analizar 6 casos que cruzan:

- diafragma rígido y diafragma semirrígido;
- torsión accidental caso a);
- torsión accidental caso b), forma 1;
- torsión accidental caso b), forma 2.

Por lo tanto, el plan ED1 no puede quedar como "confirmar si va torsión"; debe quedar como **implementar y auditar torsión accidental en los 6 casos exigidos**, verificando cada implementación contra fuentes del curso.

## Fuentes revisadas

Carpeta base:

`C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog4\00_fuentes_de_verdad`

Fuentes principales usadas:

- `01_enunciado\01_Enunciado_Taller_actualizado_2026-05-04.pdf`
- `02_apuntes\00_Apuntes_del_Curso_2026-05-08_actualizado.pdf`
- `03_material_apoyo\02_Material_Apoyo_Taller_2026.pdf`
- `04_normativa\05_NCh433_2026_para_Curso.pdf`
- `05_transcripciones_clase\sismo 10_transcripcion.txt`
- `05_transcripciones_clase\sismo 11_transcripcion.txt`
- `05_transcripciones_clase\taller sismo 8_transcripcion.txt`

Evidencia visual renderizada:

`C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog4\Edificio_1\00_goal_y_plan\evidencia_fuentes_20260515_0015`

Manifest:

`C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog4\Edificio_1\00_goal_y_plan\evidencia_fuentes_20260515_0015\manifest_evidencia_paginas.csv`

## Matriz de decisiones

| Decisión | Criterio corregido | Evidencia |
|---|---|---|
| Método de análisis ED1 | Edificio 1 se resuelve con análisis dinámico/modal espectral, no con método estático como ED2. | Enunciado p.10 pide espectros, cortes basales, periodos y casos sísmicos ED1; apuntes p.98 dicen que el método dinámico modal espectral se puede aplicar siempre; transcripción `sismo 10` explica que ED2 usa estático y ED1 requiere modal espectral. |
| Torsión accidental | Debe incluirse. | Enunciado p.11 lista explícitamente torsión accidental caso a), caso b) forma 1 y caso b) forma 2. NCh433:2026 p.34 indica que en modal espectral la torsión accidental se incluye por forma a) o b). |
| 6 casos ED1 | Son obligatorios para Parte 1. | Enunciado p.11 cruza diafragma rígido/semirrígido con torsión a, b forma 1 y b forma 2: Casos 1 a 6. |
| Diafragma rígido | Caso base exigido. | Enunciado p.10 pide considerar diafragma rígido a nivel de piso; p.11 exige casos con diafragma rígido. Apuntes p.3 a p.6 definen diafragmas y comportamiento. |
| Diafragma semirrígido | También exigido para comparación. | Enunciado p.11 exige casos con diafragma semirrígido. Debe modelarse como familia separada, no como comentario. |
| Torsión forma a) | Se implementa desplazando centros de masa ±0.05 de la dimensión perpendicular; requiere modelo/matriz de masa desplazada y espectros consistentes. | NCh433:2026 p.34; apuntes p.117-p.119; Material Apoyo p.29-p.34; transcripción `sismo 10` desde 77:33 a 85:45 y `taller sismo 8` desde 03:21 en adelante. |
| Torsión forma b) | Se implementa con momentos estáticos derivados de cortes combinados CQC del análisis sin torsión o mediante excentricidades por piso en el caso espectral. | NCh433:2026 p.34; apuntes p.122-p.123; Material Apoyo p.35-p.41; `taller sismo 8` desde 05:33 a 08:20 y 39:05 a 45:46. |
| Forma b), forma 1 | Primero se corre espectral sin torsión; se extraen cortes de piso CQC; se calcula `Mk=(Qk-Qk+1)ek`; se aplican momentos de torsión por piso como cargas estáticas y se combinan con SDX/SDY. | NCh433:2026 p.34 comentario C6.3.3; Material Apoyo p.35-p.36; apuntes p.122; transcripción `taller sismo 8` 05:33-08:20 y 39:05-44:16. |
| Forma b), forma 2 | Se ingresan excentricidades por diafragma/piso en el caso espectral; ETABS genera la torsión internamente. Debe contrastarse contra forma 1. | Material Apoyo p.40-p.41; apuntes p.123; transcripción `taller sismo 8` 45:24-45:46 y tramo posterior indica que forma 1 y forma 2 son dos formas de ingresar lo mismo al programa. |
| Combinaciones método a) | Usar el bloque oficial de 15 combinaciones ETABS para método a). | Apuntes p.118-p.119; Material Apoyo p.45. |
| Combinaciones método b) forma 1 | Usar el bloque oficial de 11 combinaciones ETABS para método b) forma 1. | Apuntes p.122; Material Apoyo p.43. |
| Combinaciones método b) forma 2 | Usar el bloque oficial de 7 combinaciones ETABS / total 19 casos según tabla del curso. | Apuntes p.123; Material Apoyo p.44. |
| Deformaciones | Verificar con `CP + SC ± Sismo`, donde sismo se considera con y sin torsión accidental. | Apuntes p.124. NCh433 p.27 exige incluir torsión accidental en desplazamientos/rotaciones de diafragmas. |
| Límite de drift ED1 HA | Para hormigón armado, control de centro de masa con `0.0020 h`; además revisar cualquier punto de planta con criterio de NCh433. | NCh433:2026 p.27 y p.29. |
| Número de modos | Norma: masa equivalente acumulada ≥90% en X e Y. Curso/taller: además reportar chequeo 95% cuando aplique; transcripción menciona que en ED1 12 modos cumplían criterio de taller. | NCh433:2026 p.34; `sismo 11_transcripcion.txt` indica 90% normativo y 95% adoptado en taller para ED1. |
| CQC | Modal espectral combina máximos modales con CQC; no se suman modos algebraicamente. | NCh433:2026 p.38; transcripciones `sismo 10` y `sismo 11` explican CQC y cortes combinados. |
| Corte basal modal | Debe compararse con mínimo y máximo normativo; si está bajo mínimo se escala, y el máximo se puede limitar según criterio del curso. | NCh433:2026 p.38-p.39; apuntes p.112; transcripción `sismo 11` explica mínimo/máximo para modal. |

## Casos oficiales ED1 a ejecutar

| Caso enunciado | Diafragma | Torsión accidental | Implementación esperada |
|---:|---|---|---|
| 1 | Rígido | Caso a) | Modelo/matriz de masa natural + desplazamientos CM ±, espectros consistentes. |
| 2 | Rígido | Caso b) forma 1 | Espectral sin torsión + momentos estáticos `TEX/TEY` por piso desde cortes CQC. |
| 3 | Rígido | Caso b) forma 2 | Espectral con excentricidades por diafragma/piso ingresadas en ETABS. |
| 4 | Semirrígido | Caso a) | Igual que Caso 1, pero con modelación semirrígida. |
| 5 | Semirrígido | Caso b) forma 1 | Igual que Caso 2, pero con modelación semirrígida. |
| 6 | Semirrígido | Caso b) forma 2 | Igual que Caso 3, pero con modelación semirrígida. |

## Entregables que exige el enunciado para ED1 Parte 1

Del enunciado p.10-p.11:

- descripción y estructuración;
- modelación en ETABS;
- peso sísmico y peso sísmico por m²;
- densidad de muros en cada dirección;
- centro de masa y centro de rigidez por piso;
- periodos asociados a mayores masas translacionales y rotacionales: `Tx*`, `Ty*`, `Tz*`;
- tabla ETABS de periodos y masas equivalentes;
- número de modos para cumplir normativa;
- corte basal de diseño en cada dirección;
- tabla tipo apuntes para corte basal, `R*` por dirección y espectros elástico/diseño;
- esfuerzo de corte y momento volcante combinado por piso;
- indicadores 1 y 13 del perfil biosísmico;
- verificación de deformaciones sísmicas para los 6 casos;
- gráficos de cumplimiento;
- corte de diseño más desfavorable en muro eje 1 y muro eje F, en todos los pisos y para los 6 casos;
- cuadro resumen de los 6 casos y conclusiones.

## Correcciones al goal anterior

- Donde decía "confirmar si se requieren 6 casos" debe decir: **implementar 6 casos exigidos por enunciado**.
- Donde decía "confirmar cómo se define torsión" debe decir: **la torsión se define por NCh433 p.34 y por las formas del curso p.117-p.123 / Material p.29-p.45**.
- Donde decía "si corresponde CM/CR" debe decir: **CM/CR corresponde porque el enunciado p.10 lo pide explícitamente**.
- El goal debe exigir evidencia por página/minuto antes de cada decisión estructural.

