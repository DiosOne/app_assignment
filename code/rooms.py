'''
Defines the layout and structure of all rooms in the game.

Each room is represented as a dictionary with:
- 'description': A string describing the room's appearance.
- 'exits': A dictionary of available movement directions and corresponding destination rooms.

Used for navigation and display throughout the game.
'''

rooms= {
    'Entrance Hall':{
        'description': 'A cold stone entrance hall with heavy doors behind you and torchlight ahead.',
        'exits':{'North':'Main Hall', 'Northeast':'Servants Quarters', 'Northwest': 'Guard Post'}
    },
    
    'Main Hall':{
        'description': 'You see a grand entrance hall, chandeliers hanging from the ceiling',
        'exits':{'North':'Dining Hall', 'East':'Servants Quarters', 'West':'Guard Post', 'Northeast':'East Wing', 'Northwest':'West Wing'}
    },
    
    'Servants Quarters':{
        'description': 'Narrow bunks and old footlockers line the walls of this cramped servants quarters.',
        'exits':{'North':'East Wing', 'West':'Main Hall', 'Northwest':'Dining Hall'}
    },
    
    'Guard Post':{
        'description':'Weapon racks, dented shields, and a worn watch table fill the old guard post.',
        'exits':{'North':'West Wing', 'East':'Main Hall', 'Northeast':'Dining Hall'}
    },

    'West Wing':{
        'description':  
            'You are in a medium sized room, with storage shelves and torches on the walls',
        'exits':{'North':'Armoury', 'East':'Dining Hall', 'West':'Bedroom', 'Northeast':'Scullery'}
    },

    'Library':{
        'description': 'A small room with dusty bookshelves lit by numerous cadelabras',
        'exits':{'West':'East Wing', 'Northwest':'Chapel'}
    },

    'Dining Hall':{
        'description': 'A large dinning table sits in the center of the room, lit by a grandiose chandelier',
        'exits':{'North':'Scullery', 'East':'East Wing', 'West':'West Wing', 'Northeast':'Chapel', 'Northwest':'Armoury'}
    },

    'Bedroom':{
        'description': 'A cosy room  with a large bed in the center with torches on the walls',
        'exits':{'East':'West Wing', 'Northeast':'Armoury'}
    },

    'East Wing':{
        'description': 'A long eastern corridor with cracked portraits and faded carpet underfoot.',
        'exits':{'North':'Chapel', 'East':'Library', 'West':'Dining Hall', 'Northwest':'Scullery'}
    },

    'Scullery':{
        'description': 'A large hearth, stained stone benches, and stacks of blackened pots fill the room.',
        'exits':{'North':'Exit', 'East':'Chapel', 'West':'Armoury', 'Northeast':'Treasury', 'Northwest':'Observatory'}
    },

    'Armoury':{
        'description': 'Rusting blades, battered helmets, and broken spear shafts are stacked against the walls.',
        'exits':{'North':'Observatory', 'East':'Scullery'}
    },

    'Chapel':{
        'description': 'A quiet chapel with cracked pews, melted candles, and a cold stone altar.',
        'exits':{'North':'Treasury', 'West':'Scullery'}
    },

    'Observatory':{
        'description': 'A domed chamber where dusty star charts surround a tarnished brass telescope.',
        'exits':{'East':'Treasury', 'Northeast':'Exit'}
    },

    'Treasury':{
        'description': 'Empty coin racks and broken lockboxes suggest this room once held great wealth.',
        'exits':{'West':'Observatory', 'Northwest':'Exit'}
    },

    'Exit':{
        'description': 'You have survived the dungeon!',
        'exits':{}
    }
}
