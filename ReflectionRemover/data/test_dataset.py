import os.path
import unittest

from data import ref_mat_dataset


class TestUtils(unittest.TestCase):
    def test_train_dataset(self):
        data_set = ref_mat_dataset.TrainDataset(os.path.expanduser('~/Desktop/ReflectionRemoveData/train'))
        data = next(iter(data_set))
        ref_mat_dataset.dump(data[0], os.path.expanduser('~/Desktop/log/train'), 'reflection')
        ref_mat_dataset.dump(data[1], os.path.expanduser('~/Desktop/log/train'), 'mat')

    def test_valid_dataset(self):
        data_set = ref_mat_dataset.ValidDataset(os.path.expanduser('~/Desktop/ReflectionRemoveData/valid'))
        data = ref_mat_dataset.get_all_data(data_set, 10)
        ref_mat_dataset.dump(data[0], os.path.expanduser('~/Desktop/log/valid'), 'reflection')
        ref_mat_dataset.dump(data[1], os.path.expanduser('~/Desktop/log/valid'), 'mat')

if __name__ == "__main__":
    unittest.main()
