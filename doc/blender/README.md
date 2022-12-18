----------

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

--------------

# Bake

## by Nerf
```shell
/home/kentaro/Desktop/output_model/2022-12-15-16-20-44/step-2500_batch-8_epoch-32_loss_0.0009_val_loss_0.0023/model

python scripts/texture.py --load-config /home/kentaro/Desktop/20221215_vehicle/model/VID_20221215_093333_00_014/-home-kentaro-Desktop-20221215_vehicle-data-VID_20221215_093333_00_014/nerfacto/2022-12-17_140135/config.yml \
      --input-mesh-filename /home/kentaro/Desktop/blender_ws/car.obj \
      --output-dir /home/kentaro/Desktop/blender_ws/car_adjust_mesh
```

# by blender
- bake.webm

----------------

# Mirror
- modifier -> mirror
  - mirror.webm

# Split
- select vertices -> p
  - split.webm

# Join
- select object -> 
  - join.webm

# Glass
- material -> Settings -> Blend Mode -> Alpha Blend
- Roughness:0.0, Transmission:1.0, IOR:1.51, Alpha:0.6
- glass.webm
----------------

# Rotate and shift
- rotate_and_shift.mp4

----------------

# Trim and export
- fbx
  - trim_and_export.webm
- obj
  - export_obj.webm

----------------

# Set materials

- UE5 blueprint