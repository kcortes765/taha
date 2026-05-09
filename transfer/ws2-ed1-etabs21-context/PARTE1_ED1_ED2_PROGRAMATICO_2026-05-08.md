# Parte 1 programatica Ed.1 + Ed.2 - Criterio WS2

## Objetivo

Resolver completamente Parte 1 de ambos edificios por flujo programatico/controlado en ETABS 21, usando WS2 como maquina de ejecucion.

Prioridad actual: Edificio 1 primero hasta cierre completo de Parte 1. Edificio 2 queda en espera hasta que Edificio 1 tenga analisis, resultados y reporte.

## Regla critica

Una sola instancia de ETABS 21. Antes de abrir ETABS o correr COM/API:

```powershell
Get-Process ETABS -ErrorAction SilentlyContinue
```

Si hay una instancia abierta, no abrir otra.

Ademas:

- no trabajar dos edificios en simultaneo;
- no correr dos scripts OAPI a la vez;
- no abrir Edificio 2 hasta cerrar o pausar formalmente Edificio 1.

## Fuentes canonicas

1. `files/01_Enunciado_Taller_actualizado_2026-05-04.pdf`
2. `files/00_Apuntes_del_Curso_2026-05-08_actualizado.pdf`
3. `files/05_NCh433_2026_para_Curso.pdf`
4. `files/02_Material_Apoyo_Taller_2026.pdf`
5. `files/08_NCh3171_2017.pdf`
6. `files/09_NCh1537_2009.pdf`
7. `files/13_GUIA_ED1_ETABS_v21.md`
8. `files/21_GUIA_ED2_ETABS_v21.md`
9. `files/22_ED2_PARTE1_CANON.md`

## Diferencia Ed.1 vs Ed.2

Edificio 1:

- Edificio irregular de 20 pisos, estructurado en base a muros de hormigon armado.
- Tiene matriz de 6 casos del enunciado.
- La geometria fue trabajada por UI y debe auditarse antes de tocar.
- No correr pipeline historico desde cero sin autorizacion.
- Modelo activo probable auditado: `HECRAS2\prog\Edif1\ED1_PARTE1_COMPLETA_TRABAJO.EDB`.
- Releases torsionales fueron pedidos por el profesor; no eliminarlos por defecto.
- Primer paso de ejecucion: crear backup y copia limpia fechada, luego completar diafragma, cargas, masa, casos, combos, analisis y tablas.

Edificio 2:

- Edificio estructurado en base a marcos.
- No hereda la matriz de 6 casos de Ed.1.
- Parte 1 mantiene nucleo de metodo estatico, con modal como exigencia/chequeo incorporado por curso.
- Existen archivos `MODELO EDIF2.*` en raiz `HECRAS2`; deben auditarse antes de correr codigo.
- Modelo activo probable auditado: `HECRAS2\Edif2\Edificio2_Estatico con carga sismica.EDB`.
- No avanzar Ed.2 hasta que Ed.1 Parte 1 este cerrado.

## Flujo minimo seguro

### 0. Auditoria antes de modificar

Para cada edificio:

- Ruta exacta del `.EDB`.
- Version/build ETABS.
- Numero de pisos y alturas.
- Conteo de objetos.
- Materiales y secciones.
- Diafragmas.
- Modificadores.
- Apoyos.
- Cargas.
- Mass source.
- Casos y combinaciones.
- Estado de analisis.
- Tablas/exportaciones disponibles.

### 1. Normativa y sitio

Usar `NCh433:2026` como base. Los apuntes actualizados fijan esa vigencia en pagina 61.

Para sitio/suelo:

- Revisar parametros de `NCh433:2026`.
- Considerar la nueva capa `NCh3793:2025`, `Vs30`, `Tg` y `H/V` cuando corresponda.
- No volver a justificar oficialmente con `NCh433:1996 + DS61` salvo como capa historica.

### 2. Metodo estatico

Apuntes actualizados pagina 98:

- `Qo = C * I * P`
- `P = peso sismico`
- `C` depende de `Ao`, `S`, `R`, `T*`, `T'`, `n`
- respetar limites `Cmin/Cmax`

Apuntes actualizados pagina 103:

- para metodo estatico, revisar 19 combinaciones con:
  - `CP`
  - `L`
  - `Lr`
  - `SDX`, `SDY`
  - `TEX`, `TEY`

### 3. Metodo dinamico modal espectral

Apuntes actualizados pagina 112:

- `Sa = (S * Ao * alpha) / (R* / I)`
- verificar participacion modal, periodos, escala/corte basal y limites normativos.

### 4. Torsion accidental

Apuntes actualizados:

- pagina 118: forma `a)`, 15 combinaciones.
- pagina 122: forma `b)`, alternativa 1, 11 combinaciones.
- pagina 123: forma `b)`, alternativa 2, 7 combinaciones.

Para Ed.1, cruzar esto con la matriz de 6 casos del enunciado.

Para Ed.2, no copiar automaticamente los 6 casos de Ed.1.

### 5. Outputs Parte 1

Para cerrar cada edificio se debe poder trazar:

- peso sismico
- CM/CR si aplica
- periodos y participacion modal
- corte basal
- espectro usado
- drift/desplazamientos
- torsion accidental
- combinaciones gobernantes
- story forces / base reactions
- demandas de elementos criticos segun entrega
- tablas ETABS exactas y filtros usados

## Estado de codigo

- Ed.1: codigo historico incluido en `code/ed1_taller_etabs_legacy/`. Estaba orientado a flujo historico/ETABS 19 y/o generacion desde cero; adaptarlo incrementalmente a ETABS 21 y al `.EDB` ya modelado por UI.
- Ed.2: flujo activo incluido en `code/ed2_pipeline_active/`. No ejecutarlo hasta cerrar Ed.1.

## Entregable inicial pedido a WS2

No correr analisis completo aun.

Primero devolver un reporte con:

- Ed.1 `.EDB` activo y estado.
- Ed.2 `.EDB` activo y estado.
- Diferencias contra fuentes canonicas.
- Que falta antes de correr Parte 1 completa.
- Riesgos de usar UI vs API.
- Propuesta de secuencia programatica segura.
