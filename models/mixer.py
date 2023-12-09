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
    def __init__(self, window, output_viewer, first_image_combo_box, second_image_combo_box, first_image_mode_compo_box,
                 second_image_mode_compo_box, component1_weight_slider, component2_weight_slider):
        self.window = window
        self.output_viewer = output_viewer
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
        self.component_1_weight_slider.valueChanged.connect(self._component_1_weight_slider_value_changed)
        self.component_2_weight_slider.valueChanged.connect(self._component_2_weight_slider_value_changed)
        self.first_image_combo_box.currentIndexChanged.connect(self._on_first_image_combox_changed)
        self.second_image_combo_box.currentIndexChanged.connect(self._on_second_image_combox_changed)
        self.first_image_mode_compo_box.currentIndexChanged.connect(self._on_first_image_mode_combox_changed)
        self.second_image_mode_compo_box.currentIndexChanged.connect(self._on_second_image_mode_combox_changed)

    def _component_1_weight_slider_value_changed(self, value) -> None:
        pass

    def _component_2_weight_slider_value_changed(self, value) -> None:
        pass

    def _on_first_image_combox_changed(self, index) -> None:
        pass

    def _on_second_image_combox_changed(self, index) -> None:
        pass

    def _on_first_image_mode_combox_changed(self, index) -> None:
        pass

    def _on_second_image_mode_combox_changed(self, index) -> None:
        pass

    def reconstruct_image_using_real_imaginary(self, real_part_weight, real, imaginary_part_weight, imaginary):
        combined_complex = real_part_weight * real + 1j * imaginary_part_weight * imaginary

        # Perform the inverse Fourier Transform
        reconstructed_image_complex = np.fft.ifft2(combined_complex)

        # Take the absolute value to obtain the magnitude
        reconstructed_magnitude = np.abs(reconstructed_image_complex)

        # Normalize the reconstructed magnitude to the range [0, 255]
        reconstructed_image = cv2.normalize(reconstructed_magnitude, None, 0, 255, cv2.NORM_MINMAX)
        print('done')

        return reconstructed_image

    def reconstruct_image_using_real_imaginary(self, image_1, image_2):
        combined_complex = self.weight_1 * image_1.real + 1j * self.weight_2 * image_2.imaginary

        # Perform the inverse Fourier Transform
        reconstructed_image_complex = np.fft.ifft2(combined_complex)

        # Take the absolute value to obtain the magnitude
        reconstructed_magnitude = np.abs(reconstructed_image_complex)

        # Normalize the reconstructed magnitude to the range [0, 255]
        reconstructed_image = cv2.normalize(reconstructed_magnitude, None, 0, 255, cv2.NORM_MINMAX)
        print('done')

        self.output_viewer.addItem(pg.ImageItem(self.reconstructed_image))

    def reconstruct_image_using_magnitude_phase(self, image_1, image_2):
        # Convert polar coordinates to Cartesian coordinates
        real_part = self.weight_1 * image_1.magnitude * np.cos(image_2.phase)
        imaginary_part = self.weight_2 * image_1.magnitude * np.sin(image_2.phase)

        # Combine real and imaginary parts to form the complex image
        complex_image = cv2.merge([real_part, imaginary_part])

        # Perform Inverse Fourier Transform to reconstruct the image
        reconstructed_image = cv2.idft(complex_image)

        # Extract the real part of the reconstructed image
        reconstructed_image = cv2.magnitude(reconstructed_image[:, :, 0], reconstructed_image[:, :, 1])

        # Normalize the reconstructed image to the range [0, 255]
        reconstructed_image = cv2.normalize(reconstructed_image, None, 0, 255, cv2.NORM_MINMAX)

        # Convert the reconstructed image to unsigned 8-bit integer (uint8)
        reconstructed_image = np.uint8(reconstructed_image)

        self.output_viewer.addItem(pg.ImageItem(self.reconstructed_image))
