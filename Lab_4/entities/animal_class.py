import random 
from typing import Tuple
from .base import EcosystemEntity
from entities.plant_class import Plant

class Animal(EcosystemEntity):
    def __init__(self, name: str, energy: float, position: Tuple[int, int], survival_rate: float, speed: int, diet: str):
        super().__init__(name, energy, position, survival_rate)
        self.speed = speed
        self.diet = diet

    def eat(self,prey=EcosystemEntity):
        pass

    def move(self):
        self.position=(
            self.position[0]+random.randint(-self.speed,self.speed),
            self.position[1]+random.randint(-self.speed,self.speed)
        )
        self.energy-=0.7

class Herbivore(Animal):
    def __init__(self, name: str, energy: int, position: Tuple[int, int], survival_rate: float, speed: int):
        super().__init__(name, energy, position, survival_rate, speed, 'plant')

    def eat(self,prey:EcosystemEntity):
        if isinstance(prey,Plant) and prey.energy>0:
            self.energy+=prey.energy
            prey.energy=0
        
    def act(self):
        self.move()

    def reproduce(self):
        if random.random()<self.survival_rate:
            return Herbivore(
                name=self.name,
                energy=self.energy//2,
                position=(self.position[0]+random.randint(-1,1),
                          self.position[1]+random.randint(-1,1)),
                          survival_rate=self.survival_rate,
                          speed=self.speed
            )
        return None
    
class Carnivore(Animal):
    def __init__(self, name: str, energy: int, position: Tuple[int, int], survival_rate: float, speed: int):
        super().__init__(name, energy, position, survival_rate, speed, "animal")

    def eat(self, prey: EcosystemEntity):
        if isinstance(prey, Animal) and prey.energy > 0:
            self.energy += prey.energy
            prey.energy = 0

    def act(self):
        self.move()

    def reproduce(self):
        if random.random() < self.survival_rate:
            return Carnivore(
                name=self.name,
                energy=self.energy // 2,
                position=(self.position[0] + random.randint(-1, 1), self.position[1] + random.randint(-1, 1)),
                survival_rate=self.survival_rate,
                speed=self.speed
            )
        return None
