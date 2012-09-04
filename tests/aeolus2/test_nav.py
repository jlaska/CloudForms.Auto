#!/usr/bin/env python

import pytest
import apps

def setup_module(module):
    test_setup = pytest.config.pluginmanager.getplugin("mozwebqa")
    module.TestAeolus.aeolus = apps.initializeProduct(test_setup.TestSetup)

class TestAeolus(object):

    @pytest.mark.demo
    def test_login_and_nav(self):
        '''
        Login and navigate to random pages
        '''

        # Login
        home = self.aeolus.load_page('Home')
        home.login()

        # Access different views
        workflow = ['users', 'pool_families', 'catalogs', 'providers', 'settings', 'logout']
        for view in workflow:
            home.go_to_page_view(view)
