class Conversions():
    '''
    We're going to use grams as the base unit for everything here.
    To get an amount dispensed, we first convert it to a weight if it's
    a volume, and then to grams to get the final amount we actually want
    '''

    MASS = {'g': 1.0, 'kg': 1000.0, 'lb': 453.592, 'oz': 28.3495}
    # the base unit for volumes will be 'ml', which we'll convert back
    # to weights using the density of the foods
    VOLUMES = {'ml': 1.0, 'cups': 240, 'pint': 472.176, 'quart': 946.353,
               'fl-oz': 29.5735, 'tbls': 14.7868}
    # testing densities
    DENSITIES = {'rice': 200.0, 'flour': 300.0, 'candy': 250.0}

    def __init__(self):
        # nothing to actually do here
        pass
