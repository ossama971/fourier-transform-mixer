import logging
import cv2
import numpy as np
import pyqtgraph as pg

from enum import Enum
from models.image_view_port import ComponentViewMode


class ImageNumber(Enum):
    """
    Enum for different component view modes.
    """

    Image1 = 0
    Image2 = 1
    Image3 = 2
    Image4 = 3


class OutputPanel:
    def __init__(
        self,
        window,
        output_viewer,
        first_image_combo_box,
        second_image_combo_box,
        first_image_mode_compo_box,
        second_image_mode_compo_box,
        component1_weight_slider,
        component2_weight_slider,
    ):
        self.window = window
        self.output_viewer = output_viewer
        self.output_viewer.showAxes(False)
        self.output_viewer.rotate(90)
        self.first_image_combo_box = first_image_combo_box
        self.second_image_combo_box = second_image_combo_box
        self.first_image_mode_compo_box = first_image_mode_compo_box
        self.second_image_mode_compo_box = second_image_mode_compo_box
        self.component_1_weight_slider = component1_weight_slider
        self.component_2_weight_slider = component2_weight_slider

        self.weight_1 = 1
        self.weight_2 = 1
        self.image_1_component = ComponentViewMode.MAGNITUDE
        self.image_2_component = ComponentViewMode.PHASE

        for mode in ComponentViewMode:
            self.first_image_mode_compo_box.addItem(mode.name.capitalize())
            self.second_image_mode_compo_box.addItem(mode.name.capitalize())

        for image in ImageNumber:
            self.first_image_combo_box.addItem(image.name.capitalize())
            self.second_image_combo_box.addItem(image.name.capitalize())

        self._initialize_slots()

    def _initialize_slots(self) -> None:
        self.component_1_weight_slider.valueChanged.connect(
            self._component_1_weight_slider_value_changed
        )
        self.component_2_weight_slider.valueChanged.connect(
            self._component_2_weight_slider_value_changed
        )

    def _component_1_weight_slider_value_changed(self, value) -> None:
        self.weight_1 = value / 10

    def _component_2_weight_slider_value_changed(self, value) -> None:
        self.weight_2 = value / 10

    def reconstruct_image_using_real_imaginary(
        self, image_1: Image, image_2: Image, region: tuple
    ):
        sliced_image_1_real = image_1.real[region[0] : region[1], region[2] : region[3]]
        logging.info(
            f"Reconstruct using real/imaginary over region {region} - ({sliced_image_1_real.shape[0]}x{sliced_image_1_real.shape[1]})"
        )

        print(sliced_image_1_real.shape)
        sliced_image_2_imaginary = image_2.imaginary[
            region[0] : region[1], region[2] : region[3]
        ]
        combined_complex = (
            self.weight_1 * sliced_image_1_real
            + 1j * self.weight_2 * sliced_image_2_imaginary
        )

        # Perform the inverse Fourier Transform
        reconstructed_image_complex = np.fft.ifft2(combined_complex)

        # Take the absolute value to obtain the magnitude
        reconstructed_magnitude = np.abs(reconstructed_image_complex)

        # Normalize the reconstructed magnitude to the range [0, 255]
        reconstructed_image = cv2.normalize(
            reconstructed_magnitude, None, 0, 255, cv2.NORM_MINMAX
        )

        self.output_viewer.addItem(pg.ImageItem(reconstructed_image))

    def reconstruct_image_using_magnitude_phase(
        self, image_1: Image, image_2: Image, region: tuple
    ):
        # Slice the magnitude of image_1 to match the region
        sliced_image_1_magnitude = image_1.magnitude[
            region[0] : region[1], region[2] : region[3]
        ]
        sliced_image_2_phase = image_2.phase[
            region[0] : region[1], region[2] : region[3]
        ]

        # Convert polar coordinates to Cartesian coordinates
        real_part = (
            self.weight_1 * sliced_image_1_magnitude * np.cos(sliced_image_2_phase)
        )

        imaginary_part = (
            self.weight_2 * sliced_image_1_magnitude * np.sin(sliced_image_2_phase)
        )

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

        self.output_viewer.addItem(pg.ImageItem(reconstructed_image))
