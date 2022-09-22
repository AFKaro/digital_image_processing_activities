from segmentation.by_region.pixel import Pixel
from segmentation.by_region.region import Region
from dataclasses import dataclass, field
from typing import List
import numpy as np

from segmentation.segmentation_by_limiar import segmentation


@dataclass
class SegmentationRegionAlgorithm:
    image: list
    regions: List[Region] = field(default_factory=lambda: [])
    visited_pixel: List[Pixel] = field(default_factory=lambda: [])

    def segmentation(self, seed_x: int, seed_y: int):
        self.add_region(seed_x, seed_y)

        self.segment_pixel(seed_x+1, seed_y, seed_x, seed_y)
        self.segment_pixel(seed_x-1, seed_y, seed_x, seed_y)
        self.segment_pixel(seed_x, seed_y+1, seed_x, seed_y)
        self.segment_pixel(seed_x, seed_y-1, seed_x, seed_y)
    
    def segment_pixel(self, x: int, y: int, seed_x: int, seed_y: int):
        if len(self.image) >= x and len(self.image[0]) >= y:
            if (self.dif_gray_levels(self.image[x][y], self.image[seed_x][seed_y])) and not self.is_visited(x, y):
                self.segmentation(x, y)
        
    def dif_gray_levels(self, pixel: int, seed: int) -> bool:
        levels = np.unique(self.image)
        return np.abs(int(pixel) - int(seed)) <= 10/100 * (255 - levels[0])
    
    def add_region(self, pixel_x: int, pixel_y: int):
        pixel = Pixel(pixel_x, pixel_y, self.image[pixel_x][pixel_y])
        self.visited_pixel.append(pixel)

        print(f"Seed: [{pixel_x},{pixel_y}], Visiteds: {len(self.visited_pixel)}")

        new_region = None
        if not self.regions:
            new_region = Region(pixels=[pixel])
            new_region.calculate_mean()
            self.regions.append(new_region)
        else:
            found_region = False
            for region in self.regions:
                if self.dif_gray_levels(region.mean, self.image[pixel_x][pixel_y]):
                    region.pixels.append(pixel)
                    region.calculate_mean()
                    new_region = region
                    found_region = True
                    break
            
            if not found_region:
                new_region = Region(pixels=[pixel])
                new_region.calculate_mean()
                self.regions.append(new_region)

    def is_visited(self, x: int, y: int) -> bool:
        for pixel in self.visited_pixel:
            if pixel.x == x and pixel.y==y:
                return True
        return False

            