# video for sns

## convert pixel art

```shell
python convert_pixel_art.py --input_image_dir_path ~/home/kentaro/Desktop/VideoCaptures \
                            --resize_sub_pixel 64 \
                            --quantize_bit 1 \
                            --output_image_dir_path ~/home/kentaro/Desktop/VideoCaptures_out
```

## merge widget

```shell
pythyon merge_image.py --top_image_path ./images/top_q.png \
                        --header_image_path ./images/header_8bit.png \
                        --input_image_dir_path ~/Desktop/input_image \
                        --bottom_background_image_path ~/images/black_bar.png \
                        --bottom_foreground_image_path ~/images/royalblue_bar.png \
                        --output_image_dir_path ~/Desktop/output_image
```