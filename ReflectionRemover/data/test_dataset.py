import os.path
import unittest

from data import ref_mat_dataset


class TestUtils(unittest.TestCase):
    def test_predict(self):
        data_set = ref_mat_dataset.TrainDataset(os.path.expanduser('~/Desktop/ReflectionRemoveData/train'))
        data = next(iter(data_set))
        ref_mat_dataset.dump(data[0], os.path.expanduser('~/Desktop/log_reflection'))
        ref_mat_dataset.dump(data[1], os.path.expanduser('~/Desktop/log_mat'))


if __name__ == "__main__":
    unittest.main()
