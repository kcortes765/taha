# ED1 torsion matrix prog2

- Fecha: 2026-05-09 09:38:58
- Base limpia: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif1\models\ED1_PARTE1_WS2_PROG2_20260508_2213.EDB`
- Log: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif1\logs\ed1_torsion_matrix_20260509_0930.log`
- JSON: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif1\logs\ed1_torsion_matrix_20260509_0930.json`
- Export root: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif1\exports\torsion_matrix_20260509_0930`

## Criterio

- Se trabaja solo sobre copias fechadas en `prog2`.
- No se reconstruye geometria.
- No se modifican releases.
- b1: torsion estatica por piso desde diferencia de cortes espectrales sin excentricidad.
- b2: excentricidad de diafragma por longitud positiva en casos `SEx_b2`/`SEy_b2`.
- La variante semirrigida cambia la definicion `D1` a semi-rigid en su propia copia.

## Variantes

### rigid

- Modelo: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif1\models\ED1_PARTE1_WS2_PROG2_RIGID_MATRIX_20260509_0930.EDB`
- Diafragma semi-rigido: `False`
- Run base sin torsion estatica OK: `True`
- Run final matriz OK: `True`
- CSV torsion b1: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif1\exports\torsion_matrix_20260509_0930\rigid\ed1_rigid_b1_floor_torsion_20260509_0930.csv`
- TorX target/base +/base -: `511.910` / `512.383` / `512.383` tonf*m
- TorY target/base +/base -: `1426.169` / `1427.487` / `1427.487` tonf*m
- Gap TorX+/TorX-/TorY+/TorY-: `0.0009241269053211817` / `0.0009241269053211817` / `0.0009241064068564869` / `0.0009241064068564869`

### semirigid

- Modelo: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif1\models\ED1_PARTE1_WS2_PROG2_SEMIRIGID_MATRIX_20260509_0930.EDB`
- Diafragma semi-rigido: `True`
- Run base sin torsion estatica OK: `True`
- Run final matriz OK: `True`
- CSV torsion b1: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif1\exports\torsion_matrix_20260509_0930\semirigid\ed1_semirigid_b1_floor_torsion_20260509_0930.csv`
- TorX target/base +/base -: `511.150` / `511.622` / `511.622` tonf*m
- TorY target/base +/base -: `1419.845` / `1421.157` / `1421.157` tonf*m
- Gap TorX+/TorX-/TorY+/TorY-: `0.0009242393571172301` / `0.0009242393571172301` / `0.0009240345739409272` / `0.0009240345739409272`

## Estado honesto

Esto cierra programaticamente las variantes rigida y semirrigida con b1/b2. Metodo a por masas desplazadas queda documentado como flujo mas riesgoso si se exige con cuatro mass sources y casos modales derivados; no se fuerza dentro del EDB principal para evitar corromper una corrida valida.
