#!/usr/bin/env python

import pytest
import apps
import logging
from data.large_dataset import Admin
from data.assert_response import *
from tests.aeolus2 import Aeolus_Test
import time

class TestNav(Aeolus_Test):

    @pytest.mark.template
    @pytest.mark.saucelabs
    def test_login_and_nav(self, mozwebqa):
        '''
        Login and cycle through select pages to test browser rendering

        Page views:
        users, new users, single user, edit user,
        user groups, new user group, single user group, edit user group,
        clouds, new cloud, single cloud, edit cloud,
        cloud resource zone, new cloud zone, single cloud zone, edit cloud zone,
        permissions, new permissions,
        images, new image,
        catalogs, new catalog, single catalog, edit catalog,
        realms, new realm,
        hwp, new hwp, single hwp, edit hwp,
        providers, new provider, single provider, edit provider,
        settings, logs, logout
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()

        time.sleep(15)

        workflow = ['users', 'users/new', 'users/1', 'users/1/edit',
                    'user_groups', 'user_groups/new', 'user_groups/1', 
                    'user_groups/1/edit', 'pool_families', 'pool_families/new',
                    'pool_families/1', 'pool_families/1/edit', 'pools', 
                    'pools/new', 'pools/1', 'pools/1/edit', 
                    'permissions', 'permissions/new', 
                    'images', 'images/new?environment=1', 'catalogs', 
                    'catalogs/new', 'catalogs/1', 'catalogs/1/edit',
                    'realms', 'realms/new', 'hardware_profiles',
                    'hardware_profiles/new', 'hardware_profiles/1',
                    'hardware_profiles/1/edit', 'providers', 'providers/new',
                    'providers/1', 'providers/1/edit',
                    'settings', 'logs', 'logout']
        for view in workflow:
            page.go_to_page_view(view)
            time.sleep(1)

    @pytest.mark.saucelabs
    def test_error_pages(self, mozwebqa):
        '''
        Login and cycle through known error pages:
        400 (bad request), 403 (forbidden), 404 (not found)
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()

        workflow = ['%400_bad_request%', '404_not_found', 
        'users/1/unknown_action', 'logout', 'users/403_forbidden', 
        '404_not_found']
        for view in workflow:
            page.go_to_page_view(view)
            time.sleep(2)

    def test_sauce_debug(self, mozwebqa):
        page = self.aeolus.load_page('Aeolus')
        page.login()
        self.wait_for_title("CloudForms Cloud Engine")
        assert page.page_title == "CloudForms Cloud Engine"
        page.go_to_page_view('images')
        page.go_to_page_view('logout')
