import cv2
import numpy as np
from utils.image_utils import resize_to_square


class Image:
    def __init__(self, image_data: np.ndarray) -> None:
        self.image_byte = cv2.cvtColor(image_data, cv2.COLOR_BGR2GRAY)
        self.image_array = cv2.transpose(self.image_byte)

        self.dft = np.fft.fft2(self.image_byte)
        self.real = np.real(self.dft)
        self.imaginary = np.imag(self.dft)
        self.magnitude = np.abs(self.dft)
        self.phase = np.angle(np.fft.fftshift(self.dft))


def load_image_from_file_name(file_name: str) -> Image:
    return Image(resize_to_square(cv2.imread(file_name)))
