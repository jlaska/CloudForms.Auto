#!/usr/bin/env python

import pytest
import apps
import logging
from data.large_dataset import Admin
from data.assert_response import *
from tests.aeolus2 import Aeolus_Test

class TestNav(Aeolus_Test):

    @pytest.mark.template
    @pytest.mark.saucelabs
    def test_login_and_nav(self):
        '''
        Login and cycle through select pages
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()

        workflow = ['users', 'pool_families', 'catalogs', 'providers',\
                    'settings', 'logout']
        for view in workflow:
            page.go_to_page_view(view)
            logging.info('nav to page %s' % view)
