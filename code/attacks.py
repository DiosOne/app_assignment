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

def roll_damage(damage):
    '''
    Rolls damage from a dice expression such as 1d6+2, 2d8, or 2d8+4+2d6.

    :param damage: Dice expression to roll.
    :type damage: str
    :return: Total damage rolled.
    :rtype: int
    '''

    total = 0
    for part in damage.replace(' ', '').split('+'):
        if 'd' in part:
            dice_count, dice_sides = part.split('d')
            for _ in range(int(dice_count)):
                total += dice_roll(f'd{dice_sides}')
        else:
            total += int(part)
    return total

def format_damage_prompt(damage):
    '''
    Formats damage dice for display in player roll prompts.

    :param damage: Dice expression to format.
    :type damage: str
    :return: Formatted damage expression.
    :rtype: str
    '''

    parts = damage.split('+')
    if len(parts) == 1:
        return damage
    return parts[0] + ''.join(f'(+{part})' for part in parts[1:])

def prompt_damage_roll(attack, attack_number=1, attack_total=1):
    '''
    Prompts the player to roll damage for a successful attack.

    :param attack: Attack data for the successful attack.
    :type attack: dict
    :param attack_number: Current attack number for multi-attack abilities.
    :type attack_number: int
    :param attack_total: Total number of attacks for the chosen ability.
    :type attack_total: int
    :return: Total damage rolled.
    :rtype: int
    '''

    while True:
        attack_label = attack['name']
        if attack_total > 1:
            attack_label = f'{attack_label} {attack_number}/{attack_total}'

        rprint(
            f'Your [bold]{attack_label}[/bold] attack hits! '
            f'Roll a [bold]{format_damage_prompt(attack["damage"])}[/bold]!'
        )
        input(f'Press Enter to Roll {format_damage_prompt(attack["damage"])}: ')
        return roll_damage(attack['damage'])

def choose_player_attack(player):
    '''
    Prompts the player to choose one of their available attacks.

    :param player: The player character choosing an attack.
    :type player: Adventurer or subclass instance.
    :return: The selected attack, or 'quit' if the player flees.
    :rtype: dict or str
    '''

    rprint('[bold]Choose your attack:[/bold]')
    for index, attack in enumerate(player.attacks, start=1):
        repeat_text = ''
        if attack.get('times', 1) > 1:
            repeat_text = f" x{attack['times']}"
        rprint(
            f"{index}. {attack['name']} "
            f"(+{attack['hit_bonus']} to hit, {attack['damage']} damage{repeat_text})"
        )

    choice = input('Attack or type "quit" to flee: ').lower()
    if choice == 'quit':
        return 'quit'

    if choice.isdigit():
        attack_index = int(choice) - 1
        if 0 <= attack_index < len(player.attacks):
            return player.attacks[attack_index]

    for attack in player.attacks:
        if choice == attack['name'].lower():
            return attack

    return None

def fight_enemy(player, enemy):
    '''
    Conducts a turn-based fight sequence between the player and an enemy.

    The player chooses an available attack or can flee.
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
        player_attack = choose_player_attack(player)

        if player_attack == 'quit':
            rprint('[yellow]You fled the fight![/yellow]')
            return 'quit'

        if player_attack is None:
            rprint('Invalid Attack. Please choose one of the listed attacks')
            continue

        attack_total = player_attack.get('times', 1)
        for attack_number in range(1, attack_total + 1):
            attack_roll= dice_roll('d20') + player_attack['hit_bonus']

            if attack_total > 1:
                rprint(f'Attack Roll {attack_number}/{attack_total}: {attack_roll}')
            else:
                rprint(f'Attack Roll: {attack_roll}')
            rprint(f'You use {player_attack["name"]} against the {enemy.name}')

            if attack_roll >= enemy.armour:
                damage_roll= prompt_damage_roll(player_attack, attack_number, attack_total)
                enemy.health-= damage_roll
                rprint(
                    f'[green]You do {damage_roll} points of damage to the '
                    f'[bold][{enemy.colour}]{enemy.name}[/{enemy.colour}][/bold]![/green]'
                )

            else:
                rprint('Your attack missed')

            if enemy.health<= 0:
                rprint(
                    f'[green]You defeated the [bold]'
                    f'[{enemy.colour}]{enemy.name}[/{enemy.colour}][/bold]![/green]'
                )
                return 'win'

        enemy_attack= random.choice(enemy.attacks)
        for _ in range(enemy_attack.get('times', 1)):
            enemy_attack_roll= dice_roll('d20') + enemy_attack['hit_bonus']

            rprint(
                f'The [{enemy.colour}]{enemy.name}[/{enemy.colour}] '
                f'uses {enemy_attack["name"]}. Attack Roll: {enemy_attack_roll}'
            )

            if enemy_attack_roll>= player.armour:
                rprint(
                    f'The [{enemy.colour}]{enemy.name}[/{enemy.colour}] '
                    f'rolls {enemy_attack["damage"]} for damage.'
                )
                enemy_damage= roll_damage(enemy_attack['damage'])

                rprint(
                    f'[red]The [bold][{enemy.colour}]{enemy.name}[/{enemy.colour}]'
                    f'[/bold] does {enemy_damage} damage![/red]')
                player.health-= enemy_damage
            else:
                rprint(
                    f'[blue]The [bold][{enemy.colour}]{enemy.name}'
                    f'[/{enemy.colour}][/bold] misses![/blue]')

            if player.health<= 0:
                break

        if player.health<= 0:
            rprint('[bold][red]You Have Been Defeated![/red][/bold]')
            choice = Prompt.ask(
                '\nWould you like to [bold]play again?[/bold]',
                choices=['Yes', 'No'],
                default='No'
            ).capitalize()

            if choice== 'Yes':
                return True

            else:
                rprint('[red]Thank you for playing[/red]')
                return False

        rprint(
            f"[cyan]Your Health: [{player.colour}]{player.health}[/{player.colour}] | "
            f"Enemy Health: [{enemy.colour}]{enemy.health}[/{enemy.colour}][/cyan]"
        )
