from typing import List
from entities.base import EcosystemEntity

class Observer:
    def update(self,entities:List[EcosystemEntity]):
        pass

class EcosystemObserver(Observer):
    def update(self, entities: List[EcosystemEntity]):
        print("\nEcosystem Status")
        print("----------------------------------------------------")
        for entity in entities:
            print(f"{entity.name} at {entity.position} with energy {entity.energy:.2f}")