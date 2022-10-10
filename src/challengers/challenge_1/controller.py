from challengers.challenge_1.segmentation_by_limiar import SegmentationByLimiar
from challengers.challenge_1.smoothing_filter import SmoothingFilter
from dataclasses import dataclass, field


@dataclass
class Controller:
    image: list
    tolerance: float = field(default=0.01)

    def execute(self, init_t: float = None) -> list:
        segmentation_alg = SegmentationByLimiar()
        smothing_alg = SmoothingFilter()
        iterations = 0

        # Initialize T Value
        if init_t is None:
            segmentation_alg.calcule_limiar(self.image)
        else:
            segmentation_alg.t_value = init_t

        while abs(segmentation_alg.t_value - segmentation_alg.t_value_ant) > self.tolerance:
            self.image = smothing_alg.smothing(self.image)
            segmentation_alg.calcule_limiar(self.image)

            iterations += 1
            dif = abs(segmentation_alg.t_value - segmentation_alg.t_value_ant)
            print(
                f"Iteration: {iterations}, T Value: {segmentation_alg.t_value}, T Ant: {segmentation_alg.t_value_ant}, dif: {dif}"
            )

        return segmentation_alg.get_new_img(self.image)
