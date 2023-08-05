"""
Adapted from NiftyNet
"""

import numpy as np
import torch
from ..torchio import INTENSITY
from ..utils import is_image_dict
from .random_transform import RandomTransform


class RandomBiasField(RandomTransform):
    def __init__(
            self,
            coefficients_range=(-0.5, 0.5),
            order=3,
            seed=None,
            verbose=False,
            ):
        super().__init__(seed=seed, verbose=verbose)
        self.coefficients_range = coefficients_range
        self.order = order

    def apply_transform(self, sample):
        coefficients = self.get_params(self.order, self.coefficients_range)
        sample['random_bias_field'] = coefficients
        for image_name, image_dict in sample.items():
            if not is_image_dict(image_dict):
                continue
            if image_dict['type'] != INTENSITY:
                continue
            coefficients = self.get_params(self.order, self.coefficients_range)
            sample[image_name]['random_bias_field'] = coefficients
            bias_field = self.generate_bias_field_map(
                image_dict['data'], self.order, coefficients)
            image_dict['data'] *= torch.from_numpy(bias_field)
        return sample

    @staticmethod
    def get_params(order, coefficients_range):
        """
        Sampling of the appropriate number of coefficients for the creation
        of the bias field map
        """
        random_coefficients = []
        for x_order in range(0, order + 1):
            for y_order in range(0, order + 1 - x_order):
                for z_order in range(0, order + 1 - (x_order + y_order)):
                    number = torch.FloatTensor(1).uniform_(*coefficients_range)
                    random_coefficients.append(number.item())
        return np.array(random_coefficients)

    @staticmethod
    def generate_bias_field_map(data, order, coefficients):
        """
        Create the bias field map using a linear combination of polynomial
        functions and the coefficients previously sampled
        """
        shape = np.array(data.shape[1:])  # first axis is channels
        half_shape = shape / 2

        ranges = [np.arange(-n, n) for n in half_shape]

        bf_map = np.zeros(shape)
        x_mesh, y_mesh, z_mesh = np.asarray(np.meshgrid(*ranges))

        x_mesh /= x_mesh.max()
        y_mesh /= y_mesh.max()
        z_mesh /= z_mesh.max()

        i = 0
        for x_order in range(order + 1):
            for y_order in range(order + 1 - x_order):
                for z_order in range(order + 1 - (x_order + y_order)):
                    random_coefficient = coefficients[i]
                    new_map = (
                        random_coefficient
                        * x_mesh ** x_order
                        * y_mesh ** y_order
                        * z_mesh ** z_order
                    )
                    bf_map += np.transpose(new_map, (1, 0, 2))  # why?
                    i += 1
        return np.exp(bf_map)
