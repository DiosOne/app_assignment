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
from rich.align import Align
from rich.panel import Panel
from rich.prompt import Prompt
from advent import Fighter, Mage, Ranger, show_stats
from enemies import BoneDevil, Ghost, Goblin, Minotaur, Ratking, Skeleton, Thug, Zombie
from loot_table import random_enemy, random_room_treasure
from attacks import combat_separator, fight_enemy
from inventory import (
    add_to_inv, can_carry, clear_inv, count_inv, current_weight,
    drop_item, item_weight, max_carry_weight, remove_from_inv, show_inv
)


player= None
run_count= 1
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
    'Guard Post':{'enemy_count':(2, 3), 'enemy_classes':rank_1_enemies},
    'Main Hall':{'enemy_count':(2, 3), 'enemy_classes':rank_1_enemies},
    'Servants Quarters':{'enemy_count':(2, 3), 'enemy_classes':rank_1_enemies},

    'Bedroom':{'enemy_count':(2, 3), 'enemy_classes':rank_1_enemies + rank_2_enemies},
    'West Wing':{'enemy_count':(2, 3), 'enemy_classes':rank_1_enemies + rank_2_enemies},
    'Dining Hall':{'enemy_count':(2, 4), 'enemy_classes':rank_1_enemies + rank_2_enemies},
    'East Wing':{'enemy_count':(2, 3), 'enemy_classes':rank_1_enemies + rank_2_enemies},
    'Library':{'enemy_count':(2, 3), 'enemy_classes':rank_1_enemies + rank_2_enemies},

    'Armoury':{'enemy_count':(2, 4), 'enemy_classes':rank_2_enemies + rank_3_enemies},
    'Scullery':{'enemy_count':(2, 4), 'enemy_classes':rank_2_enemies + rank_3_enemies},
    'Chapel':{'enemy_count':(2, 3), 'enemy_classes':rank_2_enemies + rank_3_enemies},

    'Observatory':{'enemy_count':(2, 3), 'enemy_classes':rank_1_enemies + rank_3_enemies},
    'Treasury':{'enemy_count':(2, 3), 'enemy_classes':rank_1_enemies + rank_3_enemies}
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

shop_attack_unlocks = {
    'Greatsword':{'class':'Fighter', 'attack':{'name':'Greatsword', 'hit_bonus':5, 'damage':'2d6+3'}},
    'Battleaxe':{'class':'Fighter', 'attack':{'name':'Battleaxe', 'hit_bonus':5, 'damage':'1d10+3'}},
    'Warhammer':{'class':'Fighter', 'attack':{'name':'Warhammer', 'hit_bonus':5, 'damage':'1d8+3'}},
    'Halberd':{'class':'Fighter', 'attack':{'name':'Halberd', 'hit_bonus':4, 'damage':'1d10+2'}},
    'Handaxe':{'class':'Fighter', 'attack':{'name':'Handaxe', 'hit_bonus':5, 'damage':'1d6+3'}},

    'Twin Daggers':{'class':'Ranger', 'attack':{'name':'Twin Daggers', 'hit_bonus':5, 'damage':'1d4+2', 'times':2}},
    'Rapier':{'class':'Ranger', 'attack':{'name':'Rapier', 'hit_bonus':5, 'damage':'1d8+2'}},
    'Hunter Bow':{'class':'Ranger', 'attack':{'name':'Hunter Bow', 'hit_bonus':5, 'damage':'1d8+3'}},
    'Crossbow':{'class':'Ranger', 'attack':{'name':'Crossbow', 'hit_bonus':4, 'damage':'1d10+2'}},
    'Poison Arrow':{'class':'Ranger', 'attack':{'name':'Poison Arrow', 'hit_bonus':4, 'damage':'1d8+1+1d6'}},

    'Spell Scroll: Ice Knife':{'class':'Mage', 'attack':{'name':'Ice Knife', 'hit_bonus':5, 'damage':'1d10+1d6'}},
    'Spell Scroll: Magic Missile':{'class':'Mage', 'attack':{'name':'Magic Missile', 'hit_bonus':99, 'damage':'1d4+1', 'times':3}},
    'Spell Scroll: Lightning Bolt':{'class':'Mage', 'attack':{'name':'Lightning Bolt', 'hit_bonus':6, 'damage':'3d8'}},
    'Spell Scroll: Acid Arrow':{'class':'Mage', 'attack':{'name':'Acid Arrow', 'hit_bonus':5, 'damage':'2d6+1d4'}},
    'Spell Scroll: Flame Lance':{'class':'Mage', 'attack':{'name':'Flame Lance', 'hit_bonus':6, 'damage':'2d10'}}
}

