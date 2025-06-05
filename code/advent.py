'''Module defining player character classes and stats display functions for the adventure game.
'''
from rich import print as rprint

class Adventurer:
    '''Base class for all adventurer player characters.

    :param health: Maximum health points of the adventurer.
    :type health: int
    :param armour: Armour class (defense rating).
    :type armour: int
    :param light_attack: Maximum damage for light attacks.
    :type light_attack: int
    :param heavy_attack: Maximum damage for heavy attacks.
    :type heavy_attack: int
    :param colour: Display colour for the character's name in terminal output.
    :type colour: str
    '''
    def __init__(self, health, armour, light_attack, heavy_attack, colour='white'):
        self.health = health
        self.armour = armour
        self.attack1 = light_attack
        self.attack2 = heavy_attack
        self.colour = colour

class Fighter(Adventurer):
    '''Fighter class: High health and armor, moderate damage.

    Inherits from Adventurer.

    :param Adventurer: Base adventurer class.
    :type Adventurer: class
    '''
    def __init__(self):
        super().__init__(
            health=160,
            armour=13,
            light_attack=6,
            heavy_attack=10,
            colour='bold red'
            )

class Mage(Adventurer):
    '''Mage class: Lower health and armor, higher damage output.

    Inherits from Adventurer.

    :param Adventurer: Base adventurer class.
    :type Adventurer: class
    '''
    def __init__(self):
        super().__init__(
            health=100,
            armour=10,
            light_attack=8,
            heavy_attack=16,
            colour='bold purple'
            )

class Ranger(Adventurer):
    '''Ranger class: High health and armor, lower damage but balanced stats.

    Inherits from Adventurer.

    :param Adventurer: Base adventurer class.
    :type Adventurer: class
    '''
    def __init__(self):
        super().__init__(
            health=200,
            armour=15,
            light_attack=4,
            heavy_attack=8,
            colour='bold green'
            )

def show_stats(character):
    '''Display the stats of a given character using rich formatted print.

    :param character: Adventurer or subclass instance whose stats will be displayed.
    :type character: Adventurer
    '''
    rprint(f'[{character.colour}]{character.__class__.__name__}[/{character.colour}]')
    rprint('-' * 10)
    rprint(f'Health: {character.health}')
    rprint(f'Armour Class: {character.armour}')
    rprint(f'Light Attack max damage: {character.attack1}')
    rprint(f'Heavy Attack max damage: {character.attack2}')
    rprint('*' * 10)
    rprint()
