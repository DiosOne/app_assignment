'''
Defines enemy classes and their attributes for combat encounters.

Includes:
- A base `Enemy` class with shared attributes (name, health, armour, light/heavy attack values, and colour).
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

    def __init__(self, name, health, armour, lightAttack, heavyAttack, colour):
        self.name= name
        self.health= health
        self.armour= armour
        self.attack1= lightAttack
        self.attack2= heavyAttack
        self.colour= colour


class Ratking(Enemy):
    '''
    Represents the Ratking enemy type.

    Inherits from:
        Enemy: Base class containing shared enemy attributes and methods.

    Attributes (inherited from Enemy):
        name (str): "Ratking"
        health (int): 14
        armour (int): 12
        attack1 (int): 4 (light attack damage)
        attack2 (int): 8 (heavy attack damage)
        colour (str): "orange4" (used for terminal display)
    '''

    def __init__(self):
        super().__init__(name="Ratking", health=14, armour=12, lightAttack=4, heavyAttack=8, colour='orange4')


class Skeleton(Enemy):
    '''
    Represents the Skeleton enemy type.

    Inherits from:
        Enemy: Base class containing common enemy attributes and behavior.

    Attributes (inherited from Enemy):
        name (str): "Skeleton"
        health (int): 10
        armour (int): 10
        attack1 (int): 6 (light attack damage)
        attack2 (int): 12 (heavy attack damage)
        colour (str): "white" (used for terminal display)
    '''

    def __init__(self):
        super().__init__(name="Skeleton", health=10, armour=10, lightAttack=6, heavyAttack=12, colour='white')


class Goblin(Enemy):
    '''
    Represents the Goblin enemy type.

    Inherits from:
        Enemy: Base class containing common enemy attributes and behavior.

    Attributes (inherited from Enemy):
        name (str): "Goblin"
        health (int): 20
        armour (int): 12
        attack1 (int): 4 (light attack damage)
        attack2 (int): 8 (heavy attack damage)
        colour (str): "chartreuse4" (used for terminal display)
    '''

    def __init__(self):
        super().__init__(name="Goblin", health=20, armour=12, lightAttack=4, heavyAttack=8, colour='chartreuse4')


def show_enemy_stats(enemy):
    '''
    Displays the stats of a given enemy character.

    Parameters:
        enemy (Enemy): An instance of an Enemy or its subclass (e.g., Goblin, Skeleton, Ratking).
    '''

    print(enemy.name)
    print('-' * 10)
    print(f'Health: {enemy.health}')
    print(f'Armour Class: {enemy.armour}')
    print(f'Light Attack: {enemy.attack1}')
    print(f'Heavy Attack: {enemy.attack2}')
    print('*' * 10)
    print()
