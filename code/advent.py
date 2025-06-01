from rich import print

class Adventurer:
    def __init__(self, health, armour, lightAttack, heavyAttack, colour='white'):
        self.health= health
        self.armour= armour
        self.attack1= lightAttack
        self.attack2= heavyAttack
        self.colour= colour
    
class Fighter(Adventurer):
    def __init__(self):
        super().__init__(health=16, armour=13, lightAttack=6, heavyAttack=10, colour='bold red')


class Mage(Adventurer):
    def __init__(self):
        super().__init__(health=10, armour=10, lightAttack=8, heavyAttack=16, colour='bold purple')
        


class Ranger(Adventurer):
    def __init__(self):
        super().__init__(health=20, armour=15, lightAttack=4, heavyAttack=8, colour='bold green')


def show_stats(character):
    print(f'[{character.colour}]{character.__class__.__name__}[/{character.colour}]')
    print('-' * 10)
    print(f'Health: {character.health}')
    print(f'Armour Class: {character.armour}')
    print(f'Light Attack max damage: {character.attack1}')
    print(f'Heavy Attack max damage: {character.attack2}')
    print('*' * 10)
    print()

# show_stats(Fighter)
# show_stats(Mage)
# show_stats(Ranger)
