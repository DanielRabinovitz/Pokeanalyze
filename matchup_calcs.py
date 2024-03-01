from pokedex import Pokedex
import pandas
from pprint import pprint

dex = Pokedex()
ou = dex.filter_by_tier("OU")

#csv of the type matchups
#returns matchup of type_chart[attacking_type][defending_type]
#E.g. type_chart['Water']['Fire'] = 2.0
type_chart_def = pandas.read_csv('typechart.csv')
type_chart_def.set_index('Attacking', inplace=True)
type_chart_atk = type_chart_def.T

type_list = type_chart_def.columns.tolist()

"""
Takes in a pokemon name and a tier name to calculate the pokemon's type matchups against every pokemon in the tier

Logic for matchups:
    1) Calculate the score for each type seperatley (if monotype, treat it as if it has the same type twice), then add the two scores and divide by 2 to average. The scale is the same for offense and defense, with offense wanting a higher score and defense wanting a lower score. If the score = 1, multiply by 1*2 to adjust for the fact that neutral switchins are still at a disadvantage unless they are pretty bulky
    2) Matchup scale:
        -Immunity = 0
        -Quad resist = 0.25
        -Resist = 0.5
        -Neutral = 1
        -Super effective = 2
        -Quad effective = 4
    3) E.g.
        Tusk [Ground, Fighting] vs Dhengo [Ghost, Steel]
            -Offensive score (calced as Tusk attacking Dhengo):
                Ground -> [Steel, Ghost] = 2
                Fighting -> [Steel, Ghost] = 0
                Avg: (2+0)/2 = 1.
            -Defensive score (calced as Dhengo attacking Tusk):
                Ghost -> [Ground, Fighting] = 1
                Steel -> [Ground, Fighting] = 1
                Avg: (1+1)/2 = 1.
"""

#given an attacking (atk) type and a defending (df) type, return the damage multiplier of the attacker to the defender
#E.g. type_lookup_atk('Water', 'Fire')=2.0
def type_lookup_atk(atk, df):
    return type_chart_atk[atk][df]

#given a defending (df) type and an attacking (atk) type, return the damage multiplier of the defender against the attacker
#E.g. type_lookup_de('Water', 'Fire')=0.5
def type_lookup_def(df, atk):
    return type_chart_def[df][atk]

#attacker takes in one type, defender takes in 1 or 2 types as a list.
#returns offensive multiplier of the attacker into the defending types
def offensive_mult(attacker, defender):

    #if monotype on the defensive end, treat as having the same type twice
    if len(defender) == 1:
        score = type_lookup_atk(attacker, defender[0])
        return score
    elif isinstance(defender, str):
        score = type_lookup_atk(attacker, defender)
        return score
    elif len(defender) == 2:
        #multiply the defensive types together.
        score1 = type_lookup_def(defender[0], attacker) 
        score2 = type_lookup_def(defender[1], attacker)
        return score1*score2
    
def defensive_mult(defender, attacker):

    #if monotype on the defensive end, treat as having the same type twice
    if len(defender) == 1:
        score = type_lookup_def(defender[0], attacker)
        return score
    elif isinstance(defender, str):
        score = type_lookup_def(defender, attacker)
        return score
    elif len(defender) == 2:
        #multiply the defensive types together.
        score1 = type_lookup_def(defender[0], attacker) 
        score2 = type_lookup_def(defender[1], attacker)
        return score1*score2

###TO USE LATER###

#takes in the type list of a target pokemon and an opponent pokemon, then returns the type scores that the target has vs the opponent based on the logic in the huge block comment above
#both inputs are always lists!
def type_scores(t_poke, o_poke):
    # Initialize scores
    offscore = 0
    defscore = 0

    # Both are dual-type
    if len(t_poke) == 2 and len(o_poke) == 2:
        offscore = (offensive_mult(t_poke[0], o_poke) + offensive_mult(t_poke[1], o_poke)) / 2
        defscore = (defensive_mult(t_poke, o_poke[0]) + defensive_mult(t_poke, o_poke[1])) / 2

    # t_poke is single-type, o_poke is dual-type
    elif len(t_poke) == 1 and len(o_poke) == 2:
        offscore = offensive_mult(t_poke[0], o_poke)
        defscore = (defensive_mult(t_poke, o_poke[0]) + defensive_mult(t_poke, o_poke[1])) / 2

    # t_poke is dual-type, o_poke is single-type
    elif len(t_poke) == 2 and len(o_poke) == 1:
        offscore = (offensive_mult(t_poke[0], o_poke) + offensive_mult(t_poke[1], o_poke)) / 2
        defscore = defensive_mult(t_poke, o_poke[0])

    # Both are single-type
    else:
        offscore = offensive_mult(t_poke[0], o_poke)
        defscore = defensive_mult(t_poke, o_poke[0])

    return {'Offense': round(offscore, 2), 'Defense': round(defscore, 2)}

