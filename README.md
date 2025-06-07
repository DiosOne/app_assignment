# Text Adventure

A terminal-based Python adventure game where players choose a class, explore rooms, fight enemies, find loot, and try to survive. The game features inventory management, random encounters, and stylized terminal output using `rich`.

---

## Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/DiosOne/app_assignment.git
cd code (this folder contains everything)
```

### 2. Set up Virtual Environment

using `pyenv`

```bash
pyenv virtualenv 3.12.3 textadventure
pyenv local textadventure
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the game

```bash
python main.py
```

## Required Files and Modules

- `main.py`: Main game logic and loop
- `rooms.py`: Room definitions and connections
- `advent.py`: Player classes
- `enemies.py`: Enemy classes
- `dice_rolls.py`: Random number generator for 'dice rolls'
- `loot_table.py`: Random enemy and chest loot generation
- `attacks.py`: Combat logic
- `inventory.py`: Inventory management

## External Dependencies

`rich`

- Purpose: Enhanced terminal output (colours, prompts, panels)
- License: MIT license [GitHub page](https://github.com/Textualize/rich?tab=MIT-1-ov-file)
- Legal Use: Free to use, modify, and distribute with credit
- Ethical Use: Fully open-source, no data collection, widely accepted in open-source Python projects

## Troubleshooting

- Use `python3` if `python` defaults to version 2
- Activate virtual environment before running the game
- I had one instance where `rich` wasnt working but running `test_rich.py` restarted it

## License

This project is for non-commercial, educational use.  
All original code by Dom Andrewartha aka DiosOne &copy; 2025  
Third-party package `rich` is used under the MIT License.
