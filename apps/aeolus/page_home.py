#!/usr/bin/env python

import time
import apps.aeolus
from apps.aeolus.locators import *

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

username_text_field = (By.NAME, "login")
password_text_field = (By.ID, "password-input")
login_locator = (By.NAME, "commit")

class Home(apps.aeolus.ConductorPage):

    def __init__(self, **kwargs):
        '''
        Gets page ready for testing
        '''
        apps.aeolus.ConductorPage.__init__(self, **kwargs)

        if kwargs.get('open_url', True):
            self.selenium.get(self.base_url)

    @property
    def is_username_field_present(self):
        return self.is_element_present(*username_text_field)

    @property
    def is_password_field_present(self):
        return self.is_element_present(*password_text_field)

    def login(self, user="admin", password="password"):
        time.sleep(1)
        print "logging in now................."
        self.send_text(user, *username_text_field)
        self.send_text(password, *password_text_field)
        self.click(*login_locator)
        time.sleep(1)
