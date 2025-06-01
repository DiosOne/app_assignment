import random
from rooms import rooms
from rich import print
from rich.panel import Panel
from rich.prompt import Prompt
from dice_rolls import dice_roll
from advent import Adventurer, Fighter, Mage, Ranger, show_stats
from enemies import Enemy, Goblin, Skeleton, Ratking, show_enemy_stats
from loot_table import chest_dict, enemy_drop, random_chest, random_enemy

def choose_player_class():
    print('Choose your class: [bold red]Fighter[/bold red], [bold purple]Mage[/bold purple], [bold green]Ranger[/bold green]')
    while True:
        choice= input('Class: ').capitalize()
        if choice== 'Fighter':
            return Fighter()
        elif choice== 'Mage':
            return Mage()
        elif choice== 'Ranger':
            return Ranger()
        else:
            print('Invalid class, try again')
player= choose_player_class()
print(f"[bold yellow]You have chosen the[/bold yellow] [{player.colour}]{player.__class__.__name__}[/{player.colour}]")
show_stats(player)


current_room= 'Main Hall'
collected_loot= []

def show_room(room_name):
    room= rooms[room_name]
    exits= ', '.join(room['exits'].keys())
    print(Panel(
        f'[yellow]{room.get('display_name', room_name)}[/yellow]\n\n'
        f'{room['description']}\n\n'
        f'[grey]Exits:[/grey]{exits}',
        title='Room Info'
    ))

def end_game():
    print('\n[green]You have survived![/green]')
    print('[green]You collected {collected_loot}')
    
    if collected_loot:
        for item in collected_loot:
            print(f'.{item}')
            
    else:
        print('[dark green]You didn\'t collect any loot')
        
    choice= Prompt.ask('\nWould you like to [bold]play again?[/bold]', choices=['Yes', 'No'], default='No').capitalize
    if choice== 'Yes':
        return True
    
    else:
        print('[red]Thank you for playing[/red]')
        return False
        
        
def game_loop():
    global current_room
    while True:
        if current_room== 'Exit':
            if end_game():
                current_room= 'Main Hall'
                continue
            else:
                break
            
            
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