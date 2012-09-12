import apps
import locators

class Conductor(apps.BaseProduct):
    '''Product class'''
    locators = locators.AeolusLocators()

class Conductor_Page(apps.BasePage):
    '''Page class'''

    def __init__(self, **kwargs):
        apps.BasePage.__init__(self, **kwargs)

