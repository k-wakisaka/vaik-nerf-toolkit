# colmap

## Install

```shell
sudo apt-get update
sudo apt-get install colmap
pip install -r requirements.txt
```

## MP4 to jpg

```shell
MP4_PATH=~/Desktop/data/input.mp4
OUTPUT_IMAGE_DIR=~/Desktop/data/input_image
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
ls |awk '{printf "mv \"%s\" frame_%05d.png\n", $0, NR }' |sh
```

## Prepare colmap

```shell
cd colmap/script
python process_data.py images \
        --data ~/Desktop/data/input_image \
        --output-dir ~/Desktop/data/input_colmap/ \
        --matching-method exhaustive \
        --verbose
```

- Ref. https://github.com/nerfstudio-project/nerfstudio/tree/main/scripts

## View colmap

```shell
colmap gui --import_path ~/Desktop/data/input_colmap/sparse/0/ \
           --database_path ~/Desktop/data/input_colmap/database.db \
           --image_path ~/Desktop/data/input_colmap/images
```

## colmap2poses

```shell
cd colmap/script
python colmap2poses.py --input_colmap_dir ~/Desktop/data/input_colmap
```