def show_title_screen():
    '''
    Displays the game title screen and character choices.
    '''

    rprint(Panel(
        Align.center(
        '[bold underline]..The Dungeon..[/bold underline]\n\n'
        'Choose Your Character\n\n'
        '[bold bright_red]1. Fighter[/bold bright_red]\n'
        '[bold purple]2. Mage[/bold purple]\n'
        '[bold green]3. Ranger[/bold green]'
        )
    ))

def choose_player_class():
    '''
    Prompts the player to choose a character class.

    Offers a choice between Fighter, Mage, or Ranger. Repeats the prompt 
    until a valid class is selected, then returns an instance of the chosen class.

    :return: An instance of the selected player class.
    :rtype: Fighter | Mage | Ranger
    '''
    show_title_screen()
    while True:
        choice= input('Class: ').strip().lower()
        if choice in ['1', 'fighter']:
            return Fighter()
        elif choice in ['2', 'mage']:
            return Mage()
        elif choice in ['3', 'ranger']:
            return Ranger()
        else:
            rprint('Invalid class, try again')

def apply_shop_attacks(character):
    '''
    Adds store-bought attacks to the selected character if their class can use them.

    :param character: The selected player character.
    :type character: Adventurer or subclass instance.
    '''

    counted = count_inv()
    class_name = character.__class__.__name__
    known_attacks = [attack['name'] for attack in character.attacks]
    for item_name, unlock in shop_attack_unlocks.items():
        if counted.get(item_name, 0) and unlock['class'] == class_name:
            attack = unlock['attack']
            if attack['name'] not in known_attacks:
                character.attacks.append(attack)
                known_attacks.append(attack['name'])
                rprint(f'[bright_green]{item_name} unlocks {attack["name"]}.[/bright_green]')

def start_new_run(keep_inventory=False):
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
    if not keep_inventory:
        clear_inv()
        add_to_inv('Small Health Potion', 2)

    player= choose_player_class()
    apply_shop_attacks(player)
    rprint(f"[bold yellow]You have chosen the[/bold yellow] "
           f"[{player.colour}]{player.__class__.__name__}[/{player.colour}]")
    show_stats(player)
    return 'Entrance Hall'

def enemy_count_for_room(room_name):
    '''
    Gets the scaled enemy count for the room based on completed runs.

    :param room_name: Name of the encounter room.
    :type room_name: str
    :return: Random enemy count for this room.
    :rtype: int
    '''

    encounter = encounter_table[room_name]
    min_enemies, max_enemies = encounter['enemy_count']
    scaling_bonus = min(run_count - 1, 5)
    return random.randint(min_enemies + scaling_bonus, max_enemies + scaling_bonus)


