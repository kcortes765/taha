# Contexto del Proyecto — Agente Autónomo ETABS

## Proyecto
Taller ADSE — UCN 1S-2026. Edificio 1: 20 pisos de muros HA en Antofagasta.
Prof. Juan Music Tomicic. Taller requiere modelación completa en ETABS v19.

## Objetivo del agente
Producir dos entregables PERFECTOS:
1. **Guía UI** — `docs/estudio/GUIA-COMPLETA-EDIFICIO1-ETABS-v19.md` (corregida y completa)
2. **Scripts API** — `autonomo/scripts/` (Python + comtypes, ETABS v19 OAPI)

## Datos clave del edificio
- 20 pisos, empotrado en base. Piso 1: h=3.40m, pisos 2-20: h=2.60m
- 17 ejes X + 6 ejes Y (grilla irregular)
- Antofagasta, Zona 3, Suelo C, Oficina (Cat. II)
- Hormigón G30 (f'c=30 MPa), Acero A630-420H (fy=420 MPa)
- Vigas invertidas 20/60 cm, muros 20 y 30 cm, losas 15 cm
- Shaft ascensor: 7.7 × 2.345 m
- Sobrecargas: oficinas 250, pasillos 500, techo 100 kgf/m²

## Parámetros sísmicos CONFIRMADOS (DS61 Tabla 12.3)
- Zona 3: Ao=0.4g | S=1.05 | To=0.40s | T'=0.45s | n=1.40 | p=1.60
- R=7, Ro=11 (muros HA) | I=1.0 (Cat. II)
- α(T) = [1 + 4.5·(T/To)^p] / [1 + (T/To)³] — denominador 3 FIJO
- Ec = 4700√30 = 25,743 MPa = 2,624,300 tonf/m² (factor ×101.937)

## Archivos del proyecto
```
docs/apuntes/INDICE.md          — Índice maestro de apuntes (LEER PRIMERO para temas)
docs/apuntes/*.pdf              — 14 PDFs temáticos del curso
docs/Enunciado Taller.pdf       — Enunciado oficial (14 páginas)
docs/Normas Utilizadas ADSE/    — NCh433, DS61, DS60, ACI318, NCh3171, NCh1537
docs/Material taller/           — Material Apoyo (47p), Lafontaine (143p), Manual v19 (239p)
docs/Diseño de Muros/           — 3 métodos + 2 ejemplos completos + guía ETABS
docs/Tablas/                    — Diagramas Pu-Mu muros y columnas
docs/estudio/GUIA-COMPLETA-*    — La guía que estamos perfeccionando
autonomo/scripts/               — Donde escribir los scripts API
autonomo/research/              — Donde escribir documentos de investigación
```

## Para scripts API — reglas estrictas
- Python 3.8+, comtypes para COM
- Compatible con ETABS v19 (CSI OAPI)
- NO inventar nombres de funciones API — investigar en documentación real
- Cada script debe ser autocontenido con docstring y manejo de errores
- Usar los nombres de sección del proyecto: MHA30G30, MHA20G30, VI20/60G30, Losa15G30
- Cargas: PP (SWM=1), TERP, TERT, SCP, SCT
- El pipeline debe ser modular (un script por fase)

## Lecciones COM aprendidas (de intentos anteriores)
1. comtypes.gen stale → limpiar ANTES de import
2. NUNCA Helper.CreateObject por defecto → instancias invisibles
3. Prioridad conexión: GetActiveObject → Helper.GetObject → CreateObject(visible)
4. Si nueva instancia: forzar obj.Visible=True + esperar 15s
5. File.Save() via COM produce .edb CORRUPTO si ETABS abrió sin UI
6. Separar pipeline en fases con sesiones COM independientes
7. Mantener helper/obj/model en globales del módulo (evitar GC)

## Prácticas ETABS chilenas (de Material Apoyo + Lafontaine)
- J=0 en vigas (torsion modifier)
- Inercia losa al 25% (m11, m22, m12 = 0.25)
- Cardinal Point vigas invertidas: Punto 2 (Bottom Center)
- Peso/área ≈ 1 tonf/m² como validación
- Espectro From File con Sa/g + SF=9.81
- AutoMesh = 0.4m (vano mínimo = 0.425m)
- Diafragma rígido (D1) para casos 1-3, semi-rígido para 4-6

## Normas clave y artículos
- NCh433 Mod 2009: espectro, corte basal, drift, torsión accidental
- DS61: Tabla 12.3 (S, To, T', n, p), fórmula α (Art. 12.2), R* (Art. 12.1)
- DS60: diseño HA, confinamiento, elementos de borde
- ACI318-08: diseño vigas, columnas, muros, nudo
- NCh3171: combinaciones de carga (7 combos)
- NCh1537: cargas permanentes y sobrecargas
