import argparse
from datetime import datetime
import pytz

from data import ref_mat_dataset
from models import unet
from callbacks import save_callback
import tensorflow as tf
import numpy as np
import random
import os

physical_devices = tf.config.list_physical_devices('GPU')
if len(physical_devices) > 0:
    for device in physical_devices:
        tf.config.experimental.set_memory_growth(device, True)
        print('{} memory growth: {}'.format(device, tf.config.experimental.get_memory_growth(device)))
else:
    print("Not enough GPU hardware devices available")

def set_seed(seed=777):
    tf.random.set_seed(seed)
    np.random.seed(seed)
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)


MODEL_DICT = {
    'unet': unet.prepare
}


def train(train_input_dir_path, valid_input_dir_path, load_model_dir_path, model_type, epochs, step_size, batch_size, test_max_sample,
          output_dir_path):
    # train
    TrainDataset = type(f'TrainDataset', (ref_mat_dataset.TrainDataset,), dict())
    train_dataset = TrainDataset(train_input_dir_path)
    train_dataset = train_dataset.padded_batch(batch_size=batch_size, padding_values=(
        tf.constant(0, dtype=tf.float32), tf.constant(0, dtype=tf.float32)))

    # train valid
    TrainValidDataset = type(f'TrainValidDataset', (ref_mat_dataset.ValidDataset,), dict())
    train_valid_dataset = TrainValidDataset(train_input_dir_path)
    train_valid_data = ref_mat_dataset.get_all_data(train_valid_dataset, test_max_sample)

    # valid
    ValidDataset = type(f'ValidDataset', (ref_mat_dataset.ValidDataset,), dict())
    valid_dataset = ValidDataset(valid_input_dir_path)
    valid_data = ref_mat_dataset.get_all_data(valid_dataset, test_max_sample)

    if load_model_dir_path is not None:
        model = tf.keras.models.load_model(load_model_dir_path)
    else:
        model = MODEL_DICT[model_type]((None, None, 3))

    save_model_dir_path = os.path.join(output_dir_path,
                                       f'{datetime.now(pytz.timezone("Asia/Tokyo")).strftime("%Y-%m-%d-%H-%M-%S")}')
    prefix = f'step-{step_size}_batch-{batch_size}'
    callback = save_callback.SaveCallback(save_model_dir_path=save_model_dir_path, prefix=prefix,
                                          train_valid_data=train_valid_data, valid_data=valid_data)
    model.summary()
    model.fit_generator(train_dataset, steps_per_epoch=step_size,
                        epochs=epochs,
                        validation_data=valid_data,
                        callbacks=[callback])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='train')
    parser.add_argument('--train_input_dir_path', type=str, default='~/Desktop/ReflectionRemoveData/train')
    parser.add_argument('--valid_input_dir_path', type=str, default='~/Desktop/ReflectionRemoveData/valid')
    parser.add_argument('--load_model_dir_path', type=str, default='~/Desktop/output_model/2022-12-16-17-40-54/step-2500_batch-8_epoch-17_loss_0.0006_val_loss_0.0027/model')
    parser.add_argument('--model_type', type=str, default='unet')
    parser.add_argument('--epochs', type=int, default=1000)
    parser.add_argument('--step_size', type=int, default=2500)
    parser.add_argument('--batch_size', type=int, default=8)
    parser.add_argument('--test_max_sample', type=int, default=64)
    parser.add_argument('--output_dir_path', type=str, default='~/Desktop/output_model')
    args = parser.parse_args()

    args.train_input_dir_path = os.path.expanduser(args.train_input_dir_path)
    args.valid_input_dir_path = os.path.expanduser(args.valid_input_dir_path)
    args.load_model_dir_path = os.path.expanduser(args.load_model_dir_path)
    args.output_dir_path = os.path.expanduser(args.output_dir_path)
    os.makedirs(args.output_dir_path, exist_ok=True)

    train(args.train_input_dir_path, args.valid_input_dir_path,  args.load_model_dir_path, args.model_type,
          args.epochs, args.step_size, args.batch_size, args.test_max_sample, args.output_dir_path)
