from PIL import Image, ImageDraw, ImageFont
import argparse
import os


def main(text, start_x, height, width, font_size, font_name, font_color, output_image_path):
    os.makedirs(os.path.dirname(output_image_path), exist_ok=True)

    image = Image.new("RGB", (width, height), (0, 0, 0))
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype(os.path.join(os.path.dirname(__file__), font_name), font_size)
    draw.text((start_x, 60), text, fill=font_color, font=font)

    image.save(output_image_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='make string image')
    parser.add_argument('--text', type=str, default='A.3人乗り電動自転車')
    parser.add_argument('--start_x', type=int, default=30)
    parser.add_argument('--height', type=int, default=256)
    parser.add_argument('--width', type=int, default=1280)
    parser.add_argument('--font_size', type=int, default=130)
    parser.add_argument('--font_name', type=str, default='fonts-japanese-gothic.ttf')
    parser.add_argument('--font_color', type=str, default='gold')
    parser.add_argument('--output_image_path', type=str, default='images/top_a.png')
    args = parser.parse_args()

    args.output_image_path = os.path.expanduser(args.output_image_path)

    main(args.text, args.start_x, args.height, args.width, args.font_size, args.font_name, args.font_color, args.output_image_path)
