"""
dice_rolls.py

Utility module for simulating dice rolls used in combat and gameplay mechanics.

Provides support for standard tabletop dice types such as d4, d6, d8, d10, d12, d16, and d20.

:return: A random integer representing the result of a simulated dice roll.
:rtype: int
"""

import random

def dice_roll(dice_type):
    """
    Simulates a dice roll for a given dice type.

    Supported dice types include: 'd4', 'd6', 'd8', 'd10', 'd12', 'd16', 'd20'.
    Returns a random integer between 1 and the maximum value of the dice.

    :param dice_type: A string representing the dice type (e.g., 'd6', 'd20').
    :type dice_type: str
    :return: A random integer between 1 and the max value of the specified dice.
    :rtype: int

    :raises ValueError: If an unsupported dice type is provided.
    """

    if dice_type == "d4":
        max_number = 4
    elif dice_type == "d6":
        max_number = 6
    elif dice_type == "d8":
        max_number = 8
    elif dice_type == "d10":
        max_number = 10
    elif dice_type == "d12":
        max_number = 12
    elif dice_type == "d16":
        max_number = 16
    elif dice_type == "d20":
        max_number = 20
    else:
        raise ValueError(f'Unknown dice type: {dice_type}')

    return random.randint(1, max_number)

# Example usage:
# attack_roll = dice_roll("d20")
# damage_roll = dice_roll("d8")
# print(f"Attack roll: {attack_roll}")
# print(f"Damage roll: {damage_roll}")
