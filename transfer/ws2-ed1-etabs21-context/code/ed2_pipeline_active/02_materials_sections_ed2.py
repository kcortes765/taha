"""
02_materials_sections_ed2.py — Define materials and sections for Edificio 2.

Creates:
  Materials:
    - G25: Concrete, f'c=25 MPa, Ec=4700*sqrt(25)=23500 MPa, gamma=2.5 tonf/m3
    - A630-420H: Rebar, fy=420 MPa, fu=630 MPa, Es=210,000 MPa

  Frame Sections:
    - C70x70G25: Rectangular 0.70x0.70 m, material G25 (P1-P2)
    - C65x65G25: Rectangular 0.65x0.65 m, material G25 (P3-P5)
    - V50x70G25: Rectangular 0.50x0.70 m, material G25 (P1-P2)
    - V45x70G25: Rectangular 0.45x0.70 m, material G25 (P3-P5)

  Area Sections:
    - L17G25: Slab, Shell-Thin, t=0.17 m, material G25

  Property Modifiers (ACI318):
    - Columnas (ambas): I22=I33=0.70
    - Vigas (ambas): I22=I33=0.35, J=0 (practica chilena)
    - Losa: m11=m22=m12=0.25 (inercia flexural 25%)

  NOTA: Ed.2 NO tiene muros (Shell-Wall). Solo frames y slab.

Prerequisites:
  - ETABS (v19/v21) must be open with a model (run 01_init_model_ed2.py first)
  - comtypes installed (pip install comtypes)
  - config_ed2.py in the same directory

Usage:
  python 02_materials_sections_ed2.py

Units: Tonf, m, C (eUnits=12) throughout.
Conversion: 1 MPa = 101.937 tonf/m2

COM signatures verified against: autonomo/research/com_signatures.md (R03)
Sources: Enunciado Taller ADSE 1S-2026, Material Apoyo Taller 2026 (Lafontaine/Music)
"""

import sys
import os

# Ensure config_ed2.py is importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config_ed2 import (
    connect, check_ret, set_units, log,
    UNITS_TONF_M_C,
    # Material constants — concrete G25
    MAT_CONCRETE, MAT_REBAR,
    MAT_CONC_NAME, FC_TONF_M2, EC_TONF_M2,
    POISSON_CONC, ALPHA_THERMAL_CONC, GAMMA_CONC,
    CONC_STRAIN_FC, CONC_STRAIN_ULT, CONC_FINAL_SLOPE,
    # Material constants — rebar A630-420H
    MAT_REBAR_NAME, FY_TONF_M2, FU_TONF_M2, ES_TONF_M2,
    POISSON_STEEL, ALPHA_THERMAL_STEEL, GAMMA_STEEL,
    EFY_TONF_M2, EFU_TONF_M2,
    REBAR_STRAIN_HARD, REBAR_STRAIN_ULT, REBAR_FINAL_SLOPE,
    # Section constants — columns
    COL_70_NAME, COL_70_B, COL_70_H,
    COL_65_NAME, COL_65_B, COL_65_H,
    # Section constants — beams
    VIGA_50_NAME, VIGA_50_B, VIGA_50_H,
    VIGA_45_NAME, VIGA_45_B, VIGA_45_H,
    # Section constants — slab
    LOSA_NAME, LOSA_ESP,
    # Modifiers
    COL_MODIFIERS, VIGA_MODIFIERS, LOSA_MODIFIERS,
    # Shell/slab enums
    SHELL_THIN, SLAB_SLAB,
)


# ===================================================================
# STEP 1: Define concrete material G25
# ===================================================================

