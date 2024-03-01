from pokedex import Pokedex
from pprint import pprint

dex = Pokedex().full_dex()

tiers = ['OU','UU','RU','NU', 'PU']

stat_sum = {'hp': 0,
            'atk': 0,
            'def': 0,
            'spa': 0,
            'spd': 0,
            'spe': 0,}
count = 0

for poke_name in dex:

    poke = dex[poke_name]

    #get is a dict method that gets the elements if the key exists
    if(poke.get('tier') in tiers):
        stat_sum['hp'] += poke['baseStats']['hp']
        stat_sum['atk'] += poke['baseStats']['atk']
        stat_sum['def'] += poke['baseStats']['def']
        stat_sum['spa'] += poke['baseStats']['spa']
        stat_sum['spd'] += poke['baseStats']['spd']
        stat_sum['spe'] += poke['baseStats']['spe']

        count += 1

stat_avgs = {'avg_hp' : round(stat_sum['hp']/count, 2),
             'avg_atk': round(stat_sum['atk']/count, 2),
             'avg_def': round(stat_sum['def']/count, 2),
             'avg_spa': round(stat_sum['spa']/count, 2),
             'avg_spd': round(stat_sum['spd']/count, 2),
             'avg_spe': round(stat_sum['spe']/count, 2),}

pprint(stat_avgs)