#!/Users/dan/anaconda3/bin/python
### Additional functions are here to keep the main notebook readable. ###
from smact import metals
from pymatgen import Composition

metaloxides = metals + ['As', 'P', 'O']
common_complex = ['NO3','NO2', 'PO2','PO3','PO4','PO5', 'SO4','SO3','SO2', 'CO3']

def metal_oxide_filter(formula):
    ''' Takes a formula and returns whether it is a metal oxide or not
        i.e. no other anions or non-metals allowed.
    Args: formula (str): Chemical formula
    Returns: metal_ox (bool): Whether the formula is a metal oxide.
    '''
    els = Composition(formula).elements
    if not any(el.symbol == 'O' for el in els):
        return False
    elif all(el.symbol in metaloxides for el in els):
        return True
    else:
        return False

# Function to filter for "proper oxides"
def proper_oxides(df, metal_oxides_only=False, filter_complex=True,
                  verbose=False, additional_patterns=[] , specific_formulas=[]):
    ''' Args:
            df (pandas.DataFrame): Dataframe to filter.
            metal_oxides_only (bool): If true, no other non-metals are allowed in the formula.
                Automatically includes the rules applied by filter_complex.
            filter_complex (bool): Filter out common complex anions such as nitrates, sulfates..
            additional_patterns(list): Additional patterns (strings) that may appear anywhere in
                chemical formulas to also filter out.
            specific_formulas (list): Specific chemical formulas (strings) to filter out.
        Returns:
            df (pandas.DataFrame): Dataframe with materials removed according to the above
                criteria.
    '''

    common_complex = ['NO3','NO2',
                         'PO2','PO3','PO4','PO5',
                         'SO4','SO3','SO2',
                         'CO3']
    if metal_oxides_only:
        print('Oxygen only: No other non-metals are being allowed!')
        df['metal_oxide'] = df.apply(lambda x: metal_oxide_filter(x['formula']), axis=1)
        df = df.loc[df['metal_oxide'] == True]
        df = df.drop(['metal_oxide'], axis = 1)
        print('==> After restricting to metal oxides only: {0}'.format(len(df)))

    # Iteratively remove rows containing the patterns of complex anions
    removed_complex = []
    if filter_complex:
        for pattern in common_complex:
            removed_complex += (list(df[df.formula.str.contains(pattern)].formula))
            df = df[~df.formula.str.contains(pattern)]
        print('==> After removing common O-containing anions: {0}'.format(len(df)))
        if verbose:
            print('removed:  {0}'.format(removed_complex))

    # Remove additional patterns and formulas
    removed_add = []
    if additional_patterns:
        for pattern in additional_patterns:
            removed_add += (list(df[df.formula.str.contains(pattern)].formula))
            df = df[~df.formula.str.contains(pattern)]
        print('==> After removing additional patterns in formulas: {0}'.format(len(df)))
        if verbose:
            print('removed:  {0}'.format(removed_add))

    if specific_formulas:
        removed_forms = list(df[df['formula'].isin(specific_formulas)].formula)
        df = df[~df['formula'].isin(specific_formulas)]
        print('==> After removing additional specific formulas: {0}'.format(len(df)))
        if verbose:
            print('removed:  {0}'.format(removed_forms))

    return(df)
