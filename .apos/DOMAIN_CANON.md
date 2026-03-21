# DOMAIN CANON — ADSE 1S-2026

## Edificio 1 — Parámetros fijos
- 20 pisos, H1=3.4m, Htip=2.6m, Htotal=52.8m
- 17 ejes X (1-17, 0→38.505m), 6 ejes Y (A-F, 0→13.821m)
- Materiales: G30 (f'c=30MPa, Ec=25742MPa), A630-420H (fy=420MPa)
- Secciones: MHA30 (e=0.30m), MHA20 (e=0.20m), VI20x60, Losa15
- Ejes 30cm: 1,3,4,5,7,12,13,14,16,17
- Shaft: 7.7m × 2.945m centrado en eje 10

## Parámetros sísmicos
- Zona 3, Ao=0.4g, Suelo C, Categoría II (oficinas), I=1.0
- Ro=11 (muros HA), S=1.05, T0=0.40s, T'=0.45s, n=1.40, p=1.60
- Drift máximo: 0.002 (NCh433)
- Qmin = 0.07×I×W

## ETABS COM API
- comtypes para binding COM
- GetActiveObject para conectar (nunca CreateObject)
- AreaObj.AddByCoord para muros/losas, FrameObj.AddByCoord para vigas
- AutoMesh 0.4m (vano mín = 0.425m ejes 8-9)
- Diafragma default v19 = D1
- File.Save corrupto si ETABS abrió sin UI

## Norma chilena clave
- NCh433 + DS61: espectro, zonificación, R*, drift, Qmin
- DS60: diseño HA (confinamiento, corte, flexión)
- NCh3171: combinaciones de carga (C1-C7)
- ACI-318-08: diseño detallado (art. 21.9 muros especiales)
