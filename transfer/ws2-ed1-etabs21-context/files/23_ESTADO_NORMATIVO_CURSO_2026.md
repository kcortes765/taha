# Estado Normativo del Curso - 2026

## Estado del documento
- Fecha: 2026-04-20
- Alcance: base normativa canónica del curso ADSE 1S-2026
- Objetivo: fijar qué norma manda hoy en el curso y cómo afecta a Edificio 1 y Edificio 2

## Dictamen corto
- Desde el punto de vista del curso, la base sísmica activa pasó a ser `NCh433:2026`.
- Esto no invalida automáticamente todos los números históricos del repo.
- Sí invalida tratar como canónicos los documentos derivados que siguen declarando `NCh433:1996 Mod.2009 + DS61` como base vigente del curso.

## Evidencia cruda del curso

### Transición inicial
- En clase del `2026-03-12`, antes de la aprobación oficial, el profesor todavía distinguía entre:
  - norma vigente evaluable del programa
  - aspectos nuevos de la norma que venía en camino
- Evidencia:
  - `app transcripciones/Academico/2026-2/Sismo/02_processed/transcripts/transcript_3d9ff0eeb61c.clean.txt`, líneas 154-168

### Cambio efectivo del curso
- `2026-03-27`: Music informa que se aprobó oficialmente `NCh433:2026`.
- `2026-03-29`: Music sube a Moodle la carpeta de normas del curso e incluye `NCh433:2026`.
- `2026-04-02`: Music pide bajar apuntes nuevos con disposiciones de `NCh433:2026 vigente` y estudiar esa norma.
- Evidencia:
  - `materiales_fuente/sismo/correo/emails.json`, entrada `2026-03-27 18:08`
  - `materiales_fuente/sismo/correo/emails.json`, entrada `2026-03-29 14:00`
  - `materiales_fuente/sismo/correo/emails.json`, entrada `2026-04-02 12:22`

## Jerarquía de fuentes vigente
1. `docs/Enunciado Taller.pdf`
2. Correos y transcripciones del curso posteriores al `2026-03-27`
3. `materiales_fuente/sismo/Normas Curso/Normas a Utilizar en Curso/NCh433-2026 para Curso.pdf`
4. `docs/Material taller/Material Apoyo Taller 2026.pdf`
5. `NCh3171`, `NCh1537`, `NCh430` y demás normas de material/cargas que sigan aplicando
6. Documentos derivados del repo (`docs/estudio/*.md`, guías ETABS, research, scripts)

## Regla práctica de uso
- Si el enunciado dice "normativa vigente", hoy debe leerse como `NCh433:2026` dentro del curso.
- Si una guía o resumen del repo sigue citando `NCh433 + DS61` como base vigente del curso, debe tratarse como documento histórico o parcialmente desactualizado.
- Si un valor numérico coincide entre la capa antigua y la nueva norma, se puede conservar el número, pero citando `NCh433:2026` y no defendiéndolo con `DS61`.

## Impacto sobre Edificio 1

### Qué cambia
- Cambia la base normativa oficial del curso.
- Cambia el criterio de clasificación sísmica de sitio: `Vs30 + Tg`.
- Cambia el marco de justificación para diafragmas, torsión accidental, masa y drift.

### Qué puede seguir igual numéricamente
Para `Antofagasta + Zona 3 + Sitio C + Categoría II + muros especiales de HA`, `NCh433:2026` entrega:
- `Ao = 0.40 g`
- `S = 1.05`
- `T0 = 0.40 s`
- `T' = 0.45 s`
- `n = 1.40`
- `p = 1.60`
- `I = 1.0`
- `R = 7`
- `R0 = 11`

Conclusión:
- Edificio 1 puede conservar varios números ya usados en el repo.
- Pero ya no corresponde justificarlos como `NCh433 + DS61`.

## Impacto sobre Edificio 2

### Qué se mantiene
El enunciado fija para Edificio 2:
- 5 pisos
- Antofagasta
- suelo `C`
- oficina
- diafragma rígido a nivel de piso
- análisis estático como núcleo de Parte 1

Bajo `NCh433:2026`, para `Zona 3 + Sitio C + Categoría II` se mantienen los mismos parámetros principales del caso histórico:
- `Ao = 0.40 g`
- `S = 1.05`
- `T0 = 0.40 s`
- `T' = 0.45 s`
- `n = 1.40`
- `p = 1.60`

Además:
- el método estático sigue siendo aplicable para Edificio 2 por tener `5 niveles` y `15.5 m` de altura
- el límite de drift para marcos especiales de hormigón armado sigue siendo `0.0020 h`
- la torsión accidental estática sigue usando `ea = ±0.10 b (Zk/H)`

### Qué no debe seguir igual por inercia
- La justificación normativa ya no debe escribirse contra `DS61`.
- La masa sísmica debe leerse desde `NCh433:2026 5.5.1`.
- La verificación de drift debe leerse desde `5.9.2` y `5.9.3`.

## Documentos del repo que deben tratarse como históricos o parcialmente desactualizados
- `docs/estudio/02b-Normativa-NCh433-DS61.md`
- `docs/estudio/GUIA-COMPLETA-EDIFICIO1-ETABS-v19.md`
- `docs/estudio/GUIA-EDIFICIO2-MARCOS-ETABS-v19.md`
- `docs/estudio/GUIA-EDIFICIO2-MARCOS-ETABS-v21.md`

Esto no significa que estén inútiles.
Significa que su base normativa debe filtrarse a través de este archivo antes de reutilizarlas.

## Regla final para defensa
- Defender `NCh433:2026` como base oficial del curso.
- Aclarar que en Edificio 1 y Edificio 2 varios parámetros sísmicos principales para `Zona 3 / Sitio C / Categoría II` coinciden numéricamente con la capa histórica.
- No decir "da lo mismo la norma".
- Decir: "la base normativa cambió a 2026; en estos edificios algunos parámetros principales coinciden, pero la defensa, la trazabilidad y la lectura de sitio/drift/torsión se hacen con `NCh433:2026`."
