from segmentation.region.models.region import Region
from segmentation.region.models.pixel import Pixel
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List
import numpy as np
import cv2 as cv


@dataclass
class ConnectivityStrategyInterface(ABC):
    image: list
    region: Region = None
    visited_pixel: List[Pixel] = field(default_factory=lambda: [])
    stack_pixel: List[Pixel] = field(default_factory=lambda: [])

    def __post_init__(self):
        levels = np.unique(self.image)
        self.tolerance = 5/100 * (255 - levels[0])

    @abstractmethod
    def execute(self, x: int, y: int) -> None:
        raise NotImplemented
    
    def segment_pixel(self, x: int, y: int):
        if len(self.image) > x and len(self.image[0]) > y:
            if (self.dif_gray_levels(self.image[x][y], self.region.mean)) and not self.is_visited(x, y):
                pixel = Pixel(x, y, self.image[x][y])
                self.stack_pixel.append(pixel)
                self.add_region(pixel)
        
    def dif_gray_levels(self, pixel: int, seed: int) -> bool:
        return np.abs(int(pixel) - int(seed)) <= self.tolerance
    
    def add_region(self, pixel: Pixel):
        self.visited_pixel.append(pixel)

        if not self.region:
            self.region = Region(pixels=[pixel])
            self.region.calculate_mean()
        else:   
            self.region.pixels.append(pixel)
            self.region.calculate_mean()
        
        self.mark_region()
        
    def is_visited(self, x: int, y: int) -> bool:
        for pixel in self.visited_pixel:
            if pixel.x == x and pixel.y==y:
                return True
        return False

    def mark_region(self):
        for pixel in self.region.pixels:
            self.image[pixel.x, pixel.y] = 0

        cv.imshow("segmentation", self.image)
        cv.waitKey(10)
