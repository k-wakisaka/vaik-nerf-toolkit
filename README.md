# vaik-nerf-toolkit

-----------

# Capture object

## Scaniverse with lidar
### lidar mode

---------
## Insta360

### Capture
- hdr mode

### Deep Track
- key frame
- distance 50
- export
-----------

# Video to Image

## MP4 to jpg

```shell
MP4_PATH=/home/kentaro/Desktop/20221215_vehicle/videos/VID_20221215_093333_00_014.mp4
OUTPUT_IMAGE_DIR=/home/kentaro/Desktop/20221215_vehicle/images/VID_20221215_093333_00_014
OUTPUT_FRAME_NUM=200

mkdir -p ${OUTPUT_IMAGE_DIR}
FRAME_NUM=` ffprobe -v error -select_streams v:0 -count_packets -show_entries stream=nb_read_packets -of csv=p=0 ${MP4_PATH} `
SPACE_FRAME_NUM=` expr ${FRAME_NUM} / ${OUTPUT_FRAME_NUM} `
ffmpeg -i ${MP4_PATH} -vf thumbnail=${SPACE_FRAME_NUM},setpts=N/TB -r 1 ${OUTPUT_IMAGE_DIR}/frame_%05d.png
```

## Remove except image

- remove except image

```shell
IMAGE_DIR=/home/kentaro/Desktop/20221215_vehicle/images/VID_20221215_092229_00_011
cd ${IMAGE_DIR}
find *.png |awk '{printf "mv \"%s\" frame_%05d.png\n", $0, NR }' |sh
```

----------


# Prepare colmap

```shell
ns-process-data images --data /home/kentaro/Desktop/20221215_vehicle/images/fix_images \
                       --output-dir /home/kentaro/Desktop/20221215_vehicle/data/fix_images --verbose
```

```shell
ns-process-data images --data /home/kentaro/Desktop/20221215_vehicle/images/VID_20221215_092229_00_011_unet/images \
                       --output-dir /home/kentaro/Desktop/20221215_vehicle/data/VID_20221215_092229_00_011_unet \
                       --matching-method exhaustive \
                       --verbose
```

```shell
ns-process-data images --data /home/kentaro/Desktop/20221215_vehicle/images/VID_20221215_092229_00_011_unet/images \
                       --output-dir /home/kentaro/Desktop/20221215_vehicle/data/fix_images \
                      --sfm-tool hloc \
                      --matching-method exhaustive \
                      --feature-type superpoint \
                      --matcher-type superglue \
                      --verbose
```

-----------

# Train

```shell
ns-train nerfacto --data /home/kentaro/Desktop/20221215_vehicle/data/fix_images \
                  --output-dir /home/kentaro/Desktop/20221215_vehicle/model/fix_images  \
                  --pipeline.model.predict-normals True
```

## Export mesh
```shell
ns-export poisson --load-config /home/kentaro/Desktop/20221215_vehicle/model/fix_images/-home-kentaro-Desktop-20221215_vehicle-data-fix_images/nerfacto/2022-12-20_183523/config.yml \
                  --output-dir /home/kentaro/Desktop/20221215_vehicle/mesh/fix_images
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
- repeat setlect 「Select -> Select More/Less -> More -> Shift + R 」
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
