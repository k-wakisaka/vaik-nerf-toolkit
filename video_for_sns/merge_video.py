import glob
import argparse
import os
import shutil

def main(input_video_path_1, input_video_path_2, input_video_path_3, input_video_path_4, output_image_path):
    os.makedirs(output_image_path, exist_ok=True)
    input_video_path_1_list = sorted(glob.glob(os.path.join(input_video_path_1, '*.png')))
    input_video_path_2_list = sorted(glob.glob(os.path.join(input_video_path_2, '*.png')))
    input_video_path_3_list = sorted(glob.glob(os.path.join(input_video_path_3, '*.png')))
    input_video_path_4_list = sorted(glob.glob(os.path.join(input_video_path_4, '*.png')))

    start_index = 0
    split_num = len(input_video_path_1_list)//4

    for index in range(split_num):
        shutil.copy(input_video_path_1_list[index+start_index], os.path.join(output_image_path, os.path.basename(input_video_path_1_list[index+start_index])))
    start_index += split_num
    for index in range(split_num):
        shutil.copy(input_video_path_2_list[index+start_index], os.path.join(output_image_path, os.path.basename(input_video_path_2_list[index+start_index])))
    start_index += split_num
    for index in range(split_num):
        shutil.copy(input_video_path_3_list[index+start_index], os.path.join(output_image_path, os.path.basename(input_video_path_3_list[index+start_index])))
    start_index += split_num
    for index in range(split_num):
        shutil.copy(input_video_path_4_list[index+start_index], os.path.join(output_image_path, os.path.basename(input_video_path_4_list[index+start_index])))
    start_index += split_num


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='merge video')
    parser.add_argument('--input_video_path_1', type=str, default="~/Downloads/Saved/VideoCaptures1")
    parser.add_argument('--input_video_path_2', type=str, default="~/Downloads/Saved/VideoCaptures2")
    parser.add_argument('--input_video_path_3', type=str, default="~/Downloads/Saved/VideoCaptures3")
    parser.add_argument('--input_video_path_4', type=str, default="~/Downloads/Saved/VideoCaptures4")
    parser.add_argument('--output_image_path', type=str, default='~/Downloads/Saved/VideoCapturesx')
    args = parser.parse_args()

    args.input_video_path_1 = os.path.expanduser(args.input_video_path_1)
    args.input_video_path_2 = os.path.expanduser(args.input_video_path_2)
    args.input_video_path_3 = os.path.expanduser(args.input_video_path_3)
    args.input_video_path_4 = os.path.expanduser(args.input_video_path_4)
    args.output_image_path = os.path.expanduser(args.output_image_path)

    main(args.input_video_path_1, args.input_video_path_2, args.input_video_path_3, args.input_video_path_4, args.output_image_path)
