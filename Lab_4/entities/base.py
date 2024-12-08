from abc import ABC, abstractmethod
from typing import Tuple

class EcosystemEntity(ABC):
    def __init__(self, name: str, energy: float, position: Tuple[int, int], survival_rate: float):
        self.name = name
        self.energy = energy
        self.position = position
        self.survival_rate = survival_rate

    @abstractmethod
    def act(self):
        pass

    @abstractmethod
    def reproduce(self):
        pass
