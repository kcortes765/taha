# ACTIVE SPEC - Preparar y explotar 10 sesiones GPT-5.4 Pro para Edificio 1

## Objetivo
Dejar un paquete real, autosuficiente y tecnicamente serio para correr 10 sesiones separadas de GPT-5.4 Pro sobre Edificio 1, de modo que cada chat pueda auditar una parte critica del proyecto con suficiente contexto sin depender del resto.

## Criterios de aceptacion
1. Existen 10 carpetas separadas bajo `review-ia/ed1-gpt54pro-10-sesiones/`.
2. Cada carpeta contiene:
   - prompt de arranque especifico
   - estado actual y dossier comun
   - enunciado, apuntes, material del taller y normas
   - memorias `.apos/`
   - codigo relevante del frente operativo `taller-etabs/`
   - codigo relevante del frente historico `autonomo/scripts/`
3. La carpeta no es minimalista ni dependiente de otros directorios para entender el problema.
4. El paquete explicita que el repo no es una sola version coherente y fuerza a distinguir canon, historico y dudoso.
5. El usuario puede abrir los 10 chats y trabajar con cada carpeta por separado.

## Inputs
- `review-ia/taller/`
- `docs/estudio/`
- `.apos/`
- `taller-etabs/`
- `autonomo/scripts/`
- `autonomo/research/`
- `evidencia/enunciado-ed1-vs-ed2/`
- `materiales_fuente/sismo/correo/emails.json`

## Constraints
- No adelgazar artificialmente el contexto.
- No tratar archivos sinteticos como si fueran fuente primaria cuando no lo son.
- Repetir archivos es aceptable si mejora autosuficiencia.
- Mantener claridad sobre que codigo es operativo, historico o solo evidencia de conflicto.

## Entregables activos
- `review-ia/ed1-gpt54pro-10-sesiones/00_INDICE_PAQUETES.md`
- `review-ia/ed1-gpt54pro-10-sesiones/00_DOSSIER_ED1_2026-04-20.md`
- `review-ia/ed1-gpt54pro-10-sesiones/01_PROMPT_MAESTRO_GPT54PRO_ED1.md`
- `review-ia/ed1-gpt54pro-10-sesiones/01_GEOMETRIA_CANONICA/`
- `review-ia/ed1-gpt54pro-10-sesiones/10_REDTEAM_COMISION_FINAL/`
