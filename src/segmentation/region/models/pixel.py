from dataclasses import dataclass


@dataclass
class Pixel:
    x: int
    y: int
    value: int