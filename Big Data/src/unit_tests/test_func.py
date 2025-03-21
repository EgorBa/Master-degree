import configparser
import os
import unittest
import sys

import pandas as pd

sys.path.insert(1, os.path.join(os.getcwd(), "src"))

from train import KNNModel

config = configparser.ConfigParser()
config.read("config.ini")


class TestKNNModel(unittest.TestCase):

    def setUp(self) -> None:
        self.knn_model = KNNModel()

    def test_knn(self):
        project_path = os.path.join(os.getcwd(), "data")
        X = pd.read_csv(os.path.join(project_path, 'Func_test_penguins_X.csv'), index_col=0)
        y = pd.read_csv(os.path.join(project_path, 'Func_test_penguins_y.csv'), index_col=0)
        self.assertLess(0.85, self.knn_model.predict(X, y))


if __name__ == "__main__":
    unittest.main()
