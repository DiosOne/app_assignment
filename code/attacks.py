from dice_rolls import dice_roll
from advent import Adventurer, Fighter, Mage, Ranger, show_stats
from enemies import Enemy, Goblin, Ratking, Skeleton, show_enemy_stats
from loot_table import random_chest, random_enemy
import random
from rich import print
from rich.prompt import Prompt

def fight_enemy(player, enemy):
    # enemy_class= random.choice([Goblin, Skeleton, Ratking])
    # enemy= enemy_class()
    # show_enemy_stats(enemy)
    while player.health > 0 and enemy.health > 0:
        attack_type= input('Choose your attack (light or heavy) or type "quit" to flee: ').lower()

        if attack_type == 'quit':
            print('[yellow]You fled the fight![/yellow]')
            return 'quit'

        if attack_type== 'light':
            attack_roll= dice_roll('d20') + 2
            damage_roll= dice_roll(f'd{player.attack1}')
            
        elif attack_type== "heavy":
            attack_roll= dice_roll('d20')
            damage_roll= dice_roll(f'd{player.attack2}') + 2
        else:
            print('Invalid Attack. Please choose light or heavy')
            continue

    # if player.attack1:
    #     damage_roll= dice_roll('d6')
    # elif player.attack2:
    #     damage_roll= dice_roll('d10') + 2
        
        print(f'Attack Roll: {attack_roll}')
        print(f'You attack the {enemy.name}')

        if attack_roll >= enemy.armour:
            enemy.health-= damage_roll
            print(f'[green]You do {damage_roll} points of damage to the [bold][{enemy.colour}]{enemy.name}[/{enemy.colour}][/bold]![/green]')

        else: 
            print('Your attack missed')
            
        if enemy.health<= 0:
            print(f'[green]You defeated the [bold][{enemy.colour}]{enemy.name}[/{enemy.colour}][/bold]![/green]')
            return 'win'
        
        enemy_attack_type= random.choice(['light', 'heavy'])
        enemy_attack_roll= dice_roll('d20')
        
        if enemy_attack_roll>= player.armour:
            if enemy_attack_type== 'light':
                enemy_damage= dice_roll(f'd{enemy.attack1}')
            else:
                enemy_damage= dice_roll(f'd{enemy.attack2}')
                
            player.health-= enemy_damage
            print(f'[red]The [bold][{enemy.colour}]{enemy.name}[/{enemy.colour}][/bold] does {enemy_damage} damage![/red]')
        else:
            print(f'[blue]The [bold][{enemy.colour}]{enemy.name}[/{enemy.colour}][/bold] misses![/blue]')

        if player.health<= 0:
            print('[bold][red]You Have Been Defeated![/red][/bold]')
            choice= Prompt.ask('\nWould you like to [bold]play again?[/bold]', choices=['Yes', 'No'], default='No').capitalize()
            if choice== 'Yes':
                return True
            
            else:
                print('[red]Thank you for playing[/red]')
                return False
            
                
        print(f"[cyan]Your Health: [{player.colour}]{player.health}[/{player.colour}] | Enemy Health: [{enemy.colour}]{enemy.health}[/{enemy.colour}][/cyan]")

    # item, amount = random_chest()
    # print(f"You found {amount} x {item} in the chest!")

    # drop, qty = random_enemy()
    # print(f"The enemy dropped {qty} x {drop}.")
