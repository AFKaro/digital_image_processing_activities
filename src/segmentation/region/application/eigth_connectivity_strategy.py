from segmentation.region.application.connectivity_strategy_interface import ConnectivityStrategyInterface
from segmentation.region.models.pixel import Pixel
from dataclasses import dataclass
import cv2 as cv

@dataclass
class EigthConnectivityStrategy(ConnectivityStrategyInterface):

    def execute(self, seed_x: int, seed_y: int):
        init_pixel = Pixel(seed_x, seed_y, self.image[seed_x][seed_y])
        self.stack_pixel.append(init_pixel)
        self.iterations = 0

        self.add_region(pixel=init_pixel)

        while(len(self.stack_pixel) > 0):
            pixel = self.stack_pixel.pop()
            self.iterations += 1
            print(f"Iteration: {self.iterations}, Visiteds: {len(self.visited_pixel)}, Stack: {len(self.stack_pixel)}")

            self.segment_pixel(pixel.x+1, pixel.y)
            self.segment_pixel(pixel.x-1, pixel.y)
            self.segment_pixel(pixel.x, pixel.y+1)
            self.segment_pixel(pixel.x, pixel.y-1)

            self.segment_pixel(pixel.x+1, pixel.y+1)
            self.segment_pixel(pixel.x-1, pixel.y+1)
            self.segment_pixel(pixel.x+1, pixel.y-1)
            self.segment_pixel(pixel.x-1, pixel.y-1)
            
        cv.imshow("segmentation", self.image)
        cv.waitKey(10)
