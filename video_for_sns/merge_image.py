from PIL import Image, ImageDraw, ImageFont
import argparse
import os
import glob
import re

def get_concat_v_cut_center(im1, im2):
    dst = Image.new('RGB', (min(im1.width, im2.width), im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, ((im1.width - im2.width) // 2, im1.height))
    return dst

def paste(bg, fg, ratio):
    canvas = bg.copy()
    canvas.paste(fg, (int(bg.width*ratio), 0))
    return canvas

def draw(top_image, header_image, image, bottom_background_image, bottom_foreground_image, index, length):
    process_bar_image = paste(bottom_background_image, bottom_foreground_image, index/length)
    canvas_image = get_concat_v_cut_center(top_image, header_image)
    canvas_image = get_concat_v_cut_center(canvas_image, image)
    canvas_image = get_concat_v_cut_center(canvas_image, process_bar_image)
    return canvas_image

def main(top_image_path, header_image_path, input_image_dir_path, bottom_background_image_path, bottom_foreground_image_path, output_image_dir_path):
    os.makedirs(output_image_dir_path, exist_ok=True)
    top_image = Image.open(open(top_image_path, 'rb')).convert('RGB')
    header_image = Image.open(open(header_image_path, 'rb')).convert('RGB')
    bottom_background_image = Image.open(open(bottom_background_image_path, 'rb')).convert('RGB')
    bottom_foreground_image = Image.open(open(bottom_foreground_image_path, 'rb')).convert('RGB')

    image_path_list = sorted(
        [file_path for file_path in glob.glob(os.path.join(input_image_dir_path, '**/*.*'), recursive=True) if
         re.search('.*\.(png|jpg|bmp)$', file_path)])

    for index, image_path in enumerate(image_path_list):
        image = Image.open(open(image_path, 'rb')).convert('RGB')
        draw_image = draw(top_image, header_image, image, bottom_background_image, bottom_foreground_image, index, len(image_path_list))
        draw_image.save(os.path.join(output_image_dir_path, os.path.basename(image_path)))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='make string image')
    parser.add_argument('--top_image_path', type=str, default=os.path.join(os.path.dirname(__file__), 'images/top_q.png'))
    parser.add_argument('--header_image_path', type=str, default=os.path.join(os.path.dirname(__file__), 'images/header_8bit.png'))
    parser.add_argument('--input_image_dir_path', type=str, default='~/Desktop/input_image')
    parser.add_argument('--bottom_background_image_path', type=str, default=os.path.join(os.path.dirname(__file__), 'images/black_bar.png'))
    parser.add_argument('--bottom_foreground_image_path', type=str, default=os.path.join(os.path.dirname(__file__), 'images/royalblue_bar.png'))
    parser.add_argument('--output_image_dir_path', type=str, default='~/Desktop/output_image')
    args = parser.parse_args()

    args.top_image_path = os.path.expanduser(args.top_image_path)
    args.header_image_path = os.path.expanduser(args.header_image_path)
    args.input_image_dir_path = os.path.expanduser(args.input_image_dir_path)
    args.bottom_background_image_path = os.path.expanduser(args.bottom_background_image_path)
    args.bottom_foreground_image_path = os.path.expanduser(args.bottom_foreground_image_path)
    args.output_image_dir_path = os.path.expanduser(args.output_image_dir_path)

    main(args.top_image_path, args.header_image_path, args.input_image_dir_path, args.bottom_background_image_path, args.bottom_foreground_image_path, args.output_image_dir_path)
