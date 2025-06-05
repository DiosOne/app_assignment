'''
Defines the layout and structure of all rooms in the game.

Each room is represented as a dictionary with:
- 'description': A string describing the room's appearance.
- 'exits': A dictionary of available movement directions and corresponding destination rooms.

Used for navigation and display throughout the game.
'''

rooms= {
    'Main Hall':{
        'description': 'You see a grand entrance hall, chandeliers hanging from the ceiling',
        'exits':{'North': 'Dining Hall', 'East':'Library', 'West': 'West Wing'}
    },

    'West Wing':{
        'description':  
            'You are in a medium sized room, with storage shelves and torches on the walls',
        'exits':{'North': 'Dining Hall', 'East': 'Main Hall', 'West': 'Cupboard'}
    },

    'Library':{
        'description': 'A small room with dusty bookshelves lit by numerous cadelabras',
        'exits':{'West': 'Main Hall'}
    },

    'Dining Hall':{
        'description': 'A large dinning table sits in the center of the room, lit by a chandelier',
        'exits':{'North': 'Bedroom', 'East': 'Galley', 'South': 'Main Hall', 'West': 'West Wing'}
    },

    'Bedroom':{
        'description': 'A cosy room  with a large bed in the center with torches on the walls',
        'exits':{'East': 'Dining Hall', 'West': 'Bedroom Cupboard'}
    },

    'Galley':{
        'description': 'A large hearth and stone benches fill the room',
        'exits':{'North': 'Exit', 'South': 'Dining Hall'}
    },

    'Cupboard':{
        'description': 'A small cupboard containing a chest',
        'exits':{'East': 'West Wing'}
    },

    'Bedroom Cupboard':{
        'description': 'A small cupboard containing a chest',
        'exits':{'East': 'Bedroom'}
    },

    'Exit':{
        'description': 'You have survived the dungeon!',
        'exits':{}
    }
}
