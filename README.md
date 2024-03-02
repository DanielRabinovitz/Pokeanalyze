This repository contains a 6v6 smogon singles team builder that tells you how to improve your team in any of the tiers of standard play.

You can publicly run the notebook that explains how everything works here, just hit "Run All" at the top.
https://colab.research.google.com/drive/1IFFcgsD3BpoA9wnxhfJRbKU1oQW1nndA?usp=sharing

If you just want to use the team builder, use this notebook. 
Run the first two blocks at the top for setup and then change the tier and pokemon list to test your team!
https://colab.research.google.com/drive/1yi3F3KBEfB5u037KjaR4pxQtbUvjlfqN?usp=sharing

Here's a quick breakdown of all the files used:

- pokedex.py makes a Pokedex class so that you can easily get information from the showdown API.
- matchup_calcs.py does all the low level math for calculating 1v1 matchups or the avg matchup a single pokemon has against a given tier. 
This includes stuff like type matchup scores and adjustments based on stats. The logic for the formulas is explained in the 1st notebook linked above.
- type_min_spans.py has utilities for converting between onehot vectors to represent type matchups, as well as functions to calculate the minimum sets
of types required to have a resistance to everything, to hit everything for neutral or better damage, and to hit everything for super effective damage.
- The type_min_spans folder contains the .txt files containing the sets calculated in type_min_spans.py. Those deserve a whole video on their own.
- tier_aggregtor.py lets you get the average performance of one tier vs another tier, e.g. the average of matchups of UU pokemon vs OU pokemon.
It also has a function for getting the average matchup of all pokemon inside of their own tier.
- avgstats.py is a file that just calculates the average of each stat across all tiers. 
It's not used anywhere in the rest of the code and was just me testing a summary statistic.
- teamchecker.py is the final team builder. It takes in a tier and a list of pokemon names, and then it prints feedback based on your team to the console. 


