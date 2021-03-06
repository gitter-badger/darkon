"""Copyright 2017 Neosapience, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import unittest

import darkon
import numpy as np

_num_train_data = 20
_dim_features = 5
_num_test_data = 3
_classes = 2


class MyFeeder(darkon.InfluenceFeeder):
    def __init__(self):
        self.train_x = np.random.uniform(size=_num_train_data * _dim_features).reshape([_num_train_data, -1])
        self.train_y = np.random.randint(_classes, size=_num_train_data).reshape([-1])
        self.test_x = np.random.uniform(size=_num_test_data * _dim_features).reshape([_num_test_data, -1])
        self.test_y = np.random.randint(_classes, size=_num_test_data).reshape([-1])

        self.train_y = np.eye(_classes)[self.train_y]
        self.test_y = np.eye(_classes)[self.test_y]

    def reset(self):
        np.random.seed(97)

    def train_batch(self, batch_size):
        idx = np.random.choice(_num_train_data - batch_size + 1, 1)[0]
        return self.train_x[idx:idx + batch_size], self.train_y[idx:idx + batch_size]

    def train_one(self, index):
        return self.train_x[index], self.train_y[index]

    def test_indices(self, indices):
        return self.test_x[indices], self.test_y[indices]


class InfluenceFeeder(unittest.TestCase):
    def test_feeder_reset(self):
        feeder = MyFeeder()
        feeder.reset()
        data1 = np.array(feeder.train_batch(4)[0])
        data1_next = np.array(feeder.train_batch(4)[0])
        self.assertFalse(np.all(data1 == data1_next))

        feeder.reset()
        data2 = np.array(feeder.train_batch(4)[0])
        data2_next = np.array(feeder.train_batch(4)[0])
        self.assertTrue(np.all(data1 == data2))
        self.assertTrue(np.all(data1_next == data2_next))
