"""
Generador del espectro elastico NCh433/DS61
Zona 3, Suelo C - Edificio 1 Taller ADSE UCN 1S-2026

Parametros DS61 Tabla 12.3:
  Ao = 0.4g, S = 1.05, To = 0.40s, T' = 0.45s, n = 1.40, p = 1.60

Formula DS61 Art. 12.2:
  alpha(T) = [1 + 4.5*(T/To)^p] / [1 + (T/To)^3]
  Sa = S * Ao * alpha  (en g)
"""

import os
import math

Ao = 0.4
S = 1.05
To = 0.40
p = 1.60
g_ms2 = 9.81

def alpha(T):
    if T == 0:
        return 1.0
    ratio = T / To
    return (1.0 + 4.5 * (ratio ** p)) / (1.0 + (ratio ** 3))

data = []
for i in range(101):
    T = round(i * 0.05, 2)
    a = alpha(T)
    Sa_g = S * Ao * a
    Sa_ms2 = Sa_g * g_ms2
    data.append((T, a, Sa_ms2, Sa_g))

peak = max(data, key=lambda x: x[1])
print("Pico: alpha={:.4f} en T={:.2f}s".format(peak[1], peak[0]))
print("Sa_max/g = {:.4f}".format(S * Ao * peak[1]))
print("Sa_max(m/s2) = {:.4f}".format(S * Ao * g_ms2 * peak[1]))
print()

print("Puntos clave:")
for T, a, Sa_ms2, Sa_g in data:
    if T in [0.0, 0.10, 0.20, 0.30, 0.35, 0.40, 0.50, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0]:
        print("  T={:5.2f}  alpha={:7.4f}  Sa={:7.4f} m/s2  Sa/g={:7.4f}".format(T, a, Sa_ms2, Sa_g))

script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(script_dir)

txt_path = os.path.join(script_dir, "espectro_elastico_Z3SC.txt")
with open(txt_path, "w") as f:
    for T, a, Sa_ms2, Sa_g in data:
        f.write("{:.2f}\t{:.6f}\n".format(T, Sa_g))
print("\nArchivo ETABS: {}".format(txt_path))

md_path = os.path.join(base_dir, "research", "espectro_tabla_completa.md")
with open(md_path, "w", encoding="utf-8") as f:
    f.write("# Espectro Elastico - Zona 3, Suelo C (DS61)\n\n")
    f.write("## Parametros\n\n")
    f.write("| Parametro | Valor | Fuente |\n")
    f.write("|-----------|-------|--------|\n")
    f.write("| Ao | 0.4g | NCh433, Zona 3 |\n")
    f.write("| S | 1.05 | DS61 Tabla 12.3 (Suelo C) |\n")
    f.write("| To | 0.40 s | DS61 Tabla 12.3 (Suelo C) |\n")
    f.write("| T' | 0.45 s | DS61 Tabla 12.3 (Suelo C) |\n")
    f.write("| n | 1.40 | DS61 Tabla 12.3 (Suelo C) |\n")
    f.write("| p | 1.60 | DS61 Tabla 12.3 (Suelo C) |\n\n")
    f.write("## Formula\n\n")
    f.write("```\n")
    f.write("alpha(T) = [1 + 4.5*(T/To)^p] / [1 + (T/To)^3]\n")
    f.write("Sa = S * Ao * alpha  (en unidades de g)\n")
    f.write("Sa(m/s2) = Sa/g * 9.81\n")
    f.write("```\n\n")
    f.write("## Pico del espectro\n\n")
    f.write("- alpha_max = {:.4f} en T = {:.2f} s\n".format(peak[1], peak[0]))
    f.write("- Sa_max/g = {:.4f}\n".format(S * Ao * peak[1]))
    f.write("- Sa_max = {:.4f} m/s2\n\n".format(S * Ao * g_ms2 * peak[1]))
    f.write("## Tabla Completa (T = 0.00 a 5.00 s, paso 0.05 s)\n\n")
    f.write("| T (s) | alpha | Sa (m/s2) | Sa/g |\n")
    f.write("|------:|------:|----------:|-----:|\n")
    for T, a, Sa_ms2, Sa_g in data:
        f.write("| {:.2f} | {:.4f} | {:.4f} | {:.4f} |\n".format(T, a, Sa_ms2, Sa_g))
    f.write("\n## Uso en ETABS\n\n")
    f.write("1. Archivo de entrada: `espectro_elastico_Z3SC.txt` (2 columnas: T, Sa/g)\n")
    f.write("2. Define > Functions > Response Spectrum > From File\n")
    f.write("3. Seleccionar el archivo .txt\n")
    f.write("4. Scale Factor = 9.81 (convierte Sa/g a m/s2)\n")
    f.write("5. Damping = 5%\n")
    f.write("6. Usar en Load Cases SEx y SEy\n")

print("Tabla MD: {}".format(md_path))
print("\nListo!")
