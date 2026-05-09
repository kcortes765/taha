# Checklist auditoria modelo Edificio 1 - WS2

Marcar cada item como:

- `OK`
- `NO`
- `NO VERIFICADO`
- `DUDOSO`

## 0. Seguridad licencia

- Una sola instancia de ETABS 21 abierta.
- No hay otro agente/script conectado a ETABS.
- Se verifico `Get-Process ETABS`.

## 1. Archivo activo

- Ruta exacta del `.EDB`.
- Existe backup local antes de modificar.
- El archivo corresponde a Edificio 1, no Edificio 2.
- El archivo esta bajo `HECRAS2`.

## 2. Version

- ETABS Ultimate 21.
- Build identificado.
- Modelo abre sin errores.

## 3. Stories y grillas

- 20 pisos.
- Alturas consistentes con enunciado/contexto.
- Grillas X/Y visibles y coherentes.
- Grillas auxiliares presentes donde fueron necesarias.

## 4. Muros

- Muros en X e Y presentes.
- Muros principales coinciden con planta tipo.
- Shaft/ascensor identificado.
- Espesores correctos (`MHA20G30`, `MHA30G30` segun corresponda).
- No hay muros duplicados evidentes.
- Lineas centrales conectan donde corresponde.

## 5. Vigas

- Vigas `VI20/60G30` presentes.
- Vigas invertidas con `Cardinal Point = 2 - Bottom Center`.
- `Do not transform frame stiffness for offsets from centroid` marcado.
- End length offsets automaticos.
- Rigid zone factor coherente.
- Releases aplicados solo donde corresponde.
- No hay liberacion axial/corte/torsion indebida.

## 6. Losas

- `Losa15G30` presente.
- Huella de losa real, no envolvente completa si hay vacios.
- Aberturas/vacios representados.
- Modificadores flexurales `m11/m22/m12 = 0.25`.
- Losa conectada a muros/vigas.

## 7. Mesh

- Auto mesh de losas definido.
- Auto mesh de muros definido.
- Tamano maximo objetivo: 1.0 m salvo justificacion.
- Mesh visible/verificable.
- No hay shells enormes sin subdivision razonable.

## 8. Apoyos

- Puntos de base empotrados.
- Conteo de apoyos registrado.
- No hay apoyos faltantes en muros principales.

## 9. Diafragma

- Diafragma rigido asignado si corresponde al caso activo.
- Diferenciar caso rigido vs semirigido.
- No mezclar ambos sin version de archivo clara.

## 10. Cargas

- Patrones `PP`, `SCP`, `SCT`, `TERP`, `TERT` definidos.
- Cargas por losa verificadas.
- Cargas de techo separadas si corresponde.
- Self weight multiplier revisado.

## 11. Fuente de masa

- Mass source definida.
- Incluye self mass / PP segun criterio ETABS.
- Incluye `TERP`.
- Incluye fraccion de sobrecarga segun curso/enunciado.
- No duplica peso propio.

## 12. Analisis

- Modal definido.
- Espectro definido con base NCh433:2026 del curso.
- Torsion accidental / 6 casos identificados.
- Combinaciones creadas.
- Analisis aun no corrido o corrido con evidencia.

## 13. Evidencia minima a devolver

- Captura o tabla de stories.
- Captura o tabla de propiedades de vigas invertidas.
- Captura o tabla de releases.
- Captura o tabla de modificadores de losa.
- Captura o tabla de mass source si existe.
- Lista de archivos `.EDB` encontrados en `HECRAS2`.

