#possible loot
import random
chest_dict= {
    'Gold': 200,
    'Diamonds': 5,
    'Rubies': 10,
    'Emeralds': 20,
    'Garnet': 30,
    'Sharp Dagger': 5,
    }
enemy_drop= {
    'Gold': 50,
    'Rubies': 5,
    'Garnet': 10,
    'Old Dagger': 5,
    'Junk': 10
}
def random_chest():
    item= random.choice(list(chest_dict.keys()))
    max_amount= chest_dict[item]
    amount= random.randint(1, max_amount)
    return(item, amount)

def random_enemy():
    item= random.choice(list(enemy_drop.keys()))
    max_amount= enemy_drop[item]
    amount= random.randint(1, max_amount)
    return(item, amount)


# item, amount = random_chest()
# print(f"You found {amount} x {item} in the chest!")

# drop, qty = random_enemy()
# print(f"The enemy dropped {qty} x {drop}.")
