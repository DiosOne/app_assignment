'''
Text Adventure Game - Main Entry Point

This module contains the main logic and game loop for a terminal-based text adventure.
Players can choose a character class, explore interconnected rooms, encounter enemies, 
find loot, and progress toward an exit.

Features:
- Class selection: Fighter, Mage, or Ranger.
- Random enemy encounters and enemy loot drops.
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
from enemies import BoneDevil, Ghost, Goblin, Minotaur, Ratking, Skeleton, Thug, Zombie
from loot_table import random_enemy, random_room_treasure
from attacks import fight_enemy
from inventory import add_to_inv, clear_inv, count_inv, remove_from_inv, show_inv


player= None
collected_loot= []
fought_rooms= set()
searched_rooms= set()
failed_search_rooms= set()
search_attempts= {}
searchable_rooms = [
    'Bedroom', 'Library', 'Scullery',
    'Guard Post', 'Servants Quarters', 'Dining Hall',
    'Armoury', 'Chapel', 'Observatory', 'Treasury'
]
rank_1_enemies = [Goblin, Skeleton, Ratking, Zombie]
rank_2_enemies = [Zombie, Thug, Ghost]
rank_3_enemies = [Thug, Ghost, BoneDevil, Minotaur]

encounter_table = {
    'Guard Post':{'enemy_count':(2, 5), 'enemy_classes':rank_1_enemies},
    'Main Hall':{'enemy_count':(2, 5), 'enemy_classes':rank_1_enemies},
    'Servants Quarters':{'enemy_count':(2, 5), 'enemy_classes':rank_1_enemies},

    'Bedroom':{'enemy_count':(3, 5), 'enemy_classes':rank_1_enemies + rank_2_enemies},
    'West Wing':{'enemy_count':(3, 5), 'enemy_classes':rank_1_enemies + rank_2_enemies},
    'Dining Hall':{'enemy_count':(3, 5), 'enemy_classes':rank_1_enemies + rank_2_enemies},
    'East Wing':{'enemy_count':(3, 5), 'enemy_classes':rank_1_enemies + rank_2_enemies},
    'Library':{'enemy_count':(3, 5), 'enemy_classes':rank_1_enemies + rank_2_enemies},

    'Armoury':{'enemy_count':(3, 6), 'enemy_classes':rank_2_enemies + rank_3_enemies},
    'Scullery':{'enemy_count':(3, 6), 'enemy_classes':rank_2_enemies + rank_3_enemies},
    'Chapel':{'enemy_count':(3, 6), 'enemy_classes':rank_2_enemies + rank_3_enemies},

    'Observatory':{'enemy_count':(3, 5), 'enemy_classes':rank_1_enemies + rank_3_enemies},
    'Treasury':{'enemy_count':(3, 5), 'enemy_classes':rank_1_enemies + rank_3_enemies}
}

direction_shortcuts = {
    'North':'N',
    'Northeast':'NE',
    'East':'E',
    'Southeast':'SE',
    'South':'S',
    'Southwest':'SW',
    'West':'W',
    'Northwest':'NW'
}

shortcut_directions = {shortcut:direction for direction, shortcut in direction_shortcuts.items()}

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

def start_new_run():
    '''
    Resets run state and starts the player at the entrance hall.

    :return: Starting room name for the new run.
    :rtype: str
    '''

    global player

    collected_loot.clear()
    fought_rooms.clear()
    searched_rooms.clear()
    failed_search_rooms.clear()
    search_attempts.clear()
    clear_inv()
    add_to_inv('Small Health Potion', 2)

    player= choose_player_class()
    rprint(f"[bold yellow]You have chosen the[/bold yellow] "
           f"[{player.colour}]{player.__class__.__name__}[/{player.colour}]")
    show_stats(player)
    return 'Entrance Hall'


def show_room(room_name):
    '''
    Displays the current room's name, description, and available exits using a styled panel.

    :param room_name: The key name of the room to display from the rooms dictionary.
    :type room_name: str
    '''
    room= rooms[room_name]
    exits= ', '.join(
        f'{direction}({direction_shortcuts.get(direction, direction)})'
        for direction in room['exits'].keys()
    )
    search_hint = ''
    if room_name not in searched_rooms and room_name in searchable_rooms:
        search_hint = '\n\n[grey66]Maybe you should look around this room.[/grey66]'
    rprint(Panel(
        f'[bright_blue]{room.get("display_name", room_name)}[/bright_blue]\n\n'
        f'{room["description"]}{search_hint}\n\n'
        f'[grey66]Exits:[/grey66]{exits}',
        title='Room Info'
    ))

def normalize_move(move):
    '''
    Converts full direction names and direction shortcuts into room exit keys.

    :param move: Player movement input.
    :type move: str
    :return: Normalized movement command.
    :rtype: str
    '''

    move = move.strip()
    if move.lower() in ['inventory', 'inv']:
        return 'Inventory'
    if move.lower() in ['look', 'l']:
        return 'Look'
    if move.lower() in ['look around', 'look again', 'search']:
        return 'Search'
    if move.lower() in ['use', 'use item']:
        return 'Use'
    if move.lower() == 'quit':
        return 'Quit'

    direction = move.capitalize()
    shortcut = move.upper()
    return shortcut_directions.get(shortcut, direction)

def add_loot(drops, source):
    '''
    Adds loot drops to the player's inventory and collected loot list.

    :param drops: Item and quantity tuples to add.
    :type drops: list[tuple(str, int)]
    :param source: Description of where the loot came from.
    :type source: str
    '''

    if not drops:
        rprint(f'[grey66]You find nothing useful {source}.[/grey66]')
        return

    for item_name, quantity in drops:
        add_to_inv(item_name, quantity)
        collected_loot.append((item_name, quantity))
        rprint(f"[bright_green]You found {quantity} x {item_name} {source}![/bright_green]")

def search_room(room_name):
    '''
    Searches a room for treasure.

    :param room_name: The room being searched.
    :type room_name: str
    '''

    fail_rolls = [1, 2, 3, 11, 12, 13]
    failure_messages = {
        1:'Hmm strange, maybe have a better look?',
        2:"It definetly feels like I'm missing something here...",
        3:'Whelp, guess its really empty'
    }

    if room_name not in searchable_rooms:
        rprint('[grey66]There does not seem to be anything hidden here.[/grey66]')
        return

    if room_name in searched_rooms:
        rprint('[grey66]You have already found everything useful here.[/grey66]')
        return

    attempts = search_attempts.get(room_name, 0)
    if attempts >= 3:
        rprint('[grey66]Whelp, guess its really empty[/grey66]')
        return

    search_roll = random.randint(1, 20)
    if search_roll in fail_rolls:
        attempts += 1
        search_attempts[room_name] = attempts
        failed_search_rooms.add(room_name)
        if attempts >= 3:
            searched_rooms.add(room_name)
            failed_search_rooms.discard(room_name)
        rprint(f'[grey66]{failure_messages[attempts]}[/grey66]')
        return

    drops = random_room_treasure(room_name)
    searched_rooms.add(room_name)
    failed_search_rooms.discard(room_name)
    rprint('[bright_green]You found a hidden treasure chest![/bright_green]')
    add_loot(drops, f'while searching {room_name}')

def use_item():
    '''
    Lets the player use a health potion from their inventory.
    '''

    current_player = player
    if current_player is None:
        rprint('[red]No player has been created yet.[/red]')
        return

    potion_healing = {
        'Small Health Potion':15,
        'Medium Health Potion':30,
        'Large Health Potion':50
    }
    counted = count_inv()
    potions = [item for item in potion_healing if counted.get(item, 0) > 0]

    if not potions:
        rprint('[grey66]You do not have any usable items.[/grey66]')
        return

    rprint('[bold]Choose an item to use:[/bold]')
    for index, potion in enumerate(potions, start=1):
        rprint(f'{index}. {potion} x {counted[potion]}')

    choice = input('Item number or name: ').strip().lower()
    selected_item = None
    if choice.isdigit():
        item_index = int(choice) - 1
        if 0 <= item_index < len(potions):
            selected_item = potions[item_index]
    else:
        for potion in potions:
            if choice == potion.lower():
                selected_item = potion

    if selected_item is None:
        rprint('[red]Invalid item choice.[/red]')
        return

    if current_player.health >= current_player.max_health:
        rprint('[grey66]You are already at full health.[/grey66]')
        return

    remove_from_inv(selected_item)
    healing = potion_healing[selected_item]
    old_health = current_player.health
    current_player.health = min(current_player.max_health, current_player.health + healing)
    rprint(
        f'[bright_green]You use a {selected_item} and recover '
        f'{current_player.health - old_health} hit points.[/bright_green]'
    )
    rprint(
        f'[cyan]Your Health: [{current_player.colour}]{current_player.health}'
        f'[/{current_player.colour}]/{current_player.max_health}[/cyan]'
    )

def spawn_enemy_and_fight(room_name, enemy_classes):
    """
    Spawns a random enemy and initiates combat. If the player wins, they receive loot.

    Args:
        room_name (str): The name of the room where the encounter is happening.

    Returns:
        str or bool: Returns 'win' if the enemy is defeated,
                     False if the player dies or flees,
                     or None if no combat occurs.
    """

    current_player = player
    if current_player is None:
        rprint('[red]No player has been created yet.[/red]')
        return False

    enemy_class = random.choice(enemy_classes)
    enemy = enemy_class()
    rprint(f"[red]An enemy [{enemy.colour}]{enemy.name}[/{enemy.colour}] appears![/red]")
    result = fight_enemy(current_player, enemy)
    if result == 'win':
        drops = random_enemy(enemy.name)
        add_loot(drops, f'from the {enemy.name}')
    return result

def spawn_enemies_and_fight(room_name):
    """
    Spawns the room's enemy group and fights each enemy one at a time.
    Marks the room as fought after every enemy in the room has been defeated.

    Args:
        room_name (str): The name of the room where the encounter is happening.

    Returns:
        str or bool or None: Returns 'win' if all enemies are defeated,
                             'quit' if the player flees,
                             False if the player dies,
                             or None if the room was already cleared.
    """

    encounter = encounter_table[room_name]
    min_enemies, max_enemies = encounter['enemy_count']
    enemy_count = random.randint(min_enemies, max_enemies)

    rprint(f"[red]You hear {enemy_count} enemies nearby![/red]")
    for _ in range(enemy_count):
        result = spawn_enemy_and_fight(room_name, encounter['enemy_classes'])
        if result != 'win':
            return result

    fought_rooms.add(room_name)
    return 'win'

def room_encounter(room_name):
    """
    Handles encounters in the specified room, including enemy fights or empty rooms.
    Manages whether the room has been cleared of enemies.

    Args:
        room_name (str): The name of the room where the encounter takes place.

    Returns:
        None or bool: Returns None if no enemy is present,
                      or False if the player dies during combat.
    """

    if room_name in encounter_table:
        if room_name not in fought_rooms:
            result = spawn_enemies_and_fight(room_name)
            if result is not None:
                return result
        else:
            rprint("[grey66]This room is now empty.[/grey66]")
        return

def ask_play_again():
    '''
    Prompts the player to start a new run.

    :return: True if the player wants to play again, otherwise False.
    :rtype: bool
    '''

    while True:
        choice = input('\nWould you like to play again? [Yes/No] (No): ').strip().lower()
        if choice in ['', 'n', 'no']:
            return False
        if choice in ['y', 'yes']:
            return True
        rprint('[red]Please enter Yes or No.[/red]')


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

    if ask_play_again():
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

    encounter_rooms = list(encounter_table.keys())

    current_room = start_new_run()
    while True:
        if current_room == 'Exit':
            if end_game():
                current_room = start_new_run()
                continue
            else:
                break

        show_room(current_room)
        if current_room in encounter_rooms:
            result = room_encounter(current_room)
            if result is False:
                break
            if result is True:
                current_room = start_new_run()
                continue
            if result == 'win':
                show_room(current_room)

        search_command = 'Look Again' if current_room in failed_search_rooms else 'Look Around'
        move = Prompt.ask(
            f'What direction do you wish to move? '
            f'(or type Look, {search_command}, Use, Quit, Inventory, or Inv)'
        )
        move = normalize_move(move)

        if move == 'Inventory':
            show_inv(player)
            continue
        if move == 'Look':
            show_room(current_room)
            continue
        if move == 'Search':
            search_room(current_room)
            continue
        if move == 'Use':
            use_item()
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
    