def define_concrete_G25(SapModel):
    """Define concrete material G25 (f'c = 25 MPa).

    Steps:
      1. SetMaterial — create material entry (type=Concrete)
      2. SetMPIsotropic — set E, nu, alpha
      3. SetOConcrete_1 — set f'c and stress-strain parameters
      4. SetWeightAndMass — set unit weight (gamma = 2.5 tonf/m3)

    All values in Tonf_m_C units (config_ed2.py handles conversion).

    Firmas COM: com_signatures.md §2.1, §2.3, §2.4, §2.6
    """
    log.info("Step 1: Defining concrete material G25...")
    PM = SapModel.PropMaterial

    # --- 1a: Create material entry ---
    # SetMaterial(Name, MatType) — MatType 2 = Concrete
    ret = PM.SetMaterial(MAT_CONC_NAME, MAT_CONCRETE)
    check_ret(ret, f"SetMaterial('{MAT_CONC_NAME}', Concrete)")
    log.info(f"  Material '{MAT_CONC_NAME}' created (type=Concrete)")

    # --- 1b: Isotropic properties ---
    # SetMPIsotropic(Name, E, U, A) — 4 required args
    #   E = 2,395,520 tonf/m2 (Ec = 4700*sqrt(25) MPa * 101.937)
    #   U = 0.20 (Poisson)
    #   A = 1.0E-05 /C (thermal expansion)
    ret = PM.SetMPIsotropic(
        MAT_CONC_NAME,
        EC_TONF_M2,           # E = ~2,395,520 tonf/m2
        POISSON_CONC,          # nu = 0.20
        ALPHA_THERMAL_CONC,    # alpha = 1.0E-05 /C
    )
    check_ret(ret, f"SetMPIsotropic('{MAT_CONC_NAME}')")
    log.info(f"  Isotropic: Ec={EC_TONF_M2:.0f} tonf/m2, "
             f"nu={POISSON_CONC}, alpha={ALPHA_THERMAL_CONC}")

    # --- 1c: Concrete design properties ---
    # SetOConcrete_1(Name, Fc, IsLightweight, FcsFactor, SSType, SSHysType,
    #                StrainAtFc, StrainUltimate, FinalSlope)
    # 9 required args
    ret = PM.SetOConcrete_1(
        MAT_CONC_NAME,
        FC_TONF_M2,           # f'c = ~2,548 tonf/m2 (25 MPa)
        False,                 # IsLightweight = No
        1.0,                   # FcsFactor = 1.0
        1,                     # SSType = 1 (Mander)
        0,                     # SSHysType = 0 (Elastic)
        CONC_STRAIN_FC,        # StrainAtFc = 0.002
        CONC_STRAIN_ULT,       # StrainUltimate = 0.005
        CONC_FINAL_SLOPE,      # FinalSlope = -0.1
    )
    check_ret(ret, f"SetOConcrete_1('{MAT_CONC_NAME}')")
    log.info(f"  Concrete: f'c={FC_TONF_M2:.1f} tonf/m2, "
             f"eps_fc={CONC_STRAIN_FC}, eps_u={CONC_STRAIN_ULT}")

    # --- 1d: Unit weight ---
    # SetWeightAndMass(Name, MyOption, Value) — MyOption 1 = Weight per unit volume
    ret = PM.SetWeightAndMass(MAT_CONC_NAME, 1, GAMMA_CONC)
    check_ret(ret, f"SetWeightAndMass('{MAT_CONC_NAME}')")
    log.info(f"  Weight: gamma={GAMMA_CONC} tonf/m3")

    log.info(f"  G25 complete.")


# ===================================================================
# STEP 2: Define rebar material A630-420H
# ===================================================================

