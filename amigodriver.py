# This Python file uses the following encoding: utf-8
__author__ = 'RyzhijKotik'

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains



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
        self.amigo.quit()

    def getTitle(self):
        """
        Get the title of opened page (default is "Пульт")
        :return: page title
        """
        return self.amigo.title

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
