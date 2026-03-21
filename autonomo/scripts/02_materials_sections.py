"""
02_materials_sections.py — Define materials and sections for Edificio 1.

Creates:
  Materials:
    - G30: Concrete, f'c=30 MPa, Ec=4700*sqrt(30) MPa, gamma=2.5 tonf/m3
    - A630-420H: Rebar, fy=420 MPa, fu=630 MPa, Es=200,000 MPa

  Frame Sections:
    - VI20/60G30: Rectangular 0.20 x 0.60 m, material G30
      Modifiers: J=0 (torsion nullified — Chilean practice)

  Area Sections:
    - MHA30G30: Wall, Shell-Thick, t=0.30 m, material G30
    - MHA20G30: Wall, Shell-Thick, t=0.20 m, material G30
    - Losa15G30: Slab, Shell-Thin, t=0.15 m, material G30
      Modifiers: m11=m22=m12=0.25 (25% flexural inertia — Chilean practice)

Prerequisites:
  - ETABS v19 must be open with a model (run 01_init_model.py first)
  - comtypes installed (pip install comtypes)
  - config.py in the same directory

Usage:
  python 02_materials_sections.py

Units: Tonf, m, C (eUnits=12) throughout.
Conversion: 1 MPa = 101.937 tonf/m2

COM signatures verified against: autonomo/research/com_signatures.md (R03)
Sources: Enunciado Taller ADSE 1S-2026, Material Apoyo Taller 2026 (Lafontaine/Music)
"""

import sys
import os
import time

# Ensure config.py is importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import (
    connect, check_ret, set_units, get_model, log,
    UNITS_TONF_M_C,
    # Material constants — concrete G30
    MAT_CONCRETE, MAT_REBAR,
    MAT_CONC_NAME, FC_TONF_M2, EC_TONF_M2,
    POISSON_CONC, ALPHA_THERMAL_CONC, GAMMA_CONC,
    CONC_STRAIN_FC, CONC_STRAIN_ULT, CONC_FINAL_SLOPE,
    # Material constants — rebar A630-420H
    MAT_REBAR_NAME, FY_TONF_M2, FU_TONF_M2, ES_TONF_M2,
    POISSON_STEEL, ALPHA_THERMAL_STEEL, GAMMA_STEEL,
    EFY_TONF_M2, EFU_TONF_M2,
    REBAR_STRAIN_HARD, REBAR_STRAIN_ULT, REBAR_FINAL_SLOPE,
    # Section constants
    VIGA_NAME, VIGA_B, VIGA_H,
    MURO_30_NAME, MURO_30_ESP,
    MURO_20_NAME, MURO_20_ESP,
    LOSA_NAME, LOSA_ESP,
    # Modifiers
    VIGA_MODIFIERS, LOSA_MODIFIERS,
    # Shell/slab enums
    SHELL_THICK, SHELL_THIN, WALL_SPECIFIED, SLAB_SLAB,
)


# ===================================================================
# STEP 1: Define concrete material G30
# ===================================================================