#takes in two pokemon objects as a target poke and an opponent poke and calcs the offensive and defensive matchups
def score_1v1(t_poke, o_poke):

    t_types = t_poke['types']
    o_types = o_poke['types']

    scores = type_scores(t_types, o_types)

    #adjust defscore for raw type matchup for stats

    # Constants for formulas
    o_atk = o_poke['baseStats']['atk']
    o_spa = o_poke['baseStats']['spa']
    o_def = o_poke['baseStats']['def']
    o_spd = o_poke['baseStats']['spd']
    o_spe = o_poke['baseStats']['spe']
    o_hp = o_poke['baseStats']['hp']
    t_atk = t_poke['baseStats']['atk']
    t_spa = t_poke['baseStats']['spa']
    t_def = t_poke['baseStats']['def']
    t_spd = t_poke['baseStats']['spd']
    t_spe = t_poke['baseStats']['spe']
    t_hp = t_poke['baseStats']['hp']

    #Adjust defscore for stats

    #I use the constant 86.2 because that's the avg hp of all pokes in OU to PU
    #I divide by the avg hp to weight the defensive poke's score. If their base HP is higher than 86.2, hp/86.2 this will lower the score, indicating lower expected damage to their overall HP pool. If their base HP is lower than 86.2, hp/86.2 will raise the def score indicating that they are expected take a higher portion of their hp pool

    # if o_poke is a physical attacker 
    if o_atk > o_spa:
        # Defense score = score * o_poke's atk / t_poke's defense
        scores['Defense'] = scores['Defense'] * o_atk / t_def / (t_hp/86.2)

    # if o_poke is a special attacker
    elif o_atk < o_spa:
        # Defense score = score * o_poke's spatk / t_poke's spdef
        scores['Defense'] = scores['Defense'] * o_spa / t_spd / (t_hp/86.2)

    # if the two stats are the same, average the score for a special attacker and a physical attacker.
    else:
        score_atk = scores['Defense'] * o_atk / t_def / (t_hp/86.2)
        score_spa = scores['Defense'] * o_spa / t_spd / (t_hp/86.2)
        scores['Defense'] = (score_atk+score_spa)/2

    # Adjust offscore for stats
    # if t_poke is a physical attacker 
    if t_atk > t_spa:
        # Offense score = score * t_poke's atk / o_poke's defense
        scores['Offense'] = scores['Offense'] * t_atk / o_def  / (o_hp/86.2)

    # if t_poke is a special attacker
    elif t_atk < t_spa:
        # Offense score = score * t_poke's spatk / o_poke's spdef
        scores['Offense'] = scores['Offense'] * t_spa / o_spd / (o_hp/86.2)

    # if the two stats are the same, average the ratios.
    else:
        score_atk = scores['Offense'] * t_atk / o_def / (o_hp/86.2)
        score_spa = scores['Offense'] * t_spa / o_spd / (o_hp/86.2)
        scores['Offense'] = (score_atk+score_spa)/2

    #round scores to 2 decimal points
    scores['Offense'] = round(scores['Offense'], 2)
    scores['Defense'] = round(scores['Defense'], 2)

    return scores

#wrapped for score_1v1 that takes in two pokemon names
def score_1v1_names(name1, name2):

    poke1 = dex.poke_by_name(name1)
    poke2 = dex.poke_by_name(name2)

    return score_1v1(poke1, poke2)


#takes in a poke and a tier, then finds the scores for the poke vs the entire tier
def score_vs_tier(poke, tier):
    
    tier_pokes = dex.filter_by_tier(tier)

    scores = {}

    for opponent in tier_pokes:
        scores[tier_pokes[opponent]['name']] = score_1v1(poke, tier_pokes[opponent])
    
    return scores

#prints the avg matchups for a poke
def avg_matchups(match_dict):

    total_defense = 0
    total_offense = 0

    for scores in match_dict.values():
        total_defense += scores['Defense']
        total_offense += scores['Offense']

    # Calculate averages
    average_defense = total_defense / len(match_dict)
    average_offense = total_offense / len(match_dict)

    return {'Avg_Defense': round(average_defense, 2),
            'Avg_Offense': round(average_offense, 2)}

#wrapper for the above two that only needs the name and tier strings and includes the poke's name in the final dick
def poke_vs_tier(poke_name, tier):

    poke = dex.poke_by_name(poke_name)

    avgs = avg_matchups(score_vs_tier(poke, tier))

    scores = {'Pokemon_Name': poke_name,
              'Tier_Compared_To': tier,
              'Avg_Defense': avgs['Avg_Defense'],
              'Avg_Offense': avgs['Avg_Offense']}
    
    return scores

#alt version for the above where you can directly pass in a poke object
def pokeObj_vs_tier(poke, tier):

    avgs = avg_matchups(score_vs_tier(poke, tier))

    scores = {'Pokemon_Name': poke['name'],
              'Tier_Compared_To': tier,
              'Avg_Defense': avgs['Avg_Defense'],
              'Avg_Offense': avgs['Avg_Offense']}
    
    return scores






