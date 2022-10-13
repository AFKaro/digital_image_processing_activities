from segmentation.region.application.connectivity_strategy_interface import ConnectivityStrategyInterface
from segmentation.region.application.segmentation_by_region_context import SegmentationByRegionContext
from dataclasses import dataclass, field

from segmentation.region.models.region import Region



@dataclass
class Controller:
    image: list
    region: Region = field(default=None)

    def execute(self, seed_x: int, seed_y: int, connective: ConnectivityStrategyInterface) -> None:
        segmentation_alg = SegmentationByRegionContext()
        segmentation_alg.set_strategy(connective(self.image))
        segmentation_alg.segment(seed_x, seed_y)
        self.image = segmentation_alg.strategy.image
        self.region = segmentation_alg.strategy.region