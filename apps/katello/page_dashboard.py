#!/usr/bin/env python

import apps.katello

class Dashboard(apps.katello.KatelloPage):

    @property
    def is_dashboard_dropbutton_present(self):
        return self.is_element_present(*self.locators.dashboard_dropbutton_locator)

    @property
    def is_dashboard_subscriptions_present(self):
        return self.is_element_present(*self.locators.dashboard_subscriptions_locator)

    @property
    def is_dashboard_notifications_present(self):
        return self.is_element_present(*self.locators.dashboard_nofications_locator)
