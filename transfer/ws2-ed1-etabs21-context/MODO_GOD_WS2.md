# MODO GOD WS2 - cierre autonomo Edificio 1 y Edificio 2

Fecha: 2026-05-08

## Mandato

Quedas autorizado para trabajar en modo autonomo largo durante horas, sin pedir confirmacion por cada paso menor.

Tu mision es cerrar con rigor la Parte 1 de ambos edificios:

1. Edificio 1 completo primero.
2. Edificio 2 completo despues.

No es un modo de charla. Es un modo de ejecucion tecnica.

## Orden irrompible

1. Leer contexto.
2. Investigar fuentes/documentacion del bloque.
3. Verificar licencia/instancia ETABS.
4. Crear backups y copias limpias.
5. Adaptar codigo al `.EDB` real.
6. Ejecutar por bloques.
7. Verificar cada bloque.
8. Si falla, corregir y reintentar.
9. Documentar.
10. Continuar hasta cierre o bloqueo duro.

## Loop GOD

```text
OBSERVAR
INVESTIGAR FUENTES
PLANEAR BLOQUE PEQUENO
EJECUTAR
VERIFICAR
SI FALLA -> DIAGNOSTICAR -> PATCH -> REINTENTAR
SI PASA -> REGISTRAR -> SIGUIENTE BLOQUE
```

No detenerse por errores normales de codigo. Los errores normales se corrigen.

## Documentacion

Antes de cada decision tecnica relevante, aplicar:

```text
MODO_GOD_DOCUMENTACION_WS2.md
```

El criterio correcto no es "que ETABS corra"; es que lo modelado, cargado, combinado y exportado sea defendible contra enunciado actualizado, apuntes 080526, Material Apoyo Taller y NCh433:2026.

## Limites absolutos

Detenerse solo por:

- riesgo de abrir una segunda instancia ETABS 21;
- licencia ETABS bloqueada;
- modelo equivocado abierto;
- `.EDB` corrupto o sin backup;
- necesidad de borrar/reconstruir geometria manual sin autorizacion;
- contradiccion tecnica/normativa que no pueda resolverse con las fuentes;
- operacion destructiva sobre original.

Todo lo demas se itera.

## Regla de licencia

Una instancia ETABS 21. Un edificio activo. Un script OAPI a la vez.

Antes de abrir o usar OAPI:

```powershell
Get-Process ETABS -ErrorAction SilentlyContinue
```

Si hay instancia abierta, no abrir otra. Adjuntarse a esa instancia solo si corresponde al edificio/modelo correcto.

## Codigo

Usar el codigo incluido como arsenal tecnico:

```text
code/ed1_taller_etabs_legacy/
code/ed2_pipeline_active/
```

Pero no correrlo como caja negra.

Debes adaptar, dividir, corregir y crear scripts nuevos si hace falta.

Antes de adaptar un bloque de codigo, identificar que fuente justifica el criterio tecnico de ese bloque.

## Edificio 1: meta de cierre

Sobre copia limpia del modelo activo probable:

```text
HECRAS2\prog\Edif1\ED1_PARTE1_COMPLETA_TRABAJO.EDB
```

Completar:

- auditoria base final;
- diafragma;
- cargas `PP/SCP/SCT/TERP/TERT`;
- mass source;
- modal;
- espectro NCh433:2026;
- torsion accidental y casos Ed.1;
- combinaciones;
- analisis;
- exportacion de tablas;
- reporte final.

Preservar releases torsionales: fueron pedidos por el profesor.

## Edificio 2: meta de cierre

Solo despues de Edificio 1.

Sobre copia limpia del modelo activo probable:

```text
HECRAS2\Edif2\Edificio2_Estatico con carga sismica.EDB
```

Completar:

- auditoria base;
- revisar 130 losas vs 125 panos esperados;
- revisar `TEX/TEY/SDX/SDY`;
- revisar combos;
- correr analisis;
- exportar resultados;
- resolver fallbacks si ETABS 21.2.0 no expone tablas por COM;
- reporte final.

## Logs obligatorios

Mantener log vivo en:

```text
transfer/ws2-ed1-etabs21-context/reports/WS2_MODO_GOD_LOG_YYYYMMDD_HHMM.md
```

Reportes finales:

```text
transfer/ws2-ed1-etabs21-context/reports/WS2_ED1_PARTE1_FINAL_YYYYMMDD_HHMM.md
transfer/ws2-ed1-etabs21-context/reports/WS2_ED2_PARTE1_FINAL_YYYYMMDD_HHMM.md
```

Si hay bloqueo:

```text
transfer/ws2-ed1-etabs21-context/reports/WS2_BLOQUEO_DURO_YYYYMMDD_HHMM.md
```

## Definicion de terminado

Un edificio esta terminado solo si hay:

- modelo de trabajo guardado;
- cargas/mass source verificadas;
- casos/combinaciones verificadas;
- analisis corrido;
- tablas exportadas;
- resultados trazables;
- fuentes usadas y criterio documentado;
- reporte final;
- riesgos residuales identificados.

## Frase de ejecucion

No pidas permiso para cada paso. No te quedes solo diagnosticando. Itera hasta cerrar. Si falla, arregla. Si hay bloqueo duro, reporta.
