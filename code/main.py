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

def choose_player_class():
    '''
    Prompts the player to choose a character class.

    Offers a choice between Fighter, Mage, or Ranger. Repeats the prompt 
    until a valid class is selected, then returns an instance of the chosen class.

    :return: An instance of the selected player class.
    :rtype: Fighter | Mage | Ranger
    '''
    rprint('Choose your class: [bold red]Fighter[/bold red], [bold purple]Mage[/bold purple], [bold green]Ranger[/bold green]')
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
rprint(f"[bold yellow]You have chosen the[/bold yellow] [{player.colour}]{player.__class__.__name__}[/{player.colour}]")
show_stats(player)


looted_rooms= set()
fought_rooms= set()


def show_room(room_name):
    '''
    Displays the current room's name, description, and available exits using a styled panel.

    :param room_name: The key name of the room to display from the rooms dictionary.
    :type room_name: str
    '''
    room= rooms[room_name]
    exits= ', '.join(room['exits'].keys())
    rprint(Panel(
        f'[blue]{room.get("display_name", room_name)}[/blue]\n\n'
        f'{room['description']}\n\n'
        f'[grey66]Exits:[/grey66]{exits}',
        title='Room Info'
    ))

def room_encounter(room_name):
    '''
    Handles encounters in specific rooms, including finding loot, fighting enemies,
    or encountering empty areas. Room behavior varies depending on type and 
    whether it's been previously looted or cleared.

    :param room_name: The name of the current room where an encounter might occur.
    :type room_name: str
    :return: Loot found in the room (if any), or False if the player dies during combat.
    :rtype: tuple or None or bool
    '''

    encounter_text= ''
    loot_found= None
    enemies= [Goblin, Skeleton, Ratking]

    if room_name in ['Cupboard', 'Bedroom Cupboard']:
        if room_name not in looted_rooms:
            loot_found= random_chest()
            add_to_inv(loot_found[0], loot_found[1])
            collected_loot.append(loot_found)
            encounter_text= f'[yellow] You found {loot_found[1]} x {loot_found[0]} in a chest![/yellow]'
            rprint(encounter_text)
            looted_rooms.add(room_name)
        else:
            rprint('[grey66]This chest is empty.[/grey66]')
        return

    if room_name== 'West Wing':
        if room_name not in fought_rooms:
            enemy_class= random.choice(enemies)
            enemy= enemy_class()
            encounter_text= f'[red]An enemy [{enemy.colour}]{enemy.name}[/{enemy.colour}] appears![/red]'
            rprint(encounter_text)
            result= fight_enemy(player, enemy)
            if result== 'win':
                drop= random_enemy()
                add_to_inv(drop[0],drop[1])
                collected_loot.append(drop)
                rprint(f'[bright_green]The enemy dropped {drop[1]} x {drop[0]}![/bright_green]')
                fought_rooms.add(room_name)
            elif result is False:
                return False
        else:
            rprint('[grey66]This room is now empty.[/grey66]')

    elif room_name== 'Library':
        if room_name not in fought_rooms and room_name not in looted_rooms:
            choice= random.choice(['enemy', 'chest', 'empty'])
            if choice== 'enemy':
                enemy_class= random.choice(enemies)
                enemy= enemy_class()
                encounter_text= f'[red]An enemy [{enemy.colour}]{enemy.name}[/{enemy.colour}] appears![/red]'
                rprint(encounter_text)
                result= fight_enemy(player, enemy)
                if result== 'win':
                    drop= random_enemy()
                    add_to_inv(drop[0],drop[1])
                    collected_loot.append(drop)
                    rprint(f'[bright_green]The enemy dropped {drop[1]} x {drop[0]}![/bright_green]')
                    fought_rooms.add(room_name)
                elif result is False:
                    return False
            elif choice== 'chest':
                loot_found= random_chest()
                add_to_inv(loot_found[0], loot_found[1])
                collected_loot.append(loot_found)
                encounter_text= f'[yellow] You found {loot_found[1]} x {loot_found[0]} in a chest![/yellow]'
                rprint(encounter_text)
                looted_rooms.add(room_name)
        else:
            encounter_text= '[grey66]The room is empty.[/grey66]'

    elif room_name== 'Dining Hall':
        if room_name not in fought_rooms:
            enemy_class= random.choice(enemies)
            enemy= enemy_class()
            encounter_text= f'[red]An enemy [{enemy.colour}]{enemy.name}[/{enemy.colour}] appears![/red]'
            rprint(encounter_text)
            result= fight_enemy(player, enemy)
            if result== 'win':
                drop= random_enemy()
                add_to_inv(drop[0],drop[1])
                collected_loot.append(drop)
                rprint(f'[bright_green]The enemy dropped {drop[1]} x {drop[0]}![/bright_green]')
                fought_rooms.add(room_name)
            elif result is False:
                return False

    elif room_name== 'Bedroom':
        if room_name not in fought_rooms:
            choice= random.choice(['enemy', 'empty'])
            if choice== 'enemy':
                enemy_class= random.choice(enemies)
                enemy= enemy_class()
                encounter_text= f'[red]An enemy [{enemy.colour}]{enemy.name}[/{enemy.colour}] appears![/red]'
                rprint(encounter_text)
                result= fight_enemy(player, enemy)
                if result== 'win':
                    drop= random_enemy()
                    add_to_inv(drop[0],drop[1])
                    collected_loot.append(drop)
                    rprint(f'[bright_green]The enemy dropped {drop[1]} x {drop[0]}![/bright_green]')
                    fought_rooms.add(room_name)
                elif result is False:
                    return False
            else:
                encounter_text= '[grey66]The room is empty.[/grey66]'
                rprint(encounter_text)

    elif room_name== 'Galley':
        if room_name not in fought_rooms:
            enemy_classes= random.sample(enemies, 2)
            enemies_to_fight= []
            encounter_text= ''
            for enemy_class in enemy_classes:
                enemy= enemy_class()
                enemies_to_fight.append(enemy)
                encounter_text+= f'[red]An enemy [{enemy.colour}]{enemy.name}[/{enemy.colour}] appears![/red]\n'

            rprint(encounter_text.strip())
            for enemy in enemies_to_fight:
                result= fight_enemy(player, enemy)
                if result== 'win':
                    drop= random_enemy()
                    add_to_inv(drop[0],drop[1])
                    collected_loot.append(drop)
                    rprint(f'[bright_green]The enemy dropped {drop[1]} x {drop[0]}![/bright_green]')
                    fought_rooms.add(room_name)
                elif result is False:
                    return False

    return loot_found


