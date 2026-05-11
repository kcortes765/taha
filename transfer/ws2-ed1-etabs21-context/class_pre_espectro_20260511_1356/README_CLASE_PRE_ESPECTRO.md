# Carpeta clase previa al espectro

Fecha: 2026-05-11.

Objetivo: reunir copias separadas de los modelos para trabajar en clase hasta el estado inmediatamente anterior a aplicar el espectro sísmico.

## Regla crítica

Antes de abrir ETABS o usar OAPI/API:

```powershell
Get-Process ETABS -ErrorAction SilentlyContinue
```

Usar una sola instancia de ETABS 21 y un solo edificio activo a la vez.

## Estructura

- `Edificio_1\models`: modelo de Edificio 1 para clase.
- `Edificio_1\reports`: notas y verificación del estado del modelo.
- `Edificio_2\models`: modelo de Edificio 2 para clase.
- `Edificio_2\reports`: notas y verificación del estado del modelo.
- `evidencia`: tablas, capturas o comprobaciones asociadas.
- `scripts_usados`: scripts utilizados para preparar o auditar las copias.

## Qué significa "antes del espectro"

Para Edificio 1, significa dejar listo el modelo con geometría, materiales, secciones, cargas gravitacionales, diafragmas, fuente de masa y caso modal, pero sin casos espectrales `SEx`, `SEy`, `SEx_b2`, `SEy_b2` ni torsión accidental derivada del espectro.

Para Edificio 2, el flujo principal de Parte 1 es estático. Por eso el equivalente de clase es dejar geometría, materiales, secciones, cargas gravitacionales, diafragma, fuente de masa y modal auxiliar listos, antes de aplicar las fuerzas sísmicas estáticas `EX/EY` y torsión `TEX/TEY`.

## Nota

Esta carpeta no reemplaza los modelos finales auditados. Es una zona separada para preparar material de clase.
