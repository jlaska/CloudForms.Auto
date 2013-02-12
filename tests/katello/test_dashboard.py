#!/usr/bin/env python

import pytest
import apps
import time
from tests.katello2 import Katello_Test

@pytest.mark.nondestructive
class TestDashboard(Katello_Test):

    def test_org_selection(self):
        """
        Verify dashboard page contains key elements.
        """
        home_page = self.load_page('Home')

        home_page.login()
        assert home_page.is_successful
        if pytest.config.getvalue('project-version') == '1.1':
            home_page.select_org(self.testsetup.org)
        assert home_page.is_dialog_cleared

        home_page.header.click_switcher()
        assert home_page.header.is_org_list_present

        home_page.header.select_org_from_switcher("ACME_Corporation")
        assert not home_page.header.is_org_list_present
        assert home_page.header.get_text_from_switcher == "ACME_Corporation"

    def test_dashboard_elements(self):
        """
        Verify dashboard page contains key elements.
        """
        home_page = self.load_page('Home')

        home_page.login()
        assert home_page.is_successful
        if pytest.config.getvalue('project-version') == '1.1':
            home_page.select_org(self.testsetup.org)
        assert home_page.is_dialog_cleared

        dashboard = self.katello.load_page('Dashboard')
        assert dashboard.is_tab_selected('dashboard')
        assert dashboard.is_dashboard_dropbutton_present
        assert dashboard.is_dashboard_subscriptions_present
        assert dashboard.is_dashboard_notifications_present

    def test_tab_selection(self):
        """
        Verify selecting different tabs
        """
        home_page = self.load_page('Home')

        home_page.login()
        assert home_page.is_successful
        if pytest.config.getvalue('project-version') == '1.1':
            home_page.select_org(self.testsetup.org)
        assert home_page.is_dialog_cleared

        home_page.click_tab('dashboard')
        assert home_page.is_tab_selected('dashboard')

        home_page.click_tab('content')
        assert home_page.is_tab_selected('content')

        home_page.click_tab('systems')
        assert home_page.is_tab_selected('systems')
