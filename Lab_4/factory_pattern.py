from entities.plant_class import Plant
from entities.animal_class import Herbivore,Carnivore
from entities.base import EcosystemEntity

class EntityFactory:
    @staticmethod
    def create_entity(entity_type: str, **kwargs) -> EcosystemEntity:
        if entity_type == "plant":
            return Plant(**kwargs)
        elif entity_type == "herbivore":
            return Herbivore(**kwargs)
        elif entity_type == "carnivore":
            return Carnivore(**kwargs)
        raise ValueError(f"Unknown entity type: {entity_type}")