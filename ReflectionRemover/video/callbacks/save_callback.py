import os
import tensorflow as tf

from video.data import ref_mat_dataset


class SaveCallback(tf.keras.callbacks.Callback):
    def __init__(self, save_model_dir_path, prefix, train_valid_data, valid_data):
        super(SaveCallback, self).__init__()
        os.makedirs(save_model_dir_path, exist_ok=True)

        self.save_model_dir_path = save_model_dir_path
        self.prefix = prefix
        self.train_valid_data = train_valid_data
        self.valid_data = valid_data

    def on_epoch_end(self, epoch, logs=None):
        loss_string = "_".join([f'{k}_{v:.4f}' for k, v in logs.items()])
        save_model_name = f'{self.prefix}_epoch-{epoch}_{loss_string}'
        output_model_dir_path = os.path.join(self.save_model_dir_path, save_model_name, 'model')
        os.makedirs(output_model_dir_path, exist_ok=True)
        self.model.save(output_model_dir_path)

        output_image_dir_path = os.path.join(self.save_model_dir_path, save_model_name, 'output_image')

        # train_valid
        train_valid_output_image_dir_path = os.path.join(output_image_dir_path, 'train')
        os.makedirs(train_valid_output_image_dir_path, exist_ok=True)
        predict_train_valid_data = self.predict(self.train_valid_data[0])
        diff_train_valid_data = tf.abs(self.train_valid_data[1]-predict_train_valid_data)
        ref_mat_dataset.dump(self.train_valid_data[0], train_valid_output_image_dir_path, '01_reflection')
        ref_mat_dataset.dump(predict_train_valid_data, train_valid_output_image_dir_path, '02_predict')
        ref_mat_dataset.dump(self.train_valid_data[1], train_valid_output_image_dir_path, '03_mat')
        ref_mat_dataset.dump(diff_train_valid_data, train_valid_output_image_dir_path, '04_diff')

        # valid
        valid_output_image_dir_path = os.path.join(output_image_dir_path, 'valid')
        os.makedirs(valid_output_image_dir_path, exist_ok=True)
        predict_valid_data = self.predict(self.valid_data[0])
        diff_valid_data = tf.abs(self.valid_data[1]-predict_valid_data)
        ref_mat_dataset.dump(self.valid_data[0], valid_output_image_dir_path, '01_reflection')
        ref_mat_dataset.dump(predict_valid_data, valid_output_image_dir_path, '02_predict')
        ref_mat_dataset.dump(self.valid_data[1], valid_output_image_dir_path, '03_mat')
        ref_mat_dataset.dump(diff_valid_data, valid_output_image_dir_path, '04_diff')

    def predict(self, data):
        output_data = []
        for batch_index in range(data.shape[0]):
                output_data.append(tf.squeeze(self.model.predict(tf.expand_dims(data[batch_index], 0)), 0))
        return tf.stack(output_data)