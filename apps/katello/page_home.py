#!/usr/bin/env python

import apps.katello

class Home(apps.katello.KatelloPage):

    def __init__(self, **kwargs):
        apps.katello.KatelloPage.__init__(self, **kwargs)
        self.go_to_home_page()

    @property
    def is_username_field_present(self):
        return self.is_element_present(*self.locators.username_text_field)

    @property
    def is_password_field_present(self):
        return self.is_element_present(*self.locators.password_text_field)

    @property
    def is_login_button_present(self):
        return self.is_element_present(*self.locators.login_locator)

    @property
    def is_login_logo_present(self):
        return self.is_element_present(*self.locators.login_card_logo)

    def login(self, user="admin", password="admin"):
        self.send_text(user, *self.locators.username_text_field)
        self.send_text(password, *self.locators.password_text_field)
        self.click(*self.locators.login_locator)

    def click_logout(self):
        self.click(*self.locators.logout_locator)

    def click_notification_close(self):
        self.click(*self.locators.close_notification_locator)
