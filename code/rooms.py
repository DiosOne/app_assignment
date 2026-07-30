'''
Defines the layout and structure of all rooms in the game.

Each room is represented as a dictionary with:
- 'description': A string describing the room's appearance.
- 'exits': A dictionary of available movement directions and corresponding destination rooms.

Used for navigation and display throughout the game.
'''

rooms= {
    'Entrance Hall':{
        'description': 'a description goes here',
        'exits':{'North':'Main Hall', 'Northeast':'Servants Quarters', 'Northwest': 'Guard Post'}
    },
    
    'Main Hall':{
        'description': 'You see a grand entrance hall, chandeliers hanging from the ceiling',
        'exits':{'North':'Dining Hall', 'East':'Servants Quarters', 'West':'Guard Post', 'Northeast':'East Wing', 'Northwest':'West Wing'}
    },
    
    'Servants Quarters':{
        'description': 'a description goes here',
        'exits':{'North':'East Wing', 'West':'Main Hall', 'Northwest':'Dining Hall'}
    },
    
    'Guard Post':{
        'description':'a description goes here',
        'exits':{'North':'', 'East':'', 'Northeast':''}
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

    'Scullery':{
        'description': 'A large hearth and stone benches fill the room',
        'exits':{'North': 'Exit', 'West': 'Dining Hall'}
    },

    'room-2':{
        'description': 'An empty stone room waits in silence.',
        'exits':{}
    },

    'room-3':{
        'description': 'An empty stone room waits in silence.',
        'exits':{}
    },

    'room-4':{
        'description': 'An empty stone room waits in silence.',
        'exits':{}
    },

    'room-5':{
        'description': 'An empty stone room waits in silence.',
        'exits':{}
    },

    'Exit':{
        'description': 'You have survived the dungeon!',
        'exits':{}
    }
}
