# MIT License
#
# Copyright (C) IBM Corporation 2019
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
# Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""
This module implements the Functionally Equivalent Extraction attack mainly following Jagielski et al, 2019.

This module contains en example application for MNIST which can be run as `python functionally_equivalent_extraction.py`
producing output like:

Target model - Test accuracy: 0.9259
Extracted model - Test accuracy: 0.9259
Extracted model - Test Fidelity: 0.9977

| Paper link: https://arxiv.org/abs/1909.01838
"""

import os
import logging

import numpy as np
from scipy.optimize import least_squares

from art.attacks.attack import ExtractionAttack
from art.classifiers import KerasClassifier, BlackBoxClassifier

NUMPY_DTYPE = np.float64

logger = logging.getLogger(__name__)


class FunctionallyEquivalentExtraction(ExtractionAttack):
    """
    This module implements the Functionally Equivalent Extraction attack for neural networks with two dense layers,
    ReLU activation at the first layer and logits output after the second layer.

    | Paper link: https://arxiv.org/abs/1909.01838
    """

    def __init__(self, classifier, num_neurons):
        """
        Create a `FunctionallyEquivalentExtraction` instance.

        :param classifier: A trained ART classifier.
        :type classifier: :class:`.Classifier`
        :param num_neurons: The number of neurons in the first dense layer.
        :type num_neurons: `int`
        """
        super().__init__(classifier)
        self.num_neurons = num_neurons
        self.num_classes = classifier.nb_classes()
        self.num_features = int(np.prod(classifier.input_shape))

        self.vector_u = np.random.normal(0, 1, (1, self.num_features)).astype(dtype=NUMPY_DTYPE)
        self.vector_v = np.random.normal(0, 1, (1, self.num_features)).astype(dtype=NUMPY_DTYPE)

        self.critical_points = list()

        self.w_0 = None  # Weight matrix of first dense layer
        self.b_0 = None  # Bias vector of first dense layer
        self.w_1 = None  # weight matrix of second dense layer
        self.b_1 = None  # Bias vector of second dense layer

    def extract(self, x, y=None, delta_0=0.05, fraction_true=0.3, rel_diff_slope=0.00001, rel_diff_value=0.000001,
                delta_init_value=0.1, delta_value_max=50, d2_min=0.0004, d_step=0.01, delta_sign=0.02,
                unit_vector_scale=10000, **kwargs):
        """
        Extract the targeted model.

        :param x: Samples of input data of shape (num_samples, num_features).
        :type x: `np.ndarray`
        :param y: Correct labels or target labels for `x`, depending if the attack is targeted
               or not. This parameter is only used by some of the attacks.
        :type y: `np.ndarray`
        :param delta_0: Initial step size of binary search
        :type delta_0: `float`
        :param fraction_true: Fraction of output predictions that have to fulfill criteria for critical point
        :type fraction_true: `float`
        :param rel_diff_slope: Relative slope difference at critical points
        :type rel_diff_slope: `float`
        :param rel_diff_value: Relative value difference at critical points
        :type rel_diff_value: `float`
        :param delta_init_value: Initial delta of weight value search
        :type delta_init_value: `float`
        :param delta_value_max: Maximum delta  of weight value search
        :type delta_value_max: `float`
        :param d2_min: Minimum acceptable value of sum of absolute second derivatives
        :type d2_min: `float`
        :param d_step:  Step size of delta increase
        :type d_step: `float`
        :param delta_sign: Delta of weight sign search
        :type delta_sign: `float`
        :param unit_vector_scale: Multiplicative scale of the unit vector e_j.
        :type unit_vector_scale: `int`

        :return: ART BlackBoxClassifier of the extracted model.
        :rtype: :class:`.BlackBoxClassifier`
        """
        self._critical_point_search(delta_0=delta_0, fraction_true=fraction_true, rel_diff_slope=rel_diff_slope,
                                    rel_diff_value=rel_diff_value)
        self._weight_recovery(delta_init_value=delta_init_value, delta_value_max=delta_value_max, d2_min=d2_min,
                              d_step=d_step, delta_sign=delta_sign)
        self._sign_recovery(unit_vector_scale=unit_vector_scale)
        self._last_layer_extraction(x)

        def predict(x):
            """
            Predict extracted model.

            :param x: Samples of input data of shape (num_samples, num_features)
            :type x: `np.ndarray`

            :return: Predictions with the extracted model of shape (num_samples, num_classes)
            :rtype: `np.ndarray`
            """
            layer_0 = np.maximum(np.matmul(self.w_0.T, x.T) + self.b_0, 0.0)
            layer_1 = np.matmul(self.w_1.T, layer_0) + self.b_1
            return layer_1.T

        extracted_classifier = BlackBoxClassifier(predict, input_shape=self.classifier.input_shape,
                                                  nb_classes=self.classifier.nb_classes(),
                                                  clip_values=self.classifier.clip_values,
                                                  defences=self.classifier.defences,
                                                  preprocessing=self.classifier.preprocessing)

        return extracted_classifier

    def _o_l(self, x, e_j=None):
        """
        Predict the target model.

        :param x: Samples of input data of shape (num_samples, num_features)
        :type x: `np.ndarray`
        :param e_j: Additive delta vector of shape (1, num_features)
        :type e_j: `np.ndarray`
        :return: Prediction of the target model of shape (num_samples, num_classes)
        :rtype: `np.ndarray`
        """
        if e_j is not None:
            x = x + e_j
        return self.classifier.predict(x).astype(NUMPY_DTYPE)

    def _get_x(self, var_t):
        """
        Get input sample as function of multiplicative factor of random vector.

        :param var_t: Multiplicative factor of second random vector for critical point search
        :type var_t: `float`
        :return: Input sample of shape (1, num_features)
        :rtype: `np.ndarray`
        """
        return self.vector_u + var_t * self.vector_v

    def _critical_point_search(self, delta_0, fraction_true, rel_diff_slope, rel_diff_value):
        """
        Search for critical points.

        :param delta_0: Initial step size of binary search
        :type delta_0: `float`
        :param fraction_true: Fraction of output predictions that have to fulfill criteria for critical point
        :type fraction_true: `float`
        :param rel_diff_slope: Relative slope difference at critical points
        :type rel_diff_slope: `float`
        :param rel_diff_value: Relative value difference at critical points
        :type rel_diff_value: `float`
        """
        logger.info('Searching for critical points.')
        h_square = self.num_neurons * self.num_neurons

        t_current = -h_square
        while t_current < h_square:

            delta = delta_0
            found_critical_point = False

            while not found_critical_point:

                epsilon = delta / 10

                t_1 = t_current
                t_2 = t_current + delta

                x_1 = self._get_x(t_1)
                x_1_p = self._get_x(t_1 + epsilon)
                x_2 = self._get_x(t_2)
                x_2_m = self._get_x(t_2 - epsilon)

                m_1 = (self._o_l(x_1_p) - self._o_l(x_1)) / epsilon
                m_2 = (self._o_l(x_2) - self._o_l(x_2_m)) / epsilon

                y_1 = self._o_l(x_1)
                y_2 = self._o_l(x_2)

                if np.sum(np.abs((m_1 - m_2) / m_1) < rel_diff_slope) > fraction_true * self.num_classes:
                    t_current = t_2
                    break

                t_hat = t_1 + np.divide(y_2 - y_1 - (t_2 - t_1) * m_2, m_1 - m_2)
                y_hat = y_1 + m_1 * np.divide(y_2 - y_1 - (t_2 - t_1) * m_2, m_1 - m_2)

                t_mean = np.mean(t_hat[t_hat != -np.inf])

                x_mean = self._get_x(t_mean)
                x_mean_p = self._get_x(t_mean + epsilon)
                x_mean_m = self._get_x(t_mean - epsilon)

                y = self._o_l(x_mean)

                m_x_1 = (self._o_l(x_mean_p) - self._o_l(x_mean)) / epsilon
                m_x_2 = (self._o_l(x_mean) - self._o_l(x_mean_m)) / epsilon

                if np.sum(np.abs((y_hat - y) / y) < rel_diff_value) > fraction_true * self.num_classes \
                        and t_1 < t_mean < t_2 \
                        and np.sum(np.abs((m_x_1 - m_x_2) / m_x_1) > rel_diff_slope) > fraction_true * self.num_classes:
                    found_critical_point = True
                    self.critical_points.append(x_mean)
                    t_current = t_2
                else:
                    delta = delta / 2

        if len(self.critical_points) != self.num_neurons:
            raise AssertionError('The number of critical points found ({}) does not equal the number of expected'
                                 'neurons in the first layer ({}).'.format(len(self.critical_points), self.num_neurons))

    def _weight_recovery(self, delta_init_value, delta_value_max, d2_min, d_step, delta_sign):
        """
        Recover the weights and biases of the first layer.

        :param delta_init_value: Initial delta of weight value search
        :type delta_init_value: `float`
        :param delta_value_max: Maximum delta  of weight value search
        :type delta_value_max: `float`
        :param d2_min: Minimum acceptable value of sum of absolute second derivatives
        :type d2_min: `float`
        :param d_step:  Step size of delta increase
        :type d_step: `float`
        :param delta_sign: Delta of weight sign search
        :type delta_sign: `float`
        """
        logger.info('Recovering weights of first layer.')

        # Absolute Value Recovery

        d2_ol_d2ej_xi = np.zeros((self.num_features, self.num_neurons), dtype=NUMPY_DTYPE)

        for i in range(self.num_neurons):
            for j in range(self.num_features):

                delta = delta_init_value
                e_j = np.zeros((1, self.num_features))
                d2_ol_d2ej_xi_ok = False

                while not d2_ol_d2ej_xi_ok:

                    e_j[0, j] = delta

                    d_ol_dej_xi_p_cej = (self._o_l(self.critical_points[i], e_j=e_j)
                                         - self._o_l(self.critical_points[i])) / delta
                    d_ol_dej_xi_m_cej = (self._o_l(self.critical_points[i])
                                         - self._o_l(self.critical_points[i], e_j=-e_j)) / delta

                    d2_ol_d2ej_xi[j, i] = np.sum(np.abs(d_ol_dej_xi_p_cej - d_ol_dej_xi_m_cej)) / delta

                    if d2_ol_d2ej_xi[j, i] < d2_min and delta < delta_value_max:
                        delta = delta + d_step
                    else:
                        d2_ol_d2ej_xi_ok = True

        self.a0_pairwise_ratios = np.zeros((self.num_features, self.num_neurons), dtype=NUMPY_DTYPE)

        for i in range(self.num_neurons):
            for k in range(self.num_features):
                self.a0_pairwise_ratios[k, i] = d2_ol_d2ej_xi[0, i] / d2_ol_d2ej_xi[k, i]

        # Weight Sign Recovery

        for i in range(self.num_neurons):
            d2_ol_dejek_xi_0 = None
            for j in range(self.num_features):

                e_j = np.zeros((1, self.num_features), dtype=NUMPY_DTYPE)

                e_j[0, 0] += delta_sign
                e_j[0, j] += delta_sign

                d_ol_dejek_xi_p_cejek = (self._o_l(self.critical_points[i], e_j=e_j)
                                         - self._o_l(self.critical_points[i])) / delta_sign
                d_ol_dejek_xi_m_cejek = (self._o_l(self.critical_points[i])
                                         - self._o_l(self.critical_points[i], e_j=-e_j)) / delta_sign

                d2_ol_dejek_xi = (d_ol_dejek_xi_p_cejek - d_ol_dejek_xi_m_cejek)

                if j == 0:
                    d2_ol_dejek_xi_0 = d2_ol_dejek_xi / 2.0

                co_p = np.sum(np.abs(d2_ol_dejek_xi_0 * (1 + 1 / self.a0_pairwise_ratios[j, i]) - d2_ol_dejek_xi))
                co_m = np.sum(np.abs(d2_ol_dejek_xi_0 * (1 - 1 / self.a0_pairwise_ratios[j, i]) - d2_ol_dejek_xi))

                if co_m < co_p * np.max(1 / self.a0_pairwise_ratios[:, i]):
                    self.a0_pairwise_ratios[j, i] *= -1

    def _sign_recovery(self, unit_vector_scale):
        """
        Recover the sign of weights in the first layer.

        :param unit_vector_scale: Multiplicative scale of the unit vector e_j.
        :type unit_vector_scale: `int`
        """
        logger.info('Recover sign of the weights of the first layer.')

        a0_pairwise_ratios_inverse = 1.0 / self.a0_pairwise_ratios

        self.b_0 = np.zeros((self.num_neurons, 1), dtype=NUMPY_DTYPE)

        for i in range(self.num_neurons):
            x_i = self.critical_points[i].flatten()
            self.b_0[i] = - np.matmul(a0_pairwise_ratios_inverse[:, i], x_i)

        z_0 = np.random.normal(0, 1, (self.num_features,)).astype(dtype=NUMPY_DTYPE)

        def f_z(z_i):
            return np.squeeze(np.matmul(a0_pairwise_ratios_inverse.T, np.expand_dims(z_i, axis=0).T) + self.b_0)

        result_z = least_squares(f_z, z_0)

        for i in range(self.num_neurons):

            e_i = np.zeros((self.num_neurons, 1), dtype=NUMPY_DTYPE)
            e_i[i, 0] = unit_vector_scale

            def f_v(v_i):
                # pylint: disable=W0640
                return np.squeeze(np.matmul(-a0_pairwise_ratios_inverse.T, np.expand_dims(v_i, axis=0).T) - e_i)

            v_0 = np.random.normal(0, 1, self.num_features)

            result_v_i = least_squares(f_v, v_0)

            value_p = np.sum(np.abs(self._o_l(np.expand_dims(result_z.x, axis=0))
                                    - (self._o_l(np.expand_dims(result_z.x + result_v_i.x, axis=0)))))
            value_m = np.sum(np.abs(self._o_l(np.expand_dims(result_z.x, axis=0))
                                    - (self._o_l(np.expand_dims(result_z.x - result_v_i.x, axis=0)))))

            if value_m < value_p:
                a0_pairwise_ratios_inverse[:, i] *= -1
                self.b_0[i, 0] *= -1

        self.w_0 = a0_pairwise_ratios_inverse

    def _last_layer_extraction(self, x):
        """
        Extract weights and biases of the second layer.

        :param x: Samples of input data of shape (num_samples, num_features).
        :type x: `np.ndarray`
        """
        logger.info('Extract second layer.')

        predictions = self._o_l(x)

        w_1_b_1_0 = np.random.normal(0, 1, ((self.num_neurons + 1) * self.num_classes)).astype(dtype=NUMPY_DTYPE)

        def f_w_1_b_1(w_1_b_1_i):
            layer_0 = np.maximum(np.matmul(self.w_0.T, x.T) + self.b_0, 0.0)

            w_1 = w_1_b_1_i[0:self.num_neurons * self.num_classes].reshape(self.num_neurons, self.num_classes)
            b_1 = w_1_b_1_i[self.num_neurons * self.num_classes:].reshape(self.num_classes, 1)

            layer_1 = np.matmul(w_1.T, layer_0) + b_1

            return np.squeeze((layer_1.T - predictions).flatten())

        result_a1_b1 = least_squares(f_w_1_b_1, w_1_b_1_0)

        self.w_1 = result_a1_b1.x[0:self.num_neurons * self.num_classes].reshape(self.num_neurons, self.num_classes)
        self.b_1 = result_a1_b1.x[self.num_neurons * self.num_classes:].reshape(self.num_classes, 1)


# pylint: disable=C0103, E0401
if __name__ == '__main__':
    import tensorflow as tf

    tf.compat.v1.disable_eager_execution()

    from tensorflow.keras.datasets import mnist
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Dense

    np.random.seed(0)

    number_neurons = 16

    batch_size = 128
    number_classes = 10
    epochs = 10
    img_rows = 28
    img_cols = 28
    number_channels = 1

    (x_train, y_train), (x_test, y_test) = mnist.load_data()

    x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, number_channels)
    x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, number_channels)

    input_shape = (number_channels * img_rows * img_cols,)

    x_train = x_train.reshape((x_train.shape[0], number_channels * img_rows * img_cols)).astype('float64')
    x_test = x_test.reshape((x_test.shape[0], number_channels * img_rows * img_cols)).astype('float64')

    mean = np.mean(x_train)
    std = np.std(x_train)

    x_train = (x_train - mean) / std
    x_test = (x_test - mean) / std

    y_train = tf.keras.utils.to_categorical(y_train, number_classes)
    y_test = tf.keras.utils.to_categorical(y_test, number_classes)

    if os.path.isfile('./model.h5'):
        model = tf.keras.models.load_model('./model.h5')
    else:
        model = Sequential()
        model.add(Dense(number_neurons, activation='relu', input_shape=input_shape))
        model.add(Dense(number_classes, activation='linear'))

        model.compile(loss=tf.keras.losses.CategoricalCrossentropy(from_logits=True),
                      optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001, ), metrics=['accuracy'])

        model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, verbose=1, validation_data=(x_test, y_test))

        model.save('./model.h5')

    score_target = model.evaluate(x_test, y_test, verbose=0)

    target_classifier = KerasClassifier(model=model, use_logits=True, clip_values=(0, 1))

    fee = FunctionallyEquivalentExtraction(classifier=target_classifier, num_neurons=number_neurons)
    bbc = fee.extract(x_test[0:100])

    y_test_predicted_extracted = bbc.predict(x_test)
    y_test_predicted_target = target_classifier.predict(x_test)

    print('Target model - Test accuracy:', score_target[1])
    print('Extracted model - Test accuracy:',
          np.sum(np.argmax(y_test_predicted_extracted, axis=1) == np.argmax(y_test, axis=1)) / y_test.shape[0])
    print('Extracted model - Test Fidelity:',
          np.sum(np.argmax(y_test_predicted_extracted, axis=1) == np.argmax(y_test_predicted_target, axis=1)) /
          y_test_predicted_target.shape[0])
