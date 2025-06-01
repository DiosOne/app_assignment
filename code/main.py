import random
from rooms import rooms
from rich import print
from rich.panel import Panel
from rich.prompt import Prompt
from dice_rolls import dice_roll
from advent import Adventurer, Fighter, Mage, Ranger, show_stats
from enemies import Enemy, Goblin, Skeleton, Ratking, show_enemy_stats
from loot_table import chest_dict, enemy_drop, random_chest, random_enemy

current_room= 'Main Hall'

def show_room(room_name):
    room= rooms[room_name]
    exits= ', '.join(room['exits'].keys())
    print(Panel(
        f'[yellow]{room.get('display_name', room_name)}[/yellow]\n\n'
        f'{room['description']}\n\n'
        f'[grey]Exits:[/grey]{exits}',
        title='Room Info'
    ))

def game_loop():
    global current_room
    while True:
        show_room(current_room)
        move= Prompt.ask('What direction do you wish to move? (or type Quit to exit program)').capitalize()
        
        if move== 'Quit':
            print('[red]Thank you for playing![/red]')
            break
        
        if move in rooms[current_room]['exits']:
            current_room= rooms[current_room]['exits'][move]
            
        else:
            print(f'[red]You cannot go {move}![/red]')
            
if __name__== '__main__':
    game_loop()