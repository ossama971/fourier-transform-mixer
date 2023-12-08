import cv2
import numpy as np
from utils.image_utils import resize_to_square


class Image:
    def __init__(self, file_name: str) -> None:
        image = resize_to_square(cv2.imread(file_name))

        self.image_byte = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        self.image_array = cv2.transpose(self.image_byte)

        self.dft = np.fft.fft2(self.image_byte)
        self.real = np.real(self.dft)
        self.imaginary = np.imag(self.dft)
        self.magnitude = np.abs(self.dft)
        self.phase = np.angle(np.fft.fftshift(self.dft))
