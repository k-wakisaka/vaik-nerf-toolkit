import os.path

import tensorflow as tf
import unittest

from video.models import simple, unet3d, unet2d, unet2d_tcn


class TestUtils(unittest.TestCase):
    def test_simple(self):
        model = simple.prepare((8, 512, 512, 3))
        output_model_path = os.path.expanduser('~/Desktop/simple_model.png')
        os.makedirs(os.path.dirname(output_model_path), exist_ok=True)
        tf.keras.utils.plot_model(model, output_model_path, show_shapes=True, show_layer_names=True, show_layer_activations=True)

    def test_unet3d(self):
        model = unet3d.prepare((8, 512, 512, 3))
        output_model_path = os.path.expanduser('~/Desktop/unet3d_model.png')
        os.makedirs(os.path.dirname(output_model_path), exist_ok=True)
        tf.keras.utils.plot_model(model, output_model_path, show_shapes=True, show_layer_names=True, show_layer_activations=True)

    def test_unet2d(self):
        model = unet2d.prepare((8, 512, 512, 3))
        output_model_path = os.path.expanduser('~/Desktop/unet2d_model.png')
        os.makedirs(os.path.dirname(output_model_path), exist_ok=True)
        tf.keras.utils.plot_model(model, output_model_path, show_shapes=True, show_layer_names=True, show_layer_activations=True)

    def test_unet2d_tcn(self):
        model = unet2d_tcn.prepare((8, 512, 512, 3))
        output_model_path = os.path.expanduser('~/Desktop/unet2d_tcn_model.png')
        os.makedirs(os.path.dirname(output_model_path), exist_ok=True)
        tf.keras.utils.plot_model(model, output_model_path, show_shapes=True, show_layer_names=True, show_layer_activations=True)

if __name__ == "__main__":
    unittest.main()
