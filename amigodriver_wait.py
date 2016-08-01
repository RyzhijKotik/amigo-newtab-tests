__author__ = 'RyzhijKotik'

"""
AmigoDriverWait inherits WebDriverWait to override method until:
'screen' param was added to TimeoutException calling to enable making screenshots of pages, where test fails
"""
import os
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException


IGNORED_EXCEPTIONS = (NoSuchElementException,)  # exceptions ignored during calls to the method


class AmigoDriverWait(WebDriverWait):

    def __init__(self, amigo, timeout, poll_frequency, ignored_exceptions=None):
        super(WebDriverWait, self).__init__()
        self._amigo = amigo
        self._timeout = timeout
        self._poll = poll_frequency
        self._ignored_exceptions = ignored_exceptions
        exceptions = list(IGNORED_EXCEPTIONS)
        if ignored_exceptions is not None:
            try:
                exceptions.extend(iter(ignored_exceptions))
            except TypeError:  # ignored_exceptions is not iterable
                exceptions.append(ignored_exceptions)
        self._ignored_exceptions = tuple(exceptions)

    def until(self, method, element_name, message=''):
        """Calls the method provided with the driver as an argument until the \
        return value is not False.
        Overridden from WebDriverWait: screen param was added to TimeoutException calling
        to enable making screenshots of pages, where test fails
        screenshots are put to 'screenshot' directory
        if directory doesn't exist it would be created in the current directory
        """
        stacktrace = None
        end_time = time.time() + self._timeout
        while True:
            try:
                value = method(self._amigo)
                if value:
                    return value
            except self._ignored_exceptions as exc:
                getattr(exc, 'screen', None)
                stacktrace = getattr(exc, 'stacktrace', None)
            time.sleep(self._poll)
            if time.time() > end_time:
                break
        if not os.path.exists("screenshots\\"):
           os.mkdir("screenshots\\")
        raise TimeoutException(message, self._amigo.save_screenshot("screenshots\\" + element_name + '.png'), stacktrace)