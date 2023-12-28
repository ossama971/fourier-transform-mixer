import numpy as np
import cv2
import pyqtgraph as pg
from PyQt6.QtWidgets import QSlider, QComboBox

import logging

from enum import Enum


class MixModes(Enum):
    """
    Enumeration for mixing modes
    """

    REAL_IMAGINARY = 1
    MAG_PHASE = 2


class Mixer:
    def __init__(self, window, images, output_port, region: tuple, mix_mode, roi_inner_outer) -> None:
        self.window = window
        self.output_port = output_port
        self.images = images
        self.region = region
        self.mix_mode = mix_mode
        self.roi_inner_outer = roi_inner_outer

    # def mix(self):
    #     if self.mix_mode == MixModes.REAL_IMAGINARY:
    #         self.reconstruct_new_image_using_real_imaginary(
    #             self.images[0].image,
    #             self.images[1].image,
    #             self.images[2].image,
    #             self.images[3].image,
    #             self.region,
    #         )
    #     else:
    #         self.reconstruct_new_image_using_magnitude_phase(
    #             self.images[0].image,
    #             self.images[1].image,
    #             self.images[2].image,
    #             self.images[3].image,
    #             self.region,
    #         )
    #
    # def reconstruct_new_image_using_real_imaginary(
    #         self, image_1, image_2, image_3, image_4, region: tuple
    # ):
    #     print('reconstruct_new_image_using_real_imaginary')
    #     # todo change the weights with actual weight_slider value
    #     weight_1 = self.window.image_1_weight_slider.value() / 100
    #     weight_2 = self.window.image_2_weight_slider.value() / 100
    #     weight_3 = self.window.image_3_weight_slider.value() / 100
    #     weight_4 = self.window.image_4_weight_slider.value() / 100
    #
    #     real = np.zeros_like(image_1.real[region[0]: region[1], region[2]: region[3]])
    #     imaginary = np.zeros_like(
    #         image_1.real[region[0]: region[1], region[2]: region[3]]
    #     )
    #
    #     if self.window.image_comp_1.currentText() == "Real":
    #         real += (
    #                 image_1.real[region[0]: region[1], region[2]: region[3]] * weight_1
    #         )
    #     else:
    #         imaginary += (
    #                 image_1.imaginary[region[0]: region[1], region[2]: region[3]]
    #                 * weight_1
    #         )
    #
    #     if self.window.image_comp_2.currentText() == "Real":
    #         real += (
    #                 image_2.real[region[0]: region[1], region[2]: region[3]] * weight_2
    #         )
    #     else:
    #         imaginary += (
    #                 image_2.imaginary[region[0]: region[1], region[2]: region[3]]
    #                 * weight_2
    #         )
    #
    #     if self.window.image_comp_3.currentText() == "Real":
    #         real += (
    #                 image_3.real[region[0]: region[1], region[2]: region[3]] * weight_3
    #         )
    #     else:
    #         imaginary += (
    #                 image_3.imaginary[region[0]: region[1], region[2]: region[3]]
    #                 * weight_3
    #         )
    #
    #     if self.window.image_comp_4.currentText() == "Real":
    #         real += (
    #                 image_4.real[region[0]: region[1], region[2]: region[3]] * weight_4
    #         )
    #     else:
    #         imaginary += (
    #                 image_4.imaginary[region[0]: region[1], region[2]: region[3]]
    #                 * weight_4
    #         )
    #     print('*' * 100)
    #     print('real:', real.shape)
    #     print('*' * 100)
    #     print('imaginary:', imaginary.shape)
    #     combined_complex = real + 1j * imaginary
    #
    #     # Perform the inverse Fourier Transform
    #     reconstructed_image_complex = np.fft.ifft2(combined_complex)
    #
    #     # Take the absolute value to obtain the magnitude
    #     reconstructed_magnitude = np.abs(reconstructed_image_complex)
    #
    #     # Normalize the reconstructed magnitude to the range [0, 255]
    #     reconstructed_image = cv2.normalize(
    #         reconstructed_magnitude, None, 0, 255, cv2.NORM_MINMAX
    #     )
    #     if self.output_port:
    #         self.output_port.clear()
    #     self.output_port.addItem(pg.ImageItem(reconstructed_image))
    #
    # def reconstruct_new_image_using_magnitude_phase(
    #         self, image_1, image_2, image_3, image_4, region: tuple
    # ):
    #     # todo change the weights with actual weight_slider value
    #     weight_1 = self.window.image_1_weight_slider.value() / 100
    #     weight_2 = self.window.image_2_weight_slider.value() / 100
    #     weight_3 = self.window.image_3_weight_slider.value() / 100
    #     weight_4 = self.window.image_4_weight_slider.value() / 100
    #
    #     magnitude = np.zeros_like(
    #         image_1.magnitude[region[0]: region[1], region[2]: region[3]]
    #     )
    #     phase = np.zeros_like(
    #         image_1.magnitude[region[0]: region[1], region[2]: region[3]]
    #     )
    #
    #     if self.window.image_comp_1.currentText() == "Magnitude":
    #         magnitude += image_1.magnitude * weight_1
    #     else:
    #         phase += image_1.phase * weight_1
    #
    #     if self.window.image_comp_2.currentText() == "Magnitude":
    #         magnitude += image_2.magnitude * weight_2
    #     else:
    #         phase += image_2.phase * weight_2
    #
    #     if self.window.image_comp_3.currentText() == "Magnitude":
    #         magnitude += image_3.magnitude * weight_3
    #     else:
    #         phase += image_3.phase * weight_3
    #
    #     if self.window.image_comp_4.currentText() == "Magnitude":
    #         magnitude += image_4.magnitude * weight_4
    #     else:
    #         phase += image_4.phase * weight_4
    #
    #     # Convert polar coordinates to Cartesian coordinates
    #     real_part = magnitude * np.cos(phase)
    #
    #     imaginary_part = magnitude * np.sin(phase)
    #     print('*' * 100)
    #     print('real_part:', real_part)
    #     print('*' * 100)
    #     print('imaginary_part:', imaginary_part)
    #     # Combine real and imaginary parts to form the complex image
    #     complex_image = cv2.merge([real_part, imaginary_part])
    #
    #     # Perform Inverse Fourier Transform to reconstruct the image
    #     reconstructed_image = cv2.idft(complex_image)
    #
    #     # Extract the real part of the reconstructed image
    #     reconstructed_image = cv2.magnitude(
    #         reconstructed_image[:, :, 0], reconstructed_image[:, :, 1]
    #     )
    #
    #     # Normalize the reconstructed image to the range [0, 255]
    #     reconstructed_image = cv2.normalize(
    #         reconstructed_image, None, 0, 255, cv2.NORM_MINMAX
    #     )
    #
    #     # Convert the reconstructed image to unsigned 8-bit integer (uint8)
    #     reconstructed_image = np.uint8(reconstructed_image)
    #     if self.output_port:
    #         self.output_port.clear()
    #     self.output_port.addItem(pg.ImageItem(reconstructed_image))

    def mix(self):
        images_to_mix = [image_obj.image for image_obj in self.images[:4]]
        if self.mix_mode == MixModes.REAL_IMAGINARY:
            self.reconstruct_new_image_using_real_imaginary(*images_to_mix)
        else:
            self.reconstruct_new_image_using_magnitude_phase(*images_to_mix)

    def _get_weighted_component(self, image, comp_type, weight):
        if self.roi_inner_outer == 'Inner':
            if comp_type == "Real":
                return image.real[self.region[0]: self.region[1], self.region[2]: self.region[3]] * weight
            elif comp_type == "Imaginary":
                return 1j * image.imaginary[self.region[0]: self.region[1], self.region[2]: self.region[3]] * weight
            elif comp_type == "Magnitude":
                return image.magnitude[self.region[0]: self.region[1], self.region[2]: self.region[3]] * weight
            elif comp_type == "Phase":
                return 1j * image.phase[self.region[0]: self.region[1], self.region[2]: self.region[3]] * weight


    def _combine_images(self, components):
        print('len comp:', len(components))
        print([np.iscomplexobj(comp) for comp in components])
        real_parts = [np.real(comp) for comp in components]
        imaginary_parts = [np.imag(comp) for comp in components]

        real = np.sum(real_parts, axis=0)
        imaginary = np.sum(imaginary_parts, axis=0)

        print('len real:', len(real))
        print('len real[0]:', len(real[0]))
        return real, imaginary

    def _inverse_fourier_transform(self, combined_complex):
        combined_complex_image = combined_complex[0] + 1j * combined_complex[1]
        return np.fft.ifft2(combined_complex_image)

    def _normalize_image(self, image):
        return cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX)

    def _add_image_to_output_port(self, image):
        if self.output_port:
            self.output_port.clear()
        self.output_port.addItem(pg.ImageItem(image))

    def reconstruct_new_image_using_real_imaginary(self, *images):
        print('reconstruct_new_image_using_real_imaginary')

        weights = [self.window.findChild(QSlider, f'image_{i}_weight_slider').value() / 100 for i in range(1, 5)]
        print('weights = ', weights)
        components = [
            self._get_weighted_component(image, self.window.findChild(QComboBox, f'image_comp_{i}').currentText(),
                                         weight)
            for i, (image, weight) in enumerate(zip(images, weights), start=1)
        ]
        print('components = ', components)
        combined_complex = self._combine_images(components)

        reconstructed_image_complex = self._inverse_fourier_transform(combined_complex)

        reconstructed_magnitude = np.abs(reconstructed_image_complex)

        reconstructed_image = self._normalize_image(reconstructed_magnitude)

        self._add_image_to_output_port(reconstructed_image)

    def reconstruct_new_image_using_magnitude_phase(self, *images):
        weights = [self.window.findChild(QSlider, f'image_{i}_weight_slider').value() / 100 for i in range(1, 5)]

        components = [
            self._get_weighted_component(image, self.window.findChild(QComboBox, f'image_comp_{i}').currentText(),
                                         weight)
            for i, (image, weight) in enumerate(zip(images, weights), start=1)
        ]
        # todo: fix phase calculation
        magnitude, phase = self._combine_images(components)
        real_part = magnitude * np.cos(phase)
        imaginary_part = magnitude * np.sin(phase)

        complex_image = cv2.merge([real_part, imaginary_part])

        reconstructed_image = cv2.idft(complex_image)
        reconstructed_image = cv2.magnitude(reconstructed_image[:, :, 0], reconstructed_image[:, :, 1])
        reconstructed_image = self._normalize_image(reconstructed_image)
        reconstructed_image = np.uint8(reconstructed_image)

        self._add_image_to_output_port(reconstructed_image)