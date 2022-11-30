from PIL import Image, ImageDraw, ImageFont
import argparse
import os


def main(string, font_size, font_color, output_image_path, font_name):
    os.makedirs(os.path.dirname(output_image_path), exist_ok=True)

    height = int(font_size * 1.2)
    width = int(height * len(string) / 1.25)
    image = Image.new("RGB", (width, height), (0, 0, 0))
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype(os.path.join(os.path.dirname(__file__), font_name), font_size)
    draw.text((font_size // 5, 0), string, fill=font_color, font=font)

    image.save(output_image_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='make string image')
    parser.add_argument('--string', type=str, default='A. 三角')
    parser.add_argument('--font_size', type=int, default=100)
    parser.add_argument('--font_color', type=str, default='red')
    parser.add_argument('--output_image_path', type=str, default='images/answer_red.png')
    parser.add_argument('--font_name', type=str, default='HannariMincho-Regular.otf')
    args = parser.parse_args()

    args.output_image_path = os.path.expanduser(args.output_image_path)

    main(args.string, args.font_size, args.font_color, args.output_image_path, args.font_name)
