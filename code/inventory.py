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

def show_inv():
    '''
    Displays the player's inventory. Shows item names and their quantities.
    If the inventory is empty, a message is printed to indicate that.
    '''

    if not inventory:
        rprint('[bright_black]Your inventory is empty.[/bright_black]')
    else:
        rprint('[dodger_blue1][bold]Your inventory: [/bold][/dodger_blue1]')
        counted= {}
        for item in inventory:
            counted[item]= counted.get(item, 0) + 1
        for item, count in counted.items():
            rprint(f'- {item} x {count}')
