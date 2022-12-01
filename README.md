# vaik-nerf-toolkit

-----------

# Capture object

## Insta360


-----------

# Video to Image

## MP4 to jpg

```shell
MP4_PATH=~/Desktop/input.mp4
OUTPUT_IMAGE_DIR=~/Desktop/input_image
OUTPUT_FRAME_NUM=300

mkdir -p ${OUTPUT_IMAGE_DIR}
FRAME_NUM=` ffprobe -v error -select_streams v:0 -count_packets -show_entries stream=nb_read_packets -of csv=p=0 ${MP4_PATH} `
SPACE_FRAME_NUM=` expr ${FRAME_NUM} / ${OUTPUT_FRAME_NUM} `
ffmpeg -i ${MP4_PATH} -vf thumbnail=${SPACE_FRAME_NUM},setpts=N/TB -r 1 ${OUTPUT_IMAGE_DIR}/frame_%05d.png
```

## Remove except image

- remove except image

```shell
IMAGE_DIR=${OUTPUT_IMAGE_DIR}
cd ${IMAGE_DIR}
find *.png |awk '{printf "mv \"%s\" frame_%05d.png\n", $0, NR }' |sh
```

----------


# Prepare colmap

```shell
ns-process-data images --data /home/kentaro/Desktop/input_image --output-dir ~/Desktop/data --verbose 
```

-----------

# Train

```shell
ns-train nerfacto --data ~/Desktop/data --pipeline.model.predict-normals True
```

## Export mesh
```shell
ns-export poisson --load-config /home/kentaro/Github/vaik-nerfstudio-project/outputs/-home-kentaro-Desktop-data/nerfacto/2022-12-01_093630/config.yml \
                  --output-dir ~/Desktop/output_mesh
```

--------

# Adjust mesh
- blender

## Rotate and shift

![rotate_and_shift](./blender/rotate_shift.gif)

## Trim

![trim](./blender/trim.gif)

## Delete
- rough select 「c」button
- detail select 「shift+click」

![delete](./blender/delete.gif)

## Add mesh

![add_mesh](./blender/add_mesh.gif)

## prepare video by UE5
- [video_for_sns](https://drive.google.com/file/d/16unWZmbYkJuuNoWSi7FNVFZ3HeMjNkS0/view?usp=sharing)
  - HDRIBackdrop
    - Actor Hidden In Game
  - DefaultSeq
    - Render icon
      - Capture Movie
  - output
    - 1280 x 1280 [pixels]