from PIL import Image
import argparse
import os
import re
import glob
import cv2
import numpy as np


def resize(image, resize_sub_pixel):
    if resize_sub_pixel == 1:
        return image
    else:
        resize_image = image.resize((image.size[0] // resize_sub_pixel, image.size[1] // resize_sub_pixel), Image.BILINEAR)
        result_image = resize_image.resize(image.size, Image.NEAREST)
        return result_image


def quantize(image, quantize_bit):
    if quantize_bit == 1:
        gray_image = np.asarray(image.convert('L'))
        ret, th = cv2.threshold(gray_image, 0, 255, cv2.THRESH_OTSU)
        color_image = Image.fromarray(th).convert('RGB')
        return color_image
    elif quantize_bit == 32:
        return image
    else:
        return image.quantize(2**int(quantize_bit/4*3))

def main(input_image_dir_path, resize_sub_pixel, quantize_bit, output_image_dir_path):
    os.makedirs(output_image_dir_path, exist_ok=True)

    image_path_list = sorted(
        [file_path for file_path in glob.glob(os.path.join(input_image_dir_path, '**/*.*'), recursive=True) if
         re.search('.*\.(png|jpg|bmp)$', file_path)])

    for image_path in image_path_list:
        org_image = Image.open(open(image_path, 'rb')).convert('RGB')
        resize_image = resize(org_image, resize_sub_pixel)
        quantize_image = quantize(resize_image, quantize_bit)
        quantize_image.save(os.path.join(output_image_dir_path, os.path.basename(image_path)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='convert pixel art')
    parser.add_argument('--input_image_dir_path', type=str, default='~/Desktop/input_image')
    parser.add_argument('--resize_sub_pixel', type=int, default=24, choices=[24, 12, 1])
    parser.add_argument('--quantize_bit', type=int, default=8, choices=[1, 8, 32])
    parser.add_argument('--output_image_dir_path', type=str, default='~/Desktop/output_image')
    args = parser.parse_args()

    args.input_image_dir_path = os.path.expanduser(args.input_image_dir_path)
    args.output_image_dir_path = os.path.expanduser(args.output_image_dir_path)

    main(args.input_image_dir_path, args.resize_sub_pixel, args.quantize_bit, args.output_image_dir_path)
