#!/usr/bin/env python

import apps.katello

class Home(apps.katello.KatelloPage):

    def __init__(self, **kwargs):
        apps.katello.KatelloPage.__init__(self, **kwargs)
        self.go_to_home_page()

    def click_notification_close(self):
        self.click(*self.locators.close_notification_locator)
