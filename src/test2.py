"""
DO NOT EDIT THIS FILE !!!
"""
import unittest

from test_utils import *
from seminar2 import *


class TestSoftmax(unittest.TestCase):
    """1 point"""
    def testSoftmax5(self):
        x = np.stack([np.ones(5), np.arange(5)])
        s = softmax(x)
        expected = np.array([
            [0.2, 0.2, 0.2, 0.2, 0.2],
            [0.01165623, 0.03168492, 0.08612854, 0.23412166, 0.63640865]
        ])
        self.assertTrue(np.allclose(expected, s, rtol=.01))

    def testSoftmax10(self):
        x = np.stack([np.arange(10), np.ones(10)])
        s = softmax(x)
        expected = np.array([
            [7.80134161e-05, 2.12062451e-04, 5.76445508e-04, 1.56694135e-03, 4.25938820e-03,
             1.15782175e-02, 3.14728583e-02, 8.55520989e-02, 2.32554716e-01, 6.32149258e-01],
            [.1, .1, .1, .1, .1, .1, .1, .1, .1, .1]
        ])
        self.assertTrue(np.allclose(expected, s, rtol=.01))


class TestSoftmaxLoss(unittest.TestCase):
    """1 point"""
    def testLoss2(self):
        x = np.ones((4, 3073)) * 100
        W = np.ones((3073, 2)) * 1e-3
        y = np.array([0, 0, 0, 0], dtype=int)
        loss, _ = softmax_loss_and_grad(W, x, y, 1.)
        print(loss)

    def testLoss10(self):
        x = np.ones((4, 3073)) * 100
        W = np.ones((3073, 10)) * 1e-3
        y = np.array([0, 0, 0, 0], dtype=int)
        loss, _ = softmax_loss_and_grad(W, x, y, 1.)
        print(loss)


class TestSoftmaxGrad(unittest.TestCase):
    """1 point"""
    def testDataGrad1(self):
        # Test batch_size = 1
        N, D, C = 1, 32, 10
        x = np.ones((N, D))
        W = np.ones((D, C)) * 1e-3
        y = [0]
        result = check_gradient(lambda w: softmax_loss_and_grad(w, x, y, 0), W)
        self.assertTrue(result)

    def testDataGrad8(self):
        # Test batch_size = 8
        N, D, C = 8, 32, 10
        x = np.ones((N, D))
        W = np.ones((D, C)) * 1e-3
        y = [0] * N
        result = check_gradient(lambda w: softmax_loss_and_grad(w, x, y, 0), W)
        self.assertTrue(result)

    def testRegularizationGrad(self):
        # Test reg = 100
        N, D, C = 1, 32, 10
        x = np.ones((N, D))
        W = np.ones((D, C)) * 1e-3
        y = [0]
        result = check_gradient(lambda w: softmax_loss_and_grad(w, x, y, 100), W)
        self.assertTrue(result)


class TestSoftmaxClassifier(unittest.TestCase):
    """2 points"""
    def testOverFitting(self):
        N_samples = 8
        (x_train, y_train), _ = get_preprocessed_data()
        dev_idx = np.random.choice(len(x_train), N_samples)
        X_dev, y_dev = x_train[dev_idx], y_train[dev_idx]

        cls = SoftmaxClassifier()
        loss_history = cls.train(X_dev, y_dev,
                                 learning_rate=1e-3, reg=0, num_iters=10000,
                                 batch_size=N_samples, verbose=True)
        self.assertLess(loss_history[-1], 1.0)
        self.assertGreater(loss_history[-1], 0.0)