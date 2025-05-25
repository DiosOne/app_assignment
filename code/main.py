from dice_rolls import dice_roll
from advent import Adventurer, Fighter, Mage, Ranger, show_stats
from enemies import Enemy, Goblin, Skeleton, Ratking, show_stats
import loot_table

# show_stats(Fighter)
print(Fighter.__name__)
print(f'Health: {Fighter.health}')
attack_roll= dice_roll('d20')
damage_roll= dice_roll('d12')
# print(f'Attack: {attack_roll}')
if attack_roll <= 10:
    print(f'You do {damage_roll} points of damage')
else: print('Your attack missed')