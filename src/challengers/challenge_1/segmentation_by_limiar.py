from dataclasses import dataclass, field
import numpy as np


@dataclass
class SegmentationByLimiar:
    t_value: float = field(default=None)
    t_value_ant: float = field(default=0)
    
    def calcule_limiar(self, image: list):
        t_ref = 0

        if self.t_value is None:
            # Select an estimated value for T (midpoint between the minimum and maximum values of an image)
            levels = np.unique(image)
            self.t_value = (levels[0] + levels[-1]) / 2
            self.t_value_ant = t_ref
        
        else:
            # Segment the image using T
            left = []
            rigth = []

            for line in range(0, len(image)):
                for col in range(0, len(image[line])):
                    if (image[line][col] < self.t_value):
                        left.append(image[line][col])
                    else:
                        rigth.append(image[line][col])

            # Calculate the average of the pixel intensities in each region
            mean_left = np.mean(left) if left else 0
            mean_rigth = np.mean(rigth) if rigth else 0

            # Calculate the new value of T
            self.t_value_ant = self.t_value
            self.t_value = (mean_left + mean_rigth) / 2

    def get_new_img(self, image: list) -> list:
        new_img = image.copy()

        for line in range(0, len(new_img)):
            for col in range(0, len(new_img[line])):
                if (new_img[line][col] < self.t_value):
                    new_img[line][col] = 0
                else:
                    new_img[line][col] = 255
        return new_img