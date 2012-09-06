#!/usr/bin/env python

import time
import apps.aeolus
from apps.aeolus.locators import *

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class Home(apps.aeolus.Conductor_Page):

    def __init__(self, **kwargs):
        '''
        Gets page ready for testing
        '''
        apps.aeolus.Conductor_Page.__init__(self, **kwargs)

        if kwargs.get('open_url', True):
            self.selenium.get(self.base_url)

    @property
    def is_username_field_present(self):
        return self.is_element_present(*self.locators.username_text_field)

    @property
    def is_password_field_present(self):
        return self.is_element_present(*self.locators.password_text_field)

    def login(self, user="admin", password="password"):
        self.send_text(user, *self.locators.username_text_field)
        self.send_text(password, *self.locators.password_text_field)
        self.click(*self.locators.login_locator)
