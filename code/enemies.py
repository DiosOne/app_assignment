'''
Defines enemy classes and their attributes for combat encounters.

Includes:
- A base `Enemy` class with shared attributes 
    (name, health, armour, light/heavy attack values, and colour).
- Subclasses: `Ratking`, `Skeleton`, and `Goblin`, each with unique stats.
- A `show_enemy_stats()` function to display detailed information about an enemy.

Used in the game's combat system to create and manage enemy encounters.
'''

class Enemy:
    '''
    Base class for all enemy types in the game.

    Attributes:
        name (str): The name of the enemy.
        health (int): The current health points of the enemy.
        armour (int): The enemy's armour class, used to determine hit success.
        attack1 (int): Damage potential of the enemy's light attack.
        attack2 (int): Damage potential of the enemy's heavy attack.
        colour (str): Display colour used for terminal output (Rich library).
    '''

    def __init__(self, name, health, armour, light_attack, heavy_attack, colour):
        self.name = name
        self.health = health
        self.armour = armour
        self.attack1 = light_attack
        self.attack2 = heavy_attack
        self.colour = colour


class Ratking(Enemy):
    '''
    Represents the Ratking enemy type.
    '''

    def __init__(self):
        super().__init__(
            name="Ratking",
            health=14,
            armour=12,
            light_attack=4,
            heavy_attack=8,
            colour='orange4'
        )


class Skeleton(Enemy):
    '''
    Represents the Skeleton enemy type.
    '''

    def __init__(self):
        super().__init__(
            name="Skeleton",
            health=10,
            armour=10,
            light_attack=6,
            heavy_attack=12,
            colour='white'
        )


class Goblin(Enemy):
    '''
    Represents the Goblin enemy type.
    '''

    def __init__(self):
        super().__init__(
            name="Goblin",
            health=20,
            armour=12,
            light_attack=4,
            heavy_attack=8,
            colour='chartreuse4'
        )


def show_enemy_stats(enemy):
    '''
    Displays the stats of a given enemy character.
    '''
    print(enemy.name)
    print('-' * 10)
    print(f'Health: {enemy.health}')
    print(f'Armour Class: {enemy.armour}')
    print(f'Light Attack: {enemy.attack1}')
    print(f'Heavy Attack: {enemy.attack2}')
    print('*' * 10)
    print()
