from typing import Any

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from lab2 import BaseImage, ColorModel


class GrayScaleTransform(BaseImage):
    def __init__(self, data: Any, color_model: ColorModel) -> None:
        super().__init__(data, color_model)

    def to_gray(self) -> BaseImage:
        """
        method that returns grayscale image as an object of the BaseImage class
        """
        if self.color_model != ColorModel.rgb:
            raise Exception("Color model must be RGB")
        red_layer = self.get_layer(0) * 0.299
        green_layer = self.get_layer(1) * 0.587
        blue_layer = self.get_layer(2) * 0.114
        gray = np.round((red_layer + green_layer + blue_layer)).astype('i')
        return BaseImage(gray, ColorModel.gray)

    def to_sepia(self, alpha_beta: tuple = (None, None), w: int = None) -> BaseImage:
        """
        method that returns a sepia image as an object of the BaseImage class
        depending on the given arguments: alpha and beta or w
        """
        if self.color_model != ColorModel.rgb:
            raise Exception("Color model must be RGB")
        if len(alpha_beta) != 0 and (alpha_beta[0] <= 1 or alpha_beta[1] > 1):
            raise Exception("Alpha must be greater than 1 and Beta must be less than 1")
        if len(alpha_beta) != 0 and (alpha_beta[0] + alpha_beta[1] != 2):
            raise Exception("Alpha + beta must equals 2")
        if w is not None and (w < 20 or w > 40):
            raise Exception("W must be between <20;40>")
        gray_image = self.to_gray()
        L0, L1, L2 = gray_image.data, gray_image.data, gray_image.data
        if w is None:
            L0 = np.where(L0 * alpha_beta[0] > 255, 255, L0 * alpha_beta[0])
            L2 = np.where(L2 * alpha_beta[1] > 255, 255, L2 * alpha_beta[1])
            L0 = np.round(L0).astype('i')
            L2 = np.round(L2).astype('i')
        elif len(alpha_beta) == 0:
            L0 = np.where(L0 + 2 * w > 255, 255, L0 + 2 * w)
            L1 = np.where(L1 + w > 255, 255, L1 + w)
            L0 = np.round(L0).astype('i')
            L1 = np.round(L1).astype('i')
        else:
            raise Exception("Pass only 1 argument")
        return BaseImage(np.dstack((L0, L1, L2)), ColorModel.sepia)


image_test1 = GrayScaleTransform('data/lena.jpg', ColorModel.rgb)
image_test1.show_img()
gray = image_test1.to_gray()
gray.show_img()

sepia1 = image_test1.to_sepia((1.1, 0.9))
sepia2 = image_test1.to_sepia((1.5, 0.5))
sepia3 = image_test1.to_sepia((1.9, 0.1))
sepia4 = image_test1.to_sepia((), 20)
sepia5 = image_test1.to_sepia((), 30)
sepia6 = image_test1.to_sepia((), 40)
sepia1.show_img()
sepia2.show_img()
sepia3.show_img()
sepia4.show_img()
sepia5.show_img()
sepia6.show_img()
