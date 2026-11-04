# Original file mapping and publication notes

Source: `sionna_project.zip` (supplied by the user).

All **substantive project code, 3D meshes, scene XML, native Blender files, OSM source assets, and rendered screenshot** have been kept; redundant editor-generated outputs/backups were omitted. The original ZIP remains the full untouched backup.

## Renamed/moved files

| Original relative path | GitHub path |
| --- | --- |
| `rt_visualize.py` | `scripts/rt_visualize.py` |
| `uplink_sim.py` | `scripts/uplink_sim.py` |
| `rt_visualize.ipynb` | `notebooks/01_rt_visualize.ipynb` |
| `Library.ipynb` | `notebooks/02_load_blender_scene.ipynb` |
| `University_RIS.ipynb` | `notebooks/03_university_reflector_comparison.ipynb` |
| `sionna19_RIS.ipynb` | `notebooks/04_legacy_sionna019_import.ipynb` |
| `Downlink_1user.ipynb` | `notebooks/05_downlink_radio_map_external_mat.ipynb` |
| `Untitled2.ipynb` | `notebooks/experiments/reflector_development_notes.ipynb` |
| `Untitled.ipynb` | `notebooks/experiments/downlink_radio_map_draft.ipynb` |
| `University.xml` | `scenes/University.xml` |
| `University_RIS.xml` | `scenes/University_RIS.xml` |
| `library.xml` | `scenes/library.xml` |
| `meshes/RIS_panel.ply` | `scenes/meshes/RIS_panel.ply` |
| `meshes/map_13_osm_buildings-roof.ply` | `scenes/meshes/map_13_osm_buildings-roof.ply` |
| `meshes/map_13_osm_buildings-wall.ply` | `scenes/meshes/map_13_osm_buildings-wall.ply` |
| `meshes/map_7_osm_buildings-roof.ply` | `scenes/meshes/map_7_osm_buildings-roof.ply` |
| `meshes/map_7_osm_buildings-wall.ply` | `scenes/meshes/map_7_osm_buildings-wall.ply` |
| `meshes/map_7_osm_forest.ply` | `scenes/meshes/map_7_osm_forest.ply` |
| `meshes/map_7_osm_paths_footway.ply` | `scenes/meshes/map_7_osm_paths_footway.ply` |
| `meshes/map_7_osm_paths_steps.ply` | `scenes/meshes/map_7_osm_paths_steps.ply` |
| `meshes/map_7_osm_roads_service.ply` | `scenes/meshes/map_7_osm_roads_service.ply` |
| `meshes/map_7_osm_vegetation.ply` | `scenes/meshes/map_7_osm_vegetation.ply` |
| `University.blend` | `models/University.blend` |
| `library.blend` | `models/library.blend` |
| `library.x3d` | `models/library.x3d` |
| `osm/map.osm` | `osm/map.osm` |
| `osm/map_10.osm` | `osm/map_10.osm` |
| `osm/map_10_extra.osm` | `osm/map_10_extra.osm` |
| `osm/map_11.osm` | `osm/map_11.osm` |
| `osm/map_11_extra.osm` | `osm/map_11_extra.osm` |
| `osm/map_12.osm` | `osm/map_12.osm` |
| `osm/map_13.osm` | `osm/map_13.osm` |
| `osm/map_13_extra.osm` | `osm/map_13_extra.osm` |
| `osm/map_2.osm` | `osm/map_2.osm` |
| `osm/map_3.osm` | `osm/map_3.osm` |
| `osm/map_4.osm` | `osm/map_4.osm` |
| `osm/map_5.osm` | `osm/map_5.osm` |
| `osm/map_6.osm` | `osm/map_6.osm` |
| `osm/map_6_extra.osm` | `osm/map_6_extra.osm` |
| `osm/map_7.osm` | `osm/map_7.osm` |
| `osm/map_7_extra.osm` | `osm/map_7_extra.osm` |
| `osm/map_8.osm` | `osm/map_8.osm` |
| `osm/map_8_extra.osm` | `osm/map_8_extra.osm` |
| `osm/map_9.osm` | `osm/map_9.osm` |
| `rt_paths_zoom.png` | `figures/rt_paths_zoom.png` |

## Deliberately omitted

- `.ipynb_checkpoints/ (auto-created notebook checkpoints)`
- `library.blend1, University.blend1 (Blender auto-backup)`
- `Untitled1.ipynb (empty notebook)`

## Changes made without altering the research algorithms

- Replaced hard-coded `C:\Users\...` paths in notebooks with repository-relative paths.
- Converted path references for `University_ris.xml` to the actual `University_RIS.xml` case-sensitive filename.
- Moved Ray Tracing image output into `figures/`.
- Removed Notebook saved outputs and execution counts to eliminate private PC tracebacks and stale results.
- No missing MATLAB `.mat` datasets were invented.
- No external license is assigned to the source code or 3D models.
