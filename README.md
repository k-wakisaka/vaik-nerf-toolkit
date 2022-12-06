# vaik-nerf-toolkit

-----------

# Capture object

## Insta360


-----------

# Video to Image

## MP4 to jpg

```shell
MP4_PATH=/home/kentaro/Desktop/meat.mp4
OUTPUT_IMAGE_DIR=~/Desktop/meat
OUTPUT_FRAME_NUM=300

mkdir -p ${OUTPUT_IMAGE_DIR}
FRAME_NUM=` ffprobe -v error -select_streams v:0 -count_packets -show_entries stream=nb_read_packets -of csv=p=0 ${MP4_PATH} `
SPACE_FRAME_NUM=` expr ${FRAME_NUM} / ${OUTPUT_FRAME_NUM} `
ffmpeg -i ${MP4_PATH} -vf thumbnail=2,setpts=N/TB -r 1 ${OUTPUT_IMAGE_DIR}/frame_%05d.png
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
ns-process-data images --data /home/kentaro/Desktop/meat --output-dir /home/kentaro/Desktop/meat_data --verbose 
```

-----------

# Train

```shell
ns-train nerfacto --data ~/Desktop/meat_data --pipeline.model.predict-normals True
```

## Export mesh
```shell
ns-export poisson --load-config /home/kentaro/Github/vaik-nerfstudio-project/outputs/-home-kentaro-Desktop-car_data/nerfacto/2022-12-02_182754/config.yml \
                  --output-dir ~/Desktop/output_mesh
```

--------

# Adjust mesh
- blender

## Rotate and shift

![rotate_and_shift](doc/rotate_shift.gif)

## Trim

![trim](doc/trim.gif)


## Export

![export](doc/export.gif)

## Delete
- rough select 「c」button
- detail select 「shift+click」

![delete](doc/delete.gif)

## Add mesh

![add_mesh](doc/add_mesh.gif)

-------

# Render

## prepare video by UE5
- [video_for_sns](https://drive.google.com/file/d/16unWZmbYkJuuNoWSi7FNVFZ3HeMjNkS0/view?usp=sharing)
  - HDRIBackdrop
    - Actor Hidden In Game
  - DefaultSeq
    - Render icon
      - Capture Movie
  - output
    - 1280 x 1280 [pixels]

--------

# Integrate

```shell
cd video_for_sns
./crate_video.sh
```

- comment

```
本日も、NeRF（Neural Radiance Fields）により、動画からCGオブジェクトを作成しました！

音もつけてます。
```
