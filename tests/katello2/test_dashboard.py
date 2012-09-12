#!/usr/bin/env python

import pytest
import apps
import time
from tests.katello2 import Katello_Test

@pytest.mark.nondestructive
class TestDashboard(Katello_Test):

    def test_dashboard_present(self):
        """
        Verify dashboard page contains key elements.
        """
        home_page = self.katello.load_page('Home')

        home_page.login()
        assert home_page.is_dialog_cleared

        home_page.header.click_switcher()
        assert home_page.header.is_org_list_present

        home_page.header.select_org_from_switcher("ACME_Corporation")
        assert not home_page.header.is_org_list_present
        assert home_page.header.get_text_from_switcher == "ACME_Corporation"

        dashboard = self.katello.load_page('Dashboard')
        assert dashboard.is_tab_selected('dashboard')
        assert dashboard.is_dashboard_dropbutton_present
        assert dashboard.is_dashboard_subscriptions_present
        assert dashboard.is_dashboard_notifications_present

        # TODO - inspect subscription pane
        # TODO - inspect available errata pane
        # TODO - inspect notification pane
