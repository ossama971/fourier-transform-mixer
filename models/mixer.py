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


    def mix(self):
        images_to_mix = [image_obj.image for image_obj in self.images[:4]]
        if self.mix_mode == MixModes.REAL_IMAGINARY:
            self.reconstruct_new_image_using_real_imaginary(*images_to_mix, region=self.region)
        else:
            self.reconstruct_new_image_using_magnitude_phase(*images_to_mix, region=self.region)

    def _get_weighted_component(self, image, comp_type, weight):
        if comp_type == "Real":
            return image.real * weight
        elif comp_type == "Imaginary":
            return 1j * image.imaginary * weight
        elif comp_type == "Magnitude":
            return image.magnitude * weight
        elif comp_type == "Phase":
            return 1j * image.phase * weight

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

    def reconstruct_new_image_using_real_imaginary(self, *images, region: tuple):
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

    def reconstruct_new_image_using_magnitude_phase(self, *images, region: tuple):
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