def show_room(room_name, show_exit_rooms=False):
    '''
    Displays the current room's name, description, and available exits using a styled panel.

    :param room_name: The key name of the room to display from the rooms dictionary.
    :type room_name: str
    '''
    room= rooms[room_name]
    exits = format_exits(room_name, show_exit_rooms)
    search_hint = ''
    if room_name in searched_rooms:
        search_hint = '\n\n[grey66]This room is now empty.[/grey66]'
    elif room_name in searchable_rooms:
        attempts = search_attempts.get(room_name, 0)
        if attempts == 1:
            search_hint = '\n\n[grey66]Hmm strange, maybe have a better look?[/grey66]'
        elif attempts == 2:
            search_hint = "\n\n[grey66]It definetly feels like I'm missing something here...[/grey66]"
        else:
            search_hint = '\n\n[grey66]Maybe you should look around this room.[/grey66]'
    elif room_name in fought_rooms:
        search_hint = '\n\n[grey66]This room is now empty.[/grey66]'
    rprint(Panel(
        f'[bright_blue]{room.get("display_name", room_name)}[/bright_blue]\n\n'
        f'{room["description"]}{search_hint}\n\n'
        f'[grey66]Exits: [/grey66]{exits}',
        title='Room Info'
    ))

def format_exits(room_name, show_exit_rooms=False):
    '''
    Formats exits for room display.

    :param room_name: Room whose exits are being displayed.
    :type room_name: str
    :param show_exit_rooms: Whether to include destination room names.
    :type show_exit_rooms: bool
    :return: Formatted exit list.
    :rtype: str
    '''

    exit_labels = []
    for index, (direction, destination) in enumerate(rooms[room_name]['exits'].items(), start=1):
        exit_label = f'{index}. {format_direction(direction)}'
        if show_exit_rooms:
            exit_label = f'{exit_label} - {destination}'
        exit_labels.append(exit_label)
    return ', '.join(exit_labels)

def format_direction(direction):
    '''
    Formats a direction as its movement shortcut.

    :param direction: Full direction name.
    :type direction: str
    :return: Formatted direction label.
    :rtype: str
    '''

    shortcut = direction_shortcuts.get(direction)
    if shortcut is None:
        return direction
    return f'({shortcut})'

def numbered_exits(room_name):
    '''
    Maps displayed exit numbers to room exit directions.

    :param room_name: Current room name.
    :type room_name: str
    :return: Number-to-direction mapping.
    :rtype: dict
    '''

    return {
        str(index):direction
        for index, direction in enumerate(rooms[room_name]['exits'].keys(), start=1)
    }

def normalize_move(move, room_name):
    '''
    Converts full direction names and direction shortcuts into room exit keys.

    :param move: Player movement input.
    :type move: str
    :param room_name: Current room name.
    :type room_name: str
    :return: Normalized movement command.
    :rtype: str
    '''

    move = move.strip()
    if move in numbered_exits(room_name):
        return numbered_exits(room_name)[move]

    if move.lower() in ['inventory', 'inv', 'i']:
        return 'Inventory'
    if move.lower() in ['look', 'l']:
        return 'Look'
    if move.lower() in ['look around', 'look again', 'search', 's']:
        return 'Search'
    if move.lower() in ['use', 'use item', 'u']:
        return 'Use'
    if move.lower() in ['drop', 'drop item', 'd']:
        return 'Drop'
    if move.lower() in ['quit', 'q']:
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
        accepted = 0
        remaining = quantity
        while remaining > 0:
            if can_carry(item_name):
                add_to_inv(item_name)
                collected_loot.append((item_name, 1))
                accepted += 1
                remaining -= 1
            else:
                rprint(
                    f'[yellow]You cannot carry all of the {item_name}; '
                    f'carry weight is {current_weight()}/{max_carry_weight}.[/yellow]'
                )
                rprint('[grey66]Try dropping Junk or other low-value items.[/grey66]')
                choice = input('Drop items now before leaving loot behind? [y/N]: ').strip().lower()
                if choice in ['y', 'yes']:
                    drop_inventory_item()
                    continue
                break
        if accepted:
            if source.startswith('from the '):
                rprint(f'[bright_green]You recieved {accepted} x {item_name}.[/bright_green]')
            else:
                rprint(f"[bright_green]You found {accepted} x {item_name} {source}![/bright_green]")
        if remaining:
            rprint(
                f'[yellow]You leave {remaining} x {item_name}; '
                f'carry weight is {current_weight()}/{max_carry_weight}.[/yellow]'
            )

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

