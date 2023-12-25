import numpy as np
import cv2
import pyqtgraph as pg
import logging


class Mixer:
    def __init__(self, window, region: tuple) -> None:
        self.window = window
        self.region = region

    def mix(self):
        img_idx_dictionary = {"Image1": 0, "Image2": 1, "Image3": 2, "Image4": 3}

        image_indices = {
            "output_1": [
                img_idx_dictionary[self.window.image_1_output_1.currentText()],
                img_idx_dictionary[self.window.image_2_output_1.currentText()],
            ],
            "output_2": [
                img_idx_dictionary[self.window.image_1_output_2.currentText()],
                img_idx_dictionary[self.window.image_2_output_2.currentText()],
            ],
        }

        images = {
            "output_1": [
                self.window.images[image_indices["output_1"][0]].image,
                self.window.images[image_indices["output_1"][1]].image,
            ],
            "output_2": [
                self.window.images[image_indices["output_2"][0]].image,
                self.window.images[image_indices["output_2"][1]].image,
            ],
        }
        self.window.image_output_1.clear()
        self.window.image_output_2.clear()

        for output in ["output_1", "output_2"]:
            if all(image is not None for image in images[output]):
                self._process_images(output, images[output])

    def _process_images(self, output, images):
        output_idx = int(output.split("_")[-1]) - 1
        component_1 = self.window.__getattribute__(
            f"image_1_component_{output}"
        ).currentText()
        component_2 = self.window.__getattribute__(
            f"image_2_component_{output}"
        ).currentText()

        if component_1 == "Magnitude" and component_2 == "Phase":
            self.window.output_ports[
                output_idx
            ].reconstruct_image_using_magnitude_phase(*images, region=self.region)
        elif component_1 == "Phase" and component_2 == "Magnitude":
            self.window.output_ports[
                output_idx
            ].reconstruct_image_using_magnitude_phase(
                *reversed(images), region=self.region
            )
        elif component_1 == "Real" and component_2 == "Imaginary":
            self.window.output_ports[output_idx].reconstruct_image_using_real_imaginary(
                *images, region=self.region
            )
        elif component_1 == "Imaginary" and component_2 == "Real":
            self.window.output_ports[output_idx].reconstruct_image_using_real_imaginary(
                *reversed(images), region=self.region
            )

        self.reconstruct_new_image_using_real_imaginary(self.window, self.window.images[0].image,
                                                        self.window.images[1].image,
                                                        self.window.images[2].image,
                                                        self.window.images[3].image,
                                                        self.region)

        self.reconstruct_new_image_using_magnitude_phase(self.window, self.window.images[0].image,
                                                         self.window.images[1].image,
                                                         self.window.images[2].image,
                                                         self.window.images[3].image,
                                                         self.region)

    def reconstruct_new_image_using_real_imaginary(
            self, window, image_1, image_2, image_3, image_4, region: tuple
    ):
        # todo change the weights with actual weight_slider value
        weight_1 = 1
        weight_2 = 0
        weight_3 = 1
        weight_4 = 0

        real = np.zeros_like(image_1.real[region[0]: region[1], region[2]: region[3]])
        imaginary = np.zeros_like(image_1.real[region[0]: region[1], region[2]: region[3]])

        if self.window.image_1_component_output_1.currentText() == 'Real':
            real += image_1.real[region[0]: region[1], region[2]: region[3]] * weight_1
        else:
            imaginary += image_2.imaginary[region[0]: region[1], region[2]: region[3]] * weight_1

        if self.window.image_2_component_output_1.currentText() == 'Real':
            real += image_2.real[region[0]: region[1], region[2]: region[3]] * weight_2
        else:
            imaginary += image_2.imaginary[region[0]: region[1], region[2]: region[3]] * weight_2

        if self.window.image_1_component_output_2.currentText() == 'Real':
            real += image_3.real[region[0]: region[1], region[2]: region[3]] * weight_3
        else:
            imaginary += image_3.imaginary[region[0]: region[1], region[2]: region[3]] * weight_3

        if self.window.image_2_component_output_2.currentText() == 'Real':
            real += image_4.real[region[0]: region[1], region[2]: region[3]] * weight_4
        else:
            imaginary += image_4.imaginary[region[0]: region[1], region[2]: region[3]] * weight_4

        combined_complex = (real + 1j * imaginary)

        # Perform the inverse Fourier Transform
        reconstructed_image_complex = np.fft.ifft2(combined_complex)

        # Take the absolute value to obtain the magnitude
        reconstructed_magnitude = np.abs(reconstructed_image_complex)

        # Normalize the reconstructed magnitude to the range [0, 255]
        reconstructed_image = cv2.normalize(
            reconstructed_magnitude, None, 0, 255, cv2.NORM_MINMAX
        )

        self.window.image_output_1.addItem(pg.ImageItem(reconstructed_image))

    def reconstruct_new_image_using_magnitude_phase(
            self, windows, image_1, image_2, image_3, image_4, region: tuple
    ):
        # todo change the weights with actual weight_slider value
        weight_1 = 1
        weight_2 = 1
        weight_3 = 1
        weight_4 = 1
        magnitude = np.zeros_like(image_1.magnitude[region[0]: region[1], region[2]: region[3]])
        phase = np.zeros_like(image_1.magnitude[region[0]: region[1], region[2]: region[3]])

        if self.window.image_1_component_output_1.currentText() == 'Magnitude':
            magnitude += image_1.magnitude * weight_1
        else:
            phase += image_2.phase * weight_1

        if self.window.image_2_component_output_1.currentText() == 'Magnitude':
            magnitude += image_2.magnitude * weight_2
        else:
            phase += image_2.phase * weight_2

        if self.window.image_1_component_output_2.currentText() == 'Magnitude':
            magnitude += image_3.magnitude * weight_3
        else:
            phase += image_3.phase * weight_3

        if self.window.image_2_component_output_2.currentText() == 'Magnitude':
            magnitude += image_4.magnitude * weight_4
        else:
            phase += image_4.phase * weight_4

        # Convert polar coordinates to Cartesian coordinates
        real_part = (
                magnitude * np.cos(phase)
        )

        imaginary_part = (
                magnitude * np.sin(phase)
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

        self.window.image_output_2.addItem(pg.ImageItem(reconstructed_image))
