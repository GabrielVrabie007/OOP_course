import random
from typing import List,Tuple
from factory_pattern import EntityFactory
from observer import Observer,EcosystemObserver
from entities.base import EcosystemEntity


class EcosystemSimulation:
    def __init__(self, size: Tuple[int, int]):
        self.size = size
        self.entities: List[EcosystemEntity] = []
        self.observers: List[Observer] = []
        self.total_born: List[EcosystemEntity] = []
        self.total_died: List[EcosystemEntity] = []
        self.step_count = 0

    def add_entity(self, entity: EcosystemEntity):
        self.entities.append(entity)
        self.total_born.append(entity)

    def remove_entity(self, entity: EcosystemEntity):
        if entity in self.entities:
            self.entities.remove(entity)
            self.total_died.append(entity)

    def add_observer(self, observer: Observer):
        self.observers.append(observer)

    def remove_observer(self, observer: Observer):
        self.observers.remove(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.update(self.entities)

    def simulate(self):
        self.step_count += 1
        for entity in self.entities[:]:
            entity.act()

            new_entity = entity.reproduce()
            if new_entity:
                new_entity.name += f"_{self.step_count}"
                self.add_entity(new_entity)

            if entity.energy <= 0:
                self.remove_entity(entity)

        self.notify_observers()

    def display_alive(self):
        print("\nTotal Entities Alive:")
        print("----------------------------------------------------")
        displayed = set()
        for entity in self.entities:
            if entity not in displayed:
                print(f"{entity.name} at {entity.position} with energy {entity.energy:.2f}")
                displayed.add(entity)

    def display_born(self):
        print("\nEntities Born:")
        print("----------------------------------------------------")
        for entity in self.total_born:
            print(f"{entity.name} born at {entity.position}")
        self.total_born = []

    def display_died(self):
        print("\nEntities Died:")
        print("----------------------------------------------------")
        for entity in self.total_died:
            print(f"{entity.name} died at {entity.position}") 
        self.total_died = []



def main_menu(simulation: EcosystemSimulation):
    while True:
        print("\nEcosystem Menu")
        print("----------------------------------------------------")
        print("1. View all living entities")
        print("2. View entities born")
        print("3. View entities died")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            simulation.display_alive()
        elif choice == "2":
            simulation.display_born()
        elif choice == "3":
            simulation.display_died()
        elif choice == "4":
            print("Exiting menu.")
            break
        else:
            print("Invalid choice. Please try again.")