def define_rebar_A630(SapModel):
    """Define rebar material A630-420H (fy = 420 MPa).

    Steps:
      1. SetMaterial — create material entry (type=Rebar)
      2. SetMPIsotropic — set Es, nu, alpha
      3. SetORebar_1 — set fy, fu, expected values, strain parameters
      4. SetWeightAndMass — set unit weight (gamma = 7.85 tonf/m3)

    Firmas COM: com_signatures.md §2.1, §2.3, §2.5, §2.6
    """
    log.info("Step 2: Defining rebar material A630-420H...")
    PM = SapModel.PropMaterial

    # --- 2a: Create material entry ---
    # SetMaterial(Name, MatType) — MatType 6 = Rebar
    ret = PM.SetMaterial(MAT_REBAR_NAME, MAT_REBAR)
    check_ret(ret, f"SetMaterial('{MAT_REBAR_NAME}', Rebar)")
    log.info(f"  Material '{MAT_REBAR_NAME}' created (type=Rebar)")

    # --- 2b: Isotropic properties ---
    # SetMPIsotropic(Name, E, U, A)
    #   Es = ~21,406,770 tonf/m2 (210,000 MPa * 101.937)
    #   U = 0.30 (Poisson)
    #   A = 1.17E-05 /C (thermal expansion)
    ret = PM.SetMPIsotropic(
        MAT_REBAR_NAME,
        ES_TONF_M2,           # Es = ~21,406,770 tonf/m2
        POISSON_STEEL,         # nu = 0.30
        ALPHA_THERMAL_STEEL,   # alpha = 1.17E-05 /C
    )
    check_ret(ret, f"SetMPIsotropic('{MAT_REBAR_NAME}')")
    log.info(f"  Isotropic: Es={ES_TONF_M2:.0f} tonf/m2, "
             f"nu={POISSON_STEEL}, alpha={ALPHA_THERMAL_STEEL}")

    # --- 2c: Rebar design properties ---
    # SetORebar_1(Name, Fy, Fu, EFy, EFu, SSType, SSHysType,
    #             StrainAtHardening, StrainUltimate, FinalSlope,
    #             UseCaltransDefaults)
    # All 11 args required
    ret = PM.SetORebar_1(
        MAT_REBAR_NAME,
        FY_TONF_M2,           # fy = ~42,814 tonf/m2 (420 MPa)
        FU_TONF_M2,           # fu = ~64,220 tonf/m2 (630 MPa)
        EFY_TONF_M2,          # Expected fy = fy * 1.17
        EFU_TONF_M2,          # Expected fu = fu * 1.08
        1,                     # SSType = 1 (Park)
        0,                     # SSHysType = 0 (Elastic)
        REBAR_STRAIN_HARD,     # StrainAtHardening = 0.01
        REBAR_STRAIN_ULT,      # StrainUltimate = 0.09
        REBAR_FINAL_SLOPE,     # FinalSlope = -0.1
        False,                 # UseCaltransDefaults = No
    )
    check_ret(ret, f"SetORebar_1('{MAT_REBAR_NAME}')")
    log.info(f"  Rebar: fy={FY_TONF_M2:.1f}, fu={FU_TONF_M2:.1f} tonf/m2")
    log.info(f"  Expected: Efy={EFY_TONF_M2:.1f}, Efu={EFU_TONF_M2:.1f} tonf/m2")

    # --- 2d: Unit weight ---
    ret = PM.SetWeightAndMass(MAT_REBAR_NAME, 1, GAMMA_STEEL)
    check_ret(ret, f"SetWeightAndMass('{MAT_REBAR_NAME}')")
    log.info(f"  Weight: gamma={GAMMA_STEEL} tonf/m3")

    log.info(f"  A630-420H complete.")


# ===================================================================
# STEP 3: Define column sections — C70x70G25 and C65x65G25
# ===================================================================

def define_column_sections(SapModel):
    """Define rectangular column sections for both story groups.

    - C70x70G25: 0.70 x 0.70 m (P1-P2)
    - C65x65G25: 0.65 x 0.65 m (P3-P5)

    In ETABS: T3 = depth, T2 = width (both equal for square columns)

    Firmas COM: com_signatures.md §3.1
    """
    log.info("Step 3: Defining column sections...")
    PF = SapModel.PropFrame

    columns = [
        (COL_70_NAME, COL_70_H, COL_70_B),  # C70x70G25, T3=0.70, T2=0.70
        (COL_65_NAME, COL_65_H, COL_65_B),  # C65x65G25, T3=0.65, T2=0.65
    ]

    for name, depth, width in columns:
        # SetRectangle(Name, MatProp, T3, T2)
        ret = PF.SetRectangle(
            name,
            MAT_CONC_NAME,    # "G25"
            depth,             # T3 (depth)
            width,             # T2 (width)
        )
        check_ret(ret, f"SetRectangle('{name}')")
        log.info(f"  Column '{name}': {width}x{depth}m, mat={MAT_CONC_NAME}")

    log.info(f"  Column sections complete.")


