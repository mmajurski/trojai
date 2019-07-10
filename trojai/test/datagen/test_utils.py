import unittest
import numpy as np
from numpy.random import RandomState
import tempfile
import shutil

from trojai.datagen import utils
from trojai.datagen.transform import Transform
from trojai.datagen.entity import GenericEntity


class DummyTransform_Add(Transform):
    def __init__(self, add_const):
        self.add_const = add_const
    def do(self, input_obj, random_state_obj):
        img = input_obj.get_data()
        img += self.add_const
        return GenericEntity(img, input_obj.get_mask())

class DummyTransform_Multiply(Transform):
    def __init__(self, multiply_const):
        self.multiply_const = multiply_const
    def do(self, input_obj, random_state_obj):
        img = input_obj.get_data()
        img *= self.multiply_const
        return GenericEntity(img, input_obj.get_mask())


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.clean_dataset_rootdir = tempfile.mkdtemp()

    def tearDown(self) -> None:
        try:
            shutil.rmtree(self.clean_dataset_rootdir)
        except:
            pass

    def test_process_xform_list(self):
        """
        Tests that all supplied list of serial transforms are processed
        :return:None
        """
        img = GenericEntity(np.linspace(0, 10, 100))
        xforms = [DummyTransform_Add(1), DummyTransform_Multiply(2)]
        img_expected = (img.get_data() + 1) * 2
        img_actual = utils.process_xform_list(img, xforms, RandomState())
        self.assertTrue(np.allclose(img_actual.get_data(), img_expected))


if __name__ == '__main__':
    unittest.main()