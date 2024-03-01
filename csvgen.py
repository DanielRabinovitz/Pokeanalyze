import matchup_calcs as mc
from pokedex import Pokedex
from pprint import pprint

dex = Pokedex()

#dict for each tier
# pokesOU = dex.filter_by_tier("OU")
# pokesUU = dex.filter_by_tier("UU")
# pokesRU = dex.filter_by_tier("RU")
# pokesNU = dex.filter_by_tier("NU")
# pokesPU = dex.filter_by_tier("PU")

#takes in two tier names and spits out the json for avg matchups of every pokemon in one tier vs every pokemon in other
#e.g. tier_vs_tier("UU", "OU") gets a dict of the avg matchup of each UU mon into each OU mon
def tier_vs_tier(tier1, tier2):

    #get pokes to iterate over
    pokes = dex.filter_by_tier(tier1)

    #get matchup vs tier
    matchups = [mc.poke_vs_tier(poke, tier2) for poke in pokes]

    return matchups

pprint(tier_vs_tier("OU", "OU"))
# pprint(mc.poke_vs_tier("moltres", "OU"))
# pprint(mc.poke_vs_tier("keldeo", "OU"))






