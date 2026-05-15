# RESEARCH_LOG

## 2026-05-14 - Preparación de investigación ED1 PROG4

Pregunta activa:

- ¿Cómo cerrar Edificio 1 Parte 1 con análisis dinámico/modal espectral, torsión y diafragma según fuentes oficiales del curso, sin mezclar criterios externos?

Fuentes a contrastar:

- Enunciado actualizado.
- Apuntes del curso 2026-05-08.
- Material Apoyo Taller 2026.
- NCh433:2026 usada por el curso.
- NCh3171/NCh1537 cuando el curso las use.
- Transcripciones de clase.
- Documentación oficial CSI/ETABS solo para operación OAPI.

Estrategia:

- Crear matriz decisión -> fuente -> página/minuto -> evidencia.
- Para texto en imágenes, generar evidencia visual/OCR puntual.
- Registrar contradicciones antes de implementar.
- No convertir guías MD ni respuestas previas en verdad final.

## 2026-05-15 - Resultado investigación torsión ED1

Resultado:

- ED1 requiere torsión accidental en los 6 casos del enunciado.
- La forma a) desplaza centros de masa y exige espectros/casos modales consistentes.
- La forma b) se implementa en dos formas operativas en ETABS:
  - forma 1: momentos estáticos por piso calculados desde cortes CQC;
  - forma 2: excentricidades por diafragma/piso en el caso espectral.
- Forma 1 y forma 2 deben contrastarse; el curso indica que son dos maneras de ingresar el método b).

Evidencia:

- `MATRIZ_FUENTES_ED1_PROG4_TORSION_Y_METODOLOGIA_20260515_0015.md`.
