#possible loot
'''Module for handling enemy loot generation.

Provides functions to randomly generate loot based on the defeated enemy type.
'''
import random

def add_drop(drops, item, min_amount, max_amount):
    '''Adds an item to a drop list if the rolled amount is greater than zero.'''

    amount = random.randint(min_amount, max_amount)
    if amount > 0:
        drops.append((item, amount))

def random_enemy(enemy_name):
    '''Generate loot drops for a defeated enemy.

    :param enemy_name: Name of the defeated enemy.
    :type enemy_name: str
    :return: List of item and quantity tuples dropped by the enemy.
    :rtype: list[tuple(str, int)]
    '''

    drops = []

    if enemy_name == 'Ratking':
        add_drop(drops, 'Junk', 1, 5)
        add_drop(drops, 'Gold', 10, 15)
        add_drop(drops, 'Garnet', 0, 3)

    elif enemy_name == 'Skeleton':
        add_drop(drops, 'Gold', 15, 30)
        add_drop(drops, 'Ruby', 1, 3)
        weapon = random.choice(['Sharp Dagger', 'Shortsword', None])
        if weapon is not None:
            add_drop(drops, weapon, 1, 1)

    elif enemy_name == 'Goblin':
        add_drop(drops, 'Junk', 10, 20)
        add_drop(drops, 'Gold', 20, 50)
        add_drop(drops, 'Ruby', 0, 4)
        add_drop(drops, 'Emerald', 1, 2)
        add_drop(drops, random.choice(['Old Dagger', 'Scimitar']), 1, 1)

    elif enemy_name == 'Zombie':
        add_drop(drops, 'Junk', 20, 35)
        add_drop(drops, 'Gold', 35, 45)

    elif enemy_name == 'Thug':
        add_drop(drops, 'Gold', 40, 50)
        add_drop(drops, 'Emerald', 1, 2)
        add_drop(drops, 'Diamond', 0, 1)
        add_drop(drops, 'Garnet', 2, 4)
        add_drop(drops, 'Sharp Dagger', 1, 1)

    elif enemy_name == 'Ghost':
        add_drop(drops, 'Junk', 1, 1)

    elif enemy_name == 'Bone Devil':
        add_drop(drops, 'Gold', 80, 90)
        add_drop(drops, 'Emerald', 0, 3)

    elif enemy_name == 'Minotaur':
        add_drop(drops, 'Gold', 85, 95)
        add_drop(drops, 'Diamond', 1, 4)

    return drops
