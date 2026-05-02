# Comandos WS UCN

## Primera descarga

```powershell
cd C:\Users\Civil\Documents
git clone https://github.com/kcortes765/taha.git
cd taha
git checkout codex/ws-u-ed1-ui-context
```

## Si el repo ya existe en la WS

```powershell
cd C:\Users\Civil\Documents\taha
git fetch origin
git checkout codex/ws-u-ed1-ui-context
git pull
```

## Abrir contexto

```powershell
explorer .\transfer\ws-u-ed1-ui-context
```

## Regla para el modelo ETABS

No guardar modelos `.EDB` dentro del repo salvo que se acuerde Git LFS.

Sugerencia para modelos locales:

```powershell
mkdir C:\Users\Civil\Documents\ED1_ETABS_MODELOS
```

Usar nombres tipo:

```text
ED1_01_Story2_PlantaTipo_OK.edb
ED1_02_TodosPisos_Copiados_OK.edb
ED1_03_Diaphragm_Mesh_OK.edb
ED1_04_Cargas_OK.edb
```

## Para volver con evidencia

Exportar desde ETABS a una carpeta local fuera del repo y despues copiar solo CSV/Excel/imagenes pequenas si se decide versionar.

No subir:

- `.EDB`
- backups grandes
- carpetas de analisis temporales de ETABS
- renders o capturas duplicadas sin valor tecnico

