
# Delete vertices and Fill hole and texture paint
## Edit vertices
- Delete vertices
  - Modeling -> c -> Delete
    - delete_vertices_c.webm
  - Modeling -> Alt + select vertices -> Delete -> vertices or edge
    - delete_vertices_alt.webm
- Fill hole
  - Modeling -> Shift + select vertices -> f
    - fill_hole.webm
- Subdivide
  - Shift + Alt + select vertices -> Ctrl + T -> Right click -> Subdivide
    - subdivide.webm
- Smooth
  - Ctrl + a -> Ctrl + v -> Smooth vertices

## Edit surface
- Sculpting
  - flatten
    - flatten.webm
  - grab
    - glab.webm

# Bake
```shell
/home/kentaro/Desktop/output_model/2022-12-15-16-20-44/step-2500_batch-8_epoch-32_loss_0.0009_val_loss_0.0023/model

python scripts/texture.py --load-config /home/kentaro/Desktop/20221215_vehicle/model/VID_20221215_092229_00_011/-home-kentaro-Desktop-20221215_vehicle-data-VID_20221215_092229_00_011/nerfacto/2022-12-15_153735/config.yml \
      --input-mesh-filename /home/kentaro/Desktop/blender_ws/car_adjust.fbx \
      --output-dir /home/kentaro/Desktop/blender_ws/car_adjust_mesh
```

# Rotate and shift
- rotate_and_shift.mp4

# Trim and export
- trim_and_export.webm
