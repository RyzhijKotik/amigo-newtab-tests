__author__ = 'RyzhijKotik'

"""
Parses an entity from .prop file
Verifies that the current machine state matches a given state.
"""

import title_verifier
import element_verifier


def verifyState(state, amigo):
    """
    :param state: state from a .prop file
    :param amigo: AmigoDriver objext
    """
    for key in state:
        if key == 'Title':
            title_verifier.newtabTitle((state[key].encode('cp1251').decode('utf-8')), amigo)
        elif 'Elements' in key:
            element_verifier.elementVerifier(state[key], amigo)



