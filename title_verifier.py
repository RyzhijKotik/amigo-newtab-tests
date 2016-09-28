# This Python file uses the following encoding: utf-8
__author__ = 'RyzhijKotik'

"""
Verify if the title of chrome://newtab as expected in .prop file (default is "Пульт")
"""


def newtabTitle(expected_title, amigo):
    """
    :param expected_title: title from page_title_is_pult.prop (default is "Пульт")
    :param amigo: AmigoDriver object
    """

    assert expected_title == amigo.title, \
        ('Page title is %s; Expected title is %s' %(amigo.title, expected_title)) if True else \
            ('Page title is %s; Expected title is %s' %(amigo.title, expected_title))
