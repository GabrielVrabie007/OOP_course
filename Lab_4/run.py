from simulation import EcosystemSimulation,main_menu
from observer import EcosystemObserver
from factory_pattern import EntityFactory
import random

def main():
    ecosystem = EcosystemSimulation((10, 10))
    observer = EcosystemObserver()
    ecosystem.add_observer(observer)

    for i in range(2):
        ecosystem.add_entity(EntityFactory.create_entity(
            "plant",
            name=f"Plant{i + 1}",
            energy=10,
            position=(random.randint(0, 9), random.randint(0, 9)),
            survival_rate=0.6
        ))

    for i in range(2):
        ecosystem.add_entity(EntityFactory.create_entity(
            "herbivore",
            name=f"Rabbit{i + 1}",
            energy=20,
            position=(random.randint(0, 9), random.randint(0, 9)),
            survival_rate=0.7,
            speed=2
        ))

    for i in range(2):
        ecosystem.add_entity(EntityFactory.create_entity(
            "carnivore",
            name=f"Wolf{i + 1}",
            energy=30,
            position=(random.randint(0, 9), random.randint(0, 9)),
            survival_rate=0.5,
            speed=3
        ))

    while True:
        print(f"\n----------------- Simulation Step: {ecosystem.step_count} -------------------------\n")
        ecosystem.simulate()
        try:
            user_input = input("Press Enter to continue simulation, 'menu' for menu, or 'stop' to end: ")
            if user_input.lower() == "menu":
                main_menu(ecosystem)
            elif user_input.lower() == "stop":
                print("Simulation stopped.")
                break
        except KeyboardInterrupt:
         print("\nSimulation interrupted by user.")
        
if __name__ =="__main__":
    main()