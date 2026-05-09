# Codigo incluido para WS2

Fecha: 2026-05-08

## Objetivo

Este paquete ahora incluye codigo local de referencia para Edificio 1 y Edificio 2. La carpeta `code/` estaba vacia en una version anterior del paquete; por eso se agrega explicitamente.

## Carpetas

### Edificio 1

```text
code/ed1_taller_etabs_legacy/
```

Origen local:

```text
C:\Seba\1° Sem. 2026 - UCN\taller-etabs
```

Uso:

- referencia historica de scripts ETABS para Edificio 1;
- contiene firmas OAPI, configuracion, cargas, casos, torsion, resultados y notas;
- no ejecutar `run_all.py` directamente sobre el modelo WS2 sin auditoria;
- parte del codigo nacio en flujo ETABS 19/generacion desde cero, por lo que debe adaptarse a ETABS 21 y al `.EDB` ya modelado por UI.

### Edificio 2

```text
code/ed2_pipeline_active/
```

Origen local:

```text
C:\Seba\1° Sem. 2026 - UCN\autonomo\scripts\ed2
```

Uso:

- referencia activa para Edificio 2;
- contiene pipeline, configuracion, diagnosticos y herramientas;
- no correr hasta cerrar Edificio 1 Parte 1;
- antes de correr, auditar el `.EDB` activo de Edificio 2 en `HECRAS2`.

## Archivos excluidos

Se excluyeron elementos generados o no necesarios para ejecutar codigo:

- `__pycache__`
- `*.pyc`
- `*.log`
- `*.zip`
- grandes carpetas historicas de resultados/transferencia de Edificio 2
- `.git` anidado de `taller-etabs`

## Regla de ejecucion

La IA de WS2 debe tratar este codigo como base de adaptacion, no como verdad final.

Primero:

1. leer contexto;
2. auditar el modelo real por OAPI;
3. crear copia limpia de trabajo;
4. adaptar script incremental;
5. aplicar un bloque a la vez;
6. verificar con tablas;
7. guardar reporte.

