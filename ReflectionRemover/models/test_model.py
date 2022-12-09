import os.path

import tensorflow as tf
import unittest

from models import simple


class TestUtils(unittest.TestCase):
    def test_predict(self):
        model = simple.prepare((8, 512, 512, 3))
        output_model_path = os.path.expanduser('~/Desktop/model.png')
        os.makedirs(os.path.dirname(output_model_path), exist_ok=True)
        tf.keras.utils.plot_model(model, output_model_path, show_shapes=True, show_layer_names=True, show_layer_activations=True)


if __name__ == "__main__":
    unittest.main()
