#!/usr/bin/env python

import pytest
import apps


class TestAeolus(object):

    @pytest.mark.demo
    def test_login_and_nav(self, mozwebqa):
        '''
        Login and navigate to random pages
        '''

        # aeolus = aeolus.Conductor(mozwebqa)
        aeolus = apps.getProductClass('aeolus')(mozwebqa)

        # Login
        home = aeolus.load_page('Home')
        home.login()

        # Access different views
        workflow = ['users', 'pool_families', 'catalogs', 'providers', 'settings', 'logout']
        for view in workflow:
            home.go_to_page_view(view)
