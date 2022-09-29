from segmentation.region.application.connectivity_strategy_interface import ConnectivityStrategyInterface
from segmentation.region.models.pixel import Pixel
from dataclasses import dataclass


@dataclass
class MConnectivityStrategy(ConnectivityStrategyInterface):

    def execute(self, seed_x: int, seed_y: int):
        init_pixel = Pixel(seed_x, seed_y, self.image[seed_x][seed_y])
        self.stack_pixel.append(init_pixel)
        iterations = 0

        self.add_region(pixel=init_pixel)

        while(len(self.stack_pixel) > 0):
            pixel = self.stack_pixel.pop()
            iterations += 1
            print(f"Iteration: {iterations}, Visiteds: {len(self.visited_pixel)}, Stack: {len(self.stack_pixel)}")

            self.segment_pixel(pixel.x+1, pixel.y)
            self.segment_pixel(pixel.x-1, pixel.y)
            self.segment_pixel(pixel.x, pixel.y+1)
            self.segment_pixel(pixel.x, pixel.y-1)

            if self.__intercession_four_connection(pixel.x+1, pixel.y+1, pixel.x, pixel.y) == 0:
                self.segment_pixel(pixel.x+1, pixel.y+1)

            if self.__intercession_four_connection(pixel.x-1, pixel.y+1, pixel.x, pixel.y) == 0:
                self.segment_pixel(pixel.x-1, pixel.y+1)

            if self.__intercession_four_connection(pixel.x+1, pixel.y-1, pixel.x, pixel.y) == 0:
                self.segment_pixel(pixel.x+1, pixel.y-1)

            if self.__intercession_four_connection(pixel.x-1, pixel.y-1, pixel.x, pixel.y) == 0:
                self.segment_pixel(pixel.x-1, pixel.y-1)

            iterations += 1

    def __intercession_four_connection(self, x: int, y: int, seed_x: int, seed_y: int):
        four_connection = [(x - 1, y), (x, y - 1), (x, y), (x, y + 1), (x + 1, y)]
        four_connection_seed = [(seed_x - 1, seed_y), (seed_x, seed_y - 1), (seed_x, seed_y), (seed_x, seed_y + 1), (seed_x + 1, seed_y)]

        count_intercession = 0

        for connection in four_connection:
            if connection in four_connection_seed:
                count_intercession += 1
        
        return count_intercession
