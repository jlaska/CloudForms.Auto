#!/usr/bin/env python

import apps.katello

class Dashboard(apps.katello.KatelloPage):

    def __init__(self, **kwargs):
        kwargs['open_url'] = False # don't reload this page
        apps.BasePage.__init__(self, **kwargs)

    @property
    def is_dashboard_tab_selected(self):
        return self.selenium.find_element(*self.locators.dashboard_tab_active_locator).is_displayed()

    @property
    def is_dashboard_dropbutton_present(self):
        return self.is_element_present(*self.locators.dashboard_dropbutton_locator)

    @property
    def is_dashboard_subscriptions_present(self):
        return self.is_element_present(*self.locators.dashboard_subscriptions_locator)

    @property
    def is_dashboard_notifications_present(self):
        return self.is_element_present(*self.locators.dashboard_nofications_locator)
