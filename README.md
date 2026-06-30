# landslide-data-prep

Preprocessing pipeline for AOI-based geospatial data retrieval, harmonization, and Landlab-ready raster export.

## Scope

This repo keeps the data-prep side only:

- AOI validation
- DEM retrieval or local DEM ingest
- burn severity retrieval with `remote_then_local` fallback
- soil, landcover, vegetation, climate, and topographic layer processing
- aligned raster stack generation
- Landlab-ready `.asc` export
- final GeoTIFF export

This repo does not include ML training, tuning, or prediction workflows.

## Install

```bash
conda env create -f environment.yml
conda activate landslide-data-prep
```

If you already have a working geospatial environment on this machine, you can also use it directly.

## Configure

Edit `config/base.yaml` and set:

- `aoi.aoi`
- `paths.input_dir`
- `paths.output_dir`
- `dem.cache_dir`
- local burn severity path if you use local fallback

## Run

Raster-only debug run:

```bash
python src/run_pipeline.py --config config/base.yaml --raster-only --keep-intermediates
```

Full preprocessing run with final GeoTIFF export:

```bash
python src/run_pipeline.py --config config/base.yaml --export-final-tifs
```

## Soil CLI

Standalone soil workflow:

```bash
python scripts/soil_fetch.py
python scripts/soil_harmonize.py
python scripts/soil_run.py
```

## Tests

```bash
python -m pytest -q tests
```
