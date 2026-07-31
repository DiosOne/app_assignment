'''
Defines enemy classes and their attributes for combat encounters.

Includes:
- A base `Enemy` class with shared attributes.
- Subclasses for each enemy type, each with unique stats and attacks.
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
        attacks (list): Enemy attack options with hit bonus, damage dice, and repeat count.
        colour (str): Display colour used for terminal output (Rich library).
    '''

    def __init__(self, name, health, armour, attacks, colour):
        self.name = name
        self.health = health
        self.armour = armour
        self.attacks = attacks
        self.colour = colour


class Ratking(Enemy):
    '''
    Represents the Ratking enemy type.
    '''

    def __init__(self):
        super().__init__(
            name="Ratking",
            health=24,
            armour=10,
            attacks=[
                {'name':'Bites', 'hit_bonus':2, 'damage':'2d6', 'times':2}
            ],
            colour='orange4'
        )


class Skeleton(Enemy):
    '''
    Represents the Skeleton enemy type.
    '''

    def __init__(self):
        super().__init__(
            name="Skeleton",
            health=13,
            armour=13,
            attacks=[
                {'name':'Shortsword', 'hit_bonus':4, 'damage':'1d6+2'},
                {'name':'Shortbow', 'hit_bonus':4, 'damage':'1d6+2'}
            ],
            colour='white'
        )


class Goblin(Enemy):
    '''
    Represents the Goblin enemy type.
    '''

    def __init__(self):
        super().__init__(
            name="Goblin",
            health=7,
            armour=15,
            attacks=[
                {'name':'Scimitar', 'hit_bonus':4, 'damage':'1d6+2'},
                {'name':'Shortbow', 'hit_bonus':4, 'damage':'1d6+2'}
            ],
            colour='chartreuse4'
        )


class Zombie(Enemy):
    '''
    Represents the Zombie enemy type.
    '''

    def __init__(self):
        super().__init__(
            name="Zombie",
            health=22,
            armour=8,
            attacks=[
                {'name':'Slam', 'hit_bonus':3, 'damage':'1d6+1', 'times':2}
            ],
            colour='dark_sea_green4'
        )


class Thug(Enemy):
    '''
    Represents the Thug enemy type.
    '''

    def __init__(self):
        super().__init__(
            name="Thug",
            health=32,
            armour=11,
            attacks=[
                {'name':'Mace', 'hit_bonus':4, 'damage':'1d6+2'},
                {'name':'Heavy Crossbow', 'hit_bonus':2, 'damage':'1d10'}
            ],
            colour='dark_goldenrod'
        )


class Ghost(Enemy):
    '''
    Represents the Ghost enemy type.
    '''

    def __init__(self):
        super().__init__(
            name="Ghost",
            health=45,
            armour=11,
            attacks=[
                {'name':'Withering Touch', 'hit_bonus':5, 'damage':'4d6+3'},
                {'name':'Shock', 'hit_bonus':4, 'damage':'2d8'}
            ],
            colour='bright_cyan'
        )


class BoneDevil(Enemy):
    '''
    Represents the Bone Devil enemy type.
    '''

    def __init__(self):
        super().__init__(
            name="Bone Devil",
            health=32,
            armour=16,
            attacks=[
                {'name':'Claw', 'hit_bonus':8, 'damage':'1d6+4'},
                {'name':'Sting', 'hit_bonus':8, 'damage':'1d8+4+1d6'}
            ],
            colour='bright_red'
        )


class Minotaur(Enemy):
    '''
    Represents the Minotaur enemy type.
    '''

    def __init__(self):
        super().__init__(
            name="Minotaur",
            health=76,
            armour=14,
            attacks=[
                {'name':'Greataxe', 'hit_bonus':6, 'damage':'2d8+4'},
                {'name':'Gore', 'hit_bonus':6, 'damage':'1d8+4'}
            ],
            colour='red3'
        )


def show_enemy_stats(enemy):
    '''
    Displays the stats of a given enemy character.
    '''
    print(enemy.name)
    print('-' * 10)
    print(f'Health: {enemy.health}')
    print(f'Armour Class: {enemy.armour}')
    for attack in enemy.attacks:
        print(
            f"{attack['name']}: +{attack['hit_bonus']} to hit, "
            f"{attack['damage']} damage"
        )
    print('*' * 10)
    print()
