# This program is designed to take DnD-style monster stats and use them to essentially automate mobs to make it easier for DMs to
# run combat encounters with multiple enemies. This requires multiple components to function effectively: The character sheets of the
# players, positional data for combat, and the monsters' sheet(s). The monsters will always seek to deal the most damage possible based on
# relevant information.
# Developed by Brandon Mack from 12/16/2025 - ...

# import dependencies
import sys
import os
import re
import random
from csv_importer import read_csv_as_dicts


# essential classes
class monster():
    # default monster with all stats based off of the spreadsheet provided by RufflesDMAccount on reddit:
    # https://www.reddit.com/r/UnearthedArcana/comments/8zvr6s/the_great_dd5e_monster_spreadsheet/
    def __init__(self, id):
        self.id = id
        self.name = "Default_Test"
        self.size =  "Medium"
        self.type = "Humanoid"
        self.alignment = "U"
        self.armor_class = 5
        self.total_hit_points = 15
        self.speed_generic = 30
        self.strength = 10
        self.dexterity = 10
        self.constitution = 10
        self.intelligence = 10
        self.wisdom = 10
        self.charisma = 10
        self.saving_throws = []
        self.skills = []
        self.weaknesses = "None"
        self.resistances = "None"
        self.immunities = "None"
        self.senses = "Normal"
        self.languages = "Common"
        self.additional_perks = "None"
        self.source = "Monster Manual"
        self.author = "Wizards of the Coast"


def _safe_int(value, default=None):
    if value is None:
        return default
    if isinstance(value, int):
        return value
    s = str(value)
    m = re.search(r"-?\d+", s)
    if m:
        try:
            return int(m.group(0))
        except ValueError:
            return default
    return default


def create_npc_from_row(row, id, nickname, role):
    # normalize keys to lowercase for flexible matching
    lc = {k.strip().lower(): (v.strip() if isinstance(v, str) else v) for k, v in (row or {}).items()}
    if role.lower() == 'friend':
        m = npc_friend(id, nickname = "default_nick")
        m.nickname = lc.get('nickname') or lc.get('nick') or m.nickname
    elif role.lower() == 'player':
        m = player(id, player_name = "default_player")
        m.player_name = lc.get('player name') or lc.get('player') or m.player_name
    else:
        m = monster(id)
    # name
    m.name = lc.get('name') or lc.get('monster') or m.name
    # basic text fields
    m.size = lc.get('size') or m.size
    m.type = lc.get('type') or m.type
    m.alignment = lc.get('alignment') or m.alignment
    m.source = lc.get('source') or m.source

    # numeric fields
    m.armor_class = _safe_int(lc.get('armor class') or lc.get('ac') or lc.get('armor_class') or m.armor_class, m.armor_class)
    m.total_hit_points = _safe_int(lc.get('hp') or lc.get('hit points') or lc.get('total hit points') or m.total_hit_points, m.total_hit_points)
    m.speed_generic = _safe_int(lc.get('speed') or lc.get('speed_generic') or m.speed_generic, m.speed_generic)

    # ability scores
    m.strength = _safe_int(lc.get('str') or lc.get('strength') or m.strength, m.strength)
    m.dexterity = _safe_int(lc.get('dex') or lc.get('dexterity') or m.dexterity, m.dexterity)
    m.constitution = _safe_int(lc.get('con') or lc.get('constitution') or m.constitution, m.constitution)
    m.intelligence = _safe_int(lc.get('int') or lc.get('intelligence') or m.intelligence, m.intelligence)
    m.wisdom = _safe_int(lc.get('wis') or lc.get('wisdom') or m.wisdom, m.wisdom)
    m.charisma = _safe_int(lc.get('cha') or lc.get('charisma') or m.charisma, m.charisma)

    return m

#Friendly npc is a child of parent class monster, as they will use the same stats
class npc_friend(monster):
    def __init__(self, id, nickname):
        super().__init__(id)
        self.nickname = nickname

class player(monster):
   def __init__(self, id, player_name):
       super().__init__(id)
       self.player_name = player_name

