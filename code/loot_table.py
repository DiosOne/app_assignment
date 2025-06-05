#possible loot
'''Module for handling random loot generation from chests and enemies.

Provides functions to randomly select items and their quantities
based on predefined loot tables for chests and enemies.
'''
import random
chest_dict= {
    'Gold': 200,
    'Diamonds': 5,
    'Rubies': 10,
    'Emeralds': 20,
    'Garnet': 30,
    'Sharp Dagger': 5,
    }
enemy_drop= {
    'Gold': 50,
    'Rubies': 5,
    'Garnet': 10,
    'Old Dagger': 5,
    'Junk': 10
}
def random_chest():
    '''Select a random item and quantity from the chest loot table.

    :return: Tuple containing the item name and quantity found in the chest.
    :rtype: tuple(str, int)
    '''

    item= random.choice(list(chest_dict.keys()))
    max_amount= chest_dict[item]
    amount= random.randint(1, max_amount)
    return(item, amount)

def random_enemy():
    '''Select a random item and quantity from the enemy drop loot table.

    :return: Tuple containing the item name and quantity dropped by the enemy.
    :rtype: tuple(str, int)
    '''

    item= random.choice(list(enemy_drop.keys()))
    max_amount= enemy_drop[item]
    amount= random.randint(1, max_amount)
    return(item, amount)
