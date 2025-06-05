'''_summary_

    :return: _description_
    :rtype: _type_
    '''
import random

def dice_roll(dice_type):
    '''_summary_

    :param dice_type: _description_
    :type dice_type: _type_
    :return: _description_
    :rtype: _type_
    '''

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
    elif dice_type== 'd16':
        max_number = 16
    elif dice_type == "d20":
        max_number = 20
    else:
        raise ValueError(f'Unknown dice type: {dice_type}')

    return random.randint(1, max_number)

# attack_roll = dice_roll("d20")
# damage_roll = dice_roll("d8")

# print(f"Attack roll: {attack_roll}")
# print(f"Damage roll: {damage_roll}")
