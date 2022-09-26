from segmentation.by_region.pixel import Pixel
from segmentation.by_region.region import Region
from dataclasses import dataclass, field
from typing import List
import numpy as np


@dataclass
class SegmentationRegionAlgorithm:
    image: list
    region: Region = None
    visited_pixel: List[Pixel] = field(default_factory=lambda: [])
    stack_pixel: List[Pixel] = field(default_factory=lambda: [])

    iterations: int = 0

    def segmentation_four_connect(self, seed_x: int, seed_y: int):
        self.stack_pixel.append(Pixel(seed_x, seed_y, self.image[seed_x][seed_y]))

        while(len(self.stack_pixel) > 0):
            pixel = self.stack_pixel.pop()
            self.iterations += 1
            print(f"Iteration: {self.iterations}")

            self.segment_pixel(pixel.x+1, pixel.y, pixel.x, pixel.y)
            self.segment_pixel(pixel.x-1, pixel.y, pixel.x, pixel.y)
            self.segment_pixel(pixel.x, pixel.y+1, pixel.x, pixel.y)
            self.segment_pixel(pixel.x, pixel.y-1, pixel.x, pixel.y)
    
    def segment_pixel(self, x: int, y: int, seed_x: int, seed_y: int):
        if len(self.image) >= x and len(self.image[0]) >= y:
            if (self.dif_gray_levels(self.image[x][y], self.image[seed_x][seed_y])) and not self.is_visited(x, y):
                pixel = Pixel(x, y, self.image[x][y])
                self.stack_pixel.append(pixel)
                self.add_region(pixel)
        
    def dif_gray_levels(self, pixel: int, seed: int) -> bool:
        levels = np.unique(self.image)
        return np.abs(int(pixel) - int(seed)) <= 10/100 * (255 - levels[0])
    
    def add_region(self, pixel: Pixel):
        self.visited_pixel.append(pixel)

        print(f"Seed: [{pixel.x},{pixel.y}], Visiteds: {len(self.visited_pixel)}")

        if not self.region:
            self.region = Region(pixels=[pixel])
            self.region.calculate_mean()
        else:   
            self.region.pixels.append(pixel)
            self.region.calculate_mean()
        
    def is_visited(self, x: int, y: int) -> bool:
        for pixel in self.visited_pixel:
            if pixel.x == x and pixel.y==y:
                return True
        return False

            