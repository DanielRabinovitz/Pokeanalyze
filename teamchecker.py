import tieraggregator as ta
import matchup_calcs as mc
from pokedex import Pokedex
import type_min_spans as tp
from pprint import pprint

#takes in a tier name and a list of pokemon names as strings
#Tells you what the average offense and defense scores of your pokemon are in comparison with the tier averages, and if you're missing any type matchups.
def teamcheck(tier, pokemon_names):

    #get the tier average
    avg = ta.tier_avg(tier)

    #placeholders to calc things later
    sum_offense = 0
    sum_defense = 0
    team_types = []

    for poke in pokemon_names:

        #update sums
        scores = mc.poke_vs_tier(poke, tier)
        sum_offense += scores['Avg_Offense']
        sum_defense += scores['Avg_Defense']

        #
        for type in Pokedex().poke_by_name(poke)['types']:
            team_types.append(type)
    
    #make the team scores
    team_scores = {'Team_Offense': round(sum_offense/len(pokemon_names),2),
                   'Team_Defense': round(sum_defense/len(pokemon_names),2)}
    
    #lists to store type chart data. We want the lists to be full of ones at the end.
    offensive_coverage = [0 for i in range(len(mc.type_chart_def.columns.tolist()))]
    defensive_coverage = [0 for i in range(len(mc.type_chart_def.columns.tolist()))]

    #actually calculate the type chart scores
    for type in team_types:

        #get onehot list for type. 
        type_off = tp.onehot_offense_relaxed(type)
        type_def = tp.onehot_defense(type)
                    
        #update the lists above to reflect each type score
        for i in range(len(type_off)):
            
            if type_off[i] == 1:
                offensive_coverage[i] = 1

            if type_def[i] == 1:
                defensive_coverage[i] = 1

    #variables to tell you if your team has good offensive and defensive type matchups
    off_covered = False
    def_covered = False
    missing_off = []
    missing_def = []

    #if all types are covered, set to true. Otherwise find the list of missing types.
    if sum(offensive_coverage) == len(offensive_coverage):
        off_covered = True
    else:
        for i in range(len(type_off)):
            if offensive_coverage[i] == 0:
                new_type = mc.index_to_type[i]
                missing_off.append(new_type)

    if sum(defensive_coverage) == len(defensive_coverage):
        def_covered = True
    else:
        for i in range(len(type_def)):
            if defensive_coverage[i] == 0:
                new_type = mc.index_to_type[i]
                missing_def.append(new_type)

    #variables for how much higher/lower your team is offensive and defensivley as a percentage
    off_percent = 100*(round(team_scores['Team_Offense']/avg['Avg_Offense'], 2))
    def_percent = 100*(round(team_scores['Team_Defense']/avg['Avg_Defense'], 2))

    off_percent_high = False
    def_percent_low = False

    if off_percent >= 100:
        off_percent_high = True

    if def_percent <= 100:
        def_percent_low = True

    #helper functions for the feedback portion, returns a string with the % difference between your score and the average score.
    def off_diff():
        diff = off_percent - 100
        if diff >= 0:
            return f'{diff}% more'
        if diff < 0:
            return f'{diff * -1}% less'

    def def_diff():
        diff = def_percent - 100
        if diff >= 1:
            return f'{diff}% more'
        if diff < 1:
            return f'{diff * -1}% less'

    print(f'''Your Team Offense:{team_scores['Team_Offense']} 
{tier} Average Offense: {avg['Avg_Offense']}
Your team deals {off_diff()} damage than average. \n''')
    
    if(off_percent >= 100):
        print('Your team is above average offensivley!\n')
    else:
        print('Your team is not above average offensivley.\n')
    
    print(f'''Your Team Defense:{team_scores['Team_Defense']} 
{tier} Average Defense: {avg['Avg_Defense']}
Your team takes {def_diff()} damage than average.\n''')

    if(def_percent <= 100):
        print('Your team is above average defensivley!\n')
    else:
        print('Your team is not above average defensivley.\n')

    if off_covered == False:
        print('You cannot hit these types for at minimum neutral damage:', missing_off)
    else:
        print('You can hit every type for neutral or super effective damage!')

    if def_covered == False:
        print('You cannot switch into these types safely:', missing_def,'\n')
    else:
        print(f'You can switch into and safely resist any type!\n')


    if(off_covered and def_covered and off_percent >= 100 and def_percent <= 100):
        print('Your team is prepared for any type matchup,\nand your pokemon match up well both offensivley and defensivley into the tier.\nCongratulations, your team is very well rounded!')
    elif(off_covered and off_percent >= 100 and def_percent <= 100):
        print('Your team is prepared for any offensive type matchup and uses good pokemon,\nbut you have a hole in your defenses.\nFind pokemon that patch up your exposed type weakness.')
    elif(def_covered and off_percent >= 100 and def_percent <= 100):
        print('Your team is prepared for any defensive type matchup and uses good pokemon,\nbut some types can completley wall your team.\nFind pokemon that patch up your offensive type weakness.')
    elif(off_covered and def_covered and def_percent <= 100):
        print('Your team is prepared for any type matchup,\nand your pokemon match up well defensivley into the tier.\nUnless you are running a stall team, your team could use more offensive pokemon.')
    elif(off_covered and def_covered and off_percent >= 100):
        print('Your team is prepared for any type matchup,\nand your pokemon match up well offensivley into the tier.\nUnless you are running a hyper offense team, your team could use more defensive pokemon.')
    elif(off_covered and def_covered):
        print('Your team is prepared for any type matchup,\nbut your pokemon do not match up well into the tier. Focus on pokemon with better stats.')    
    else:
        print('Your team may be incomplete, or your team aims for a specific gimmick. \nFocus on using pokemon with stats and typings that better match the metagame\nand making sure that the types on your team are well rounded.')