def drop_inventory_item():
    '''
    Lets the player drop unwanted inventory items.
    '''

    counted = count_inv()
    if not counted:
        rprint('[grey66]Your inventory is empty.[/grey66]')
        return

    items = list(counted.keys())
    rprint('[bold]Choose an item to drop:[/bold]')
    for index, item in enumerate(items, start=1):
        rprint(f'{index}. {item} x {counted[item]} ({item_weight(item)} weight each)')

    choice = input('Item number or name: ').strip().lower()
    selected_item = None
    if choice.isdigit():
        item_index = int(choice) - 1
        if 0 <= item_index < len(items):
            selected_item = items[item_index]
    else:
        for item in items:
            if choice == item.lower():
                selected_item = item

    if selected_item is None:
        rprint('[red]Invalid item choice.[/red]')
        return

    quantity_choice = input(f'How many {selected_item} do you want to drop? ').strip()
    if quantity_choice.isdigit():
        quantity = int(quantity_choice)
    else:
        quantity = 1

    dropped = drop_item(selected_item, quantity)
    if dropped:
        rprint(f'[yellow]You dropped {dropped} x {selected_item}.[/yellow]')
        rprint(f'[cyan]Carry Weight: {current_weight()}/{max_carry_weight}[/cyan]')
    else:
        rprint('[red]You do not have that item.[/red]')

def combat_result_status(result):
    '''
    Gets the status value from a combat result.
    '''

    if isinstance(result, dict):
        return result.get('status')
    return result

def remaining_attack_from_result(result):
    '''
    Gets unused attack data from a combat result.
    '''

    if isinstance(result, dict):
        return result.get('remaining_attack')
    return None

def attack_name_plural(attack):
    '''
    Gets a readable plural name for a carried-over attack.
    '''

    attack_name = attack['name']
    if attack_name.endswith('s'):
        return attack_name
    return f'{attack_name}s'

def spawn_enemy_and_fight(room_name, enemy_classes, pending_attack=None):
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
    opening_attack = None
    if pending_attack is not None:
        choice = input(
            f'Attack with remaining {attack_name_plural(pending_attack["attack"])}? [y/n]: '
        ).strip().lower()
        if choice in ['y', 'yes']:
            opening_attack = pending_attack
    combat_separator()
    result = fight_enemy(current_player, enemy, opening_attack)
    if combat_result_status(result) == 'win':
        drops = random_enemy(enemy.name)
        add_loot(drops, f'from the {enemy.name}')
        combat_separator()
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
    enemy_count = enemy_count_for_room(room_name)

    rprint(f"[red]You hear {enemy_count} enemies nearby![/red]\n")
    pending_attack = None
    for _ in range(enemy_count):
        result = spawn_enemy_and_fight(room_name, encounter['enemy_classes'], pending_attack)
        if combat_result_status(result) != 'win':
            return result
        pending_attack = remaining_attack_from_result(result)

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

def convert_gems_to_gold():
    '''
    Converts gems in the inventory into gold.
    '''

    gem_values = {
        'Garnet':15,
        'Ruby':30,
        'Rubies':30,
        'Emerald':50,
        'Emeralds':50,
        'Diamond':100,
        'Diamonds':100
    }
    counted = count_inv()
    total_gold = 0
    for gem, value in gem_values.items():
        quantity = counted.get(gem, 0)
        for _ in range(quantity):
            drop_item(gem)
            if can_carry('Gold', value):
                add_to_inv('Gold', value)
                total_gold += value
            else:
                add_to_inv(gem)
                rprint(f'[yellow]You cannot carry the Gold value of your {gem}.[/yellow]')

    if total_gold:
        rprint(f'[bright_green]You exchange your gems for {total_gold} Gold.[/bright_green]')
    else:
        rprint('[grey66]You do not have any gems to exchange.[/grey66]')