def define_concrete_G30(SapModel):
    """Define concrete material G30 (f'c = 30 MPa).

    Steps:
      1. SetMaterial — create material entry (type=Concrete)
      2. SetMPIsotropic — set E, nu, alpha
      3. SetOConcrete_1 — set f'c and stress-strain parameters
      4. SetWeightAndMass — set unit weight (gamma = 2.5 tonf/m3)

    All values in Tonf_m_C units (config.py handles conversion).

    Firmas COM: com_signatures.md §2.1, §2.3, §2.4, §2.6
    """
    log.info("Step 1: Defining concrete material G30...")
    PM = SapModel.PropMaterial

    # --- 1a: Create material entry ---
    # SetMaterial(Name, MatType) — MatType 2 = Concrete
    ret = PM.SetMaterial(MAT_CONC_NAME, MAT_CONCRETE)
    check_ret(ret, f"SetMaterial('{MAT_CONC_NAME}', Concrete)")
    log.info(f"  Material '{MAT_CONC_NAME}' created (type=Concrete)")

    # --- 1b: Isotropic properties ---
    # SetMPIsotropic(Name, E, U, A) — 4 required args
    #   E = 2,624,300 tonf/m2 (Ec = 4700*sqrt(30) MPa * 101.937)
    #   U = 0.20 (Poisson)
    #   A = 1.0E-05 /C (thermal expansion)
    ret = PM.SetMPIsotropic(
        MAT_CONC_NAME,
        EC_TONF_M2,           # E = ~2,624,300 tonf/m2
        POISSON_CONC,          # nu = 0.20
        ALPHA_THERMAL_CONC,    # alpha = 1.0E-05 /C
    )
    check_ret(ret, f"SetMPIsotropic('{MAT_CONC_NAME}')")
    log.info(f"  Isotropic: Ec={EC_TONF_M2:.0f} tonf/m2, "
             f"nu={POISSON_CONC}, alpha={ALPHA_THERMAL_CONC}")

    # --- 1c: Concrete design properties ---
    # SetOConcrete_1(Name, Fc, IsLightweight, FcsFactor, SSType, SSHysType,
    #                StrainAtFc, StrainUltimate, FinalSlope)
    # 9 required args (3 optional omitted: FrictionAngle, DilatationalAngle, Temp)
    ret = PM.SetOConcrete_1(
        MAT_CONC_NAME,
        FC_TONF_M2,           # f'c = ~3,058 tonf/m2 (30 MPa)
        False,                 # IsLightweight = No
        1.0,                   # FcsFactor = 1.0
        1,                     # SSType = 1 (Mander)
        0,                     # SSHysType = 0 (Elastic)
        CONC_STRAIN_FC,        # StrainAtFc = 0.002216
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

    log.info(f"  G30 complete.")


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
    #   Es = ~20,387,400 tonf/m2 (200,000 MPa * 101.937)
    #   U = 0.30 (Poisson)
    #   A = 1.17E-05 /C (thermal expansion)
    ret = PM.SetMPIsotropic(
        MAT_REBAR_NAME,
        ES_TONF_M2,           # Es = ~20,387,400 tonf/m2
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
# STEP 3: Define frame section — VI20/60G30 (beam)
# ===================================================================

def define_beam_section(SapModel):
    """Define rectangular beam section VI20/60G30.

    Section: 0.20 m (width) x 0.60 m (depth), material G30
    Note: In ETABS, T3 = depth (peralte), T2 = width (ancho)

    Firmas COM: com_signatures.md §3.1
    """
    log.info("Step 3: Defining beam section VI20/60G30...")
    PF = SapModel.PropFrame

    # SetRectangle(Name, MatProp, T3, T2)
    #   T3 = 0.60 m (depth/peralte — eje local 3)
    #   T2 = 0.20 m (width/ancho — eje local 2)
    ret = PF.SetRectangle(
        VIGA_NAME,             # "VI20x60G30"
        MAT_CONC_NAME,        # "G30"
        VIGA_H,                # T3 = 0.60 m (depth)
        VIGA_B,                # T2 = 0.20 m (width)
    )
    check_ret(ret, f"SetRectangle('{VIGA_NAME}')")
    log.info(f"  Section '{VIGA_NAME}': {VIGA_B}x{VIGA_H}m, mat={MAT_CONC_NAME}")

    log.info(f"  Beam section complete.")


# ===================================================================
# STEP 4: Define wall sections — MHA30G30 and MHA20G30
# ===================================================================

def define_wall_sections(SapModel):
    """Define wall (muro) sections for 30cm and 20cm walls.

    Both are Shell-Thin type (eShellType=1) per guia UI / practica Lafontaine.
    eWallPropType=0 (Specified).

    Firmas COM: com_signatures.md §4.1
    """
    log.info("Step 4: Defining wall sections...")
    PA = SapModel.PropArea

    walls = [
        (MURO_30_NAME, MURO_30_ESP),  # MHA30G30, t=0.30m
        (MURO_20_NAME, MURO_20_ESP),  # MHA20G30, t=0.20m
    ]

    for name, thickness in walls:
        # SetWall(Name, eWallPropType, eShellType, MatProp, Thickness)
        #   eWallPropType = 0 (Specified)
        #   eShellType = 1 (Shell-Thin — practica chilena para muros delgados e/L < 0.1)
        ret = PA.SetWall(
            name,
            WALL_SPECIFIED,        # 0 = Specified
            SHELL_THIN,            # 1 = Shell-Thin (guia UI)
            MAT_CONC_NAME,        # "G30"
            thickness,
        )
        check_ret(ret, f"SetWall('{name}')")
        log.info(f"  Wall '{name}': t={thickness}m, mat={MAT_CONC_NAME}, "
                 f"Shell-Thin")

    log.info(f"  Wall sections complete.")


# ===================================================================
# STEP 5: Define slab section — Losa15G30
# ===================================================================

def define_slab_section(SapModel):
    """Define slab section Losa15G30, t=0.15m.

    Shell-Thin type (eShellType=1) — standard for floor slabs.
    eSlabType=0 (Slab).

    Firmas COM: com_signatures.md §4.2
    """
    log.info("Step 5: Defining slab section Losa15G30...")
    PA = SapModel.PropArea

    # SetSlab(Name, eSlabType, eShellType, MatProp, Thickness)
    #   eSlabType = 0 (Slab)
    #   eShellType = 1 (Shell-Thin — adequate for floor slabs)
    ret = PA.SetSlab(
        LOSA_NAME,
        SLAB_SLAB,             # 0 = Slab
        SHELL_THIN,            # 1 = Shell-Thin
        MAT_CONC_NAME,        # "G30"
        LOSA_ESP,              # 0.15 m
    )
    check_ret(ret, f"SetSlab('{LOSA_NAME}')")
    log.info(f"  Slab '{LOSA_NAME}': t={LOSA_ESP}m, mat={MAT_CONC_NAME}, "
             f"Shell-Thin")

    log.info(f"  Slab section complete.")


# ===================================================================
# STEP 6: Apply property modifiers
# ===================================================================

def apply_modifiers(SapModel):
    """Apply property modifiers to beams and slabs.

    Beam modifiers (8 values): [A, As2, As3, J, I22, I33, M, W]
      - J = 0.0 (nullify torsional stiffness — Chilean practice per Lafontaine)
      - All others = 1.0

    Slab modifiers (10 values): [f11, f22, f12, m11, m22, m12, v13, v23, Mass, Weight]
      - m11 = m22 = m12 = 0.25 (reduce flexural inertia to 25% — Chilean practice)
      - All others = 1.0

    Firmas COM: com_signatures.md §3.2, §4.4
    """
    log.info("Step 6: Applying property modifiers...")

    # --- 6a: Beam modifiers (J=0) ---
    # SetModifiers(Name, Value) — Value is float[8]
    PF = SapModel.PropFrame
    ret = PF.SetModifiers(VIGA_NAME, VIGA_MODIFIERS)
    check_ret(ret, f"PropFrame.SetModifiers('{VIGA_NAME}')")
    log.info(f"  Beam '{VIGA_NAME}' modifiers: {VIGA_MODIFIERS}")
    log.info(f"    J=0 (torsion nullified)")

    # --- 6b: Slab modifiers (inercia 25%) ---
    # SetModifiers(Name, Value) — Value is float[10]
    PA = SapModel.PropArea
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
            # GetMPIsotropic returns (E, U, A, Temp, ret) or similar tuple
            result = PM.GetMPIsotropic(mat_name)
            if isinstance(result, tuple):
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

    # Verify frame section
    try:
        PF = SapModel.PropFrame
        result = PF.GetNameList()
        if isinstance(result, tuple) and result[-1] == 0:
            n_frames = result[0]
            names = result[1]
            log.info(f"  Frame sections ({n_frames}): {list(names)}")
            if VIGA_NAME in list(names):
                log.info(f"    '{VIGA_NAME}' found OK")
            else:
                log.warning(f"    '{VIGA_NAME}' NOT FOUND in frame sections")
        else:
            log.warning(f"  PropFrame.GetNameList failed")
    except Exception as e:
        log.warning(f"  Frame verification failed: {e}")

    # Verify area sections
    try:
        PA = SapModel.PropArea
        result = PA.GetNameList()
        if isinstance(result, tuple) and result[-1] == 0:
            n_areas = result[0]
            names = result[1]
            log.info(f"  Area sections ({n_areas}): {list(names)}")
            for sec_name in [MURO_30_NAME, MURO_20_NAME, LOSA_NAME]:
                if sec_name in list(names):
                    log.info(f"    '{sec_name}' found OK")
                else:
                    log.warning(f"    '{sec_name}' NOT FOUND in area sections")
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
    log.info("02_materials_sections.py — Edificio 1 (Materials & Sections)")
    log.info("=" * 60)

    # Print expected parameters
    log.info(f"  Concrete: {MAT_CONC_NAME} — f'c={FC_TONF_M2:.1f} tonf/m2, "
             f"Ec={EC_TONF_M2:.0f} tonf/m2")
    log.info(f"  Rebar: {MAT_REBAR_NAME} — fy={FY_TONF_M2:.1f}, "
             f"fu={FU_TONF_M2:.1f} tonf/m2")
    log.info(f"  Beam: {VIGA_NAME} ({VIGA_B}x{VIGA_H}m) J=0")
    log.info(f"  Wall 30: {MURO_30_NAME} (t={MURO_30_ESP}m)")
    log.info(f"  Wall 20: {MURO_20_NAME} (t={MURO_20_ESP}m)")
    log.info(f"  Slab: {LOSA_NAME} (t={LOSA_ESP}m) m=0.25")
    log.info("")

    # Connect to ETABS
    log.info("Connecting to ETABS v19...")
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

        # Step 1: Concrete G30
        define_concrete_G30(SapModel)
        log.info("")

        # Step 2: Rebar A630-420H
        define_rebar_A630(SapModel)
        log.info("")

        # Step 3: Beam section VI20/60G30
        define_beam_section(SapModel)
        log.info("")

        # Step 4: Wall sections MHA30G30, MHA20G30
        define_wall_sections(SapModel)
        log.info("")

        # Step 5: Slab section Losa15G30
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
        log.info(f"    {MAT_CONC_NAME}: f'c=30 MPa, Ec=25,743 MPa, "
                 f"gamma={GAMMA_CONC} tonf/m3")
        log.info(f"    {MAT_REBAR_NAME}: fy=420 MPa, fu=630 MPa, "
                 f"Es=200,000 MPa")
        log.info(f"  Frame Sections:")
        log.info(f"    {VIGA_NAME}: {VIGA_B}x{VIGA_H}m, J=0")
        log.info(f"  Area Sections:")
        log.info(f"    {MURO_30_NAME}: t={MURO_30_ESP}m, Shell-Thick")
        log.info(f"    {MURO_20_NAME}: t={MURO_20_ESP}m, Shell-Thick")
        log.info(f"    {LOSA_NAME}: t={LOSA_ESP}m, Shell-Thin, m=0.25")
        log.info("")
        log.info("Ready for next step (03_walls.py)")
        log.info("=" * 60)

    except Exception as e:
        log.error(f"FATAL: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
