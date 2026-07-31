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

def add_enemy_potion_drop(drops):
    '''Adds a possible health potion drop to enemy loot.'''

    potion_roll = random.randint(1, 100)
    if potion_roll <= 8:
        drops.append(('Large Health Potion', 1))
    elif potion_roll <= 28:
        drops.append(('Medium Health Potion', 1))
    elif potion_roll <= 58:
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

    add_enemy_potion_drop(drops)
    return drops

def medium_chest():
    '''Generate loot for a medium chest.'''

    return [
        ('Gold', random.randint(50, 100)),
        ('Diamond', random.randint(1, 3)),
        ('Emerald', random.randint(2, 5))
    ]

def large_chest():
    '''Generate loot for the large treasury chest.'''

    drops = [
        ('Gold', random.randint(150, 200)),
        ('Diamond', random.randint(5, 10)),
        ('Emerald', random.randint(10, 15))
    ]
    if random.randint(1, 100) <= 12:
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

    if room_name in room_potions:
        drops.append((room_potions[room_name], 1))

    if room_name == 'Treasury':
        drops.extend(large_chest())

    if room_name in medium_chest_rooms and random.choice([True, False]):
        drops.extend(medium_chest())

    return drops
