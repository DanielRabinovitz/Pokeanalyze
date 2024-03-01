import requests

#pokedex database API

#class for getting and storing the data with various getters
class Pokedex:
        
        #constructor
        def __init__(self):
                #get data from showdown
                url = r'https://play.pokemonshowdown.com/data/pokedex.json'
                response = requests.get(url)        

                #store it as a python dict
                if response.status_code == 200:
                    self.dex = response.json()
                else:
                    self.dex = {}
                    print(f"Failed to retrieve data from {url}")
        
        #get all mons
        def full_dex(self):
             return self.dex
        
        #get the JSON for a specific mon
        def poke_by_name(self, name):
            """Return a Pokémon's data by its name."""
            # Directly access the Pokémon by name if it exists in the data
            return self.dex.get(name.lower(), None)
        
        #get all mons with a particular type
        def filter_by_type(self, pokemon_type):
            """Return a dictionary of Pokémon of a specific type."""
            return {name: details for name, details in self.dex.items() if pokemon_type.lower() in [t.lower() for t in details['types']]}
        
        #get all mons in a particular tier
        def filter_by_tier(self, tier):
            """Return a dictionary of Pokémon by a specific tier."""
            return {name: details for name, details in self.dex.items() if details.get('tier', '').lower() == tier.lower()}


#gets a list of all values in a specific field of a dictionary
#util method for parsing the output of any API searches
def field_listify(data, field_name):
    return [details[field_name] for details in data.values()]

