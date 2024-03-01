import pandas as pd
from itertools import combinations
import matchup_calcs as mc

#returns a onehot list for what types the target type is neutral or better against offensivley 
#e.g. onehot_offense('Normal') will return all 1's except for 0's on Rock, Steel, and Ghost
def onehot_offense_strict(type):
    # Using list comprehension to apply the condition to each element in the row
    return [1 if x > 1 else 0 for x in mc.type_chart_atk[type]]

#returns a onehot list for what types the target type beats offensivley 
#e.g. onehot_offense('Fire') will return all 0's except for 1's on Bug, Grass, Ice, and Steel
def onehot_offense_relaxed(type):
    # Using list comprehension to apply the condition to each element in the row
    return [1 if x >= 1 else 0 for x in mc.type_chart_atk[type]]

#returns a onehot list for what types the target type beats defensivley 
# e.g. onehot_defense('Psychic') will return all 0's except for 1's on Psychic, fighting
def onehot_defense(type):
    # Using list comprehension to apply the condition to each element in the row
    return [1 if x < 1 else 0 for x in mc.type_chart_def[type]]

#helper method to only return tuples that do not contain any of the previous tuples, because this is a minimum set covering problem
def filter_unique_tuples(tuples_list):
    unique_tuples = []  # List to store unique tuples without any previously seen tuple completely contained

    for current_tuple in sorted(tuples_list, key=len):  # Sort by length to ensure smaller tuples are considered first
        # Check if the current tuple contains any of the previously added tuples as a subset
        if not any(set(sub_tuple).issubset(set(current_tuple)) for sub_tuple in unique_tuples if sub_tuple != current_tuple):
            unique_tuples.append(current_tuple)

    return unique_tuples

#Finds every combination of types that hits every type for neutral
def offensive_relaxed_min_covers(df):
    # Store combinations that meet criteria
    valid_combinations = []
    types = mc.type_list  # Get all types from the DataFrame columns

    # Generate all combinations for the given types
    for r in range(2, len(types) + 1):  # Start from 2 to include all types

        #go over all combos
        for combo in combinations(types, r):

            #make a list of 1s with length of all types
            combo_score = [0 for i in range(len(mc.type_chart_def.columns.tolist()))]

            # Check if this combo can get everything super effectivley
            for type in combo:
                    
                    #get onehot list for type
                    type_scores = onehot_offense_relaxed(type)
                    
                    #multiply by each type score.
                    for i in range(len(combo_score)):
                        if type_scores[i] == 1:
                            combo_score[i] = 1

                        #this is boolean algebra. If everything is a 1, then we are done. 
                        if sum(combo_score)==len(combo_score):
                            # add to list of good combos and move to next combo
                            valid_combinations.append(combo)
                            break 
                
    return filter_unique_tuples(sorted(set(valid_combinations), key=len)) #return combos that don't contain any of the previous combos

#Finds every combination of types that hits every  type for super effective
def offensive_strict_min_covers(df):
    # Store combinations that meet criteria
    valid_combinations = []
    types = mc.type_list  # Get all types from the DataFrame columns

    # Generate all combinations for the given types
    for r in range(2, len(types) + 1):  # Start from 2 to include all types

        #go over all combos
        for combo in combinations(types, r):

            #make a list of 1s with length of all types
            combo_score = [0 for i in range(len(mc.type_chart_def.columns.tolist()))]

            # Check if this combo can get everything super effectivley
            for type in combo:
                    
                    #get onehot list for type
                    type_scores = onehot_offense_strict(type)
                    
                    #multiply by each type score.
                    for i in range(len(combo_score)):
                        if type_scores[i] == 1:
                            combo_score[i] = 1

                        #this is boolean algebra. If everything is a 1, then we are done. 
                        if sum(combo_score)==len(combo_score):
                            # add to list of good combos and move to next combo
                            valid_combinations.append(combo)
                            break 
                
    return filter_unique_tuples(sorted(set(valid_combinations), key=len)) #return combos that don't contain any of the previous combos

#Finds every combination of types that resists or is immune to every type
def defensive_min_covers(df):
    # Store combinations that meet criteria
    valid_combinations = []
    types = mc.type_list  # Get all types from the DataFrame columns

    # Generate all combinations for the given types
    for r in range(2, len(types) + 1):  # Start from 2 to include all types

        #go over all combos
        for combo in combinations(types, r):

            #make a list of 1s with length of all types
            combo_score = [0 for i in range(len(mc.type_chart_def.columns.tolist()))]

            # Check if this combo can get everything super effectivley
            for type in combo:
                    
                    #get onehot list for type
                    type_scores = onehot_defense(type)
                    
                    #multiply by each type score.
                    for i in range(len(combo_score)):
                        if type_scores[i] == 1:
                            combo_score[i] = 1

                        #this is boolean algebra. If everything is a 1, then we are done. 
                        if sum(combo_score)==len(combo_score):
                            # add to list of good combos and move to next combo
                            valid_combinations.append(combo)
                            break 
                
    return filter_unique_tuples(sorted(set(valid_combinations), key=len)) #return combos that don't contain any of the previous combos


#Everything below is for calculating the solutions the files that are already in the type_min_spans folder. Uncomment if you need to run locally for some reason but otherwise the below makes importing this file annoying. 

#find all three min spans: offensive_relaxed, offensive_strict, and defensive min spans, then write them to file.

# offensive_relaxed = offensive_relaxed_min_covers(mc.type_chart_atk)

# with open('type_min_spans/offensive_relaxed.txt', 'w') as file:
#     for sublist in offensive_relaxed:
#         # Joining each element of the sublist with a space and writing it to the file
#         file.write(', '.join(sublist) + '\n')
        
# print("offensive_relaxed!")

# offensive_strict = offensive_strict_min_covers(mc.type_chart_atk)

# with open('type_min_spans/offensive_strict.txt', 'w') as file:
#     for sublist in offensive_strict:
#         # Joining each element of the sublist with a space and writing it to the file
#         file.write(', '.join(sublist) + '\n')

# print("offensive_strict!")

# defensive = defensive_min_covers(mc.type_chart_def)

# with open('type_min_spans/defensive.txt', 'w') as file:
#     for sublist in defensive:
#         # Joining each element of the sublist with a comma and writing it to the file
#         file.write(', '.join(sublist) + '\n')

# print("defensive!")
