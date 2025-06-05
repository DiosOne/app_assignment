'''
Text Adventure Game - Main Entry Point

This module contains the main logic and game loop for a terminal-based text adventure.
Players can choose a character class, explore interconnected rooms, encounter enemies, 
find loot, and progress toward an exit.

Features:
- Class selection: Fighter, Mage, or Ranger.
- Random enemy encounters and chest loot.
- Inventory management and turn-based combat.
- Rich text output for enhanced terminal display.

Entry point: game_loop()

Requires:
- rich
- modules: rooms, advent, enemies, loot_table, attacks, inventory
'''

import random
from rooms import rooms
from rich import print as rprint
from rich.panel import Panel
from rich.prompt import Prompt
from advent import Fighter, Mage, Ranger, show_stats
from enemies import Goblin, Skeleton, Ratking
from loot_table import random_chest, random_enemy
from attacks import fight_enemy
from inventory import add_to_inv, show_inv


collected_loot= []
looted_rooms= set()
fought_rooms= set()

def choose_player_class():
    '''
    Prompts the player to choose a character class.

    Offers a choice between Fighter, Mage, or Ranger. Repeats the prompt 
    until a valid class is selected, then returns an instance of the chosen class.

    :return: An instance of the selected player class.
    :rtype: Fighter | Mage | Ranger
    '''
    rprint('Choose your class: [bold bright_red]Fighter[/bold bright_red], '
           '[bold purple]Mage[/bold purple], [bold green]Ranger[/bold green]')
    while True:
        choice= input('Class: ').capitalize()
        if choice== 'Fighter':
            return Fighter()
        elif choice== 'Mage':
            return Mage()
        elif choice== 'Ranger':
            return Ranger()
        else:
            rprint('Invalid class, try again')

player= choose_player_class()
rprint(f"[bold yellow]You have chosen the[/bold yellow] "
       f"[{player.colour}]{player.__class__.__name__}[/{player.colour}]")
show_stats(player)


def show_room(room_name):
    '''
    Displays the current room's name, description, and available exits using a styled panel.

    :param room_name: The key name of the room to display from the rooms dictionary.
    :type room_name: str
    '''
    room= rooms[room_name]
    exits= ', '.join(room['exits'].keys())
    rprint(Panel(
        f'[bright_blue]{room.get("display_name", room_name)}[/bright_blue]\n\n'
        f'{room['description']}\n\n'
        f'[grey66]Exits:[/grey66]{exits}',
        title='Room Info'
    ))

def spawn_enemy_and_fight(room_name):
    """
    Spawns a random enemy and initiates combat. If the player wins, they receive loot.
    Marks the room as fought to prevent repeat encounters.

    Args:
        room_name (str): The name of the room where the encounter is happening.

    Returns:
        str or bool: Returns 'win' if the enemy is defeated,
                     False if the player dies or flees,
                     or None if no combat occurs.
    """

    enemy_class = random.choice([Goblin, Skeleton, Ratking])
    enemy = enemy_class()
    rprint(f"[red]An enemy [{enemy.colour}]{enemy.name}[/{enemy.colour}] appears![/red]")
    result = fight_enemy(player, enemy)
    if result == 'win':
        drop = random_enemy()
        add_to_inv(drop[0], drop[1])
        collected_loot.append(drop)
        rprint(f"[bright_green]The enemy dropped {drop[1]} x {drop[0]}![/bright_green]")
        fought_rooms.add(room_name)
    return result

def spawn_chest_and_loot(room_name):
    """
    Spawns a chest with loot in the specified room if not already looted.
    Adds the loot to the player's inventory and marks the room as looted.

    Args:
        room_name (str): The name of the room where the chest is located.

    Returns:
        tuple or None: Returns the loot item and quantity if loot is found,
                       otherwise None if the chest has already been looted.
    """

    loot_found = random_chest()
    add_to_inv(loot_found[0], loot_found[1])
    collected_loot.append(loot_found)
    looted_rooms.add(room_name)
    rprint(f"[yellow]You found {loot_found[1]} x {loot_found[0]} in a chest![/yellow]")
    return loot_found

