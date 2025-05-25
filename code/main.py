from dice_rolls import dice_roll
from advent import Adventurer, Fighter, Mage, Ranger, show_stats
from enemies import Enemy, Goblin, Skeleton, Ratking

show_stats(Fighter)
attack_roll= dice_roll('d20')
print(f'Attack: {attack_roll}')