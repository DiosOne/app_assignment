from dice_rolls import dice_roll
from advent import Adventurer, Fighter, Mage, Ranger, show_stats
from enemies import Enemy, Goblin, Ratking, Skeleton, show_enemy_stats
from loot_table import random_chest, random_enemy
import random
from rich import print

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

    # if player.attack1:
    #     damage_roll= dice_roll('d6')
    # elif player.attack2:
    #     damage_roll= dice_roll('d10') + 2
        
    print(f'Attack Roll: {attack_roll}')
    print(f'You attack the {enemy.name}')

    if attack_roll >= enemy.armour:
        enemy.health-= damage_roll
        print(f'[green]You do {damage_roll} points of damage to the [bold{enemy.colour}{enemy.name}][/bold{enemy.colour}]![/green]')
    else: 
        print('Your attack missed')
        
    if enemy.health<= 0:
        print(f'[green]You defeated the [bold{enemy.colour}{enemy.name}][/bold{enemy.colour}]![/green]')
        return 'win'
    
    

# item, amount = random_chest()
# print(f"You found {amount} x {item} in the chest!")

# drop, qty = random_enemy()
# print(f"The enemy dropped {qty} x {drop}.")