def room_encounter(room_name):
    """
    Handles encounters in the specified room, including enemy fights, loot chests,
    or empty rooms. Manages whether the room has been looted or cleared of enemies.

    Args:
        room_name (str): The name of the room where the encounter takes place.

    Returns:
        tuple or None or bool: Returns loot found in the room (item, quantity) if any,
                               None if no loot or enemy is present,
                               or False if the player dies during combat.
    """

    if room_name in ['Cupboard', 'Bedroom Cupboard']:
        if room_name not in looted_rooms:
            return spawn_chest_and_loot(room_name)
        rprint("[grey66]This chest is empty.[/grey66]")
        return

    if room_name in ['West Wing', 'Dining Hall', 'Bedroom']:
        if room_name not in fought_rooms:
            if room_name == 'Bedroom' and random.choice(['enemy', 'empty']) == 'empty':
                rprint("[grey66]The room is empty.[/grey66]")
                return
            result = spawn_enemy_and_fight(room_name)
            if result is False:
                return False
        else:
            rprint("[grey66]This room is now empty.[/grey66]")
        return

    if room_name == 'Library':
        if room_name not in fought_rooms and room_name not in looted_rooms:
            encounter = random.choice(['enemy', 'chest', 'empty'])
            if encounter == 'enemy':
                result = spawn_enemy_and_fight(room_name)
                if result is False:
                    return False
            elif encounter == 'chest':
                return spawn_chest_and_loot(room_name)
            else:
                rprint("[grey66]The room is empty.[/grey66]")
        else:
            rprint("[grey66]The room is empty.[/grey66]")
        return

    if room_name == 'Galley':
        if room_name not in fought_rooms:
            enemies = random.sample([Goblin, Skeleton, Ratking], 2)
            for enemy_class in enemies:
                enemy = enemy_class()
                rprint(
                    f"[red]An enemy [{enemy.colour}]{enemy.name}[/{enemy.colour}] appears![/red]"
                )
                result = fight_enemy(player, enemy)
                if result == 'win':
                    drop = random_enemy()
                    add_to_inv(drop[0], drop[1])
                    collected_loot.append(drop)
                    rprint(f"[bright_green]The enemy dropped {drop[1]} x {drop[0]}![/bright_green]")
                elif result is False:
                    return False
            fought_rooms.add(room_name)
        else:
            rprint("[grey66]This room is now empty.[/grey66]")
        return


def end_game():
    """
    Handles the end-of-game sequence by displaying the player's collected loot
    and prompting to play again or exit.

    Returns:
        bool: True if the player chooses to play again, False otherwise.
    """

    rprint('\n[green]You have survived![/green]')
    if collected_loot:
        rprint('[green]You collected the following loot:[/green]')
        for item_name, quantity in collected_loot:
            rprint(f'- {quantity} x {item_name}')
    else:
        rprint("[dark_green]You didn't collect any loot.[/dark_green]")

    choice = Prompt.ask(
        '\nWould you like to [bold]play again?[/bold]',
        choices=['Yes', 'No'],
        default='No'
    ).capitalize()

    if choice == 'Yes':
        return True
    else:
        rprint('[red]Thank you for playing[/red]')
        return False



def game_loop():
    """
    Main game loop controlling player movement, room encounters, and game flow.

    The loop continues until the player reaches the 'Exit' room, chooses to quit,
    or dies in combat. It manages displaying rooms, handling encounters,
    showing inventory, and restarting the game if the player survives and opts to play again.
    """

    encounter_rooms = [
        'West Wing', 'Library', 'Dining Hall',
        'Bedroom', 'Galley', 'Cupboard', 'Bedroom Cupboard'
    ]

    current_room = 'Main Hall'
    while True:
        if current_room == 'Exit':
            if end_game():
                collected_loot.clear()
                current_room = 'Main Hall'
                continue
            else:
                break

        show_room(current_room)
        if current_room in encounter_rooms:
            result = room_encounter(current_room)
            if result is False:
                break

        move = Prompt.ask(
            'What direction do you wish to move? (or type Quit to exit, or Inventory to check)'
        ).capitalize()

        if move == 'Inventory':
            show_inv()
            continue
        if move == 'Quit':
            rprint('[red]Thank you for playing![/red]')
            break
        if move in rooms[current_room]['exits']:
            current_room = rooms[current_room]['exits'][move]
        else:
            rprint(f'[red]You cannot go {move}![/red]')

if __name__== '__main__':
    game_loop()

    # sort out the readme and notes
