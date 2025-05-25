class Adventurer:
    def __init__(self, health, armour, lightAttack, heavyAttack):
        self.health= health
        self.armour= armour
        self.attack1= lightAttack
        self.attack2= heavyAttack
    
class Fighter(Adventurer):
    health = int(16)
    armour= int(13)
    lightAttack= int(6)
    heavyAttack= int(10)

class Mage(Adventurer):
    health= int(10)
    armour= int(10)
    lightAttack= int(8)
    heavyAttack= int(16)

class Ranger(Adventurer):
    health= int(20)
    armour= int(15)
    lightAttack= int(4)
    heavyAttack= int(8)

def show_stats(cls):
    print(cls.__name__)
    print('-' * 10)
    print(f'Health: {cls.health}')
    print(f'Armour Class: {cls.armour}')
    print(f'Light Attack: {cls.lightAttack}')
    print(f'Heavy Attack: {cls.heavyAttack}')
    print('*' * 10)
    print()

# show_stats(Fighter)
# show_stats(Mage)
# show_stats(Ranger)
