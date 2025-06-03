inventory = []

def add_to_inv(item, quantity=1):
    for i in range(quantity):
        inventory.append(item)
        
def show_inv():
    if not inventory:
        print('[bright_black]Your inventory is empty.[/bright_black]')
    else:
        print('[bold][dodger_blue1]Your inventory: [/dodger_blue1][/bold]')
        counted= {}
        for item in inventory:
            counted[item]= counted.get(item, 0) + 1
        for item, count in counted.items():
            print(f'- {item}x{count}')
            
