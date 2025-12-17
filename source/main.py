# This program is designed to take DnD-style monster stats and use them to essentially automate mobs to make it easier for DMs to
# run combat encounters with multiple enemies. This requires multiple components to function effectively: The character sheets of the
# players, positional data for combat, and the monsters' sheet(s). The monsters will always seek to deal the most damage possible based on
# relevant information.
# Developed by Brandon Mack from 12/16/2025 - ...

# import dependencies


# essential classes
class player():
    def __init__(self):
        pass

class monster():
    def __init__(self):
        pass

class npc_friend():
    def __init__(self):
        pass

# main method
def main():
    # initialize variables
    encounter = True


    # import character sheets into a list of player objects


    # import monster sheets into a list of monster objects


    # import friendly npc sheets into a list of friendly npc objects


    # finalize all combatants in encounter and begin combat loop

    # roll initiatives, and input player initiatives. Monsters will use a RNG as their scores.
    # input p1, p2,..., pn.

    # RNG 1-20 + initiative modifier from monster objects

    # Make all values in descending order

    # print turn order

    # determine starting positions on combat grid (1 space = 5 feet)
    # Grid size = X, Y

    # input all entity starting positions, position will be applied to location attribute of objects

    while encounter == True:
        # Begin action loop
        # if NPC turn, determine answer from available actions

        # else if player turn, choose from listed actions and follow prompts

        break
    

# supporting methods: import player sheet, import monster sheet, import NPC sheet(should be identical to monster sheet), RNG with different dice sizes

# follow-up methods (stretch goals): GUI, LLM integration