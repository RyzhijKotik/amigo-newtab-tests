__author__ = 'RyzhijKotik'

"""
Make an action from the actions dictionary: open, close, click element, hover element etc.
"""

def runCommand(command, amigo):
    if command == 'open':
        amigo.amigoOpen()
    elif command == 'close':
        amigo.amigoClose()
    elif command[:5:] == 'click':
        amigo.clickElement(command[6::])
    elif command[:5:] == 'hover':
        amigo.hoverElement(command[6::])
    else:
        raise (Exception('Unknown command %s' % command))