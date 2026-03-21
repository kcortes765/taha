# Feature R04 — Verificar fórmulas NCh433+DS61

## Estado: COMPLETADA ✅

## Resumen

Verificación exhaustiva de TODAS las fórmulas sísmicas contra las normas originales
(NCh433.Of1996 Mod.2009 y DS61-2011), con extracción directa del texto normativo
usando PyMuPDF.

## Hallazgos principales

### 1. Disputa R* — RESUELTA
- **Versión A es la CORRECTA**: R* = 1 + T*/(0.10·To + T*/Ro)
- Fuente: NCh433 Art. 6.3.5.3, Ecuación (10), pág. 39 del PDF
- La Versión B (R* = 1+(Ro-1)·T*/(0.10·To+T*)) NO aparece en la norma
- DS61 NO modificó la fórmula de R*

### 2. Fórmulas verificadas (10 fórmulas)
- α(T): denominador exponente 3 FIJO ✅
- R*: Ecuación (10) confirmada ✅
- Sa: S·α·I·Ao/R* ✅
- C: 2.75·S·Ao/(g·R)·(T'/T*)^n ✅ (S añadido por DS61)
- Cmín: S·Ao/(6·g) ✅
- Cmáx: 0.35·S·Ao/g para R=7 ✅
- Qo, Qmín, Qmáx ✅
- CQC con ξ=0.05 ✅

### 3. Valores numéricos calculados
- Cmín = 0.0700 → Qmín ≈ 656 tonf
- R*(T*=1.0) = 8.639
- R*(T*=1.3) = 9.218
- Cmín GOBIERNA para T* > ~0.8s (típico edificios altos muros HA)

### 4. Bugs encontrados en app-c1
- **CRÍTICO**: R* usa fórmula incorrecta (calculators.js:27, app.js:739)
  - App: R* = 1 + (Ro-1)·T/(0.1·Ro+T) — usa Ro en vez de To
  - NCh433: R* = 1 + T*/(0.10·To + T*/Ro)
  - Error ~33% en R* para T*=1.0s
- Posible inversión T0/T vs T/T0 en calcAlpha
- Pregunta questions.js:1039 con respuesta incorrecta (4.47 debería ser 4.2)

## Output generado
- `autonomo/research/formulas_verificadas.md` (~450 líneas, 13 secciones)

## Método de verificación
1. Extracción directa del PDF NCh433 usando PyMuPDF (fitz)
2. DS61 es PDF escaneado — verificación cruzada con apuntes y fuentes web
3. Cálculos numéricos independientes para confirmar coherencia
4. Comparación con implementaciones existentes (app-c1, GUIA, RESUMEN)

## Tiempo: ~30 min
