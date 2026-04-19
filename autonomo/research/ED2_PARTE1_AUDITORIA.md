# Auditoria de Derivados - Ed.2 Parte 1

## Criterio
- `confirmado`: coincide con el canon oficial
- `util como referencia`: sirve, pero no define verdad
- `contradice canon`: debe corregirse o archivarse del flujo principal
- `sale del flujo principal`: se conserva solo como referencia historica o anexo

## 1. `docs/estudio/GUIA-EDIFICIO2-MARCOS-ETABS-v21.md`
- `confirmado`
  - geometria, materiales, secciones, grilla, cachos rigidos, diafragma D1
  - notas operativas ETABS 21, tablas, visualizacion, locale
- `util como referencia`
  - tips de interfaz, section cuts, rutas de menu, exportacion de tablas
- `contradice canon`
  - flujo principal montado sobre response spectrum
  - torsion accidental tratada como camino dinamico heredado
  - referencias a `SF=9806.65` y espectro como solucion oficial
- `sale del flujo principal`
  - casos `SDX/SDY/SDTX/SDTY`
  - desarrollo modal-espectral como resolucion principal de Parte 1

## 2. `autonomo/scripts/ed2`
- `confirmado`
  - `01-07`: modelo, materiales, secciones, geometria, losas, asignaciones y cargas gravitacionales
  - formulas `calc_C`, `calc_Cmin`, `calc_Cmax`, `EA_STATIC` en `config_ed2.py`
- `util como referencia`
  - parsing robusto de tablas ETABS en `12_extract_results_ed2.py`
  - manejo COM v19/v21 y compatibilidad DatabaseTables
- `contradice canon`
  - `08-12` orientados a response spectrum y torsion dinamica
  - `COMBINATIONS` originales basadas en `SDX/SDY`
  - verificacion basada en `R*` y flujo elastico-espectral
- `sale del flujo principal`
  - generacion sintetica en `generate_taller_ed2.py`
  - hardcodes en `plot_results_ed2.py`

## 3. `autonomo/research/VERIFICACION-TITANICA.md`
- `util como referencia`
  - evidencia de una ronda previa de revision intensa
  - inventario de discrepancias historicas
- `contradice canon`
  - afirma que Ed.2 usa analisis dinamico como camino oficial
  - declara Ed.2 "listo" bajo una logica que hoy no es la oficial
- `sale del flujo principal`
  - todo el tramo que presenta modal-espectral como solucion definitiva de Parte 1

## 4. `.apos/BOOTSTRAP.md`, `.apos/HANDOFF.md`, `.apos/STATUS.md`
- `util como referencia`
  - memoria operativa del proyecto y antecedentes de sesiones
- `contradice canon`
  - estado "Ed.2 completado" sin distinguir fuente, referencia y evidencia real local
  - mezcla de cierre tecnico con memoria de trabajo
- `sale del flujo principal`
  - cualquier afirmacion de cierre que no remita a `.edb` y CSV reales del flujo oficial

## 5. Criterio de continuidad
- Se reutiliza lo confirmado.
- Lo util como referencia se mantiene con rotulo de derivado.
- Lo que contradice canon se corrige en guia, pipeline y memorias.
- Lo que sale del flujo principal queda archivado logicamente y no puede volver a ser default.
