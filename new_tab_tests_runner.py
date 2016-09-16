__author__ = 'RyzhijKotik'

"""
Parsing args to get amigo binary file, crx file ant name of test to run
Parsing .config and .prop files to make states and actions dictionaries
Creating an AmigoDriver() object
Running tests from .config
"""

import sys
import os
import argparse
import amigodriver
import urllib
import urllib.request
import unittest
import json
import xmlrunner
import verifier_runner
import command_runner
import warnings
import time
from win32com.shell import shell, shellcon


class Config:
    """
    Describes the system states, actions and test cses from newtab.config
    states is a dictionary {key: sate name, value: property state}
    actions is a dictionary {key: action name, value: command}
    tests is an array of test cases
    """
    def __init__(self):
        self.states = {}
        self.actions = {}
        self.tests = []


class NewTabTest(unittest.TestCase):
    """
    Tests a test from testsuite in config file
    """
    def __init__(self, name, test, config, amigo):

        """
        :param name: The name of this test
        :param test: An array of alternating state names and action names
        :param config: The Config object.
        """
        super(NewTabTest, self).__init__()
        self._name = name
        self._test = test
        self._config = config
        self._amigo = amigo

    def tearDown(self):
        for method, error in self._outcome.errors:
            if error:
                self._amigo.amigo.save_screenshot("test-reports\\screenshot-failure-" + self._name + time.strftime("%Y%m%d%H%M%S") + ".png")
        self._amigo.amigoClose()

    def id(self):
        """Returns the name of the test.
        Overridden by Chromium authors from unittest.TestCase so that id() contains the name of the
        test case from the config file in place of the name of this class's test
        function.
        """
        return unittest.TestCase.id(self).replace(self._testMethodName, self._name)

    def runTest(self):
        """
        Runs a Test Case
        """
        self.assertEqual(1, len(self._test) % 2,
                     'The length of test array must be odd')

        for i in range(0, len(self._test), 2):
            """
            Going through tests array and filling the actions and states arrays.
            Actions are even 0, 2, 4 etc.
            States are odd 1, 2, 5 etc.
            """
            action = self._test[i]

            #Running an action from actions dictionary
            command_runner.runCommand(self._config.actions[action], self._amigo)

            #Verifies that the current machine state matches a given state.
            if i < len(self._test)-1:
                state = self._test[i+1]
                verifier_runner.verifyState(self._config.states[state], self._amigo)

def mergePropertyDictionaries(current_property, new_property):

    for key, value in iter(new_property.items()):
        if key not in current_property:
            current_property[key] = value
        else:
            warnings.warn("Property keys: \n%s\n%s\nhave the same names!\n"
                          "The first value will be ovewritten by the second!"
                          %(current_property, new_property))
            assert (isinstance(current_property[key], dict) and
                    isinstance(value, dict))
            # This merges two dictionaries together. In case there are keys with
            # the same name, the latter will override the former.
            new_dict = current_property[key].copy()
            new_dict.update(value)

def parsePropertyFiles(directory, filenames):
    """
    Parses an array of .prop files
    :param directory: directory of config file
    :param filenames: array of state names
    :return: dictionary of properties
    """
    property = {}
    for filename in filenames:
        path = os.path.join(directory, filename)
        new_property = json.load(open(path))
        mergePropertyDictionaries(property, new_property)
    return property


def parseConfigFile(filename):
    """
    Parses newtab.config
    :param full path to .config
    :return: Config object
    """
    if os.path.exists(filename):
        with open(filename, "r") as fp:
            config_data = json.load(fp)
        config = Config()
        config.tests = config_data['tests']
        directory = os.path.dirname(os.path.abspath(filename))
        for state_name, state_property_filenames in config_data['states']:
            config.states[state_name] = parsePropertyFiles(directory,
                                                           state_property_filenames)
        for action_name, action_command in config_data['actions']:
            config.actions[action_name] = action_command
    else:
        raise('Could not find a config file ' + filename)
    return config

def main():
    """
    Parses the arguments in script run configuration
    Mandatory arguments are config, binary-path (path to amigo.exe),
    crx-url (path to packed newtab.crx at service.amigo.mail.ru or ftp)
    """
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--binary-path', default="\\Amigo\\Application\\amigo.exe",
                           help="Path to Amigo Browser directory")
    argparser.add_argument('--crx-url',
                           help='Path to NewTab packed extension')
    argparser.add_argument('--config', metavar='FILENAME',
                           help='Path to test configuration file')
    argparser.add_argument('test', nargs='*',
                           help='Name(s) of test(s) to run')
    args = argparser.parse_args()

    if not args.config:
        argparser.error('missing mandatory --config FILENAME argument')

    local_appdata_path = shell.SHGetFolderPath(0, shellcon.CSIDL_LOCAL_APPDATA,
                                               None, 0)
    assert os.path.exists(local_appdata_path + args.binary_path), ('Could not find amigo.exe %s' %
                                               args.binary_path)
    crx_path = "C:\\newtab.crx"
    if args.crx_url:
        urllib.request.urlretrieve(args.crx_url, crx_path)
    else:
        raise AssertionError('newtab.crx url must be passed through arguments')

    assert os.path.exists(crx_path), ('Could not find newtab.exe %s' %
                                               crx_path)

    if not os.path.exists("test-reports\\"):
        os.mkdir("test-reports\\")
    suite = unittest.TestSuite()
    amigo = amigodriver.AmigoDriver(local_appdata_path + args.binary_path, crx_path)
    config = parseConfigFile(args.config)

    for test in config.tests:
        # If tests were specified via |tests|, their names are formatted like so:
        test_name = '%s.%s.%s' % (NewTabTest.__module__,
                                  NewTabTest.__name__,
                                  test['name'])
        if not args.test or test_name in args.test:
            suite.addTest(NewTabTest(test['name'], test['traversal'], config, amigo))

    xmlrunner.XMLTestRunner(output='test-reports').run(suite)

if __name__ == '__main__':
    sys.exit(main())