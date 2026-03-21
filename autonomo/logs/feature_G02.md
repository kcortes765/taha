# Feature G02 — Corregir guía: fórmulas R*, C, Cmín, Cmáx

**Estado**: COMPLETADA
**Fecha**: 2026-03-21
**Archivo editado**: `docs/estudio/GUIA-COMPLETA-EDIFICIO1-ETABS-v19.md`

## Hallazgo principal

Las fórmulas en la sección 11.5 ya estaban **correctas** (probablemente corregidas por G01).
El trabajo se enfocó en **mejorar claridad, coherencia y utilidad práctica**.

## Cambios realizados

### 1. Distinción n vs p (sección 11.5, después de fórmula C)
- Agregado callout de advertencia diferenciando n=1.40 (exponente de C, método estático)
  vs p=1.60 (exponente de α(T), espectro dinámico)
- Error frecuente de estudiantes: usar n donde va p o viceversa

### 2. Comportamiento límite de R* (sección 11.5, después de fórmula R*)
- Tabla con R* para T*→0, T*=To, T*=1.0, T*→∞
- Nota explicando por qué R* > R=7 es normal (Qmín controla)

### 3. Workflow ETABS mejorado (sección 11.5, procedimiento paso a paso)
- Reorganizado en 4 pasos claros (A-D) con rutas de menú ETABS
- Paso A: obtener T* del modal
- Paso B: calcular C y verificar límites (con 3 casos: Cmín/C/Cmáx)
- Paso C: calcular Qo y R*
- Paso D: verificar Qmín con resultados modales, incluye fórmula de escalamiento

### 4. Dos métodos ETABS para aplicar R* (sección 11.5)
- Método A: reducir SF del Load Case (9.81/R*)
- Método B (recomendado): mantener espectro elástico, reducir en combinaciones
- Sección separada de verificación Qmín obligatoria

### 5. Tabla resumen formato entregable (sección 11.5, nueva)
- Tabla completa con todos los parámetros para ambas direcciones (X, Y)
- Campos a completar: T*, R*, C, Cdiseño, P, Qo, Qbasal, Qmín, f_escala
- Formato listo para presentar al Prof. Music

### 6. Indicador R* biosísmico corregido (sección 11.7)
- Antes: "R* < R → se usa Cmáx, edificio más rígido que lo esperado" (impreciso)
- Ahora: interpretación completa para R*>R, R*≈R, R*<R con sus implicancias

## Verificación de coherencia

| Sección | Fórmula | Estado |
|---------|---------|--------|
| 7.2 (espectro) | α con p=1.60, denominador ^3 fijo | ✅ Correcto |
| 7.4 (Load Cases) | SF=9.81 con espectro en Sa/g | ✅ Coherente |
| 11.5 (corte basal) | R*, C, Cmín, Cmáx, cálculos numéricos | ✅ Correcto |
| 11.7 (biosísmico) | Indicador R* con interpretación | ✅ Corregido |

### Verificación numérica independiente
- α(T=0.35) = 2.7753 → guía: 2.7752 ✅
- α(T=1.00) = 1.2328 → guía: 1.2328 ✅
- R*(T*=1.0) = 8.639 ✅
- R*(T*=1.3) = 9.218 ✅
- Cmín = 0.0700 ✅
- Cmáx = 0.1470 ✅

## Nota sobre formulas_verificadas.md
La tabla de α (sección 2) del documento R04 tiene errores numéricos en algunos valores
intermedios (ej: (T/To)^p para T=1.0 dice 4.5571 pero el valor correcto es 4.332).
Las fórmulas TEXT son correctas; solo los cálculos tabulados tienen redondeo/error.
La GUÍA usa sus propios valores correctos, no los de esa tabla.
