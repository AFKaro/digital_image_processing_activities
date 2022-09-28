from segmentation.region.models.pixel import Pixel
from dataclasses import dataclass, field
from typing import List


@dataclass
class Region:
    mean: int = 0
    pixels: List[Pixel] = field(default_factory=lambda: [])

    def calculate_mean(self):
        sum_pixels = 0
        for pixel in self.pixels:
            sum_pixels += pixel.value
        self.mean = sum_pixels / len(self.pixels)
