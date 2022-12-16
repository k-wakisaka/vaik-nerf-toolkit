from tqdm import tqdm
import argparse
import os
import glob
import re
import tensorflow as tf
import tensorflow_addons as tfa
from PIL import Image


def pad(tf_image, div=16):
    padding_height = div - tf_image.shape[0] % div
    padding_width = div - tf_image.shape[1] % div
    tf_image = tf.pad(tf_image, tf.constant([[0, padding_height], [0, padding_width], [0, 0]]), "CONSTANT")
    return tf_image, (padding_height, padding_width)


def crop(tf_image, padding):
    return tf_image[:tf_image.shape[0] - padding[0], :tf_image.shape[1] - padding[1], :]


def predict(input_model_dir_path, input_image_dir_path, output_image_dir_path, rescale=255.):
    os.makedirs(output_image_dir_path, exist_ok=True)
    model = tf.keras.models.load_model(input_model_dir_path)

    image_path_list = sorted(
        [file_path for file_path in glob.glob(os.path.join(input_image_dir_path, '**/*.*'), recursive=True) if
         re.search('.*\.(png|jpg|bmp)$', file_path)])

    output_image_list = []
    for image_path in tqdm(image_path_list):
        tf_image = tf.image.decode_image(tf.io.read_file(image_path), channels=3)
        tf_image = tf.image.resize(tf_image, (tf_image.shape[0], tf_image.shape[1]))
        tf_image, padding = pad(tf_image)
        tf_image = tf.cast(tf_image, tf.float32) / rescale
        predict_image = tf.squeeze(model.predict(tf.expand_dims(tf_image, 0)), 0)
        predict_image = crop(predict_image, padding)
        predict_image = tf.cast(tf.clip_by_value(predict_image * rescale, 0., 255.), tf.uint8).numpy()
        output_image_list.append(predict_image)

    output_image_dir_path_0 = os.path.join(output_image_dir_path, 'images')
    os.makedirs(output_image_dir_path_0, exist_ok=True)
    output_image_dir_path_2 = os.path.join(output_image_dir_path, 'images_2')
    os.makedirs(output_image_dir_path_2, exist_ok=True)
    output_image_dir_path_4 = os.path.join(output_image_dir_path, 'images_4')
    os.makedirs(output_image_dir_path_4, exist_ok=True)
    output_image_dir_path_8 = os.path.join(output_image_dir_path, 'images_8')
    os.makedirs(output_image_dir_path_8, exist_ok=True)

    for image_path, output_image in zip(image_path_list, output_image_list):
        image = Image.fromarray(output_image)
        image.save(os.path.join(output_image_dir_path_0, os.path.basename(image_path)))

        image_2 = image.resize((image.width // 2, image.height // 2))
        image_2.save(os.path.join(output_image_dir_path_2, os.path.basename(image_path)))

        image_4 = image.resize((image.width // 4, image.height // 4))
        image_4.save(os.path.join(output_image_dir_path_4, os.path.basename(image_path)))

        image_8 = image.resize((image.width // 8, image.height // 8))
        image_8.save(os.path.join(output_image_dir_path_8, os.path.basename(image_path)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='predict')
    parser.add_argument('--input_model_dir_path', type=str,
                        default='~/Desktop/output_model/2022-12-10-17-00-29-unet-image-focal/step-1000_batch-8_epoch-97_loss_0.1055_val_loss_0.0788/model')
    parser.add_argument('--input_image_dir_path', type=str, default='/home/kentaro/Desktop/ref_suv_mask_data/mask_image')
    parser.add_argument('--output_image_dir_path', type=str, default='/home/kentaro/Desktop/ref_suv_mask_data/unet_mask_image')
    args = parser.parse_args()

    args.input_model_dir_path = os.path.expanduser(args.input_model_dir_path)
    args.input_image_dir_path = os.path.expanduser(args.input_image_dir_path)
    args.output_image_dir_path = os.path.expanduser(args.output_image_dir_path)

    predict(args.input_model_dir_path, args.input_image_dir_path, args.output_image_dir_path)