# ===================================================================
# STEP 4: Define beam sections — V50x70G25 and V45x70G25
# ===================================================================

def define_beam_sections(SapModel):
    """Define rectangular beam sections for both story groups.

    - V50x70G25: 0.50 x 0.70 m (P1-P2)
    - V45x70G25: 0.45 x 0.70 m (P3-P5)

    In ETABS: T3 = depth (peralte), T2 = width (ancho)
    Vigas Ed.2 son normales (NO invertidas), cardinal point = centroide.

    Firmas COM: com_signatures.md §3.1
    """
    log.info("Step 4: Defining beam sections...")
    PF = SapModel.PropFrame

    beams = [
        (VIGA_50_NAME, VIGA_50_H, VIGA_50_B),  # V50x70G25, T3=0.70, T2=0.50
        (VIGA_45_NAME, VIGA_45_H, VIGA_45_B),  # V45x70G25, T3=0.70, T2=0.45
    ]

    for name, depth, width in beams:
        # SetRectangle(Name, MatProp, T3, T2)
        ret = PF.SetRectangle(
            name,
            MAT_CONC_NAME,    # "G25"
            depth,             # T3 = 0.70 m (depth)
            width,             # T2 = 0.50 or 0.45 m (width)
        )
        check_ret(ret, f"SetRectangle('{name}')")
        log.info(f"  Beam '{name}': {width}x{depth}m, mat={MAT_CONC_NAME}")

    log.info(f"  Beam sections complete.")


# ===================================================================
# STEP 5: Define slab section — L17G25
# ===================================================================

def define_slab_section(SapModel):
    """Define slab section L17G25, t=0.17m.

    Shell-Thin type (eShellType=1) — standard for floor slabs.
    eSlabType=0 (Slab).

    Firmas COM: com_signatures.md §4.2
    """
    log.info("Step 5: Defining slab section L17G25...")
    PA = SapModel.PropArea

    # SetSlab(Name, eSlabType, eShellType, MatProp, Thickness)
    #   eSlabType = 0 (Slab)
    #   eShellType = 1 (Shell-Thin — adequate for floor slabs)
    ret = PA.SetSlab(
        LOSA_NAME,
        SLAB_SLAB,             # 0 = Slab
        SHELL_THIN,            # 1 = Shell-Thin
        MAT_CONC_NAME,        # "G25"
        LOSA_ESP,              # 0.17 m
    )
    check_ret(ret, f"SetSlab('{LOSA_NAME}')")
    log.info(f"  Slab '{LOSA_NAME}': t={LOSA_ESP}m, mat={MAT_CONC_NAME}, "
             f"Shell-Thin")

    log.info(f"  Slab section complete.")


# ===================================================================
# STEP 6: Apply property modifiers
# ===================================================================

