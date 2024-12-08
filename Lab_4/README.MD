# Ecosystem Simulation

This project simulates an ecosystem where plants, herbivores, and carnivores interact within a grid environment. The simulation models energy flow, reproduction, and survival dynamics among different types of entities using Python.

## Features

- **Entities**:
  - **Plants**: Grow energy over time and reproduce under certain conditions.
  - **Herbivores**: Consume plants for energy, move across the grid, and reproduce.
  - **Carnivores**: Hunt herbivores for energy, move across the grid, and reproduce.
- **Factory Pattern**:

  - The `EntityFactory` class simplifies the creation of entities (`Plant`, `Herbivore`, `Carnivore`).

- **Observer Pattern**:

  - Observers, such as `EcosystemObserver`, monitor and display the ecosystem's status in real-time.

- **Simulation Features**:
  - Entity actions (e.g., moving, eating, reproducing).
  - Dynamic tracking of birth and death rates.

## How to Run

1. Create a new Virtual Environment

   - python -m venv venv

   - venv\Scripts\activate

2. Install the required Python packages:

   ```bash
        pip install -r requirements.txt
   ```

3. Run python file named "run.py"