def end_game():
    '''
    Handles the end-of-game sequence. Displays a summary of the player's collected loot
    and prompts them to play again or exit. Clears collected loot if the player chooses to replay.

    :return: True if the player wants to play again, False otherwise.
    :rtype: bool
    '''

    rprint('\n[green]You have survived![/green]')
    # rprint('[green]You collected {collected_loot}[/green]')

    if collected_loot:
        rprint('[green]You collected the following loot:[/green]')
        for item_name, quantity in collected_loot:
            rprint(f'- {quantity} x {item_name}')
    else:
        rprint('[dark green]You didn\'t collect any loot.[/dark green]')


    choice= Prompt.ask('\nWould you like to [bold]play again?[/bold]', choices=['Yes', 'No'], default='No').capitalize()
    if choice== 'Yes':
        return True

    else:
        rprint('[red]Thank you for playing[/red]')
        return False


def game_loop():
    '''
    The main game loop that controls the player's movement, room exploration,
    and encounter handling. Continues until the player either reaches the Exit,
    chooses to quit, or dies. Handles inventory viewing and restarting the game
    if the player survives and opts to play again.
    '''


    encounter_rooms= ['West Wing', 'Library', 'Dining Hall', 'Bedroom', 'Galley', 'Cupboard', 'Bedroom Cupboard']
    current_room= 'Main Hall'
    while True:
        if current_room== 'Exit':
            if end_game():
                collected_loot.clear()
                current_room= 'Main Hall'
                continue
            else:
                break


        show_room(current_room)
        if current_room in encounter_rooms:
            result = room_encounter(current_room)
            if result is False:
                break
        move= Prompt.ask('What direction do you wish to move? (or type Quit to exit, or Inventory to check)').capitalize()

        if move== 'Inventory':
            show_inv()
            continue

        if move== 'Quit':
            rprint('[red]Thank you for playing![/red]')
            break

        if move in rooms[current_room]['exits']:
            current_room= rooms[current_room]['exits'][move]

        else:
            rprint(f'[red]You cannot go {move}![/red]')

if __name__== '__main__':
    game_loop()

    # sort out the readme and notes
    # docstrings
