import random
from .base import EcosystemEntity

class Plant(EcosystemEntity):
    def act(self):
        self.energy += 1

    def reproduce(self):
        if random.random() < self.survival_rate:
            return Plant(
                name=self.name,
                energy=self.energy,
                position=(self.position[0] + random.randint(-1, 1), self.position[1] + random.randint(-1, 1)),
                survival_rate=self.survival_rate
            )
        return None