# main method
def main():
    # initialize variables
    encounter = True

    # Load monster CSV (path can be passed as first arg)
    default_csv = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Data', 'Monster Spreadsheet (D&D5e) - Official Stats.csv'))
    csv_path = sys.argv[1] if len(sys.argv) > 1 else default_csv
    try:
        monsters = read_csv_as_dicts(csv_path)
        print(f'Loaded {len(monsters)} monster rows (preview):')
        #for m in monsters:
            #print(m)
    except Exception as e:
        print('Could not load CSV:', e)

    # Convert CSV rows to monster objects (remove limit for full load when desired)
    try:
        full_rows = read_csv_as_dicts(csv_path, limit=None)
        monster_objs = [create_npc_from_row(r, i + 1, None, 'monster') for i, r in enumerate(full_rows)]
        print(f'Instantiated {len(monster_objs)} monster objects.')
    except Exception as e:
        print('Could not instantiate monsters:', e)
        monster_objs = []

    # Simple encounter: roll initiative for each monster and print turn order
    # Find which monsters are participating in the encounter
    participants = []
    while encounter == True:
        participating_names = input('Enter enemy monster names for encounter one at a time, or "exit" to quit: ')
        #Exit condition when finished adding monsters
        if participating_names.lower() == 'exit':
            encounter = False
            break
        else:
        #Otherwise, add monster to encounter list
            for monster in monster_objs:
                name = monster.name.strip()
                if name == participating_names:
                    participants.append(monster)
                    print(f'Added {name} to encounter.')


    # import friendly npc sheets into a list of friendly npc objects
    # Load friendly CSV (path can be passed as second arg)
    default_csv = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Data', 'Friends.csv'))
    csv_path = sys.argv[2] if len(sys.argv) > 1 else default_csv
    try:
        friends = read_csv_as_dicts(csv_path)
        print(f'Loaded {len(friends)} friend rows (preview):')
        #for m in friends:
            #print(m)
    except Exception as e:
        print('Could not load CSV:', e)

    # Convert CSV rows to npc_friend objects (remove limit for full load when desired)
    try:
        full_rows = read_csv_as_dicts(csv_path, limit=None)
        npc_friend_objs = [create_npc_from_row(r, i + 1, None, 'friend') for i, r in enumerate(full_rows)]
        print(f'Instantiated {len(npc_friend_objs)} npc_friend objects.')
    except Exception as e:
        print('Could not instantiate friends:', e)
        npc_friend_objs = []

    # Now, integrate friendly npcs into encounter
    encounter = True
    while encounter == True:
        participating_names = input('Enter friendly names for encounter one at a time, or "exit" to quit: ')
        #Exit condition when finished adding friends
        if participating_names.lower() == 'exit':
            encounter = False
            break
        else:
        #Otherwise, add friends to encounter list
            for friends in npc_friend_objs:
                nickname = friends.nickname.strip()
                if nickname == participating_names:
                    participants.append(friends)
                    print(f'Added {nickname} to encounter.')

    # Finally, import character sheets into a list of player objects
    # Load player CSV (path can be passed as third arg)
    default_csv = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Data', 'Players.csv'))
    csv_path = sys.argv[3] if len(sys.argv) > 1 else default_csv
    try:
        players = read_csv_as_dicts(csv_path)
        print(f'Loaded {len(players)} player rows (preview):')
        #for m in players:
            #print(m)
    except Exception as e:
        print('Could not load CSV:', e)

    # Convert CSV rows to player objects (remove limit for full load when desired)
    try:
        full_rows = read_csv_as_dicts(csv_path, limit=None)
        player_objs = [create_npc_from_row(r, i + 1, None, 'player') for i, r in enumerate(full_rows)]
        print(f'Instantiated {len(player_objs)} player objects.')
    except Exception as e:
        print('Could not instantiate players:', e)
        player_objs = []

    # Now, integrate players into encounter
    encounter = True
    while encounter == True:
        participating_names = input('Enter player names for encounter one at a time, or "exit" to quit: ')
        #Exit condition when finished adding players
        if participating_names.lower() == 'exit':
            encounter = False
            break
        else:
        #Otherwise, add players to encounter list
            for player in player_objs:
                player_name = player.player_name.strip()
                if player_name == participating_names:
                    participants.append(player)
                    print(f'Added {player_name} to encounter.')


    # Next, roll initiatives for each participant and sort them in descending order
    if participants:
        for m in participants:
            dex = m.dexterity if isinstance(m.dexterity, int) else 10
            dex_mod = (dex - 10) // 2
            m.initiative = random.randint(1, 20) + dex_mod
        participants.sort(key=lambda x: getattr(x, 'initiative', 0), reverse=True)
        print('Turn order (name - initiative):')
        for m in participants:
            print(f"{m.name} - {getattr(m, 'initiative', 0)}")

    # Next steps: set up combat grid and positions

    # determine starting positions on combat grid (1 space = 5 feet)
    # Grid size = X, Y

    # input all entity starting positions, position will be applied to location attribute of objects

    #while encounter == True:
        # Begin action loop
        # if NPC turn, determine answer from available actions

        # else if player turn, choose from listed actions and follow prompts

        #break
    

# supporting methods: import player sheet, import monster sheet, import NPC sheet(should be identical to monster sheet), RNG with different dice sizes

# follow-up methods (stretch goals): GUI, LLM integration

if __name__ == '__main__':
    main()