import tensorflow as tf
import glob
import os
import re
import random


def dump(data, output_dir_path):
    os.makedirs(output_dir_path, exist_ok=True)
    for index, image in enumerate(data):
        tf.keras.utils.save_img(os.path.join(output_dir_path, f'{index:04d}.png'), image)


class TrainDataset:
    image_shape = (1024, 1024, 3)
    crop_reflection_images_shape = (8, 512, 512, 3)
    crop_mat_images_shape = (8, 512, 512, 3)
    random_frame_max_range = 8
    output_signature = (
        tf.TensorSpec(name=f'crop_reflection_images', shape=crop_reflection_images_shape, dtype=tf.uint8),
        tf.TensorSpec(name=f'crop_mat_images', shape=crop_mat_images_shape, dtype=tf.uint8))
    image_dict = None

    def __new__(cls, input_dir_path):
        cls.image_dict = cls._prepare_image_dict(input_dir_path)
        dataset = tf.data.Dataset.from_generator(
            cls.generator,
            output_signature=cls.output_signature
        )
        return dataset

    @classmethod
    def _prepare_image_dict(cls, input_dir_path):
        image_dict = {}
        sub_dir_path_list = sorted(glob.glob(os.path.join(input_dir_path, '*/')))
        for index, sub_dir_path in enumerate(sub_dir_path_list):
            mat_image_path_list = sorted(
                [file_path for file_path in glob.glob(os.path.join(sub_dir_path, '**/*_mat_*.*'), recursive=True) if
                 re.search('.*\.(png|jpg|bmp)$', file_path)])
            reflection_image_path_list = sorted(
                [file_path for file_path in glob.glob(os.path.join(sub_dir_path, '**/*_ref_*.*'), recursive=True) if
                 re.search('.*\.(png|jpg|bmp)$', file_path)])
            image_dict[index] = {'reflection': reflection_image_path_list, 'mat': mat_image_path_list}
        return image_dict

    @classmethod
    def generator(cls):
        while True:
            crop_reflection_images = []
            crop_mat_images = []
            video_index = random.choice(list(cls.image_dict.keys()))
            target_frame_index = random.choice(range(len(cls.image_dict[video_index]['reflection'])))
            random_frame_start_index = max(0, target_frame_index - cls.random_frame_max_range // 2)
            random_frame_end_index = min(len(cls.image_dict[video_index]['reflection']) - 1,
                                         target_frame_index + cls.random_frame_max_range // 2)
            crop_start_y = random.randint(0, cls.image_shape[0] - cls.crop_reflection_images_shape[1] - 1)
            crop_start_x = random.randint(0, cls.image_shape[1] - cls.crop_reflection_images_shape[2] - 1)
            for batch_frame_index in range(cls.crop_reflection_images_shape[0]):
                random_frame_index = random.randint(random_frame_start_index, random_frame_end_index)

                reflection_tf_image = tf.image.decode_image(
                    tf.io.read_file(cls.image_dict[video_index]['reflection'][random_frame_index]), channels=3)
                reflection_tf_image = tf.image.resize(reflection_tf_image, (cls.image_shape[0], cls.image_shape[1]),
                                                      preserve_aspect_ratio=True)
                crop_reflection_tf_image = reflection_tf_image[
                                           crop_start_y:crop_start_y + cls.crop_reflection_images_shape[1],
                                           crop_start_x:crop_start_x + cls.crop_reflection_images_shape[2], :]
                crop_reflection_images.append(tf.cast(crop_reflection_tf_image, tf.uint8))

                mat_tf_image = tf.image.decode_image(
                    tf.io.read_file(cls.image_dict[video_index]['mat'][random_frame_index]), channels=3)
                mat_tf_image = tf.image.resize(mat_tf_image, (cls.image_shape[0], cls.image_shape[1]),
                                               preserve_aspect_ratio=True)
                crop_mat_tf_image = mat_tf_image[crop_start_y:crop_start_y + cls.crop_reflection_images_shape[1],
                                    crop_start_x:crop_start_x + cls.crop_reflection_images_shape[2], :]
                crop_mat_images.append(tf.cast(crop_mat_tf_image, tf.uint8))
            yield tf.stack(crop_reflection_images), tf.stack(crop_mat_images)
