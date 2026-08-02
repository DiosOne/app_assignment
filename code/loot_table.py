#possible loot
'''Module for handling enemy loot generation.

Provides functions to randomly generate loot based on defeated enemies and searched rooms.
'''
import random

def add_drop(drops, item, min_amount, max_amount):
    '''Adds an item to a drop list if the rolled amount is greater than zero.'''

    amount = random.randint(min_amount, max_amount)
    if amount > 0:
        drops.append((item, amount))

def chance_drop(drops, chance, item, min_amount, max_amount):
    '''Adds an item to a drop list if a percentage chance succeeds.'''

    if random.randint(1, 100) <= chance:
        add_drop(drops, item, min_amount, max_amount)

def add_enemy_potion_drop(drops):
    '''Adds a possible health potion drop to enemy loot.'''

    potion_roll = random.randint(1, 100)
    if potion_roll <= 3:
        drops.append(('Large Health Potion', 1))
    elif potion_roll <= 10:
        drops.append(('Medium Health Potion', 1))
    elif potion_roll <= 25:
        drops.append(('Small Health Potion', 1))

def random_enemy(enemy_name):
    '''Generate loot drops for a defeated enemy.

    :param enemy_name: Name of the defeated enemy.
    :type enemy_name: str
    :return: List of item and quantity tuples dropped by the enemy.
    :rtype: list[tuple(str, int)]
    '''

    drops = []

    if enemy_name == 'Ratking':
        chance_drop(drops, 70, 'Junk', 1, 3)
        chance_drop(drops, 55, 'Gold', 5, 10)
        chance_drop(drops, 15, 'Garnet', 1, 2)

    elif enemy_name == 'Skeleton':
        chance_drop(drops, 60, 'Gold', 8, 18)
        chance_drop(drops, 20, 'Ruby', 1, 2)
        weapon = random.choices(['Sharp Dagger', 'Shortsword', None], weights=[10, 10, 80])[0]
        if weapon is not None:
            add_drop(drops, weapon, 1, 1)

    elif enemy_name == 'Goblin':
        chance_drop(drops, 75, 'Junk', 1, 3)
        chance_drop(drops, 65, 'Gold', 10, 25)
        chance_drop(drops, 15, 'Ruby', 1, 2)
        chance_drop(drops, 10, 'Emerald', 1, 1)
        if random.randint(1, 100) <= 20:
            add_drop(drops, random.choice(['Old Dagger', 'Scimitar']), 1, 1)

    elif enemy_name == 'Zombie':
        chance_drop(drops, 70, 'Junk', 1, 3)
        chance_drop(drops, 35, 'Gold', 10, 25)

    elif enemy_name == 'Thug':
        chance_drop(drops, 75, 'Gold', 20, 35)
        chance_drop(drops, 25, 'Emerald', 1, 1)
        chance_drop(drops, 8, 'Diamond', 1, 1)
        chance_drop(drops, 35, 'Garnet', 1, 2)
        chance_drop(drops, 20, 'Sharp Dagger', 1, 1)

    elif enemy_name == 'Ghost':
        chance_drop(drops, 30, 'Junk', 1, 1)

    elif enemy_name == 'Bone Devil':
        chance_drop(drops, 70, 'Gold', 35, 55)
        chance_drop(drops, 25, 'Emerald', 1, 2)

    elif enemy_name == 'Minotaur':
        chance_drop(drops, 80, 'Gold', 40, 60)
        chance_drop(drops, 35, 'Diamond', 1, 2)

    add_enemy_potion_drop(drops)
    return drops

def medium_chest():
    '''Generate loot for a medium chest.'''

    return [
        ('Gold', random.randint(25, 50)),
        ('Diamond', random.randint(0, 1)),
        ('Emerald', random.randint(1, 3))
    ]

def large_chest():
    '''Generate loot for the large treasury chest.'''

    drops = [
        ('Gold', random.randint(90, 130)),
        ('Diamond', random.randint(2, 5)),
        ('Emerald', random.randint(4, 8))
    ]
    if random.randint(1, 100) <= 8:
        drops.append((random.choice(['Medium Health Potion', 'Large Health Potion']), 1))
    return drops

def random_room_treasure(room_name):
    '''Generate treasure found by searching a room.

    :param room_name: Name of the searched room.
    :type room_name: str
    :return: List of item and quantity tuples found in the room.
    :rtype: list[tuple(str, int)]
    '''

    drops = []

    room_potions = {
        'Bedroom':'Large Health Potion',
        'Library':'Large Health Potion',
        'Scullery':'Large Health Potion',
        'Guard Post':'Small Health Potion',
        'Servants Quarters':'Small Health Potion',
        'Dining Hall':'Small Health Potion',
        'Armoury':'Medium Health Potion',
        'Chapel':'Medium Health Potion',
        'Observatory':'Medium Health Potion'
    }

    medium_chest_rooms = ['Servants Quarters', 'Guard Post', 'Bedroom', 'Armoury', 'Library']

    if room_name in room_potions and random.randint(1, 100) <= 60:
        drops.append((room_potions[room_name], 1))

    if room_name == 'Treasury':
        drops.extend(large_chest())

    if room_name in medium_chest_rooms and random.randint(1, 100) <= 35:
        drops.extend(medium_chest())

    if not drops:
        drops.append(('Gold', random.randint(5, 15)))

    return [(item, quantity) for item, quantity in drops if quantity > 0]