def spend_gold(amount):
    '''
    Removes gold from the inventory if the player has enough.
    '''

    counted = count_inv()
    if counted.get('Gold', 0) < amount:
        return False
    drop_item('Gold', amount)
    return True

def store():
    '''
    Lets the player buy useful items between successful runs.
    '''

    store_items = {
        '1':('Small Health Potion', 30),
        '2':('Medium Health Potion', 75),
        '3':('Large Health Potion', 140),
        '4':('Sharp Dagger', 120),
        '5':('Shortsword', 180),
        '6':('Greatsword', 260),
        '7':('Battleaxe', 240),
        '8':('Warhammer', 220),
        '9':('Halberd', 220),
        '10':('Handaxe', 120),
        '11':('Twin Daggers', 170),
        '12':('Rapier', 190),
        '13':('Hunter Bow', 230),
        '14':('Crossbow', 210),
        '15':('Poison Arrow', 80),
        '16':('Spell Scroll: Ice Knife', 180),
        '17':('Spell Scroll: Magic Missile', 220),
        '18':('Spell Scroll: Lightning Bolt', 300),
        '19':('Spell Scroll: Acid Arrow', 200),
        '20':('Spell Scroll: Flame Lance', 280)
    }

    rprint('[bold yellow]The dungeon trader opens their pack.[/bold yellow]')
    while True:
        counted = count_inv()
        rprint(f'[cyan]Gold: {counted.get("Gold", 0)} | Carry Weight: {current_weight()}/{max_carry_weight}[/cyan]')
        for item_number, (item_name, price) in store_items.items():
            rprint(f'{item_number}. {item_name} - {price} Gold')
        choice = input('Buy item number, Exchange gems, or Leave: ').strip().lower()

        if choice in ['leave', 'l', '']:
            return
        if choice in ['exchange', 'exchange gems', 'gems']:
            convert_gems_to_gold()
            continue
        if choice not in store_items:
            rprint('[red]Invalid store choice.[/red]')
            continue

        item_name, price = store_items[choice]
        if not can_carry(item_name):
            rprint('[red]You cannot carry that item.[/red]')
            continue
        if not spend_gold(price):
            rprint('[red]You do not have enough Gold.[/red]')
            continue
        add_to_inv(item_name)
        rprint(f'[bright_green]You bought 1 x {item_name}.[/bright_green]')


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
        counted_loot= {}
        for item_name, quantity in collected_loot:
            counted_loot[item_name]= counted_loot.get(item_name, 0) + quantity
        for item_name, quantity in counted_loot.items():
            rprint(f'- {quantity} x {item_name}')
    else:
        rprint("[dark_green]You didn't collect any loot.[/dark_green]")

    play_again = ask_play_again()
    if play_again:
        store()
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

    global run_count

    current_room = start_new_run()
    show_current_room = True
    while True:
        if current_room == 'Exit':
            if end_game():
                run_count += 1
                current_room = start_new_run(keep_inventory=True)
                show_current_room = True
                continue
            else:
                break

        if show_current_room:
            show_room(current_room)
        else:
            show_current_room = True

        if current_room in encounter_rooms and current_room not in fought_rooms:
            result = room_encounter(current_room)
            if result is False:
                break
            if result is True:
                current_room = start_new_run()
                show_current_room = True
                continue
            if result == 'win':
                show_room(current_room)

        move = Prompt.ask(
            f'What would you like to do? Choose a direction, or type "look" for more info, '
            f'"search" to search the room, "inv" to check inventory, "use" for potions, '
            f'or "quit" to quit the game'
        )
        move = normalize_move(move, current_room)

        if move == 'Inventory':
            show_inv(player)
            continue
        if move == 'Look':
            show_room(current_room, show_exit_rooms=True)
            show_current_room = False
            continue
        if move == 'Search':
            search_room(current_room)
            continue
        if move == 'Use':
            use_item()
            continue
        if move == 'Drop':
            drop_inventory_item()
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
    
