# colmap

## Install

```shell
sudo apt-get update
sudo apt-get install colmap
pip install -r requirements.txt
```

## Prepare colmap

```shell
python script/process_data.py video \
        --data ~/Desktop/data/input.mp4 \
        --output-dir ~/Desktop/data/input_colmap/ \
        --num-frames-target 300 \
        --matching-method exhaustive \
        --verbose
```

- Ref. https://github.com/nerfstudio-project/nerfstudio/tree/main/scripts

## View colmap

```shell
colmap gui --import_path ~/Desktop/data/input_colmap/colmap/sparse/0/ \
           --database_path ~/Desktop/data/input_colmap/colmap/database.db \
           --image_path ~/Desktop/data/input_colmap/images
```