class Adventurer:
    def __init__(self, health, armour, lightAttack, heavyAttack):
        self.health= health
        self.armour= armour
        self.attack1= lightAttack
        self.attack2= heavyAttack
    
class Fighter(Adventurer):
    def __init__(self):
        super().__init__(health=16, armour=13, lightAttack=6, heavyAttack=10)


class Mage(Adventurer):
    def __init__(self):
        super().__init__(health=10, armour=10, lightAttack=8, heavyAttack=16)
        


class Ranger(Adventurer):
    def __init__(self):
        super().__init__(health=20, armour=15, lightAttack=4, heavyAttack=8)


def show_stats(character):
    print(character.__class__.__name__)
    print('-' * 10)
    print(f'Health: {character.health}')
    print(f'Armour Class: {character.armour}')
    print(f'Light Attack max damage: {character.lightAttack}')
    print(f'Heavy Attack max damage: {character.heavyAttack}')
    print('*' * 10)
    print()

# show_stats(Fighter)
# show_stats(Mage)
# show_stats(Ranger)
