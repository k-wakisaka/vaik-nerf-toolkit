from tqdm import tqdm
import argparse
import os
import glob
import re
import tensorflow as tf
import tensorflow_addons as tfa
from PIL import Image


def split(image_path_list, batch_frame=8):
    def _split(image_path_list, batch_frame=8):
        for index in range(0, len(image_path_list), batch_frame):
            yield image_path_list[index:index + batch_frame]

    split_image_path_list = list(_split(image_path_list, batch_frame))
    split_ex_image_path_list = []
    for split_index, image_path_list in enumerate(split_image_path_list):
        if len(image_path_list) < batch_frame and split_index > 0:
            split_ex_image_path_list.append(
                [split_image_path_list[split_index - 1][len(image_path_list):], image_path_list])
        else:
            split_ex_image_path_list.append([[], image_path_list])
    return split_ex_image_path_list


def pad(tf_image, div=16):
    padding_height = div - tf_image.shape[0] % div
    padding_width = div - tf_image.shape[1] % div
    tf_image = tf.pad(tf_image, tf.constant([[0, padding_height], [0, padding_width], [0, 0]]), "CONSTANT")
    return tf_image, (padding_height, padding_width)


def crop(tf_image, padding):
    return tf_image[:tf_image.shape[0] - padding[0], :tf_image.shape[1] - padding[1], :]


def inference(model, ex_image_path_list, rescale=255.):
    image_list = []
    padding_list = []
    for image_path in ex_image_path_list[0]:
        tf_image = tf.image.decode_image(tf.io.read_file(image_path), channels=3)
        tf_image, padding = pad(tf_image)
        tf_image = tf.cast(tf_image, tf.float32) / rescale
        image_list.append(tf_image)
        padding_list.append(padding)
    for image_path in ex_image_path_list[1]:
        tf_image = tf.image.decode_image(tf.io.read_file(image_path), channels=3)
        tf_image, padding = pad(tf_image)
        tf_image = tf.cast(tf_image, tf.float32) / rescale
        image_list.append(tf_image)
        padding_list.append(padding)
    tf_input_images = tf.stack(image_list)
    tf_output_images = tf.squeeze(model.predict(tf.expand_dims(tf_input_images, 0)), 0)
    output_image_list = []
    for frame_index in range(tf_output_images.shape[0]):
        predict_image = crop(tf_output_images[frame_index], padding_list[frame_index])
        predict_image = tf.cast(tf.clip_by_value(predict_image * rescale, 0., 255.), tf.uint8).numpy()
        output_image_list.append(predict_image)
    return output_image_list[len(ex_image_path_list[0]):]


def predict(input_model_dir_path, input_image_dir_path, output_image_dir_path, batch_frame=8, rescale=255.):
    os.makedirs(output_image_dir_path, exist_ok=True)
    model = tf.keras.models.load_model(input_model_dir_path)

    image_path_list = sorted(
        [file_path for file_path in glob.glob(os.path.join(input_image_dir_path, '**/*.*'), recursive=True) if
         re.search('.*\.(png|jpg|bmp)$', file_path)])

    split_ex_image_path_list = split(image_path_list, batch_frame)

    output_image_list = []
    for ex_image_path_list in tqdm(split_ex_image_path_list):
        sub_output_image_list = inference(model, ex_image_path_list)
        output_image_list.extend(sub_output_image_list)

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
                        default='~/Desktop/output_model/2022-12-12-17-50-52-unet3d-mse/step-1000_batch-1_epoch-91_loss_0.0047_val_loss_0.0108/model')
    parser.add_argument('--input_image_dir_path', type=str, default='~/Desktop/input_images')
    parser.add_argument('--output_image_dir_path', type=str, default='~/Desktop/output_images')
    args = parser.parse_args()

    args.input_model_dir_path = os.path.expanduser(args.input_model_dir_path)
    args.input_image_dir_path = os.path.expanduser(args.input_image_dir_path)
    args.output_image_dir_path = os.path.expanduser(args.output_image_dir_path)

    predict(args.input_model_dir_path, args.input_image_dir_path, args.output_image_dir_path)
