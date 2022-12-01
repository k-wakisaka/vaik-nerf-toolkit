VIDEO_WHITE_DIR=~/Downloads/Saved/VideoCaptures0
VIDEO_1_DIR=~/Downloads/Saved/VideoCaptures1
VIDEO_2_DIR=~/Downloads/Saved/VideoCaptures2
VIDEO_3_DIR=~/Downloads/Saved/VideoCaptures3
VIDEO_4_DIR=~/Downloads/Saved/VideoCaptures4

####################
# prepare images

# quantize
VIDEO_WHITE_OUT_1bit_DIR=~/Downloads/Saved/VideoCaptures0_1bit
python convert_pixel_art.py --input_image_dir_path "${VIDEO_WHITE_DIR}" \
                            --resize_sub_pixel 24 \
                            --quantize_bit 1 \
                            --output_image_dir_path "${VIDEO_WHITE_OUT_1bit_DIR}"

VIDEO_WHITE_OUT_8bit_DIR=~/Downloads/Saved/VideoCaptures0_8bit
python convert_pixel_art.py --input_image_dir_path "${VIDEO_WHITE_DIR}" \
                            --resize_sub_pixel 12 \
                            --quantize_bit 8 \
                            --output_image_dir_path "${VIDEO_WHITE_OUT_8bit_DIR}"

VIDEO_WHITE_OUT_32bit_DIR=~/Downloads/Saved/VideoCaptures0_32bit
cp -r ${VIDEO_WHITE_DIR} ${VIDEO_WHITE_OUT_32bit_DIR}

# merge
VIDEO_WHITE_OUT_merge_DIR=~/Downloads/Saved/VideoCapturesx
python merge_video.py --input_video_path_1 "${VIDEO_1_DIR}" \
                       --input_video_path_2 "${VIDEO_2_DIR}" \
                       --input_video_path_3 "${VIDEO_3_DIR}" \
                       --input_video_path_4 "${VIDEO_4_DIR}" \
                       --output_image_path "${VIDEO_WHITE_OUT_merge_DIR}"
####################
# integrate
integrate_VIDEO_WHITE_OUT_1bit_DIR=~/Downloads/Saved/integrate_VideoCaptures0_1bit
python merge_image.py --top_image_path ./images/top_q.png \
                       --header_image_path ./images/header_1bit.png \
                       --input_image_dir_path "${VIDEO_WHITE_OUT_1bit_DIR}" \
                       --bottom_background_image_path ./images/black_bar.png  \
                       --bottom_foreground_image_path ./images/white_bar.png \
                       --output_image_dir_path "${integrate_VIDEO_WHITE_OUT_1bit_DIR}"

integrate_VIDEO_WHITE_OUT_8bit_DIR=~/Downloads/Saved/integrate_VideoCaptures0_8bit
python merge_image.py --top_image_path ./images/top_q.png \
                       --header_image_path ./images/header_8bit.png \
                       --input_image_dir_path "${VIDEO_WHITE_OUT_8bit_DIR}" \
                       --bottom_background_image_path ./images/black_bar.png  \
                       --bottom_foreground_image_path ./images/royalblue_bar.png \
                       --output_image_dir_path "${integrate_VIDEO_WHITE_OUT_8bit_DIR}"

integrate_VIDEO_WHITE_OUT_32bit_DIR=~/Downloads/Saved/integrate_VideoCaptures0_32bit
python merge_image.py --top_image_path ./images/top_q.png \
                       --header_image_path ./images/header_32bit.png \
                       --input_image_dir_path "${VIDEO_WHITE_OUT_32bit_DIR}" \
                       --bottom_background_image_path ./images/black_bar.png  \
                       --bottom_foreground_image_path ./images/crimson_bar.png \
                       --output_image_dir_path "${integrate_VIDEO_WHITE_OUT_32bit_DIR}"

integrate_VIDEO_WHITE_OUT_merge_DIR=~/Downloads/Saved/integrate_VideoCapturesx
python merge_image.py --top_image_path ./images/top_a.png \
                       --header_image_path ./images/header_32bit.png \
                       --input_image_dir_path "${VIDEO_WHITE_OUT_merge_DIR}" \
                       --bottom_background_image_path ./images/black_bar.png  \
                       --bottom_foreground_image_path ./images/gold_bar.png \
                       --output_image_dir_path "${integrate_VIDEO_WHITE_OUT_merge_DIR}"

####################
# mp4
OUTPUT_MP4_DIR=~/Downloads/Saved/MP4
mkdir ${OUTPUT_MP4_DIR} -p

bit1_MP4_PATH=${OUTPUT_MP4_DIR}/1bit.mp4
ffmpeg -r 30 -f image2 -i ${integrate_VIDEO_WHITE_OUT_1bit_DIR}/Default.%04d.png -vcodec libx264 -crf 25  -pix_fmt yuv420p ${bit1_MP4_PATH}

bit8_MP4_PATH=${OUTPUT_MP4_DIR}/8bit.mp4
ffmpeg -r 30 -f image2 -i ${integrate_VIDEO_WHITE_OUT_8bit_DIR}/Default.%04d.png -vcodec libx264 -crf 25  -pix_fmt yuv420p ${bit8_MP4_PATH}

bit32_MP4_PATH=${OUTPUT_MP4_DIR}/32bit.mp4
ffmpeg -r 30 -f image2 -i ${integrate_VIDEO_WHITE_OUT_32bit_DIR}/Default.%04d.png -vcodec libx264 -crf 25  -pix_fmt yuv420p ${bit32_MP4_PATH}

merge_MP4_PATH=${OUTPUT_MP4_DIR}/merge.mp4
ffmpeg -r 30 -f image2 -i ${integrate_VIDEO_WHITE_OUT_merge_DIR}/Default.%04d.png -vcodec libx264 -crf 25  -pix_fmt yuv420p ${merge_MP4_PATH}

# concatenate
out_MP4_PATH=${OUTPUT_MP4_DIR}/out.mp4
out_txt_PATH=${OUTPUT_MP4_DIR}/file.txt
echo "file ${bit1_MP4_PATH}" >> ${out_txt_PATH}
echo "file ${bit8_MP4_PATH}" >> ${out_txt_PATH}
echo "file ${bit32_MP4_PATH}" >> ${out_txt_PATH}
echo "file ${merge_MP4_PATH}" >> ${out_txt_PATH}

ffmpeg -safe 0 -f concat -i ${out_txt_PATH} -c copy ${out_MP4_PATH}

# change speed
speed_out_MP4_PATH=${OUTPUT_MP4_DIR}/speed_out.mp4
ffmpeg -i ${out_MP4_PATH} -vf setpts=PTS/1.5 -af atempo=1.5 ${speed_out_MP4_PATH}

# change size
resize_MP4_PATH=${OUTPUT_MP4_DIR}/resize_out.mp4
ffmpeg -i ${speed_out_MP4_PATH} -vf scale=-1:1280 ${resize_MP4_PATH}

