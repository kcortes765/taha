# MODO GOD documentacion WS2 - fuentes, norma y apuntes

Fecha: 2026-05-08

## Mandato

Toda decision tecnica debe estar alineada con las fuentes del curso y la normativa vigente del ramo.

No basta con que el codigo corra. Debe correr con criterio defendible frente al profesor.

## Fuentes prioritarias

Leer y usar en este orden cuando haya conflicto:

1. `files/01_Enunciado_Taller_actualizado_2026-05-04.pdf`
2. `files/00_Apuntes_del_Curso_2026-05-08_actualizado.pdf`
3. `files/02_Material_Apoyo_Taller_2026.pdf`
4. `files/05_NCh433_2026_para_Curso.pdf`
5. `files/08_NCh3171_2017.pdf`
6. `files/09_NCh1537_2009.pdf`
7. `files/13_GUIA_ED1_ETABS_v21.md`
8. `files/21_GUIA_ED2_ETABS_v21.md`
9. `files/22_ED2_PARTE1_CANON.md`
10. `files/10_INDICE_Apuntes.md`
11. `files/11_02c_Analisis_Estatico.pdf`
12. `files/12_02d_Analisis_Dinamico_Modal_Espectral.pdf`

Fuentes historicas solo para comparacion:

- `files/01_Enunciado_Taller.pdf`
- `files/06_NCh433_1996_Mod2009_historica.pdf`
- `files/07_DS61_2011_historico.pdf`

## Regla de conflicto

Si dos fuentes se contradicen:

1. gana el enunciado actualizado para alcance/entregables/datos del taller;
2. gana `Apuntes del Curso 2026-05-08` para criterio vigente del curso;
3. gana `NCh433:2026` para base normativa sismica;
4. `Material Apoyo Taller 2026` manda en procedimientos ETABS/torsion/drift/combinaciones cuando el curso lo da como metodo de taller;
5. documentos historicos sirven para entender, no para justificar si contradicen la capa 2026.

## Que investigar antes de aplicar codigo

Antes de cada bloque ETABS, verificar contra fuentes:

### Diafragma

- si el caso debe ser rigido/semirigido;
- como se reporta drift y torsion;
- que tablas ETABS usa el material de apoyo.

### Cargas y masa

- patrones `PP`, `SCP`, `SCT`, `TERP`, `TERT`;
- techo vs piso tipo;
- fraccion de sobrecarga en masa;
- evitar duplicar peso propio;
- cambio del enunciado actualizado: en ambos edificios considerar no aglomeracion de personas.

### Sismo

- uso de `NCh433:2026` como capa vigente;
- parametros de sitio/zona/categoria;
- espectro;
- `R`, `R*`, escalas y limites;
- corte basal y control.

### Torsion accidental

- Edificio 1 conserva matriz/casos propios;
- revisar formas/metodos del Material Apoyo Taller;
- no copiar automaticamente criterios de Edificio 1 a Edificio 2.

### Combinaciones

- verificar contra Material Apoyo Taller, apuntes actualizados y NCh3171;
- no crear combinaciones por intuicion;
- registrar cada combo creada y su fuente.

### Resultados

- peso sismico;
- CM/CR cuando aplique;
- periodos y participacion modal;
- corte basal;
- drifts;
- story forces/base reactions;
- torsion;
- tablas ETABS exactas y filtros.

## Output documental obligatorio

Cada reporte de ejecucion debe incluir una seccion:

```text
Fuentes usadas y criterio
```

Con:

- archivo;
- pagina/seccion si se pudo identificar;
- decision tomada;
- como se tradujo a ETABS/codigo.

## Prohibido

- Usar solo memoria o intuicion.
- Justificar con DS61/NCh433 historica si contradice la capa 2026.
- Aplicar formulas/combinaciones sin dejar fuente.
- Cambiar releases torsionales Ed.1 sin fuente/orden explicita.
- Inventar resultados cuando ETABS no entregue tabla.

## Frase rectora

Primero fuente, luego codigo, luego ETABS, luego tabla. Si una decision no se puede defender con fuente, no queda cerrada.