def apply_modifiers(SapModel):
    """Apply property modifiers to columns, beams, and slabs.

    Column modifiers (8 values): [A, As2, As3, J, I22, I33, M, W]
      - I22 = I33 = 0.70 (ACI318 Table 6.6.3.1.1(a))
      - All others = 1.0

    Beam modifiers (8 values): [A, As2, As3, J, I22, I33, M, W]
      - J = 0.0 (nullify torsional stiffness — Chilean practice per Lafontaine)
      - I22 = I33 = 0.35 (ACI318)
      - All others = 1.0

    Slab modifiers (10 values): [f11, f22, f12, m11, m22, m12, v13, v23, Mass, Weight]
      - m11 = m22 = m12 = 0.25 (reduce flexural inertia to 25% — Chilean practice)
      - All others = 1.0

    Firmas COM: com_signatures.md §3.2, §4.4
    """
    log.info("Step 6: Applying property modifiers...")

    PF = SapModel.PropFrame
    PA = SapModel.PropArea

    # --- 6a: Column modifiers (I22=I33=0.70) ---
    for col_name in [COL_70_NAME, COL_65_NAME]:
        ret = PF.SetModifiers(col_name, COL_MODIFIERS)
        check_ret(ret, f"PropFrame.SetModifiers('{col_name}')")
        log.info(f"  Column '{col_name}' modifiers: {COL_MODIFIERS}")
        log.info(f"    I22=I33=0.70 (ACI318)")

    # --- 6b: Beam modifiers (J=0, I22=I33=0.35) ---
    for viga_name in [VIGA_50_NAME, VIGA_45_NAME]:
        ret = PF.SetModifiers(viga_name, VIGA_MODIFIERS)
        check_ret(ret, f"PropFrame.SetModifiers('{viga_name}')")
        log.info(f"  Beam '{viga_name}' modifiers: {VIGA_MODIFIERS}")
        log.info(f"    J=0 (torsion nullified), I22=I33=0.35")

    # --- 6c: Slab modifiers (inercia 25%) ---
    ret = PA.SetModifiers(LOSA_NAME, LOSA_MODIFIERS)
    check_ret(ret, f"PropArea.SetModifiers('{LOSA_NAME}')")
    log.info(f"  Slab '{LOSA_NAME}' modifiers: {LOSA_MODIFIERS}")
    log.info(f"    m11=m22=m12=0.25 (flexural inertia 25%)")

    log.info(f"  Modifiers complete.")


# ===================================================================
# STEP 7: Verify definitions
# ===================================================================

def verify_materials(SapModel):
    """Verify that materials were created correctly."""
    log.info("Step 7a: Verifying materials...")
    PM = SapModel.PropMaterial

    for mat_name in [MAT_CONC_NAME, MAT_REBAR_NAME]:
        try:
            result = PM.GetMPIsotropic(mat_name)
            if isinstance(result, (tuple, list)):
                ret_code = result[-1]
                if ret_code == 0:
                    E = result[0]
                    nu = result[1]
                    log.info(f"  {mat_name}: E={E:.0f} tonf/m2, nu={nu}")
                else:
                    log.warning(f"  {mat_name}: GetMPIsotropic ret={ret_code}")
            else:
                log.info(f"  {mat_name}: exists (return type: {type(result)})")
        except Exception as e:
            log.warning(f"  {mat_name}: verification failed: {e}")


def verify_sections(SapModel):
    """Verify that sections were created correctly."""
    log.info("Step 7b: Verifying sections...")

    # Verify frame sections
    try:
        PF = SapModel.PropFrame
        result = PF.GetNameList()
        if isinstance(result, (tuple, list)) and result[-1] == 0:
            n_frames = result[0]
            names = result[1]
            log.info(f"  Frame sections ({n_frames}): {list(names)}")
            for sec_name in [COL_70_NAME, COL_65_NAME, VIGA_50_NAME, VIGA_45_NAME]:
                if sec_name in list(names):
                    log.info(f"    '{sec_name}' found OK")
                else:
                    log.warning(f"    '{sec_name}' NOT FOUND in frame sections")
        else:
            log.warning(f"  PropFrame.GetNameList failed")
    except Exception as e:
        log.warning(f"  Frame verification failed: {e}")

    # Verify area sections
    try:
        PA = SapModel.PropArea
        result = PA.GetNameList()
        if isinstance(result, (tuple, list)) and result[-1] == 0:
            n_areas = result[0]
            names = result[1]
            log.info(f"  Area sections ({n_areas}): {list(names)}")
            if LOSA_NAME in list(names):
                log.info(f"    '{LOSA_NAME}' found OK")
            else:
                log.warning(f"    '{LOSA_NAME}' NOT FOUND in area sections")
        else:
            log.warning(f"  PropArea.GetNameList failed")
    except Exception as e:
        log.warning(f"  Area verification failed: {e}")


# ===================================================================
# MAIN
# ===================================================================

