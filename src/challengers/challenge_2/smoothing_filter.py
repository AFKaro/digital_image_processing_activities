from dataclasses import dataclass, field
import cv2 as cv


@dataclass
class SmoothingFilter:
    mask: tuple = field(default=None)
    
    def __post_init__(self):
        self.mask = (3, 3)
        
    def smothing(self, image: list):
        for i in range(10):
            image = cv.medianBlur(image, 3)
        return image