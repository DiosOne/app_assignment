'''Module defining player character classes and stats display functions for the adventure game.
'''
import re
from rich import print as rprint

SUN_YELLOW = '#FCCF03'

def colour_dice(damage):
    '''
    Colours dice expressions for display.
    '''

    return re.sub(r'\d+d\d+', rf'[{SUN_YELLOW}]\g<0>[/{SUN_YELLOW}]', damage)

class Adventurer:
    '''Base class for all adventurer player characters.

    :param health: Maximum health points of the adventurer.
    :type health: int
    :param armour: Armour class (defense rating).
    :type armour: int
    :param attacks: Attack options available to the adventurer.
    :type attacks: list
    :param colour: Display colour for the character's name in terminal output.
    :type colour: str
    '''
    def __init__(self, health, armour, attacks, colour='white'):
        self.max_health = health
        self.health = health
        self.armour = armour
        self.attacks = attacks
        self.colour = colour

class Fighter(Adventurer):
    '''Fighter class: High health and armor, moderate damage.

    Inherits from Adventurer.

    :param Adventurer: Base adventurer class.
    :type Adventurer: class
    '''
    def __init__(self):
        super().__init__(
            health=95,
            armour=17,
            attacks=[
                {'name':'Longsword', 'hit_bonus':5, 'damage':'1d10+1'},
                {'name':'Heavy Crossbow', 'hit_bonus':3, 'damage':'1d10+5'}
            ],
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
            health=80,
            armour=15,
            attacks=[
                {'name':'Fire Bolt', 'hit_bonus':5, 'damage':'1d10'},
                {'name':'Scorching Ray', 'hit_bonus':5, 'damage':'2d6', 'times':3}
            ],
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
            health=90,
            armour=16,
            attacks=[
                {'name':'Shortsword', 'hit_bonus':4, 'damage':'1d6+2', 'times':2},
                {'name':'Longbow', 'hit_bonus':4, 'damage':'1d8+2', 'times':2}
            ],
            colour='bold green'
            )

def show_stats(character):
    '''Display the stats of a given character using rich formatted print.

    :param character: Adventurer or subclass instance whose stats will be displayed.
    :type character: Adventurer
    '''
    rprint(f'[{character.colour}]{character.__class__.__name__}[/{character.colour}]')
    rprint('-' * 10)
    rprint(f'Health: [cyan]{character.health}[/cyan]')
    rprint(f'Armour Class: [cyan]{character.armour}[/cyan]')
    for attack in character.attacks:
        rprint(
            f"{attack['name']}: [cyan]+{attack['hit_bonus']} to hit[/cyan], "
            f"{colour_dice(attack['damage'])} damage"
        )
    rprint('*' * 10)
    rprint()
