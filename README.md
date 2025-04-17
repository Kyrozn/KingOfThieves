# King of Thieves - Python Edition 🏰🦝

A 2D stealth and strategy game developed in Python using Tkinter. Inspired by the famous King of Thieves, this project immerses you in a world where you must avoid deadly traps, steal treasures, and protect your own dungeon!

## Features

- 🧱 **2D Gameplay with Tkinter**: Simple yet effective graphical interface with sprites and animations.
- 🌀 **Dodge Traps**: Test your reflexes and avoid obstacles such as Saw, Grindur, and Bomb.
- 🪙 **Collect Treasures**: Complete levels by reaching the chest without dying.
- 📊 **Statistics & Graphs**: Visualize your performance with built-in graphs.

## Installation

### Requirements

**Python 3.x**: Ensure you have Python installed on your system.

**Tkinter**: Usually comes bundled with Python.

**numpy**: For calculations and data manipulation.

**pandas**: For data analysis and statistics.

**matplotlib**: Used to generate performance graphs.

### Installation Steps
Clone the repository:

```bash
git clone https://github.com/Kyrozn/KingOfThieves.git
cd KingOfThieves
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Run the game:

```bash
python .\core\main.py
```

## How to Play

- 🕹️ Just press the space bar — the thief moves automatically.

- ❌ Avoid traps! Colliding with them will reset your progress.

- 🧠 Analyze the environment and plan your movements accordingly.

- 📈 View your performance data through dynamic graphs.

## Project Structure

```
KINGOFTHIEVES/
│
├── core/
│   ├── config.py        # Game configuration settings
│   ├── main.py          # Game entry point
│   └── menu.py          # Main menu interface
│
├── data/
│   ├── data.py          # Data handling logic
│   └── file.csv         # Performance/statistics data
│
├── game/
│   ├── chest.py         # Chest logic
│   ├── door.py          # Door and level exit logic
│   ├── game.py          # Game loop and core gameplay
│   ├── map.py           # Map and level design
│   ├── player.py        # Player class and movement
│   └── trap.py          # Trap definitions (e.g., saws, spikes)
│
├── utils/
│   └── graph.py         # Performance graph generation
│
├── requirements.txt     # Dependencies list
├── .gitignore           # Files and folders to ignore in Git
└── README.md            # Project documentation
```

Authors
Developed by Kyrian & Mathieu

[GitHub](https://github.com/Kyrozn/KingOfThieves/)

Enjoy stealing... or getting stolen from! 🦝🔓