
 Wumpus World AI Simulation

A Python-based simulation of the classic **Wumpus World** problem from Artificial Intelligence, where an agent navigates a 4x4 grid world to find gold while avoiding deadly pits and the Wumpus creature.

 Overview

Wumpus World is a knowledge-based environment used to demonstrate **logical reasoning, decision-making, and AI search algorithms**. The agent must:

* Detect **percepts** such as breeze (near pits) and stench (near Wumpus).
* Infer safe squares based on observations.
* Avoid hazards and retrieve the gold successfully.

This project includes:

* A **grid-based 4x4 world** with random or pre-defined placement of pits, Wumpus, and gold.
* An **AI agent** capable of logical inference to make safe moves.
* Optional **visualization** with step-by-step moves showing the agent's decisions.
* **Restart and debug modes** to test different strategies.
* Sound effects and interactive features (optional).

 Features

* Safe navigation using **logical reasoning**.
* Step-by-step simulation of agent decisions.
* Mini-map display showing explored squares.
* Configurable environment for experimentation.

 Technologies

* Python 3.x
* [Ursina Engine](https://www.ursinaengine.org/) (for 3D visualization)
* Standard Python libraries: `random`, `time`, etc.

 How to Run

1. Clone the repository:

   ```bash
   git clone https://github.com/username/wumpus-world.git
   ```
2. Install dependencies:

   ```bash
   pip install ursina
   ```
3. Run the simulation:

   ```bash
   python main.py
   ```

 Project Structure

```
wumpus-world/
├── wumpus.py           # Entry point

└── README.md
```

 Learning Outcomes

* Understanding **knowledge representation** in AI.
* Implementing **decision-making algorithms** based on percepts.
* Experimenting with **safe exploration strategies** in uncertain environments.


Do you want me to do that?
