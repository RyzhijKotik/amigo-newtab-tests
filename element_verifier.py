__author__ = 'RyzhijKotik'

"""
Trying to find an element by xpath from the .prop file at the NewTabPage
If element doesn't exist we through assertation error
"""

def elementVerifier(elements, amigo):
    """
    :param elements: dictionary of expected elements from .prop files
    :param amigo: AmigoDriver() object
    """
    for element in elements:
        amigo.findElement(elements[element].encode('cp1251').decode('utf-8'), element)









