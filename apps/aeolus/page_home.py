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
        self.go_to_home_page()
