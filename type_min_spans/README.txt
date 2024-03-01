The docs in this folder are the smallest possible lists of types that satisfy specific criteria. The lists are assuming that all pokemon involved are monotype, because otherwise these would be *really* difficult to calculate.


Defensive:

    defensive.txt is the combinations of types that can switch in at least one pokemon to an attack of any given type and have the switch in resist or be immune to the attack.

    Example defensive type: Bug, Dragon, Dark, Steel
    This combination of types holds at least one resistance to every type.

Offensive:

    There are two here, to satisfy different criteria.

        offensive_relaxed.txt is the combinations of types necessary to hit any monotype pokemon in the game for neutral damage.

        E.g. Ice, Ground
        No team of monotype pokemon can resists both Ice and Ground at the same time.

        offensive_strict.txt is the combinations of types necessary to hit every type in the game for super effective damage.

        E.g. Grass, Ice, Fighting, Ground, Flying, Dark, Steel
        No team of monotype pokemon can switch into all of these attackin types without taking super effective damage.

