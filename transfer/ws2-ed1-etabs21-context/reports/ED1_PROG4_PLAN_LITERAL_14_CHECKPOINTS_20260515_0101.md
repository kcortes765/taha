# Plan literal ED1 PROG4 Parte 1 - 14 checkpoints

Fecha: 2026-05-15 01:01 America/Santiago

## Objetivo

Cerrar Edificio 1 Parte 1 en PROG4 con una ejecución que pueda defenderse contra el enunciado, apuntes, material de apoyo y transcripciones de clase, sin depender de interpretaciones compactas no explicadas.

El informe final se organiza en 6 casos oficiales del enunciado, pero la ejecución ETABS queda separada en 14 checkpoints/EDB para que el Método A quede literal como `5 modelos y 6 análisis`.

## Base de trabajo

Base congelada:

`C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog4\Edificio_1\06_parte1_completa_20260515_0016\00_base_congelada\ED1_PROG4_CIERRE_MODAL_20260512_2306.EDB`

Base de trabajo:

`C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog4\Edificio_1\06_parte1_completa_20260515_0016\01_modelos_trabajo\ED1_PROG4_PARTE1_WORKING_20260515_0016.EDB`

Regla: no modificar la base congelada.

## Checkpoints por generar

### Método A con diafragma rígido

1. `ED1_PROG4_C1_RIGID_A_00_CM_ORIGINAL_YYYYMMDD_HHMM.EDB`
2. `ED1_PROG4_C1_RIGID_A_01_SX_CM_PLUS_Y_YYYYMMDD_HHMM.EDB`
3. `ED1_PROG4_C1_RIGID_A_02_SX_CM_MINUS_Y_YYYYMMDD_HHMM.EDB`
4. `ED1_PROG4_C1_RIGID_A_03_SY_CM_PLUS_X_YYYYMMDD_HHMM.EDB`
5. `ED1_PROG4_C1_RIGID_A_04_SY_CM_MINUS_X_YYYYMMDD_HHMM.EDB`

Estos cinco EDB alimentan el Caso 1 del enunciado.

### Método A con diafragma semirrígido

6. `ED1_PROG4_C4_SEMIRIGID_A_00_CM_ORIGINAL_YYYYMMDD_HHMM.EDB`
7. `ED1_PROG4_C4_SEMIRIGID_A_01_SX_CM_PLUS_Y_YYYYMMDD_HHMM.EDB`
8. `ED1_PROG4_C4_SEMIRIGID_A_02_SX_CM_MINUS_Y_YYYYMMDD_HHMM.EDB`
9. `ED1_PROG4_C4_SEMIRIGID_A_03_SY_CM_PLUS_X_YYYYMMDD_HHMM.EDB`
10. `ED1_PROG4_C4_SEMIRIGID_A_04_SY_CM_MINUS_X_YYYYMMDD_HHMM.EDB`

Estos cinco EDB alimentan el Caso 4 del enunciado.

### Método B forma 1 y forma 2

11. `ED1_PROG4_C2_RIGID_B1_YYYYMMDD_HHMM.EDB`
12. `ED1_PROG4_C3_RIGID_B2_YYYYMMDD_HHMM.EDB`
13. `ED1_PROG4_C5_SEMIRIGID_B1_YYYYMMDD_HHMM.EDB`
14. `ED1_PROG4_C6_SEMIRIGID_B2_YYYYMMDD_HHMM.EDB`

Estos cuatro EDB alimentan los Casos 2, 3, 5 y 6 del enunciado.

## Flujo técnico por bloque

### Bloque 0 - seguridad ETABS

Antes de cada script:

```powershell
Get-Process ETABS -ErrorAction SilentlyContinue
```

Condiciones:

- si ETABS está abierto por el usuario, no abrir otra instancia;
- si la instancia está colgada en `miOpen`, `Model Initialization`, `array`, `recovering results` o diálogo similar, registrar evidencia y cerrar sólo esa instancia antes de reintentar;
- no ejecutar dos scripts OAPI en paralelo;
- al final del goal, cerrar ETABS.

### Bloque 1 - auditoría base

Exportar y validar:

- historias y alturas;
- grillas;
- materiales y secciones;
- muros, losas y vigas;
- apoyos;
- releases y offsets;
- modificadores;
- cargas gravitacionales;
- mass source;
- diafragma;
- modal base;
- CM/CR, o bloqueo documentado si ETABS no expone CR.

### Bloque 2 - espectros y tabla manual

Crear Excel ED1 con:

- peso sísmico y peso por m2;
- densidad de muros X/Y;
- modos, masas equivalentes, `Tx*`, `Ty*`, `Tz*`;
- `R*` X/Y;
- espectro elástico y espectro de diseño;
- corte basal elástico, diseño, mínimo y escalamiento;
- índice 1 e índice 13 del perfil biosísmico;
- hojas para pegar tablas ETABS;
- hoja de trazabilidad fuente/página/minuto.

### Bloque 3 - Método A

Para cada diafragma:

- crear EDB natural;
- crear EDB CM +Y para sismo X;
- crear EDB CM -Y para sismo X;
- crear EDB CM +X para sismo Y;
- crear EDB CM -X para sismo Y;
- correr modal y espectral correspondiente;
- exportar `Base Reactions`, `Story Forces`, `Story Drifts`, `Modal Participating Mass Ratios`, `Modal Periods`, `Diaphragm Center Of Mass Displacements`;
- registrar espectro usado por cada estado.

### Bloque 4 - Método B forma 1

Para cada diafragma:

- correr espectral sin torsión accidental;
- extraer cortes combinados CQC por piso;
- calcular fuerzas de piso por diferencia de cortes;
- calcular `Mk = (Qk - Qk+1) * ek`;
- aplicar momentos de torsión como cargas estáticas por piso;
- crear 11 combinaciones de apuntes p.122/material p.43;
- correr y exportar resultados.

### Bloque 5 - Método B forma 2

Para cada diafragma:

- ingresar excentricidades por piso en el caso espectral;
- crear 7 combinaciones de apuntes p.123/material p.44;
- correr y exportar resultados;
- comparar con B1 en cortes y desplazamientos.

### Bloque 6 - deformaciones

Verificar según apuntes p.124:

`CP + SC ± Sismo`

Con sismo:

- sin torsión accidental;
- con torsión accidental positiva;
- con torsión accidental negativa;
- en X e Y;
- para diafragma rígido y semirrígido.

Controles:

- condición 1: drift relativo en centro de masa;
- condición 2: drift relativo en punto crítico de planta respecto al centro de masa;
- límite `0.002 h` para hormigón armado en centro de masa;
- límite adicional `0.001 h` para exceso de punto extremo sobre centro de masa.

### Bloque 7 - corte en muros eje 1 y eje F

Para los 6 casos oficiales:

- extraer corte de diseño más desfavorable en muro eje 1;
- extraer corte de diseño más desfavorable en muro eje F;
- reportar piso, combinación/caso y valor;
- hacer tabla todos los pisos.

### Bloque 8 - auditoría final

Auditar:

- cada EDB abre sin diálogo;
- cada EDB tiene resultados;
- `.LOG/.OUT` sin errores relevantes;
- tablas exportadas no vacías;
- masa participante cumple NCh433;
- corte basal cumple mínimo;
- deformaciones cumplen o quedan explicitadas;
- B1 y B2 quedan comparadas;
- Método A queda trazado a 5 estados por diafragma;
- no quedan procesos ETABS vivos.

## Entregables

- 14 EDB/checkpoints con nombres explícitos;
- reportes por caso y reporte consolidado;
- CSV/JSON de resultados;
- Excel ED1 manual/control;
- guía UI ED1 completa;
- paquete de transferencia;
- delta APOS;
- commit Git de todo lo versionable.

## Criterio de avance

No se declara Edificio 1 cerrado si falta cualquiera de estos puntos:

- los 6 casos del enunciado;
- la expansión de Método A a 5 estados por diafragma;
- las deformaciones `CP + SC ± Sismo`;
- la comparación B1/B2;
- corte basal mínimo;
- corte de muros eje 1 y eje F;
- evidencia ETABS exportada;
- auditoría final sin instancia ETABS viva.

