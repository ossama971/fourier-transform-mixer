import numpy as np
import cv2
import pyqtgraph as pg
import logging

from enum import Enum


class MixModes(Enum):
    """
    Enumeration for mixing modes
    """

    REAL_IMAGINARY = 1
    MAG_PHASE = 2


class Mixer:
    def __init__(self, window, images, output_port, region: tuple) -> None:
        self.window = window
        self.output_port = output_port
        self.images = images
        self.region = region

    def mix(self):
        self.reconstruct_new_image_using_real_imaginary(
            self.window,
            self.images[0].image,
            self.images[1].image,
            self.images[2].image,
            self.images[3].image,
            self.region,
        )

        self.reconstruct_new_image_using_magnitude_phase(
            self.window,
            self.images[0].image,
            self.images[1].image,
            self.images[2].image,
            self.images[3].image,
            self.region,
        )

    def reconstruct_new_image_using_real_imaginary(
        self, window, image_1, image_2, image_3, image_4, region: tuple
    ):
        # todo change the weights with actual weight_slider value
        weight_1 = 1
        weight_2 = 0
        weight_3 = 1
        weight_4 = 0

        real = np.zeros_like(image_1.real[region[0] : region[1], region[2] : region[3]])
        imaginary = np.zeros_like(
            image_1.real[region[0] : region[1], region[2] : region[3]]
        )

        if self.window.image_comp_1.currentText() == "Real":
            real += (
                image_1.real[region[0] : region[1], region[2] : region[3]] * weight_1
            )
        else:
            imaginary += (
                image_1.imaginary[region[0] : region[1], region[2] : region[3]]
                * weight_1
            )

        if self.window.image_comp_2.currentText() == "Real":
            real += (
                image_2.real[region[0] : region[1], region[2] : region[3]] * weight_2
            )
        else:
            imaginary += (
                image_2.imaginary[region[0] : region[1], region[2] : region[3]]
                * weight_2
            )

        if self.window.image_comp_3.currentText() == "Real":
            real += (
                image_3.real[region[0] : region[1], region[2] : region[3]] * weight_3
            )
        else:
            imaginary += (
                image_3.imaginary[region[0] : region[1], region[2] : region[3]]
                * weight_3
            )

        if self.window.image_comp_4.currentText() == "Real":
            real += (
                image_4.real[region[0] : region[1], region[2] : region[3]] * weight_4
            )
        else:
            imaginary += (
                image_4.imaginary[region[0] : region[1], region[2] : region[3]]
                * weight_4
            )

        combined_complex = real + 1j * imaginary

        # Perform the inverse Fourier Transform
        reconstructed_image_complex = np.fft.ifft2(combined_complex)

        # Take the absolute value to obtain the magnitude
        reconstructed_magnitude = np.abs(reconstructed_image_complex)

        # Normalize the reconstructed magnitude to the range [0, 255]
        reconstructed_image = cv2.normalize(
            reconstructed_magnitude, None, 0, 255, cv2.NORM_MINMAX
        )

        self.output_port.addItem(pg.ImageItem(reconstructed_image))

    def reconstruct_new_image_using_magnitude_phase(
        self, windows, image_1, image_2, image_3, image_4, region: tuple
    ):
        # todo change the weights with actual weight_slider value
        weight_1 = self.window.image_1_output_1_slider.value() / 100
        weight_2 = self.window.image_2_output_1_slider.value() / 100
        weight_3 = self.window.image_1_output_2_slider.value() / 100
        weight_4 = self.window.image_2_output_2_slider.value() / 100

        magnitude = np.zeros_like(
            image_1.magnitude[region[0] : region[1], region[2] : region[3]]
        )
        phase = np.zeros_like(
            image_1.magnitude[region[0] : region[1], region[2] : region[3]]
        )

        if self.window.image_comp_1.currentText() == "Magnitude":
            magnitude += image_1.magnitude * weight_1
        else:
            phase += image_1.phase * weight_1

        if self.window.image_comp_2.currentText() == "Magnitude":
            magnitude += image_2.magnitude * weight_2
        else:
            phase += image_2.phase * weight_2

        if self.window.image_comp_3.currentText() == "Magnitude":
            magnitude += image_3.magnitude * weight_3
        else:
            phase += image_3.phase * weight_3

        if self.window.image_comp_4.currentText() == "Magnitude":
            magnitude += image_4.magnitude * weight_4
        else:
            phase += image_4.phase * weight_4

        # Convert polar coordinates to Cartesian coordinates
        real_part = magnitude * np.cos(phase)

        imaginary_part = magnitude * np.sin(phase)

        # Combine real and imaginary parts to form the complex image
        complex_image = cv2.merge([real_part, imaginary_part])

        # Perform Inverse Fourier Transform to reconstruct the image
        reconstructed_image = cv2.idft(complex_image)

        # Extract the real part of the reconstructed image
        reconstructed_image = cv2.magnitude(
            reconstructed_image[:, :, 0], reconstructed_image[:, :, 1]
        )

        # Normalize the reconstructed image to the range [0, 255]
        reconstructed_image = cv2.normalize(
            reconstructed_image, None, 0, 255, cv2.NORM_MINMAX
        )

        # Convert the reconstructed image to unsigned 8-bit integer (uint8)
        reconstructed_image = np.uint8(reconstructed_image)

        self.output_port.addItem(pg.ImageItem(reconstructed_image))
