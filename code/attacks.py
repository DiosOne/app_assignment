'''
Module attacks.py

Provides combat functionality between the player and enemy characters.
Includes the fight_enemy function which handles turn-based fighting,
attack type selection, hit/miss logic, damage calculation, and health updates.
Uses dice rolls to determine attack success and damage.

Dependencies:
- random: for random choice selection
- dice_rolls.dice_roll: for dice-based random rolls
- rich.print (imported as rprint): for styled console output
- rich.prompt.Prompt: for interactive user input during defeat
'''

import random
from dice_rolls import dice_roll
from rich import print as rprint
from rich.prompt import Prompt

def fight_enemy(player, enemy):
    '''
    Conducts a turn-based fight sequence between the player and an enemy.

    The player chooses attack types (light or heavy) or can flee.
    Each attack involves dice rolls to determine hits and damage.
    The enemy attacks back automatically after the player's turn.
    The fight continues until either combatant's health reaches zero or the player flees.

    :param player: The player character object engaging in combat.
    :type player: Adventurer or subclass instance (e.g., Fighter, Mage, Ranger)
    :param enemy: The enemy character object the player is fighting.
    :type enemy: Enemy or subclass instance (e.g., Goblin, Skeleton, Ratking)
    :return: 'win' if player defeats enemy, 'quit' if player flees,
             True if player chooses to play again after defeat,
             False if player chooses not to play again after defeat.
    :rtype: str or bool
    '''

    while player.health > 0 and enemy.health > 0:
        attack_type= input('Choose your attack (light or heavy) or type "quit" to flee: ').lower()

        if attack_type == 'quit':
            rprint('[yellow]You fled the fight![/yellow]')
            return 'quit'

        if attack_type== 'light':
            attack_roll= dice_roll('d20') + 2
            damage_roll= dice_roll(f'd{player.attack1}')

        elif attack_type== "heavy":
            attack_roll= dice_roll('d20')
            damage_roll= dice_roll(f'd{player.attack2}') + 2
        else:
            rprint('Invalid Attack. Please choose light or heavy')
            continue


        rprint(f'Attack Roll: {attack_roll}')
        rprint(f'You attack the {enemy.name}')

        if attack_roll >= enemy.armour:
            enemy.health-= damage_roll
            rprint(f'[green]You do {damage_roll} points of damage to the [bold][{enemy.colour}]{enemy.name}[/{enemy.colour}][/bold]![/green]')

        else:
            rprint('Your attack missed')

        if enemy.health<= 0:
            rprint(f'[green]You defeated the [bold][{enemy.colour}]{enemy.name}[/{enemy.colour}][/bold]![/green]')
            return 'win'

        enemy_attack_type= random.choice(['light', 'heavy'])
        enemy_attack_roll= dice_roll('d20')

        if enemy_attack_roll>= player.armour:
            if enemy_attack_type== 'light':
                enemy_damage= dice_roll(f'd{enemy.attack1}')
            else:
                enemy_damage= dice_roll(f'd{enemy.attack2}')

            player.health-= enemy_damage
            rprint(f'[red]The [bold][{enemy.colour}]{enemy.name}[/{enemy.colour}][/bold] does {enemy_damage} damage![/red]')
        else:
            rprint(f'[blue]The [bold][{enemy.colour}]{enemy.name}[/{enemy.colour}][/bold] misses![/blue]')

        if player.health<= 0:
            rprint('[bold][red]You Have Been Defeated![/red][/bold]')
            choice= Prompt.ask('\nWould you like to [bold]play again?[/bold]', choices=['Yes', 'No'], default='No').capitalize()
            if choice== 'Yes':
                return True

            else:
                rprint('[red]Thank you for playing[/red]')
                return False

        rprint(f"[cyan]Your Health: [{player.colour}]{player.health}[/{player.colour}] | Enemy Health: [{enemy.colour}]{enemy.health}[/{enemy.colour}][/cyan]")
