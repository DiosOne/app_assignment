class Enemy:
    def __init__(self, name, health, armour, lightAttack, heavyAttack):
        self.name = name
        self.health = health
        self.armour = armour
        self.attack1 = lightAttack
        self.attack2 = heavyAttack


class Ratking(Enemy):
    def __init__(self):
        super().__init__(name="Ratking", health=14, armour=12, lightAttack=4, heavyAttack=8)


class Skeleton(Enemy):
    def __init__(self):
        super().__init__(name="Skeleton", health=10, armour=10, lightAttack=6, heavyAttack=12)


class Goblin(Enemy):
    def __init__(self):
        super().__init__(name="Goblin", health=20, armour=12, lightAttack=4, heavyAttack=8)


def show_enemy_stats(enemy):
    print(enemy.name)
    print('-' * 10)
    print(f'Health: {enemy.health}')
    print(f'Armour Class: {enemy.armour}')
    print(f'Light Attack: {enemy.attack1}')
    print(f'Heavy Attack: {enemy.attack2}')
    print('*' * 10)
    print()

# show_stats(Ratking)
# show_stats(Skeleton)
# show_stats(Goblin)
