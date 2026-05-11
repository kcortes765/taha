# WS2 APOS delta - guardar y transferencia Git clase pre-espectro

Fecha: 2026-05-11 14:24.

## Objetivo

Guardar en APOS y transferir al repositorio Git el estado completo útil para descargar desde laptop personal.

## Paquete agregado al repo

Carpeta:

`transfer\ws2-ed1-etabs21-context\class_pre_espectro_20260511_1356`

ZIP:

`transfer\ws2-ed1-etabs21-context\CLASS_PRE_ESPECTRO_20260511_1356.zip`

## Contenido incluido

- `ED1_CLASE_PRE_ESPECTRO_20260511.EDB`
- `ED2_CLASE_PRE_ESPECTRO_20260511.EDB`
- reportes JSON/MD de ambos modelos;
- log del pipeline ED2 pasos 1 a 8;
- resultados modales auxiliares ED2;
- scripts usados para preparar/guardar las copias;
- resumen operativo y README;
- manifiesto SHA256.

## Contenido excluido intencionalmente

No se versionaron temporales pesados de solver ETABS como `.Y00`, `.Y01`, `.K_0`, `.msh`, `.OUT` ni archivos equivalentes, porque no son necesarios para descargar/abrir las copias `.EDB` limpias de clase.

## Estado ETABS

Al momento del guardado había una sola instancia ETABS 21.2.0 respondiendo, con `ED2_CLASE_PRE_ESPECTRO_20260511` activo. No se abrió una segunda instancia.
