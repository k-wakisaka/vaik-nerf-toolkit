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
                       --bottom_foreground_image_path ./images/crimson_bar.png \
                       --output_image_dir_path "${integrate_VIDEO_WHITE_OUT_merge_DIR}"

####################
# mp4
OUTPUT_MP4_DIR=~/Downloads/Saved/MP4
mkdir ${OUTPUT_MP4_DIR} -p

bit1_MP4_PATH=${OUTPUT_MP4_DIR}/1bit.mp4
ffmpeg -r 30 -f image2 -i ${integrate_VIDEO_WHITE_OUT_1bit_DIR}/Default.%04d.png -vcodec libx264 -crf 25  -pix_fmt yuv420p ${bit1_MP4_PATH}
ffmpeg -i ${bit1_MP4_PATH} -vf setpts=PTS/1.5 -af atempo=1.5 ${bit1_MP4_PATH}.speed.mp4 -y

bit8_MP4_PATH=${OUTPUT_MP4_DIR}/8bit.mp4
ffmpeg -r 30 -f image2 -i ${integrate_VIDEO_WHITE_OUT_8bit_DIR}/Default.%04d.png -vcodec libx264 -crf 25  -pix_fmt yuv420p ${bit8_MP4_PATH}
ffmpeg -i ${bit8_MP4_PATH} -vf setpts=PTS/1.5 -af atempo=1.5 ${bit8_MP4_PATH}.speed.mp4 -y

bit32_MP4_PATH=${OUTPUT_MP4_DIR}/32bit.mp4
ffmpeg -r 30 -f image2 -i ${integrate_VIDEO_WHITE_OUT_32bit_DIR}/Default.%04d.png -vcodec libx264 -crf 25  -pix_fmt yuv420p ${bit32_MP4_PATH}
ffmpeg -i ${bit32_MP4_PATH} -vf setpts=PTS/1.5 -af atempo=1.5 ${bit32_MP4_PATH}.speed.mp4 -y

merge_MP4_PATH=${OUTPUT_MP4_DIR}/merge.mp4
ffmpeg -r 30 -f image2 -i ${integrate_VIDEO_WHITE_OUT_merge_DIR}/Default.%04d.png -vcodec libx264 -crf 25  -pix_fmt yuv420p ${merge_MP4_PATH}
ffmpeg -i ${merge_MP4_PATH} -vf setpts=PTS/1.5 -af atempo=1.5 ${merge_MP4_PATH}.speed.mp4 -y

####################
# wav
INPUT_WAV_PATH=~/Downloads/Saved/bicycle.wav
OUTPUT_1bit_WAV_PATH=~/Downloads/Saved/1bit.wav
python bit_converter.py --input_wav_path "${INPUT_WAV_PATH}" \
                       --depth_bit 1 \
                       --sample_rate 11025 \
                       --output_wav_path "${OUTPUT_1bit_WAV_PATH}"
OUTPUT_8bit_WAV_PATH=~/Downloads/Saved/8bit.wav
python bit_converter.py --input_wav_path "${INPUT_WAV_PATH}" \
                       --depth_bit 3 \
                       --sample_rate 14025 \
                       --output_wav_path "${OUTPUT_8bit_WAV_PATH}"
OUTPUT_32bit_WAV_PATH=~/Downloads/Saved/32bit.wav
python bit_converter.py --input_wav_path "${INPUT_WAV_PATH}" \
                       --depth_bit 16 \
                       --sample_rate 44100 \
                       --output_wav_path "${OUTPUT_32bit_WAV_PATH}"
OUTPUT_merge_WAV_PATH=~/Downloads/Saved/merge_bit.wav
python bit_converter.py --input_wav_path "${INPUT_WAV_PATH}" \
                       --depth_bit 16 \
                       --sample_rate 44100 \
                       --output_wav_path "${OUTPUT_merge_WAV_PATH}"
############
# concat
TRIM_SECONDS=6
ffmpeg -i ${OUTPUT_1bit_WAV_PATH} -t ${TRIM_SECONDS} ${OUTPUT_1bit_WAV_PATH}.trim.wav -y
ffmpeg -i ${OUTPUT_8bit_WAV_PATH} -t ${TRIM_SECONDS} ${OUTPUT_8bit_WAV_PATH}.trim.wav -y
ffmpeg -i ${OUTPUT_32bit_WAV_PATH} -t ${TRIM_SECONDS} ${OUTPUT_32bit_WAV_PATH}.trim.wav -y
ffmpeg -i ${OUTPUT_merge_WAV_PATH} -t ${TRIM_SECONDS} ${OUTPUT_merge_WAV_PATH}.trim.wav -y

ffmpeg -i ${bit1_MP4_PATH}.speed.mp4 -i ${OUTPUT_1bit_WAV_PATH}.trim.wav -c:v copy ${bit1_MP4_PATH}.concat.mp4
ffmpeg -i ${bit8_MP4_PATH}.speed.mp4 -i ${OUTPUT_8bit_WAV_PATH}.trim.wav -c:v copy ${bit8_MP4_PATH}.concat.mp4
ffmpeg -i ${bit32_MP4_PATH}.speed.mp4 -i ${OUTPUT_32bit_WAV_PATH}.trim.wav -c:v copy ${bit32_MP4_PATH}.concat.mp4
ffmpeg -i ${merge_MP4_PATH}.speed.mp4 -i ${OUTPUT_merge_WAV_PATH}.trim.wav -c:v copy ${merge_MP4_PATH}.concat.mp4
############
# Integrate
# concatenate
out_MP4_PATH1=${OUTPUT_MP4_DIR}/out1.mp4
out_MP4_PATH2=${OUTPUT_MP4_DIR}/out2.mp4
out_MP4_PATH3=${OUTPUT_MP4_DIR}/out.mp4


ffmpeg -i ${bit1_MP4_PATH}.concat.mp4 -i ${bit8_MP4_PATH}.concat.mp4  -filter_complex "[0:v]setpts=N/FRAME_RATE/TB[0];[1:v]setpts=N/FRAME_RATE/TB[1];[0][0:a][1][1:a]concat=n=2:v=1:a=1" ${out_MP4_PATH1}
ffmpeg -i ${out_MP4_PATH1} -i ${bit32_MP4_PATH}.concat.mp4  -filter_complex "[0:v]setpts=N/FRAME_RATE/TB[0];[1:v]setpts=N/FRAME_RATE/TB[1];[0][0:a][1][1:a]concat=n=2:v=1:a=1" ${out_MP4_PATH2}
ffmpeg -i ${out_MP4_PATH2} -i ${merge_MP4_PATH}.concat.mp4  -filter_complex "[0:v]setpts=N/FRAME_RATE/TB[0];[1:v]setpts=N/FRAME_RATE/TB[1];[0][0:a][1][1:a]concat=n=2:v=1:a=1" ${out_MP4_PATH3}
# change size
resize_MP4_PATH=${OUTPUT_MP4_DIR}/resize_out.mp4
ffmpeg -i ${out_MP4_PATH3} -vf scale=-1:1280 ${resize_MP4_PATH}