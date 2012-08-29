#!/usr/bin/env python

import pytest
import apps
import time

@pytest.mark.nondestructive
class TestDashboard:

    def test_dashboard_present(self, mozwebqa):
        """
        Verify dashboard page contains key elements.
        """
        katello = apps.getProductClass(mozwebqa.project)(mozwebqa)
        home_page = katello.load_page('Home')

        home_page.login()
        assert home_page.is_successful
        assert home_page.is_dialog_cleared

        home_page.header.click_switcher()
        assert home_page.header.is_org_list_present

        home_page.header.select_org_from_switcher("redhat")
        assert not home_page.header.is_org_list_present
        assert home_page.header.get_text_from_switcher == "redhat"

        dashboard = katello.load_page('Dashboard')
        assert dashboard.is_dashboard_tab_selected
        assert dashboard.is_dashboard_dropbutton_present
        assert dashboard.is_dashboard_subscriptions_present
        assert dashboard.is_dashboard_notifications_present

        # TODO - inspect subscription pane
        # TODO - inspect available errata pane
        # TODO - inspect notification pane
