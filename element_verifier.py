__author__ = 'RyzhijKotik'

"""
Trying to find an element by xpath from the .prop file at the NewTabPage
If element doesn't exist we through assertation error
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException


def elementVerifier(elements, amigo):
  """
    :param elements: dictionary of expected elements from .prop files
    :param amigo: AmigoDriver() object
    """
  for element in elements:
    try:
      WebDriverWait(amigo.amigo, 3). \
        until(EC.presence_of_element_located((By.XPATH, elements[element].encode('cp1251').decode('utf-8'))))
    except(TimeoutException):
      return element


