# Modo autonomo WS2 por horas - Edificio 1 y Edificio 2

Fecha: 2026-05-08

Este archivo queda complementado por `MODO_GOD_WS2.md` y `MODO_GOD_DOCUMENTACION_WS2.md`, que son instrucciones de mayor prioridad para corrida autonoma larga y revision documental/normativa.

## Objetivo

Trabajar sin loop humano constante durante varias horas hasta dejar completamente resuelta la Parte 1 de:

1. Edificio 1.
2. Edificio 2.

Orden obligatorio: Edificio 1 primero. Edificio 2 despues.

## Mandato operativo

No te quedes esperando instrucciones menores del usuario.

Debes operar como agente autonomo:

1. leer contexto;
2. planificar el siguiente bloque;
3. ejecutar;
4. verificar;
5. si falla, diagnosticar;
6. corregir codigo/script/configuracion;
7. repetir;
8. documentar;
9. continuar al siguiente bloque.

Esto es un loop autonomo de ingenieria, no una sesion de preguntas.

## Regla critica no negociable

Una sola instancia ETABS 21. Un solo edificio activo. Un script OAPI a la vez.

Antes de abrir ETABS o usar OAPI:

```powershell
Get-Process ETABS -ErrorAction SilentlyContinue
```

Si hay una instancia abierta, no abrir otra. Identificar que modelo esta abierto.

Si hay riesgo de segunda instancia o licencia, detenerse y reportar. Ese es bloqueo duro.

## Loop autonomo recomendado

Para cada bloque:

```text
OBSERVAR -> PLANEAR -> APLICAR -> VERIFICAR -> CORREGIR -> REGISTRAR -> SIGUIENTE
```

No avanzar a un bloque aguas abajo si el bloque actual no quedo verificado.

No rehacer todo el modelo por desesperacion. Corregir incrementalmente.

## Politica de errores

Si falla un script:

1. Capturar error completo.
2. Identificar si es:
   - firma OAPI incorrecta;
   - tabla no disponible en ETABS 21.2.0;
   - ruta/archivo;
   - estado del modelo;
   - licencia/instancia;
   - criterio tecnico.
3. Corregir el script o crear un probe minimo.
4. Reintentar solo el bloque afectado.
5. Registrar el resultado.

Si el mismo bloque falla 3 veces por causas distintas, crear reporte de bloqueo y proponer workaround.

## Bloqueos duros: detener y reportar

Detenerse solo si ocurre alguno:

- aparece o se requiere segunda instancia ETABS;
- ETABS queda sin licencia;
- el `.EDB` no abre o queda corrupto;
- no existe backup/copia limpia;
- el modelo abierto no corresponde al edificio esperado;
- se detecta diferencia geometrica mayor no resoluble por codigo seguro;
- una decision normativa critica no esta en fuentes y no se puede inferir con seguridad;
- se requiere borrar o reconstruir geometria manual ya hecha por UI.

Fuera de esos casos, seguir iterando.

## Copias limpias obligatorias

Antes de modificar:

- backup del original;
- copia de trabajo fechada;
- registrar rutas exactas.

Nunca guardar cambios destructivos sobre el original.

## Edificio 1: cierre Parte 1

Modelo activo probable:

```text
HECRAS2\prog\Edif1\ED1_PARTE1_COMPLETA_TRABAJO.EDB
```

Trabajo esperado:

1. Re-auditar estado base en la copia limpia.
2. Preservar releases torsionales pedidos por el profesor.
3. Asignar diafragma `D1`.
4. Definir y aplicar cargas `PP/SCP/SCT/TERP/TERT`.
5. Definir mass source correcta.
6. Definir modal.
7. Definir espectral NCh433:2026.
8. Definir torsion accidental y combinaciones Ed.1.
9. Correr analisis.
10. Extraer tablas.
11. Verificar Parte 1 contra enunciado/material de apoyo.
12. Reportar resultados y riesgos residuales.

## Edificio 2: cierre Parte 1

Solo despues de Edificio 1 cerrado.

Modelo activo probable:

```text
HECRAS2\Edif2\Edificio2_Estatico con carga sismica.EDB
```

Trabajo esperado:

1. Crear backup/copia limpia.
2. Auditar 5 stories, grillas, frames, losas, diafragma, cargas, mass source y combos.
3. Revisar 130 losas vs canon nominal 125 panos.
4. Revisar `TEX/TEY/SDX/SDY`.
5. Revisar `Combo 1` a `Combo 19`.
6. Correr analisis si todo esta validado.
7. Extraer resultados.
8. Si COM no expone drifts/story forces, usar export UI o workaround documentado sin inventar resultados.

## Evidencia obligatoria

Crear reportes en:

```text
transfer/ws2-ed1-etabs21-context/reports/
```

Minimo:

```text
WS2_AUTONOMO_LOG_YYYYMMDD_HHMM.md
WS2_ED1_PARTE1_FINAL_YYYYMMDD_HHMM.md
WS2_ED2_PARTE1_FINAL_YYYYMMDD_HHMM.md
WS2_BLOQUEOS_SI_EXISTEN_YYYYMMDD_HHMM.md
```

Cada reporte debe incluir:

- ruta del `.EDB`;
- version/build ETABS;
- confirmacion de una sola instancia;
- scripts creados/modificados;
- cambios aplicados;
- tablas exportadas;
- resultados clave;
- fallas encontradas;
- correcciones realizadas;
- riesgos residuales;
- siguiente accion.

## Criterio de exito

Edificio queda cerrado solo si existe:

- modelo de trabajo guardado;
- cargas y mass source verificadas;
- casos/combinaciones verificadas;
- analisis corrido;
- tablas exportadas;
- reporte final trazable;
- lista de pendientes reducida a riesgos residuales no bloqueantes.

## Frase rectora

No preguntar por cada paso. Iterar con rigor. Si falla, corregir y reintentar. Si hay bloqueo duro, detener y reportar.
