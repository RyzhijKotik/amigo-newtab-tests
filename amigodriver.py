__author__ = 'RyzhijKotik'

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
import amigodriver_wait


class AmigoDriver:

    """Launch Amigo Browser using chromedriver with options: path to amigo.exe, path to newtab.crx
    """

    def __init__(self, binary_path, crx_path):
        """
        Setting ChromeDriver options
        :param binary_path: path to amigo.exe
        :param crx_path: path to newtab.crx (url)
        """
        self.options = webdriver.ChromeOptions()
        self.options.binary_location = binary_path
        self.options.add_extension(crx_path)

    def amigoOpen(self):
        """
         Opens chrome://newtab as a webpage in Amigo
        """
        self.amigo = webdriver.Chrome(chrome_options=self.options)
        self.amigo.get("chrome://newtab")

    def amigoClose(self):
        """
        close Amigo, quit chromedriver
        """
        self.amigo.close()

    def getTitle(self):
        """
        Get the title of opened page (default is "Пульт")
        :return: page title
        """
        return self.amigo.title

    def findElement(self, xpath, element_name):
        """
        Looking if the element from .prop file is visible at NewTabPage
        Timeout=10 sec is given to wait for NewTab page loading
        :param xpath: selenium xpath to element (see onboarding_is_shown.prop for example)
        :param element_name: name of element from .prop file, used only in timeout error message
        """
        element_visibility = expected_conditions.visibility_of_element_located((By.XPATH, xpath))
        timeout_message = "Can not find element " + element_name + " - Xpath " + xpath
        amigodriver_wait.AmigoDriverWait(self.amigo, timeout=5, poll_frequency=0.5).\
            until(element_visibility, element_name, timeout_message)

    def clickElement(self, xpath):
        """
        Emulate mouse click at the element
        """
        elem = self.amigo.find_element_by_xpath(xpath)
        elem.click()

    def hoverElement(self, xpath):
        """
        Emulate mouse hover at the element
        """
        elem = self.amigo.find_element_by_xpath(xpath)
        hover = ActionChains(self.amigo).move_to_element(elem)
        hover.perform()