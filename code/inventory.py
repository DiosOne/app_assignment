inventory = []

def add_to_inv(item, quantity=1):
    for i in range(quantity):
        inventory.append(item)
        
def show_inv():
    if not inventory:
        print('[grey]Your inventory is empty.[/grey]')
    else:
        print('')