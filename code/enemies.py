class Enemy:
    def __init__(self, health, armour, lightAttack, heavyAttack):
        self.health= health
        self.armour= armour
        self.attack1= lightAttack
        self.attack2= heavyAttack
    
class Ratking(Enemy):
    health = int(14)
    armour= int(12)
    lightAttack= int(4)
    heavyAttack= int(8)

class Skeleton(Enemy):
    health= int(10)
    armour= int(10)
    lightAttack= int(6)
    heavyAttack= int(12)

class Goblin(Enemy):
    health= int(20)
    armour= int(12)
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

# show_stats(Ratking)
# show_stats(Skeleton)
# show_stats(Goblin)
