__author__ = 'RyzhijKotik'

from selenium.webdriver.common.action_chains import ActionChains

"""
Make an action from the actions dictionary: open, close, click element, hover element etc.
"""

def runCommand(command, amigo):
    if command == 'open':
        pass
        #amigo.amigoOpen()
    elif command == 'close':
       # amigo.amigoClose()
        pass
    elif command[:5:] == 'click':
        xpath = command[6::]
        elem = amigo.find_element_by_xpath(xpath)
        elem.click()
    elif command[:5:] == 'hover':
        xpath = command[6::]
        elem = amigo.find_element_by_xpath(xpath)
        hover = ActionChains(amigo).move_to_element(elem)
        hover.perform()
    else:
        raise (Exception('Unknown command %s' % command))