def main():
    """Main entry point: define materials, sections, and modifiers."""
    log.info("=" * 60)
    log.info("02_materials_sections_ed2.py — Edificio 2 (Materials & Sections)")
    log.info("=" * 60)

    # Print expected parameters
    log.info(f"  Concrete: {MAT_CONC_NAME} — f'c={FC_TONF_M2:.1f} tonf/m2, "
             f"Ec={EC_TONF_M2:.0f} tonf/m2")
    log.info(f"  Rebar: {MAT_REBAR_NAME} — fy={FY_TONF_M2:.1f}, "
             f"fu={FU_TONF_M2:.1f} tonf/m2")
    log.info(f"  Col P1-2: {COL_70_NAME} ({COL_70_B}x{COL_70_H}m) I=0.70")
    log.info(f"  Col P3-5: {COL_65_NAME} ({COL_65_B}x{COL_65_H}m) I=0.70")
    log.info(f"  Beam P1-2: {VIGA_50_NAME} ({VIGA_50_B}x{VIGA_50_H}m) J=0, I=0.35")
    log.info(f"  Beam P3-5: {VIGA_45_NAME} ({VIGA_45_B}x{VIGA_45_H}m) J=0, I=0.35")
    log.info(f"  Slab: {LOSA_NAME} (t={LOSA_ESP}m) m=0.25")
    log.info("")

    # Connect to ETABS
    log.info("Connecting to ETABS...")
    try:
        SapModel = connect()
    except ConnectionError as e:
        log.error(str(e))
        sys.exit(1)
    except ImportError:
        log.error("comtypes not installed — run: pip install comtypes")
        sys.exit(1)

    try:
        # Ensure correct units
        set_units(UNITS_TONF_M_C)
        log.info(f"  Units set to Tonf_m_C (={UNITS_TONF_M_C})")
        log.info("")

        # Step 1: Concrete G25
        define_concrete_G25(SapModel)
        log.info("")

        # Step 2: Rebar A630-420H
        define_rebar_A630(SapModel)
        log.info("")

        # Step 3: Column sections C70x70G25, C65x65G25
        define_column_sections(SapModel)
        log.info("")

        # Step 4: Beam sections V50x70G25, V45x70G25
        define_beam_sections(SapModel)
        log.info("")

        # Step 5: Slab section L17G25
        define_slab_section(SapModel)
        log.info("")

        # Step 6: Property modifiers
        apply_modifiers(SapModel)
        log.info("")

        # Step 7: Verify
        verify_materials(SapModel)
        verify_sections(SapModel)
        log.info("")

        # Refresh view
        try:
            SapModel.View.RefreshView(0, False)
        except Exception:
            pass

        # Summary
        log.info("=" * 60)
        log.info("SUMMARY")
        log.info("=" * 60)
        log.info(f"  Materials:")
        log.info(f"    {MAT_CONC_NAME}: f'c=25 MPa, Ec=23,500 MPa, "
                 f"gamma={GAMMA_CONC} tonf/m3")
        log.info(f"    {MAT_REBAR_NAME}: fy=420 MPa, fu=630 MPa, "
                 f"Es=210,000 MPa")
        log.info(f"  Frame Sections:")
        log.info(f"    {COL_70_NAME}: {COL_70_B}x{COL_70_H}m, I22=I33=0.70 (P1-P2)")
        log.info(f"    {COL_65_NAME}: {COL_65_B}x{COL_65_H}m, I22=I33=0.70 (P3-P5)")
        log.info(f"    {VIGA_50_NAME}: {VIGA_50_B}x{VIGA_50_H}m, J=0, I=0.35 (P1-P2)")
        log.info(f"    {VIGA_45_NAME}: {VIGA_45_B}x{VIGA_45_H}m, J=0, I=0.35 (P3-P5)")
        log.info(f"  Area Sections:")
        log.info(f"    {LOSA_NAME}: t={LOSA_ESP}m, Shell-Thin, m=0.25")
        log.info("")
        log.info("Ready for next step (03_columns_ed2.py)")
        log.info("=" * 60)

    except Exception as e:
        log.error(f"FATAL: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
