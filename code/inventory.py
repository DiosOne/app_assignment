'''
Inventory management module for the text adventure game.

Provides functionality to:
- Store collected loot items in a global inventory list.
- Add new items (with optional quantities) to the inventory.
- Display the current contents of the inventory using styled terminal output via Rich.

Dependencies:
- rich: For enhanced terminal formatting and user feedback.
'''

from rich import print as rprint
inventory = []
max_carry_weight = 250

item_weights = {
    'Gold':0.1,
    'Ruby':3,
    'Rubies':3,
    'Emerald':3,
    'Emeralds':3,
    'Garnet':2,
    'Diamond':4,
    'Diamonds':4,
    'Junk':1,
    'Old Dagger':5,
    'Sharp Dagger':5,
    'Shortsword':7,
    'Scimitar':7,
    'Greatsword':9,
    'Battleaxe':8,
    'Warhammer':8,
    'Halberd':9,
    'Handaxe':5,
    'Twin Daggers':6,
    'Rapier':6,
    'Hunter Bow':7,
    'Crossbow':7,
    'Poison Arrow':2,
    'Spell Scroll: Ice Knife':1,
    'Spell Scroll: Magic Missile':1,
    'Spell Scroll: Lightning Bolt':1,
    'Spell Scroll: Acid Arrow':1,
    'Spell Scroll: Flame Lance':1,
    'Small Health Potion':10,
    'Medium Health Potion':20,
    'Large Health Potion':40
}

def add_to_inv(item, quantity=1):
    '''
    Adds one or more of the specified item to the player's inventory.

    :param item: The item to add to the inventory.
    :type item: str
    :param quantity: The number of times to add the item, defaults to 1.
    :type quantity: int, optional
    '''

    for _ in range(quantity):
        inventory.append(item)

def item_weight(item):
    '''
    Gets the weight of an item.
    '''

    return item_weights.get(item, 1)

def current_weight():
    '''
    Gets the current total inventory weight.
    '''

    return sum(item_weight(item) for item in inventory)

def displayed_weight():
    '''
    Gets the current inventory weight rounded to one decimal place for display.
    '''

    return round(current_weight(), 1)

def can_carry(item, quantity=1):
    '''
    Checks whether the inventory can carry the requested item quantity.
    '''

    return current_weight() + item_weight(item) * quantity <= max_carry_weight

def remove_from_inv(item):
    '''
    Removes one of the specified item from the player's inventory.

    :param item: The item to remove from the inventory.
    :type item: str
    :return: True if the item was removed, otherwise False.
    :rtype: bool
    '''

    if item in inventory:
        inventory.remove(item)
        return True
    return False

def count_inv():
    '''
    Counts the player's inventory items.

    :return: Dictionary of item names and their quantities.
    :rtype: dict
    '''

    counted= {}
    for item in inventory:
        counted[item]= counted.get(item, 0) + 1
    return counted

def drop_item(item, quantity=1):
    '''
    Drops one or more of an item from the inventory.
    '''

    dropped = 0
    for _ in range(quantity):
        if remove_from_inv(item):
            dropped += 1
        else:
            break
    return dropped

def show_inv(player=None):
    '''
    Displays the player's inventory. Shows item names and their quantities.
    If the inventory is empty, a message is printed to indicate that.

    :param player: Optional player whose health will be displayed.
    :type player: Adventurer or subclass instance, optional
    '''

    if player is not None:
        rprint(
            f'[cyan]Health: [{player.colour}]{player.health}'
            f'[/{player.colour}]/{player.max_health}[/cyan]'
        )
    rprint(f'[cyan]Carry Weight: {displayed_weight()}/{max_carry_weight}[/cyan]')

    if not inventory:
        rprint('[bright_black]Your inventory is empty.[/bright_black]')
    else:
        rprint('[dodger_blue1][bold]Your inventory: [/bold][/dodger_blue1]')
        counted= count_inv()
        for item, count in counted.items():
            rprint(f'- {item} x {count}')

def clear_inv():
    '''
    Clears all items from the player's inventory.
    '''

    inventory.clear()
