import tensorflow as tf
import glob
import os
import re
import random
from tqdm import tqdm

def dump(data, output_dir_path, suffix='video.data', rescale=255.):
    if len(data.shape) == 4:
        data = tf.expand_dims(data, axis=0)
    for batch_index in range(data.shape[0]):
        for frame_index, image in enumerate(data[batch_index]):
            sub_output_dir_path = os.path.join(output_dir_path, f'batch_{batch_index:04d}')
            os.makedirs(sub_output_dir_path, exist_ok=True)
            tf.keras.utils.save_img(os.path.join(sub_output_dir_path, f'frame_{frame_index:04d}_{suffix}.png'), image*rescale)


class TrainDataset:
    image_shape = (1024, 1024, 3)
    crop_reflection_images_shape = (8, 512, 512, 3)
    crop_mat_images_shape = (8, 512, 512, 3)
    random_frame_max_range = 8
    output_signature = (
        tf.TensorSpec(name=f'crop_reflection_images', shape=crop_reflection_images_shape, dtype=tf.float32),
        tf.TensorSpec(name=f'crop_mat_images', shape=crop_mat_images_shape, dtype=tf.float32))
    image_dict = None

    def __new__(cls, input_dir_path):
        cls.image_dict = cls._prepare_image_dict(input_dir_path)
        dataset = tf.data.Dataset.from_generator(
            cls._generator,
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
    def _generator(cls):
        while True:
            crop_reflection_images = []
            crop_mat_images = []
            video_index = random.choice(list(cls.image_dict.keys()))
            target_frame_index = random.choice(range(len(cls.image_dict[video_index]['reflection'])-cls.crop_reflection_images_shape[0]))
            crop_start_y = random.randint(0, cls.image_shape[0] - cls.crop_reflection_images_shape[1] - 1)
            crop_start_x = random.randint(0, cls.image_shape[1] - cls.crop_reflection_images_shape[2] - 1)
            is_reverse = random.uniform(0, 1.0) > 0.5
            for batch_frame_index in range(cls.crop_reflection_images_shape[0]):
                if is_reverse:
                    random_frame_index = target_frame_index + cls.crop_reflection_images_shape[0] - batch_frame_index
                else:
                    random_frame_index = target_frame_index + batch_frame_index

                reflection_tf_image = tf.image.decode_image(tf.io.read_file(cls.image_dict[video_index]['reflection'][random_frame_index]), channels=3)
                reflection_tf_image = tf.image.resize(reflection_tf_image, (cls.image_shape[0], cls.image_shape[1]),
                                                      preserve_aspect_ratio=True)
                crop_reflection_tf_image = reflection_tf_image[
                                           crop_start_y:crop_start_y + cls.crop_reflection_images_shape[1],
                                           crop_start_x:crop_start_x + cls.crop_reflection_images_shape[2], :]
                crop_reflection_images.append(crop_reflection_tf_image/255.)

                mat_tf_image = tf.image.decode_image(
                    tf.io.read_file(cls.image_dict[video_index]['mat'][random_frame_index]), channels=3)
                mat_tf_image = tf.image.resize(mat_tf_image, (cls.image_shape[0], cls.image_shape[1]),
                                               preserve_aspect_ratio=True)
                crop_mat_tf_image = mat_tf_image[crop_start_y:crop_start_y + cls.crop_reflection_images_shape[1],
                                    crop_start_x:crop_start_x + cls.crop_reflection_images_shape[2], :]
                crop_mat_images.append(crop_mat_tf_image/255.)
            yield tf.stack(crop_reflection_images), tf.stack(crop_mat_images)


class ValidDataset(TrainDataset):
    def __new__(cls, input_dir_path):
        return super(ValidDataset, cls).__new__(cls, input_dir_path)

def get_all_data(dataset, max_sample_num):
    dataset = iter(dataset)
    data_list = []
    sample_num = 0
    for data in tqdm(dataset, desc=f'prepare {max_sample_num} valid samples'):
        data_list.append(data)
        sample_num += 1
        if sample_num >= max_sample_num:
            break
    all_data_list = [None for _ in range(len(data_list[0]))]
    for index in range(len(data_list[0])):
        all_data_list[index] = tf.stack([data[index] for data in data_list])
    return tuple(all_data_list)