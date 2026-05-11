# Edificio 1 Parte 1 prog2 - setup

- Fecha: 2026-05-08 22:26:19
- Modelo: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif1\models\ED1_PARTE1_WS2_PROG2_20260508_2213.EDB`
- Log: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif1\logs\ed1_setup_20260508_2226.log`
- JSON: `C:\Users\Civil\Documents\Rio mapocho (no borrar por favor)\HECRAS2\prog2\Edif1\logs\ed1_setup_20260508_2226.json`

## Estado

Trabajo ejecutado sobre copia en `prog2`, no sobre el EDB vivo original.
No se modificaron releases de vigas.

## Resumen JSON

```json
{
  "phase": "setup",
  "model_path": "C:\\Users\\Civil\\Documents\\Rio mapocho (no borrar por favor)\\HECRAS2\\prog2\\Edif1\\models\\ED1_PARTE1_WS2_PROG2_20260508_2213.EDB",
  "log_path": "C:\\Users\\Civil\\Documents\\Rio mapocho (no borrar por favor)\\HECRAS2\\prog2\\Edif1\\logs\\ed1_setup_20260508_2226.log",
  "json_path": "C:\\Users\\Civil\\Documents\\Rio mapocho (no borrar por favor)\\HECRAS2\\prog2\\Edif1\\logs\\ed1_setup_20260508_2226.json",
  "started": "2026-05-08 22:26:04",
  "etabs": {
    "pid": 23284,
    "started_by_script": false,
    "attach_method": "GetObjectProcess",
    "version": "21.2.0"
  },
  "setup": {
    "audit_before": {
      "model_path": "C:\\Users\\Civil\\Documents\\Rio mapocho (no borrar por favor)\\HECRAS2\\prog2\\Edif1\\models\\ED1_PARTE1_WS2_PROG2_20260508_2213.EDB",
      "stories": {
        "names": [
          "Story1",
          "Story2",
          "Story3",
          "Story4",
          "Story5",
          "Story6",
          "Story7",
          "Story8",
          "Story9",
          "Story10",
          "Story11",
          "Story12",
          "Story13",
          "Story14",
          "Story15",
          "Story16",
          "Story17",
          "Story18",
          "Story19",
          "Story20"
        ],
        "elevations": [
          3.4,
          6.0,
          8.6,
          11.200000000000001,
          13.8,
          16.4,
          19.0,
          21.6,
          24.2,
          26.8,
          29.400000000000002,
          32.0,
          34.6,
          37.2,
          39.800000000000004,
          42.4,
          45.0,
          47.6,
          50.2,
          52.800000000000004
        ],
        "heights": [
          3.4,
          2.6,
          2.6,
          2.6,
          2.6,
          2.6,
          2.6,
          2.6,
          2.6,
          2.6,
          2.6,
          2.6,
          2.6,
          2.6,
          2.6,
          2.6,
          2.6,
          2.6,
          2.6,
          2.6
        ],
        "count": 20
      },
      "counts": {
        "areas": 880,
        "frames": 320,
        "points": 1350
      },
      "area_properties": {
        "MHA30G30": 260,
        "MHA20G30": 320,
        "Losa15G30": 300
      },
      "slab_elevations": {
        "6.0": 15,
        "52.8": 15,
        "50.2": 15,
        "47.6": 15,
        "45.0": 15,
        "42.4": 15,
        "39.8": 15,
        "37.2": 15,
        "34.6": 15,
        "32.0": 15,
        "29.4": 15,
        "26.8": 15,
        "24.2": 15,
        "21.6": 15,
        "19.0": 15,
        "16.4": 15,
        "13.8": 15,
        "11.2": 15,
        "8.6": 15,
        "3.4": 15
      },
      "slab_diaphragms": {
        "D1": 300
      },
      "frame_properties": {
        "VI20/60G30": 320
      },
      "base_points": 50,
      "base_restraints": {
        "(True, True, True, True, True, True)": 50
      },
      "load_patterns": [
        "Dead",
        "Live",
        "PP",
        "TERP",
        "TERT",
        "SCP",
        "SCT",
        "TorX+",
        "TorX-",
        "TorY+",
        "TorY-"
      ],
      "response_combos": [
        "ED1_C1_1.4CP",
        "ED1_C2_1.2CP_1.6L_0.5Lr",
        "ED1_C3_1.2CP_L_1.6Lr",
        "ED1_DYN_XP",
        "ED1_DYN_XN",
        "ED1_DYN_YP",
        "ED1_DYN_YN",
        "ED1_DYN_09_XP",
        "ED1_DYN_09_XN",
        "ED1_DYN_09_YP",
        "ED1_DYN_09_YN"
      ]
    },
    "diaphragm_supports": {
      "slabs_with_diaphragm": 300,
      "base_points_fixed": 50
    },
    "load_assignments": {
      "TERP": 285,
      "SCP": 285,
      "TERT": 15,
      "SCT": 15
    },
    "mass_modal": {
      "mass_source_ok": true,
      "modal_case": "MODAL",
      "modal_modes_ok": true
    },
    "spectrum_ok": true,
    "rs_cases": {
      "SEx": true,
      "SEy": true,
      "SEx_b2": true,
      "SEy_b2": true
    },
    "torsion": {
      "SEx_ecc_override": true,
      "SEy_ecc_override": true
    },
    "combos": {
      "ED1_C1_1.4CP": true,
      "ED1_C2_1.2CP_1.6L_0.5Lr": true,
      "ED1_C3_1.2CP_L_1.6Lr": true,
      "ED1_DYN_XP": true,
      "ED1_DYN_XN": true,
      "ED1_DYN_YP": true,
      "ED1_DYN_YN": true,
      "ED1_DYN_09_XP": true,
      "ED1_DYN_09_XN": true,
      "ED1_DYN_09_YP": true,
      "ED1_DYN_09_YN": true
    },
    "audit_after": {
      "model_path": "C:\\Users\\Civil\\Documents\\Rio mapocho (no borrar por favor)\\HECRAS2\\prog2\\Edif1\\models\\ED1_PARTE1_WS2_PROG2_20260508_2213.$et",
      "stories": {
        "names": [
          "Story1",
          "Story2",
          "Story3",
          "Story4",
          "Story5",
          "Story6",
          "Story7",
          "Story8",
          "Story9",
          "Story10",
          "Story11",
          "Story12",
          "Story13",
          "Story14",
          "Story15",
          "Story16",
          "Story17",
          "Story18",
          "Story19",
          "Story20"
        ],
        "elevations": [
          3.4,
          6.0,
          8.6,
          11.200000000000001,
          13.8,
          16.4,
          19.0,
          21.6,
          24.2,
          26.8,
          29.400000000000002,
          32.0,
          34.6,
          37.2,
          39.800000000000004,
          42.4,
          45.0,
          47.6,
          50.2,
          52.800000000000004
        ],
        "heights": [
          3.4,
          2.6,
          2.6,
          2.6,
          2.6,
          2.6,
          2.6,
          2.6,
          2.6,
          2.6,
          2.6,
          2.6,
          2.6,
          2.6,
          2.6,
          2.6,
          2.6,
          2.6,
          2.6,
          2.6
        ],
        "count": 20
      },
      "counts": {
        "areas": 880,
        "frames": 320,
        "points": 1350
      },
      "area_properties": {
        "MHA30G30": 260,
        "MHA20G30": 320,
        "Losa15G30": 300
      },
      "slab_elevations": {
        "6.0": 15,
        "52.8": 15,
        "50.2": 15,
        "47.6": 15,
        "45.0": 15,
        "42.4": 15,
        "39.8": 15,
        "37.2": 15,
        "34.6": 15,
        "32.0": 15,
        "29.4": 15,
        "26.8": 15,
        "24.2": 15,
        "21.6": 15,
        "19.0": 15,
        "16.4": 15,
        "13.8": 15,
        "11.2": 15,
        "8.6": 15,
        "3.4": 15
      },
      "slab_diaphragms": {
        "D1": 300
      },
      "frame_properties": {
        "VI20/60G30": 320
      },
      "base_points": 50,
      "base_restraints": {
        "(True, True, True, True, True, True)": 50
      },
      "load_patterns": [
        "Dead",
        "Live",
        "PP",
        "TERP",
        "TERT",
        "SCP",
        "SCT",
        "TorX+",
        "TorX-",
        "TorY+",
        "TorY-"
      ],
      "response_combos": [
        "ED1_C1_1.4CP",
        "ED1_C2_1.2CP_1.6L_0.5Lr",
        "ED1_C3_1.2CP_L_1.6Lr",
        "ED1_DYN_XP",
        "ED1_DYN_XN",
        "ED1_DYN_YP",
        "ED1_DYN_YN",
        "ED1_DYN_09_XP",
        "ED1_DYN_09_XN",
        "ED1_DYN_09_YP",
        "ED1_DYN_09_YN"
      ]
    }
  },
  "completed": "2026-05-08 22:26:19"
}
```
