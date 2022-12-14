----------
# Flow_bk
- Smooth vertices -> Merge vertices -> Remove vertices -> Boolean intersect -> Export -> Boolean diff -> Export -> Import -> Merge vertices
  - Select vertices -> Select more -> Remove vertices
    - Sculpting(Grab) -> Remove vertices -> Merge vertices(a few points) -> Dissolve edge -> knife -> Remove vertices -> Sculpting(Inflate/smooth/Scrape) knife -> split mesh
      - Mirror -> Join -> Merge vertices -> fill (glass) -> Add tire -> Normalize Normals-> Apply(Transform) -> Export(fbx)
        - Import -> Material(two side)
----------
# Flow
- Smooth vertices -> Merge vertices -> Shift & Rotate -> Remove vertices -> Bisect -> Apply all transform -> Export
    - Manual Sculpting(Inflate/smooth/Scrape) by knife & s + z + 0 -> split mesh
      - Mirror -> Attach Item(mirror) -> cApply(Transform) -> Export(fbx)
        - Import -> Material(two side)

# Select
- c
- Ctrl + left click
- Alt + e + left click

# Sort
- s -> x/y/z -> 0 -> Enter

# Delete vertices and Fill hole and texture paint
## Edit vertices
- Smooth vertices
  - Ctrl + a -> right click -> adjust distance
- merge vertices
  - Ctrl + a -> merge vertices -> adjust distance
- Delete vertices
  - Modeling -> c -> Delete
    - delete_vertices_c.webm
  - Modeling -> select vertices -> select -> select more -> Delete -> vertices or edge
    - delete_vertices_alt.webm
- Fill hole
  - Modeling -> Shift + select vertices -> f -> Ctrl + T -> right click -> subdivide
    - fill_hole.webm
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
