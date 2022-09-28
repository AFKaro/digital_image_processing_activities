from segmentation.region.application.connectivity_strategy_interface import ConnectivityStrategyInterface
from dataclasses import field

from segmentation.region.models.region import Region


class SegmentationByRegionContext:
    _strategy: ConnectivityStrategyInterface = field(init=False, default=None)

    def get_strategy(self) -> ConnectivityStrategyInterface:
        return self._strategy

    def set_strategy(self, strategy: ConnectivityStrategyInterface) -> None:
        self._strategy = strategy

    def segment(self, seed_x: int, seed_y: int) -> None:
        self._strategy.execute(seed_x, seed_y)
    
    def get_region(self) -> Region:
        return self._strategy.region

    strategy = property(fget=get_strategy, fset=set_strategy)