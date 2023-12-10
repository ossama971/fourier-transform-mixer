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
