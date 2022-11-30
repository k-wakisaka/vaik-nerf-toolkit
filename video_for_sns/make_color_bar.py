from PIL import Image, ImageDraw, ImageFont
import argparse
import os


def main(height, width, color, output_image_path):
    os.makedirs(os.path.dirname(output_image_path), exist_ok=True)

    image = Image.new("RGB", (width, height), color)
    image.save(output_image_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='make color bar')
    parser.add_argument('--height', type=int, default=128)
    parser.add_argument('--width', type=int, default=1280)
    parser.add_argument('--color', type=str, default='crimson')
    parser.add_argument('--output_image_path', type=str, default='./images/crimson_bar.png')
    args = parser.parse_args()

    args.output_image_path = os.path.expanduser(args.output_image_path)

    main(args.height, args.width, args.color, args.output_image_path)
